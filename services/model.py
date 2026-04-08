import logging
from langchain_core.messages import HumanMessage
from langgraph.graph import MessagesState, StateGraph, END
from langgraph.prebuilt import ToolNode
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type

from services.llm_client import get_model, get_tool, get_pydantic_class

logger = logging.getLogger(__name__)

INDEX_TO_CLASS = {0: "VOC", 1: "ROC", 2: "FD", 3: "TD"}
PREFIX_TO_CLASS = {"VOC": "VOC", "ROC": "ROC", "FD": "FD", "TD": "TD"}


def _build_graph(Pydantic_Object):
    model = get_model()
    tool = get_tool()
    model_with_tools = model.bind_tools([tool])
    model_with_structured_output = model.with_structured_output(Pydantic_Object)

    class AgentState(MessagesState):
        final_response: Pydantic_Object

    def call_model(state: AgentState):
        response = model_with_tools.invoke(state["messages"])
        return {"messages": [response]}

    def respond(state: AgentState):
        response = model_with_structured_output.invoke(
            [HumanMessage(content=state["messages"][-2].content)]
        )
        return {"final_response": response}

    def should_continue(state: AgentState):
        last_message = state["messages"][-1]
        return "respond" if not last_message.tool_calls else "continue"

    workflow = StateGraph(AgentState)
    workflow.add_node("agent", call_model)
    workflow.add_node("respond", respond)
    workflow.add_node("tools", ToolNode([tool]))
    workflow.set_entry_point("agent")
    workflow.add_conditional_edges("agent", should_continue, {"continue": "tools", "respond": "respond"})
    workflow.add_edge("tools", "agent")
    workflow.add_edge("respond", END)
    return workflow.compile()


@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=2, max=30),
    retry=retry_if_exception_type(RuntimeError),
    reraise=True,
)
def openmodel(client_business_requirement: str, wricef_type: str) -> dict:
    prefix = client_business_requirement.split(" ")[0] if client_business_requirement else ""
    class_name = PREFIX_TO_CLASS.get(prefix)
    if not class_name:
        raise ValueError(f"Business requirement must start with one of: {', '.join(PREFIX_TO_CLASS.keys())}")

    Pydantic_Object = get_pydantic_class(wricef_type, class_name)
    graph = _build_graph(Pydantic_Object)

    logger.info("Invoking LLM graph for wricefType=%s class=%s", wricef_type, class_name)
    result = graph.invoke(input={"messages": [("human", client_business_requirement)]})
    return result["final_response"].dict()


@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=2, max=30),
    retry=retry_if_exception_type(RuntimeError),
    reraise=True,
)
def openmodel_regeneration(
    client_business_requirement: str,
    wricefType: str,
    previous_response: str,
    current_response: str,
    index_value: int,
) -> dict:
    class_name = INDEX_TO_CLASS.get(index_value)
    if not class_name:
        raise ValueError(f"Invalid index_value {index_value}. Must be 0-3.")

    Pydantic_Object = get_pydantic_class(wricefType, class_name)
    graph = _build_graph(Pydantic_Object)

    human_input = (
        f"Client Business Requirement: {client_business_requirement} "
        f"Previous Response: {previous_response} "
        f"Current Response: {current_response} "
        f"Based on the Client Business Requirement & Previous Response Enhance Current Response"
    )

    logger.info("Invoking regeneration LLM graph for wricefType=%s class=%s", wricefType, class_name)
    result = graph.invoke(input={"messages": [("human", human_input)]})
    return result["final_response"].dict()

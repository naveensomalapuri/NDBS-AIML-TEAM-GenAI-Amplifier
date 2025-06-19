import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_openai import AzureChatOpenAI
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_core.messages import HumanMessage
from typing import Annotated
from typing_extensions import TypedDict
from pydantic import BaseModel, Field
from langgraph.graph import MessagesState, StateGraph, END
from langgraph.prebuilt import ToolNode
from langchain_tavily import TavilySearch
import importlib


def openmodel(client_business_requirement, wricefType):
    """
    Process business requirements using LLM and structured output
    
    Args:
        client_business_requirement (str): The business requirement text
        client_name (str): The name of the client
        
    Returns:
        dict: Structured response as a dictionary
    """
    # ------------------------------------------------------------------------------
    # Load Environment Variables
    # ------------------------------------------------------------------------------
    load_dotenv()

    # Retrieve and validate the Tavily API key
    tavily_api_key = os.getenv("TAVILY_API_KEY")
    if tavily_api_key is None:
        raise ValueError("TAVILY_API_KEY not found in the environment. Please add it to your .env file.")
    
    os.environ["TAVILY_API_KEY"] = tavily_api_key

    # Retrieve Azure OpenAI credentials
    api_key = os.getenv("AZURE_OPENAI_API_KEY")
    api_base = os.getenv("AZURE_OPENAI_ENDPOINT")
    api_version = os.getenv("OPENAI_API_VERSION")
    deployment = os.getenv("AZURE_OPENAI_DEPLOYMENT")
    
    # Validate all required environment variables are present
    if not api_key or not api_base or not api_version or not deployment:
        missing_vars = []
        if not api_key: missing_vars.append("AZURE_OPENAI_API_KEY")
        if not api_base: missing_vars.append("AZURE_OPENAI_ENDPOINT") 
        if not api_version: missing_vars.append("OPENAI_API_VERSION")
        if not deployment: missing_vars.append("AZURE_OPENAI_DEPLOYMENT")
        
        raise ValueError(f"Missing required environment variables: {', '.join(missing_vars)}")

    # ------------------------------------------------------------------------------
    # Initialize the Tavily Search Tool
    # ------------------------------------------------------------------------------
    tool = TavilySearch(
        max_results=5,
        topic="general",
        search_depth="advanced",
    )

    # ------------------------------------------------------------------------------
    # Dynamically Import Pydantic Classes Based on wricefType
    # ------------------------------------------------------------------------------
    try:
        # Use wricefType as-is (case-sensitive)
        module_path = f"services.{wricefType}"
        module = importlib.import_module(module_path)

        # Choose the class based on the business requirement
        if "VOC" in client_business_requirement:
            Pydantic_Object = getattr(module, "VOC")
        elif "ROC" in client_business_requirement:
            Pydantic_Object = getattr(module, "ROC")
        elif "FD" in client_business_requirement:
            Pydantic_Object = getattr(module, "FD")
        elif "TD" in client_business_requirement:
            Pydantic_Object = getattr(module, "TD")
        else:
            raise ValueError("Business requirement must contain one of: VOC, ROC, FD, TD.")

    except ModuleNotFoundError:
        raise ImportError(f"Module 'services.{wricefType}' not found.")
    except AttributeError as e:
        raise ImportError(f"Expected class not found in module 'services.{wricefType}': {e}")


    # ------------------------------------------------------------------------------
    # Define the Agent State for the Conversational Workflow
    # ------------------------------------------------------------------------------
    class AgentState(MessagesState):
        """
        Represents the current conversation state.
        Inherits a list of chat messages and includes a final structured response.
        """
        final_response: Pydantic_Object

    # ------------------------------------------------------------------------------
    # Initialize the Azure OpenAI Chat Model with proper parameters
    # ------------------------------------------------------------------------------
    try:
        model = AzureChatOpenAI(
            api_key=api_key,                  
            azure_endpoint=api_base,          
            api_version=api_version,        
            azure_deployment=deployment,
            model_name=deployment,  # Explicitly set model name to be the same as deployment
            temperature=0,
            # Use model_kwargs instead of extra_headers
            model_kwargs={"extra_headers": {"x-ms-model-mesh-model-name": deployment}},
        )
    except Exception as e:
        # Provide a more helpful error message
        raise ValueError(f"Failed to initialize Azure OpenAI model: {str(e)}. Verify your Azure OpenAI credentials and deployment.")

    # Bind the TavilySearch tool to the chat model
    model_with_tools = model.bind_tools([tool])
    
    # Configure the model to return structured output
    model_with_structured_output = model.with_structured_output(Pydantic_Object)

    # ------------------------------------------------------------------------------
    # Define Functions for the Conversational Workflow
    # ------------------------------------------------------------------------------
    def call_model(state: AgentState):
        """
        Invokes the chat model using the current list of messages in the conversation state.
        """
        try:
            response = model_with_tools.invoke(state["messages"])
            return {"messages": [response]}
        except Exception as e:
            raise RuntimeError(f"Error calling the model: {str(e)}")

    def respond(state: AgentState):
        """
        Generates the final structured response.
        """
        try:
            response = model_with_structured_output.invoke(
                [HumanMessage(content=state["messages"][-2].content)]
            )
            return {"final_response": response}
        except Exception as e:
            raise RuntimeError(f"Error generating structured response: {str(e)}")

    def should_continue(state: AgentState):
        """
        Determines if the workflow should continue tool invocation or generate the final response.
        """
        messages = state["messages"]
        last_message = messages[-1]
        return "respond" if not last_message.tool_calls else "continue"

    # ------------------------------------------------------------------------------
    # Build the StateGraph Workflow
    # ------------------------------------------------------------------------------
    workflow = StateGraph(AgentState)

    # Define nodes representing stages of the workflow
    workflow.add_node("agent", call_model)
    workflow.add_node("respond", respond)
    workflow.add_node("tools", ToolNode([tool]))

    # Set the entry point to the workflow
    workflow.set_entry_point("agent")

    # Conditional edge based on whether to invoke a tool or to generate a final response
    workflow.add_conditional_edges(
        "agent",
        should_continue,
        {
            "continue": "tools",
            "respond": "respond",
        },
    )

    # Loop back to the agent node after using a tool
    workflow.add_edge("tools", "agent")
    # Final node connecting to the end of the workflow
    workflow.add_edge("respond", END)
    graph = workflow.compile()

    # ------------------------------------------------------------------------------
    # Invoke the Workflow with User Input
    # ------------------------------------------------------------------------------
    try:
        # Process the user's input and get structured response
        Human_Input = client_business_requirement
        result = graph.invoke(input={"messages": [("human", Human_Input)]})
        answer = result["final_response"]
        
        # Convert the structured response to a dictionary
        answer_dict = answer.dict()
        return answer_dict
    except Exception as e:
        # Provide a helpful error message
        error_msg = f"Error processing business requirement: {str(e)}"
        print(error_msg)
        raise RuntimeError(error_msg)







# def openmodel_regeneration(client_business_requirement, wricefType, previous_response, current_response, index_value):
#     # Google Colab specific import for handling user data storage (if needed)
#     # In this updated version, we use the .env file for keys.
#     # from google.colab import userdata

#     # ------------------------------------------------------------------------------
#     # 3. Load Environment Variables from .env File
#     # ------------------------------------------------------------------------------
#     # Load variables from a .env file located in the same directory.
#     load_dotenv()

#     # Retrieve the Tavily API key from the environment variables
#     tavily_api_key = os.getenv("TAVILY_API_KEY")
#     if tavily_api_key is None:
#         raise ValueError("TAVILY_API_KEY not found in the environment. Please add it to your .env file.")

#     # Now you can use tavily_api_key as needed, for example:
#     os.environ["TAVILY_API_KEY"] = tavily_api_key


#     # ------------------------------------------------------------------------------
#     # 4. Initialize the Tavily Search Tool
#     # ------------------------------------------------------------------------------
#     # Create an instance of the TavilySearch tool with the desired parameters.
#     tool = TavilySearch(
#         max_results=5,
#         topic="general",
#         search_depth="advanced",
#         # Optional parameters (uncomment if necessary):
#         # include_answer=False,
#         # include_raw_content=False,
#         # include_images=False,
#         # include_image_descriptions=False,
#         # time_range="day",
#         # include_domains=None,
#         # exclude_domains=None
#     )
#     # The tool can be invoked as needed (e.g., tool.invoke({"query": "your query"})).

#     # ------------------------------------------------------------------------------
#     # 5. Define the Structured Model for Functional Design Requirements
#     # ------------------------------------------------------------------------------



#     # ------------------------------------------------------------------------------
#     # Dynamically Import Pydantic Class Based on index_value
#     # ------------------------------------------------------------------------------

#     # Map of index values to class names
#     index_to_class_name = {
#         0: "VOC",
#         1: "ROC",
#         2: "FD",
#         3: "TD"
#     }

#     try:
#         # Get the class name from index
#         class_name = index_to_class_name.get(index_value)
#         if class_name is None:
#             raise ValueError("Invalid index value. Must be 0 (VOC), 1 (ROC), 2 (FD), or 3 (TD).")

#         # Dynamically import the module using wricefType
#         module_path = f"services.{wricefType}"
#         module = importlib.import_module(module_path)

#         # Dynamically get the Pydantic class from the module
#         Pydantic_Object = getattr(module, class_name)

#     except ModuleNotFoundError:
#         raise ImportError(f"Module 'services.{wricefType}' not found.")
#     except AttributeError as e:
#         raise ImportError(f"Expected class '{class_name}' not found in module 'services.{wricefType}': {e}")


#     # ------------------------------------------------------------------------------
#     # 6. Define the Agent State for the Conversational Workflow
#     # ------------------------------------------------------------------------------
#     class AgentState(MessagesState):
#         """
#         Represents the current conversation state.
#         Inherits a list of chat messages and includes a final structured response.
#         """
#         final_response: Pydantic_Object

#     # ------------------------------------------------------------------------------
#     # 7. Initialize the Chat Model and Bind Tools
#     # ------------------------------------------------------------------------------
#     # Retrieve the GROQ API key from environment variables.
#     groq_api_key = os.environ.get("GROQ_API_KEY")
#     # Initialize the ChatGroq model with the provided API key and specific model name.
#     model = ChatGroq(groq_api_key=groq_api_key, model_name="llama-3.3-70b-versatile")

#     # Bind the TavilySearch tool to the chat model.
#     model_with_tools = model.bind_tools([tool])
#     # Configure the model to return structured output following the Pydantic_Object model.
#     model_with_structured_output = model.with_structured_output(Pydantic_Object)

#     # ------------------------------------------------------------------------------
#     # 8. Define Functions for the Conversational Workflow
#     # ------------------------------------------------------------------------------
#     def call_model(state: AgentState):
#         """
#         Invokes the chat model using the current list of messages in the conversation state.
        
#         Args:
#             state (AgentState): The current conversation state.
            
#         Returns:
#             dict: A dictionary containing a new list of messages from the model.
#         """
#         response = model_with_tools.invoke(state["messages"])
#         return {"messages": [response]}

#     def respond(state: AgentState):
#         """
#         Generates the final structured response.
        
#         Converts a previous tool response into a HumanMessage and invokes the model to produce the final output.
        
#         Args:
#             state (AgentState): The current conversation state.
            
#         Returns:
#             dict: A dictionary containing the final structured response.
#         """
#         response = model_with_structured_output.invoke(
#             [HumanMessage(content=state["messages"][-2].content)]
#         )
#         return {"final_response": response}

#     def should_continue(state: AgentState):
#         """
#         Determines if the workflow should continue tool invocation or generate the final response.
        
#         Args:
#             state (AgentState): The conversation state.
        
#         Returns:
#             str: "continue" if tool calls exist; otherwise "respond".
#         """
#         messages = state["messages"]
#         last_message = messages[-1]
#         return "respond" if not last_message.tool_calls else "continue"

#     # ------------------------------------------------------------------------------
#     # 9. Build the StateGraph Workflow
#     # ------------------------------------------------------------------------------
#     workflow = StateGraph(AgentState)

#     # Define nodes representing stages of the workflow.
#     workflow.add_node("agent", call_model)
#     workflow.add_node("respond", respond)
#     workflow.add_node("tools", ToolNode([tool]))

#     # Set the entry point to the workflow.
#     workflow.set_entry_point("agent")

#     # Conditional edge based on whether to invoke a tool or to generate a final response.
#     workflow.add_conditional_edges(
#         "agent",
#         should_continue,
#         {
#             "continue": "tools",
#             "respond": "respond",
#         },
#     )

#     # Loop back to the agent node after using a tool.
#     workflow.add_edge("tools", "agent")
#     # Final node connecting to the end of the workflow.
#     workflow.add_edge("respond", END)
#     graph = workflow.compile()

#     # ------------------------------------------------------------------------------
#     # 10. (Optional) Display the Workflow Graph
#     # ------------------------------------------------------------------------------
#     # try:
#     #     display(Image(graph.get_graph().draw_mermaid_png()))
#     # except Exception:
#     #     pass

#     # ------------------------------------------------------------------------------
#     # 11. Invoke the Workflow with User Input
#     # ------------------------------------------------------------------------------
#     # Prompt for user input (query or voice of the customer).
#     Human_Input = "Client Business Requirement : " + client_business_requirement + "Privous Response : " + previous_response + "Current Response : " + current_response + "Based on the Client Business Requirement & Previous Response Enhance Current Response"
#     print(Human_Input)
#     answer = graph.invoke(input={"messages": [("human", Human_Input)]})["final_response"]

#     # Print the final structured response.
#     print("\nStructured Final Response:")
#     print(answer)

#     # Optionally, convert the structured response to a dictionary.
#     answer_dict = answer.dict()
#     print("\nResponse as a Dictionary:")
#     print(answer_dict)
#     return answer_dict



def openmodel_regeneration(client_business_requirement, wricefType, previous_response, current_response, index_value):
    """
    Regenerate and enhance business requirements using Azure OpenAI and structured output
    
    Args:
        client_business_requirement (str): The business requirement text
        wricefType (str): The type of WRICE framework
        previous_response (str): The previous response to compare against
        current_response (str): The current response to enhance
        index_value (int): Index to determine which Pydantic class to use (0=VOC, 1=ROC, 2=FD, 3=TD)
        
    Returns:
        dict: Enhanced structured response as a dictionary
    """
    # ------------------------------------------------------------------------------
    # Load Environment Variables
    # ------------------------------------------------------------------------------
    load_dotenv()

    # Retrieve and validate the Tavily API key
    tavily_api_key = os.getenv("TAVILY_API_KEY")
    if tavily_api_key is None:
        raise ValueError("TAVILY_API_KEY not found in the environment. Please add it to your .env file.")
    
    os.environ["TAVILY_API_KEY"] = tavily_api_key

    # Retrieve Azure OpenAI credentials
    api_key = os.getenv("AZURE_OPENAI_API_KEY")
    api_base = os.getenv("AZURE_OPENAI_ENDPOINT")
    api_version = os.getenv("OPENAI_API_VERSION")
    deployment = os.getenv("AZURE_OPENAI_DEPLOYMENT")
    
    # Validate all required environment variables are present
    if not api_key or not api_base or not api_version or not deployment:
        missing_vars = []
        if not api_key: missing_vars.append("AZURE_OPENAI_API_KEY")
        if not api_base: missing_vars.append("AZURE_OPENAI_ENDPOINT") 
        if not api_version: missing_vars.append("OPENAI_API_VERSION")
        if not deployment: missing_vars.append("AZURE_OPENAI_DEPLOYMENT")
        
        raise ValueError(f"Missing required environment variables: {', '.join(missing_vars)}")

    # ------------------------------------------------------------------------------
    # Initialize the Tavily Search Tool
    # ------------------------------------------------------------------------------
    tool = TavilySearch(
        max_results=5,
        topic="general",
        search_depth="advanced",
    )

    # ------------------------------------------------------------------------------
    # Dynamically Import Pydantic Class Based on index_value
    # ------------------------------------------------------------------------------
    # Map of index values to class names
    index_to_class_name = {
        0: "VOC",
        1: "ROC",
        2: "FD",
        3: "TD"
    }

    try:
        # Get the class name from index
        class_name = index_to_class_name.get(index_value)
        if class_name is None:
            raise ValueError("Invalid index value. Must be 0 (VOC), 1 (ROC), 2 (FD), or 3 (TD).")

        # Dynamically import the module using wricefType
        module_path = f"services.{wricefType}"
        module = importlib.import_module(module_path)

        # Dynamically get the Pydantic class from the module
        Pydantic_Object = getattr(module, class_name)

    except ModuleNotFoundError:
        raise ImportError(f"Module 'services.{wricefType}' not found.")
    except AttributeError as e:
        raise ImportError(f"Expected class '{class_name}' not found in module 'services.{wricefType}': {e}")

    # ------------------------------------------------------------------------------
    # Define the Agent State for the Conversational Workflow
    # ------------------------------------------------------------------------------
    class AgentState(MessagesState):
        """
        Represents the current conversation state.
        Inherits a list of chat messages and includes a final structured response.
        """
        final_response: Pydantic_Object

    # ------------------------------------------------------------------------------
    # Initialize the Azure OpenAI Chat Model with proper parameters
    # ------------------------------------------------------------------------------
    try:
        model = AzureChatOpenAI(
            api_key=api_key,                  
            azure_endpoint=api_base,          
            api_version=api_version,        
            azure_deployment=deployment,
            model_name=deployment,  # Explicitly set model name to be the same as deployment
            temperature=0,
            # Use model_kwargs instead of extra_headers
            model_kwargs={"extra_headers": {"x-ms-model-mesh-model-name": deployment}},
        )
    except Exception as e:
        # Provide a more helpful error message
        raise ValueError(f"Failed to initialize Azure OpenAI model: {str(e)}. Verify your Azure OpenAI credentials and deployment.")

    # Bind the TavilySearch tool to the chat model
    model_with_tools = model.bind_tools([tool])
    
    # Configure the model to return structured output
    model_with_structured_output = model.with_structured_output(Pydantic_Object)

    # ------------------------------------------------------------------------------
    # Define Functions for the Conversational Workflow
    # ------------------------------------------------------------------------------
    def call_model(state: AgentState):
        """
        Invokes the chat model using the current list of messages in the conversation state.
        
        Args:
            state (AgentState): The current conversation state.
            
        Returns:
            dict: A dictionary containing a new list of messages from the model.
        """
        try:
            response = model_with_tools.invoke(state["messages"])
            return {"messages": [response]}
        except Exception as e:
            raise RuntimeError(f"Error calling the model: {str(e)}")

    def respond(state: AgentState):
        """
        Generates the final structured response.
        
        Converts a previous tool response into a HumanMessage and invokes the model to produce the final output.
        
        Args:
            state (AgentState): The current conversation state.
            
        Returns:
            dict: A dictionary containing the final structured response.
        """
        try:
            response = model_with_structured_output.invoke(
                [HumanMessage(content=state["messages"][-2].content)]
            )
            return {"final_response": response}
        except Exception as e:
            raise RuntimeError(f"Error generating structured response: {str(e)}")

    def should_continue(state: AgentState):
        """
        Determines if the workflow should continue tool invocation or generate the final response.
        
        Args:
            state (AgentState): The conversation state.
        
        Returns:
            str: "continue" if tool calls exist; otherwise "respond".
        """
        messages = state["messages"]
        last_message = messages[-1]
        return "respond" if not last_message.tool_calls else "continue"

    # ------------------------------------------------------------------------------
    # Build the StateGraph Workflow
    # ------------------------------------------------------------------------------
    workflow = StateGraph(AgentState)

    # Define nodes representing stages of the workflow
    workflow.add_node("agent", call_model)
    workflow.add_node("respond", respond)
    workflow.add_node("tools", ToolNode([tool]))

    # Set the entry point to the workflow
    workflow.set_entry_point("agent")

    # Conditional edge based on whether to invoke a tool or to generate a final response
    workflow.add_conditional_edges(
        "agent",
        should_continue,
        {
            "continue": "tools",
            "respond": "respond",
        },
    )

    # Loop back to the agent node after using a tool
    workflow.add_edge("tools", "agent")
    # Final node connecting to the end of the workflow
    workflow.add_edge("respond", END)
    graph = workflow.compile()

    # ------------------------------------------------------------------------------
    # Invoke the Workflow with User Input
    # ------------------------------------------------------------------------------
    try:
        # Construct the enhanced prompt for regeneration
        Human_Input = (
            f"Client Business Requirement: {client_business_requirement} "
            f"Previous Response: {previous_response} "
            f"Current Response: {current_response} "
            f"Based on the Client Business Requirement & Previous Response Enhance Current Response"
        )
        
        print(Human_Input)
        
        # Process the input and get structured response
        result = graph.invoke(input={"messages": [("human", Human_Input)]})
        answer = result["final_response"]

        # Print the final structured response
        print("\nStructured Final Response:")
        print(answer)

        # Convert the structured response to a dictionary
        answer_dict = answer.dict()
        print("\nResponse as a Dictionary:")
        print(answer_dict)
        
        return answer_dict
        
    except Exception as e:
        # Provide a helpful error message
        error_msg = f"Error processing regeneration request: {str(e)}"
        print(error_msg)
        raise RuntimeError(error_msg)
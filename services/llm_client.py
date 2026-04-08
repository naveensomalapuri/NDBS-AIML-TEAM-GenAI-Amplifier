import os
import importlib
import logging
from dotenv import load_dotenv
from langchain_openai import AzureChatOpenAI
from langchain_tavily import TavilySearch

load_dotenv()

logger = logging.getLogger(__name__)

ALLOWED_WRICEF_TYPES = {"Workflow", "Reports", "Interface", "Conversions", "Enhancements", "Forms", "General"}

_azure_model: AzureChatOpenAI = None
_tavily_tool: TavilySearch = None


def get_model() -> AzureChatOpenAI:
    global _azure_model
    if _azure_model is None:
        api_key = os.getenv("AZURE_OPENAI_API_KEY")
        api_base = os.getenv("AZURE_OPENAI_ENDPOINT")
        api_version = os.getenv("OPENAI_API_VERSION")
        deployment = os.getenv("AZURE_OPENAI_DEPLOYMENT")

        missing = [k for k, v in {
            "AZURE_OPENAI_API_KEY": api_key,
            "AZURE_OPENAI_ENDPOINT": api_base,
            "OPENAI_API_VERSION": api_version,
            "AZURE_OPENAI_DEPLOYMENT": deployment,
        }.items() if not v]

        if missing:
            raise ValueError(f"Missing required environment variables: {', '.join(missing)}")

        _azure_model = AzureChatOpenAI(
            api_key=api_key,
            azure_endpoint=api_base,
            api_version=api_version,
            azure_deployment=deployment,
            model_name=deployment,
            temperature=0,
            model_kwargs={"extra_headers": {"x-ms-model-mesh-model-name": deployment}},
            timeout=120,
            max_retries=3,
        )
    return _azure_model


def get_tool() -> TavilySearch:
    global _tavily_tool
    if _tavily_tool is None:
        tavily_api_key = os.getenv("TAVILY_API_KEY")
        if not tavily_api_key:
            raise ValueError("TAVILY_API_KEY not found in environment.")
        os.environ["TAVILY_API_KEY"] = tavily_api_key
        _tavily_tool = TavilySearch(max_results=5, topic="general", search_depth="advanced")
    return _tavily_tool


def validate_wricef_type(wricef_type: str) -> str:
    if wricef_type not in ALLOWED_WRICEF_TYPES:
        raise ValueError(
            f"Invalid wricefType '{wricef_type}'. Must be one of: {', '.join(sorted(ALLOWED_WRICEF_TYPES))}"
        )
    return wricef_type


def get_pydantic_class(wricef_type: str, class_name: str):
    validate_wricef_type(wricef_type)
    try:
        module = importlib.import_module(f"services.{wricef_type}")
        return getattr(module, class_name)
    except ModuleNotFoundError:
        raise ImportError(f"Module 'services.{wricef_type}' not found.")
    except AttributeError as e:
        raise ImportError(f"Class '{class_name}' not found in 'services.{wricef_type}': {e}")

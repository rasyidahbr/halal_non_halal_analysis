"""
Module for handling LlamaIndex operations for document retrieval and chat.
"""
import streamlit as st
from pathlib import Path
from typing import Tuple, Optional, Any

# Try to import llama_index, but make it optional
try:
    from llama_index import VectorStoreIndex, ServiceContext
    from llama_index.chat_engine import CondenseQuestionChatEngine
    from llama_index.llms import OpenAI
    from llama_index import StorageContext, load_index_from_storage
    LLAMA_INDEX_AVAILABLE = True
except ImportError:
    LLAMA_INDEX_AVAILABLE = False
    # Create placeholder classes to avoid errors
    class VectorStoreIndex:
        pass
    class ServiceContext:
        pass
    class CondenseQuestionChatEngine:
        pass


@st.cache_resource(show_spinner=False)
def load_index_and_context(
    persist_dir: str, 
    model_name: str, 
    temperature: float, 
    context_window: int, 
    system_prompt: str
) -> Tuple[Any, Any]:
    """
    Load the LlamaIndex index and service context.
    
    Args:
        persist_dir (str): Directory where the index is persisted
        model_name (str): OpenAI model name to use
        temperature (float): Temperature setting for the model
        context_window (int): Context window size
        system_prompt (str): System prompt for the model
        
    Returns:
        Tuple[Any, Any]: Tuple of (index, service context)
        
    Raises:
        ImportError: If LlamaIndex is not available
    """
    if not LLAMA_INDEX_AVAILABLE:
        raise ImportError(
            "LlamaIndex is required for this feature. "
            "Please install it with: pip install llama-index"
        )
        
    with st.spinner(text="Loading – hang tight! This should take 1-2 minutes."):
        # Rebuild the storage context
        storage_context = StorageContext.from_defaults(persist_dir=persist_dir)

        # Load the index
        index = load_index_from_storage(storage_context)

        # Load the model 
        gpt_context = ServiceContext.from_defaults(
            llm=OpenAI(model=model_name, temperature=temperature), 
            context_window=context_window, 
            system_prompt=system_prompt
        )
        
        return index, gpt_context


def get_chat_engine(index: Any, service_context: Any) -> Any:
    """
    Create a chat engine from an index and service context.
    
    Args:
        index: LlamaIndex vector store index
        service_context: Service context for the model
        
    Returns:
        Any: Chat engine for conversational QA
        
    Raises:
        ImportError: If LlamaIndex is not available
    """
    if not LLAMA_INDEX_AVAILABLE:
        raise ImportError(
            "LlamaIndex is required for this feature. "
            "Please install it with: pip install llama-index"
        )
        
    query_engine = index.as_query_engine(service_context=service_context)
    chat_engine = CondenseQuestionChatEngine.from_defaults(query_engine, verbose=True)
    return chat_engine
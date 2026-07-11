import config_cache
from functools import lru_cache
import os

from langchain_classic.chains import create_retrieval_chain
from langchain_classic.chains.combine_documents import (
    create_stuff_documents_chain
)

from app.state_schema import GuideState
from app.retrievers.retrievers import get_retriever
from app.prompts.prompts import rcs_prompt
from langchain_groq import ChatGroq



###############################################################################
# Cache Resources Retriever
###############################################################################

@lru_cache(maxsize=10)
def get_resources_retriever(role: str):

    print(f"Loading Resources retriever for {role}")

    return get_retriever(
        collection_name="Resources_db",
        api_endpoint=os.getenv("ASTRA_ENDPOINT_RCS"),
        token=os.getenv("ASTRA_TOKEN_RCS"),
        role=role,
        k=8,
    )



###############################################################################
# Resources RAG Node
###############################################################################

def resources_RAG(state: GuideState):

    print("------ RESOURCES NODE ------")


    resources_retriever = get_resources_retriever(
        state.role
    )


    llm = ChatGroq(
        model=state.model,
        api_key=state.api_key,
        temperature=0,
    )


    document_chain = create_stuff_documents_chain(
        llm,
        rcs_prompt,
    )


    retrieval_chain = create_retrieval_chain(
        resources_retriever,
        document_chain,
    )


    result = retrieval_chain.invoke(
        {
            "input": state.question,
            "role": state.role,
        }
    )


    return {
        "rcs_response": result["answer"]
    }
import config_cache
from functools import lru_cache
import os

from langchain_classic.chains import create_retrieval_chain
from langchain_classic.chains.combine_documents import (
    create_stuff_documents_chain
)

from app.state_schema import GuideState
from app.retrievers.retrievers import get_retriever
from app.prompts.prompts import rm_prompt
from langchain_groq import ChatGroq



###############################################################################
# Cache Roadmap Retriever
###############################################################################

@lru_cache(maxsize=10)
def get_roadmap_retriever(role: str):

    print(f"Loading Roadmap retriever for {role}")

    return get_retriever(
        collection_name="Roadmap_db",
        api_endpoint=os.getenv("ASTRA_ENDPOINT_RM"),
        token=os.getenv("ASTRA_TOKEN_RM"),
        role=role,
        k=8,
    )



###############################################################################
# Roadmap RAG Node
###############################################################################

def rm_RAG(state: GuideState):

    print("------ ROADMAP NODE ------")


    roadmap_retriever = get_roadmap_retriever(
        state.role
    )


    llm = ChatGroq(
        model=state.model,
        api_key=state.api_key,
        temperature=0,
    )


    document_chain = create_stuff_documents_chain(
        llm,
        rm_prompt,
    )


    retrieval_chain = create_retrieval_chain(
        roadmap_retriever,
        document_chain,
    )


    result = retrieval_chain.invoke(
        {
            "input": state.question,
            "role": state.role,
        }
    )


    return {
        "rm_response": result["answer"]
    }
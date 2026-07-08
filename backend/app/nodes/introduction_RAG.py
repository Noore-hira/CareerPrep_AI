from functools import lru_cache
import os

from langchain_groq import ChatGroq
from langchain_classic.chains import create_retrieval_chain
from langchain_classic.chains.combine_documents import (
    create_stuff_documents_chain
)

from app.retrievers.retrievers import get_retriever
from app.state_schema import GuideState
from app.prompts.prompts import intro_prompt



###############################################################################
# Cache AstraDB Retriever
###############################################################################

@lru_cache(maxsize=10)
def get_intro_retriever(role: str):

    print(f"Loading Introduction retriever for {role}")

    return get_retriever(
        collection_name="Introduction_db",
        api_endpoint=os.getenv("ASTRA_DB_API_ENDPOINT"),
        token=os.getenv("ASTRA_DB_APPLICATION_TOKEN"),
        role=role,
        k=8,
    )



###############################################################################
# Introduction RAG Node
###############################################################################

def intro_RAG(state: GuideState):

    print("------ INTRODUCTION NODE ------")


    intro_retriever = get_intro_retriever(
        state.role
    )


    llm = ChatGroq(
        model=state.model,
        api_key=state.api_key,
        temperature=0,
    )


    document_chain = create_stuff_documents_chain(
        llm,
        intro_prompt,
    )


    retrieval_chain = create_retrieval_chain(
        intro_retriever,
        document_chain,
    )


    result = retrieval_chain.invoke(
        {
            "input": state.question,
            "role": state.role,
        }
    )


    return {
        "intro_response": result["answer"]
    }
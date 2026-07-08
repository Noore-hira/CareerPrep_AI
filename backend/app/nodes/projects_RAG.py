from functools import lru_cache
import os

from langchain_groq import ChatGroq
from langchain_classic.chains import create_retrieval_chain
from langchain_classic.chains.combine_documents import (
    create_stuff_documents_chain
)

from app.state_schema import GuideState
from app.retrievers.retrievers import get_retriever
from app.prompts.prompts import pj_prompt



###############################################################################
# Cache Projects Retriever
###############################################################################

@lru_cache(maxsize=10)
def get_projects_retriever(role: str):

    print(f"Loading Projects retriever for {role}")

    return get_retriever(
        collection_name="Projects_db",
        api_endpoint=os.getenv("ASTRA_ENDPOINT_PJ"),
        token=os.getenv("ASTRA_TOKEN_PJ"),
        role=role,
        k=10,
    )



###############################################################################
# Projects RAG Node
###############################################################################

def projects_RAG(state: GuideState):

    print("------ PROJECTS NODE ------")


    projects_retriever = get_projects_retriever(
        state.role
    )


    llm = ChatGroq(
        model=state.model,
        api_key=state.api_key,
        temperature=0,
    )


    document_chain = create_stuff_documents_chain(
        llm,
        pj_prompt,
    )


    retrieval_chain = create_retrieval_chain(
        projects_retriever,
        document_chain,
    )


    result = retrieval_chain.invoke(
        {
            "input": state.question,
            "role": state.role,
        }
    )


    return {
        "pj_response": result["answer"]
    }
import config_cache
from functools import lru_cache
import os

from langchain_groq import ChatGroq
from langchain_classic.chains import create_retrieval_chain
from langchain_classic.chains.combine_documents import (
    create_stuff_documents_chain,
)

from app.retrievers.retrievers import get_retriever
from app.prompts.prompts import iv_prompt
from app.state_schema import GuideState


###############################################################################
# Retriever Cache
###############################################################################

@lru_cache(maxsize=10)
def cached_retriever(role: str):

    print(f"Loading Interview retriever for {role}")

    return get_retriever(
        collection_name="Interview_db",
        api_endpoint=os.getenv("ASTRA_ENDPOINT_IV"),
        token=os.getenv("ASTRA_TOKEN_IV"),
        role=role,
        k=10,
    )


###############################################################################
# Interview Node
###############################################################################

def interview_RAG(state: GuideState):

    print("------ INTERVIEW QUESTIONS NODE ------")

    retriever = cached_retriever(state.role)

    llm = ChatGroq(
        model=state.model,
        api_key=state.api_key,
        temperature=0,
    )

    document_chain = create_stuff_documents_chain(
        llm,
        iv_prompt,
    )

    retrieval_chain = create_retrieval_chain(
        retriever,
        document_chain,
    )

    result = retrieval_chain.invoke(
        {
            "input": state.question,
            "role": state.role,
        }
    )

    return {
        "iv_response": result["answer"]
    }
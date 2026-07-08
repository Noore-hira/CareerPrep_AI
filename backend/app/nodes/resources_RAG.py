from langchain_groq import ChatGroq
from langchain_classic.chains import create_retrieval_chain
from langchain_classic.chains.combine_documents import create_stuff_documents_chain

from app.state_schema import GuideState
from app.retrievers.retrievers import get_retriever
from app.prompts.prompts import rcs_prompt

import os


def resources_RAG(state: GuideState):

    print("------ RESOURCES NODE ------")

    resources_retriever = get_retriever(
        "Resources_db",
        os.getenv("ASTRA_ENDPOINT_RCS"),
        os.getenv("ASTRA_TOKEN_RCS"),
        state.role,
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
from langchain_groq import ChatGroq
from langchain_classic.chains import create_retrieval_chain
from langchain_classic.chains.combine_documents import create_stuff_documents_chain

from app.state_schema import GuideState
from app.retrievers.retrievers import get_retriever
from app.prompts.prompts import rm_prompt

import os


def rm_RAG(state: GuideState):

    print("------ ROADMAP NODE ------")

    roadmap_retriever = get_retriever(
        "Roadmap_db",
        os.getenv("ASTRA_ENDPOINT_RM"),
        os.getenv("ASTRA_TOKEN_RM"),
        state.role,
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
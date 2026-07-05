from langchain_groq import ChatGroq
from app.state_schema import GuideState
from app.retrievers.retrievers import get_retriever
from langchain_classic.chains.combine_documents import create_stuff_documents_chain
from langchain_classic.chains import create_retrieval_chain
from app.prompts.prompts import pj_prompt
import os
from dotenv import load_dotenv

load_dotenv()
groq_api=os.getenv("GROQ_API")

def projects_RAG(state:GuideState):

    print("------ PROJECTS NODE ------")
    projects_retriever = get_retriever("Projects_db",os.getenv("ASTRA_ENDPOINT_PJ"),os.getenv("ASTRA_TOKEN_PJ"),state.role)
    llm=ChatGroq(model="groq/compound", api_key=groq_api)
    document_chain=create_stuff_documents_chain(llm,pj_prompt)
    retrieval_chain=create_retrieval_chain(projects_retriever,document_chain)
    result=retrieval_chain.invoke({"input": state.question ,"role":state.role})
    return {
        "pj_response": result["answer"]
    }
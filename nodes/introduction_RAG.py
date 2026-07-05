from langchain_groq import ChatGroq
from retrievers.retrievers import get_retriever
from state_schema import GuideState
from langchain_classic.chains.combine_documents import create_stuff_documents_chain
from langchain_classic.chains import create_retrieval_chain
from prompts.prompts import intro_prompt
import os
from dotenv import load_dotenv

load_dotenv()
groq_api=os.getenv("GROQ_API")

def intro_RAG(state:GuideState):

    print("------ INTRODUCTION NODE ------")

    intro_retriever=get_retriever("Introduction_db",os.getenv("ASTRA_DB_API_ENDPOINT"),os.getenv("ASTRA_DB_APPLICATION_TOKEN"),state.role)
    llm=ChatGroq(model="groq/compound", api_key=groq_api)
    document_chain=create_stuff_documents_chain(llm,intro_prompt)
    retrieval_chain=create_retrieval_chain(intro_retriever,document_chain)
    result=retrieval_chain.invoke({"input": state.question ,"role":state.role})
    return {
        "intro_response": result["answer"]
    }
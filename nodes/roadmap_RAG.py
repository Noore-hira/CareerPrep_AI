from langchain_groq import ChatGroq
from state_schema import GuideState
from retrievers.retrievers import get_retriever
from langchain_classic.chains.combine_documents import create_stuff_documents_chain
from langchain_classic.chains import create_retrieval_chain
from prompts.prompts import rm_prompt
import os
from dotenv import load_dotenv

load_dotenv()
groq_api=os.getenv("GROQ_API")

def rm_RAG(state:GuideState):

    print("------ ROADMAP NODE ------")
    
    roadmap_retriever = get_retriever("Roadmap_db",os.getenv("ASTRA_ENDPOINT_RM"),os.getenv("ASTRA_TOKEN_RM"),state.role)
    llm=ChatGroq(model="groq/compound", api_key=groq_api)
    document_chain=create_stuff_documents_chain(llm,rm_prompt)
    retrieval_chain=create_retrieval_chain(roadmap_retriever,document_chain)
    result=retrieval_chain.invoke({"input": state.question ,"role":state.role})
    return {
        "rm_response": result["answer"]
    }

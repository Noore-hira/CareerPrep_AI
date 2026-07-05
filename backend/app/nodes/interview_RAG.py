from langchain_groq import ChatGroq
from app.retrievers.retrievers import get_retriever
from app.state_schema import GuideState
from langchain_classic.chains.combine_documents import create_stuff_documents_chain
from langchain_classic.chains import create_retrieval_chain
from app.prompts.prompts import iv_prompt
import os
from dotenv import load_dotenv

load_dotenv()
groq_api=os.getenv("GROQ_API")

def interview_RAG(state:GuideState):

    print("------ INTERVIEW QUESTIONS NODE ------")
    
    interview_retriever = get_retriever("Interview_db",os.getenv("ASTRA_ENDPOINT_IV"),os.getenv("ASTRA_TOKEN_IV"),state.role)
    try:
        llm=ChatGroq(model="groq/compound", api_key=groq_api)
        document_chain=create_stuff_documents_chain(llm,iv_prompt)
        retrieval_chain=create_retrieval_chain(interview_retriever,document_chain)
        result=retrieval_chain.invoke({"input": state.question ,"role":state.role})
    except Exception as e:
        print(f"Error: {e}")
    return {
        "iv_response": result["answer"]
    }
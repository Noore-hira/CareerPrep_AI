from langchain_groq import ChatGroq
from state_schema import GuideState
from nodes.interview_RAG import interview_RAG
from nodes.introduction_RAG import intro_RAG
from nodes.resources_RAG import resources_RAG
from nodes.roadmap_RAG import rm_RAG
from nodes.projects_RAG import projects_RAG
import os
from dotenv import load_dotenv

api_key=os.getenv("GROQ_API")

def merge(state:GuideState) -> GuideState:
    print("------ MERGE NODE ------")
    prompt=f"""
    You are an expert Career Guide Generator below are given the different 
    sections of the guide you have to merge them structurally with sequence:
    - Introduction 
    - Roadmap
    - Resources
    - Interview Questions
    - Resume Tips and Projects
    if some irrelevant information found just omit it
    {state.intro_response}
    {state.rm_response} 
    {state.rcs_response}
    {state.iv_response}
    {state.pj_response}
    """
    llm=ChatGroq(model="llama-3.3-70b-versatile", api_key=api_key)
    response=llm.invoke(prompt).content
    return state.model_copy(update={"merge_response":response})
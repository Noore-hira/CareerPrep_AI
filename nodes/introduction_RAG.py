from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from retrievers.retrievers import intro_retriever
from state_schema import GuideState
from langchain_classic.chains.combine_documents import create_stuff_documents_chain
from langchain_classic.chains import create_retrieval_chain
import os
from dotenv import load_dotenv

load_dotenv()
groq_api=os.getenv("GROQ_API")

def intro_RAG(state:GuideState) -> GuideState:
    llm=ChatGroq(model="llama-3.3-70b-versatile", api_key=groq_api)
    prompt=PromptTemplate.from_template(
    """ You are an expert career advisor and technical writer.
        Your task is to write the **Introduction** section of an Interview Preparation Guide for the role: **{role}**.
        Use ONLY the information provided in the retrieved context. Do not use outside knowledge, make assumptions, or hallucinate information. If any information is missing from the context, simply omit it.
        The introduction should be beginner-friendly, professional, and well-structured.
        Generate the following sections in order:

    # Introduction

    ## Who is a {role}?
    Provide a concise explanation of the role.

    ## What does a {role} do?
    Explain the primary responsibilities and day-to-day work.

    ## Key Responsibilities
    Summarize the major responsibilities using bullet points.

    ## Skills Required
    Organize the required skills into logical categories where applicable, such as:
    - Programming Languages
    - Frameworks & Libraries
    - Databases
    - Cloud & DevOps
    - Tools
    - Soft Skills

    Only include categories supported by the retrieved context.

    ## Career Opportunities
    Briefly describe industries, job roles, and career growth opportunities.

    ## Average Salary (2026)
    If salary information exists in the retrieved context, present it as a Markdown table. Otherwise, omit this section.

    Formatting Requirements:
    - Use Markdown headings.
    - Use bullet points where appropriate.
    - Keep the content concise (approximately 500–800 words).
    - Avoid repetition.
    - Maintain a professional tone.
    - Do not mention the retrieved context or source documents.
    - Do not generate information that is not present in the retrieved context.

    Retrieved Context:
    {context} 
        
        """
    )

    document_chain=create_stuff_documents_chain(llm,prompt)
    retrieval_chain=create_retrieval_chain(intro_retriever,document_chain)
    result=retrieval_chain.invoke({"input": state.question ,"role":"AI engineer"})
    return state.model_copy(update={"intro_response":result["answer"]})
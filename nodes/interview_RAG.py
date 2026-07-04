from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from retrievers.retrievers import intrerview_retriever
from state_schema import GuideState
from langchain_classic.chains.combine_documents import create_stuff_documents_chain
from langchain_classic.chains import create_retrieval_chain
import os
from dotenv import load_dotenv

load_dotenv()
groq_api=os.getenv("GROQ_API")

def interview_RAG(state:GuideState) -> GuideState:
    llm=ChatGroq(model="llama-3.3-70b-versatile", api_key=groq_api)
    prompt=PromptTemplate.from_template(
        """
        You are an expert technical interviewer, hiring manager, and technical writer.

        Your task is to write the **Interview Questions** section of an Interview Preparation Guide for the role: **{role}**.

        Use ONLY the information provided in the retrieved context. Do not use outside knowledge, make assumptions, or hallucinate information. If any information is missing from the context, simply omit it.

        The interview preparation section should be well-organized, beginner-friendly, and suitable for candidates preparing for technical interviews.

        Generate the following sections in order:

        # Interview Questions

        ## Interview Preparation Overview

        Briefly explain the purpose of interview preparation for the {role} position and what candidates should focus on before attending interviews.

        ## Technical Interview Questions

        Organize the interview questions into logical categories based on the retrieved context.

        Examples of possible categories include:
        - Theory Based
        - Data Structures & Algorithms
        - Behavioral Questions
        - Coding Questions
        - Logical Questions

        Only include categories that exist in the retrieved context.

        For each category:

        - Add a Markdown heading.
        - List the interview questions as numbered items.
        - Do not generate answers

        ## Interview Tips

        Summarize the interview preparation advice 

        Examples may include:
        - Communication tips
        - Problem-solving approach
        - Time management
        - Resume preparation
        - Project explanation
        - Confidence and professionalism

        Formatting Requirements:
        - Use Markdown headings.
        - Use numbered lists for interview questions.
        - Use bullet points where appropriate.
        - Keep the content approximately 700–1200 words.
        - Organize questions into meaningful categories.
        - Avoid repetition.
        - Maintain a professional and beginner-friendly tone.
        - Do not mention the retrieved context or source documents.
        - Do not generate information that is not present in the retrieved context.
        - Omit any section for which no information exists in the retrieved context.

        Retrieved Context:
        {context}
        """
        )

    document_chain=create_stuff_documents_chain(llm,prompt)
    retrieval_chain=create_retrieval_chain(intrerview_retriever,document_chain)
    result=retrieval_chain.invoke({"input": "give me interview question for DevOps engineering" ,"role":"DevOps engineer"})
    return state.model_copy(update={"iv_response": result["answer"]})
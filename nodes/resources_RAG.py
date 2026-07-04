from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from state_schema import GuideState
from retrievers.retrievers import resources_retriever
from langchain_classic.chains.combine_documents import create_stuff_documents_chain
from langchain_classic.chains import create_retrieval_chain
import os
from dotenv import load_dotenv

load_dotenv()
groq_api=os.getenv("GROQ_API")

def resources_RAG(state:GuideState)-> GuideState:

    print("------ RESOURCES NODE ------")

    llm=ChatGroq(model="llama-3.3-70b-versatile", api_key=groq_api)
    prompt=PromptTemplate.from_template(
        """
        You are an expert career advisor and technical writer.
        Your task is to write the **Learning Resources** section of an Interview Preparation Guide for the role: **{role}**.
        Use ONLY the information provided in the retrieved context. Do not use outside knowledge, make assumptions, or hallucinate information. If any information is missing from the context, simply omit it.
        The resources section should be beginner-friendly, practical, and well-structured.

        Generate the following sections in order:

        # Learning Resources

        ## Recommended Learning Platforms
        List the recommended platforms, websites, or learning portals along with a brief description of what learners can study on each platform.

        ## Free Online Courses
        Present the available free courses as a Markdown table with columns similar to:
        - Course Name
        - Platform
        - Description

        Only include columns that are supported by the retrieved context.

        ## YouTube Channels
        List the recommended YouTube channels along with a short description of the type of content they provide.

        ## Documentation & Official Resources
        List official documentation, learning guides, or reference websites that are recommended for learning the role.

        ## Books (Optional)
        If books are available in the retrieved context, list them with a one-line description. Otherwise, omit this section.

        ## Practice Platforms (Optional)
        If coding practice, interview practice, or hands-on learning platforms exist in the retrieved context, list them with a brief description. Otherwise, omit this section.

        Formatting Requirements:
        - Use Markdown headings.
        - Use bullet points where appropriate.
        - Present courses in Markdown tables whenever possible.
        - Keep descriptions concise.
        - Keep the content approximately 500–800 words.
        - Avoid repetition.
        - Maintain a professional tone.
        - Do not mention the retrieved context or source documents.
        - Do not generate information that is not present in the retrieved context.
        - Omit any section for which no information exists in the retrieved context.

        Retrieved Context:
        {context}
        """
        )

    document_chain=create_stuff_documents_chain(llm,prompt)
    retrieval_chain=create_retrieval_chain(resources_retriever,document_chain)
    result=retrieval_chain.invoke({"input": "give different resources for learning AI engineering" ,"role":"AI engineer"})
    return state.model_copy(update={"rcs_response":result["answer"]})
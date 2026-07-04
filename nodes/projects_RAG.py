from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from state_schema import GuideState
from retrievers.retrievers import projects_retriever
from langchain_classic.chains.combine_documents import create_stuff_documents_chain
from langchain_classic.chains import create_retrieval_chain
import os
from dotenv import load_dotenv

load_dotenv()
groq_api=os.getenv("GROQ_API")

def projects_RAG(state:GuideState) -> GuideState:

    print("------ PROJECTS NODE ------")

    llm=ChatGroq(model="llama-3.3-70b-versatile", api_key=groq_api)
    prompt=PromptTemplate.from_template(
        """
        You are an expert career advisor, recruiter, and technical writer.
        Your task is to write the **Resume Tips & Portfolio Projects** section of an Interview Preparation Guide for the role: **{role}**.
        Use ONLY the information provided in the retrieved context. Do not use outside knowledge, make assumptions, or hallucinate information. If any information is missing from the context, simply omit it.
        The content should be practical, concise, beginner-friendly, and focused on helping candidates build a strong resume and portfolio.

        Generate the following sections in order:

        # Resume Tips & Portfolio Projects

        ## Resume Best Practices

        Summarize the most important resume writing recommendations provided in the retrieved context.

        Include guidance such as:
        - Resume structure
        - Resume length
        - Professional summary
        - Technical skills section
        - Work experience
        - Education
        - Certifications
        - Achievements
        - Formatting recommendations

        Only include topics supported by the retrieved context.

        ## Portfolio Projects

        List the recommended portfolio projects mentioned in the retrieved context.

        For each project include:

        - Project Name
        - Brief Description
        - Skills or Technologies Demonstrated
        - Why the project is valuable for interviews

        Present the projects as Markdown subsections or bullet points.

        ## GitHub & Portfolio Recommendations

        If the retrieved context contains recommendations for GitHub repositories, portfolio organization, documentation, README files, deployment, demonstrations, or project presentation, summarize them as bullet points.

        Otherwise, omit this section.

        ## Final Advice

        Provide a short concluding paragraph summarizing how candidates can strengthen their resume and portfolio based only on the retrieved context.

        Formatting Requirements:
        - Use Markdown headings.
        - Use bullet points where appropriate.
        - Keep explanations concise and practical.
        - Organize each project clearly.
        - Keep the content approximately 600–900 words.
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
    retrieval_chain=create_retrieval_chain(projects_retriever,document_chain)
    result=retrieval_chain.invoke({"input": "give me different project ideas for Software Engineering role" ,"role":"Software engineer"})
    return state.model_copy(update={"pj_response": result["answer"]})
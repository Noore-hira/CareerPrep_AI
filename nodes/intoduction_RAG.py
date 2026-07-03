from langchain_groq import ChatGroq
from langchain_astradb import AstraDBVectorStore
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.document_loaders import PyMuPDFLoader,DirectoryLoader
from langchain_core.prompts import PromptTemplate
from preproccess import preprocess_documents
from state_schema import GuideState
from langchain_core.output_parsers import StrOutputParser
from langchain_classic.chains.combine_documents import create_stuff_documents_chain
from langchain_classic.chains import create_retrieval_chain
from langgraph.graph import StateGraph
import os
from dotenv import load_dotenv

load_dotenv()
api_endpoint=os.getenv("ASTRA_DB_API_ENDPOINT")
token=os.getenv("ASTRA_DB_APPLICATION_TOKEN")
groq_api=os.getenv("GROQ_API")
os.environ["HF_TOKEN"]=os.getenv("HF_TOKEN")

files=[r"D:\langchain\Projects\Interview_guide\Dataset\introduction\AI Engineer - Introduction (2026).pdf",
       r"D:\langchain\Projects\Interview_guide\Dataset\introduction\Data Engineer - Introduction (2026).pdf",
       r"D:\langchain\Projects\Interview_guide\Dataset\introduction\DevOps Engineer - Introduction (2026).pdf",
       r"D:\langchain\Projects\Interview_guide\Dataset\introduction\Full Stack Developer - Introduction (2026).pdf",
       r"D:\langchain\Projects\Interview_guide\Dataset\introduction\Software Engineer - Introduction (2026).pdf"]

all_docs=[]
for file in files:
    docs=preprocess_documents(file)
    all_docs.extend(docs)

#print(len(all_docs))
#print(all_docs[5].metadata)

def intro_RAG(state:GuideState) -> GuideState:

    chunks=RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200).split_documents(all_docs)
    #print(len(chunks))
    #print(chunks[10])

    embeddings=HuggingFaceEmbeddings(model="BAAI/bge-base-en-v1.5")

    vectorstore = AstraDBVectorStore(
        embedding=embeddings,
        collection_name="Introduction_db",
        api_endpoint=api_endpoint,
        token=token,

    )

    #vectorstore.add_documents(chunks)
    retriever=vectorstore.as_retriever(search_kwargs={"k":8})

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
    retrieval_chain=create_retrieval_chain(retriever,document_chain)
    result=retrieval_chain.invoke({"input": state.question ,"role":"AI engineer"})
    return state.model_copy(update={"intro_response":result["answer"]})
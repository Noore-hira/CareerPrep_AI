from langchain_groq import ChatGroq
from langchain_astradb import AstraDBVectorStore
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.prompts import PromptTemplate
from preproccess import preprocess_documents
from state_schema import GuideState
from langchain_classic.chains.combine_documents import create_stuff_documents_chain
from langchain_classic.chains import create_retrieval_chain
from langgraph.graph import StateGraph
import os
from dotenv import load_dotenv

load_dotenv()
api_endpoint=os.getenv("ASTRA_ENDPOINT_RM")
token=os.getenv("ASTRA_TOKEN_RM")
groq_api=os.getenv("GROQ_API")
os.environ["HF_TOKEN"]=os.getenv("HF_TOKEN")

files=[r"D:\langchain\Projects\Interview_guide\Dataset\roadmap\AI Engineer Roadmap (Beginner to Job-Ready) – 2026.pdf",
       r"D:\langchain\Projects\Interview_guide\Dataset\roadmap\Data Engineer Roadmap (Beginner to Job-Ready) – 2026.pdf",
       r"D:\langchain\Projects\Interview_guide\Dataset\roadmap\DevOps Engineer Roadmap.pdf",
       r"D:\langchain\Projects\Interview_guide\Dataset\roadmap\Full Stack Developer Roadmap (Beginner to Job-Ready) – 2026.pdf",
       r"D:\langchain\Projects\Interview_guide\Dataset\roadmap\Software Engineer Roadmap (Beginner to Job-Ready) – 2026.pdf"]

all_docs=[]
for file in files:
    docs=preprocess_documents(file)
    all_docs.extend(docs)

#print(len(all_docs))
#print(all_docs[5].metadata)

def rm_RAG(state:GuideState) -> GuideState:

    chunks=RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200).split_documents(all_docs)
    #print(len(chunks))
    #print(chunks[10])

    embeddings=HuggingFaceEmbeddings(model="BAAI/bge-base-en-v1.5")

    vectorstore = AstraDBVectorStore(
        embedding=embeddings,
        collection_name="Roadmap_db",
        api_endpoint=api_endpoint,
        token=token,

    )

    #vectorstore.add_documents(chunks)
    retriever=vectorstore.as_retriever(search_kwargs={"k":5})

    llm=ChatGroq(model="llama-3.3-70b-versatile", api_key=groq_api)
    prompt=PromptTemplate.from_template(
    """
You are an expert career advisor and technical writer.
Your task is to write the **Roadmap** section of an Interview Preparation Guide for the role: **{role}**.
Use ONLY the information provided in the retrieved context. Do not use outside knowledge, make assumptions, or hallucinate information. If any information is missing from the context, simply omit it.
The roadmap should be beginner-friendly, sequential, practical, and easy to follow.
Generate the following sections in order:

# Roadmap

## Overview
Briefly explain the recommended learning journey for becoming a {role}.

## Step-by-Step Roadmap

Organize the roadmap into sequential learning stages. Use the stage names and ordering provided in the retrieved context. For each stage:

- Explain what should be learned.
- Mention the important concepts, technologies, or tools covered in that stage.
- Briefly explain why the stage is important before moving to the next one.

## Recommended Learning Timeline

If a learning timeline exists in the retrieved context, summarize it as a Markdown table.

Example columns (only if supported by the retrieved context):
- Stage
- Estimated Duration
- Learning Outcome

Otherwise, omit this section.

## Final Advice

Conclude with a short summary encouraging learners to follow the roadmap consistently and focus on practical implementation, based only on the retrieved context.

Formatting Requirements:
- Use Markdown headings.
- Use numbered headings or bullet points for roadmap stages.
- Use Markdown tables where appropriate.
- Keep explanations concise and practical.
- Keep the content approximately 600–1000 words.
- Maintain the logical order of the roadmap from the retrieved context.
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
    retrieval_chain=create_retrieval_chain(retriever,document_chain)
    result=retrieval_chain.invoke({"input": "give me roadmap of AI engineer step by step" ,"role":"AI engineer"})
    print(result)
    return state.model_copy(update={"rm_response":result["answer"]})
print(rm_RAG)

from langchain_groq import ChatGroq
from langchain_astradb import AstraDBVectorStore
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.prompts import PromptTemplate
from preproccess import preprocess_documents
from state_schema import GuideState
from langchain_classic.chains.combine_documents import create_stuff_documents_chain
from langchain_classic.chains import create_retrieval_chain
import os
from dotenv import load_dotenv

load_dotenv()
api_endpoint=os.getenv("ASTRA_ENDPOINT_RCS")
token=os.getenv("ASTRA_TOKEN_RCS")
groq_api=os.getenv("GROQ_API")
os.environ["HF_TOKEN"]=os.getenv("HF_TOKEN")

files=[r"D:\langchain\Projects\Interview_guide\Dataset\resources\AI Engineering Learning Resources 2026.pdf",
       r"D:\langchain\Projects\Interview_guide\Dataset\resources\Data Engineering Learning Resources (2026).pdf",
       r"D:\langchain\Projects\Interview_guide\Dataset\resources\DevOps Engineering Learning Resources (2026).pdf",
       r"D:\langchain\Projects\Interview_guide\Dataset\resources\Full Stack Development Learning Resources (2026).pdf",
       r"D:\langchain\Projects\Interview_guide\Dataset\resources\Software Engineering Learning Resources (2026).pdf"]

all_docs=[]
for file in files:
    docs=preprocess_documents(file)
    all_docs.extend(docs)

#print(len(all_docs))
#print(all_docs[5].metadata)

def resources_RAG(state:GuideState)-> GuideState:
    chunks=RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200).split_documents(all_docs)
        #print(len(chunks))
        #print(chunks[10])

    embeddings=HuggingFaceEmbeddings(model="BAAI/bge-base-en-v1.5")

    vectorstore = AstraDBVectorStore(
        embedding=embeddings,
        collection_name="Resources_db",
        api_endpoint=api_endpoint,
        token=token,

        )

    #vectorstore.add_documents(chunks)
    retriever=vectorstore.as_retriever(search_kwargs={"k":8})

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
    retrieval_chain=create_retrieval_chain(retriever,document_chain)
    result=retrieval_chain.invoke({"input": "give different resources for learning AI engineering" ,"role":"AI engineer"})
    return state.model_copy(update={"rcs_response":result["answer"]})
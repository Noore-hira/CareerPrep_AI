from langchain_astradb import AstraDBVectorStore
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.prompts import PromptTemplate
from preproccess import preprocess_documents
import os
from dotenv import load_dotenv

load_dotenv()
os.environ["HF_TOKEN"]=os.getenv("HF_TOKEN")

#files=[r"D:\langchain\Projects\Interview_guide\Dataset\resume_tips_and_projects\AI_Engineer_Resume_Updated.pdf",
#       r"D:\langchain\Projects\Interview_guide\Dataset\resume_tips_and_projects\Data Engineer Resume Tips & Portfolio Projects (2026).pdf",
#       r"D:\langchain\Projects\Interview_guide\Dataset\resume_tips_and_projects\DevOps Engineer Resume Tips & Portfolio Projects (2026).pdf",
#       r"D:\langchain\Projects\Interview_guide\Dataset\resume_tips_and_projects\Full Stack Developer Resume Tips & Portfolio Projects (2026).pdf",
#       r"D:\langchain\Projects\Interview_guide\Dataset\resume_tips_and_projects\Software Engineer Resume Tips & Portfolio Projects (2026).pdf"]

#all_docs=[]
#for file in files:
#    docs=preprocess_documents(file)
#    all_docs.extend(docs)

#print(len(all_docs))
#print(all_docs[5].metadata)
#chunks=RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200).split_documents(all_docs)
        #print(len(chunks))
        #print(chunks[10])


embeddings=HuggingFaceEmbeddings(model="BAAI/bge-base-en-v1.5")

def get_retriever(collection_name: str,api_endpoint,token, k: int = 8):
    vectorstore = AstraDBVectorStore(
        collection_name=collection_name,
        embedding=embeddings,
        api_endpoint=api_endpoint,
        token=token,
    )

    return vectorstore.as_retriever(search_kwargs={"k": k})

intro_retriever = get_retriever("Introduction_db",os.getenv("ASTRA_DB_API_ENDPOINT"),os.getenv("ASTRA_DB_APPLICATION_TOKEN"))
roadmap_retriever = get_retriever("Roadmap_db",os.getenv("ASTRA_ENDPOINT_RM"),os.getenv("ASTRA_TOKEN_RM"))
resources_retriever = get_retriever("Resources_db",os.getenv("ASTRA_ENDPOINT_RCS"),os.getenv("ASTRA_TOKEN_RCS"))
intrerview_retriever = get_retriever("Interview_db",os.getenv("ASTRA_ENDPOINT_IV"),os.getenv("ASTRA_TOKEN_IV"))
projects_retriever = get_retriever("Projects_db",os.getenv("ASTRA_ENDPOINT_PJ"),os.getenv("ASTRA_TOKEN_PJ"))
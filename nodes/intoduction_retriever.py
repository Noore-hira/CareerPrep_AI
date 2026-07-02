from langchain_groq import ChatGroq
from langchain_astradb import AstraDBVectorStore
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.document_loaders import PyMuPDFLoader,DirectoryLoader
from preproccess import preprocess_documents
import os
from dotenv import load_dotenv

load_dotenv()
api_endpoint=os.getenv("ASTRA_DB_API_ENDPOINT")
token=os.getenv("ASTRA_DB_APPLICATION_TOKEN")
groq_api=os.getenv("GROQ_API")
os.environ["HF_TOKEN"]=os.getenv("HF_TOKEN")

files=["D:\langchain\Projects\Interview_guide\Dataset\introduction\AI Engineer - Introduction (2026).pdf",
       "D:\langchain\Projects\Interview_guide\Dataset\introduction\Data Engineer - Introduction (2026).pdf",
       "D:\langchain\Projects\Interview_guide\Dataset\introduction\DevOps Engineer - Introduction (2026).pdf",
       "D:\langchain\Projects\Interview_guide\Dataset\introduction\Full Stack Developer - Introduction (2026).pdf",
       "D:\langchain\Projects\Interview_guide\Dataset\introduction\Software Engineer - Introduction (2026).pdf"]

all_docs=[]
for file in files:
    docs=preprocess_documents(file)
    all_docs.extend(docs)


print(len(all_docs))
print(all_docs[5].metadata)

chunks=RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200).split_documents(all_docs)
print(len(chunks))
print(chunks[10])

embeddings=HuggingFaceEmbeddings(model="BAAI/bge-base-en-v1.5")

vectorstore = AstraDBVectorStore(
    embedding=embeddings,
    collection_name="Introduction_db",
    api_endpoint=api_endpoint,
    token=token,
)

#vectorstore.add_documents(chunks)
retriever=vectorstore.as_retriever(search_kwargs={"k":4})
results=retriever.invoke("AI engineer Skills required")
print(results)


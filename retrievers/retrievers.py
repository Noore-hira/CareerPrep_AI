from langchain_astradb import AstraDBVectorStore
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.prompts import PromptTemplate
from preproccess import preprocess_documents, preprocess_txt_documents
from langchain_text_splitters import RecursiveCharacterTextSplitter
import os
from astrapy import DataAPIClient
from dotenv import load_dotenv

load_dotenv()
os.environ["HF_TOKEN"]=os.getenv("HF_TOKEN")

#files=[r"D:\langchain\Projects\Interview_guide\Dataset\interview_questions\AI Engineer.txt",
       #r"D:\langchain\Projects\Interview_guide\Dataset\interview_questions\Data Engineer.txt",
       #r"D:\langchain\Projects\Interview_guide\Dataset\interview_questions\DevOps Engineer.txt",
       #r"D:\langchain\Projects\Interview_guide\Dataset\interview_questions\FullStack Developer.txt",
       #r"D:\langchain\Projects\Interview_guide\Dataset\interview_questions\Software Engineer.txt"]

#all_docs=[]
#for file in files:
    #docs=preprocess_txt_documents(file)
    #all_docs.extend(docs)

#print(len(all_docs))
#print(all_docs[0].metadata)
#chunks=RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200).split_documents(all_docs)
#print(len(chunks))
#print(chunks[-1].metadata)

embeddings=HuggingFaceEmbeddings(model="BAAI/bge-base-en-v1.5")

def get_retriever(collection_name: str,api_endpoint, token,role ,k: int = 8):
    vectorstore = AstraDBVectorStore(
        collection_name=collection_name,
        embedding=embeddings,
        api_endpoint=api_endpoint,
        token=token,
    )
    #vectorstore.add_documents(chunks)
    return vectorstore.as_retriever(search_kwargs={
                                        "k": k,
                                         "filter":{"role":role} })

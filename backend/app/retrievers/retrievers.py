from langchain_astradb import AstraDBVectorStore
from langchain_huggingface import HuggingFaceEmbeddings
from dotenv import load_dotenv
import os

load_dotenv()

os.environ["HF_TOKEN"] = os.getenv("HF_TOKEN")

# OpenShift writable cache directories
os.environ["HF_HOME"] = "/tmp/huggingface"
os.environ["HUGGINGFACE_HUB_CACHE"] = "/tmp/huggingface/hub"
os.environ["TRANSFORMERS_CACHE"] = "/tmp/huggingface/transformers"
os.environ["TORCH_HOME"] = "/tmp/torch"


# Lazy loaded embedding model
_embeddings = None


def get_embeddings():

    global _embeddings

    if _embeddings is None:

        print("Loading HuggingFace embedding model...")

        _embeddings = HuggingFaceEmbeddings(
            model_name="BAAI/bge-base-en-v1.5"
        )

    return _embeddings



def get_retriever(
    collection_name: str,
    api_endpoint,
    token,
    role,
    k: int = 8
):

    embeddings = get_embeddings()

    vectorstore = AstraDBVectorStore(
        collection_name=collection_name,
        embedding=embeddings,
        api_endpoint=api_endpoint,
        token=token,
    )

    return vectorstore.as_retriever(
        search_kwargs={
            "k": k,
            "filter": {
                "role": role
            }
        }
    )
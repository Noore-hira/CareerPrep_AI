from langchain_astradb import AstraDBVectorStore
from langchain_huggingface import HuggingFaceEmbeddings
from dotenv import load_dotenv
import os


load_dotenv()


# Load HF token only when needed
HF_TOKEN = os.getenv("HF_TOKEN")

if HF_TOKEN:
    os.environ["HF_TOKEN"] = HF_TOKEN


# Global cache
_embeddings = None


def get_embeddings():
    """
    Lazy load HuggingFace embedding model.
    It loads only on the first API request.
    """

    global _embeddings

    if _embeddings is None:
        print("Loading HuggingFace embedding model...")

        _embeddings = HuggingFaceEmbeddings(
            model_name="BAAI/bge-base-en-v1.5"
        )

        print("Embedding model loaded")

    return _embeddings



def get_retriever(
    collection_name: str,
    api_endpoint,
    token,
    role,
    k: int = 8
):
    """
    Lazy creates AstraDB retriever.
    """

    print("Creating AstraDB retriever...")

    embeddings = get_embeddings()

    vectorstore = AstraDBVectorStore(
        collection_name=collection_name,
        embedding=embeddings,
        api_endpoint=api_endpoint,
        token=token,
    )


    retriever = vectorstore.as_retriever(
        search_kwargs={
            "k": k,
            "filter": {
                "role": role
            }
        }
    )

    print("Retriever ready")

    return retriever
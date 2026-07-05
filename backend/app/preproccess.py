from pathlib import Path
import re
from langchain_community.document_loaders import PyMuPDFLoader

def preprocess_documents(pdf_path: str):
    """
    Load a PDF using PyMuPDFLoader, clean the extracted text,
    and replace the metadata with a standardized schema.
    """

    loader = PyMuPDFLoader(pdf_path)
    docs = loader.load()

    pdf_path = Path(pdf_path)

    role = pdf_path.stem
    section = pdf_path.parent.name

    for i, doc in enumerate(docs):

        text = doc.page_content

        # ---------- Clean Text ----------

        # Remove isolated bullet lines
        text = re.sub(r'^\s*[•●▪◦]\s*$', '', text, flags=re.MULTILINE)

        # Replace tabs
        text = text.replace("\t", " ")

        # Remove multiple spaces
        text = re.sub(r"[ ]{2,}", " ", text)

        # Remove excessive blank lines
        text = re.sub(r"\n{3,}", "\n\n", text)

        doc.page_content = text.strip()

        # ---------- Replace Metadata ----------

        doc.metadata = {

            "role": role,
            "section": section,

            "page_number": i + 1,

            "file_name": pdf_path.name,
            "file_path": str(pdf_path),
            "location": f"{role}/{pdf_path.name}",

            "source": "CareerPrep_AI_Dataset",
            "version": "2026",

        }

    return docs

from pathlib import Path
import re

from langchain_core.documents import Document


def preprocess_txt_documents(txt_path: str):
    """
    Load a TXT file, clean the text, and create a Document
    with standardized metadata.
    """

    txt_path = Path(txt_path)

    # Read file
    with open(txt_path, "r", encoding="utf-8") as f:
        text = f.read()

    # ---------- Clean Text ----------

    # Replace tabs with spaces
    text = text.replace("\t", " ")

    # Remove multiple spaces
    text = re.sub(r"[ ]{2,}", " ", text)

    # Remove excessive blank lines
    text = re.sub(r"\n{3,}", "\n\n", text)

    text = text.strip()

    # ---------- Metadata ----------

    role = txt_path.stem
    section = txt_path.parent.name

    doc = Document(
        page_content=text,
        metadata={
            "role": role,
            "section": section,

            # TXT files are treated as a single page/document
            "page_number": 1,

            "file_name": txt_path.name,
            "file_path": str(txt_path),
            "location": f"{role}/{txt_path.name}",

            "source": "CareerPrep_AI_Dataset",
            "version": "2026",
        },
    )

    return [doc]
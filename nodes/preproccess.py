from pathlib import Path
import re
from langchain_community.document_loaders import PyMuPDFLoader

SECTION_ORDER = {
    "Introduction": 1,
    "Roadmap": 2,
    "Resources": 3,
    "Interview Questions": 4,
    "Resume Tips": 5,
}


def preprocess_documents(pdf_path: str):
    """
    Load a PDF using PyMuPDFLoader, clean the extracted text,
    and replace the metadata with a standardized schema.
    """

    loader = PyMuPDFLoader(pdf_path)
    docs = loader.load()

    pdf_path = Path(pdf_path)

    role = pdf_path.parent.name
    section = pdf_path.stem

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
            "section_order": SECTION_ORDER.get(section, 999),

            "page_number": i + 1,

            "file_name": pdf_path.name,
            "file_path": str(pdf_path),
            "location": f"{role}/{pdf_path.name}",

            "source": "CareerPrep_AI_Dataset",
            "version": "2026",

        }

    return docs
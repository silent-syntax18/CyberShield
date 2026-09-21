import os
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter

from rag_engine import create_vectorstore


DOCUMENT_PATH = "rag/documents/cybersecurity_basics.txt"


def load_document():
    with open(DOCUMENT_PATH, "r", encoding="utf-8") as file:
        text = file.read()

    return Document(
        page_content=text,
        metadata={
            "source": "CyberShield Cybersecurity Knowledge Base"
        }
    )


def build_knowledge_base():

    print("Loading cybersecurity knowledge...")

    document = load_document()

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=100
    )

    chunks = splitter.split_documents([document])

    print(f"Created {len(chunks)} knowledge chunks.")

    create_vectorstore(chunks)

    print("CyberShield RAG knowledge base created successfully!")


if __name__ == "__main__":
    build_knowledge_base()
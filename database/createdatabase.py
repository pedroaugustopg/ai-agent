from pathlib import Path

from dotenv import load_dotenv
from langchain_chroma import Chroma
from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent
BASE_FOLDER = BASE_DIR / "base"
CHROMA_DB = BASE_DIR / "chroma_db"


def createdb():
    documents = load_documents()
    chunks = split_chunks(documents)
    vectorize_chunks(chunks)

def load_documents():
    loader = PyPDFDirectoryLoader(str(BASE_FOLDER), glob="*.pdf")
    documents = loader.load()
    print(f"Documents loaded: {len(documents)}")
    return documents

def split_chunks(documents):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=5000,
        chunk_overlap=500,
        length_function=len,
        add_start_index=True,
    )

    chunks = text_splitter.split_documents(documents)
    print(f"Chunks created: {len(chunks)}")
    return chunks

def vectorize_chunks(chunks):
    Chroma.from_documents(
        documents=chunks,
        embedding=OpenAIEmbeddings(),
        persist_directory=str(CHROMA_DB),
    )

    print("Vector database created successfully.")


if __name__ == "__main__":
    createdb()
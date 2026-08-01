from pathlib import Path

from langchain_chroma import Chroma
from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter


BASE_DIR = Path(__file__).resolve().parent.parent
BASE_FOLDER = BASE_DIR / "base"
CHROMA_DB = BASE_DIR / "chroma_db"

def createdb():
    documents = load_documents()
    chunks = split_chunks(documents)
    vectorize_chunks(chunks)

def load_documents():
    loader = PyPDFDirectoryLoader(str(BASE_FOLDER), glob="*.pdf")
    return loader.load()

def split_chunks(documents):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=5000,
        chunk_overlap=500,
        length_function=len,
        add_start_index=True,
    )

    return splitter.split_documents(documents)

def vectorize_chunks(chunks):

    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=str(CHROMA_DB),
    )

    print("Vector database created successfully.")


if __name__ == "__main__":
    createdb()
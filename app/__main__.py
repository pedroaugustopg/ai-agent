from pathlib import Path

from langchain_chroma import Chroma
from langchain_core.prompts import ChatPromptTemplate
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_ollama import ChatOllama


BASE_DIR = Path(__file__).resolve().parent.parent
CHROMA_DB = BASE_DIR / "chroma_db"

PROMPT_TEMPLATE = """
You are an AI assistant.

Answer the user's question using ONLY the information contained in the knowledge base below.

If the answer is not present in the knowledge base, answer exactly:

"I could not find this information in the knowledge base."

Knowledge Base:
{knowledge_base}

Question:
{question}
"""

def question():

    user_question = input("Write your question: ")

    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    database = Chroma(
        persist_directory=str(CHROMA_DB),
        embedding_function=embeddings
    )

    retriever = database.as_retriever(
        search_kwargs={"k": 4}
    )

    documents = retriever.invoke(user_question)

    if not documents:
        print("No relevant information was found.")
        return

    knowledge_base = "\n\n------------------------\n\n".join(
        document.page_content for document in documents
    )

    prompt = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)

    messages = prompt.invoke(
        {
            "question": user_question,
            "knowledge_base": knowledge_base
        }
    )

    model = ChatOllama(
        model="llama3.1",
        temperature=0
    )

    try:
        response = model.invoke(messages)

        print("\nAI Response:\n")
        print(response.content)

    except Exception:
        print(
            "Ollama is not running. Install Ollama and start a local model before executing."
        )


if __name__ == "__main__":
    question()
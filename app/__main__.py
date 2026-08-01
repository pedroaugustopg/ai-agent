from pathlib import Path

from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from langchain_chroma import Chroma
from langchain_openai import ChatOpenAI, OpenAIEmbeddings

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent
CHROMA_DB = BASE_DIR / "chroma_db"

PROMPT_TEMPLATE = """
Answer the user's question based only on the information below.

Knowledge Base:
{knowledge_base}

Question:
{question}
"""


def question():
    user_question = input("Write your question: ")

    embedding_function = OpenAIEmbeddings()
    database = Chroma(
        persist_directory=str(CHROMA_DB),
        embedding_function=embedding_function
    )

    results = database.similarity_search_with_relevance_scores(
        user_question,
        k=4
    )

    if len(results) == 0 or results[0][1] < 0.7:
        print("Could not find relevant information in the database.")
        return

    knowledge_base = "\n\n----\n\n".join(
        result[0].page_content for result in results
    )

    prompt = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)

    messages = prompt.invoke({
        "question": user_question,
        "knowledge_base": knowledge_base
    })

    model = ChatOpenAI()

    response = model.invoke(messages)

    print("\nAI Response:\n")
    print(response.content)


if __name__ == "__main__":
    question()


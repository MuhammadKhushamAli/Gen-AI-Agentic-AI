from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings
from langchain_qdrant import QdrantVectorStore
from openai import OpenAI

load_dotenv()

# Vector Embedding
vector_embedding_model = OpenAIEmbeddings(
    model="text-embedding-3-large"
)

vector_db = QdrantVectorStore.from_existing_collection(
    collection_name="learning_rag_practice",
    embedding=vector_embedding_model,
    url="http://localhost:6333"
)

user_input = input("Enter here: ")

collections = vector_db.similarity_search(query=user_input)

context = "\n\n\n".join([f"Page Content: {collection.page_content}\nPage Number: {collection.metadata["page_label"]}\nSource: {collection.metadata["source"]}" for collection in collections])

SYSTEM = f"""
You are an AI agent who is answering the query according to given context retreved from pdf file with content and number
You will only answer the question from the pdf and navigate user to the correcct page in pdf

Context:
{context}
"""

client = OpenAI()

response = client.chat.completions.create(
    model="gpt-5",
    messages=[
        { "role": "system", "content": SYSTEM },
        { "role": "user", "content": user_input}
    ]
)

print(response.choices[0].message.content)
from dotenv import load_dotenv
from openai import OpenAI
from langchain_openai import OpenAIEmbeddings
from langchain_qdrant import QdrantVectorStore

load_dotenv()

openai_client = OpenAI()

embedding_model = OpenAIEmbeddings(
    model="text-embedding-3-large"
)

vector_db = QdrantVectorStore.from_existing_collection(
    url="http://localhost:6333",
    collection_name="learning_rag_practice",
    embedding=embedding_model
)

async def processor(query: str):
    print("Searching For Chunks...")

    chunks = vector_db.similarity_search(query=query)
    
    context = [f"\n\n\nPage Content: {chunk.page_content}\nPage Number: {chunk.metadata["page_label"]}\nSource: {chunk.metadata["source"]}" for chunk in chunks]

    SYSTEM = f"""
        You are an AI agent who is answering the query according to given context retreved from pdf file with content and number
        You will only answer the question from the pdf and navigate user to the correcct page in pdf

        Context:
        {context}
    """

    response = openai_client.chat.completions.create(
        model="gpt-5",
        messages=[
            { "role": "system", "content": SYSTEM },
            { "role": "user", "content": query }
        ]
    )

    print(f"🤖 {response.choices[0].message.content}")
    return response.choices[0].message.content
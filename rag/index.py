from pathlib import Path
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_qdrant import QdrantVectorStore
from dotenv import load_dotenv

load_dotenv()

file_path = Path(__file__).parent / "nodejs.pdf"

# Loading Pdf
pdf_loader = PyPDFLoader(file_path=file_path)
file_data = pdf_loader.load()

# Splitting to Chunks
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200
)
splitted_chunks = text_splitter.split_documents(file_data)

# Making Embeding Model
vector_embedding_model = OpenAIEmbeddings(
    model="text-embedding-3-large"
)

# Making Quadrant Store
quadrant_store = QdrantVectorStore.from_documents(
    documents=splitted_chunks,
    embedding=vector_embedding_model,
    url="http://localhost:6333",
    collection_name="learning_rag_practice"
)

print("All Done")

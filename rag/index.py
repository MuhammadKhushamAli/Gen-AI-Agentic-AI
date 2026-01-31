from pathlib import Path
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings

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




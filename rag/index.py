from pathlib import Path
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

file_path = Path(__file__).parent / "nodejs.pdf"

pdf_loader = PyPDFLoader(file_path=file_path)
file_data = pdf_loader.load()

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200
)
splitted_chunks = text_splitter.split_documents(file_data)


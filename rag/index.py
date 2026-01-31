from pathlib import Path
from langchain_community.document_loaders import PyPDFLoader

file_path = Path(__file__).parent / "nodejs.pdf"

pdf_loader = PyPDFLoader(file_path=file_path)
file_data = pdf_loader.load()

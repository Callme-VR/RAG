from pathlib import Path
from typing import List, Any

# Loaders
from langchain_community.document_loaders import (
    PyPDFLoader,
    TextLoader,
    CSVLoader,
    Docx2txtLoader,
    JSONLoader
)
from langchain_community.document_loaders.excel import UnstructuredExcelLoader


def Load_all_documents(data_path: str) -> List[Any]:
    """
    Load all supported files from the data directory and convert to LangChain document structure.
    Supported: PDF, TXT, CSV, Excel, Word, JSON
    """
    
    # use the project root data Folder
    data_path = Path(data_path).resolve()
    print(f"[DEBUG] Loading documents from: {data_path}")
    
    # store all documents
    documents = []
    
    # pdf files
    pdf_files = list(data_path.glob("**/*.pdf"))
    print(f"[DEBUG] Found {len(pdf_files)} PDF files: {[str(f) for f in pdf_files]}")
    
    for pdf_file in pdf_files:
        print(f"[DEBUG] Loading Pdf: {pdf_file}")
        try:
            loader = PyPDFLoader(str(pdf_file))
            loaded = loader.load()
            print(f"[DEBUG] Loaded {len(loaded)} pages from {pdf_file}")
            documents.extend(loaded)
        except Exception as e:
            print(f"[ERROR] Failed to load {pdf_file}: {e}")
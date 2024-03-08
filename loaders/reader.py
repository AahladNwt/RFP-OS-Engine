from langchain.document_loaders import (
    PyMuPDFLoader,
    PyPDFLoader,
    Docx2txtLoader,
    TextLoader, 
    UnstructuredImageLoader
)
from utils.util import read_tables
from llama_index import download_loader
from pathlib import Path
from langchain.docstore.document import Document
from typing import List
# from diskcache import Cache
# Create a disk-based cache
# cache = Cache('path_to_directory', expire=200)
PDFReader = download_loader("PDFReader")
DocxReader = download_loader("DocxReader")


# @cache.memoize() # Decorator to cache the function result
def parse_docs(file_path:str) -> List[Document]:
    """_summary_

    Returns:
        _type_: _description_
    """
    
    # load document 
    if file_path:
        loader = PDFReader()
        documents = loader.load_data(file=Path(file_path))
        # documents = read_tables(file_path,documents)
    elif file_path.endswith('docx'):
        loader = DocxReader()
        documents = loader.load_data(file=Path(file_path))
    elif file_path.endswith('.txt'):
        loader = TextLoader(file_path)
        documents = loader.load()
        
    elif file_path.endswith('jpg') or file_path.endswith('jpg'):
        loader = UnstructuredImageLoader(file_path, mode="elements")
        documents = loader.load()
        
    else:
        raise ValueError("Load the right file")
    
    return documents
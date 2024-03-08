import sys
sys.path.append("..")
# import torch
import os
from utils.util import read_tables
from langchain.docstore.document import Document
from typing import List
from langchain.document_loaders import PyPDFDirectoryLoader, UnstructuredPDFLoader, PyPDFLoader
# from diskcache import Cache
from llama_index import download_loader
from pathlib import Path
# cache = Cache('company_directory', expire=200)
PDFReader = download_loader("PDFReader")

# DEVICE = "cuda:0" if torch.cuda.is_available() else "cpu"
# embeddings = HuggingFaceInstructEmbeddings(
# model_name="hkunlp/instructor-large", model_kwargs={"device": DEVICE}
# )
 

# @cache.memoize() # Decorator to cache the function result
def load_vendor_contractors_info(orgfile_names)->List[Document]:
    #loader = PyPDFLoader(orgfile_names[0])
    #documents = loader.load()
    #print("Type Of Documment>>>", type(documents))
    # loader = [UnstructuredPDFLoader(file, mode="elements") for file in orgfile_names]  
    documents = []
    for file in orgfile_names:
        loader = PDFReader()
        document = loader.load_data(file=Path(file))
        # document = read_tables(file,documents )
        documents.extend(document)
    return documents






     


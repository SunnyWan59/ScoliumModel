import pypdf
import os
from langchain_cohere import CohereEmbeddings
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.document_loaders.generic import GenericLoader
from langchain_community.document_loaders.parsers import GrobidParser
from langchain_text_splitters import RecursiveCharacterTextSplitter

from pinecone import Pinecone
from langchain_pinecone import PineconeVectorStore

import asyncio

os.environ["COHERE_API_KEY"] = "pwYNrztZvPYTflPTWTQuLjbF27ES4kr6OMoCt3wf"
os.environ["PINECONE_API_KEY"] = "pcsk_3wj9Yc_Z4qKuzouzoT3gRmkjMZEQE3pdiXYqfM3krLaMkbdvkiwHcqdQYYbfbVLML2XUH"
pinecone_api_key = os.environ.get("PINECONE_API_KEY")

async def _lazy_load_pdf(file_path):
    loader = PyPDFLoader(file_path)
    pages = []
    async for page in loader.alazy_load():
        pages.append(page)
    return pages

def Grobid_Load(file_path):
    loader = GenericLoader.from_filesystem(
        "../Papers/",
        glob="*",
        suffixes=[".pdf"],
        parser=GrobidParser(segment_sentences=False),
    )
    docs = loader.load()


text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,  # chunk size (characters)
    chunk_overlap=200,  # chunk overlap (characters)
    add_start_index=True,  # track index in original document
)




class Indexer():
    def __init__(self, index_name = "scholium-index"): 
        self.embeddings = CohereEmbeddings(model="embed-english-v3.0")
        self.pc = Pinecone(api_key= pinecone_api_key)

        # Check if index exists
        existing_indexes = [index_info["name"] for index_info in self.pc.list_indexes()]
        if index_name not in existing_indexes: 
            raise ValueError(f"Index {index_name} does not exist")
        else:
            self.index = self.pc.Index(index_name)
        
        self.vector_store = PineconeVectorStore(embedding=self.embeddings, index=self.index)
        
    def index_document(self, file_path):
        pages = asyncio.run(_lazy_load_pdf(file_path))
        all_splits = text_splitter.split_documents(pages)
        self.vector_store.add_documents(documents=all_splits)


if __name__ == "__main__":
    file_path = os.path.join(os.path.dirname(__file__), "DistilBERT.pdf")
    # pages = asyncio.run(_lazy_load_pdf(file_path))
    # print(len(pages[3].page_content))
    # all_splits = text_splitter.split_documents(pages)
    # splitcount = len(all_splits)
    # print(f"Split page into {splitcount} sub-documents.")
    indexer = Indexer()
    indexer.index_document(file_path)



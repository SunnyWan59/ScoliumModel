import os
from model import CohereModel, create_config, get_output
from langchain_cohere import CohereEmbeddings,ChatCohere
from langchain_core.vectorstores import InMemoryVectorStore
from langchain_community.document_loaders import JSONLoader
from langchain_pinecone import PineconeVectorStore
from pinecone import Pinecone

pinecone_api_key = "pcsk_3wj9Yc_Z4qKuzouzoT3gRmkjMZEQE3pdiXYqfM3krLaMkbdvkiwHcqdQYYbfbVLML2XUH"

#Another security risk
os.environ["LANGSMITH_API_KEY"] = "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"
os.environ["COHERE_API_KEY"] = "pwYNrztZvPYTflPTWTQuLjbF27ES4kr6OMoCt3wf"




class RAG():
    def __init__(self,index_name = "scholium-index"):
        '''
        A class ro represent our RAG model
        '''
        self.model  = CohereModel()
        self.embeddings = CohereEmbeddings(model="embed-english-v3.0")
        pc = Pinecone(api_key=...)
        index = pc.Index(index_name)
        self.vector_store = PineconeVectorStore(embedding=self.embeddings, index=index)




if __name__ == "__main__":
    model = CohereModel()
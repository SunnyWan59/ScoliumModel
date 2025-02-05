import os
from dotenv import load_dotenv


from pinecone import Pinecone
from langchain_pinecone import PineconeVectorStore
from langchain_openai import ChatOpenAI,OpenAIEmbeddings

from ScholiumModel.citations import metadata_to_chicago


load_dotenv()

DB_URI = os.environ.get("DB_URI")
pinecone_api_key = os.environ.get("PINECONE_API_KEY")

embeddings = OpenAIEmbeddings(model="text-embedding-3-small")

pc = Pinecone(api_key= pinecone_api_key)
index = pc.Index("scholium-index")
vector_store = PineconeVectorStore(embedding=embeddings, index=index)

def get_citation(query:str):
    citations = []
    retrieved_docs = vector_store.similarity_search(query.strip("\""), k=1)
    for doc in retrieved_docs:
        citations.append(metadata_to_chicago(doc.metadata))
    return "\n\n".join(citations)

if __name__ == "__main__":
    print(get_citation("Another intuition is that chain of thought allows the model to spend more computation"))

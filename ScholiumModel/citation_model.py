import os

from langchain_openai import ChatOpenAI,OpenAIEmbeddings

from dotenv import load_dotenv

from langchain_core.tools import tool
from langchain_core.messages import SystemMessage

from pinecone import Pinecone
from langchain_pinecone import PineconeVectorStore

load_dotenv()

OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
DB_URI = os.environ.get("DB_URI")
pinecone_api_key = os.environ.get("PINECONE_API_KEY")
model = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=1,
    max_tokens=None,
    timeout=None,
    max_retries=2,
)

embeddings = OpenAIEmbeddings(model="text-embedding-3-small")

pc = Pinecone(api_key= pinecone_api_key)
index = pc.Index("scholium-index")
vector_store = PineconeVectorStore(embedding=embeddings, index=index)



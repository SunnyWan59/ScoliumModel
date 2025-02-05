import os
from dotenv import load_dotenv

from langchain_core.tools import tool
from langchain_core.messages import SystemMessage
from langchain_core.documents import Document

from langgraph.graph import START, StateGraph

from typing_extensions import List, TypedDict

from pinecone import Pinecone
from langchain_pinecone import PineconeVectorStore
from langchain_openai import ChatOpenAI,OpenAIEmbeddings



load_dotenv()

OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
DB_URI = os.environ.get("DB_URI")
pinecone_api_key = os.environ.get("PINECONE_API_KEY")
model = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0,
    max_tokens=None,
    timeout=None,
    max_retries=2,
)

embeddings = OpenAIEmbeddings(model="text-embedding-3-small")

pc = Pinecone(api_key= pinecone_api_key)
index = pc.Index("scholium-index")
vector_store = PineconeVectorStore(embedding=embeddings, index=index)


system_prompt = (
    "You are a helpful assistant. You get citations for quotes from {context}."
    "Chicago cite the papers of the quotes. Only give the citation."
    "{context}"
)

question_prefix = "Only give me the citation of this quote: "

class State(TypedDict):
    question: str
    context: List[Document]
    answer: str

def retrieve(state: State):
    retrieved_docs = vector_store.similarity_search(state["question"])
    return retrieved_docs

def compile_graph():
    graph_builder = StateGraph(State).add_sequence([retrieve])
    graph_builder.add_edge(START, "retrieve")
    return graph_builder.compile()
    
if __name__ == "__main__":
    question = question_prefix + "Another intuition is that chain of thought allows the model to spend more computation"
    test_state = State(question= question)
    context= retrieve(test_state)
    md = context[0].metadata
    print(md)
import os
from dotenv import load_dotenv

from langchain_core.tools import tool


from langgraph.graph import END, START, StateGraph
from langgraph.prebuilt import ToolNode, tools_condition
from langgraph.graph import MessagesState, StateGraph
from langchain_core.messages import SystemMessage


from typing_extensions import List, TypedDict

from pinecone import Pinecone
from langchain_pinecone import PineconeVectorStore
from langchain_openai import ChatOpenAI,OpenAIEmbeddings

from ScholiumModel.citations import metadata_to_chicago


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

@tool(parse_docstring=True)
def cite(query: str):
    """Find a citation based on the query
    Args:
        query: the query to be cited
    """
    retrieved_docs = vector_store.similarity_search(query, k=2)
    serialized_docs = []
    for doc in retrieved_docs:
        serialized_docs.append(metadata_to_chicago(doc.metadata))
    serialized = "\n\n".join(serialized_docs)    
    return serialized


def query_or_respond(state: MessagesState):
    """Generate tool call for retrieval or respond."""
    llm_with_tools = model.bind_tools([cite])
    response = llm_with_tools.invoke(state["messages"])
    return {"messages": [response]}

tools = ToolNode([cite])

if __name__ == "__main__":
    pass
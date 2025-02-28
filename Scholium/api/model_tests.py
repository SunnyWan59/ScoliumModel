
import os
from openai import OpenAI
from pinecone import Pinecone

from langchain_openai import ChatOpenAI,OpenAIEmbeddings
from langchain_core.messages import HumanMessage

from api.model import RAG
from api.pinecone_vectorstore import ScholiumPineconeVectorStore

LANGSMITH_API_KEY = os.environ.get("LANGSMITH_API_KEY")
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
DB_URI = os.environ.get("DB_URI")
pinecone_api_key = os.environ.get("PINECONE_API_KEY")
model = ChatOpenAI(
    model="gpt-4o",
    temperature=1,
    max_tokens=None,
    timeout=None,
    max_retries=2,
)

embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
client = OpenAI(api_key=OPENAI_API_KEY)

pc = Pinecone(api_key= pinecone_api_key)
index = pc.Index("arxiv-index")
index2 = pc.Index("scholium-index")

async def invoke_chat(query:str, thread: str):
    input_messages = [HumanMessage(query)]
    config = {"configurable": {"thread_id": thread}}
    output = await RAG.ainvoke({"messages": input_messages},config)
    output["messages"][-1].pretty_print()

async def test_chat():
    thread = "123"
    response = await invoke_chat("Give me papers on BERT",thread)
    return response

def draw_graph(graph):
    from IPython.display import Image, display
    image_obj = Image(graph.get_graph().draw_mermaid_png())
    with open("graph.png", "wb") as f:
        f.write(image_obj.data)

def test_index(query):
    vector_store = ScholiumPineconeVectorStore(client, index)
    return [
        paper["metadata"]["title"] for paper in vector_store.similarity_search_with_score_cutoff(query,10,0.5)
    ]

if __name__ == "__main__":

    import asyncio  
    asyncio.run(test_chat())
    draw_graph(RAG)

    print(test_index("Give me papers on BERT and Law"))

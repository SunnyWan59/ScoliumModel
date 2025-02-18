from api.model import RAG

import os
from langchain_openai import ChatOpenAI,OpenAIEmbeddings
from langchain_core.messages import HumanMessage


from pinecone import Pinecone
from langchain_pinecone import PineconeVectorStore



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

pc = Pinecone(api_key= pinecone_api_key)
index = pc.Index("scholium-index")
vector_store = PineconeVectorStore(embedding=embeddings, index=index)

async def invoke_chat(query:str, thread: str):
    input_messages = [HumanMessage(query)]
    config = {"configurable": {"thread_id": thread}}
    output = await RAG.ainvoke({"messages": input_messages},config)
    output["messages"][-1].pretty_print()

async def test_chat():
    thread = "123"
    await invoke_chat("Hello", thread)
    await invoke_chat("dog",thread)
    

if __name__ == "__main__":

    import asyncio  
    asyncio.run(test_chat())
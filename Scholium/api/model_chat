from api.model import compile_graph

import os
from langchain_openai import ChatOpenAI,OpenAIEmbeddings


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

def chat(thread:str, input_message:str):
        graph = compile_graph()
        config = {"configurable": {"thread_id": thread}}

        for step in graph.stream(
            {"messages": [{"role": "user", "content": input_message}]},
            stream_mode="values",
            config= config,):
            step["messages"][-1].pretty_print()

def chat_in_terminal(thread: str):
    while True:
        input_message = input("Enter your query:")
        if input_message == "exit":
            print("Exiting...")
            return
        else:
            chat(thread, input_message)


if __name__ == "__main__":
    # chat_in_terminal("test1")
    chat("123","Give me papers on ecoders")

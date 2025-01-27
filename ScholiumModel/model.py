import os

from langchain_cohere import CohereEmbeddings, ChatCohere
from langchain_core.tools import tool
from langchain_core.messages import SystemMessage, AIMessage, HumanMessage

from pinecone import Pinecone
from langchain_pinecone import PineconeVectorStore


from langgraph.graph import END
from langgraph.prebuilt import ToolNode, tools_condition
from langgraph.graph import MessagesState, StateGraph

from langchain_postgres import PostgresChatMessageHistory
import psycopg
from langgraph.checkpoint.postgres import PostgresSaver
from langgraph.checkpoint.memory import MemorySaver



#Another security risk
os.environ["LANGSMITH_API_KEY"] = "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"
os.environ["COHERE_API_KEY"] = "pwYNrztZvPYTflPTWTQuLjbF27ES4kr6OMoCt3wf"
os.environ["PINECONE_API_KEY"] = "pcsk_3wj9Yc_Z4qKuzouzoT3gRmkjMZEQE3pdiXYqfM3krLaMkbdvkiwHcqdQYYbfbVLML2XUH"
pinecone_api_key = os.environ.get("PINECONE_API_KEY")
DB_URI = "postgresql://neondb_owner:npg_SUp1iMyYFH5h@ep-autumn-scene-a8lger8v-pooler.eastus2.azure.neon.tech/neondb?sslmode=require"

model = ChatCohere(model="command-r-plus")

embeddings = CohereEmbeddings(model="embed-english-v3.0")

pc = Pinecone(api_key= pinecone_api_key)
index = pc.Index("scholium-index")
vector_store = PineconeVectorStore(embedding=embeddings, index=index)

# with ConnectionPool(
#     conninfo=DB_URI,
#     max_size=20,
#     ) as pool:
#         checkpointer = PostgresSaver(pool)


@tool(response_format="content_and_artifact")
def retrieve(query: str):
    """Retrieve information related to a query."""
    retrieved_docs = vector_store.similarity_search(query, k=2)
    serialized_docs = []
    for doc in retrieved_docs:
        formatted_doc = f"Source: {doc.metadata}\nContent: {doc.page_content}"
        serialized_docs.append(formatted_doc)

    serialized = "\n\n".join(serialized_docs)
    return serialized, retrieved_docs

def query_or_respond(state: MessagesState):
    """Generate tool call for retrieval or respond."""
    tool_model = model.bind_tools([retrieve])
    response = tool_model.invoke(state["messages"])
    return {"messages": [response]}

tools = ToolNode([retrieve])

def generate(state: MessagesState):
    '''
    Generates the desired answer to the user's question
    '''
    recent_tool_messages = []
    for message in state["messages"]:
        if message.type == "tool":
            recent_tool_messages.append(message)
        else:
            break
    tool_messages = recent_tool_messages

    docs_content = "\n\n".join(doc.content for doc in tool_messages)
    system_message_content = (
        "You are an assistant for question-answering tasks. "
        "Use the following pieces of retrieved context to answer "
        "the question. If you don't know the answer, say that you "
        "don't know. Use three sentences maximum and keep the "
        "answer concise. Also make sure to cite the context where you got the answer from."
        "\n\n"
        f"{docs_content}"
    )
    prompt = [SystemMessage(system_message_content)]
    for message in state["messages"]:
        if message.type in ("human", "system") or (message.type == "ai" and not message.tool_calls):
            prompt.append(message)

    response = model.invoke(prompt)
    return {"messages": [response]}



def compile_graph():
    graph_builder = StateGraph(MessagesState)
    graph_builder.add_node(query_or_respond)
    graph_builder.add_node(tools)
    graph_builder.add_node(generate)
    graph_builder.set_entry_point("query_or_respond")
    graph_builder.add_conditional_edges(
        "query_or_respond",
        tools_condition,
        {END: END, "tools": "tools"},
    )
    graph_builder.add_edge("tools", "generate")
    graph_builder.add_edge("generate", END)
    # checkpointer = PostgresSaver.from_conn_string(DB_URI)
    checkpointer = MemorySaver()
    graph = graph_builder.compile(checkpointer=checkpointer)
    return graph


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

API_KEYS = {    
    "LANGSMITH_API_KEY": "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",
    "COHERE_API_KEY": "pwYNrztZvPYTflPTWTQuLjbF27ES4kr6OMoCt3wf",
    "PINECONE_API_KEY": "pcsk_3wj9Yc_Z4qKuzouzoT3gRmkjMZEQE3pdiXYqfM3krLaMkbdvkiwHcqdQYYbfbVLML2XUH"
}

if __name__ == "__main__":
    # chat_in_terminal("test1")
    # connect_database()
    chat_in_terminal("test1")
    # chat("test1", "Hello!")
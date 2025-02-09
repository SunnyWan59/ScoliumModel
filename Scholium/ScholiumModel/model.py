import os
import re
from langchain_openai import ChatOpenAI,OpenAIEmbeddings

from langchain_core.tools import tool
from langchain_core.messages import SystemMessage
from langchain_core.documents import Document

from pinecone import Pinecone
from langchain_pinecone import PineconeVectorStore


from langgraph.graph import END
from langgraph.prebuilt import ToolNode, tools_condition
from langgraph.graph import MessagesState, StateGraph

# from langgraph.checkpoint.postgres import PostgresSaver 
from langgraph.checkpoint.memory import MemorySaver

from dotenv import load_dotenv

from ScholiumModel.citations import metadata_to_chicago

from typing import Optional

load_dotenv()

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

class ResearchState(MessagesState):
    """
    This is the state of the agent.
    It is a subclass of the MessagesState class from langgraph.
    """
    answer: Optional[str]


def extract_paper_titles(text):
    """
    Finds all substrings in `text` that are enclosed in matching single or double quotes.
    
    Parameters:
        text (str): The input string.
    
    Returns:
        List[str]: A list of quoted substrings, including the surrounding quote characters.
    """
    pattern = r'(["\'])(.*?)\1'
    matches = re.finditer(pattern, text)
    return [match.group(0) for match in matches]


def get_paper_metadata(titles:list[str], metadata):
    metadata_list = []
    for title in titles:
        if title.strip("\"") in metadata:
            metadata_list.append(metadata[title.strip("\"")])
    return metadata_list


@tool(response_format="content_and_artifact")
def retrieve(query: str):
    """Retrieve information related to a query."""
    retrieved_docs = vector_store.similarity_search(query, k=5)
    serialized_docs = []
    retrieved_metadata = {}
    for doc in retrieved_docs:
        formatted_doc = f"Source: {doc.metadata}\nContent: {doc.page_content}"
        serialized_docs.append(formatted_doc)
        retrieved_metadata[doc.metadata['Title']] = doc.metadata
    serialized = "\n\n".join(serialized_docs)
    return serialized, retrieved_metadata

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
    for message in reversed(state["messages"]):
        if message.type == "tool":
            recent_tool_messages.append(message)
        else:
            break
    tool_messages = recent_tool_messages[::-1]

    docs_content = "\n\n".join(doc.content for doc in tool_messages)

    system_message_content = (
        "You are an assistant for question-answering tasks. Your job is to recommend papers from the retrieved context."
        "Use the following pieces of retrieved context to answer "
        "the question. If you don't know the answer, say that you "
        "don't know. Do not make up sources or use sources that are not in the retrieved context."
        "Surround the titles of the papers with quotation marks."
        "\n\n"
        f"{docs_content}"
    )

    prompt = [SystemMessage(system_message_content)]
    for message in state["messages"]:
        if message.type in ("human", "system") or (message.type == "ai" and not message.tool_calls):
            prompt.append(message)

    response = model.invoke(prompt)
    used_papers = extract_paper_titles(response.content)
    metadata = get_paper_metadata(used_papers, tool_messages[0].artifact)
    response.response_metadata = metadata
    print(response)
    return {"messages": [response], "answer": response.content}


def compile_graph():
    graph_builder = StateGraph(ResearchState)
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

RAG = compile_graph()

if __name__ == "__main__":
    chat_in_terminal("test1")
    # chat("123","Give me papers on ecoders")

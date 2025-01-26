import os
from langchain_cohere import ChatCohere
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import START, MessagesState, StateGraph
from langchain_core.messages import HumanMessage, SystemMessage, trim_messages, AIMessage

#API Key
os.environ["COHERE_API_KEY"] = "pwYNrztZvPYTflPTWTQuLjbF27ES4kr6OMoCt3wf"

#Model
class CohereModel:
    def __init__(self):  
        self.model = ChatCohere(model="command-r-plus")
        self.chat_history = StateGraph(state_schema=MessagesState)
        self.chat_history.add_edge(START, "model")
        self.chat_history.add_node("model", self.call_model)
        self.memory = MemorySaver()
        self.app = self.chat_history.compile(checkpointer=self.memory)
        self.trimmer = trim_messages(
                max_tokens=65,
                strategy="last",
                token_counter= self.model,
                include_system=True,
                allow_partial=False,
                start_on="human",
            )


    def call_model(self, state: MessagesState):
        trimmed_messages = self.trimmer.invoke(state["messages"])
        response = self.model.invoke(trimmed_messages)
        return {"messages": response}


def get_output(query, config, app):
    input_messages = [HumanMessage(query)]
    response = ""
    for chunk, metadata in app.stream(
        {"messages": input_messages},
        config,
        stream_mode="messages",
    ):
        if isinstance(chunk, AIMessage):  # Filter to just model responses
            response += " " + chunk.content


    return response



def create_config(thread_id: str):
    return {"configurable": {"thread_id": thread_id}}



if __name__ == "__main__":
    model = CohereModel()
    config = create_config("test")
    queries = ["Hi my name is Bob", "What's my name?"]
    for query in queries:
        print("Human Query: ", query)
        print(get_output(query, config, model.app))

    config2 = create_config("test2")
    print("---New thread---")
    print("Human Query: ", queries[-1])
    print(get_output(queries[-1], config2, model.app))
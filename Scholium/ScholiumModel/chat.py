from langchain.callbacks.base import BaseCallbackHandler
from langchain.schema import ChatMessage
import streamlit as st

from ScholiumModel.model import compile_graph 

st.title("Scholium")
if "messages" not in st.session_state:
    st.session_state["messages"] = [ChatMessage(role="assistant", content="How can I help you?")]

st.empty()
for msg in st.session_state.messages:
    st.chat_message(msg.role).write(msg.content)

if prompt := st.chat_input():
    st.session_state.messages.append(ChatMessage(role="user", content=prompt))
    st.chat_message("user").write(prompt)
    graph = compile_graph()
    response = graph.invoke({"messages": [{"role": "user", "content":st.session_state.messages[-1].content}]})
    st.session_state.messages.append(ChatMessage(role="assistant", content=response['messages'][-1].content))
    st.chat_message("assistant").write(response['messages'][-1].content)

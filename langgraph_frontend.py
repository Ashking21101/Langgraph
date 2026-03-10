import streamlit as st
from langgraph_backend import chatbot
from langchain_core.messages import HumanMessage

CONFIG = {"configurable": {"thread_id": "thread_1"}}

st.set_page_config(page_title="LangGraph Chatbot")

st.title("LangGraph Chatbot")

# session state is bascially a type of list , Think of it as temporary memory for the UI session.
if "message_history" not in st.session_state:
    st.session_state.message_history = []


for message in st.session_state.message_history:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

user_input = st.chat_input("Type here...")
if user_input:
    with st.chat_message("user"):
        st.markdown(user_input)
    st.session_state.message_history.append({"role": "user", "content": user_input})


    #response = chatbot.invoke({"messages": [HumanMessage(content=user_input)]},config=CONFIG)
    #ai_message = response["messages"][-1].content
    #with st.chat_message("assistant"):
    #    st.markdown(ai_message)
    #st.session_state.message_history.append({"role": "assistant", "content": ai_message})

    # OR 


    # with streaming
    with st.chat_message("assistant"):
        ai_message = st.write_stream(
            message_chunk.content for message_chunk, metadata in chatbot.stream(
                {"messages":[HumanMessage(content=user_input)]},
                config={'configurable':{"thread_id":"thread_1"}},
                stream_mode='messages'
            )
        )
    st.session_state.message_history.append({"role": "assistant", "content": ai_message})









#User types message
#      ↓
#Streamlit UI receives input
#      ↓
#Display user message
#      ↓
#Send message to LangGraph
#      ↓
#LangGraph loads memory
#      ↓
#LLM generates response
#      ↓
#Return AI message
#      ↓
#Display response
#      ↓
#Save to session_state
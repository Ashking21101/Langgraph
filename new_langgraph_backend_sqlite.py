from langgraph.graph import StateGraph, START, END
from typing import TypedDict, Annotated, Literal 
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage, BaseMessage
from dotenv import load_dotenv
import os
from pydantic import BaseModel, Field
import operator
import warnings
warnings.filterwarnings("ignore", category=UserWarning, module="pydantic")
from langgraph.checkpoint.sqlite import SqliteSaver
from langgraph.graph import add_messages # use add_messages (reducer func) for list of BaseMessage
import sqlite3


load_dotenv()

class ChatState(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]    # basemessage is the parent class of humanmessage, systemmessage and aimessage


llm = ChatOpenAI(model="gpt-4.1-nano")

def chat_node(state: ChatState):
    messages = state['messages']
    response = llm.invoke(messages)
    return {'messages': [response]}
    

# **************** SQLITE Db **********************************
conn = sqlite3.connect(database='chatbot.db', check_same_thread=False)
checkpointer = SqliteSaver(conn = conn)
# *************************************************************


graph = StateGraph(ChatState)
graph.add_node('chat_node', chat_node)
graph.add_edge(START, 'chat_node')
graph.add_edge('chat_node', END)


chatbot = graph.compile(checkpointer=checkpointer)

def retrieve_all_threads():
    all_threads = set()
    for checkpoint in checkpointer.list(None): # i want all, and not for specific
        all_threads.add(checkpoint.config["configurable"]["thread_id"])
    return list(all_threads)


# test
#CONFIG = {'configurable':{"thread_id":"thread_1"}}
#response = chatbot.invoke(
#    {'messages':[HumanMessage(content='what is my name')]},
#    config = CONFIG
#    )
#print(response)
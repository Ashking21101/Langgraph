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
from langgraph.checkpoint.memory import MemorySaver # it only save in local Ram
from langgraph.graph import add_messages # use add_messages (reducer func) for list of BaseMessage



load_dotenv()

class ChatState(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]    # basemessage is the parent class of humanmessage, systemmessage and aimessage


llm = ChatOpenAI(model="gpt-4.1-nano")

def chat_node(state: ChatState):
    messages = state['messages']
    response = llm.invoke(messages)
    return {'messages': [response]}
    


checkpointer = MemorySaver()

graph = StateGraph(ChatState)
graph.add_node('chat_node', chat_node)
graph.add_edge(START, 'chat_node')
graph.add_edge('chat_node', END)


chatbot = graph.compile(checkpointer=checkpointer)


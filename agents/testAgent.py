import time
import streamlit as st
from langgraph.prebuilt import ToolNode, tools_condition
from langgraph.graph import MessagesState, StateGraph, START, END
from langchain_core.messages import HumanMessage, SystemMessage
from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser, JsonOutputParser
from typing_extensions import TypedDict, List
from langgraph.prebuilt import ToolNode, tools_condition
from langgraph.graph import MessagesState, StateGraph, START, END
from langchain_core.messages import HumanMessage, SystemMessage
from concurrent.futures import *
import ast
import json
from utils.utils import getCohereLLM

def getResponseFromTestAgent():
    """Agent that is used to check about cricket related queries"""

    llm = getCohereLLM()
    return llm.invoke("How many ODI worldcups did Indian cricket team won? Answer it in a single word")

import time
import streamlit as st
from langgraph.prebuilt import ToolNode, tools_condition
from langgraph.graph import MessagesState, StateGraph, START, END
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser, JsonOutputParser
from typing_extensions import TypedDict, List
from langgraph.prebuilt import ToolNode, tools_condition
from langgraph.graph import MessagesState, StateGraph, START, END
from langchain_core.messages import HumanMessage, SystemMessage
from concurrent.futures import *
import ast
import json
from utils.utils import getCohereLLM
from agents.testAgent import getResponseFromTestAgent
from utils.AgentState import AgentState
from utils.utils import promptCreationForDataFrame

routerPrompt = PromptTemplate(
    template="""
    You are an intelligent router who has great knowledge of code development and business analysis for a sales analytics assistant.
    Classify the user request into one of these categories:
    - The **Code Agent**: if the task involves writing, running, or modifying code (e.g., calculations, transformations, SQL queries, Python functions, etc.)
    - The **Chart Agent**: if the task involves generating or updating a chart or visual representation of data.
    - The **Insight Agent**: if the task involves summarizing, interpreting, or explaining data (e.g., trends, outliers, recommendations, KPIs).
    
    Just a single word answer required, no more additional responses
    Return only the label: insight, code, or chart.
    
    User input: {user_query}
    
    Check these examples how the output format is
    
    Example1 - display the chart for the sales in this quarter
    Output - 'chart'
    
    Example2 - get the sales average in the quarter
    Output - 'code'
    
    """,
    input_variables=["user_query"],
)

llm = getCohereLLM()

query_decomposer = routerPrompt | llm | StrOutputParser()

def routerAgent(state: AgentState):

    """It is an classifier agent for a sales AI assistant.Classify the prompt correctly into one of: code, insight, chart."""

    dataframeprompt = promptCreationForDataFrame()

    prompt0 = """
    You are an intelligent router who has great knowledge of code development and business analysis (understand scheme of dataset given) for a sales analytics assistant.
    You know when to be a developer or when to be a business analyst by just seeing the prompt
    Please use chart only when there is a use of visualization or creating charts.
    """

    prompt1 = """
        
        - **code**: If the task involves calculating/finding the value something with in dataframe object, filtering data, finding maximum/minimum, ranking, grouping, counting but not for visualization — even if the user asks it in natural language.”
        - **chart**: if the user's request is about visualizing/creating charts the data — line charts, bar charts, pie charts, histograms, etc.
        - **insight**: if the user is asking for an analysis,insights , explanation, conclusion, trend analysis, or recommendation , or reasons — not just a simple fact or max value.
        
        Just a single word answer required, no more additional responses
        Return only the label: insight, code, or chart.
        """

    prompt2 = """
        User input: {user_query}
    
        Check these examples how the output format is
        
        Example1 - display the chart for the sales in this quarter
        Output - 'chart'
        
        Example2 - get the sales average in the quarter
        Output - 'code'
        
        Example3 - reasons why sales are more in FY25
        Output - 'insight'
        
        """

    prompt_template =prompt0 + "/n" +  dataframeprompt + "/n" + prompt1  + "/n" + prompt2
    global routerPrompt
    routerPromptWithDF = PromptTemplate(
        template=prompt_template,
        input_variables=["user_query"],
    )
    global query_decomposer
    query_decomposer2 = routerPromptWithDF | llm

    print(routerPromptWithDF)

    user_query = state["user_input"]
    decision = query_decomposer2.invoke({"user_query": user_query})
    if "steps" in state:
        steps = state["steps"]
    else:
        steps = []
    steps.append("RouterAgent")
    decision = decision.strip().lower()
    return {
        "user_input" : user_query,
        "generation" : decision,
        "steps" : steps
    }

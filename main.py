#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

@author: arunvoleti
"""

from flask import Flask, Response, jsonify
from flask import Flask, render_template, request
from gevent.pywsgi import WSGIServer
import json
from agents.testAgent import getResponseFromTestAgent
from langgraph.graph import StateGraph, END
from utils.AgentState import AgentState
from agents.supervisorAgent import routerAgent
from agents.codeAgent import codeAgent
from agents.chartAgent import chartAgent
from agents.insightsAgent import insightAgent

app = Flask(__name__)

def router(state):
    """Decides which agent to use based on the user message."""
    user_input = state["generation"].lower()

    if "code" in user_input or "generate python" in user_input:
        return "code"
    elif "insight" in user_input or "summary" in user_input:
        return "insight"
    elif "chart" in user_input or "plot" in user_input or "visualize" in user_input:
        return "chart"
    else:
        return "insight"  # Default fallback


@app.route("/testLLM", methods=["POST"])
def metadataparse():
    if request.method == "POST":
        inputModelPaylod = request.data
        user_input = inputModelPaylod.decode('utf-8')

        graph = StateGraph(AgentState)

        # Add nodes
        graph.add_node("router", routerAgent)
        graph.add_node("code_agent", codeAgent)
        graph.add_node("insight_agent", insightAgent)
        graph.add_node("chart_agent", chartAgent)

        # Routing logic
        graph.set_entry_point("router")
        graph.add_conditional_edges(
            "router",
            lambda state, config: router(state),
            path_map={
                "code": "code_agent",
                "insight": "insight_agent",
                "chart": "chart_agent",
            },
        )

        # All agent nodes go to END
        graph.add_edge("code_agent", END)
        graph.add_edge("insight_agent", END)
        graph.add_edge("chart_agent", END)

        flow = graph.compile()
        result = flow.invoke({"user_input": user_input})
        print(result["generation"])
        return result["generation"]




if __name__ == '__main__':
    # app.run(debug=True, host='0.0.0.0', port='5000')
    # app.debug = True
    http = WSGIServer(('', 5003), app.wsgi_app)

    # Serve your application
    http.serve_forever()

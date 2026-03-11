# Standard Imports
from langgraph.graph import StateGraph, START, END

# Project Imports
from .utils.state import State
from .utils.nodes import context_node, query_node

workflow = StateGraph(State)
workflow.add_node("context_node", context_node)
workflow.add_node("query_node", query_node)
workflow.add_edge(START, "context_node")
workflow.add_edge("context_node", "query_node")
workflow.add_edge("query_node", END)

graph = workflow.compile()

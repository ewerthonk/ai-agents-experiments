from langgraph.graph.message import MessagesState

class State(MessagesState):
    db_id: str
    question: str
    context: str | None
    query: str | None
    dataset: str = "spider_dev"
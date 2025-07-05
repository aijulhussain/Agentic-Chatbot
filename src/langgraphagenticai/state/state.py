from typing_extensions import TypedDict
from langgraph.graph.message import add_messages
from typing import Annotated

class State(TypedDict):
    """
    Represent the structer of the state used in graph.
    
    """
    messages: Annotated[list, add_messages]
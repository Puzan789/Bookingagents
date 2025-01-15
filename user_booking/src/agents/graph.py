from langgraph.graph import StateGraph,MessagesState,END,START 
from .agents import getuserintent,extractInformation,give_response,booking_node,rag_node,userintents,should_continue
from src.models.agentsModels import getuserInfo
from langgraph.checkpoint.memory import MemorySaver

class GraphBuilder:
    def __init__(self):
        self.builder = StateGraph(getuserInfo)

    def setup_nodes(self):
        self.builder.add_node("user_intents", getuserintent)
        self.builder.add_node("extractinformation", extractInformation)
        self.builder.add_node("give_response", give_response)
        self.builder.add_node("booking_node", booking_node)
        self.builder.add_node("rag_node", rag_node)
    def setup_edges(self):
        self.builder.add_edge(START, "user_intents")
        self.builder.add_conditional_edges(
            "user_intents", userintents, ["extractinformation", "booking_node", "rag_node"]
        )
        self.builder.add_conditional_edges(
            "extractinformation", should_continue, ["give_response", END]
        )
        self.builder.add_edge("give_response", END)
        self.builder.add_edge("booking_node", END)
        self.builder.add_edge("rag_node", END)

    def compile_graph(self):
        memory = MemorySaver()
        return self.builder.compile(checkpointer=memory)
    def build(self):
        self.setup_nodes()
        self.setup_edges()
        return self.compile_graph()





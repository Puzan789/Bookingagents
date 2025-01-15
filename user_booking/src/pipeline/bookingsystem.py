from src.agents.graph import GraphBuilder
builder=GraphBuilder()
thread = {"configurable": {"thread_id": "1"}}

class Bookingsystempipeline:
    def __init__(self):
        self.graph=builder.build()

    def get_response(self,user_query:str):
        output=self.graph.invoke({"input":user_query},thread)
        return output["messages"][-1].content


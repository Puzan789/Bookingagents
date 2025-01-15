from pydantic import BaseModel,Field
from langgraph.graph import StateGraph,MessagesState,END


###############contactinfo #########
class Contactinfo(BaseModel):
    name:str |None=None
    phone:int  | None=None
    email:str  | None=None

####userinformation #########
class info(BaseModel):
    userInfo:list[Contactinfo]=Field(
        description="Comprehensive list of analysis with their roles and affiliations."
    )


###userintent##
class userIntent(BaseModel):
    intent:int


####userinfomodel
class getuserInfo(MessagesState):
    input: str
    Contactinfo: Contactinfo
    extracted_info:str
    missing_fields:list[str]
    userintent:userIntent
    booked_date:str


####datemodel####
class date(BaseModel):
    date:str
    
## For api 
class userQuery(BaseModel):
    user_query: str
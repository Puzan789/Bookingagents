from src.prompts import *
from src.services.rag import AnswerRAG
from src.models.agentsModels import Contactinfo,info,userIntent,getuserInfo,date
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_groq import ChatGroq
import os 
from langgraph.graph import START,END
from datetime import datetime
from src.prompts.prompts import user_intent_finder_prompt,user_response_prompt,info_catch_instructions
from langchain_core.messages import HumanMessage, SystemMessage
#setup environment variable
os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY")
llm = ChatGroq(temperature=0, model_name="Gemma2-9b-It")
rag=AnswerRAG()
today_date= datetime.today().strftime('%Y-%m-%d (%A)')
missing_fields =[]

#create user intents 
def getuserintent(state:getuserInfo):
    input=state["input"]
    llm_structured_output=llm.with_structured_output(userIntent)
    system_message=user_intent_finder_prompt.format(input=input)
    result=llm_structured_output.invoke([SystemMessage(content=system_message)])
    return {"userintent":result.intent}
#get userintents
def userintents(state:getuserInfo):
    userintents=state.get("userintent")
    if userintents == 0:
       return "extractinformation"
    elif userintents == 1:
        return "booking_node"
    else:
        return "rag_node"

#book the appointment
def booking_node(state:getuserInfo):
    input=state["input"]
    llm_structured_output=llm.with_structured_output(date)
    system_message=user_response_prompt.format(user_input=input,today_date=today_date)
    result=llm_structured_output.invoke([SystemMessage(content=system_message)])
    response=f"Your date is booked for {result.date}"
    return {"booked_date":result.date,"messages":[response]}

#node for rag 
def rag_node(state:getuserInfo):
    input=state["input"]
    answer = rag.query(input)
    return {"messages":[answer]}

#extract user information
def extractInformation(state:getuserInfo):
    input=state["input"]
    structured_llm=llm.with_structured_output(Contactinfo)
    system_message=info_catch_instructions.format(input=input)
    result=structured_llm.invoke([SystemMessage(content=system_message)]+[HumanMessage(content="Extract the user information")])
    contact_info_dict={
        "name":result.name,
        "phone":result.phone,
        "email":result.email,
    }
    return {"Contactinfo":contact_info_dict}
#continue node
def should_continue(state:getuserInfo):
        extracted_info = state.get("Contactinfo", {})
        print(extracted_info)
        if extracted_info:
                
            # Check if 'name' is missing
            if extracted_info.get("name") is None:
                missing_fields.append("name")
            
            # Check if 'phone' is missing or its length is not 10
            if extracted_info.get("phone") is None:
                try:
                    if len(extracted_info.get("phone"))  !=10:
                        missing_fields.append("phone number length must be 10")
                except:
                    missing_fields.append("phonenumber ")
            
            # Check if 'email' is missing
            if extracted_info.get("email") is None:
                missing_fields.append("email")
            
            # If there are missing fields, return a message
            print(missing_fields)
            if missing_fields:
                state["missing_fields"] = missing_fields 
                print(f'''ths is {state["missing_fields"]}''')
                return "give_response"
            return END
        
        return END

        
#response giving node 
def give_response(state: getuserInfo):
    if not missing_fields:  # Handles None or an empty list
        message = "Thank you, we will contact you soon."
    elif len(missing_fields) > 1:
        field_list = ", ".join(missing_fields[:-1]) + " and " + missing_fields[-1]
        message = f"Please provide {field_list}."
    else:
        message = f"Please provide {missing_fields[0]}."

    return {"messages": [message]}
        
    

user_intent_finder_prompt= """You are a helpful AI assistant whose task is to classify user messages into three distinct categories. Analyze the user's message and respond with only a single number (0, 1, or 2) based on these rules:

Return 0 if:
- User wants to call or contact you
- User requests a phone conversation
- User asks for direct communication
- User wants to have a voice chat
Examples: "I want to call you", "can you contact me", "let's have a call", "can we talk on phone?"

Return 1 if:
- User wants to book an appointment
- User asks about scheduling a meeting
- User wants to make a reservation
Examples: "book an appointment", "I need to schedule a meeting", "make a reservation"

Return 2 if:
- User asks general questions about the context
- User requests information or assistance
- User wants to have a text conversation
- Any other message that doesn't fit categories 0 or 1
Examples: "what is machine learning?", "help me with my homework", "explain quantum physics"

Input: {input}

Remember to see the input and then decidee."""


#prompt for user_response
user_response_prompt="""The user wants to book an appointment.. 
Your task is to:
1. Parse this request and return ONLY a date in YYYY-MM-DD format
2. Today date is {today_date}
3. If the day has already passed this week, assume they mean next week
4. Return ONLY the date, no other text

The input user is this : {user_input}
"""


#user information extractionprompt
info_catch_instructions="""
You are the extractor who extract user information like name phonenumber and emailaddress if anything not present there return none if phonenumber is not length of 10 return none
from a given user input{input}
"""
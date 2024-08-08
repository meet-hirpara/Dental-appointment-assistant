import json
from langchain_google_genai import GoogleGenerativeAI
from datetime import datetime
from langchain_core.prompts import PromptTemplate

# Initialize the Google Generative AI model
llm = GoogleGenerativeAI(model="gemini-pro", google_api_key="AIzaSyAv57Fkw2UPQHtR8tO0mP6A6cOdI9XrORo")

# Function to understand user context
def interpret_intent(user_input):
    prompts = [
        f"Does the user want to book an appointment? The user said: '{user_input}'."
    ]
    response = llm.invoke(prompts)  # Use the correct method for generating responses
    response_text = response[0] if isinstance(response, list) else response
    return "yes" in response_text.lower()

# Function to generate questions
def generate_question(context):
    prompt = f"Given the context: {context}, generate a question that the dental appointment assistant should ask next."
    response = llm.invoke([prompt])
    question = response[0] if isinstance(response, list) else response
    return question


# Function to validate a name
def is_valid_name(name):
    return isinstance(name, str) and len(name.strip()) > 0

# Function to validate a date
def is_valid_date(date_str):
    try:
        template = """Your task is to provide yes or no base on user query. if user query has date then return "yes" otherwise return "no".
        for example: 12th may, 1 jan, 32 feb 2024 {example}
        Following is user query : {input}"""

        prompt = PromptTemplate.from_template(
            template = template
        )
        chain = prompt | llm
        response = chain.invoke({"input":str(date_str),"example":"12th jan"})
        print(response)
        if "yes" in response.lower():
            return True
        else:
            return False
    except ValueError:
        return False

# Function to validate a time
def is_valid_time(time_str):
    try:
        template = """Your task is to provide yes or no base on user query. if user query has time then return "yes" otherwise return "no".
        for example: 10 AM, 1am, 3pm, 10 in morining, 5 in evening.
        Following is user query : {input}"""

        prompt = PromptTemplate.from_template(
            template = template
        )
        chain = prompt | llm
        response = chain.invoke({"input":str(time_str)})
        print(response)
        if "yes" in response.lower():
            return True
        else:
            return False
    except ValueError:
        return False

# Function to ask for valid input
def ask_for_input(prompt, validate_func):
    while True:
        print(f"Agent: {prompt}")
        user_input = input("User: ")
        if validate_func(user_input):
            return user_input
        else:
            print("Agent: Please provide a valid input.")

# function to handle booking
def book_appointment():
    print("Agent: Hi, I am your dental appointment assistant. How can I help you today?")
    user_input = input("User: ")
    
    # check if the user wants to book an appointment
    if interpret_intent(user_input):
        # Ask for the user's name
        context = "Ask the user for their name."
        question = generate_question(context)
        user_name = ask_for_input(question, is_valid_name)
        
        # Ask for the appointment date
        context = "Ask the user for the date of their appointment."
        question = generate_question(context)
        appointment_date = ask_for_input(question, is_valid_date)
        
        # Ask for the appointment time
        context = "Ask the user for the time of their appointment."
        question = generate_question(context)
        appointment_time = ask_for_input(question, is_valid_time)
        
        # Store the appointment details
        appointment_details = {
            'name': user_name,
            'date': appointment_date,
            'time': appointment_time
        }
        
        json_response = json.dumps(appointment_details, indent=4)
        
        print(f"Agent: Your appointment is confirmed!\nHere are your appointment details:\n{json_response}")
    else:
        print("Agent: I'm sorry, I can only help with booking appointments.")


book_appointment()

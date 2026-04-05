import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.tools import tool
from langgraph.prebuilt import create_react_agent
import database as db


load_dotenv()



# Tool 1: Medications
@tool
def add_medication_tool(name: str, time: str):
    """
    Use this tool to add a new medication to the patient's schedule. 
    Requires the medication name and the time to take it.
    """
    db.add_medicine(name, time)
    return f"Successfully added {name} at {time} to the database."

# Tool 2: Fitness (NEW)
@tool
def log_fitness_tool(activity: str, duration: str):
    """
    Use this tool to log a physical activity, workout, or exercise.
    Requires the activity name (e.g., Running, Yoga) and duration (e.g., 30 mins).
    """
    db.add_fitness_log(activity, duration)
    return f"Successfully logged {duration} of {activity}."
@tool
def log_symptom_tool(symptom_description: str):
    """Use this tool when the user mentions a health issue, pain, or symptom."""
    db.add_symptom(symptom_description)
    return f"I've noted down your symptom: {symptom_description}. Please monitor it."

# Tool list update karo
tools = [add_medication_tool, log_fitness_tool, log_symptom_tool]

# Groq Llama 3 Model Setup
llm = ChatGroq(model="llama-3.3-70b-versatile", temperature=0)

# We added the new tool to the list!
tools = [add_medication_tool, log_fitness_tool]

agent_executor = create_react_agent(llm, tools)

def chat_with_agent(user_input):
    try:
        # Updated the prompt so the AI knows it can track fitness now
        # UPGRADED SYSTEM PROMPT (Domain Specialization)
       # 🔥 UPGRADED STRICT SYSTEM PROMPT (Domain Guardrail)
        system_prompt = """You are a highly empathetic, professional Indian Healthcare AI Assistant. 
        Your job is to help patients track their medications, fitness logs, and symptoms. 
        
        🚨 STRICT RULE: You are restricted to answering ONLY questions related to healthcare, medicine, fitness, hygiene, and wellness. 
        If the user asks about politics, general knowledge, movies, coding, math, or ANY non-health topic, you MUST strictly refuse to answer.
        Instead, reply politely with exactly this: "I am a specialized Health & Wellness Assistant. I can only help you with medical, fitness, and health-related queries."
        
        When users ask for general wellness advice, provide culturally relevant Indian suggestions (like Yoga, Dal, Paneer). 
        Always be medically safe and advise consulting a real doctor for serious issues. 
        Strictly use your tools to save data to the database when requested."""
        response = agent_executor.invoke({
            "messages": [
                ("system", system_prompt),
                ("user", user_input)
            ]
        })
        return response["messages"][-1].content
    except Exception as e:
        return f"Error connecting to AI: {str(e)}"

import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage
from db.database import add_medicine

# load env
load_dotenv()

# get API key
llm = ChatOpenAI(
    temperature=0,
    openai_api_key=os.getenv("OPENAI_API_KEY")
)

def process_input(user_input):
    prompt = f"""
    Extract medicine name and time from this sentence:
    "{user_input}"

    Respond ONLY in this format:
    medicine: <name>
    time: <time>
    """

    response = llm.invoke([HumanMessage(content=prompt)])
    output = response.content.lower()

    try:
        med_name = output.split("medicine:")[1].split("\n")[0].strip()
        med_time = output.split("time:")[1].strip()

        add_medicine(med_name, med_time)

        return f"✅ Added {med_name} at {med_time}"

    except:
        return "❌ Couldn't understand. Try again."
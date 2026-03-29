import os
import re
from datetime import datetime
from dotenv import load_dotenv
from google import genai
from db.database import add_medicine, add_reminder

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

MODEL_CANDIDATES = [
    "gemini-3-flash-preview",
    "gemini-2.5-flash",
    "gemini-2.5-pro",
]

def _call_gemini(prompt: str) -> str:
    last_error = None
    for model_name in MODEL_CANDIDATES:
        try:
            response = client.models.generate_content(
                model=model_name,
                contents=prompt,
            )
            return (response.text or "").strip()
        except Exception as e:
            last_error = e
    raise last_error

def process_input(user_input: str) -> str:
    text = user_input.lower().strip()

    # Fast path for simple inputs like: take dolo at 9 pm
    pattern = r"^(take|add)?\s*(\w+)\s*at\s*(.+)$"
    match = re.search(pattern, text)

    if match and "," not in text and len(text.split()) <= 5:
        med_name = match.group(2)
        med_time = match.group(3).strip()

        add_medicine(med_name, med_time)

        try:
            now = datetime.now()
            reminder_dt = datetime.strptime(med_time, "%I %p")
            reminder_dt = reminder_dt.replace(
                year=now.year,
                month=now.month,
                day=now.day
            )
            add_reminder(med_name, reminder_dt.isoformat())
        except Exception:
            pass

        return f"✅ Added {med_name} at {med_time} + reminder set"

    # AI path for complex inputs
    try:
        prompt = f"""
Extract medicine name and time from this sentence:
"{user_input}"

Respond ONLY in this format:
medicine: <name>
time: <time>
advice: <short line>
"""

        output = _call_gemini(prompt).lower()

        med_name = output.split("medicine:")[1].split("\n")[0].strip()
        med_time = output.split("time:")[1].split("\n")[0].strip()

        advice = ""
        if "advice:" in output:
            advice = output.split("advice:")[1].strip()

        add_medicine(med_name, med_time)

        try:
            now = datetime.now()
            reminder_dt = datetime.strptime(med_time, "%I %p")
            reminder_dt = reminder_dt.replace(
                year=now.year,
                month=now.month,
                day=now.day
            )
            add_reminder(med_name, reminder_dt.isoformat())
        except Exception:
            pass

        if advice:
            return f"✅ Added {med_name} at {med_time} + reminder set\n💡 {advice}"
        return f"✅ Added {med_name} at {med_time} + reminder set"

    except Exception as e:
        return f"❌ Error: {str(e)}"

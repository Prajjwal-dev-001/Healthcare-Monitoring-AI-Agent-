import streamlit as st
from datetime import datetime

from db.database import (
    add_medicine,
    get_medicines,
    add_reminder,
    get_reminders,
    mark_reminder_taken,
    delete_reminder,
    get_due_reminders
)

from agent.agent import process_input

st.title("Healthcare AI Agent 🏥")

# -------------------------
# Add Medicine
# -------------------------
st.header("Add Medication 💊")

med_name = st.text_input("Medicine Name")
med_time = st.text_input("Time (e.g., 8 PM)")

if st.button("Add Medicine"):
    if med_name and med_time:
        add_medicine(med_name, med_time)
        st.success("Medicine added successfully!")
        st.rerun()
    else:
        st.warning("Please fill all fields")

# -------------------------
# Show Medicines
# -------------------------
st.header("Your Medications 📋")

meds = get_medicines()

if meds:
    for med in meds:
        st.write(f"{med[1]} at {med[2]}")
else:
    st.info("No medicines added yet.")

# -------------------------
# Reminder System
# -------------------------
st.divider()
st.header("Medication Reminder 🔔")

rem_name = st.text_input("Medicine Name for Reminder", key="rem_name")

col1, col2 = st.columns(2)
with col1:
    rem_date = st.date_input("Reminder Date", value=datetime.now().date(), key="rem_date")
with col2:
    rem_time = st.time_input(
        "Reminder Time",
        value=datetime.now().time().replace(second=0, microsecond=0),
        key="rem_time"
    )

if st.button("Save Reminder"):
    if rem_name.strip():
        reminder_dt = datetime.combine(rem_date, rem_time)
        add_reminder(rem_name.strip(), reminder_dt.isoformat())
        st.success("Reminder saved successfully!")
        st.rerun()
    else:
        st.warning("Please enter medicine name")

due_reminders = get_due_reminders()

st.subheader("Due Reminders ⏰")
if due_reminders:
    for r in due_reminders:
        rid, med_name, reminder_at, status = r
        dt = datetime.fromisoformat(reminder_at)
        st.warning(f"⏰ {med_name} — {dt.strftime('%d %b %Y, %I:%M %p')}")
else:
    st.success("No due reminders right now.")

st.subheader("All Reminders 📅")
reminders = get_reminders()

if reminders:
    for r in reminders:
        rid, med_name, reminder_at, status = r
        dt = datetime.fromisoformat(reminder_at)

        st.write(f"**{med_name}** — {dt.strftime('%d %b %Y, %I:%M %p')} — {status}")

        c1, c2 = st.columns(2)
        with c1:
            if status != "taken":
                if st.button("Mark as taken", key=f"taken_{rid}"):
                    mark_reminder_taken(rid)
                    st.success("Marked as taken.")
                    st.rerun()
        with c2:
            if st.button("Delete", key=f"delete_{rid}"):
                delete_reminder(rid)
                st.success("Deleted.")
                st.rerun()
else:
    st.info("No reminders saved yet.")

# -------------------------
# AI Assistant
# -------------------------
st.divider()
st.header("AI Assistant 🤖")

user_query = st.text_input("Type like: Take Paracetamol at 8 PM")

if st.button("Ask AI"):
    if user_query:
        with st.spinner("AI is thinking... 🤖"):
            response = process_input(user_query)

        st.success(response)
        st.rerun()  
    else:
        st.warning("Please enter something!")

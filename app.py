import streamlit as st
from db.database import add_medicine, get_medicines

st.title("Healthcare AI Agent 🏥")

# Add Medicine
st.header("Add Medication 💊")

med_name = st.text_input("Medicine Name")
med_time = st.text_input("Time (e.g., 8 PM)")

if st.button("Add Medicine"):
    if med_name and med_time:
        add_medicine(med_name, med_time)
        st.success("Medicine added successfully!")
    else:
        st.warning("Please fill all fields")

# Show Medicines
st.header("Your Medications 📋")

meds = get_medicines()

for med in meds:
    st.write(f"{med[1]} at {med[2]}")

from agent.agent import process_input

st.header("AI Assistant 🤖")

user_query = st.text_input("Type like: Take Paracetamol at 8 PM")

if st.button("Ask AI"):
    if user_query:
        response = process_input(user_query)
        st.success(response)
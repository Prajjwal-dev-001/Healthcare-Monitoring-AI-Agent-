import streamlit as st
import pandas as pd
import database as db
import agent

# Page Setup
st.set_page_config(page_title="AI Health Assistant", page_icon="🩺", layout="wide")
st.title("🩺 Personal Healthcare Monitor")
st.markdown("Welcome to your AI-powered health tracking platform. (Track A)")

# Sidebar (Same as before)
with st.sidebar:
    st.header("📊 Health Dashboard")
    st.info("Agent Status: Online 🟢 (Powered by Groq)")
    
    st.subheader("Your Current Medications")
    meds = db.get_all_medicines()
    if meds:
        for med in meds:
            st.success(f"💊 **{med[1]}** (Time: {med[2]})")
    else:
        st.info("No medications tracked yet.")
        
    st.divider()
    
    st.subheader("🏃‍♂️ Recent Fitness Logs")
    fitness_logs = db.get_recent_fitness_logs()
    if fitness_logs:
        for log in fitness_logs:
            st.warning(f"**{log[0]}** for {log[1]} (Logged: {log[2]})")
    else:
        st.info("No fitness activities logged yet.")

# 🔥 NEW: UI Tabs for Professional Look
tab1, tab2 = st.tabs(["💬 Chat Assistant", "📈 Health Analytics"])

# --- TAB 1: Chat Assistant ---
with tab1:
    st.subheader("Chat with your Health Assistant")

    if "messages" not in st.session_state:
        st.session_state.messages = [{"role": "assistant", "content": "Hello! I am your Health Assistant. Tell me which medicine to add, or log your recent workout!"}]

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    if prompt := st.chat_input("E.g., I ran for 45 minutes this morning"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                response = agent.chat_with_agent(prompt)
                st.markdown(response)
                st.session_state.messages.append({"role": "assistant", "content": response})
                
        st.rerun()

# --- TAB 2: Analytics & Graphs ---
# --- TAB 2: Analytics & Graphs ---
with tab2:
    st.subheader("Workout Frequency Tracker")
    chart_data = db.get_fitness_data_for_chart()
    
    if chart_data:
        # SQLite data ko Pandas me convert kar rahe hain graph ke liye
        df = pd.DataFrame(chart_data, columns=["Date", "Workouts"])
        df.set_index("Date", inplace=True)
        
        # Streamlit  inbuilt Bar Chart
        st.bar_chart(df)
        st.info("💡 This chart shows how many times you worked out each day.")
        
        # 🔥 NEW: Export to CSV Feature
        st.divider()
        st.subheader("📥 Export Your Data")
        csv_data = df.to_csv().encode('utf-8')
        st.download_button(
            label="Download Fitness Data (CSV)",
            data=csv_data,
            file_name="my_fitness_report.csv",
            mime="text/csv",
        )
    else:
        st.info("Not enough data to show analytics yet. Go to the Chat tab and log a workout!")

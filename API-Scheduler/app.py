import streamlit as st
from scheduler import start_scheduler, validate_time_format

st.set_page_config(page_title="API Scheduler", layout="centered")

# ---------------- CLEAN UI ----------------
st.markdown("""
<style>
body {
    background-color: white;
    color: black;
}
.stTextInput input {
    background-color: #f5f5f5;
    color: black;
}
.stButton button {
    background-color: black;
    color: white;
}
</style>
""", unsafe_allow_html=True)

st.title("API Scheduler")

st.write("Schedule API calls at specific times")

# session state
if "tasks" not in st.session_state:
    st.session_state.tasks = []

# inputs
url = st.text_input("Enter URL").strip()
time_input = st.text_input("Enter Time (HH:MM:SS)").strip()

# NEW: browser open
open_browser = st.checkbox("Open in browser on success")

# add task
if st.button("Add Task"):
    if url and time_input:
        if validate_time_format(time_input):
            st.session_state.tasks.append((url, time_input))
            st.success("Task added")
        else:
            st.error("Invalid time format")
    else:
        st.warning("Enter URL and Time")

# show tasks
st.subheader("Scheduled Tasks")

if st.session_state.tasks:
    for i, task in enumerate(st.session_state.tasks, 1):
        st.write(f"{i}. {task[0]} at {task[1]}")
else:
    st.write("No tasks added")

# start scheduler
if st.button("Start Scheduler"):
    if st.session_state.tasks:
        start_scheduler(st.session_state.tasks, open_browser)
        st.success("Scheduler started")

        # prevent duplicate run
        st.session_state.tasks = []
    else:
        st.warning("No tasks to schedule")


import streamlit as st
import uuid

st.set_page_config(page_title="DailyTask - TODO", page_icon="check.png", layout="wide")


if 'tasks' not in st.session_state:
    st.session_state.tasks = []
if 'incompleted_tasks' not in st.session_state:
    st.session_state.incompleted_tasks = []
if 'priority_tasks' not in st.session_state:
    st.session_state.priority_tasks = []
if 'completed_count' not in st.session_state:
    st.session_state.completed_count = 0
if 'total_tasks' not in st.session_state:
    st.session_state.total_tasks = 0

st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Home", "Task Analytics",  "About"])

if page == "Home":
    st.title("Complete Growth Mindset - To-Do List")

    task_input = st.text_input("Enter a new task:")
    priority = st.selectbox("Select Priority:", ["High", "Medium", "Low"], index=1)
    recurring = st.selectbox("Repeat Task:", ["None", "Daily", "Weekly", "Monthly"], index=0)
    
    if st.button("Add Task") and task_input:
        priority_color = "red" if priority == "High" else "orange" if priority == "Medium" else "yellow"
        st.session_state.tasks.append({
            "id": str(uuid.uuid4()), "task": task_input, "completed": False, 
            "priority": priority, "color": priority_color, "recurring": recurring
        })
        st.session_state.total_tasks += 1


    st.subheader("Your Tasks")
    for index, task in enumerate(st.session_state.tasks):
        col1, col2, col3, col4 = st.columns([0.3, 5, 1, 1])
        task_color = "green" if task['completed'] else "white"
        recurrence_text = f"<small>{task['recurring']}</small>" if task['recurring'] != "None" else ""
        with col1:
            priority_dot = "🔴" if task['priority'] == "High" else "🟠" if task['priority'] == "Medium" else "🟡"
            st.markdown(f"<span style='font-size:20px;'>{priority_dot}</span>", unsafe_allow_html=True)
        with col2:
            st.markdown(f"<span style='color:{task_color}; font-weight:bold;'>{'✔️' if task['completed'] else '❌'} {task['task']} {recurrence_text}</span>", unsafe_allow_html=True)
        with col3:
            if st.button("✅", key=f"complete_{task['id']}"):
                st.session_state.tasks[index]['completed'] = not task['completed']
                if task['completed']:
                    st.session_state.completed_count += 1
                st.rerun()
        with col4:
            if st.button("❌", key=f"delete_{task['id']}"):
                st.session_state.incompleted_tasks.append(task)
                st.session_state.tasks = [t for t in st.session_state.tasks if t['id'] != task['id']]
                st.rerun()

    # Display incompleted tasks
    if st.session_state.incompleted_tasks:
        st.subheader("INCOMPLETED TASKS")
        for task in st.session_state.incompleted_tasks:
            st.markdown(f"<span style='color:red; font-weight:bold;'>❌ {task['task']}</span>", unsafe_allow_html=True)

    if st.button("Clear All"):
        st.session_state.tasks = []
        st.session_state.incompleted_tasks = []
        st.session_state.priority_tasks = []
        st.session_state.completed_count = 0
        st.session_state.total_tasks = 0
        st.rerun()

elif page == "Task Analytics":
    st.title("📊 Task Analytics")
    st.write(f"Total Tasks: {st.session_state.total_tasks}")
    st.write(f"Completed Tasks: {st.session_state.completed_count}")
    st.write("Cancelled Tasks: " + str(len(st.session_state.incompleted_tasks)))
    if st.session_state.total_tasks > 0:
        completion_rate = (st.session_state.completed_count / st.session_state.total_tasks) * 100
        st.write(f"Completion Rate: {completion_rate:.2f}%")
    


elif page == "About":
    st.title("📌 About the AI To-Do List Manager")
    
    st.markdown("""
        This **AI-Powered To-Do List application** helps users efficiently manage their daily tasks.  
        It allows you to **add, track, and prioritize** tasks with **smart suggestions** and **due date tracking** to keep you on top of your schedule.

        ### 🔹 **Key Features:**
        - ✅ **Priority Levels:** High, Medium, Low.
        - ✅ **Task Completion Monitoring.**
        - ✅ **Task Analytics** to track progress.
        - ✅ **Pomodoro Timer** to enhance focus.

        🚀 Stay productive and take control of your time with this AI-enhanced To-Do List app!
    """, unsafe_allow_html=True)


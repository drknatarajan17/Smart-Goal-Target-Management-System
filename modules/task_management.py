import streamlit as st
import pandas as pd
import os
from datetime import date

def task_management():

    st.title("✅ Task Management")

    task_file = "data/tasks.csv"
    goal_file = "data/goals.csv"

    # ----------------------------
    # Load Goals
    # ----------------------------

    if os.path.exists(goal_file):
        goals = pd.read_csv(goal_file)
        goal_list = goals["Goal Name"].tolist()
    else:
        goal_list = []

    # ----------------------------
    # Load Tasks
    # ----------------------------

    if os.path.exists(task_file):
        tasks = pd.read_csv(task_file)
    else:
        tasks = pd.DataFrame(columns=[
            "Task ID",
            "Goal",
            "Task Name",
            "Description",
            "Priority",
            "Due Date",
            "Progress",
            "Status"
        ])

    # ----------------------------
    # Add Task
    # ----------------------------

    st.subheader("➕ Add New Task")

    with st.form("task_form"):

        goal = st.selectbox(
            "Select Goal",
            goal_list if goal_list else ["No Goal Available"]
        )

        task_name = st.text_input("Task Name")

        description = st.text_area("Description")

        priority = st.selectbox(
            "Priority",
            ["High","Medium","Low"]
        )

        due_date = st.date_input(
            "Due Date",
            date.today()
        )

        progress = st.slider(
            "Progress %",
            0,
            100,
            0
        )

        status = st.selectbox(
            "Status",
            [
                "Pending",
                "In Progress",
                "Completed",
                "On Hold"
            ]
        )

        submit = st.form_submit_button("Save Task")

    if submit:

        task_id = "TASK-" + str(len(tasks)+1).zfill(4)

        new = pd.DataFrame([{
            "Task ID":task_id,
            "Goal":goal,
            "Task Name":task_name,
            "Description":description,
            "Priority":priority,
            "Due Date":due_date,
            "Progress":progress,
            "Status":status
        }])

        tasks = pd.concat([tasks,new],ignore_index=True)

        os.makedirs("data",exist_ok=True)

        tasks.to_csv(task_file,index=False)

        st.success("Task Added Successfully")

    st.divider()

    # ----------------------------
    # Search Task
    # ----------------------------

    st.subheader("🔍 Search Tasks")

    keyword = st.text_input("Search Task")

    display = tasks.copy()

    if keyword:

        display = display[
            display["Task Name"].str.contains(
                keyword,
                case=False,
                na=False
            )
        ]

    st.dataframe(display,use_container_width=True)

    st.divider()

    # ----------------------------
    # Filter
    # ----------------------------

    st.subheader("📂 Filter Tasks")

    c1,c2 = st.columns(2)

    with c1:

        status_filter = st.selectbox(
            "Status Filter",
            ["All"] + list(tasks["Status"].unique())
            if not tasks.empty else ["All"]
        )

    with c2:

        priority_filter = st.selectbox(
            "Priority Filter",
            ["All"] + list(tasks["Priority"].unique())
            if not tasks.empty else ["All"]
        )

    filtered = tasks.copy()

    if status_filter != "All":

        filtered = filtered[
            filtered["Status"]==status_filter
        ]

    if priority_filter != "All":

        filtered = filtered[
            filtered["Priority"]==priority_filter
        ]

    st.dataframe(filtered,use_container_width=True)

    st.divider()

    # ----------------------------
    # KPI Dashboard
    # ----------------------------

    total = len(tasks)

    completed = len(
        tasks[tasks["Status"]=="Completed"]
    )

    pending = len(
        tasks[tasks["Status"]=="Pending"]
    )

    progress_avg = 0

    if total>0:

        progress_avg = round(
            tasks["Progress"].mean(),
            2
        )

    c1,c2,c3,c4 = st.columns(4)

    c1.metric("Total Tasks",total)

    c2.metric("Completed",completed)

    c3.metric("Pending",pending)

    c4.metric(
        "Average Progress",
        str(progress_avg)+"%"
    )

    st.divider()

    # ----------------------------
    # Charts
    # ----------------------------

    st.subheader("📊 Task Analytics")

    if not tasks.empty:

        st.bar_chart(
            tasks["Status"].value_counts()
        )

        st.bar_chart(
            tasks["Priority"].value_counts()
        )

        st.bar_chart(
            tasks.set_index(
                "Task Name"
            )["Progress"]
        )

    st.divider()

    # ----------------------------
    # Pending Tasks
    # ----------------------------

    st.subheader("📌 Pending Tasks")

    pending_tasks = tasks[
        tasks["Status"]!="Completed"
    ]

    st.dataframe(
        pending_tasks,
        use_container_width=True
    )

    st.divider()

    # ----------------------------
    # Download
    # ----------------------------

    st.download_button(
        "📥 Download Task Report",
        tasks.to_csv(index=False).encode("utf-8"),
        "tasks.csv",
        "text/csv"
    )

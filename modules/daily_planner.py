import streamlit as st
import pandas as pd
import os
from datetime import date

def daily_planner():

    st.title("📅 Daily Planner")

    file = "data/daily_planner.csv"

    # ----------------------------
    # Load Data
    # ----------------------------

    if os.path.exists(file):
        df = pd.read_csv(file)
    else:
        df = pd.DataFrame(columns=[
            "Task ID",
            "Date",
            "Time Slot",
            "Task",
            "Priority",
            "Status",
            "Remarks"
        ])

    # ----------------------------
    # Add Daily Task
    # ----------------------------

    st.subheader("➕ Add Daily Task")

    with st.form("daily_form"):

        task_date = st.date_input(
            "Date",
            date.today()
        )

        time_slot = st.selectbox(
            "Time Slot",
            [
                "🌅 Morning",
                "🌞 Afternoon",
                "🌇 Evening",
                "🌙 Night"
            ]
        )

        task = st.text_input("Task")

        priority = st.selectbox(
            "Priority",
            [
                "High",
                "Medium",
                "Low"
            ]
        )

        status = st.selectbox(
            "Status",
            [
                "Pending",
                "Completed",
                "Missed"
            ]
        )

        remarks = st.text_area("Remarks")

        submit = st.form_submit_button("Save")

    if submit:

        task_id = "DAY-" + str(len(df)+1).zfill(4)

        new = pd.DataFrame([{
            "Task ID":task_id,
            "Date":task_date,
            "Time Slot":time_slot,
            "Task":task,
            "Priority":priority,
            "Status":status,
            "Remarks":remarks
        }])

        df = pd.concat([df,new],ignore_index=True)

        os.makedirs("data",exist_ok=True)

        df.to_csv(file,index=False)

        st.success("Daily Task Added Successfully")

    st.divider()

    # ----------------------------
    # Today's Schedule
    # ----------------------------

    st.subheader("📌 Today's Schedule")

    today = str(date.today())

    today_tasks = df[df["Date"]==today]

    st.dataframe(
        today_tasks,
        use_container_width=True
    )

    st.divider()

    # ----------------------------
    # Search Task
    # ----------------------------

    st.subheader("🔍 Search Task")

    keyword = st.text_input("Enter Task Name")

    display = df.copy()

    if keyword:

        display = display[
            display["Task"].str.contains(
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

    st.subheader("📂 Filter")

    c1,c2 = st.columns(2)

    with c1:

        slot = st.selectbox(
            "Time Slot",
            ["All"] +
            list(df["Time Slot"].unique())
            if not df.empty else ["All"]
        )

    with c2:

        status_filter = st.selectbox(
            "Status",
            ["All"] +
            list(df["Status"].unique())
            if not df.empty else ["All"]
        )

    filtered = df.copy()

    if slot!="All":

        filtered = filtered[
            filtered["Time Slot"]==slot
        ]

    if status_filter!="All":

        filtered = filtered[
            filtered["Status"]==status_filter
        ]

    st.dataframe(
        filtered,
        use_container_width=True
    )

    st.divider()

    # ----------------------------
    # KPI Dashboard
    # ----------------------------

    total = len(df)

    completed = len(
        df[df["Status"]=="Completed"]
    )

    pending = len(
        df[df["Status"]=="Pending"]
    )

    missed = len(
        df[df["Status"]=="Missed"]
    )

    productivity = 0

    if total>0:

        productivity = round(
            (completed/total)*100,
            2
        )

    c1,c2,c3,c4 = st.columns(4)

    c1.metric(
        "Total Tasks",
        total
    )

    c2.metric(
        "Completed",
        completed
    )

    c3.metric(
        "Pending",
        pending
    )

    c4.metric(
        "Productivity",
        str(productivity)+"%"
    )

    st.divider()

    # ----------------------------
    # Charts
    # ----------------------------

    st.subheader("📊 Daily Analytics")

    if not df.empty:

        st.bar_chart(
            df["Time Slot"].value_counts()
        )

        st.bar_chart(
            df["Priority"].value_counts()
        )

        st.bar_chart(
            df["Status"].value_counts()
        )

    st.divider()

    # ----------------------------
    # Productivity Meter
    # ----------------------------

    st.subheader("🚀 Daily Productivity")

    st.progress(productivity/100)

    if productivity >= 90:

        st.success("🌟 Excellent! You completed almost everything today.")

    elif productivity >= 70:

        st.info("👍 Good progress. Keep pushing!")

    elif productivity >= 50:

        st.warning("⚠ Try completing more important tasks.")

    else:

        st.error("❌ You need better planning tomorrow.")

    st.divider()

    # ----------------------------
    # Export Report
    # ----------------------------

    st.download_button(
        "📥 Download Daily Planner",
        df.to_csv(index=False).encode("utf-8"),
        "daily_planner.csv",
        "text/csv"
    )

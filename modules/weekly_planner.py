import streamlit as st
import pandas as pd
import os
from datetime import date

def weekly_planner():

    st.title("📅 Weekly Planner")

    file = "data/weekly_planner.csv"

    # ---------------------------------------
    # Load Data
    # ---------------------------------------

    if os.path.exists(file):
        df = pd.read_csv(file)
    else:
        df = pd.DataFrame(columns=[
            "Task ID",
            "Day",
            "Task",
            "Category",
            "Priority",
            "Status",
            "Remarks"
        ])

    # ---------------------------------------
    # Add Weekly Task
    # ---------------------------------------

    st.subheader("➕ Add Weekly Plan")

    with st.form("weekly_form"):

        day = st.selectbox(
            "Day",
            [
                "Monday",
                "Tuesday",
                "Wednesday",
                "Thursday",
                "Friday",
                "Saturday",
                "Sunday"
            ]
        )

        task = st.text_input("Task")

        category = st.selectbox(
            "Category",
            [
                "Career",
                "Business",
                "Finance",
                "Health",
                "Learning",
                "Family",
                "Personal",
                "Politics",
                "Travel"
            ]
        )

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
                "In Progress",
                "Completed"
            ]
        )

        remarks = st.text_area("Remarks")

        submit = st.form_submit_button("Save Weekly Task")

    if submit:

        task_id = "WEEK-" + str(len(df)+1).zfill(4)

        new = pd.DataFrame([{
            "Task ID":task_id,
            "Day":day,
            "Task":task,
            "Category":category,
            "Priority":priority,
            "Status":status,
            "Remarks":remarks
        }])

        df = pd.concat([df,new],ignore_index=True)

        os.makedirs("data",exist_ok=True)

        df.to_csv(file,index=False)

        st.success("Weekly Plan Saved Successfully")

    st.divider()

    # ---------------------------------------
    # Weekly Schedule
    # ---------------------------------------

    st.subheader("📋 Weekly Schedule")

    st.dataframe(df,use_container_width=True)

    st.divider()

    # ---------------------------------------
    # Search
    # ---------------------------------------

    st.subheader("🔍 Search Weekly Task")

    keyword = st.text_input("Search")

    if keyword:

        search = df[
            df["Task"].str.contains(
                keyword,
                case=False,
                na=False
            )
        ]

        st.dataframe(search,use_container_width=True)

    st.divider()

    # ---------------------------------------
    # Filter
    # ---------------------------------------

    st.subheader("📂 Filter Tasks")

    c1,c2 = st.columns(2)

    with c1:

        day_filter = st.selectbox(
            "Day Filter",
            ["All"] + list(df["Day"].unique())
            if not df.empty else ["All"]
        )

    with c2:

        status_filter = st.selectbox(
            "Status Filter",
            ["All"] + list(df["Status"].unique())
            if not df.empty else ["All"]
        )

    filtered = df.copy()

    if day_filter != "All":
        filtered = filtered[
            filtered["Day"] == day_filter
        ]

    if status_filter != "All":
        filtered = filtered[
            filtered["Status"] == status_filter
        ]

    st.dataframe(filtered,use_container_width=True)

    st.divider()

    # ---------------------------------------
    # KPI Dashboard
    # ---------------------------------------

    total = len(df)

    completed = len(
        df[df["Status"]=="Completed"]
    )

    pending = len(
        df[df["Status"]=="Pending"]
    )

    progress = 0

    if total>0:
        progress = round(
            completed/total*100,
            2
        )

    c1,c2,c3,c4 = st.columns(4)

    c1.metric("Total Plans",total)
    c2.metric("Completed",completed)
    c3.metric("Pending",pending)
    c4.metric("Weekly Score",str(progress)+" %")

    st.divider()

    # ---------------------------------------
    # Weekly Charts
    # ---------------------------------------

    st.subheader("📊 Weekly Analytics")

    if not df.empty:

        st.bar_chart(
            df["Day"].value_counts()
        )

        st.bar_chart(
            df["Category"].value_counts()
        )

        st.bar_chart(
            df["Priority"].value_counts()
        )

        st.bar_chart(
            df["Status"].value_counts()
        )

    st.divider()

    # ---------------------------------------
    # Weekly Productivity Meter
    # ---------------------------------------

    st.subheader("🚀 Weekly Productivity")

    st.progress(progress/100)

    if progress>=90:

        st.success("Excellent Week! 🎉")

    elif progress>=70:

        st.info("Good Progress 👍")

    elif progress>=50:

        st.warning("Average Performance")

    else:

        st.error("Needs Improvement")

    st.divider()

    # ---------------------------------------
    # Weekly Summary
    # ---------------------------------------

    st.subheader("📈 Weekly Summary")

    if not df.empty:

        summary = df.groupby(
            "Category"
        ).size().reset_index(name="Tasks")

        st.dataframe(
            summary,
            use_container_width=True
        )

    st.divider()

    # ---------------------------------------
    # Download Report
    # ---------------------------------------

    st.download_button(
        "📥 Download Weekly Planner",
        df.to_csv(index=False).encode("utf-8"),
        "weekly_planner.csv",
        "text/csv"
    )

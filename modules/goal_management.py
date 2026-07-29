import streamlit as st
import pandas as pd
import os
from datetime import date

def goal_management():

    st.title("🎯 Goal Management")

    file = "data/goals.csv"

    # -----------------------------
    # Load Existing Data
    # -----------------------------

    if os.path.exists(file):
        df = pd.read_csv(file)
    else:
        df = pd.DataFrame(columns=[
            "Goal ID",
            "Goal Name",
            "Category",
            "Description",
            "Priority",
            "Start Date",
            "Target Date",
            "Progress",
            "Status"
        ])

    # -----------------------------
    # Add New Goal
    # -----------------------------

    st.subheader("➕ Add New Goal")

    with st.form("goal_form"):

        goal_name = st.text_input("Goal Name")

        category = st.selectbox(
            "Category",
            [
                "Career",
                "Business",
                "Finance",
                "Health",
                "Education",
                "Politics",
                "Personal",
                "Family",
                "Travel",
                "Other"
            ]
        )

        description = st.text_area("Description")

        priority = st.selectbox(
            "Priority",
            [
                "High",
                "Medium",
                "Low"
            ]
        )

        start_date = st.date_input(
            "Start Date",
            date.today()
        )

        target_date = st.date_input(
            "Target Date"
        )

        progress = st.slider(
            "Progress (%)",
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

        submit = st.form_submit_button("Save Goal")

    if submit:

        goal_id = "GOAL-" + str(len(df)+1).zfill(4)

        new = pd.DataFrame([{
            "Goal ID":goal_id,
            "Goal Name":goal_name,
            "Category":category,
            "Description":description,
            "Priority":priority,
            "Start Date":start_date,
            "Target Date":target_date,
            "Progress":progress,
            "Status":status
        }])

        df = pd.concat([df,new],ignore_index=True)

        os.makedirs("data",exist_ok=True)

        df.to_csv(file,index=False)

        st.success("Goal Added Successfully")

    st.divider()

    # -----------------------------
    # Search Goal
    # -----------------------------

    st.subheader("🔍 Search Goal")

    keyword = st.text_input("Search by Goal Name")

    display = df.copy()

    if keyword:

        display = display[
            display["Goal Name"].str.contains(
                keyword,
                case=False,
                na=False
            )
        ]

    st.dataframe(
        display,
        use_container_width=True
    )

    st.divider()

    # -----------------------------
    # Filter
    # -----------------------------

    st.subheader("📂 Filter Goals")

    col1,col2 = st.columns(2)

    with col1:

        category_filter = st.selectbox(
            "Category",
            ["All"] + list(df["Category"].unique())
            if not df.empty else ["All"]
        )

    with col2:

        status_filter = st.selectbox(
            "Status",
            ["All"] + list(df["Status"].unique())
            if not df.empty else ["All"]
        )

    filtered = df.copy()

    if category_filter!="All":
        filtered = filtered[
            filtered["Category"]==category_filter
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

    # -----------------------------
    # Goal Summary
    # -----------------------------

    st.subheader("📊 Goal Summary")

    total = len(df)

    completed = len(
        df[df["Status"]=="Completed"]
    )

    pending = len(
        df[df["Status"]=="Pending"]
    )

    progress_avg = 0

    if total>0:

        progress_avg = round(
            df["Progress"].mean(),
            2
        )

    c1,c2,c3,c4 = st.columns(4)

    c1.metric(
        "Total Goals",
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
        "Average Progress",
        str(progress_avg)+"%"
    )

    st.divider()

    # -----------------------------
    # Charts
    # -----------------------------

    st.subheader("📈 Goal Analytics")

    if not df.empty:

        st.bar_chart(
            df["Category"].value_counts()
        )

        st.bar_chart(
            df.set_index(
                "Goal Name"
            )["Progress"]
        )

    st.divider()

    # -----------------------------
    # Download
    # -----------------------------

    st.download_button(
        "📥 Download Goals CSV",
        df.to_csv(index=False).encode(),
        "goals.csv",
        "text/csv"
    )

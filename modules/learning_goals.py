import streamlit as st
import pandas as pd
import os
from datetime import date

def learning_goals():

    st.title("📚 Learning Goals & Skill Tracker")

    file = "data/learning_goals.csv"

    # -------------------------------------
    # Load Data
    # -------------------------------------

    if os.path.exists(file):
        df = pd.read_csv(file)
    else:
        df = pd.DataFrame(columns=[
            "Learning ID",
            "Date",
            "Category",
            "Course",
            "Platform",
            "Skill",
            "Study Hours",
            "Progress",
            "Target Date",
            "Status",
            "Certificate",
            "Remarks"
        ])

    # -------------------------------------
    # Add Learning Goal
    # -------------------------------------

    st.subheader("➕ Add Learning Goal")

    with st.form("learning_form"):

        learning_date = st.date_input(
            "Date",
            date.today()
        )

        category = st.selectbox(
            "Learning Category",
            [
                "Programming",
                "Artificial Intelligence",
                "Machine Learning",
                "Deep Learning",
                "Data Science",
                "Cyber Security",
                "Cloud Computing",
                "Electrical Engineering",
                "Electronics",
                "EV Technology",
                "Research",
                "Communication",
                "Management",
                "Business",
                "Politics",
                "Finance",
                "Language",
                "Certification",
                "Others"
            ]
        )

        course = st.text_input("Course / Book / Research Topic")

        platform = st.selectbox(
            "Platform",
            [
                "Coursera",
                "Udemy",
                "NPTEL",
                "Infosys Springboard",
                "YouTube",
                "MIT OCW",
                "GitHub",
                "IEEE",
                "Springer",
                "Self Learning",
                "Other"
            ]
        )

        skill = st.text_input("Skill")

        study_hours = st.number_input(
            "Study Hours",
            min_value=0.0,
            value=1.0
        )

        progress = st.slider(
            "Completion %",
            0,
            100,
            0
        )

        target_date = st.date_input(
            "Target Completion Date",
            date.today()
        )

        status = st.selectbox(
            "Status",
            [
                "Not Started",
                "In Progress",
                "Completed"
            ]
        )

        certificate = st.selectbox(
            "Certificate Earned",
            [
                "No",
                "Yes"
            ]
        )

        remarks = st.text_area("Remarks")

        submit = st.form_submit_button("Save Learning Goal")

    if submit:

        learning_id = "LEARN-" + str(len(df)+1).zfill(4)

        new = pd.DataFrame([{
            "Learning ID": learning_id,
            "Date": learning_date,
            "Category": category,
            "Course": course,
            "Platform": platform,
            "Skill": skill,
            "Study Hours": study_hours,
            "Progress": progress,
            "Target Date": target_date,
            "Status": status,
            "Certificate": certificate,
            "Remarks": remarks
        }])

        df = pd.concat([df, new], ignore_index=True)

        os.makedirs("data", exist_ok=True)
        df.to_csv(file, index=False)

        st.success("Learning Goal Saved Successfully!")

    st.divider()

    # -------------------------------------
    # Dashboard
    # -------------------------------------

    st.subheader("📊 Learning Dashboard")

    total = len(df)

    completed = len(
        df[df["Status"]=="Completed"]
    )

    progress_avg = 0

    hours = 0

    certificates = len(
        df[df["Certificate"]=="Yes"]
    )

    if total > 0:

        progress_avg = round(
            df["Progress"].mean(),
            2
        )

        hours = round(
            df["Study Hours"].sum(),
            2
        )

    c1,c2,c3,c4 = st.columns(4)

    c1.metric("Courses", total)
    c2.metric("Completed", completed)
    c3.metric("Study Hours", hours)
    c4.metric("Certificates", certificates)

    st.divider()

    # -------------------------------------
    # Learning Records
    # -------------------------------------

    st.subheader("📋 Learning Records")

    st.dataframe(df, use_container_width=True)

    st.divider()

    # -------------------------------------
    # Search
    # -------------------------------------

    keyword = st.text_input("🔍 Search")

    if keyword:

        search = df[
            df["Course"].astype(str).str.contains(
                keyword,
                case=False,
                na=False
            )
        ]

        st.dataframe(search, use_container_width=True)

    st.divider()

    # -------------------------------------
    # Charts
    # -------------------------------------

    st.subheader("📈 Learning Analytics")

    if not df.empty:

        st.bar_chart(
            df["Category"].value_counts()
        )

        st.bar_chart(
            df["Platform"].value_counts()
        )

        st.bar_chart(
            df["Status"].value_counts()
        )

        st.line_chart(
            df.set_index("Course")["Progress"]
        )

    st.divider()

    # -------------------------------------
    # AI Learning Coach
    # -------------------------------------

    st.subheader("🤖 AI Learning Coach")

    if progress_avg >= 90:

        st.success("Outstanding! You're mastering your learning goals.")

    elif progress_avg >= 70:

        st.info("Great progress. Continue learning consistently.")

    elif progress_avg >= 50:

        st.warning("Good start. Increase your daily study time.")

    else:

        st.error("Create a daily learning schedule to improve consistency.")

    st.divider()

    # -------------------------------------
    # Download
    # -------------------------------------

    st.download_button(
        "📥 Download Learning Report",
        df.to_csv(index=False).encode("utf-8"),
        "learning_goals.csv",
        "text/csv"
    )

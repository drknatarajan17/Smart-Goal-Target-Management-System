import streamlit as st
import pandas as pd
import os
from datetime import date

def career_goals():

    st.title("🚀 Career Goals & Professional Growth")

    file = "data/career_goals.csv"

    # -----------------------------------------
    # Load Data
    # -----------------------------------------

    if os.path.exists(file):
        df = pd.read_csv(file)
    else:
        df = pd.DataFrame(columns=[
            "Career ID",
            "Date",
            "Career Goal",
            "Category",
            "Organization",
            "Priority",
            "Target Date",
            "Progress",
            "Status",
            "Remarks"
        ])

    # -----------------------------------------
    # Add Career Goal
    # -----------------------------------------

    st.subheader("➕ Add Career Goal")

    with st.form("career_form"):

        goal_date = st.date_input("Date", date.today())

        goal = st.text_input(
            "Career Goal"
        )

        category = st.selectbox(
            "Category",
            [
                "Job",
                "Promotion",
                "Research",
                "Teaching",
                "Conference",
                "Publication",
                "Patent",
                "Certification",
                "Startup",
                "Business",
                "Politics",
                "Government Position",
                "Skill Development",
                "Higher Education",
                "Other"
            ]
        )

        organization = st.text_input(
            "Organization / Company"
        )

        priority = st.selectbox(
            "Priority",
            [
                "High",
                "Medium",
                "Low"
            ]
        )

        target = st.date_input(
            "Target Date",
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
                "Planned",
                "In Progress",
                "Completed",
                "Cancelled"
            ]
        )

        remarks = st.text_area("Remarks")

        submit = st.form_submit_button(
            "Save Career Goal"
        )

    if submit:

        career_id = "CAR-" + str(len(df)+1).zfill(4)

        new = pd.DataFrame([{
            "Career ID":career_id,
            "Date":goal_date,
            "Career Goal":goal,
            "Category":category,
            "Organization":organization,
            "Priority":priority,
            "Target Date":target,
            "Progress":progress,
            "Status":status,
            "Remarks":remarks
        }])

        df = pd.concat(
            [df,new],
            ignore_index=True
        )

        os.makedirs(
            "data",
            exist_ok=True
        )

        df.to_csv(
            file,
            index=False
        )

        st.success(
            "Career Goal Saved Successfully!"
        )

    st.divider()

    # -----------------------------------------
    # Dashboard
    # -----------------------------------------

    total = len(df)

    completed = len(
        df[df["Status"]=="Completed"]
    )

    inprogress = len(
        df[df["Status"]=="In Progress"]
    )

    avg_progress = 0

    if total>0:

        avg_progress = round(
            df["Progress"].mean(),
            2
        )

    c1,c2,c3,c4 = st.columns(4)

    c1.metric("Goals",total)
    c2.metric("Completed",completed)
    c3.metric("In Progress",inprogress)
    c4.metric("Average Progress",str(avg_progress)+" %")

    st.divider()

    # -----------------------------------------
    # Search
    # -----------------------------------------

    keyword = st.text_input(
        "🔍 Search Career Goal"
    )

    display = df.copy()

    if keyword:

        display = display[
            display["Career Goal"].str.contains(
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

    # -----------------------------------------
    # Filter
    # -----------------------------------------

    c1,c2 = st.columns(2)

    with c1:

        category_filter = st.selectbox(
            "Category",
            ["All"]+
            list(df["Category"].unique())
            if not df.empty else ["All"]
        )

    with c2:

        status_filter = st.selectbox(
            "Status",
            ["All"]+
            list(df["Status"].unique())
            if not df.empty else ["All"]
        )

    filtered = df.copy()

    if category_filter!="All":

        filtered = filtered[
            filtered["Category"]==
            category_filter
        ]

    if status_filter!="All":

        filtered = filtered[
            filtered["Status"]==
            status_filter
        ]

    st.dataframe(
        filtered,
        use_container_width=True
    )

    st.divider()

    # -----------------------------------------
    # Charts
    # -----------------------------------------

    st.subheader(
        "📊 Career Analytics"
    )

    if not df.empty:

        st.bar_chart(
            df["Category"].value_counts()
        )

        st.bar_chart(
            df["Status"].value_counts()
        )

        st.bar_chart(
            df.set_index(
                "Career Goal"
            )["Progress"]
        )

    st.divider()

    # -----------------------------------------
    # AI Career Coach
    # -----------------------------------------

    st.subheader(
        "🤖 AI Career Coach"
    )

    if avg_progress>=90:

        st.success(
            "Outstanding! You're achieving your career goals consistently."
        )

    elif avg_progress>=70:

        st.info(
            "Excellent progress. Continue building your professional profile."
        )

    elif avg_progress>=50:

        st.warning(
            "Good start. Focus on completing high-priority career goals."
        )

    else:

        st.error(
            "Create a structured monthly career development plan."
        )

    st.divider()

    # -----------------------------------------
    # Download
    # -----------------------------------------

    st.download_button(
        "📥 Download Career Report",
        df.to_csv(index=False).encode("utf-8"),
        "career_goals.csv",
        "text/csv"
    )

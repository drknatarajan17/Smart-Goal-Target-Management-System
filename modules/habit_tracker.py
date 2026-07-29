import streamlit as st
import pandas as pd
import os
from datetime import date

def habit_tracker():

    st.title("🔥 Habit Tracker")

    file = "data/habits.csv"

    # ----------------------------------
    # Load Data
    # ----------------------------------

    if os.path.exists(file):
        df = pd.read_csv(file)
    else:
        df = pd.DataFrame(columns=[
            "Habit ID",
            "Date",
            "Habit",
            "Target",
            "Achieved",
            "Unit",
            "Status",
            "Remarks"
        ])

    # ----------------------------------
    # Add Habit
    # ----------------------------------

    st.subheader("➕ Add Daily Habit")

    with st.form("habit_form"):

        habit_date = st.date_input(
            "Date",
            date.today()
        )

        habit = st.selectbox(
            "Habit",
            [
                "Exercise",
                "Walking",
                "Running",
                "Cycling",
                "Meditation",
                "Reading",
                "Coding",
                "Water Intake",
                "Sleep",
                "Learning",
                "Writing",
                "Prayer",
                "Other"
            ]
        )

        target = st.number_input(
            "Target",
            min_value=1,
            value=1
        )

        achieved = st.number_input(
            "Achieved",
            min_value=0,
            value=0
        )

        unit = st.selectbox(
            "Unit",
            [
                "Minutes",
                "Hours",
                "Pages",
                "Glasses",
                "KM",
                "Times"
            ]
        )

        remarks = st.text_area("Remarks")

        submit = st.form_submit_button("Save Habit")

    if submit:

        status = "Completed" if achieved >= target else "Pending"

        habit_id = "HAB-" + str(len(df)+1).zfill(4)

        new = pd.DataFrame([{
            "Habit ID":habit_id,
            "Date":habit_date,
            "Habit":habit,
            "Target":target,
            "Achieved":achieved,
            "Unit":unit,
            "Status":status,
            "Remarks":remarks
        }])

        df = pd.concat([df,new],ignore_index=True)

        os.makedirs("data",exist_ok=True)

        df.to_csv(file,index=False)

        st.success("Habit Saved Successfully")

    st.divider()

    # ----------------------------------
    # Today's Habits
    # ----------------------------------

    st.subheader("📅 Today's Habits")

    today = str(date.today())

    today_df = df[df["Date"]==today]

    st.dataframe(today_df,use_container_width=True)

    st.divider()

    # ----------------------------------
    # Search Habit
    # ----------------------------------

    st.subheader("🔍 Search Habit")

    keyword = st.text_input("Search")

    display = df.copy()

    if keyword:

        display = display[
            display["Habit"].str.contains(
                keyword,
                case=False,
                na=False
            )
        ]

    st.dataframe(display,use_container_width=True)

    st.divider()

    # ----------------------------------
    # Filter
    # ----------------------------------

    st.subheader("📂 Filter")

    c1,c2 = st.columns(2)

    with c1:

        habit_filter = st.selectbox(
            "Habit",
            ["All"] + list(df["Habit"].unique())
            if not df.empty else ["All"]
        )

    with c2:

        status_filter = st.selectbox(
            "Status",
            ["All"] + list(df["Status"].unique())
            if not df.empty else ["All"]
        )

    filtered = df.copy()

    if habit_filter!="All":

        filtered = filtered[
            filtered["Habit"]==habit_filter
        ]

    if status_filter!="All":

        filtered = filtered[
            filtered["Status"]==status_filter
        ]

    st.dataframe(filtered,use_container_width=True)

    st.divider()

    # ----------------------------------
    # Dashboard
    # ----------------------------------

    total = len(df)

    completed = len(
        df[df["Status"]=="Completed"]
    )

    pending = len(
        df[df["Status"]=="Pending"]
    )

    score = 0

    if total>0:

        score = round(
            completed/total*100,
            2
        )

    c1,c2,c3,c4 = st.columns(4)

    c1.metric("Total Habits",total)

    c2.metric("Completed",completed)

    c3.metric("Pending",pending)

    c4.metric("Consistency",str(score)+" %")

    st.divider()

    # ----------------------------------
    # Habit Charts
    # ----------------------------------

    st.subheader("📊 Habit Analytics")

    if not df.empty:

        st.bar_chart(
            df["Habit"].value_counts()
        )

        st.bar_chart(
            df["Status"].value_counts()
        )

    st.divider()

    # ----------------------------------
    # Habit Streak
    # ----------------------------------

    streak = completed

    st.subheader("🔥 Habit Streak")

    st.metric(
        "Current Streak",
        str(streak)+" Days"
    )

    st.progress(score/100)

    st.divider()

    # ----------------------------------
    # AI Suggestions
    # ----------------------------------

    st.subheader("🤖 Habit Coach")

    if score>=90:

        st.success(
            "Excellent consistency! Keep your routine going."
        )

    elif score>=70:

        st.info(
            "Good work! Try to complete all your planned habits."
        )

    elif score>=50:

        st.warning(
            "You are halfway there. Focus on your high-priority habits."
        )

    else:

        st.error(
            "Build one habit at a time. Consistency is more important than intensity."
        )

    st.divider()

    # ----------------------------------
    # Download
    # ----------------------------------

    st.download_button(
        "📥 Download Habit Report",
        df.to_csv(index=False).encode("utf-8"),
        "habit_tracker.csv",
        "text/csv"
    )

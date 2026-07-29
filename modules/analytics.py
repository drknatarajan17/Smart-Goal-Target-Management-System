import streamlit as st
import pandas as pd
import os

def analytics():

    st.title("📊 Smart Analytics Dashboard")

    st.markdown("### Overall Performance Summary")

    # -----------------------------
    # File Locations
    # -----------------------------

    files = {
        "Goals": "data/goals.csv",
        "Tasks": "data/tasks.csv",
        "Habits": "data/habits.csv",
        "Finance": "data/financial_goals.csv",
        "Fitness": "data/fitness_goals.csv",
        "Learning": "data/learning_goals.csv",
        "Career": "data/career_goals.csv",
        "Business": "data/business_goals.csv"
    }

    summary = []

    # -----------------------------
    # Load Data
    # -----------------------------

    for name, file in files.items():

        if os.path.exists(file):

            df = pd.read_csv(file)

            summary.append({
                "Module": name,
                "Records": len(df)
            })

        else:

            summary.append({
                "Module": name,
                "Records": 0
            })

    summary_df = pd.DataFrame(summary)

    # -----------------------------
    # KPI Cards
    # -----------------------------

    total_modules = len(summary_df)

    active_modules = len(
        summary_df[
            summary_df["Records"] > 0
        ]
    )

    total_records = summary_df["Records"].sum()

    avg_records = round(
        total_records / total_modules,
        2
    )

    c1,c2,c3,c4 = st.columns(4)

    c1.metric("Modules", total_modules)

    c2.metric("Active Modules", active_modules)

    c3.metric("Total Records", total_records)

    c4.metric("Average Records", avg_records)

    st.divider()

    # -----------------------------
    # Overall Summary
    # -----------------------------

    st.subheader("📋 Module Summary")

    st.dataframe(
        summary_df,
        use_container_width=True
    )

    st.divider()

    # -----------------------------
    # Charts
    # -----------------------------

    st.subheader("📈 Overall Analytics")

    st.bar_chart(
        summary_df.set_index("Module")["Records"]
    )

    st.divider()

    # -----------------------------
    # Goal Completion
    # -----------------------------

    goal_file = "data/goals.csv"

    if os.path.exists(goal_file):

        goals = pd.read_csv(goal_file)

        if "Status" in goals.columns:

            st.subheader("🎯 Goal Status")

            st.bar_chart(
                goals["Status"].value_counts()
            )

    # -----------------------------
    # Task Analytics
    # -----------------------------

    task_file = "data/tasks.csv"

    if os.path.exists(task_file):

        tasks = pd.read_csv(task_file)

        if "Status" in tasks.columns:

            st.subheader("✅ Task Status")

            st.bar_chart(
                tasks["Status"].value_counts()
            )

    # -----------------------------
    # Habit Analytics
    # -----------------------------

    habit_file = "data/habits.csv"

    if os.path.exists(habit_file):

        habits = pd.read_csv(habit_file)

        if "Habit" in habits.columns:

            st.subheader("🔥 Habit Analytics")

            st.bar_chart(
                habits["Habit"].value_counts()
            )

    # -----------------------------
    # Finance
    # -----------------------------

    finance_file = "data/financial_goals.csv"

    if os.path.exists(finance_file):

        finance = pd.read_csv(finance_file)

        st.subheader("💰 Financial Summary")

        if len(finance)>0:

            total_target = finance["Target Amount"].sum()

            total_saved = finance["Current Amount"].sum()

            c1,c2 = st.columns(2)

            c1.metric(
                "Target Amount",
                f"${total_target:,.2f}"
            )

            c2.metric(
                "Current Savings",
                f"${total_saved:,.2f}"
            )

    # -----------------------------
    # Business
    # -----------------------------

    business_file = "data/business_goals.csv"

    if os.path.exists(business_file):

        business = pd.read_csv(business_file)

        if len(business)>0:

            st.subheader("🏢 Business Summary")

            revenue = business["Current Revenue"].sum()

            profit = business["Profit"].sum()

            c1,c2 = st.columns(2)

            c1.metric(
                "Revenue",
                f"${revenue:,.2f}"
            )

            c2.metric(
                "Profit",
                f"${profit:,.2f}"
            )

    st.divider()

    # -----------------------------
    # Productivity Score
    # -----------------------------

    st.subheader("🚀 Productivity Score")

    productivity = round(
        (active_modules/total_modules)*100,
        2
    )

    st.progress(productivity/100)

    st.metric(
        "Overall Productivity",
        str(productivity)+"%"
    )

    st.divider()

    # -----------------------------
    # AI Summary
    # -----------------------------

    st.subheader("🤖 AI Executive Summary")

    if productivity >= 90:

        st.success(
            "Outstanding! Your personal ecosystem is performing exceptionally well."
        )

    elif productivity >= 70:

        st.info(
            "Good progress. Continue updating your goals and habits regularly."
        )

    elif productivity >= 50:

        st.warning(
            "Several modules are inactive. Updating them regularly will improve your insights."
        )

    else:

        st.error(
            "Very limited data is available. Start tracking your goals consistently to unlock meaningful analytics."
        )

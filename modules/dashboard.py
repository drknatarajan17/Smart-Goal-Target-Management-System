import streamlit as st
import pandas as pd
import os

def dashboard():

    st.title("🎯 Smart Goal & Target Dashboard")
    st.markdown("Track your goals, tasks, habits and productivity from one place.")

    # -------------------------
    # Load Data
    # -------------------------

    def load_data(file):
        if os.path.exists(file):
            return pd.read_csv(file)
        return pd.DataFrame()

    goals = load_data("data/goals.csv")
    tasks = load_data("data/tasks.csv")
    habits = load_data("data/habits.csv")

    # -------------------------
    # Goal Statistics
    # -------------------------

    total_goals = len(goals)

    completed_goals = 0
    in_progress = 0
    pending = 0
    overdue = 0

    if not goals.empty:

        completed_goals = len(goals[goals["Status"]=="Completed"])
        in_progress = len(goals[goals["Status"]=="In Progress"])
        pending = len(goals[goals["Status"]=="Pending"])

        if "Overdue" in goals.columns:
            overdue = len(goals[goals["Overdue"]=="Yes"])

    success_rate = 0

    if total_goals>0:
        success_rate = round((completed_goals/total_goals)*100,2)

    # -------------------------
    # KPI Cards
    # -------------------------

    st.subheader("📊 Goal Overview")

    c1,c2,c3,c4,c5 = st.columns(5)

    c1.metric("Total Goals",total_goals)
    c2.metric("Completed",completed_goals)
    c3.metric("In Progress",in_progress)
    c4.metric("Pending",pending)
    c5.metric("Success %",str(success_rate)+" %")

    st.divider()

    # -------------------------
    # Task Summary
    # -------------------------

    total_tasks = len(tasks)

    completed_tasks = 0

    if not tasks.empty:

        completed_tasks = len(tasks[tasks["Status"]=="Completed"])

    pending_tasks = total_tasks-completed_tasks

    c1,c2,c3 = st.columns(3)

    c1.metric("Total Tasks",total_tasks)
    c2.metric("Completed Tasks",completed_tasks)
    c3.metric("Pending Tasks",pending_tasks)

    st.divider()

    # -------------------------
    # Habit Summary
    # -------------------------

    st.subheader("🔥 Habit Tracker Summary")

    if habits.empty:

        st.info("No habits added yet.")

    else:

        st.dataframe(habits,use_container_width=True)

    st.divider()

    # -------------------------
    # Today's Priorities
    # -------------------------

    st.subheader("📌 Today's Priorities")

    if goals.empty:

        st.warning("No goals available.")

    else:

        priority = goals.sort_values("Priority")

        st.dataframe(priority.head(10),use_container_width=True)

    st.divider()

    # -------------------------
    # Goal Categories
    # -------------------------

    st.subheader("📂 Goal Categories")

    if not goals.empty:

        if "Category" in goals.columns:

            chart = goals["Category"].value_counts()

            st.bar_chart(chart)

    else:

        st.info("No Goal Categories Available.")

    st.divider()

    # -------------------------
    # Progress Distribution
    # -------------------------

    st.subheader("📈 Goal Progress")

    if not goals.empty:

        if "Progress" in goals.columns:

            progress = goals[["Goal Name","Progress"]]

            progress = progress.set_index("Goal Name")

            st.bar_chart(progress)

    st.divider()

    # -------------------------
    # Upcoming Deadlines
    # -------------------------

    st.subheader("⏳ Upcoming Deadlines")

    if not goals.empty:

        if "Target Date" in goals.columns:

            deadline = goals.sort_values("Target Date")

            st.dataframe(
                deadline[
                    [
                        "Goal Name",
                        "Target Date",
                        "Status"
                    ]
                ],
                use_container_width=True
            )

    else:

        st.info("No deadlines available.")

    st.divider()

    # -------------------------
    # Productivity Score
    # -------------------------

    productivity = 50

    productivity += completed_goals*5

    productivity -= pending*2

    productivity -= overdue*3

    if productivity>100:
        productivity=100

    if productivity<0:
        productivity=0

    st.subheader("🚀 Productivity Score")

    st.progress(productivity/100)

    st.metric("Overall Score",str(productivity)+"/100")

    st.divider()

    # -------------------------
    # Smart Insights
    # -------------------------

    st.subheader("🤖 AI Insights")

    if total_goals==0:

        st.info("Create your first goal to begin your journey.")

    else:

        if success_rate>=80:

            st.success("Excellent! You are consistently achieving your goals.")

        elif success_rate>=60:

            st.warning("Good progress. Focus on completing pending goals.")

        else:

            st.error("Your completion rate is low. Prioritize fewer goals and finish them first.")

        if pending_tasks>10:

            st.warning("You have many pending tasks. Try completing small tasks first.")

        if overdue>0:

            st.error(f"{overdue} goals are overdue.")

        if productivity>90:

            st.success("Outstanding productivity!")

        elif productivity<50:

            st.warning("Your productivity needs improvement.")

    st.divider()

    st.caption("© Smart Goal & Target Management System")

import streamlit as st
import pandas as pd
import os
from datetime import datetime

def ai_goal_coach():

    st.title("🤖 AI Goal Coach")
    st.markdown("### Your Personal AI Productivity & Success Advisor")

    files = {
        "Goals":"data/goals.csv",
        "Tasks":"data/tasks.csv",
        "Habits":"data/habits.csv",
        "Financial":"data/financial_goals.csv",
        "Fitness":"data/fitness_goals.csv",
        "Learning":"data/learning_goals.csv",
        "Career":"data/career_goals.csv",
        "Business":"data/business_goals.csv"
    }

    loaded = {}

    # -----------------------------------
    # Load Available Data
    # -----------------------------------

    for name,file in files.items():

        if os.path.exists(file):

            loaded[name] = pd.read_csv(file)

    st.success(f"{len(loaded)} Modules Loaded Successfully")

    st.divider()

    # -----------------------------------
    # Life Score
    # -----------------------------------

    total_modules = len(files)

    active_modules = len(loaded)

    life_score = round(
        active_modules/total_modules*100,
        2
    )

    st.subheader("🏆 Life Score")

    st.progress(life_score/100)

    st.metric(
        "Overall Life Score",
        str(life_score)+" %"
    )

    st.divider()

    # -----------------------------------
    # Goal Suggestions
    # -----------------------------------

    st.subheader("🎯 Goal Advisor")

    if "Goals" in loaded:

        goals = loaded["Goals"]

        if "Status" in goals.columns:

            pending = len(
                goals[
                    goals["Status"]!="Completed"
                ]
            )

            completed = len(
                goals[
                    goals["Status"]=="Completed"
                ]
            )

            st.metric("Completed Goals",completed)
            st.metric("Pending Goals",pending)

            if pending>completed:

                st.warning(
                    "You have more pending goals than completed ones. Focus on finishing existing goals before creating new ones."
                )
            else:

                st.success(
                    "Excellent! You are completing goals consistently."
                )

    st.divider()

    # -----------------------------------
    # Task Advisor
    # -----------------------------------

    st.subheader("✅ Task Advisor")

    if "Tasks" in loaded:

        tasks = loaded["Tasks"]

        if "Status" in tasks.columns:

            pending = len(
                tasks[
                    tasks["Status"]!="Completed"
                ]
            )

            st.metric(
                "Pending Tasks",
                pending
            )

            if pending>10:

                st.error(
                    "Too many pending tasks. Prioritize High Priority tasks first."
                )

            elif pending>5:

                st.warning(
                    "Consider finishing pending tasks this week."
                )

            else:

                st.success(
                    "Task backlog is under control."
                )

    st.divider()

    # -----------------------------------
    # Habit Advisor
    # -----------------------------------

    st.subheader("🔥 Habit Coach")

    if "Habits" in loaded:

        habits = loaded["Habits"]

        if "Status" in habits.columns:

            completed = len(
                habits[
                    habits["Status"]=="Completed"
                ]
            )

            total = len(habits)

            if total>0:

                habit_score = round(
                    completed/total*100,
                    2
                )

                st.metric(
                    "Habit Consistency",
                    str(habit_score)+"%"
                )

                if habit_score<60:

                    st.warning(
                        "Consistency is more important than intensity. Build habits every day."
                    )

                else:

                    st.success(
                        "Excellent daily discipline!"
                    )

    st.divider()

    # -----------------------------------
    # Financial Coach
    # -----------------------------------

    st.subheader("💰 Financial Advisor")

    if "Financial" in loaded:

        finance = loaded["Financial"]

        target = finance["Target Amount"].sum()
        saved = finance["Current Amount"].sum()

        if target>0:

            progress = round(
                saved/target*100,
                2
            )

            st.metric(
                "Savings Progress",
                str(progress)+"%"
            )

            if progress<50:

                st.warning(
                    "Increase monthly savings and reduce unnecessary expenses."
                )

            else:

                st.success(
                    "Your financial goals are progressing well."
                )

    st.divider()

    # -----------------------------------
    # Learning Coach
    # -----------------------------------

    st.subheader("📚 Learning Coach")

    if "Learning" in loaded:

        learning = loaded["Learning"]

        if len(learning)>0:

            hours = learning["Study Hours"].sum()

            st.metric(
                "Study Hours",
                round(hours,2)
            )

            if hours<50:

                st.warning(
                    "Increase weekly learning hours."
                )

            else:

                st.success(
                    "Excellent commitment to continuous learning."
                )

    st.divider()

    # -----------------------------------
    # Fitness Coach
    # -----------------------------------

    st.subheader("🏋 Fitness Coach")

    if "Fitness" in loaded:

        fitness = loaded["Fitness"]

        latest = fitness.iloc[-1]

        bmi = latest["BMI"]

        st.metric(
            "Current BMI",
            bmi
        )

        if bmi>25:

            st.warning(
                "Maintain regular exercise and balanced nutrition."
            )

        elif bmi<18.5:

            st.warning(
                "Focus on healthy weight gain and strength training."
            )

        else:

            st.success(
                "Healthy BMI. Keep maintaining your fitness."
            )

    st.divider()

    # -----------------------------------
    # Career Coach
    # -----------------------------------

    st.subheader("🚀 Career Coach")

    if "Career" in loaded:

        career = loaded["Career"]

        avg = career["Progress"].mean()

        st.metric(
            "Career Progress",
            str(round(avg,2))+"%"
        )

        if avg<50:

            st.warning(
                "Complete certifications, research papers, and networking activities."
            )

        else:

            st.success(
                "Your career development is moving in the right direction."
            )

    st.divider()

    # -----------------------------------
    # Business Coach
    # -----------------------------------

    st.subheader("🏢 Business Advisor")

    if "Business" in loaded:

        business = loaded["Business"]

        revenue = business["Current Revenue"].sum()
        profit = business["Profit"].sum()

        st.metric("Revenue",f"${revenue:,.0f}")
        st.metric("Profit",f"${profit:,.0f}")

        if profit<0:

            st.error(
                "Business is operating at a loss. Review expenses and pricing."
            )

        else:

            st.success(
                "Business is generating positive profit."
            )

    st.divider()

    # -----------------------------------
    # Weekly Mission
    # -----------------------------------

    st.subheader("🎯 AI Weekly Mission")

    missions = [
        "Complete at least 5 pending tasks.",
        "Exercise for 30 minutes every day.",
        "Read 100 pages this week.",
        "Save at least 10% of your monthly income.",
        "Learn one new professional skill.",
        "Review your business progress every Sunday.",
        "Sleep at least 7 hours every night.",
        "Spend quality time with your family."
    ]

    for mission in missions:
        st.checkbox(mission)

    st.divider()

    # -----------------------------------
    # Final Summary
    # -----------------------------------

    st.subheader("🏆 AI Success Prediction")

    if life_score>=90:

        st.success(
            "Excellent! You are maintaining a highly balanced life with strong progress across personal, professional, financial, and health goals."
        )

    elif life_score>=70:

        st.info(
            "You are progressing well. Stay consistent and review your goals every week."
        )

    elif life_score>=50:

        st.warning(
            "Several areas need attention. Focus on habits, task completion, and financial planning."
        )

    else:

        st.error(
            "Your tracking data is limited. Start updating each module regularly to receive meaningful AI insights."
        )

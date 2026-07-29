import streamlit as st
import pandas as pd
import os
from datetime import datetime

def reports():

    st.title("📄 Reports & Performance Summary")

    st.markdown("Generate consolidated reports for all your goals and activities.")

    files = {
        "Goals": "data/goals.csv",
        "Tasks": "data/tasks.csv",
        "Habits": "data/habits.csv",
        "Financial Goals": "data/financial_goals.csv",
        "Fitness": "data/fitness_goals.csv",
        "Learning": "data/learning_goals.csv",
        "Career": "data/career_goals.csv",
        "Business": "data/business_goals.csv"
    }

    report = []

    st.subheader("📋 Module Summary")

    for module, file in files.items():

        if os.path.exists(file):

            df = pd.read_csv(file)

            records = len(df)

            updated = datetime.fromtimestamp(
                os.path.getmtime(file)
            ).strftime("%d-%m-%Y %H:%M")

        else:

            records = 0
            updated = "Not Available"

        report.append({
            "Module": module,
            "Records": records,
            "Last Updated": updated
        })

    summary = pd.DataFrame(report)

    st.dataframe(
        summary,
        use_container_width=True
    )

    st.divider()

    # -------------------------------------
    # Overall KPI
    # -------------------------------------

    st.subheader("📊 Overall KPI")

    total_modules = len(summary)

    active_modules = len(
        summary[
            summary["Records"] > 0
        ]
    )

    total_records = summary["Records"].sum()

    completion = round(
        active_modules / total_modules * 100,
        2
    )

    c1, c2, c3, c4 = st.columns(4)

    c1.metric("Modules", total_modules)
    c2.metric("Active", active_modules)
    c3.metric("Records", total_records)
    c4.metric("Completion", f"{completion}%")

    st.progress(completion/100)

    st.divider()

    # -------------------------------------
    # Individual Reports
    # -------------------------------------

    st.subheader("📑 Individual Module Reports")

    module = st.selectbox(
        "Choose Module",
        list(files.keys())
    )

    filename = files[module]

    if os.path.exists(filename):

        data = pd.read_csv(filename)

        st.dataframe(
            data,
            use_container_width=True
        )

        st.download_button(
            f"📥 Download {module} Report",
            data.to_csv(index=False).encode("utf-8"),
            f"{module.lower().replace(' ','_')}.csv",
            "text/csv"
        )

    else:

        st.warning("No data available.")

    st.divider()

    # -------------------------------------
    # Executive Summary
    # -------------------------------------

    st.subheader("📈 Executive Summary")

    st.write(f"**Total Modules :** {total_modules}")

    st.write(f"**Modules with Data :** {active_modules}")

    st.write(f"**Total Records :** {total_records}")

    st.write(f"**Completion :** {completion}%")

    st.divider()

    # -------------------------------------
    # Charts
    # -------------------------------------

    st.subheader("📊 Reports Dashboard")

    st.bar_chart(
        summary.set_index(
            "Module"
        )["Records"]
    )

    st.divider()

    # -------------------------------------
    # AI Report
    # -------------------------------------

    st.subheader("🤖 AI Performance Review")

    if completion >= 90:

        st.success(
            "Excellent! Almost every area of your life is being tracked effectively."
        )

    elif completion >= 70:

        st.info(
            "Good progress. Continue updating your data regularly."
        )

    elif completion >= 50:

        st.warning(
            "Several modules need more frequent updates."
        )

    else:

        st.error(
            "Very limited information is available. Start tracking your goals consistently."
        )

    st.divider()

    # -------------------------------------
    # Download Master Report
    # -------------------------------------

    st.download_button(
        "📥 Download Executive Summary",
        summary.to_csv(index=False).encode("utf-8"),
        "executive_summary.csv",
        "text/csv"
    )

import streamlit as st
import pandas as pd
import os
from datetime import date

def fitness_goals():

    st.title("🏋️ Fitness Goal Tracker")

    file = "data/fitness_goals.csv"

    # -----------------------------------
    # Load Data
    # -----------------------------------

    if os.path.exists(file):
        df = pd.read_csv(file)
    else:
        df = pd.DataFrame(columns=[
            "Fitness ID",
            "Date",
            "Weight (kg)",
            "Height (cm)",
            "BMI",
            "Walking (km)",
            "Running (km)",
            "Workout (min)",
            "Calories Burned",
            "Water (L)",
            "Sleep (hrs)",
            "Heart Rate",
            "Remarks"
        ])

    # -----------------------------------
    # Add Fitness Record
    # -----------------------------------

    st.subheader("➕ Daily Fitness Entry")

    with st.form("fitness_form"):

        record_date = st.date_input("Date", date.today())

        weight = st.number_input(
            "Weight (kg)",
            min_value=20.0,
            max_value=250.0,
            value=70.0
        )

        height = st.number_input(
            "Height (cm)",
            min_value=100.0,
            max_value=250.0,
            value=170.0
        )

        walking = st.number_input(
            "Walking Distance (km)",
            min_value=0.0,
            value=0.0
        )

        running = st.number_input(
            "Running Distance (km)",
            min_value=0.0,
            value=0.0
        )

        workout = st.number_input(
            "Workout Duration (Minutes)",
            min_value=0,
            value=0
        )

        calories = st.number_input(
            "Calories Burned",
            min_value=0,
            value=0
        )

        water = st.number_input(
            "Water Intake (Litres)",
            min_value=0.0,
            value=2.0
        )

        sleep = st.number_input(
            "Sleep (Hours)",
            min_value=0.0,
            max_value=24.0,
            value=7.0
        )

        heart_rate = st.number_input(
            "Heart Rate (BPM)",
            min_value=40,
            max_value=220,
            value=72
        )

        remarks = st.text_area("Remarks")

        submit = st.form_submit_button("Save Fitness Record")

    if submit:

        bmi = round(weight / ((height / 100) ** 2), 2)

        fitness_id = "FIT-" + str(len(df)+1).zfill(4)

        new = pd.DataFrame([{
            "Fitness ID": fitness_id,
            "Date": record_date,
            "Weight (kg)": weight,
            "Height (cm)": height,
            "BMI": bmi,
            "Walking (km)": walking,
            "Running (km)": running,
            "Workout (min)": workout,
            "Calories Burned": calories,
            "Water (L)": water,
            "Sleep (hrs)": sleep,
            "Heart Rate": heart_rate,
            "Remarks": remarks
        }])

        df = pd.concat([df, new], ignore_index=True)

        os.makedirs("data", exist_ok=True)
        df.to_csv(file, index=False)

        st.success("Fitness Record Saved Successfully!")

    st.divider()

    # -----------------------------------
    # Records
    # -----------------------------------

    st.subheader("📋 Fitness Records")

    st.dataframe(df, use_container_width=True)

    st.divider()

    # -----------------------------------
    # Search
    # -----------------------------------

    keyword = st.text_input("Search by Remark")

    if keyword:

        result = df[
            df["Remarks"].astype(str).str.contains(
                keyword,
                case=False,
                na=False
            )
        ]

        st.dataframe(result, use_container_width=True)

    st.divider()

    # -----------------------------------
    # Dashboard
    # -----------------------------------

    if not df.empty:

        latest = df.iloc[-1]

        c1, c2, c3, c4 = st.columns(4)

        c1.metric(
            "Weight",
            str(latest["Weight (kg)"]) + " kg"
        )

        c2.metric(
            "BMI",
            latest["BMI"]
        )

        c3.metric(
            "Water",
            str(latest["Water (L)"]) + " L"
        )

        c4.metric(
            "Sleep",
            str(latest["Sleep (hrs)"]) + " hrs"
        )

    st.divider()

    # -----------------------------------
    # BMI Status
    # -----------------------------------

    st.subheader("⚖️ BMI Assessment")

    if not df.empty:

        bmi = latest["BMI"]

        if bmi < 18.5:

            st.warning("Underweight")

        elif bmi < 25:

            st.success("Normal Weight")

        elif bmi < 30:

            st.warning("Overweight")

        else:

            st.error("Obese")

    st.divider()

    # -----------------------------------
    # Charts
    # -----------------------------------

    st.subheader("📊 Fitness Analytics")

    if not df.empty:

        st.line_chart(
            df.set_index("Date")["Weight (kg)"]
        )

        st.line_chart(
            df.set_index("Date")["BMI"]
        )

        st.bar_chart(
            df.set_index("Date")["Calories Burned"]
        )

        st.bar_chart(
            df.set_index("Date")["Workout (min)"]
        )

        st.line_chart(
            df.set_index("Date")["Water (L)"]
        )

        st.line_chart(
            df.set_index("Date")["Sleep (hrs)"]
        )

    st.divider()

    # -----------------------------------
    # AI Fitness Coach
    # -----------------------------------

    st.subheader("🤖 AI Fitness Coach")

    if not df.empty:

        if latest["Workout (min)"] < 30:

            st.warning("Increase workout duration to at least 30 minutes per day.")

        else:

            st.success("Excellent workout consistency!")

        if latest["Water (L)"] < 2:

            st.warning("Increase your daily water intake.")

        if latest["Sleep (hrs)"] < 7:

            st.warning("Aim for at least 7–8 hours of sleep.")

        if latest["BMI"] > 25:

            st.info("Maintain a calorie deficit and stay physically active.")

    st.divider()

    # -----------------------------------
    # Download
    # -----------------------------------

    st.download_button(
        "📥 Download Fitness Report",
        df.to_csv(index=False).encode("utf-8"),
        "fitness_goals.csv",
        "text/csv"
    )

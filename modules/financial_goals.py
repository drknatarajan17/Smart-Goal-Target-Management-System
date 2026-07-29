import streamlit as st
import pandas as pd
import os
from datetime import date

def financial_goals():

    st.title("💰 Financial Goals")

    file = "data/financial_goals.csv"

    # ----------------------------------
    # Load Data
    # ----------------------------------

    if os.path.exists(file):
        df = pd.read_csv(file)
    else:
        df = pd.DataFrame(columns=[
            "Goal ID",
            "Goal Name",
            "Category",
            "Target Amount",
            "Current Amount",
            "Remaining Amount",
            "Target Date",
            "Status",
            "Remarks"
        ])

    # ----------------------------------
    # Add Financial Goal
    # ----------------------------------

    st.subheader("➕ Add Financial Goal")

    with st.form("finance_form"):

        goal_name = st.text_input("Goal Name")

        category = st.selectbox(
            "Category",
            [
                "Savings",
                "Emergency Fund",
                "House",
                "Land",
                "Car",
                "Bike",
                "Education",
                "Investment",
                "Loan Repayment",
                "Business",
                "Retirement",
                "Travel",
                "Other"
            ]
        )

        target_amount = st.number_input(
            "Target Amount",
            min_value=0.0,
            value=10000.0
        )

        current_amount = st.number_input(
            "Current Savings",
            min_value=0.0,
            value=0.0
        )

        target_date = st.date_input(
            "Target Date",
            date.today()
        )

        remarks = st.text_area("Remarks")

        submit = st.form_submit_button("Save Goal")

    if submit:

        remaining = target_amount - current_amount

        if remaining <= 0:
            status = "Completed"
            remaining = 0
        else:
            status = "In Progress"

        goal_id = "FIN-" + str(len(df)+1).zfill(4)

        new = pd.DataFrame([{
            "Goal ID":goal_id,
            "Goal Name":goal_name,
            "Category":category,
            "Target Amount":target_amount,
            "Current Amount":current_amount,
            "Remaining Amount":remaining,
            "Target Date":target_date,
            "Status":status,
            "Remarks":remarks
        }])

        df = pd.concat([df,new],ignore_index=True)

        os.makedirs("data",exist_ok=True)

        df.to_csv(file,index=False)

        st.success("Financial Goal Added Successfully")

    st.divider()

    # ----------------------------------
    # Display Goals
    # ----------------------------------

    st.subheader("📋 Financial Goal List")

    st.dataframe(df,use_container_width=True)

    st.divider()

    # ----------------------------------
    # Search
    # ----------------------------------

    st.subheader("🔍 Search Goal")

    keyword = st.text_input("Search Goal")

    if keyword:

        search = df[
            df["Goal Name"].str.contains(
                keyword,
                case=False,
                na=False
            )
        ]

        st.dataframe(search,use_container_width=True)

    st.divider()

    # ----------------------------------
    # Dashboard
    # ----------------------------------

    total_goals = len(df)

    completed = len(
        df[df["Status"]=="Completed"]
    )

    inprogress = len(
        df[df["Status"]=="In Progress"]
    )

    target = 0
    current = 0
    remaining = 0

    if not df.empty:

        target = df["Target Amount"].sum()
        current = df["Current Amount"].sum()
        remaining = df["Remaining Amount"].sum()

    c1,c2,c3 = st.columns(3)

    c1.metric("Financial Goals",total_goals)
    c2.metric("Completed",completed)
    c3.metric("In Progress",inprogress)

    st.divider()

    c1,c2,c3 = st.columns(3)

    c1.metric("Target Amount",f"₹ {target:,.2f}")
    c2.metric("Saved",f"₹ {current:,.2f}")
    c3.metric("Remaining",f"₹ {remaining:,.2f}")

    st.divider()

    # ----------------------------------
    # Progress
    # ----------------------------------

    st.subheader("📈 Overall Savings Progress")

    if target > 0:

        progress = (current/target)*100

    else:

        progress = 0

    st.progress(progress/100)

    st.metric(
        "Savings Progress",
        str(round(progress,2))+" %"
    )

    st.divider()

    # ----------------------------------
    # Charts
    # ----------------------------------

    st.subheader("📊 Financial Analytics")

    if not df.empty:

        st.bar_chart(
            df.set_index("Goal Name")["Current Amount"]
        )

        st.bar_chart(
            df["Category"].value_counts()
        )

    st.divider()

    # ----------------------------------
    # AI Suggestions
    # ----------------------------------

    st.subheader("🤖 Financial Advisor")

    if progress >= 90:

        st.success("Excellent! You are very close to achieving your financial goals.")

    elif progress >= 70:

        st.info("Great progress. Continue your monthly savings.")

    elif progress >= 50:

        st.warning("You're halfway there. Consider increasing your monthly savings.")

    else:

        st.error("Your savings rate is low. Review your expenses and increase investments.")

    st.divider()

    # ----------------------------------
    # Download
    # ----------------------------------

    st.download_button(
        "📥 Download Financial Report",
        df.to_csv(index=False).encode("utf-8"),
        "financial_goals.csv",
        "text/csv"
    )

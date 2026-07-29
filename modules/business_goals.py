import streamlit as st
import pandas as pd
import os
from datetime import date

def business_goals():

    st.title("🏢 Business Goals & Startup Management")

    file = "data/business_goals.csv"

    # ---------------------------------------
    # Load Data
    # ---------------------------------------

    if os.path.exists(file):
        df = pd.read_csv(file)
    else:
        df = pd.DataFrame(columns=[
            "Business ID",
            "Business Name",
            "Business Type",
            "Category",
            "Target Revenue",
            "Current Revenue",
            "Monthly Target",
            "Investment",
            "Expenses",
            "Profit",
            "Owner",
            "Status",
            "Target Date",
            "Remarks"
        ])

    # ---------------------------------------
    # Add Business
    # ---------------------------------------

    st.subheader("➕ Add Business Goal")

    with st.form("business_form"):

        business_name = st.text_input("Business Name")

        business_type = st.selectbox(
            "Business Type",
            [
                "Startup",
                "Small Business",
                "Freelancing",
                "Consultancy",
                "Manufacturing",
                "Retail",
                "Software",
                "Agriculture",
                "Real Estate",
                "Education",
                "Other"
            ]
        )

        category = st.selectbox(
            "Category",
            [
                "Technology",
                "Education",
                "Agriculture",
                "Transport",
                "Healthcare",
                "Finance",
                "Retail",
                "Manufacturing",
                "Real Estate",
                "Other"
            ]
        )

        target_revenue = st.number_input(
            "Target Revenue",
            min_value=0.0,
            value=100000.0
        )

        current_revenue = st.number_input(
            "Current Revenue",
            min_value=0.0,
            value=0.0
        )

        monthly_target = st.number_input(
            "Monthly Revenue Target",
            min_value=0.0,
            value=10000.0
        )

        investment = st.number_input(
            "Investment",
            min_value=0.0,
            value=0.0
        )

        expenses = st.number_input(
            "Expenses",
            min_value=0.0,
            value=0.0
        )

        owner = st.text_input("Owner")

        status = st.selectbox(
            "Business Status",
            [
                "Idea",
                "Planning",
                "Running",
                "Paused",
                "Closed"
            ]
        )

        target_date = st.date_input(
            "Target Date",
            date.today()
        )

        remarks = st.text_area("Remarks")

        submit = st.form_submit_button("Save Business")

    if submit:

        business_id = "BUS-" + str(len(df)+1).zfill(4)

        profit = current_revenue - expenses

        new = pd.DataFrame([{
            "Business ID":business_id,
            "Business Name":business_name,
            "Business Type":business_type,
            "Category":category,
            "Target Revenue":target_revenue,
            "Current Revenue":current_revenue,
            "Monthly Target":monthly_target,
            "Investment":investment,
            "Expenses":expenses,
            "Profit":profit,
            "Owner":owner,
            "Status":status,
            "Target Date":target_date,
            "Remarks":remarks
        }])

        df = pd.concat([df,new],ignore_index=True)

        os.makedirs("data",exist_ok=True)

        df.to_csv(file,index=False)

        st.success("Business Saved Successfully!")

    st.divider()

    # ---------------------------------------
    # Dashboard
    # ---------------------------------------

    st.subheader("📊 Business Dashboard")

    total = len(df)

    running = len(
        df[df["Status"]=="Running"]
    )

    target = df["Target Revenue"].sum() if not df.empty else 0

    revenue = df["Current Revenue"].sum() if not df.empty else 0

    profit = df["Profit"].sum() if not df.empty else 0

    c1,c2,c3,c4,c5 = st.columns(5)

    c1.metric("Businesses",total)

    c2.metric("Running",running)

    c3.metric("Revenue",f"₹ {revenue:,.0f}")

    c4.metric("Profit",f"₹ {profit:,.0f}")

    progress = 0

    if target>0:

        progress = round(
            revenue/target*100,
            2
        )

    c5.metric("Target",str(progress)+" %")

    st.progress(progress/100 if progress<=100 else 1.0)

    st.divider()

    # ---------------------------------------
    # Business Records
    # ---------------------------------------

    st.subheader("📋 Business Portfolio")

    st.dataframe(df,use_container_width=True)

    st.divider()

    # ---------------------------------------
    # Search
    # ---------------------------------------

    keyword = st.text_input(
        "🔍 Search Business"
    )

    if keyword:

        result = df[
            df["Business Name"].str.contains(
                keyword,
                case=False,
                na=False
            )
        ]

        st.dataframe(result,use_container_width=True)

    st.divider()

    # ---------------------------------------
    # Charts
    # ---------------------------------------

    st.subheader("📈 Business Analytics")

    if not df.empty:

        st.bar_chart(
            df["Business Type"].value_counts()
        )

        st.bar_chart(
            df["Status"].value_counts()
        )

        st.bar_chart(
            df.set_index(
                "Business Name"
            )["Current Revenue"]
        )

        st.bar_chart(
            df.set_index(
                "Business Name"
            )["Profit"]
        )

    st.divider()

    # ---------------------------------------
    # AI Business Advisor
    # ---------------------------------------

    st.subheader("🤖 AI Business Advisor")

    if progress>=90:

        st.success(
            "Excellent! Your businesses are on track to achieve their revenue goals."
        )

    elif progress>=70:

        st.info(
            "Good progress. Focus on increasing profit margins and customer acquisition."
        )

    elif progress>=50:

        st.warning(
            "Revenue is improving. Review your monthly targets and optimize expenses."
        )

    else:

        st.error(
            "Business growth is below target. Consider revising your strategy, marketing, or pricing."
        )

    if profit < 0:

        st.error("⚠️ Overall business portfolio is running at a loss.")

    else:

        st.success("✅ Overall business portfolio is profitable.")

    st.divider()

    # ---------------------------------------
    # Export
    # ---------------------------------------

    st.download_button(
        "📥 Download Business Report",
        df.to_csv(index=False).encode("utf-8"),
        "business_goals.csv",
        "text/csv"
    )

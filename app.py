import streamlit as st

# Import Modules
from modules.dashboard import dashboard
from modules.goal_management import goal_management
from modules.task_management import task_management
from modules.daily_planner import daily_planner
from modules.weekly_planner import weekly_planner
from modules.habit_tracker import habit_tracker
from modules.financial_goals import financial_goals
from modules.fitness_goals import fitness_goals
from modules.learning_goals import learning_goals
from modules.career_goals import career_goals
from modules.business_goals import business_goals
from modules.analytics import analytics
from modules.reports import reports
from modules.ai_goal_coach import ai_goal_coach

# Page Configuration
st.set_page_config(
    page_title="Smart Goal & Target Management System",
    page_icon="🎯",
    layout="wide"
)

# Sidebar
st.sidebar.title("🎯 Goal & Target Tracker")

menu = [
    "🏠 Dashboard",
    "🎯 Goal Management",
    "✅ Task Management",
    "📅 Daily Planner",
    "📆 Weekly Planner",
    "🔥 Habit Tracker",
    "💰 Financial Goals",
    "🏋️ Fitness Goals",
    "📚 Learning Goals",
    "💼 Career Goals",
    "🚀 Business Goals",
    "📊 Analytics",
    "📑 Reports",
    "🤖 AI Goal Coach"
]

choice = st.sidebar.radio("Navigation", menu)

# Navigation
if choice == "🏠 Dashboard":
    dashboard()

elif choice == "🎯 Goal Management":
    goal_management()

elif choice == "✅ Task Management":
    task_management()

elif choice == "📅 Daily Planner":
    daily_planner()

elif choice == "📆 Weekly Planner":
    weekly_planner()

elif choice == "🔥 Habit Tracker":
    habit_tracker()

elif choice == "💰 Financial Goals":
    financial_goals()

elif choice == "🏋️ Fitness Goals":
    fitness_goals()

elif choice == "📚 Learning Goals":
    learning_goals()

elif choice == "💼 Career Goals":
    career_goals()

elif choice == "🚀 Business Goals":
    business_goals()

elif choice == "📊 Analytics":
    analytics()

elif choice == "📑 Reports":
    reports()

elif choice == "🤖 AI Goal Coach":
    ai_goal_coach()

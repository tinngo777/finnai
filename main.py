import streamlit as st
from account import run_account
from profile_management import questionnaire
from main_page import run_main_page
from expense_tracking import expense_tracking
from budget_tracker import budget_tracker

# Initialize session state
if "current_page" not in st.session_state:
    st.session_state["current_page"] = "login"
if "user_id" not in st.session_state:
    st.session_state["user_id"] = ""
if "username" not in st.session_state:
    st.session_state["username"] = ""

# Navigation
if st.session_state["current_page"] == "login":
    run_account()
elif st.session_state["current_page"] == "questionnaire":
    questionnaire(st.session_state["user_id"])
elif st.session_state["current_page"] == "main_page":
    run_main_page(st.session_state["user_id"])
elif st.session_state["current_page"] == "expense_tracking":
    expense_tracking(st.session_state["user_id"])
elif st.session_state["current_page"] == "budget_tracker":
    budget_tracker(st.session_state["user_id"])

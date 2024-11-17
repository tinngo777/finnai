import streamlit as st
from budget_tracker import budget_tracker
from expense_tracking import expense_tracking
from profile_management import profile_page
from saving_visualization import saving_progress_main

from firebase_setup import db

def main_menu(user_id):
    first_name = st.session_state.get("first_name", "User")
    # Custom CSS for styling
    st.markdown(
        """
        <style>
        .main-header {
            background-color: #4FBF26; 
            color: #FFF6B5; 
            padding: 40px 20px;
            text-align: center;
            border-radius: 50px;
        }
        .profile-picture {
            display: flex;
            justify-content: center;
            margin-top: -40px;
        }
        .profile-circle {
            width: 150px;
            height: 150px;
            background-color: #DFF3E3; 
            border-radius: 50%;
            display: flex;
            justify-content: center;
            align-items: center;
            font-size: 18px;
            color: #006400;
            margin-bottom: 20px;
        }
        .button-container {
            display: flex;
            justify-content: center;
            flex-wrap: wrap;
            gap: 15px;
            margin-top: 20px;
        }
        .button {
            background-color: #4FBF26; 
            color: #FFFFFF;
            border: 1px solid #D4D4D4;
            border-radius: 50px;
            padding: 10px 20px;
            font-size: 16px;
            text-align: center;
            cursor: pointer;
        }
        .button:hover {
            background-color: #FFE58A; 
        }
        .center-text {
            text-align: center;
            margin: 20px 0;
            color: #006400;
        }
        .settings-sidebar {
            background-color: #F4F4F4;
            padding: 20px;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    # Sidebar
    with st.sidebar:
        st.markdown('<div class="settings-sidebar"><h3>Settings</h3></div>', unsafe_allow_html=True)
        st.checkbox("Enable Notifications", value=True, key="notifications_checkbox")
        theme = st.selectbox("Theme", options=["Green and Yellow", "Light"], key="theme_selectbox")
        if st.button("Log Out", key="logout_sidebar_button"):
            st.session_state.update({"current_page": "login", "user_id": "", "first_name": ""})

    # Main Header with Profile Section
    st.markdown(f'<div class="main-header"><h1>Welcome, {first_name}!</h1></div>', unsafe_allow_html=True)
    st.markdown('<div class="profile-picture"><div class="profile-circle">No Photo</div></div>', unsafe_allow_html=True)

    # Centered Text for Question
    st.markdown('<div class="center-text"><h2>What would you like FinnAi to do?</h2></div>', unsafe_allow_html=True)

    # Navigation Buttons with Unique Keys
    if st.button("View and Edit Your Profile", key="view_edit_profile_button"):
        st.session_state["current_page"] = "profile_page"
    if st.button("Create a Budget", key="create_budget_button"):
        st.session_state["current_page"] = "budget_tracker"
    if st.button("Track Your Expenses", key="track_expenses_button"):
        st.session_state["current_page"] = "expense_tracking"
    if st.button("Show Your Saving Progress", key="saving_progress_button"):
        st.session_state["current_page"] = "savings_progress"
    

# Main Execution
def run_main_page(user_id):
    if "user_id" not in st.session_state or not st.session_state["user_id"]:
        st.error("User not logged in! Please log in first.")
        st.stop()

    # Fetch user details from Firestore
    user_doc = db.collection("users").document(user_id).get()
    user_data = user_doc.to_dict() if user_doc.exists else {"first_name": "User"}

    # Update session state with user data
    st.session_state["first_name"] = user_data.get("first_name", "User")

    # Current page
    current_page = st.session_state.get("current_page", "main_menu")

    if current_page == "budget_tracker":
        budget_tracker(user_id)
    elif current_page == "expense_tracking":
        expense_tracking(user_id)
    elif current_page == "profile_page":
        profile_page(user_id)
    elif current_page == "savings_progress":
        saving_progress_main(user_id)  # Placeholder for savings progress page
    else:
        # Default to main menu
        main_menu(user_id)
import streamlit as st
from budget_tracker import budget_tracker
from expense_tracking import expense_tracking
from profile_management import profile_page

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
        st.checkbox("Enable Notifications", value=True)
        theme = st.selectbox("Theme", options=["Green and Yellow", "Light"])
        if st.button("Log Out"):
            st.session_state.current_page = "login"

    # Main Header with Profile Section
    st.markdown(f'<div class="main-header"><h1>Welcome, {st.session_state.get("first_name", "User")}!</h1></div>', unsafe_allow_html=True)
    st.markdown('<div class="profile-picture"><div class="profile-circle">No Photo</div></div>', unsafe_allow_html=True)

    # Centered Text for Question
    st.markdown('<div class="center-text"><h2>What would you like FinnAi to do?</h2></div>', unsafe_allow_html=True)

    # Navigation Buttons
    if st.button("View and Edit Your Profile"):
        st.session_state["current_page"] = "profile_page"
    if st.button("Create a Budget"):
        st.session_state.current_page = "budget_tracker"
    if st.button("Track Your Expenses"):
        st.session_state.current_page = "expense_tracking"
    if st.button("Show Your Saving Progress"):
        st.session_state.current_page = "savings_progress"
    if st.button("Log Out"):
        st.session_state.update({"current_page": "login", "user_id": "", "username": ""})

# Main Execution
def run_main_page():
    if "user_id" not in st.session_state:
        st.error("User not logged in! Please log in first.")
    elif st.session_state.current_page == "main_menu":
        main_menu(st.session_state["user_id"])
    elif st.session_state.current_page == "budget_tracker":
        budget_tracker(st.session_state["user_id"])
    elif st.session_state.current_page == "expense_tracking":
        expense_tracking(st.session_state["user_id"])

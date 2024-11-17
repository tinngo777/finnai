import streamlit as st
import json
import requests

from firebase_setup import db


# Firebase API key (secure this in production)
FIREBASE_API_KEY = "AIzaSyCzROV0lpPfk6RdGeMV9iC8KklQEKpHaAA"

# Initialize navigation
if "current_page" not in st.session_state:
    st.session_state["current_page"] = "login"
if "user_id" not in st.session_state:
    st.session_state["user_id"] = ""
if "username" not in st.session_state:
    st.session_state["username"] = ""

# Firebase Functions
def sign_up_with_email_and_password(email, password, username=None):
    try:
        rest_api_url = "https://identitytoolkit.googleapis.com/v1/accounts:signUp"
        payload = {
            "email": email,
            "password": password,
            "returnSecureToken": True,
        }
        if username:
            payload["displayName"] = username
        payload = json.dumps(payload)
        r = requests.post(rest_api_url, params={"key": FIREBASE_API_KEY}, data=payload)
        if r.status_code == 200:
            # Successful signup
            response_data = r.json()
            st.session_state["user_id"] = response_data["localId"]
            st.session_state["username"] = username or "User"
            st.session_state["current_page"] = "questionnaire"  # Redirect to profile setup
            st.success("Signup successful! Redirecting to profile setup...")
        else:
            # Handle specific Firebase errors
            error_message = r.json().get('error', {}).get('message', '')
            if error_message == "EMAIL_EXISTS":
                st.warning("This email is already associated with an account. Please sign in instead.")
            else:
                st.warning(f"Sign-up failed: {error_message}")
    except Exception as e:
        st.error(f"An error occurred during sign-up: {e}")


def sign_in_with_email_and_password(email, password):
    try:
        rest_api_url = "https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword"
        payload = {
            "email": email,
            "password": password,
            "returnSecureToken": True
        }
        payload = json.dumps(payload)
        r = requests.post(rest_api_url, params={"key": FIREBASE_API_KEY}, data=payload)
        if r.status_code == 200:
            # Successful login
            data = r.json()
            st.session_state["user_id"] = data["localId"]
            st.session_state["username"] = data.get("displayName", "User")
            st.session_state["current_page"] = "main_page"  # Redirect to main page
            st.success("Login successful! Redirecting to dashboard...")
        else:
            # Handle specific error messages from Firebase
            error_message = r.json().get('error', {}).get('message', '')
            if error_message == "EMAIL_NOT_FOUND":
                st.warning("It seems you don't have an account with us. Please create a new account.")
            elif error_message == "INVALID_PASSWORD":
                st.warning("The password you entered is incorrect. Please try again.")
            else:
                st.warning(f"Sign-in failed: {error_message}")
    except Exception as e:
        st.error(f"An error occurred during sign-in: {e}")


def reset_password(email):
    try:
        rest_api_url = "https://identitytoolkit.googleapis.com/v1/accounts:sendOobCode"
        payload = {
            "email": email,
            "requestType": "PASSWORD_RESET"
        }
        payload = json.dumps(payload)
        r = requests.post(rest_api_url, params={"key": FIREBASE_API_KEY}, data=payload)
        if r.status_code == 200:
            st.success("Password reset email sent successfully.")
        else:
            error_message = r.json().get('error', {}).get('message')
            st.warning(f"Password reset failed: {error_message}")
    except Exception as e:
        st.error(f"Password reset failed: {e}")

# Login Form
def login_form():
    st.subheader("Sign In to FinnAi")
    email = st.text_input("Email Address")
    password = st.text_input("Password", type="password")
    if st.button("Sign In"):
        sign_in_with_email_and_password(email, password)

    if st.button("Create new account"):
        st.session_state["current_page"] = "signup"

# Sign-Up Form
def signup_form():
    st.subheader("Create a FinnAi Account")
    email = st.text_input("Enter Email")
    password = st.text_input("Enter Password", type="password")
    username = st.text_input("Choose a Username")
    if st.button("Sign Up"):
        sign_up_with_email_and_password(email, password, username)

    if st.button("Back to Sign In"):
        st.session_state["current_page"] = "login"

# Main Display Logic
def run_account():
    if st.session_state["current_page"] == "login":
        login_form()
    elif st.session_state["current_page"] == "signup":
        signup_form()

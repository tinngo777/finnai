import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore
import datetime

# Firebase init
if not firebase_admin._apps:
    cred = credentials.Certificate("firebase-adminsdk.json")
    firebase_admin.initialize_app(cred)

# Firestore instance
db = firestore.client()


def get_user_id():
    return st.session_state.get("user_id")

def get_saving_goal(user_id):
    doc = db.collection("users").document(user_id).get()
    if doc.exists:
        user_data = doc.to_dict()
        saving_goal = user_data.get("saving_goal", {})
        if saving_goal:
            return saving_goal["target"], saving_goal.get("timeframe", "No timeframe provided")
    return None, None


def get_saving_data(user_id, timeframe):
    # User choose 
    today = datetime.date.today()
    if timeframe == "Last Month":
        start_date = today - datetime.timedelta(days=30)
    elif timeframe == "Last 3 Months":
        start_date = today - datetime.timedelta(days=90)
    elif timeframe == "Last 6 Months":
        start_date = today - datetime.timedelta(days=180)
    elif timeframe == "Last Year":
        start_date = today - datetime.timedelta(days=365)
    else:
        start_date = today

    # Fetch saving data from Firestore
    saving_data = db.collection("users").document(user_id).collection("savings").where(
        "date", ">=", start_date).stream()
    
    total_saving = 0
    for record in saving_data:
        total_saving += record.to_dict().get("amount", 0)
    
    return total_saving

def display_saving_progress(user_id):
    st.title("Your Saving Progress")

    # Fetch saving goals and timeframe
    target, timeframe = get_saving_goal(user_id)
    if not target:
        st.error("Saving goal not set. Please check your profile again.")
        return
    
    st.write(f"**Saving Goal:** ${target}")
    st.write(f"**Timeframe:**{timeframe}")

    # User choose which timeframe for saving visualization
    timeframe_option = st.selectbox("Select Timeframe", ["Last Month", "Last 3 Months", "Last 6 Months", "Last Year"])


    # Fetch saving data for selected timeframe
    total_saving = get_saving_data(user_id, timeframe_option)


    # Calculate progress
    progress = total_saving / target if target > 0 else 0


    # Display progress bar and summary
    st.progress(progress)
    st.write(f"**Total Saving:** ${total_saving}")
    if progress >= 1.0:
        st.success("Congratulations! You've achieved your saving goal!")
    else:
        st.info(f"You are {100 - (progress * 100):.2f}% away from your goal!")


def saving_progress_main(user_id):
    st.sidebar.title("Saving Progress")
    display_saving_progress(user_id)


if __name__== "__main__":
    user_id = get_user_id()
    if user_id:
        saving_progress_main(user_id)
    else:
        st.error("Please log in again to view your progress.")

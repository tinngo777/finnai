import streamlit as st
import datetime
from firebase_setup import db


def questionnaire(user_id):
    st.title("Let's tell us something about yourself.")

    # User input fields
    first_name = st.text_input("First Name", key="first_name_input")
    last_name = st.text_input("Last Name", key="last_name_input")
    middle_name = st.text_input("Middle Name (optional)", key="middle_name_input")
    phone = st.text_input("Phone", key="phone_input")
    email = st.text_input("Email", key="email_input")
    dob = st.date_input(
        "Your Date of Birth",
        min_value=datetime.date(1900, 1, 1),
        max_value=datetime.date.today(),
        key = "dob_input"
    )
    monthly_income = st.number_input("Monthly Income", min_value=0, step=100, key = "income_input")
    monthly_expenses = st.number_input("Monthly Expenses", min_value=0, step=100, key = "expenses_input")
    saving_goal = st.number_input("Saving Goal", min_value=0, step=100, key = "goal_input")

    if st.button("Submit", key="submit_button"):
        # Save the profile data
        data = {
            "first_name": first_name,
            "last_name": last_name,
            "middle_name": middle_name,
            "phone": phone,
            "email": email,
            "dob": dob.strftime("%Y-%m-%d"),
            "monthly_income": monthly_income,
            "monthly_expenses": monthly_expenses,
            "saving_goal": saving_goal,
        }
        db.collection("users").document(user_id).set(data, merge=True)
        st.success("Your profile has been saved!")
        st.session_state.current_page = "main_menu"

def profile_page(user_id):
    st.title("Your Profile")

    # Fetch user data from Firestore
    user_doc = db.collection("users").document(user_id).get()
    user_data = user_doc.to_dict() if user_doc.exists else None

    if user_data is None:
        st.error("User profile not found.")
        return

    # Profile picture (circular)
    st.write("### Profile Picture")
    if user_data.get("profile_picture"):
        st.image(user_data["profile_picture"], width=150, caption="Profile Picture", use_column_width=False)
    else:
        # Circular placeholder
        st.markdown(
            """
            <div style="width: 150px; height: 150px; border-radius: 50%; background: lightgray; display: flex; justify-content: center; align-items: center; margin-bottom: 10px;">
                <span style="font-size: 16px; color: gray;">Add Photo</span>
            </div>
            """,
            unsafe_allow_html=True,
        )
        uploaded_file = st.file_uploader("Upload a new profile picture", type=["jpg", "png", "jpeg"])
        if uploaded_file:
            user_data["profile_picture"] = uploaded_file.getvalue()  # Save binary image data
            db.collection("users").document(user_id).update({"profile_picture": user_data["profile_picture"]})
            st.success("Profile picture updated!")

    # Display user info
    st.write(f"**Name:** {user_data['first_name']} {user_data['middle_name']} {user_data['last_name']}")
    st.write(f"**Phone:** {user_data['phone']}")
    st.write(f"**Email:** {user_data['email']}")
    st.write(f"**Date of Birth:** {user_data['dob']}")
    st.write(f"**Monthly Income:** ${user_data['monthly_income']}")
    st.write(f"**Monthly Expenses:** ${user_data['monthly_expenses']}")
    st.write(f"**Savings Goal:** ${user_data['saving_goal']}")

    if st.button("Edit Profile"):
        st.session_state.current_page = "questionnaire"
        if st.session_state.profile_submitted == False:
            st.success("Your profile is saved!")
            if st.button("Go to Main Page"):
                st.session_state.current_page = "main_page"


# Main block for testing
if __name__ == "__main__":
    if "current_page" not in st.session_state:
        st.session_state.current_page = "questionnaire"
    if "user_id" not in st.session_state:
        st.session_state.user_id = "test_user_id"  # Replace with actual user_id from session_state

    if st.session_state.current_page == "questionnaire":
        questionnaire(st.session_state.user_id)
    elif st.session_state.current_page == "profile_page":
        profile_page(st.session_state.user_id)

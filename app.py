import streamlit as st
from budget_tracker import budget_tracker
from expense_tracking import expense_tracking

# Sidebar for navigation
st.sidebar.title("Navigation")
option = ["Welcome", "Budget Tracker", "Expense Tracking", "Visualization", "Saving Goal"]
page = st.sidebar.radio("Go to", option)

# Render the selected page
if page == "Budget Tracker":
    budget_tracker()
elif page == "Expense Tracking":
    expense_tracking()
elif page == "Visualization":
    st.write("Visualization page coming soon!")
elif page == "Saving Goal":
    st.write("Saving Goal page coming soon!")
else:
    st.write("Welcome to the Financial Tracker App!")

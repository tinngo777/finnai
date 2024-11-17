import streamlit as st
import pandas as pd
from firebase_setup import db  # Ensure db is a Firestore client, not Realtime Database

# Budget Tracker Function
def budget_tracker(user_id):
    st.title("Budget Tracker")

    if not user_id:
        st.error("User not logged in! Please log in to manage your budget.")
        return

    if 'budget_entries' not in st.session_state:
        st.session_state['budget_entries'] = [{'Category': '', 'OriginalValue': 0.0}]

    # Create placeholders for budget entries
    st.subheader("Add Budget Entries")

    categories = ["Rent", "Food", "Utilities", "Shopping", "Tuition", "Other"]

    # Function to add a new blank entry
    def add_entry():
        st.session_state['budget_entries'].append({'Category': '', 'OriginalValue': 0.0})

    # Display input fields for each entry
    for idx, entry in enumerate(st.session_state['budget_entries']):
        col1, col2 = st.columns(2)
        with col1:
            entry['Category'] = st.selectbox(
                f"Category {idx + 1}",
                options=[""] + categories,
                index=categories.index(entry['Category']) + 1 if entry['Category'] else 0,
                key=f"category_{idx}"
            )
        with col2:
            entry['OriginalValue'] = st.number_input(
                f"Original Budget {idx + 1} (in $)",
                value=entry['OriginalValue'],
                min_value=0.0,
                step=0.01,
                key=f"original_value_{idx}"
            )

    # Button to add a new entry
    if st.button("Add Another Entry"):
        add_entry()

    # Submit all entries
    if st.button("Submit All"):
        # Filter out invalid entries
        valid_entries = [
            {
                **entry,
                'RemainingValue': entry['OriginalValue']  # Set RemainingValue = OriginalValue
            }
            for entry in st.session_state['budget_entries']
            if entry['Category'] and entry['OriginalValue'] > 0
        ]

        if valid_entries:
            try:
                # Reference the logged-in user's budget_entries collection
                collection_ref = db.collection("users").document(user_id).collection("budget_entries")
                
                # Add each valid entry with custom document ID
                for entry in valid_entries:
                    collection_ref.document(entry['Category']).set(entry)

                st.success(f"Submitted {len(valid_entries)} entries successfully!")
                st.write(pd.DataFrame(valid_entries))
                st.session_state['budget_entries'] = [{'Category': '', 'OriginalValue': 0.0}]  # Reset entries
            except Exception as e:
                st.error(f"An error occurred while submitting data to Firestore: {e}")


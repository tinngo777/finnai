import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from firebase_setup import db  # Ensure this is your Firestore client setup
from datetime import datetime
from google.cloud import firestore



# Fetch budget data for a specific user from Firebase
def fetch_budget(user_id):
    try:
        budgets_ref = db.collection("users").document(user_id).collection("budget_entries")
        docs = budgets_ref.stream()

        # Convert Firestore documents to a dictionary
        budget = {
            doc.id: {
                "OriginalValue": doc.to_dict().get("OriginalValue", 0),
                "RemainingValue": doc.to_dict()["RemainingValue"]
            }
            for doc in docs
        }
        return budget
    except Exception as e:
        st.error(f"Error fetching budgets: {e}")
        return None

# Update budget for a specific user in Firebase
def update_budget(user_id, category, new_value):
    try:
        budget_ref = db.collection("users").document(user_id).collection("budget_entries").document(category)
        budget_ref.update({"RemainingValue": new_value})
        return True
    except Exception as e:
        st.error(f"Error updating budget: {e}")
        return False

# Add an expense entry to Firebase with description
def add_expense(user_id, category, value, description):
    try:
        # Reference the expense document for the category
        expense_ref = db.collection("users").document(user_id).collection("expense_entries").document(category)

        # Add the expense entry to the Expenses array
        expense_entry = {
            "Value": value,
            "Timestamp": datetime.now().isoformat(),
            "Description": description
        }
        expense_ref.set(
            {"Expenses": firestore.ArrayUnion([expense_entry])}, merge=True
        )
        return True
    except Exception as e:
        st.error(f"Error adding expense: {e}")
        return False


# Fetch expenses for all categories
def fetch_expenses(user_id):
    try:
        expenses_ref = db.collection("users").document(user_id).collection("expense_entries")
        docs = expenses_ref.stream()

        # Aggregate expenses by category
        expenses = {
            doc.id: sum(entry["Value"] for entry in doc.to_dict().get("Expenses", []))
            for doc in docs
        }
        return expenses
    except Exception as e:
        st.error(f"Error fetching expenses: {e}")
        return None

# Fetch expenses and create a pie chart
def visualize_expenses(expenses):
    if expenses:
        st.subheader("Expense Breakdown")
        # Create a pie chart
        fig, ax = plt.subplots()
        ax.pie(expenses.values(), labels=expenses.keys(), autopct="%1.1f%%")
        ax.axis("equal")  # Equal aspect ratio ensures the pie chart is circular
        st.pyplot(fig)
    else:
        st.error("No expenses found to visualize!")

# Bar plot for original vs remaining budget
def plot_budget_comparison(budget):
    st.subheader("Budget Comparison: Original vs Remaining")
    
    # Prepare data for plotting
    categories = list(budget.keys())
    original_values = [details["OriginalValue"] for details in budget.values()]
    remaining_values = [details["RemainingValue"] for details in budget.values()]
    
    # Create horizontal bar plot
    fig, ax = plt.subplots(figsize=(8, len(categories) * 0.6))  # Adjust height based on number of categories
    bar_height = 0.4
    
    y_pos = range(len(categories))
    ax.barh(y_pos, original_values, height=bar_height, label="Original Budget", alpha=0.7, color="blue")
    ax.barh(y_pos, remaining_values, height=bar_height, label="Remaining Budget", alpha=0.7, color="green")
    
    # Extend x-axis limits for label placement
    max_value = max(original_values + remaining_values)
    ax.set_xlim(0, max_value * 1.2)  # Add 20% extra space to the right

    # Add labels to the bars for Remaining Value
    for i, remaining in enumerate(remaining_values):
        ax.text(
            remaining + max_value * 0.02,  # Slightly to the right of the bar
            i,                             # Corresponding y-position
            f"${remaining:.2f}",           # Display as a dollar amount
            va="center",                   # Centered vertically
            fontsize=9,                    # Adjust font size
            color="black"
        )
    
    # Customize the plot
    ax.set_yticks(y_pos)
    ax.set_yticklabels(categories)
    ax.set_xlabel("Budget ($)")
    ax.set_title("Original vs Remaining Budget")
    ax.legend()

    # Display the plot
    st.pyplot(fig)


# Streamlit App
def expense_tracking(user_id):
    st.title("Expense Tracking")

    if not user_id:
        st.error("User not logged in! Please log in to track your expenses.")
        return

    # Fetch budget data for the logged-in user
    budget = fetch_budget(user_id)
    if not budget:
        st.error("No budget data found for this user!")
        return

    # Display remaining and original budget
    st.subheader("Budget Overview")
    budget_df = pd.DataFrame.from_dict(
        {
            category: {
                "Original Budget": details["OriginalValue"],
                "Remaining Budget": details["RemainingValue"]
            }
            for category, details in budget.items()
        },
        orient="index"
    )
    st.write(budget_df)

    # Plot budget comparison
    plot_budget_comparison(budget)

    # Fetch and display the pie chart for expenses
    expenses = fetch_expenses(user_id)
    visualize_expenses(expenses)

    # Add Expense Section
    col1, col2, col3 = st.columns(3)

    with col1:
        category = st.selectbox("Select Expense Category", list(budget.keys()))
    with col2:
        value = st.number_input("Enter Expense Value", min_value=0.0, step=1.0)
    with col3:
        description = st.text_input("Enter Description")

    if st.button("Add Expense"):
        if category in budget:
            if value <= budget[category]["RemainingValue"]:
                new_budget_value = budget[category]["RemainingValue"] - value
                if update_budget(user_id, category, new_budget_value):
                    if add_expense(user_id, category, value, description):
                        st.success(f"Expense added! Remaining budget for {category}: ${new_budget_value:.2f}")
                    else:
                        st.error("Failed to log the expense in Firebase.")
                else:
                    st.error("Failed to update the budget in Firebase.")
            else:
                st.error(f"Not enough budget for {category}. Current budget: ${budget[category]['RemainingValue']:.2f}")
        else:
            st.error("Invalid category selected!")

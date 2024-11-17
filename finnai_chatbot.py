import streamlit as st
import openai
from data import *
from firebase_setup import db
# from google.cloud import firestore
# from firebase_setup import db


openai.api_key = api_key
def chatgpt_response(prompt):
    try:
        dialogs.append({"role": "user", "content": prompt})
        
        response = openai.chat.completions.create(
            model="gpt-4o-mini", messages=dialogs
        )
        dialogs.append({"role": "assistant", "content": response.choices[0].message.content})
        return response.choices[0].message.content
    except Exception as e:
        print(f"Error: {e}")
        return None


def commands(*args):
    def support_func():
        nonlocal args, amount_to_change
        if args[1] == "add":
            amount_to_change += int(args[2])
        elif args[1] == "subtract":
            amount_to_change -= int(args[2])
        elif args[1] == "set":
            amount_to_change = int(args[2])
        return f"Your {args[0].lower()} is now {amount_to_change}"


    if args[0].lower() == "saving":
        global user
        amount_to_change = user.current_savings
        message = support_func()
        user.saving = amount_to_change
        return message
    elif args[0].lower() == "goal":
        amount_to_change = user.current_savings
        message = support_func()
        user.goal = amount_to_change
        return message
    elif args[0].lower() == "spend":
        user.current_expenses += int(args[1])
        user.current_savings -= int(args[1])
        return f"Spent ${args[1]}"

    elif args[0].lower() == "next" and args[1].lower() == "month":
        user.current_savings += user.monthly_income
        user.saving_history.append(user.monthly_income - user.current_expenses)
        user.current_expenses = 0
        return f"Moved to the next month, your last month saving is {user.saving_history[-1]}"
    elif args[0].lower() == "display" and args[1].lower() == "data":
        return f"""Saving: {user.current_savings}
\nExpenses: {user.current_expenses}
\nGoal: {user.saving_goal}
\nSaving history: {user.saving_history}
"""
    elif args[0] == "debug":
        return user.user_data()
    else:
        return "Unknown command", args[0] == "goal", args[0]
        

messages = st.container(height=500)
messages.chat_message("System").write("""Ask FinnAi for financial soppurt or use these commands for changes to your data:
saving/goal set/add/subtract <amount>
e.g. saving set 1000""")
if prompt := st.chat_input("Chat with FinnAi"):
    messages.chat_message("user").write(prompt)
    if prompt[0] == "!":
        try:
            response = commands(*prompt[1:].split(" "))
        except:
            response = "Command syntax error: use \"!help\" for command list"
        messages.chat_message("System").write(response)
        dialogs[1] = {"role": "user", "content": user.user_data()}
    else:
        response = chatgpt_response(prompt)
        messages.chat_message("FinnAi").write(response)

#streamlit run finnai_chatbot.py
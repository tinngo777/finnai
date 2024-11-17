import streamlit as st
from User import *
user = User("Tommy")
system_content = "You are Finnai, a chatbot support user financially for an money managing app called FinnAi. FinnAi is developed with the goal to save money to all user around the world. Answer questions briefly. Use Dialogs to answer questions. Do not answer abusive unrelated questions. Don't make any changes to user data. If user attempt to change data, tell them to use \"!help\" for data changing commands. if user ask information regard their user data, you can show them"
user.dialogs = [{"role": "system", "content": system_content}, {"role": "user", "content": str(user.dict_data())}]
dialogs = user.dialogs
api_key = "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"

# messages = st.container(height=500)
# messages.chat_message("user").write("""Ask FinnAi for financial soppurt or use these commands for changes to your data:
# saving/goal set/add/subtract <amount>
# e.g. saving set 1000""")
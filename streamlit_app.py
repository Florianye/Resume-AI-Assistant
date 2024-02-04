# Main execution block for Streamlit app
import streamlit as st
from ai_assistant import initialize_bot, interact_with_bot
import dotenv
import os

st.title("CV Chatbot")
st.write("Ask questions about the CV and get answers from the chatbot.")

# #@st.cache_data()
# def initialize_bot_st():
#     dotenv.load_dotenv(".env", override=True)
#     qa_with_source = initialize_bot(os.environ["OPENAI_API_KEY"])#OPENAI_API_KEY=st.secrets["OPENAI_API_KEY"])
#     return qa_with_source

dotenv.load_dotenv(".env", override=True)
qa_with_source = initialize_bot(os.environ["OPENAI_API_KEY"])

# Store LLM generated responses
if "messages" not in st.session_state.keys():
    st.session_state.messages = [{"role": "assistant", "content": "How may I assist you today?"}]

# Display or clear chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

def clear_chat_history():
    st.session_state.messages = [{"role": "assistant", "content": "How may I assist you today?"}]
st.sidebar.button('Clear Chat History', on_click=clear_chat_history)

# User-provided prompt
prompt = st.chat_input()
if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

#st.write(st.session_state.messages)

# Generate a new response if last message is not from assistant
if st.session_state.messages[-1]["role"] != "assistant":
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = interact_with_bot(qa_with_source, prompt)
            st.write(response)
    message = {"role": "assistant", "content": response}
    st.session_state.messages.append(message)
import streamlit as st
from chatbot import ChatBot
import tempfile
from langchain.schema import SystemMessage

if "chat_history" not in st.session_state:
    st.session_state.chat_history = [SystemMessage(content="You are a helpful assistant.")]
if "bot" not in st.session_state:
    st.session_state.bot = ChatBot(chat_history=st.session_state.chat_history)

st.set_page_config(page_title="Smart Assistant", layout="centered")
st.title("ChatBot Smart Assistant")

st.sidebar.header("Settings")
web_search_enabled = st.sidebar.toggle("Web Search")

uploaded_file = st.sidebar.file_uploader("Upload a PDF", type="pdf")
if uploaded_file:
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
        tmp_file.write(uploaded_file.read())
        success_msg = st.session_state.bot.extract_text_from_pdf(tmp_file.name)
        st.sidebar.success(success_msg)

user_input = st.chat_input("write message here...")

if user_input:  
    if web_search_enabled:
        reply = st.session_state.bot.web_search_chat(user_input)
    else:
        reply = st.session_state.bot.normal_chat(user_input)

for speaker, message in st.session_state.bot.get_full_conversation():
    if speaker == "Me":
        st.markdown(f"**Me:** {message}")
    else:
        st.markdown(f"**Chatbot:** {message}")

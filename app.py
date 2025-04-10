import streamlit as st
from chatbot import ChatBot  
import tempfile

bot = ChatBot()
st.title("ChatBot Assistant")

st.sidebar.subheader("Choose a Mode")
mode = st.sidebar.radio("Select Mode", ["Normal Chat", "PDF Mode", "Web Search"])

uploaded_file = None
if mode == "PDF Mode":
    uploaded_file = st.sidebar.file_uploader("Upload a PDF", type="pdf")
    if uploaded_file:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
            tmp_file.write(uploaded_file.read())
            pdf_response = bot.extract_text_from_pdf(tmp_file.name)
            st.sidebar.success(pdf_response)


user_input = st.text_input("Enter the Message:", key="user_input", placeholder='Write Something...')

response_placeholder = st.empty()


if st.button("Send"):
    if mode == "Normal Chat":
        if user_input:
            response = bot.normal_chat(user_input)
            response_placeholder.markdown(f"**Normal Chat Result:** {response}")
        else:
            st.warning("Please enter a message.")

    elif mode == "Web Search":
        if user_input:
            response = bot.web_search_chat(user_input)
            response_placeholder.markdown(f"**Web Search Result:** {response}")
        else:
            st.warning("Please enter a message.")

    elif mode == "PDF Mode":
        if not uploaded_file:
            st.warning("Please upload a PDF first.")
        elif user_input:
            response = bot.answer_from_pdf(user_input)
            response_placeholder.markdown(f"**Result from PDF:** {response}")
        else:
            st.warning("Please enter a question.")


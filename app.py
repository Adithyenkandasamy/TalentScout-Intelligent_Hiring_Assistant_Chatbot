import streamlit as st
import google.generativeai as genai
from prompts import SYSTEM_PROMPT, TECH_QUESTION_PROMPT
from utils import is_exit_keyword
from dotenv import load_dotenv
import os

load_dotenv()

# Configure Gemini
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel(
    model_name="gemini-2.5-flash",
    system_instruction=SYSTEM_PROMPT
)

st.set_page_config(page_title="TalentScout Hiring Assistant", layout="centered")
st.title("🤖 TalentScout Hiring Assistant")

if "chat" not in st.session_state:
    st.session_state.chat = model.start_chat(history=[])

if "candidate" not in st.session_state:
    st.session_state.candidate = {}

user_input = st.chat_input("Type your response here...")

if user_input:
    if is_exit_keyword(user_input):
        st.chat_message("assistant").write(
            "Thank you for your time! 🎉 Our recruitment team will contact you if your profile matches."
        )
        st.stop()

    # User message
    st.chat_message("user").write(user_input)

    # Gemini response
    response = st.session_state.chat.send_message(user_input)
    st.chat_message("assistant").write(response.text)

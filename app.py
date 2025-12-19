import streamlit as st
from google import genai
from google.genai import types, errors
from prompts import SYSTEM_PROMPT, TECH_QUESTION_PROMPT
from utils import is_exit_keyword
from dotenv import load_dotenv
import os

load_dotenv()

# Configure Gemini
@st.cache_resource
def get_client():
    return genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

client = get_client()

st.set_page_config(page_title="TalentScout Hiring Assistant", layout="centered")
st.title("🤖 TalentScout Hiring Assistant")

if "chat" not in st.session_state:
    st.session_state.chat = client.chats.create(
        model="gemini-2.0-flash-exp",
        config=types.GenerateContentConfig(
            system_instruction=SYSTEM_PROMPT
        )
    )

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
    try:
        response = st.session_state.chat.send_message(user_input)
        st.chat_message("assistant").write(response.text)
    except errors.ClientError as e:
        if e.code == 429:
            st.error("⚠️ API Quota Exceeded. Please try again later.")
        elif e.code == 404:
            st.error("⚠️ Model not found. Check your API configuration.")
        else:
            st.error(f"⚠️ An error occurred: {e}")
    except Exception as e:
        st.error(f"⚠️ An unexpected error occurred: {e}")

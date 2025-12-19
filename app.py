import streamlit as st
from groq import Groq
from prompts import SYSTEM_PROMPT, TECH_QUESTION_PROMPT
from utils import is_exit_keyword, get_tech_stack_note, save_interview
from dotenv import load_dotenv
import os


load_dotenv()

# Configure Groq
@st.cache_resource
def get_client():
    return Groq(api_key=os.getenv("GROQ_API_KEY"))

client = get_client()

st.set_page_config(page_title="TalentScout Hiring Assistant", layout="centered")
st.title("🤖 TalentScout Hiring Assistant")

# Sidebar
with st.sidebar:
    st.header("Controls")
    if st.button("🗑️ Clear Chat"):
        st.session_state.messages = []
        st.rerun()
    
    if st.button("💾 Download Transcript"):
        if st.session_state.messages:
            filename = save_interview(st.session_state.messages)
            st.success(f"Saved to {filename}")
            with open(filename, "r") as f:
                st.download_button(
                    label="📥 Click to Download JSON",
                    data=f,
                    file_name=os.path.basename(filename),
                    mime="application/json"
                )
        else:
            st.warning("No chat history to save.")

    st.markdown("---")
    st.markdown("**Model:** `llama-3.3-70b-versatile`")
    st.markdown("**Powered by:** [Groq](https://groq.com)")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

user_input = st.chat_input("Type your response here...")

if user_input:
    if is_exit_keyword(user_input):
        st.chat_message("assistant").write(
            "Thank you for your time! 🎉 Our recruitment team will contact you if your profile matches."
        )
        st.stop()

    # User message
    st.session_state.messages.append({"role": "user", "content": user_input})
    st.chat_message("user").write(user_input)

    # Tech Stack Logic
    system_note = get_tech_stack_note(user_input)
    
    # Auto-save Logic
    if is_exit_keyword(user_input):
        filename = save_interview(st.session_state.messages)
        st.chat_message("assistant").write(
            f"Thank you! Your interview has been saved to `{filename}`. Our team will review it shortly. 👋"
        )
        st.stop()

    # Prepare messages for Groq
    messages_payload = [{"role": "system", "content": SYSTEM_PROMPT}] + st.session_state.messages
    if system_note:
        # Inject steering instruction as a system message at the end
        messages_payload.append({"role": "system", "content": system_note})
            
    # Groq response
    try:
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=messages_payload,
            temperature=0.7,
            max_tokens=1024,
            top_p=1,
            stream=False,
            stop=None,
        )
        response_text = completion.choices[0].message.content
        st.session_state.messages.append({"role": "assistant", "content": response_text})
        st.chat_message("assistant").write(response_text)
    except Exception as e:
        st.error(f"⚠️ An error occurred: {e}")


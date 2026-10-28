import os
import streamlit as st
from dotenv import load_dotenv
from groq import Groq

# Load environment variables
load_dotenv()

# Configure Streamlit page
st.set_page_config(
    page_title="AI Chatbot with Memory",
    page_icon="🤖",
    layout="centered"
)

st.title("🤖 AI Chatbot with Memory")
st.caption("Powered by Groq and GPT-OSS 20B")

# Initialize Groq client
api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    st.error("GROQ_API_KEY not found. Please add it to your .env file.")
    st.stop()

client = Groq(api_key=api_key)

# Initialize conversation memory
if "conversation" not in st.session_state:
    st.session_state.conversation = []

# Display previous messages
for message in st.session_state.conversation:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])


# Chat input
user_message = st.chat_input("Ask me anything...")

if user_message:
    # Display user message
    with st.chat_message("user"):
        st.markdown(user_message)

    # Store user message in conversation memory
    st.session_state.conversation.append({
        "role": "user",
        "content": user_message
    })

    # Generate AI response
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                response = client.chat.completions.create(
                    model="openai/gpt-oss-20b",
                    messages=st.session_state.conversation,
                    temperature=0.2
                )

                reply = response.choices[0].message.content
                st.markdown(reply)

                # Store AI response in conversation memory
                st.session_state.conversation.append({
                    "role": "assistant",
                    "content": reply
                })

            except Exception as e:
                st.error(f"Sorry, something went wrong: {e}")

# Sidebar controls
with st.sidebar:
    st.header("Chat Settings")

    st.write(
        f"Messages in memory: {len(st.session_state.conversation)}"
    )

    if st.button("🗑️ Clear Conversation"):
        st.session_state.conversation = []
        st.rerun()
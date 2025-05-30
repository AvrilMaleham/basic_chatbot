import streamlit as st
from openai import OpenAI
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Set page config
st.set_page_config(page_title="Avril's AI Chat", page_icon="🤖")

# Title
st.title("🤖 Avril's AI Chat")

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Initialize session state for messages
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
if prompt := st.chat_input("Type your message..."):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Generate AI response
    with st.chat_message("assistant"):
        try:
            stream = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=st.session_state.messages,
                stream=True,
            )
            
            response = st.write_stream(stream)
            
        except Exception as e:
            st.error(f"Error: {str(e)}")
            response = "Sorry, I encountered an error."
    
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response})
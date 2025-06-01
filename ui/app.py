import streamlit as st
import requests

st.set_page_config(page_title="Avril's AI Chat", page_icon="🤖")
st.title("🤖 Avril's AI Chat")

API_URL = "http://api:8000/ask/"

if "messages" not in st.session_state:
    st.session_state.messages = []

if prompt := st.chat_input("Type your message..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    try:
        response = requests.post(API_URL, json={"query": prompt})
        response.raise_for_status()
        data = response.json()
        answer = data.get("answer", "Sorry, I couldn't find an answer.")
    except Exception as e:
        answer = f"Error contacting the API: {e}"
  
    st.session_state.messages.append({"role": "assistant", "content": answer})

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

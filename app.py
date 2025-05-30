import streamlit as st
from utils import load_vectorstore, create_qa_chain

st.set_page_config(page_title="Avril's AI Chat", page_icon="🤖")
st.title("🤖 Avril's AI Chat")

@st.cache_resource
def init_qa_chain():
    vectorstore = load_vectorstore()
    return create_qa_chain(vectorstore)

qa_chain = init_qa_chain()

if "messages" not in st.session_state:
    st.session_state.messages = []

if prompt := st.chat_input("Type your message..."):
    st.session_state.messages.append({"role": "user", "content": prompt})

    response = qa_chain.invoke(prompt)
    if isinstance(response, dict):
        answer = response.get('result', 'Sorry, no answer found.')
    else:
        answer = response
    st.session_state.messages.append({"role": "assistant", "content": answer})

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

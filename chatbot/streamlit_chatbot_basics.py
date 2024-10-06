import streamlit as st

with st.chat_message(name = "user", avatar= "👤"):
    st.write("Hello!")

with st.chat_message(name = "bot", avatar= "🤖"):
    st.write("Hello! How may I assist you?")
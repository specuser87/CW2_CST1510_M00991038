import streamlit as st
from ai_assistant import generate_ai_response

st.title("AI Cybersecurity Assistant")

user_input = st.text_area("Enter your cybersecurity data or question:")

if st.button("Analyze"):
    if user_input.strip():
        with st.spinner("Thinking..."):
            ai_response = generate_ai_response(user_input)
            st.write(ai_response)
    else:
        st.warning("Please enter some text first.")

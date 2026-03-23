import streamlit as st
import requests
import os
from dotenv import load_dotenv

load_dotenv()

API_URL = os.getenv("API_URL", "http://localhost:8000/query")

st.set_page_config(page_title="Agentic Assistant", page_icon="🤖")
st.title("🤖 Agentic Research Assistant")
st.markdown("Ask a question, and the agent will decide which tools to use.")

question = st.text_input("Your question:")

if st.button("Ask"):
    if question:
        with st.spinner("Thinking..."):
            try:
                response = requests.post(API_URL, json={"question": question})
                if response.status_code == 200:
                    data = response.json()
                    st.write("**Answer:**", data["answer"])
                    with st.expander("See reasoning steps"):
                        for step in data.get("steps", []):
                            st.write(f"- {step}")
                else:
                    st.error(f"Error: {response.status_code}")
            except Exception as e:
                st.error(f"Connection error: {e}")
    else:
        st.warning("Please enter a question.")
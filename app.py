import streamlit as st
import json
import google.generativeai as genai

st.set_page_config(page_title="ARE", layout="wide")

st.title("🧠 Adversarial Reasoning Engine")

# ------------------------
# API KEY INPUT
# ------------------------
api_key = st.sidebar.text_input("Gemini API Key", type="password")

model = None

if api_key:
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel("gemini-1.5-flash")
        st.sidebar.success("Model loaded successfully")
    except Exception as e:
        st.sidebar.error(f"Error: {str(e)}")

# ------------------------
# CORE FUNCTION
# ------------------------
def run_engine(prompt):
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"ERROR: {str(e)}"

# ------------------------
# UI
# ------------------------
user_input = st.text_area("Enter your question")

if st.button("Run"):
    if not api_key:
        st.warning("Enter API key")
    elif not model:
        st.error("Model not initialized")
    elif not user_input.strip():
        st.warning("Enter a question")
    else:
        result = run_engine(user_input)
        st.write(result)

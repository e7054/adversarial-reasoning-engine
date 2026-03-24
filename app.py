import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="ARE", layout="wide")

st.title("🧠 Adversarial Reasoning Engine")

# ------------------------
# API KEY
# ------------------------
api_key = st.sidebar.text_input("Gemini API Key", type="password")

model = None

if api_key:
    try:
        genai.configure(api_key=api_key)

        models = list(genai.list_models())

        valid_model = None

        for m in models:
            if "generateContent" in m.supported_generation_methods:
                valid_model = m.name
                break

        if valid_model:
            model = genai.GenerativeModel(valid_model)
            st.sidebar.success(f"Using model: {valid_model}")
        else:
            st.sidebar.error("No compatible models found")

    except Exception as e:
        st.sidebar.error(str(e))

# ------------------------
# RUN
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
        st.error("Model not available")
    elif not user_input.strip():
        st.warning("Enter a question")
    else:
        result = run_engine(user_input)
        st.write(result)

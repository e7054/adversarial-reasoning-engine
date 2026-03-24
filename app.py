import streamlit as st
import json
import re
import google.generativeai as genai

st.set_page_config(page_title="Adversarial Reasoning Engine", layout="wide")

st.title("🧠 Adversarial Reasoning Engine")

# Sidebar
st.sidebar.header("Setup")
gemini_key = st.sidebar.text_input("Gemini API Key", type="password")

model = None
model_name = None

if gemini_key:
    genai.configure(api_key=gemini_key)

    try:
        models = list(genai.list_models())

        for m in models:
            if "generateContent" in m.supported_generation_methods:
                model_name = m.name
                break

        if model_name:
            model = genai.GenerativeModel(model_name)

    except Exception as e:
        st.sidebar.error(str(e))

if model_name:
    st.sidebar.success(f"Using: {model_name}")
else:
    st.sidebar.warning("No valid model detected")

# Helpers
def extract_json(text):
    try:
        return json.loads(text)
    except:
        match = re.search(r"\{.*\}", text, re.DOTALL)
        if match:
            return json.loads(match.group(0))
        return {"solution": text}

def call_model(prompt):
    return model.generate_content(prompt).text

def run_stage(prompt):
    return extract_json(call_model(prompt))

# Engine
def run_engine(user_input):
    progress = st.progress(0)
    status = st.empty()

    status.text("Understanding request...")
    progress.progress(25)
    data = run_stage(f"Return JSON. Break request: {user_input}")

    status.text("Building solution...")
    progress.progress(50)
    data = run_stage(f"Return JSON. Build solution: {json.dumps(data)}")

    status.text("Checking issues...")
    progress.progress(75)
    data = run_stage(f"Return JSON. Find issues: {json.dumps(data)}")

    status.text("Improving solution...")
    progress.progress(100)
    data = run_stage(f"Return JSON. Fix everything: {json.dumps(data)}")

    return data

# UI
user_input = st.text_area("What do you want help with?", height=150)

if st.button("Run Analysis"):
    if not gemini_key:
        st.warning("Enter API key")
    elif not model:
        st.error("No valid model available")
    elif not user_input.strip():
        st.warning("Enter a request")
    else:
        result = run_engine(user_input)

        st.subheader("Final Answer")
        st.write(result.get("solution", result))

        with st.expander("Technical Details"):
            st.json(result)

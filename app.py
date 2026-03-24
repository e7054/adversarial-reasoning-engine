import streamlit as st
import json
import re
import google.generativeai as genai

st.set_page_config(page_title="Adversarial Reasoning Engine", layout="wide")

st.title("🧠 Adversarial Reasoning Engine")

# ------------------------
# SIDEBAR
# ------------------------
st.sidebar.header("Setup")
gemini_key = st.sidebar.text_input("Gemini API Key", type="password")

model = None
model_name = None

if gemini_key:
    try:
        genai.configure(api_key=gemini_key)
        models = list(genai.list_models())

        for m in models:
            if "generateContent" in m.supported_generation_methods:
                model_name = m.name
                break

        if model_name:
            model = genai.GenerativeModel(model_name)

    except Exception as e:
        st.sidebar.error(f"Model init failed: {str(e)}")

if model_name:
    st.sidebar.success(f"Using: {model_name}")
else:
    st.sidebar.warning("No valid model detected")

# ------------------------
# HELPERS
# ------------------------
def extract_json(text):
    if not text:
        return {"error": "Empty response from model"}

    try:
        return json.loads(text)
    except:
        try:
            match = re.search(r"\{.*\}", text, re.DOTALL)
            if match:
                return json.loads(match.group(0))
        except:
            pass

    return {"raw_output": text}

def call_model(prompt):
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return json.dumps({"error": str(e)})

def run_stage(label, prompt):
    st.write(f"### {label}")
    raw = call_model(prompt)
    parsed = extract_json(raw)

    with st.expander(f"{label} Output"):
        st.write(parsed)

    return parsed

# ------------------------
# ENGINE
# ------------------------
def run_engine(user_input):
    data = run_stage(
        "1. Understanding",
        f"Return JSON with intent, constraints, requirements: {user_input}"
    )

    data = run_stage(
        "2. Build Solution",
        f"Return JSON with full solution: {json.dumps(data)}"
    )

    data = run_stage(
        "3. Critique",
        f"Return JSON listing flaws, risks, edge cases: {json.dumps(data)}"
    )

    data = run_stage(
        "4. Improve",
        f"Return JSON with corrected and final solution: {json.dumps(data)}"
    )

    return data

# ------------------------
# UI
# ------------------------
user_input = st.text_area("What do you want help with?", height=150)

if st.button("Run Analysis"):
    if not gemini_key:
        st.warning("Enter API key")
    elif not model:
        st.error("No valid model available")
    elif not user_input.strip():
        st.warning("Enter a request")
    else:
        with st.spinner("Running reasoning engine..."):
            result = run_engine(user_input)

        st.subheader("Final Answer")
        st.write(result.get("solution", result))

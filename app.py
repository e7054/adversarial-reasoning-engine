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

if gemini_key:
    try:
        genai.configure(api_key=gemini_key)
        models = list(genai.list_models())

        for m in models:
            if "generateContent" in m.supported_generation_methods:
                model = genai.GenerativeModel(m.name)
                break

    except Exception as e:
        st.sidebar.error(str(e))

# ------------------------
# HELPERS
# ------------------------
def extract_json(text):
    if not text:
        return {"error": "Empty response"}

    try:
        return json.loads(text)
    except:
        match = re.search(r"\{.*\}", text, re.DOTALL)
        if match:
            try:
                return json.loads(match.group(0))
            except:
                pass

    return {"answer": text}

def call_model(prompt):
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return json.dumps({"error": str(e)})

# ------------------------
# SIMPLE ENGINE (STABLE)
# ------------------------
def run_engine(user_input):
    prompt = f"""
You are a precise reasoning engine.

Return STRICT JSON:
{{
  "answer": "...clear answer...",
  "key_points": ["...", "..."],
  "assumptions": ["..."],
  "confidence": "high | medium | low"
}}

Question:
{user_input}
"""
    raw = call_model(prompt)
    return extract_json(raw)

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
        result = run_engine(user_input)

        if "answer" in result:
            st.subheader("Answer")
            st.write(result["answer"])

            st.subheader("Key Points")
            st.write(result.get("key_points", []))

            st.subheader("Assumptions")
            st.write(result.get("assumptions", []))

            st.subheader("Confidence")
            st.write(result.get("confidence", "unknown"))
        else:
            st.write(result)

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
# CORE CALL
# ------------------------
def call_model(prompt):
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"ERROR: {str(e)}"

# ------------------------
# MULTI-PASS ENGINE
# ------------------------
def run_engine(question):
    # PASS 1 — INITIAL ANSWER
    draft_prompt = f"""
Answer the question thoroughly and rigorously.

Question:
{question}
"""
    draft = call_model(draft_prompt)

    # PASS 2 — CRITIQUE
    critique_prompt = f"""
Critically evaluate the following answer.

Identify:
- flaws
- gaps
- incorrect assumptions
- missing edge cases

Answer:
{draft}
"""
    critique = call_model(critique_prompt)

    # PASS 3 — IMPROVE
    improve_prompt = f"""
Improve the original answer using the critique.

Produce a final, corrected, higher-quality answer.

Original Answer:
{draft}

Critique:
{critique}
"""
    final = call_model(improve_prompt)

    return draft, critique, final

# ------------------------
# UI
# ------------------------
user_input = st.text_area("Enter your question")

if st.button("Run"):
    st.write("Running multi-pass reasoning...")

    if not api_key:
        st.warning("Enter API key")

    elif not model:
        st.error("Model not available")

    elif not user_input.strip():
        st.warning("Enter a question")

    else:
        draft, critique, final = run_engine(user_input)

        st.subheader("🧩 Initial Answer")
        st.write(draft)

        st.subheader("🔍 Critique")
        st.write(critique)

        st.subheader("✅ Final Improved Answer")
        st.write(final)

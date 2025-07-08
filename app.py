import streamlit as st
import fitz  # PyMuPDF for PDF parsing
import cohere

# --- CONFIGURATION ---
st.set_page_config(page_title="AI Resume Coach (Cohere)", layout="centered")
st.title("🧠 AI Resume Coach (Powered by Cohere)")

# --- COHERE API KEY ---
COHERE_API_KEY = "S3niVNb2oLTUPTmiz9HpxIggCqKe58wGesppFT24"  # Replace with your actual API key
co = cohere.Client(COHERE_API_KEY)

# --- RESUME UPLOAD ---
uploaded_file = st.file_uploader("📄 Upload your Resume (PDF only)", type=["pdf"])
resume_text = ""

if uploaded_file:
    doc = fitz.open(stream=uploaded_file.read(), filetype="pdf")
    for page in doc:
        resume_text += page.get_text()
    st.success("✅ Resume uploaded and text extracted.")

# --- JOB DESCRIPTION INPUT ---
jd_text = st.text_area("📋 Paste the Job Description", height=250)

# --- FEEDBACK GENERATION ---
if st.button("🧠 Get Resume Feedback"):
    if not resume_text.strip() or not jd_text.strip():
        st.error("Please upload a resume and paste a job description.")
    else:
        st.info("Generating feedback using Cohere's command-r model...")

        # Construct the prompt
        prompt = f"""
You are an AI resume coach. Evaluate the candidate's resume against the job description provided.
Provide feedback in the following format:

✅ Strengths:
- ...

❌ Weaknesses:
- ...

💡 Suggestions:
- ...

Focus only on relevant points based on the job requirements. Be specific and actionable.

---

JOB DESCRIPTION:
{jd_text}

---

RESUME:
{resume_text}

---
"""

        try:
            response = co.chat(
            model="command-r",
            message=prompt,
            temperature=0.3,
            )
            feedback = response.text

            st.markdown("### 📝 Resume Feedback")
            st.markdown(feedback)
        except Exception as e:
            st.error(f"Cohere API Error: {e}")
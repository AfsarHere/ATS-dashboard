import streamlit as st
import re
import docx2txt
import PyPDF2

st.set_page_config(page_title="ATS Resume Checker", layout="wide")

st.title("📊 ATS Resume Score Checker")

# --- Upload or Paste JD ---
st.subheader("Paste or Upload Job Description")
jd_input = st.text_area("Paste Job Description here:", height=200)
jd_file = st.file_uploader("Or upload JD (TXT, DOCX, PDF)", type=["txt", "docx", "pdf"])

# --- Upload Resume ---
st.subheader("Upload Resume")
resume_file = st.file_uploader("Upload Resume (DOCX, PDF, TXT)", type=["docx", "pdf", "txt"])

# --- Extract text helper ---
def extract_text(file):
    text = ""
    if file.name.endswith(".docx"):
        text = docx2txt.process(file)
    elif file.name.endswith(".pdf"):
        reader = PyPDF2.PdfReader(file)
        for page in reader.pages:
            text += page.extract_text()
    elif file.name.endswith(".txt"):
        text = file.read().decode("utf-8")
    return text

# --- Get text from JD ---
jd_text = jd_input
if jd_file is not None:
    jd_text = extract_text(jd_file)

# --- Run ATS only if JD + Resume are provided ---
if st.button("Run ATS Analysis"):
    if not jd_text or not resume_file:
        st.error("Please provide both Job Description and Resume")
    else:
        resume_text = extract_text(resume_file)

        # --- Keyword Extraction ---
        jd_keywords = set(re.findall(r"\b[a-zA-Z]+\b", jd_text.lower()))
        resume_words = set(re.findall(r"\b[a-zA-Z]+\b", resume_text.lower()))

        # Strong matches
        strong_matches = jd_keywords.intersection(resume_words)
        # Missing
        missing = jd_keywords - resume_words
        # Partial = simulate by identifying root words
        partial_matches = {w for w in jd_keywords if any(w[:5] in r for r in resume_words)} - strong_matches

        # ATS Score
        score = (len(strong_matches) / len(jd_keywords)) * 100 if jd_keywords else 0

        # --- Display Results ---
        st.metric("ATS Match Score", f"{score:.1f}%")

        st.subheader("✅ Strong Matches")
        st.write(", ".join(list(strong_matches)[:30]) if strong_matches else "None")

        st.subheader("⚠️ Partial Matches")
        st.write(", ".join(list(partial_matches)[:30]) if partial_matches else "None")

        st.subheader("❌ Missing Matches")
        st.write(", ".join(list(missing)[:30]) if missing else "None")

        st.subheader("📝 Suggestions to Improve Resume")
        st.write(f"""
        - Add missing JD keywords to your resume (see ❌ list above).  
        - Reframe achievements to include phrases like “data-driven insights”, “market trend analysis”, “mentoring junior team members”.  
        - If applicable, mention tools like **Adobe Analytics / Adobe Campaign**.  
        - Show strict adherence to **timelines and budgets**.  
        - Highlight **continuous improvement & innovation** explicitly.  
        """)

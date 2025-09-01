# app.py
import streamlit as st
import re

# Function to extract keywords (simple approach)
def extract_keywords(text):
    text = text.lower()
    # split by common delimiters and remove short words
    words = re.findall(r'\b\w{3,}\b', text)
    return set(words)

# Function to compute ATS score
def ats_score(jd_text, resume_text):
    jd_keywords = extract_keywords(jd_text)
    resume_keywords = extract_keywords(resume_text)

    matched = jd_keywords.intersection(resume_keywords)
    missing = jd_keywords.difference(resume_keywords)

    score = len(matched) / len(jd_keywords) * 100

    return round(score, 1), matched, missing

# Streamlit UI
st.set_page_config(page_title="ATS Dashboard", layout="wide")
st.title("🚀 ChatGPT-style ATS Dashboard")

st.markdown("""
This tool analyzes your **Resume** against a **Job Description (JD)** 
and provides a score with keyword match insights.
""")

jd_text = st.text_area("Paste the Job Description (JD) here:", height=200)
resume_text = st.text_area("Paste your Resume here:", height=300)

if st.button("Analyze ATS Score"):
    if not jd_text.strip() or not resume_text.strip():
        st.warning("Please provide both JD and Resume text to analyze.")
    else:
        score, matched, missing = ats_score(jd_text, resume_text)
        st.subheader(f"ATS Score: {score}%")
        st.markdown(f"**Matched Keywords ({len(matched)}):** {', '.join(list(matched)[:20])} {'...' if len(matched) > 20 else ''}")
        st.markdown(f"**Missing Keywords ({len(missing)}):** {', '.join(list(missing)[:20])} {'...' if len(missing) > 20 else ''}")
        st.success("✅ Analysis complete!")

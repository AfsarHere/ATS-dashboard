# app.py
import streamlit as st
import re

# Libraries to read files
from io import BytesIO
import PyPDF2
import docx

# Function to extract text from PDF
def extract_text_pdf(file):
    reader = PyPDF2.PdfReader(file)
    text = ""
    for page in reader.pages:
        text += page.extract_text() + "\n"
    return text

# Function to extract text from DOCX
def extract_text_docx(file):
    doc = docx.Document(file)
    text = "\n".join([para.text for para in doc.paragraphs])
    return text

# Keyword extraction
def extract_keywords(text):
    text = text.lower()
    words = re.findall(r'\b\w{3,}\b', text)
    return set(words)

# ATS score calculation
def ats_score(jd_text, resume_text):
    jd_keywords = extract_keywords(jd_text)
    resume_keywords = extract_keywords(resume_text)

    matched = jd_keywords.intersection(resume_keywords)
    missing = jd_keywords.difference(resume_keywords)

    score = len(matched) / len(jd_keywords) * 100 if jd_keywords else 0
    return round(score, 1), matched, missing

# Streamlit UI
st.set_page_config(page_title="ATS Dashboard", layout="wide")
st.title("🚀 ChatGPT-style ATS Dashboard (File Upload Version)")

st.markdown("""
Upload your **Resume** (PDF or Word) and paste the **Job Description (JD)** below to get a ChatGPT-style ATS score.
""")

# Upload Resume file
uploaded_file = st.file_uploader("Upload your Resume (PDF or DOCX)", type=["pdf", "docx"])
jd_text = st.text_area("Paste the Job Description (JD) here:", height=200)

resume_text = ""
if uploaded_file:
    if uploaded_file.type == "application/pdf":
        resume_text = extract_text_pdf(uploaded_file)
    elif uploaded_file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
        resume_text = extract_text_docx(uploaded_file)
    st.success("✅ Resume text extracted successfully!")

# ATS Analysis
if st.button("Analyze ATS Score"):
    if not jd_text.strip() or not resume_text.strip():
        st.warning("Please provide both JD and Resume to analyze.")
    else:
        score, matched, missing = ats_score(jd_text, resume_text)
        st.subheader(f"ATS Score: {score}%")
        st.markdown(f"**Matched Keywords ({len(matched)}):** {', '.join(list(matched)[:20])} {'...' if len(matched) > 20 else ''}")
        st.markdown(f"**Missing Keywords ({len(missing)}):** {', '.join(list(missing)[:20])} {'...' if len(missing) > 20 else ''}")
        st.success("✅ Analysis complete!")

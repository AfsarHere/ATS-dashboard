import streamlit as st
import pandas as pd
from PyPDF2 import PdfReader
from docx import Document

def extract_text(file):
    if file.name.endswith(".pdf"):
        reader = PdfReader(file)
        return " ".join([page.extract_text() for page in reader.pages if page.extract_text()])
    elif file.name.endswith(".docx"):
        doc = Document(file)
        return " ".join([p.text for p in doc.paragraphs])
    elif file.name.endswith(".txt"):
        return file.read().decode("utf-8")
    return ""

def calculate_score(jd_text, resume_text):
    jd_words = set(jd_text.lower().split())
    resume_words = set(resume_text.lower().split())
    matched = jd_words.intersection(resume_words)
    score = (len(matched) / len(jd_words)) * 100 if jd_words else 0
    return round(score, 2), matched

st.title("📊 ATS Score Checker")

jd_file = st.file_uploader("Upload Job Description (PDF/DOCX/TXT)", type=["pdf", "docx", "txt"])
resume_file = st.file_uploader("Upload Resume (PDF/DOCX/TXT)", type=["pdf", "docx", "txt"])

if jd_file and resume_file:
    jd_text = extract_text(jd_file)
    resume_text = extract_text(resume_file)

    score, matched_keywords = calculate_score(jd_text, resume_text)

    st.subheader(f"✅ ATS Score: {score}%")
    st.write("**Matched Keywords:**")
    st.write(", ".join(matched_keywords))
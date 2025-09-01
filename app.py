import streamlit as st
import docx
import PyPDF2

# --- Helper functions ---
def read_pdf(file):
    reader = PyPDF2.PdfReader(file)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text

def read_docx(file):
    doc = docx.Document(file)
    return "\n".join([para.text for para in doc.paragraphs])

def extract_text(file):
    if file.name.endswith(".pdf"):
        return read_pdf(file)
    elif file.name.endswith(".docx"):
        return read_docx(file)
    else:
        return str(file.read(), "utf-8")

def calculate_score(jd_text, resume_text):
    jd_words = set(jd_text.lower().split())
    resume_words = set(resume_text.lower().split())
    matched = jd_words.intersection(resume_words)
    score = (len(matched) / len(jd_words)) * 100 if jd_words else 0
    return score, matched

# --- Streamlit UI ---
st.title("ATS Resume Score Checker")

# Option 1: Paste JD
jd_input = st.text_area("Paste Job Description here", height=200)

# Option 2: Upload JD
jd_file = st.file_uploader("Or upload Job Description file", type=["pdf", "docx", "txt"])

resume_file = st.file_uploader("Upload Resume", type=["pdf", "docx", "txt"])

if (jd_input or jd_file) and resume_file:
    # If pasted JD available, prefer that
    if jd_input:
        jd_text = jd_input
    else:
        jd_text = extract_text(jd_file)

    resume_text = extract_text(resume_file)

    score, matched = calculate_score(jd_text, resume_text)

    st.subheader("📊 ATS Score")
    st.write(f"Your resume matches **{score:.2f}%** of the job description keywords.")

    st.subheader("✅ Matched Keywords")
    st.write(", ".join(matched) if matched else "No keywords matched.")

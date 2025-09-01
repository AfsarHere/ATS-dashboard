# app.py
import streamlit as st
import re
from io import BytesIO
import PyPDF2
import docx
import spacy

# Load SpaCy model
nlp = spacy.load("en_core_web_sm")

# Stopwords list
stopwords = set([
    "the","and","for","with","you","your","to","a","of","in","on","as","at","is","be",
    "by","an","or","that","this","will","are","from","our","us","we"
])

# --- File extraction ---
def extract_text_pdf(file):
    reader = PyPDF2.PdfReader(file)
    text = "".join([page.extract_text() for page in reader.pages if page.extract_text()])
    return text

def extract_text_docx(file):
    doc = docx.Document(file)
    text = "\n".join([para.text for para in doc.paragraphs])
    return text

def extract_resume(file):
    if file.type == "application/pdf":
        return extract_text_pdf(file)
    elif file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
        return extract_text_docx(file)
    else:
        return ""

# --- Text processing ---
def clean_text(text):
    text = text.lower()
    text = re.sub(r'[^a-z0-9\s]', '', text)
    words = [w for w in text.split() if w not in stopwords]
    return words

def get_ngrams(words, n=2):
    return [' '.join(words[i:i+n]) for i in range(len(words)-n+1)]

# --- Semantic matching ---
def semantic_match(jd_text, resume_text, threshold=0.75):
    jd_doc = nlp(jd_text)
    resume_doc = nlp(resume_text)
    matched = []
    for sent1 in jd_doc.sents:
        for sent2 in resume_doc.sents:
            if sent1.similarity(sent2) >= threshold:
                matched.append(sent1.text.strip())
    return matched

# --- ATS Scoring ---
def ats_score(jd_text, resume_text):
    jd_words = clean_text(jd_text)
    resume_words = clean_text(resume_text)

    # 2-word and 3-word phrases
    jd_ngrams = set(get_ngrams(jd_words, 2) + get_ngrams(jd_words, 3))
    resume_ngrams = set(get_ngrams(resume_words, 2) + get_ngrams(resume_words, 3))

    matched_keywords = jd_ngrams.intersection(resume_ngrams)
    missing_keywords = jd_ngrams.difference(resume_ngrams)

    # Semantic matching
    sem_matches = semantic_match(jd_text, resume_text)
    sem_score = len(sem_matches)/len(list(nlp(jd_text).sents)) if jd_text.strip() else 0

    # Weighted Score
    exact_match_score = len(matched_keywords)/len(jd_ngrams) if jd_ngrams else 0
    total_score = 0.7*exact_match_score + 0.3*sem_score
    total_score = round(total_score*100,1)

    return total_score, matched_keywords, missing_keywords, sem_matches

# --- Streamlit UI ---
st.set_page_config(page_title="Next-Gen ATS Dashboard", layout="wide")
st.title("🚀 Next-Gen ChatGPT-Style ATS Dashboard")

st.markdown("""
Upload your **Resume** (PDF or Word) and paste the **Job Description (JD)** to get an advanced ATS score.
""")

# Upload Resume
uploaded_file = st.file_uploader("Upload Resume (PDF/DOCX)", type=["pdf","docx"])
jd_text = st.text_area("Paste Job Description (JD) here:", height=200)

resume_text = ""
if uploaded_file:
    resume_text = extract_resume(uploaded_file)
    if resume_text:
        st.success("✅ Resume text extracted successfully!")
    else:
        st.error("❌ Could not extract text from the file.")

# Analyze Button
if st.button("Analyze ATS Score"):
    if not jd_text.strip() or not resume_text.strip():
        st.warning("Please provide both JD and Resume.")
    else:
        score, matched, missing, sem_matches = ats_score(jd_text, resume_text)
        st.subheader(f"Overall ATS Score: {score}%")
        st.markdown(f"**Exact Keyword Matches ({len(matched)}):** {', '.join(list(matched)[:20])} {'...' if len(matched) > 20 else ''}")
        st.markdown(f"**Missing Keywords ({len(missing)}):** {', '.join(list(missing)[:20])} {'...' if len(missing) > 20 else ''}")
        st.markdown(f"**Semantic Matches ({len(sem_matches)} sentences):** {', '.join([s[:60]+'...' for s in sem_matches[:5]])} {'...' if len(sem_matches) > 5 else ''}")
        st.success("✅ ATS Analysis Complete!")

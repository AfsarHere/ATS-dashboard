import streamlit as st
import re
import PyPDF2
import docx
import spacy
from nltk.corpus import stopwords, wordnet

# Load Spacy model (semantic similarity)
nlp = spacy.load("en_core_web_sm")
stop_words = set(stopwords.words("english"))

# --- Helper: Extract text from different formats ---
def extract_text(file):
    text = ""
    if file.name.endswith(".docx"):
        doc = docx.Document(file)
        text = "\n".join([para.text for para in doc.paragraphs])
    elif file.name.endswith(".pdf"):
        reader = PyPDF2.PdfReader(file)
        for page in reader.pages:
            text += page.extract_text() or ""
    elif file.name.endswith(".txt"):
        text = file.read().decode("utf-8")
    return text

# --- Preprocess text (cleaning, stopword removal) ---
def preprocess(text):
    text = text.lower()
    text = re.sub(r'[^a-z\s]', '', text)
    words = [w for w in text.split() if w not in stop_words]
    return words

# --- Semantic Match Helper ---
def semantic_match(word, resume_words):
    if word in resume_words:
        return True
    for syn in wordnet.synsets(word):
        for lemma in syn.lemmas():
            if lemma.name() in resume_words:
                return True
    return False

# --- Weighted Score Calculator ---
HIGH_WEIGHT = ["marketing strategy", "campaign management", "digital marketing", "adobe", "analytics", "lead generation"]
MEDIUM_WEIGHT = ["cross-functional", "leadership", "collaboration", "consumer insights", "brand awareness"]
LOW_WEIGHT = ["team", "dynamic", "fast-paced", "communication", "growth"]

def calculate_score(jd_text, resume_text):
    jd_words = preprocess(jd_text)
    resume_words = preprocess(resume_text)

    score = 0
    total_weight = 0

    for word in jd_words:
        if word in HIGH_WEIGHT:
            weight = 3
        elif word in MEDIUM_WEIGHT:
            weight = 2
        elif word in LOW_WEIGHT:
            weight = 1
        else:
            weight = 1  # default

        total_weight += weight
        if semantic_match(word, resume_words):
            score += weight

    return round((score / total_weight) * 100, 1)

# --- Streamlit UI ---
st.set_page_config(page_title="📊 ATS Resume Score Checker", layout="centered")

st.title("📊 ATS Resume Score Checker")

# Job Description Input
jd_input = st.text_area("Paste Job Description here:", height=250)
jd_file = st.file_uploader("Or upload JD (TXT, DOCX, PDF)", type=["txt", "docx", "pdf"])

# Resume Input
resume_file = st.file_uploader("Upload Resume (DOCX, PDF, TXT)", type=["docx", "pdf", "txt"])

if st.button("Check ATS Score"):
    if (jd_input or jd_file) and resume_file:
        jd_text = jd_input if jd_input else extract_text(jd_file)
        resume_text = extract_text(resume_file)

        score = calculate_score(jd_text, resume_text)

        st.subheader("📈 ATS Match Score")
        st.progress(score / 100)
        st.metric(label="JD–Resume Match", value=f"{score}%")

        # Suggestions
        st.subheader("📝 Suggestions to Improve Resume")
        if score < 60:
            st.write("- Add missing JD keywords and phrases explicitly into your resume.")
            st.write("- Mention tools like Adobe Analytics / Adobe Campaign if relevant.")
            st.write("- Highlight experience with timelines, budgets, and team mentoring.")
            st.write("- Use phrasing like 'data-driven insights', 'market trend analysis'.")
        elif score < 80:
            st.write("- Good match! Improve by adding more JD-specific terms.")
        else:
            st.write("- Excellent! Your resume is highly aligned with the JD.")
    else:
        st.warning("⚠️ Please provide both a Job Description and a Resume.")

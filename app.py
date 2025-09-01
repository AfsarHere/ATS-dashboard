import re
from collections import Counter
import streamlit as st

STOPWORDS = {
    "a","an","the","and","or","for","to","of","in","on","at","by","with","from","as","is","are","was","were",
    "be","been","being","this","that","these","those","it","its","into","over","under","after","before","during",
    "via","about","your","you","we","our","their","they","them","he","she","his","her","him","i","me","my","mine"
}

def tokenize(text: str):
    tokens = re.findall(r"\b[a-z0-9]+\b", text.lower())
    return [t for t in tokens if t not in STOPWORDS and len(t) > 2]

st.title("ATS Resume Scorer")
st.write("Paste your resume and a job description below. The tool calculates ATS match score and gives suggestions.")

resume_text = st.text_area("Resume Text:", height=250)
job_text = st.text_area("Job Description Text:", height=250)

if st.button("Calculate ATS Score"):
    if not resume_text.strip() or not job_text.strip():
        st.warning("Please enter both resume and job description text.")
    else:
        resume_tokens = tokenize(resume_text)
        job_tokens = tokenize(job_text)

        resume_counter = Counter(resume_tokens)
        job_set = set(job_tokens)

        matches = sorted([kw for kw in job_set if kw in resume_counter])
        missing = sorted([kw for kw in job_set if kw not in resume_counter])

        ats_score = (len(matches) / len(job_set) * 100) if job_set else 0.0

        suggestions = []
        if ats_score < 50:
            suggestions.append("Your resume is missing many key skills. Add relevant keywords from the job description.")
        elif ats_score < 80:
            suggestions.append("Your resume is moderately aligned. Emphasize missing high-priority skills.")
        else:
            suggestions.append("Great alignment! Your resume matches most of the job keywords.")

        st.subheader("ATS Score")
        st.metric(label="Match Score (%)", value=f"{ats_score:.1f}%")

        st.subheader("Matched Keywords")
        st.write(", ".join(matches) if matches else "No matches found")

        st.subheader("Missing Keywords")
        st.write(", ".join(missing) if missing else "None, perfect match!")

        st.subheader("Suggestions")
        for s in suggestions:
            st.write(f"- {s}")

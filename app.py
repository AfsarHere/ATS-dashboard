import streamlit as st
import spacy
from spacy.cli import download
from collections import Counter

# Download and load spaCy model
download("en_core_web_sm")
nlp = spacy.load("en_core_web_sm")

st.title("ATS Resume Scorer")
st.write("Paste your resume and job description below. The tool will calculate your ATS match score and provide suggestions.")

resume_text = st.text_area("Resume Text:", height=250)
job_text = st.text_area("Job Description Text:", height=250)

if st.button("Calculate ATS Score"):
    if not resume_text.strip() or not job_text.strip():
        st.warning("Please enter both resume and job description text.")
    else:
        # NLP processing
        resume_doc = nlp(resume_text.lower())
        job_doc = nlp(job_text.lower())
        
        # Extract keywords (nouns, proper nouns, verbs)
        resume_keywords = [token.lemma_ for token in resume_doc if token.pos_ in ["NOUN", "PROPN", "VERB"]]
        job_keywords = [token.lemma_ for token in job_doc if token.pos_ in ["NOUN", "PROPN", "VERB"]]
        
        # Count matches and missing
        resume_counter = Counter(resume_keywords)
        matches = [kw for kw in set(job_keywords) if kw in resume_counter]
        missing = [kw for kw in set(job_keywords) if kw not in resume_counter]
        
        # ATS Score
        ats_score = len(matches) / len(set(job_keywords)) * 100 if len(set(job_keywords)) > 0 else 0
        
        # Suggestions
        suggestions = []
        if ats_score < 50:
            suggestions.append("Your resume is missing many key skills. Add relevant keywords from the job description.")
        if ats_score >= 50 and ats_score < 80:
            suggestions.append("Your resume is moderately aligned. Consider emphasizing missing high-priority skills.")
        if ats_score >= 80:
            suggestions.append("Great alignment! Your resume matches most of the job keywords.")
        
        # Display results
        st.subheader("ATS Score")
        st.metric(label="Match Score (%)", value=f"{ats_score:.1f}%")
        
        st.subheader("Matched Keywords")
        st.write(", ".join(matches) if matches else "No matches found")
        
        st.subheader("Missing Keywords")
        st.write(", ".join(missing) if missing else "None, perfect match!")
        
        st.subheader("Suggestions")
        for s in suggestions:
            st.write(f"- {s}")

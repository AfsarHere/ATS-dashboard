import streamlit as st
import spacy
from spacy.cli import download

# Download the English model if not already installed
download("en_core_web_sm")

# Load the spaCy model
nlp = spacy.load("en_core_web_sm")

st.title("ATS Dashboard")

st.write("Enter some text below to analyze with spaCy:")

user_input = st.text_area("Your text here:", "Type something...")

if st.button("Analyze"):
    if user_input.strip() == "":
        st.warning("Please enter some text first!")
    else:
        doc = nlp(user_input)
        
        st.subheader("Tokens and Part-of-Speech")
        token_data = [(token.text, token.pos_, token.dep_) for token in doc]
        st.table(token_data)
        
        st.subheader("Named Entities (color-coded)")
        import re
        # Highlight entities with colors
        colors = {"ORG": "lightblue", "GPE": "lightgreen", "PERSON": "lightpink", "DATE": "lightyellow"}
        html_text = user_input
        for ent in doc.ents:
            color = colors.get(ent.label_, "lightgray")
            html_text = re.sub(r"\b" + re.escape(ent.text) + r"\b", f"<mark style='background-color:{color}'>{ent.text}</mark>", html_text)
        st.markdown(html_text, unsafe_allow_html=True)

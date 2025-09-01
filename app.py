import streamlit as st
import spacy
from spacy.cli import download

# -----------------------
# Ensure spaCy model is installed
# -----------------------
download("en_core_web_sm")  # downloads if not already installed
nlp = spacy.load("en_core_web_sm")  # load the model

# -----------------------
# Streamlit app layout
# -----------------------
st.title("ATS Dashboard")

st.write("Enter some text below to analyze with spaCy:")

# Text input
user_input = st.text_area("Your text here:", "Type something...")

if st.button("Analyze"):
    if user_input.strip() == "":
        st.warning("Please enter some text first!")
    else:
        doc = nlp(user_input)
        
        # Show tokens with part-of-speech
        st.subheader("Tokens and Part-of-Speech")
        token_data = [(token.text, token.pos_, token.dep_) for token in doc]
        st.table(token_data)
        
        # Show named entities
        st.subheader("Named Entities")
        entity_data = [(ent.text, ent.label_) for ent in doc.ents]
        if entity_data:
            st.table(entity_data)
        else:
            st.info("No named entities found in the text.")

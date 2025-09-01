import streamlit as st
import spacy

# Load the model (assumes installed via requirements.txt)
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
        
        st.subheader("Named Entities")
        entity_data = [(ent.text, ent.label_) for ent in doc.ents]
        if entity_data:
            st.table(entity_data)
        else:
            st.info("No named entities found in the text.")

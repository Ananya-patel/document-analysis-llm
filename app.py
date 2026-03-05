import streamlit as st
import PyPDF2
import os
import json
from groq import Groq
from dotenv import load_dotenv
from collections import Counter

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))


# ---- Helper functions ----

def extract_text_from_pdf(pdf_file):
    text = ""
    reader = PyPDF2.PdfReader(pdf_file)
    for page_num, page in enumerate(reader.pages):
        text += f"\n--- Page {page_num + 1} ---\n"
        text += page.extract_text()
    return text


def summarize(text):
    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {
                "role": "system",
                "content": "You are a helpful assistant that summarizes documents clearly."
            },
            {
                "role": "user",
                "content": f"Summarize this document in 5 bullet points:\n\n{text[:15000]}"
            }
        ]
    )
    return response.choices[0].message.content


def extract_fields(text):
    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {
                "role": "system",
                "content": "You are a structured data extractor. Return ONLY valid JSON. No markdown, no explanation."
            },
            {
                "role": "user",
                "content": f"""Extract these fields and return as JSON.
Use EXACTLY these key names:

{{
    "main_topic": "what is this document about",
    "key_entities": ["person/place/org1", "person/place/org2"],
    "main_themes": ["theme1", "theme2"],
    "time_period": "time period covered if mentioned",
    "document_type": "article/report/paper/other"
}}

Document:
{text[:15000]}"""
            }
        ]
    )
    raw = response.choices[0].message.content.strip()
    if raw.startswith("```"):
        raw = raw.split("```")[1]
        if raw.startswith("json"):
            raw = raw[4:]
    return json.loads(raw)


def classify_chunks(text):
    chunks = [text[i:i+1000] for i in range(0, min(len(text), 10000), 1000)]
    categories = []
    for chunk in chunks:
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {
                    "role": "system",
                    "content": """Classify text into ONE category:
History, Language, Religion, Arts, Sports, Food, Popular Culture, Science, Other
Reply with ONLY the category name."""
                },
                {
                    "role": "user",
                    "content": f"Classify:\n\n{chunk}"
                }
            ]
        )
        categories.append(response.choices[0].message.content.strip())
    return Counter(categories)


# ---- Streamlit UI ----

st.set_page_config(page_title="Document Analysis", page_icon="📄")

st.title(" Document Analysis Using LLMs")
st.caption("Project 1 of your RAG journey — upload any PDF and analyze it")

uploaded_file = st.file_uploader("Upload a PDF", type="pdf")

if uploaded_file:
    with st.spinner("Extracting text from PDF..."):
        text = extract_text_from_pdf(uploaded_file)

    st.success(f" Extracted {len(text):,} characters from {uploaded_file.name}")

    col1, col2, col3 = st.columns(3)
    
    with col1:
        run_summary = st.button(" Summarize")
    with col2:
        run_extract = st.button(" Extract Fields")
    with col3:
        run_classify = st.button(" Classify")

    if run_summary:
        with st.spinner("Summarizing..."):
            result = summarize(text)
        st.subheader("Summary")
        st.write(result)

    if run_extract:
        with st.spinner("Extracting structured fields..."):
            result = extract_fields(text)
        st.subheader("Extracted Fields")
        st.json(result)

    if run_classify:
        with st.spinner("Classifying document sections..."):
            result = classify_chunks(text)
        st.subheader("Content Distribution")
        for category, count in result.most_common():
            st.progress(
                count / sum(result.values()),
                text=f"{category}: {count} chunks"
            )

st.divider()
st.caption("Built with Groq + LLaMA 3.1 | Part of RAG Mastery Journey")
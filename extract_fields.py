import PyPDF2
import os
import json
from groq import Groq
from dotenv import load_dotenv

load_dotenv()


def extract_text_from_pdf(pdf_path):
    text = ""
    with open(pdf_path, "rb") as file:
        reader = PyPDF2.PdfReader(file)
        for page_num, page in enumerate(reader.pages):
            text += f"\n--- Page {page_num + 1} ---\n"
            text += page.extract_text()
    return text


def extract_structured_fields(text):
    client = Groq(api_key=os.getenv("GROQ_API_KEY"))

    text_chunk = text[:15000]

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {
                "role": "system",
                "content": """You are a structured data extractor. 
Extract information from documents and return ONLY valid JSON.
No explanation, no markdown, no extra text. Just raw JSON."""
            },
            {
                "role": "user",
                "content": f"""Extract the following fields from this document and return as JSON:

{{
    "country": "Japan",
    "primary_religions": ["Religion1", "Religion2"],
    "primary_language": "language name",
    "writing_scripts": ["script1", "script2"],
    "cultural_influences": ["country1", "country2"],
    "traditional_clothing": "garment name",
    "key_art_forms": ["art1", "art2"],
    "global_rank_cultural_influence": "4th"
}}


Document:
{text_chunk}"""
            }
        ]
    )

    raw = response.choices[0].message.content
    
    # Clean and parse JSON
    raw = raw.strip()
    if raw.startswith("```"):
        raw = raw.split("```")[1]
        if raw.startswith("json"):
            raw = raw[4:]
    
    return json.loads(raw)


if __name__ == "__main__":
    print("Extracting text from PDF...")
    extracted = extract_text_from_pdf("document.pdf")

    print("Sending to Groq for structured extraction...\n")
    fields = extract_structured_fields(extracted)

    print("=== EXTRACTED FIELDS ===")
    print(json.dumps(fields, indent=2))
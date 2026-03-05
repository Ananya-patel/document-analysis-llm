import PyPDF2
import os
from groq import Groq
from dotenv import load_dotenv
from httpx._transports import base

load_dotenv()

# ---- Extract text (reusing what we learned) ----
def extract_text_from_pdf(pdf_path):
    text = ""
    with open(pdf_path, "rb") as file:
        reader = PyPDF2.PdfReader(file)
        for page_num, page in enumerate(reader.pages):
            page_text = page.extract_text()
            text += f"\n--- Page {page_num + 1} ---\n"
            text += page_text
    return text


# ---- Send to Groq ----
def summarize_text(text):
    client = Groq(api_key=os.getenv("GROQ_API_KEY"))
    
    # We can only send a portion - this is the context window problem in action
    text_chunk = text[:20000]
    
    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {
                "role": "system",
                "content": "You are a helpful assistant that summarizes documents clearly and concisely."
            },
            {
                "role": "user",
                "content": f"Summarize this document in 5 bullet points:\n\n{text_chunk}"
            }
        ]
    )
    
    return response.choices[0].message.content


if __name__ == "__main__":
    print("Extracting text...")
    extracted = extract_text_from_pdf("document.pdf")
    print(f"Total characters: {len(extracted)}")
    
    print("\nSending to Groq...\n")
    summary = summarize_text(extracted)
    
    print("=== SUMMARY ===")
    print(summary)
import PyPDF2
import os
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


def split_into_chunks(text, chunk_size=1000):
    """Split text into chunks of roughly chunk_size characters"""
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end]
        chunks.append(chunk)
        start = end
    return chunks


def classify_chunk(client, chunk, chunk_num):
    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {
                "role": "system",
                "content": """You are a document classifier.
Classify the given text into EXACTLY ONE of these categories:
- History
- Language
- Religion  
- Arts
- Sports
- Food
- Popular Culture
- Other

Reply with ONLY the category name. Nothing else."""
            },
            {
                "role": "user",
                "content": f"Classify this text:\n\n{chunk}"
            }
        ]
    )
    return response.choices[0].message.content.strip()


if __name__ == "__main__":
    print("Extracting text...")
    extracted = extract_text_from_pdf("document.pdf")

    print("Splitting into chunks...")
    chunks = split_into_chunks(extracted, chunk_size=1000)
    print(f"Total chunks: {len(chunks)}")

    client = Groq(api_key=os.getenv("GROQ_API_KEY"))

    print("\nClassifying each chunk...\n")
    
    results = {}
    
    for i, chunk in enumerate(chunks[:10]):  # First 10 chunks only
        category = classify_chunk(client, chunk, i)
        results[f"Chunk {i+1}"] = category
        print(f"Chunk {i+1}: {category}")

    print("\n=== CLASSIFICATION SUMMARY ===")
    
    # Count categories
    from collections import Counter
    counts = Counter(results.values())
    for category, count in counts.most_common():
        print(f"{category}: {count} chunks")
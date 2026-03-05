import PyPDF2
import os

def extract_text_from_pdf(pdf_path):
    text = ""
    
    with open(pdf_path, "rb") as file:
        reader = PyPDF2.PdfReader(file)
        
        print(f"Total pages: {len(reader.pages)}")
        
        for page_num, page in enumerate(reader.pages):
            page_text = page.extract_text()
            text += f"\n--- Page {page_num + 1} ---\n"
            text += page_text
    
    return text


if __name__ == "__main__":
    extracted = extract_text_from_pdf("document.pdf")
    print(extracted[:3000])
    print(f"\n\nTotal characters extracted: {len(extracted)}")
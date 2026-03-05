# 📄 Document Analysis Using LLMs

> Project 1 of my RAG Mastery Journey — building toward full RAG systems from scratch.

A Streamlit app that lets you upload any PDF and analyze it using LLMs (Groq + LLaMA 3.1).
Three analysis modes: summarization, structured field extraction, and content classification.

---

##  What This Project Taught Me

- How LLMs process raw text from PDFs
- Why context windows are a real limitation (63,607 chars vs ~15,000 limit)
- Prompt engineering: why examples beat descriptions
- LLM as summarizer, structured parser, and classifier
- Why this limitation is exactly what RAG solves → Project 2

---

##  Features

| Feature | Description |
|---|---|
| 📝 Summarize | Generates 5 bullet point summary of any PDF |
| 🔍 Extract Fields | Pulls structured JSON fields from unstructured text |
| 🏷️ Classify | Labels document sections by topic category |

---

## 🛠️ Tech Stack

- **LLM:** LLaMA 3.1 8B via Groq API
- **PDF Processing:** PyPDF2
- **UI:** Streamlit
- **Language:** Python 3.11

---

## ⚙️ Setup & Run Locally

**1. Clone the repo**
```bash
git clone https://github.com/YOUR_USERNAME/document-analysis-llm.git
cd document-analysis-llm
```

**2. Create virtual environment**
```bash
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # Mac/Linux
```

**3. Install dependencies**
```bash
pip install -r requirements.txt
```

**4. Set up environment variables**

Create a `.env` file in the root folder:
```
GROQ_API_KEY=your-groq-api-key-here
```

Get a free Groq API key at [console.groq.com](https://console.groq.com)

**5. Run the app**
```bash
streamlit run app.py
```

Open `http://localhost:8501` in your browser.

---

## 📁 Project Structure
```
project1/
├── app.py              # Main Streamlit application
├── extract.py          # PDF text extraction
├── summarize.py        # LLM summarization
├── extract_fields.py   # Structured JSON extraction
├── classify.py         # Document classification
├── requirements.txt    # Dependencies
├── .env               # API keys (never committed)
└── README.md          # This file
```

---

## 🧠 Key Learning: The Context Window Problem

This project exists to make one thing viscerally clear:
```
Document size:     63,607 characters
LLM context limit: ~15,000 characters  
Ratio:             4x too large
```

You cannot just dump a large document into an LLM. This is why RAG exists.
**Project 2** solves this properly with chunking, embeddings, and vector search.

---

## 🗺️ Part of RAG Mastery Journey

| Project | Topic | Status |
|---|---|---|
| **Project 1** | Document Analysis Using LLMs | ✅ Complete |
| Project 2 | RAG System From Scratch | 🔄 Next |
| Project 3 | Multi-Document RAG | ⬜ Upcoming |

---

LIVE KEY 

https://document-analysis-llm.streamlit.app/
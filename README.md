# 🚀 NASA Knowledge Assistant

An AI-powered RAG (Retrieval-Augmented Generation) chatbot that answers questions about NASA missions, programs, scientific research, and general space exploration.
This project uses Python, Flask, FAISS, Sentence Transformers, and Google Gemini to create a fast and accurate knowledge assistant with a NASA-themed frontend UI.

---

## 📌 Overview

This project demonstrates how to build a complete AI assistant capable of:

* Answering detailed questions about NASA using retrieved PDF knowledge

* Extracting text from multiple NASA PDFs

* Converting documents into embeddings

* Storing them in a FAISS vector index

* Fetching relevant context for each query

* Producing high-quality answers with Google Gemini

* Displaying replies with a smooth typewriter animation

* Running on a clean NASA-styled web UI

---

## 🛰️ Features
### Backend

✔ Multi-PDF ingestion

✔ Automatic text chunking

✔ Vector embedding generation

✔ FAISS similarity search

✔ RAG-powered answer generation

✔ Smart system prompt

✔ Automatic index build on startup (no manual button)

### Frontend

✔ NASA-themed UI

✔ Glass-background container

✔ Watermarked chat panel

✔ Blue NASA color palette

✔ Typewriter effect for bot responses

✔ Mobile-friendly layout

✔ Floating “Visit NASA” link button

✔ Clean user & bot chat bubbles

---

## 🧠 Tech Stack
### Backend

* Python 3.10+

* Flask – lightweight web server

* Google Gemini (google-genai) – LLM for answer generation

* Sentence Transformers – text embeddings

* FAISS – fast vector similarity search

* pdfplumber – PDF text extraction

* dotenv – environment variables

### Frontend

* HTML + CSS + Vanilla JavaScript

* Typewriter effect

* NASA custom theme

* Responsive design

---

## 📂 Project Structure
```bash
nasa/
│
├── app.py
├── config.py
├── utils/
│   ├── ingest.py
│   ├── embed.py
│   ├── retrieve.py
│   └── chat.py
│
├── data/
│   ├── nasa_doc1.pdf
│   ├── nasa_doc2.pdf
│   ├── nasa_doc3.pdf
│   └── nasa.txt     # contains NASA general info
│
├── vectorstore/
│   ├── index.faiss
│   └── meta.pkl
│
├── static/
│   ├── bg.jpg
│   └── logo.png
│
├── templates/
│   └── index.html
│
└── .env
```

---

## 🔧 How It Works (RAG Pipeline)
### 1. PDF Ingestion
```
utils/ingest.py
```
* Reads all NASA PDFs from /data

* Cleans text

* Splits into overlapping chunks (default: 800 chars, overlap 200)

* Returns a list of text chunks

### 2. Embedding Generation
```
utils/embed.py
```
* Converts chunks → embedding vectors using all-MiniLM-L6-v2

* Builds & saves a FAISS vector index

* Stores metadata for each chunk

### 3. Query Processing
```
utils/retrieve.py
```
* Converts the user question into an embedding

* Searches FAISS for relevant NASA content

* Returns matching chunks

### 4. Answer Generation
```
utils/chat.py
```
* Builds a system prompt for a “NASA Knowledge Assistant”

* Feeds context + question to Gemini

* Returns the generated answer

### 5. Frontend Display

* User enters a question

* AJAX /chat POST call is made

* Response is typed letter-by-letter using a typewriter animation

* Chat history grows inside the NASA-styled UI

---

## ⚙️ Setup & Installation
### 1. Clone the Repository
```bash
git clone https://github.com/your-username/nasa-knowledge-assistant.git
cd nasa-knowledge-assistant
```
### 2. Create a Virtual Environment
```python
python -m venv venv
source venv/bin/activate    # macOS / Linux
venv\Scripts\activate       # Windows
```
### 3. Install Dependencies
```python
pip install -r requirements.txt
```
### 4. Add Your .env File
```
Create .env:

GEMINI_API_KEY=your_key_here
PDF_PATH=data/*.pdf
```
### 5. Run the App
```bash
python app.py
```

Access at:

### http://127.0.0.1:5000

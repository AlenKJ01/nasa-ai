# utils/ingest.py
import pdfplumber
import os
import re
from config import PDF_PATH, CHUNK_SIZE, OVERLAP

def clean_text(s: str) -> str:
    s = re.sub(r"\s+", " ", s)
    return s.strip()

def pdf_to_text(pdf_path: str) -> str:
    text_parts = []
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            txt = page.extract_text() or ""
            text_parts.append(txt)
    full = "\n\n".join(text_parts)
    return clean_text(full)

def chunk_text(text: str, chunk_size: int = CHUNK_SIZE, overlap: int = OVERLAP):
    chunks = []
    start = 0
    L = len(text)
    while start < L:
        end = min(start + chunk_size, L)
        chunk = text[start:end]
        chunks.append(chunk)
        start = end - overlap if end < L else end
    return chunks

def ingest(data_dir: str = None):
    """
    Ingest all PDFs found under the `data` folder (or PDF_PATH if specified).
    Also appends data/my_profile.txt when present.
    Returns list of dicts: {id, text}
    """
    # determine folder to scan
    if data_dir:
        base = data_dir
    else:
        # attempt to use PDF_PATH env/fallback; if it's a single file, use its parent folder
        if os.path.isdir(PDF_PATH):
            base = PDF_PATH
        else:
            base = os.path.dirname(PDF_PATH) or "data"

    base = os.path.abspath(base)
    print(f"[ingest] scanning folder: {base}")

    # gather all pdf files
    pdf_files = []
    for fname in os.listdir(base):
        if fname.lower().endswith(".pdf"):
            pdf_files.append(os.path.join(base, fname))

    if not pdf_files:
        print("[ingest] WARNING: no PDF files found in", base)

    combined_texts = []
    for p in pdf_files:
        try:
            print("[ingest] reading:", p)
            txt = pdf_to_text(p)
            combined_texts.append(f"--- SOURCE: {os.path.basename(p)} ---\n\n{txt}")
        except Exception as e:
            print(f"[ingest] failed to read {p}: {e}")

    # load candidate profile if present
    profile_path = os.path.join(base, "my_profile.txt")
    profile_text = ""
    if os.path.exists(profile_path):
        print("[ingest] loading profile:", profile_path)
        with open(profile_path, "r", encoding="utf-8") as f:
            profile_text = f.read().strip()
        combined_texts.append("--- SOURCE: CANDIDATE_PROFILE ---\n\n" + profile_text)
    else:
        print("[ingest] no profile file found at", profile_path)

    full_text = "\n\n".join(combined_texts)
    full_text = clean_text(full_text)
    print(f"[ingest] total text length: {len(full_text)} characters")

    chunks = chunk_text(full_text)
    print(f"[ingest] created {len(chunks)} chunks from PDFs + profile")

    return [{"id": f"chunk_{i}", "text": c} for i, c in enumerate(chunks)]

if __name__ == "__main__":
    docs = ingest()
    print("Sample chunk:", docs[0]["text"][:300] if docs else "no chunks")

import os
import json
import fitz  # PyMuPDF
from pathlib import Path
from uuid import uuid4
import re

PDF_DIR = Path("data/pdfs")
CHUNK_DIR = Path("data/text_chunks")

def clean_text(text):
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

def chunk_text(text, max_tokens=500):
    sentences = re.split(r'(?<=[.?!])\s+', text)
    chunks = []
    current_chunk = ""
    for sentence in sentences:
        if len(current_chunk) + len(sentence) <= max_tokens:
            current_chunk += sentence + " "
        else:
            chunks.append(current_chunk.strip())
            current_chunk = sentence + " "
    if current_chunk:
        chunks.append(current_chunk.strip())
    return chunks

def parse_pdf_to_chunks(pdf_path):
    doc = fitz.open(pdf_path)
    full_text = ""
    for page in doc:
        full_text += page.get_text()
    full_text = clean_text(full_text)
    return chunk_text(full_text)

def save_chunks_to_json(source_filename, chunks):
    CHUNK_DIR.mkdir(parents=True, exist_ok=True)
    out_path = CHUNK_DIR / f"{Path(source_filename).stem}_chunks.json"
    data = [{
        "id": str(uuid4()),
        "source": source_filename,
        "text": chunk
    } for chunk in chunks]
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

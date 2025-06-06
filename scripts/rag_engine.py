import os
import json
import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from pathlib import Path

CHUNK_DIR = Path("data/text_chunks")
model = SentenceTransformer('all-MiniLM-L6-v2')

def load_chunks():
    texts = []
    metadata = []
    for file in CHUNK_DIR.glob("*.json"):
        with open(file, "r", encoding="utf-8") as f:
            data = json.load(f)
            for entry in data:
                texts.append(entry["text"])
                metadata.append(entry)
    return texts, metadata

def get_relevant_chunks(query, top_k=5):
    texts, metadata = load_chunks()
    if not texts:
        return []
    query_vec = model.encode([query])
    text_vecs = model.encode(texts)
    sims = cosine_similarity(query_vec, text_vecs)[0]
    top_indices = np.argsort(sims)[-top_k:][::-1]
    return [metadata[i] for i in top_indices]

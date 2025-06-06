import json
from pathlib import Path
from uuid import uuid4
from datetime import datetime
from keybert import KeyBERT
import re
from collections import Counter
from sklearn.feature_extraction.text import ENGLISH_STOP_WORDS

# KeyBERT model will be loaded lazily to avoid import-time overhead.
_kw_model = None


def extract_topic(text: str) -> str:
    """Return the top keyword as a simple topic label."""
    global _kw_model
    if _kw_model is None:
        try:
            _kw_model = KeyBERT("all-MiniLM-L6-v2")
        except Exception:
            _kw_model = False
    if _kw_model:
        try:
            keywords = _kw_model.extract_keywords(text, stop_words="english", top_n=1)
            if keywords:
                return keywords[0][0]
        except Exception:
            pass

    # Fallback keyword extraction using term frequency
    words = re.findall(r"\b[a-zA-Z]{3,}\b", text.lower())
    words = [w for w in words if w not in ENGLISH_STOP_WORDS]
    if not words:
        return ""
    return Counter(words).most_common(1)[0][0]

MEMORY_FILE = Path("data/memory/memory.json")


def load_log():
    if MEMORY_FILE.exists():
        with open(MEMORY_FILE, "r", encoding="utf-8") as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return []
    return []


def add_entry(question, answer, summary, impact_score=5):
    topic_text = f"{question} {summary} {answer}"
    topic = extract_topic(topic_text)

    entry = {
        "id": str(uuid4()),
        "timestamp": datetime.utcnow().isoformat(),
        "question": question,
        "answer": answer,
        "summary": summary,
        "impact_score": impact_score,
        "topic": topic,
    }
    log = load_log()
    log.append(entry)
    MEMORY_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(MEMORY_FILE, "w", encoding="utf-8") as f:
        json.dump(log, f, indent=2, ensure_ascii=False)

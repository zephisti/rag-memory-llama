import json
from pathlib import Path
from uuid import uuid4
from datetime import datetime

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
    entry = {
        "id": str(uuid4()),
        "timestamp": datetime.utcnow().isoformat(),
        "question": question,
        "answer": answer,
        "summary": summary,
        "impact_score": impact_score,
    }
    log = load_log()
    log.append(entry)
    MEMORY_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(MEMORY_FILE, "w", encoding="utf-8") as f:
        json.dump(log, f, indent=2, ensure_ascii=False)

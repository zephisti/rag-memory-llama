import json
from pathlib import Path
from uuid import uuid4

MEMORY_LOG = Path("data/memory/memory.json")
CHUNK_DIR = Path("data/text_chunks")
OUTPUT_FILE = CHUNK_DIR / "memory_chunks.json"

def load_memory_entries():
    if not MEMORY_LOG.exists():
        print("⚠️ No memory log found.")
        return []
    with open(MEMORY_LOG, "r", encoding="utf-8") as f:
        return json.load(f)

def create_chunks_from_memory(entries):
    chunks = []
    for entry in entries:
        if isinstance(entry, str):
            try:
                entry = json.loads(entry)
            except Exception as e:
                print(f"❌ Skipping invalid entry: {e}")
                continue
        context = f"Q: {entry['question']}\nA: {entry['answer']}"
        chunk = {
            "id": str(uuid4()),
            "source": "memory_log",
            "text": context,
            "summary": entry.get("summary", ""),
            "impact_score": entry.get("impact_score", 5)
        }
        chunks.append(chunk)
    return chunks

def save_chunks(chunks):
    CHUNK_DIR.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(chunks, f, indent=2, ensure_ascii=False)
    print(f"✅ Saved {len(chunks)} memory chunks to {OUTPUT_FILE}")

def main():
    entries = load_memory_entries()
    chunks = create_chunks_from_memory(entries)
    save_chunks(chunks)

if __name__ == "__main__":
    main()

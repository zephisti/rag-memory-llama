import sys
import re
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent / "scripts"))

from rag_engine import get_relevant_chunks
from ollama_interface import query_llama
from memory_manager import add_entry


def main():
    question = input("Ask a question: ").strip()
    if not question:
        print("No question entered.")
        return

    chunks = get_relevant_chunks(question)
    context = "\n\n".join([c["text"] for c in chunks])
    if context:
        print("\nRetrieved top relevant chunks...\n")
    response = query_llama(question, system_context=context)
    print(f"Response:\n{response}\n")

    summary_prompt = f"Summarize this answer in 1 sentence:\n{response}"
    summary = query_llama(summary_prompt)
    print(f"Summary: {summary}")

    score_prompt = (
        f"Rate the importance of this answer on a scale from 1 to 10:\n{response}"
    )
    score_str = query_llama(score_prompt)
    match = re.search(r"\b([1-9]|10)\b", score_str)
    try:
        impact_score = int(match.group(1)) if match else 5
    except Exception:
        impact_score = 5

    print(f"Impact Score: {impact_score}")

    add_entry(question, response, summary, impact_score)
    print("Memory log updated.")


if __name__ == "__main__":
    main()

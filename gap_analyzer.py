import json
import re
from collections import defaultdict, Counter
from datetime import datetime, timedelta
from pathlib import Path
import argparse
from sklearn.feature_extraction.text import ENGLISH_STOP_WORDS

MEMORY_FILE = Path("data/memory/memory.json")

OPEN_PROMPT_WORDS = re.compile(r"\b(what|how|why|should)\b", re.IGNORECASE)


def load_entries(path: Path):
    if not path.exists():
        return []
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError:
        return []


def extract_topic(text: str) -> str:
    words = re.findall(r"\b[a-zA-Z]{3,}\b", text.lower())
    words = [w for w in words if w not in ENGLISH_STOP_WORDS]
    if not words:
        return "misc"
    return Counter(words).most_common(1)[0][0]


def group_by_topic(entries):
    groups = defaultdict(list)
    for e in entries:
        topic = e.get("topic")
        if not topic:
            text = f"{e.get('question', '')} {e.get('summary', '')} {e.get('answer', '')}"
            topic = extract_topic(text)
        groups[topic].append(e)
    return groups


def analyze_groups(groups):
    now = datetime.utcnow()
    gap_info = {}
    for topic, items in groups.items():
        total = len(items)
        high_impact = [e for e in items if e.get("impact_score", 0) > 7]
        open_questions = [e["question"] for e in items if OPEN_PROMPT_WORDS.search(e.get("question", ""))]
        latest_ts = max(datetime.fromisoformat(e["timestamp"]) for e in items)
        gap_info[topic] = {
            "total": total,
            "high_impact": len(high_impact),
            "open_questions": open_questions,
            "stale": (now - latest_ts).days > 10,
        }
    return gap_info


def filter_by_mode(gap_info, mode):
    if mode == "focused":
        def cond(v):
            return v["high_impact"] == 1 or v["stale"]
    elif mode == "explore":
        def cond(v):
            return v["total"] < 3
    else:
        def cond(v):
            return v["total"] < 3 or v["high_impact"] == 1 or v["stale"]
    return {k: v for k, v in gap_info.items() if cond(v)}


def suggest_questions(topic):
    return [
        f"What else should I explore about {topic}?",
        f"How does {topic} apply in new contexts?",
    ]


def output_markdown(gaps):
    lines = []
    for topic, info in gaps.items():
        lines.append(f"### {topic}")
        reasons = []
        if info["total"] < 3:
            reasons.append("fewer than 3 entries")
        if info["high_impact"] == 1:
            reasons.append("only one high-impact entry")
        if info["stale"]:
            reasons.append("not updated in last 10 days")
        lines.append(f"- Gap: {', '.join(reasons)}")
        if info["open_questions"]:
            lines.append("- Existing open questions:")
            for q in info["open_questions"]:
                lines.append(f"  - {q}")
        lines.append("- Suggested next questions:")
        for q in suggest_questions(topic):
            lines.append(f"  - {q}")
        lines.append("")
    print("\n".join(lines))


def main():
    parser = argparse.ArgumentParser(description="Analyze learning gaps")
    parser.add_argument("--memory-file", type=Path, default=MEMORY_FILE)
    parser.add_argument("--mode", choices=["all", "focused", "explore"], default="all")
    args = parser.parse_args()

    entries = load_entries(args.memory_file)
    if not entries:
        print("No memory entries found.")
        return
    groups = group_by_topic(entries)
    gap_info = analyze_groups(groups)
    selected = filter_by_mode(gap_info, args.mode)
    if not selected:
        print("No gaps found for mode", args.mode)
        return
    output_markdown(selected)


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Summarize memory entries by topic."""
import argparse
import json
from collections import defaultdict
from pathlib import Path

from memory_manager import extract_topic


def filter_entries(entries, threshold):
    """Return entries with impact_score >= threshold."""
    if threshold <= 0:
        return entries
    return [e for e in entries if e.get("impact_score", 0) >= threshold]


def load_entries(path: Path):
    if not path.exists():
        print(f"No memory file found at {path}")
        return []
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError:
        print("Memory file contains invalid JSON")
        return []


def group_by_topic(entries):
    groups = defaultdict(list)
    for e in entries:
        topic = e.get("topic")
        if not topic:
            text = f"{e.get('question', '')} {e.get('summary', '')} {e.get('answer', '')}"
            topic = extract_topic(text) or "misc"
        groups[topic].append(e)
    return groups


def topic_summary(topic, entries):
    bullet_points = []
    for e in entries:
        summary = e.get("summary") or e.get("answer", "")
        bullet_points.append(f"- {summary}")
    bullets = "\n".join(bullet_points)
    return f"Here\u2019s what you\u2019ve learned so far about {topic}:\n{bullets}"


def top_questions(entries, n=3):
    sorted_e = sorted(entries, key=lambda x: x.get("impact_score", 0), reverse=True)
    return [(e["question"], e.get("impact_score", 0)) for e in sorted_e[:n]]


def main():
    parser = argparse.ArgumentParser(description="Reflect on memory grouped by topic")
    parser.add_argument(
        "--memory-file",
        type=Path,
        default=Path("data/memory/memory.json"),
        help="Path to memory JSON file",
    )
    parser.add_argument(
        "--show-top",
        action="store_true",
        help="Show top 3 questions per topic by impact score",
    )
    parser.add_argument(
        "--score-threshold",
        type=float,
        default=0,
        help="Minimum impact score required to include an entry",
    )
    args = parser.parse_args()

    entries = load_entries(args.memory_file)
    entries = filter_entries(entries, args.score_threshold)
    if not entries:
        print("No memory entries to reflect on.")
        return

    groups = group_by_topic(entries)
    for topic, items in groups.items():
        print("\n" + topic_summary(topic, items))
        if args.show_top:
            print("Top questions:")
            for q, s in top_questions(items):
                print(f"  - ({s}) {q}")


if __name__ == "__main__":
    main()

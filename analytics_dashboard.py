import json
from pathlib import Path
from collections import defaultdict
import sys
import argparse

import matplotlib.pyplot as plt

sys.path.append(str(Path(__file__).resolve().parent / 'scripts'))
from memory_manager import extract_topic

MEMORY_FILE = Path('data/memory/memory.json')
REPORT_FILE = Path('data/analytics_report.md')
PLOT_FILE = Path('data/topic_frequency.png')

def load_entries(path: Path):
    if not path.exists():
        return []
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except json.JSONDecodeError:
        return []

def analyze(entries):
    scores = defaultdict(list)
    counts = defaultdict(int)
    for e in entries:
        topic = e.get('topic')
        if not topic:
            text = f"{e.get('question', '')} {e.get('summary', '')} {e.get('answer', '')}"
            topic = extract_topic(text) or 'misc'
        score = e.get('impact_score', 0)
        scores[topic].append(score)
        counts[topic] += 1
    avg_scores = {t: sum(v)/len(v) for t, v in scores.items()}
    return avg_scores, counts

def top_questions(entries, n=5):
    sorted_e = sorted(entries, key=lambda x: x.get('impact_score', 0), reverse=True)
    return [(e['question'], e.get('impact_score', 0)) for e in sorted_e[:n]]

def plot_counts(counts):
    topics = list(counts.keys())
    values = [counts[t] for t in topics]
    plt.figure(figsize=(8,4))
    plt.bar(topics, values, color='skyblue')
    plt.ylabel('Question Count')
    plt.xlabel('Topic')
    plt.title('Question Frequency per Topic')
    plt.tight_layout()
    PLOT_FILE.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(PLOT_FILE)
    plt.close()

def write_report(avg_scores, counts, top_qs):
    lines = ['# Analytics Report', '']
    lines.append('## Average Impact Score per Topic')
    lines.append('')
    lines.append('| Topic | Avg Impact | Questions |')
    lines.append('|-------|-----------:|----------:|')
    for t, avg in avg_scores.items():
        lines.append(f'| {t} | {avg:.2f} | {counts[t]} |')
    lines.append('')
    if PLOT_FILE.exists():
        lines.append(f'![Frequency]({PLOT_FILE.name})')
        lines.append('')
    lines.append('## Top 5 Most Impactful Questions')
    for q, s in top_qs:
        lines.append(f'- ({s}) {q}')
    REPORT_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(REPORT_FILE, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))

def main():
    parser = argparse.ArgumentParser(description='Generate analytics dashboard')
    parser.add_argument('--memory-file', type=Path, default=MEMORY_FILE)
    args = parser.parse_args()

    entries = load_entries(args.memory_file)
    if not entries:
        print('No memory entries found.')
        return
    avg_scores, counts = analyze(entries)
    top_qs = top_questions(entries)
    plot_counts(counts)
    write_report(avg_scores, counts, top_qs)
    print(f'Report saved to {REPORT_FILE}')
    if PLOT_FILE.exists():
        print(f'Plot saved to {PLOT_FILE}')

if __name__ == '__main__':
    main()

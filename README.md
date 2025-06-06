# 🧠 Reflective AI Research Assistant

A local-first, intelligent research assistant that:
- Ingests PDFs
- Answers context-aware questions
- Summarizes your learnings
- Scores insights by impact
- Suggests gaps in your understanding
- Evolves with every question you ask

---

## 📌 Project Overview

This system helps you **upload research**, **ask questions**, and **track learning** over time using local LLaMA 3.2 (via [Ollama](https://ollama.com)). It stores every answer, analyzes its quality, and lets you reflect on your learning history with analytics, memory chunking, and meta-questioning agents.

---

## 🔧 Features

### 📁 PDF Upload & Chunking
- Drag-and-drop PDF upload from a GUI
- Extracted text is broken into chunks and stored in `data/text_chunks/`

### 🤖 Local Question Answering
- Ask questions using the GUI or CLI
- Retrieves relevant chunks from your research
- Sends to local `llama3` model using `ollama run`
- Displays answer, summary, and auto-generated **impact score**

### 🧠 Dual Memory Architecture
- `memory.json`: logs full Q&A history with timestamp, score, and summary
- `memory_chunks.json`: stores sub-chunks of summaries and answers for granular search

### 📊 Analytics Dashboard
- Run `analytics_dashboard.py` to generate:
  - Topic frequency chart (`topic_frequency.png`)
  - Markdown report (`analytics_report.md`)
  - Highlighted top-impact questions

### 🧪 Reflection & Filtering
- Run `reflect_by_topic.py` to:
  - Group learnings by topic
  - Filter by `--score-threshold`
  - Show `--show-top` insights
- Helps identify high-value vs low-value content

### 🧠 Gap Analyzer (Meta Agent)
- Run `gap_analyzer.py` to:
  - Find neglected or stale topics
  - Suggest open-ended questions you haven’t asked
  - Propose next steps to deepen your understanding

---

## 📁 Folder Structure

```
rag-memory-llama/
├── app_gui.py
├── main_cli.py
├── requirements.txt
├── README.md
├── scripts/
│   ├── pdf_parser.py
│   ├── memory_manager.py
│   ├── memory_chunker.py
│   ├── analytics_dashboard.py
│   ├── reflect_by_topic.py
│   ├── gap_analyzer.py
│   └── ollama_interface.py
├── data/
│   ├── pdfs/
│   ├── text_chunks/
│   ├── memory/
│   │   ├── memory.json
│   │   ├── memory_chunks.json
│   ├── analytics/
│   │   ├── analytics_report.md
│   │   └── topic_frequency.png
```

---

## ⚙️ Setup

### Prerequisites
- Python 3.8+
- [Ollama](https://ollama.com) with `llama3` model installed

### Install Dependencies
```bash
pip install -r requirements.txt
```

### Launch Ollama
```bash
ollama serve
```

### Test Ollama Works
```bash
ollama run llama3 "Hello!"
```

---

## 🚀 How to Use

### 1. Run the GUI
```bash
python app_gui.py
```

- Upload PDFs
- Ask questions
- View model responses
- All memory is stored automatically

### 2. Ask from CLI
```bash
python main_cli.py
```

- Same capabilities as the GUI but in terminal form

### 3. Reflect on Your Learning
```bash
python scripts/reflect_by_topic.py --score-threshold 7 --show-top
```

### 4. Generate Analytics
```bash
python scripts/analytics_dashboard.py
```

### 5. Find Gaps in Understanding
```bash
python scripts/gap_analyzer.py --mode all
```

---

## 💡 Impact Score: What It Means

Each answer gets an `impact_score` from 0–1000, based on:
- Relevance to your question
- Clarity and completeness
- Insightfulness or novelty

Use this score to filter what’s worth reviewing, reflecting on, or improving.

---

## 🤖 Codex-Driven Development

You used [GitHub Copilot/Codex](https://openai.com/blog/copilot) to:
- Auto-fix bugs in reflection scripts
- Generate patch suggestions
- Complete and merge GitHub pull requests
- Expand core logic using your own prompts

This means the system is **self-extensible** — you can continue growing it by prompting Codex from inside GitHub.

---

## 📈 Future Roadmap

- [ ] Weekly Digest Generator (`weekly_digest.py`)
- [ ] Flashcard Export (`flashcards.md`)
- [ ] Semantic Search over All Chunks
- [ ] Codex Planner Agent (auto-asks 1 new question/day)
- [ ] Multi-user SaaS mode with shared knowledge base
- [ ] Notion/Obsidian sync or export

---

## 🧑‍💻 Author

Built by [zephisti](https://github.com/zephisti) using:
- Ollama + LLaMA 3.2
- Python (Tkinter, JSON, matplotlib)
- GitHub Copilot & Codex agents

---

## 📜 License

MIT — Educational and experimental.

---

> ✨ “It doesn’t just answer your questions — it remembers, improves, and reflects on them with you.”


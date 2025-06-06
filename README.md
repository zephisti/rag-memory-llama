# 🧠 Reflective AI Research Assistant

A personal, offline-capable, self-improving research engine powered by PDFs, local LLaMA (via Ollama), and Codex-driven memory reflection.

> "Upload documents. Ask smarter questions. Learn what you’ve already learned."

---

## 📌 Project Overview

This AI-powered desktop tool allows you to:
- Upload and chunk PDFs
- Ask questions with context-aware answers
- Track, summarize, and **reflect** on your research history
- View trends in engagement, learning depth, and topic gaps
- Receive suggested next questions based on memory analysis

Designed to evolve with you — it gets smarter the more you use it.

---

## 🔧 Features

### 🔍 PDF Upload + Chunking
- Upload PDFs via GUI (`app_gui.py`)
- Automatically chunks and stores as searchable JSON

### 🤖 Question Answering
- Ask questions in the GUI or CLI (`main_cli.py`)
- LLaMA 3.2 via Ollama answers using RAG context
- Each answer gets summarized + scored for impact

### 🧠 Memory Reflection
- `reflect_by_topic.py`: Groups and summarizes your learning by topic
- Supports filters like `--score-threshold` to surface only valuable entries

### 📊 Analytics + Reports
- `analytics_dashboard.py`: 
  - Topic frequency visualization
  - Markdown summary of your strongest/weakest areas

### 🧠 Meta Question Agent (Codex-powered)
- `gap_analyzer.py`: Finds gaps in your research based on history
- Suggests new questions to help deepen your learning

---

## 🖥️ Requirements

- Python 3.8+
- [Ollama](https://ollama.com) installed and serving `llama3`
- Required Python packages:

```bash
pip install -r requirements.txt


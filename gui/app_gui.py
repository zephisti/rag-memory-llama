import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
import shutil
import os
import threading
import sys
from pathlib import Path
from uuid import uuid4
from datetime import datetime
import json
import re

sys.path.append(str(Path(__file__).resolve().parent.parent / "scripts"))

from pdf_parser import parse_pdf_to_chunks, save_chunks_to_json
from rag_engine import get_relevant_chunks
from ollama_interface import query_llama

PDF_DIR = Path("data/pdfs")
CHUNK_DIR = Path("data/text_chunks")
MEMORY_FILE = Path("data/memory/memory.json")

class PDFUploaderApp:
    def __init__(self, root):
        self.root = root
        self.root.title("📚 PDF Upload & Chunker + Query")
        self.root.geometry("650x550")

        self.upload_button = tk.Button(root, text="📁 Upload PDF", command=self.upload_pdf)
        self.upload_button.pack(pady=10)

        self.status_area = scrolledtext.ScrolledText(root, height=20, width=80, wrap=tk.WORD)
        self.status_area.pack(padx=10, pady=10)
        self.status_area.insert(tk.END, "📋 Upload a PDF to begin processing...\n")

        self.query_label = tk.Label(root, text="Ask a question about your research:")
        self.query_label.pack()

        self.query_entry = tk.Entry(root, width=80)
        self.query_entry.pack(pady=4)

        self.ask_button = tk.Button(root, text="🧠 Ask", command=self.ask_question)
        self.ask_button.pack()

        PDF_DIR.mkdir(parents=True, exist_ok=True)
        CHUNK_DIR.mkdir(parents=True, exist_ok=True)
        MEMORY_FILE.parent.mkdir(parents=True, exist_ok=True)

    def log(self, message):
        self.status_area.insert(tk.END, f"{message}\n")
        self.status_area.see(tk.END)

    def upload_pdf(self):
        file_path = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
        if not file_path:
            return
        filename = os.path.basename(file_path)
        dest_path = PDF_DIR / filename
        try:
            shutil.copy(file_path, dest_path)
            self.log(f"✅ PDF uploaded: {filename}")
            threading.Thread(target=self.process_pdf, args=(filename,)).start()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to upload PDF: {e}")

    def process_pdf(self, filename):
        try:
            pdf_path = PDF_DIR / filename
            self.log(f"🔍 Parsing: {filename}")
            chunks = parse_pdf_to_chunks(pdf_path)
            save_chunks_to_json(filename, chunks)
            self.log(f"✅ Extracted {len(chunks)} chunks from {filename}")
        except Exception as e:
            self.log(f"❌ Error parsing {filename}: {e}")

    def ask_question(self):
        query = self.query_entry.get().strip()
        if not query:
            self.log("⚠️ Enter a question first.")
            return

        self.log(f"\n🔍 Query: {query}")
        chunks = get_relevant_chunks(query)
        context = "\n\n".join([c['text'] for c in chunks])

        self.log("📚 Retrieved top relevant chunks...")
        response = query_llama(query, system_context=context)
        self.log(f"🤖 LLaMA Response:\n{response}")

        summary_prompt = f"Summarize this answer in 1 sentence:\n{response}"
        summary = query_llama(summary_prompt)
        self.log(f"📌 Summary: {summary}")

        score_prompt = f"Rate the importance of this answer on a scale from 1 to 10:\n{response}"
        score_str = query_llama(score_prompt)
        try:
            match = re.search(r'\b([1-9]|10)\b', score_str)
            impact_score = int(match.group(1)) if match else 5
        except:
            impact_score = 5

        self.log(f"⭐️ Impact Score: {impact_score}")
        self.save_to_memory_log(query, response, summary, impact_score)

    def save_to_memory_log(self, question, answer, summary, impact_score=5):
        new_entry = {
            "id": str(uuid4()),
            "timestamp": datetime.utcnow().isoformat(),
            "question": question,
            "answer": answer,
            "summary": summary,
            "impact_score": impact_score
        }

        if MEMORY_FILE.exists():
            with open(MEMORY_FILE, "r", encoding="utf-8") as f:
                try:
                    log = json.load(f)
                except:
                    log = []
        else:
            log = []

        log.append(new_entry)

        with open(MEMORY_FILE, "w", encoding="utf-8") as f:
            json.dump(log, f, indent=2, ensure_ascii=False)

        self.log("💾 Memory log updated.")

if __name__ == "__main__":
    root = tk.Tk()
    app = PDFUploaderApp(root)
    root.mainloop()

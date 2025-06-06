from flask import Flask, request, jsonify, send_from_directory
from pathlib import Path
import re
import json

from scripts.pdf_parser import parse_pdf_to_chunks, save_chunks_to_json
from scripts.rag_engine import get_relevant_chunks
from scripts.ollama_interface import query_llama
from scripts.memory_manager import add_entry, load_log

PDF_DIR = Path('data/pdfs')

app = Flask(__name__, static_folder='.')

@app.route('/')
def index():
    return send_from_directory('.', 'frontend.html')

@app.route('/upload', methods=['POST'])
def upload_pdf():
    if 'pdf' not in request.files:
        return jsonify({'error': 'no file'}), 400
    f = request.files['pdf']
    PDF_DIR.mkdir(parents=True, exist_ok=True)
    path = PDF_DIR / f.filename
    f.save(path)
    chunks = parse_pdf_to_chunks(path)
    save_chunks_to_json(f.filename, chunks)
    return jsonify({'status': 'ok', 'chunks': len(chunks)})

@app.route('/ask', methods=['POST'])
def ask_question():
    data = request.get_json() or {}
    question = data.get('question')
    if not question:
        return jsonify({'error': 'no question'}), 400
    chunks = get_relevant_chunks(question)
    context = "\n\n".join([c['text'] for c in chunks])
    response = query_llama(question, system_context=context)
    summary = query_llama(f"Summarize this answer in 1 sentence:\n{response}")
    score_str = query_llama(
        f"Rate the importance of this answer on a scale from 1 to 10:\n{response}"
    )
    match = re.search(r'\b([1-9]|10)\b', score_str)
    try:
        impact = int(match.group(1)) if match else 5
    except Exception:
        impact = 5
    add_entry(question, response, summary, impact)
    return jsonify({'answer': response, 'impact': impact})

@app.route('/memory')
def memory():
    return jsonify(load_log())

if __name__ == '__main__':
    app.run(debug=True)

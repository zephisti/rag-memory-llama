import subprocess

def query_llama(prompt, system_context=None, model="llama3.2"):
    full_prompt = ""
    if system_context:
        full_prompt += f"<<SYS>>\n{system_context}\n<</SYS>>\n"
    full_prompt += f"{prompt}"
    try:
        result = subprocess.run(
            ["ollama", "run", model, full_prompt],
            capture_output=True,
            text=True,
            encoding="utf-8",
            timeout=60
        )
        return result.stdout.strip()
    except Exception as e:
        return f"❌ Error calling LLaMA: {e}"

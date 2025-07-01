import os
import sys
import re
import uuid
import json
import httpx

def format_conversation_history(history: list[dict]) -> str:
    formatted_history = ""
    for message in list(history)[-10:]:
        prefix = "User:" if message["role"] == "user" else "assistant:"
        clean = re.sub(r"\b(Assistant|User)\s*:\s*", "", message["content"], flags=re.IGNORECASE).strip()
        formatted_history += f"{prefix} {clean}\n"
    return formatted_history

def build_system_prompt(formatted_history: str, prompt_file: str = "default.txt", tone="casual", emotion="helpful") -> str:
    metadata_line = f"Tone: {tone} | Emotion: {emotion}"
    prompt_dir = "prompts"
    if getattr(sys, 'frozen', False):
        base_path = sys._MEIPASS
    else:
        base_path = os.path.abspath(".")
    prompt_path = os.path.join(base_path, prompt_dir, prompt_file)
    print(f"Using prompt file: {prompt_path}")
    if not os.path.exists(prompt_path):
        raise FileNotFoundError(f"Prompt file '{prompt_path}' not found.")
    with open(prompt_path, "r", encoding="utf-8") as f:
        base_prompt = f.read()
    system_prompt = base_prompt.format(
        metadata=metadata_line,
        history=formatted_history
    )
    return system_prompt

def generate_response_from_ollama(prompt: str) -> str:
    request_id = str(uuid.uuid4())[:8]
    print(f"[Request {request_id}] Sending prompt to Ollama...")
    payload = {
        "model": "llama3",
        "prompt": prompt,
        "stream": True
    }
    final_response = ""
    with httpx.stream("POST", "http://localhost:11434/api/generate", json=payload, timeout=60.0) as r:
        for line in r.iter_lines():
            if not line.strip():
                continue
            try:
                chunk = json.loads(line)
                final_response += chunk.get("response", "")
            except json.JSONDecodeError:
                print(f"[Ollama Stream Error] Could not parse: {line}")
    print(f"[Request {request_id}] Final model output: {final_response[:200]}")
    return final_response
    
def parse_model_response(output_text: str) -> tuple[str, list[tuple[str, str]]]:
    match = re.search(r"assistant:\s*(.*)", output_text, re.DOTALL)
    assistant_section = match.group(1).strip() if match else output_text.strip()
    assistant_section = re.sub(r"Tone:\s*\w+\s*\|\s*Emotion:\s*\w+", "", assistant_section).strip()
    assistant_reply_raw = assistant_section
    tags = re.findall(r"<([^:>]+):([^>]+)>", assistant_reply_raw)
    return assistant_section, tags

def run_chat_completion():
    history = []
    print("Type 'exit' to quit.\n")
    while True:
        user_input = input("You: ")
        if user_input.lower() == "exit":
            break

        history.append({"role": "user", "content": user_input})
        formatted = format_conversation_history(history)
        system_prompt = build_system_prompt(formatted)
        response = generate_response_from_ollama(system_prompt)
        cleaned_response = parse_model_response(response)
        print("Assistant: ", cleaned_response[0])
        history.append({"role": "assistant", "content": cleaned_response[0]})

if __name__ == "__main__":
    run_chat_completion()

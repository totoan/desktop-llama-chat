import threading
import tkinter as tk
from tkinter import scrolledtext

from chat_app_resources import (
    format_conversation_history, 
    build_system_prompt, 
    generate_response_from_ollama, 
    parse_model_response,
)

history = []

def handle_send(input_box, output_box):
    user_input = input_box.get().strip()
    if not user_input:
        return
    input_box.delete(0, tk.END)

    output_box.configure(state="normal")
    output_box.insert(tk.END, f"You: {user_input}\n")
    output_box.configure(state="disabled")

    history.append({"role": "user", "content": user_input})

    def generate_response():
        formatted = format_conversation_history(history)
        system_prompt = build_system_prompt(formatted)
        response = generate_response_from_ollama(system_prompt)
        reply, _ = parse_model_response(response)

        history.append({"role": "assistant", "content": reply})
        output_box.configure(state="normal")
        output_box.insert(tk.END, f"Assistant: {reply}\n\n")
        output_box.configure(state="disabled")
        output_box.see(tk.END)

    threading.Thread(target=generate_response).start()

def create_app():
    root = tk.Tk()
    root.title("Desktop Assistant App")
    root.geometry("600x500")
    root.configure(bg="#1e1e1e")

    output_box = scrolledtext.ScrolledText(root, wrap=tk.WORD, bg="#2a2a2a", fg="#ffffff", font=("Arial", 11))
    output_box.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
    output_box.configure(state="disabled")

    input_frame = tk.Frame(root, bg="#1e1e1e")
    input_frame.pack(fill=tk.X, padx=10, pady=(0, 10))

    input_box = tk.Entry(input_frame, bg="#333333", fg="#ffffff", font=("Arial", 11))
    input_box.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))
    input_box.bind("<Return>", lambda event: handle_send(input_box, output_box))

    send_button = tk.Button(input_frame, text="Send", command=lambda: handle_send(input_box, output_box), bg="#444444", fg="#ffffff", font=("Arial", 11))
    send_button.pack(side=tk.RIGHT)

    root.mainloop()

if __name__ == "__main__":
    create_app()
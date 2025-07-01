🗨️ Desktop Assistant App (Llama 3 Chat)
A simple desktop chatbot application powered by the Llama 3 large language model.
It provides a local, private, and customizable chat experience with a modern Tkinter GUI.

✨ Features
💬 Interactive chat interface with scrolling conversation history.
⚡️ Fast, local responses using the Llama 3 model via Ollama backend.
🖥️ Simple desktop GUI built with Tkinter.
🗂️ Modular prompt system with support for tone and emotion metadata.
🔧 Easy to customize or extend for different prompt styles or system behaviors.

🛠️ Tech Stack
Python 3.10+
Tkinter for GUI
Ollama (Llama 3 backend) — local HTTP API
httpx for streaming responses

🚀 Installation
Clone the repository:

git clone https://github.com/totoan/desktop-llama-chat.git
cd desktop-llama-chat

Set up a virtual environment (optional but recommended):
python -m venv .venv
source .venv/bin/activate    # On Windows: .venv\Scripts\activate

Install dependencies:
pip install -r requirements.txt

Install and start Ollama (Llama 3 backend):
This app requires Ollama to run the Llama 3 model locally.
Download and install Ollama from https://ollama.com/.
Make sure Ollama is running on http://localhost:11434 before starting the app.

Run the app:
python assistant_app.py

💡 Usage
Type your message into the input box and press Enter or click Send.
The assistant reply will appear in the scrolling chat window.
Prompts can be customized in the prompts/default.txt file, including tone and emotion tags.

📂 Project Structure
.
├── assistant_app.py         # Main GUI app entry point
├── chat_app_resources.py    # Core logic: prompt building, history formatting, API calls
├── prompts/
│   └── default.txt          # Base prompt template
├── requirements.txt
└── README.md

⚖️ License
MIT License.
Feel free to modify or use for personal or educational purposes.

🤝 Contributing
Contributions are welcome!
Open an issue or submit a pull request if you'd like to improve or extend the app.

## - Multi-Turn Gemini Chatbot

A beginner-friendly chatbot made with Python, Flask, HTML, CSS, JavaScript, and the Google Gemini API.

## Features

- Uses a real Gemini LLM API
- Remembers earlier messages in the same conversation
- Keeps each conversation separate with its own ID
- Sends only the latest 10 messages to Gemini
- Has a custom system instruction for a friendly learning assistant
- Shows clear messages when the API or server fails
- Keeps the API key in a local `.env` file
- Includes a New Chat button

## 1. Get a Gemini API key

Open Google AI Studio:

https://aistudio.google.com/app/apikey

Create your own API key. Check the current free-tier availability, limits, and regional eligibility in Google AI Studio. Free usage is subject to Google's terms and can change.

Never paste your API key into Python, JavaScript, README, screenshots, or GitHub.

## 2. Open the project in VS Code

Extract the ZIP file and open the `gemini-multiturn-chatbot` folder in VS Code.

Open Terminal > New Terminal.

## 3. Create a virtual environment

Windows PowerShell:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

If PowerShell blocks activation, you can use Command Prompt:

```cmd
.venv\Scripts\activate.bat
```

Install the packages:

```powershell
python -m pip install -r requirements.txt
```

## 4. Add your API key

In VS Code, copy `.env.example` and rename the copy to `.env`.

Open `.env` and add your own key:

```env
GEMINI_API_KEY=your_real_gemini_key
```

Do not add quotation marks around the key. Do not upload `.env` to GitHub. The `.gitignore` file already excludes it.

## 5. Run the chatbot

```powershell
python app.py
```

Open this in your browser:

http://127.0.0.1:5000

## 6. Test conversation memory

Send these messages in the same chat:

1. My name is Alex.
2. I am learning Python.
3. What programming language am I learning?
4. What is my name?
5. Explain a Python variable with a simple example.

The chatbot should remember the name and programming language from the earlier messages.

Click New Chat to start a separate conversation.

## 7. How context management works

In `app.py`:

```python
MAX_HISTORY_MESSAGES = 10
```

The app stores the conversation history and sends only the latest 10 messages to Gemini with each request. A normal user/assistant exchange uses two messages, so this is about five complete turns.

This is a simple context-window strategy. The conversation history is stored in server memory, so it is cleared when the Flask server restarts. For a production project, use a database such as SQLite or PostgreSQL.

## 8. Backend endpoint

`POST /api/chat`

Example request:

```json
{
  "message": "What is my name?",
  "conversation_id": "your-conversation-id"
}
```

`POST /api/new` creates a new conversation ID.

## 9. Upload to GitHub

Create a new public repository:

https://github.com/new

Choose a repository name such as `Multi-Turn-Gemini-Chatbot`.

In the VS Code terminal, run:

```powershell
git init
git add .
git status
```

Check carefully that `.env` is not listed. Then:

```powershell
git commit -m "Add multi-turn Gemini chatbot"
git branch -M main
git remote add origin https://github.com/YOUR-USERNAME/Multi-Turn-Gemini-Chatbot.git
git push -u origin main
```

Replace `YOUR-USERNAME` with your GitHub username.

## Important notes

- The Gemini API key is private. Never commit it.
- The free tier has usage limits and availability conditions.
- This project uses in-memory conversation storage for a simple college demo.
- Do not use Flask debug mode on a public production server.

## Useful links

- Gemini API key: https://aistudio.google.com/app/apikey
- Gemini API documentation: https://ai.google.dev/gemini-api/docs
- GitHub: https://github.com

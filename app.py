import os
import uuid
from threading import Lock

from dotenv import load_dotenv
from flask import Flask, jsonify, render_template, request
from google import genai
from google.genai import errors

# Read the API key from the .env file.
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

app = Flask(__name__)

# The app can start without a key, but chat requests will show a clear error.
client = genai.Client(api_key=api_key) if api_key else None

# This is the personality and role of the chatbot.
SYSTEM_PROMPT = """
You are StudyBuddy, a friendly learning assistant for college students.
Explain topics in simple English and use small examples.
Be patient with beginners and answer clearly.
If you do not know something, say so instead of guessing.
"""

# Each conversation ID has its own message history.
conversations = {}
history_lock = Lock()

# Only the latest 10 messages are sent to Gemini each time.
MAX_HISTORY_MESSAGES = 10


@app.route("/")
def home():
    return render_template("index.html")


@app.post("/api/chat")
def chat():
    data = request.get_json(silent=True) or {}
    message = data.get("message", "")
    conversation_id = data.get("conversation_id")

    if not isinstance(message, str) or not message.strip():
        return jsonify({"error": "Please type a message first."}), 400

    message = message.strip()

    if len(message) > 4000:
        return jsonify({"error": "Please keep your message under 4,000 characters."}), 400

    if not client:
        return jsonify({
            "error": "Gemini API key is missing. Add GEMINI_API_KEY to your .env file."
        }), 500

    # Create a new conversation ID when the browser does not send one.
    if not isinstance(conversation_id, str) or not conversation_id:
        conversation_id = str(uuid.uuid4())

    # Get this conversation's earlier messages.
    with history_lock:
        old_history = list(conversations.get(conversation_id, []))

    # Gemini uses 'user' for the user and 'model' for the chatbot.
    new_history = old_history + [
        {"role": "user", "parts": [{"text": message}]}
    ]

    # Context management: send only the latest 10 messages.
    short_history = new_history[-MAX_HISTORY_MESSAGES:]

    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=short_history,
            config={
                "system_instruction": SYSTEM_PROMPT,
                "temperature": 0.7,
            },
        )

        reply = response.text

        if not reply:
            return jsonify({
                "error": "Gemini did not return a reply. Please try again."
            }), 502

        # Save the conversation only after Gemini replies successfully.
        saved_history = new_history + [
            {"role": "model", "parts": [{"text": reply}]}
        ]

        with history_lock:
            conversations[conversation_id] = saved_history

        return jsonify({
            "conversation_id": conversation_id,
            "reply": reply,
        })

    except errors.APIError as error:
        app.logger.error("Gemini API error: %s", error)
        return jsonify({
            "error": "Gemini could not process the request. Check your API key, quota, and try again."
        }), 502
    except TimeoutError:
        return jsonify({
            "error": "The request took too long. Please try again."
        }), 504
    except Exception:
        app.logger.exception("Unexpected chatbot error")
        return jsonify({
            "error": "Something went wrong. Please check your internet connection and try again."
        }), 500


@app.post("/api/new")
def new_chat():
    conversation_id = str(uuid.uuid4())

    with history_lock:
        conversations[conversation_id] = []

    return jsonify({"conversation_id": conversation_id})


if __name__ == "__main__":
    # Debug mode is useful locally. Do not use it on a public production server.
    app.run(debug=True, port=5000)

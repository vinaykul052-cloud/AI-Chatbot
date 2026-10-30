# AI-Powered Customer Support Chatbot

A retrieval-based chatbot built with Python, Flask and NLP. It answers customer
support FAQs (orders, returns, payments, delivery), understands English and
Hinglish, remembers conversation context, and logs every interaction in SQLite.

## Features
- NLP preprocessing: lowercase, punctuation removal, tokenization, lemmatization (NLTK)
- Intent matching with TF-IDF and cosine similarity (scikit-learn)
- Confidence threshold and vocabulary-coverage check for safe fallback replies
- Context handling: follow-up replies like "yes" or "no" are understood per session
- Hinglish support (e.g. "mera order kahan hai")
- Interaction logs (message, reply, intent, score, timestamp) stored in SQLite
- Simple chat UI using HTML, CSS and JavaScript

## Tech Stack
Python, Flask, NLTK, scikit-learn, SQLite, HTML/CSS/JavaScript

## How It Works
User message -> Flask `/chat` API -> preprocessing -> TF-IDF + cosine similarity
-> context check -> response -> log saved in SQLite -> JSON reply

## Project Structure
```
ai-chatbot/
├── app.py            # Flask server and API routes
├── chatbot.py        # NLP, intent matching, context logic
├── database.py       # SQLite logging
├── intents.json      # Intents, patterns and responses
├── templates/index.html
└── static/ (style.css, script.js)
```

## Setup
```bash
git clone <your-repo-link>
cd ai-chatbot
python -m venv venv
venv\Scripts\activate        # Mac/Linux: source venv/bin/activate
pip install -r requirements.txt
python app.py
```
Open http://127.0.0.1:5000 in your browser.

## API
- `POST /chat` with `{"message": "hello", "session_id": "optional"}`
- `GET /logs` returns the last 20 interactions

## Limitations
- Retrieval-based: it picks from predefined responses and cannot generate new answers
- Context is stored in memory and resets when the server restarts
- Hindi in Devanagari script and other languages fall back to a default reply

## Future Improvements
- Multilingual support using Hugging Face sentence-transformers
- Context storage in Redis or a database
- Admin dashboard to review fallback queries and add new intents

## Author
[VK]
## Output<img width="497" height="701" alt="image" src="https://github.com/user-attachments/assets/2f9eb581-74d9-481f-8fe8-da66df51fa4e" />


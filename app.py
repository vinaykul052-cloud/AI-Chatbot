#session id  create krege 
#har user ko ek unique id milti hai (uuid) taaki uski conversation logs mei group ho ske

import uuid
from flask import Flask, request, jsonify, render_template

from chatbot import get_response
from database import init_db, save_log, get_logs

app = Flask(__name__)
init_db() # Initialize the database when the app starts 

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    message = (data or {}).get("message", "").strip()
    session_id = (data or {}).get("session_id") or str(uuid.uuid4())

    if not message:
        return jsonify({"error": "Message cannot be empty."}), 400
    response, intent, score = get_response(message,session_id)
    #print("DEBUG: ", intent, score, session_id)
    save_log(session_id, message, response, intent, score)
    return jsonify({
        "response": response,
        "intent": intent,
        "score": score,
        "session_id": session_id
    })

@app.route("/logs")
def logs():
    rows = get_logs(20) # Fetch the last 20 logs
    return jsonify([
        {"id": r[0], "session_id": r[1], "message": r[2],
         "intent": r[3], "score": r[4], "timestamp": r[5]}
        for r in rows
    ])

if __name__ == "__main__":
    app.run(debug=True)
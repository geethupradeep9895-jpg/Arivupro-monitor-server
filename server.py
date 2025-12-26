from flask import Flask, request, jsonify
from datetime import datetime

app = Flask(__name__)

# In-memory event store
EVENTS = []

@app.route("/")
def home():
    return jsonify({
        "status": "ArivuPro Monitor OK",
        "time": datetime.utcnow().isoformat()
    })

@app.route("/report", methods=["POST"])
def report():
    data = request.get_json(force=True, silent=True)

    if not data:
        return jsonify({"error": "Invalid JSON"}), 400

    event = {
        "branch": data.get("branch", "Unknown"),
        "room": data.get("room", "Unknown"),
        "events": [{
            "severity": data.get("severity", "WARNING"),
            "message": data.get("message", "")
        }],
        "issues": [],
        "timestamp": datetime.utcnow().isoformat()
    }

    EVENTS.append(event)

    # Keep only last 100 events
    if len(EVENTS) > 100:
        EVENTS.pop(0)

    return jsonify({"status": "ok"})

@app.route("/events", methods=["GET"])
def events():
    return jsonify(EVENTS)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)


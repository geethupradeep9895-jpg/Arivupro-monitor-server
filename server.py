from flask import Flask, request, jsonify
from datetime import datetime, timezone
import os

app = Flask(__name__)
EVENTS = []

def now():
    return datetime.now(timezone.utc).isoformat()

@app.get("/")
def home():
    return jsonify({
        "status": "ArivuPro Monitor OK",
        "time": now()
    })

@app.post("/ingest")
def ingest():
    data = request.get_json(force=True, silent=True) or {}
    EVENTS.append({
        "ts": now(),
        "branch": data.get("branch", ""),
        "room": data.get("room", ""),
        "events": data.get("events", []),
        "issues": data.get("issues", [])
    })
    return jsonify({"ok": True, "count": len(EVENTS)})

@app.get("/events")
def events():
    return jsonify(EVENTS[-50:])

if __name__ == "__main__":
    port = int(os.environ.get("PORT", "8080"))
    app.run(host="0.0.0.0", port=port)


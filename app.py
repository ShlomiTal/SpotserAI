import os
from flask import Flask, request, jsonify
from signals.logic import save_signal, update_results
from utils.analysis import get_statistics
from utils.enhancer import suggest_improvements

app = Flask(__name__)

@app.route("/")
def home():
    return {"status": "UltraSignalX API Online"}

@app.route("/signal", methods=["POST"])
def receive_signal():
    data = request.json
    if not data or "symbol" not in data:
        return {"error": "Invalid signal"}, 400
    save_signal(data)
    return {"status": "Signal saved"}

@app.route("/update", methods=["POST"])
def update_signal_result():
    updated = update_results()
    return {"status": "Results updated", "updated": updated}

@app.route("/stats", methods=["GET"])
def stats():
    return get_statistics()

@app.route("/optimize", methods=["GET"])
def optimize():
    return suggest_improvements()

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

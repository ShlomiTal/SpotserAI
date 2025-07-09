from flask import Flask, request, jsonify
from signals.logic import save_signal, update_results

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
    update_results()
    return {"status": "Updated results"}

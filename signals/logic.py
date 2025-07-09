import json
from datetime import datetime, timedelta

SIGNAL_FILE = "signals/memory.json"

def load_signals():
    try:
        with open(SIGNAL_FILE, "r") as f:
            return json.load(f)
    except:
        return []

def save_signals(data):
    with open(SIGNAL_FILE, "w") as f:
        json.dump(data, f, indent=2)

def save_signal(signal):
    signals = load_signals()
    signal["timestamp"] = datetime.utcnow().isoformat()
    signal["result"] = None
    signals.append(signal)
    save_signals(signals)

def update_results():
    signals = load_signals()
    now = datetime.utcnow()
    updated = []
    for s in signals:
        if s["result"] is not None:
            updated.append(s)
            continue
        signal_time = datetime.fromisoformat(s["timestamp"])
        if now - signal_time > timedelta(minutes=50):  # נגיד 10 נרות של 5 דק
            # כאן נבצע חיבור ל־API של מחירים כדי לבדוק הצלחה
            # בינתיים סימולציה:
            import random
            s["result"] = "win" if random.random() > 0.3 else "loss"
        updated.append(s)
    save_signals(updated)

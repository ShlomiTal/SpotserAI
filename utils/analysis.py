import json
from signals.logic import load_signals

def get_statistics():
    signals = load_signals()
    total = len(signals)
    wins = sum(1 for s in signals if s.get("result") == "win")
    losses = sum(1 for s in signals if s.get("result") == "loss")
    win_rate = (wins / total * 100) if total else 0
    return {
        "total_signals": total,
        "wins": wins,
        "losses": losses,
        "win_rate_percent": round(win_rate, 2)
    }

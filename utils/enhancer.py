from signals.logic import load_signals

def suggest_improvements():
    signals = load_signals()
    rsi_zone_wins = {}
    count = {}

    for s in signals:
        if s.get("result") not in ["win", "loss"]:
            continue
        rsi = s.get("rsi")
        if rsi is None:
            continue
        zone = f"{int(rsi // 10) * 10}-{int(rsi // 10) * 10 + 9}"
        count.setdefault(zone, 0)
        rsi_zone_wins.setdefault(zone, 0)
        count[zone] += 1
        if s["result"] == "win":
            rsi_zone_wins[zone] += 1

    best_zones = {
        zone: round((rsi_zone_wins[zone] / count[zone]) * 100, 2)
        for zone in count if count[zone] >= 5
    }

    sorted_zones = sorted(best_zones.items(), key=lambda x: x[1], reverse=True)
    return {
        "best_rsi_zones": sorted_zones[:3],
        "tip": "Consider focusing on RSI zones with win rate > 70%"
    }

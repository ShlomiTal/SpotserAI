import os
import hmac
import hashlib
import time
from fastapi import FastAPI, Request
import httpx
from dotenv import load_dotenv

# Load API keys from environment
load_dotenv()

BINANCE_API_KEY = os.getenv("BINANCE_API_KEY")
BINANCE_API_SECRET = os.getenv("BINANCE_API_SECRET")
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

BACKTEST_LOG = "backtest_log.txt"

app = FastAPI()

@app.get("/")
def read_root():
    return {"status": "OK", "message": "The bot is running"}

def binance_futures_request(method, endpoint, params):
    url = f"https://fapi.binance.com{endpoint}"
    params["timestamp"] = int(time.time() * 1000)
    query_string = "&".join([f"{k}={v}" for k, v in params.items()])
    signature = hmac.new(BINANCE_API_SECRET.encode(), query_string.encode(), hashlib.sha256).hexdigest()
    params["signature"] = signature
    headers = {"X-MBX-APIKEY": BINANCE_API_KEY}
    if method == "GET":
        return httpx.get(url, params=params, headers=headers).json()
    else:
        return httpx.post(url, params=params, headers=headers).json()

def get_futures_balance():
    data = binance_futures_request("GET", "/fapi/v2/balance", {})
    for asset in data:
        if asset["asset"] == "USDT":
            return float(asset["availableBalance"])
    return 0

def place_order(side, quantity):
    params = {
        "symbol": "SOLUSDT",
        "side": side.upper(),
        "type": "MARKET",
        "quantity": quantity
    }
    return binance_futures_request("POST", "/fapi/v1/order", params)

def set_leverage(leverage):
    params = {
        "symbol": "SOLUSDT",
        "leverage": leverage
    }
    return binance_futures_request("POST", "/fapi/v1/leverage", params)

def place_tp_sl(side, entry_price, quantity):
    tp_price = round(entry_price * 1.5, 2)
    sl_price = round(entry_price * 0.5, 2)
    opposite_side = "SELL" if side == "BUY" else "BUY"

    tp_params = {
        "symbol": "SOLUSDT",
        "side": opposite_side,
        "type": "TAKE_PROFIT_MARKET",
        "stopPrice": tp_price,
        "closePosition": "true",
        "workingType": "MARK_PRICE"
    }
    binance_futures_request("POST", "/fapi/v1/order", tp_params)

    sl_params = {
        "symbol": "SOLUSDT",
        "side": opposite_side,
        "type": "STOP_MARKET",
        "stopPrice": sl_price,
        "closePosition": "true",
        "workingType": "MARK_PRICE"
    }
    binance_futures_request("POST", "/fapi/v1/order", sl_params)

def send_telegram(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {"chat_id": TELEGRAM_CHAT_ID, "text": message}
    httpx.post(url, json=payload)

def log_backtest(details):
    with open(BACKTEST_LOG, "a") as f:
        f.write(f"{time.strftime('%Y-%m-%d %H:%M:%S')} - {details}\n")

@app.post("/webhook")
async def webhook(request: Request):
    data = await request.json()
    side = data.get("side")

    if side:
        set_leverage(75)
        balance = get_futures_balance()
        allocation = balance * 0.25
        latest_price = binance_futures_request("GET", "/fapi/v1/ticker/price", {"symbol": "SOLUSDT"})
        price = float(latest_price["price"])
        quantity = round((allocation * 75) / price, 2)

        order = place_order(side, quantity)
        entry_price = float(order['fills'][0]['price']) if 'fills' in order else price
        place_tp_sl(side, entry_price, quantity)

        message = (
            f"📢 SOLUSDT Futures Trade Executed\n\n"
            f"Side: {side}\nQuantity: {quantity}\nEntry: {entry_price}\n"
            f"TP: {round(entry_price * 1.5, 2)}\nSL: {round(entry_price * 0.5, 2)}\n"
            f"Balance Used: {allocation:.2f} USDT (25%)"
        )
        send_telegram(message)

        log_details = f"SIDE={side}, ENTRY={entry_price}, QTY={quantity}, TP={round(entry_price * 1.5, 2)}, SL={round(entry_price * 0.5, 2)}"
        log_backtest(log_details)

        return {"status": "success", "details": order}
    else:
        return {"status": "error", "message": "Missing side"}

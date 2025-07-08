# SOLUSDT Futures Trading Bot

## ✅ Features:
- Auto Futures Trading on Binance (SOLUSDT)
- Leverage: 75x
- 25% Balance Allocation Per Trade
- Auto TP (+50%) & SL (-50%)
- Telegram Trade Notifications
- Auto Backtest Logging

## ✅ Setup:
1. Fill `.env` with your Binance API keys and Telegram Bot details.
2. Install dependencies:
```bash
pip install -r requirements.txt
```
3. Run the bot locally:
```bash
uvicorn main:app --host 0.0.0.0 --port 8000
```
4. Deploy to Railway or similar.

## ✅ TradingView Webhook Example:
```json
{
  "side": "BUY"
}
```

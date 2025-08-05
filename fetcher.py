import yfinance as yf
import pandas as pd

def get_stock_data(ticker):
    info = yf.Ticker(ticker).info

    price = info.get('currentPrice', 0)
    roe = info.get('returnOnEquity', 0)
    debt_equity = info.get('debtToEquity', 1000)
    promoter_holding = info.get('heldPercentInsiders', 0)

    data = yf.download(ticker, period="1mo", interval="1d")
    rsi = calculate_rsi(data['Close'])

    score = 0
    if price <= 500: score += 20
    if roe and roe > 0.15: score += 20
    if debt_equity and debt_equity < 100: score += 20
    if promoter_holding and promoter_holding > 0.30: score += 20
    if rsi and 30 < rsi < 70: score += 20

    return {
        "ticker": ticker,
        "price": round(price, 2),
        "score": round(score, 1),
        "reason": f"ROE: {roe}, Debt/Equity: {debt_equity}, RSI: {rsi}",
    }

def calculate_rsi(series, period=14):
    delta = series.diff().dropna()
    gain = delta.where(delta > 0, 0)
    loss = -delta.where(delta < 0, 0)

    avg_gain = gain.rolling(window=period).mean()
    avg_loss = loss.rolling(window=period).mean()

    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))
    last_rsi = rsi.iloc[-1] if not rsi.empty else None

    return round(last_rsi, 2) if last_rsi else None

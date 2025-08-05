import yfinance as yf
import pandas as pd

def calculate_rsi(series, period=14):
    delta = series.diff().dropna()
    gain = delta.where(delta > 0, 0)
    loss = -delta.where(delta < 0, 0)

    avg_gain = gain.rolling(window=period).mean()
    avg_loss = loss.rolling(window=period).mean()

    rs = avg_gain / avg_loss
    rsi_series = 100 - (100 / (1 + rs))

    last_rsi = rsi_series.iloc[-1] if not rsi_series.empty else None
    return round(last_rsi, 2) if last_rsi is not None else None

def get_stock_data(ticker):
    score = 0
    try:
        data = yf.download(ticker, period="1mo", interval="1d", progress=False)

        # Check if data is valid
        if not data.empty and "Close" in data.columns and not data["Close"].isna().any():
            # Price movement scoring
            if data["Close"].iloc[-1] > data["Close"].iloc[0]:
                score += 10

            # RSI scoring
            rsi = calculate_rsi(data["Close"])
            if rsi is not None and 30 < rsi < 70:
                score += 20
        else:
            rsi = None  # In case data["Close"] is invalid

    except Exception as e:
        print(f"Error processing {ticker}: {e}")
        rsi = None

    return {
        "ticker": ticker,
        "score": score,
        "rsi": rsi
    }

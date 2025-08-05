import pandas as pd
from fetcher import get_stock_data
import os
from datetime import datetime

MAX_SHARES = 50
MIN_SHARES = 10
BUDGET_PER_STOCK = 500

def suggest_quantity(price):
    qty = min(MAX_SHARES, max(MIN_SHARES, int(10000 / price)))
    return qty

def format_markdown(results):
    lines = []
    lines.append(f"# 📊 Stock Suggestions — {datetime.now().strftime('%Y-%m-%d %H:%M')}\n")
    lines.append("| Ticker | Price | Score | Qty | Total ₹ | Reason |")
    lines.append("|--------|-------|-------|-----|---------|--------|")
    for stock in results:
        lines.append(f"| {stock['ticker']} | ₹{stock['price']} | {stock['score']} | {stock['buy_quantity']} | ₹{stock['total_cost']} | {stock['reason']} |")
    return "\n".join(lines)

def main():
    tickers_df = pd.read_csv("tickers.csv")
    results = []

    for ticker in tickers_df['ticker']:
        stock = get_stock_data(ticker)
        if stock['score'] >= 60 and stock['price'] <= BUDGET_PER_STOCK:
            stock['buy_quantity'] = suggest_quantity(stock['price'])
            stock['total_cost'] = round(stock['buy_quantity'] * stock['price'], 2)
            results.append(stock)

    sorted_results = sorted(results, key=lambda x: x['score'], reverse=True)
    os.makedirs("results", exist_ok=True)
    filename = f"results/suggestions_{datetime.now().strftime('%Y%m%d_%H%M')}.md"

    with open(filename, "w", encoding="utf-8") as f:
        f.write(format_markdown(sorted_results))

    print(f"✅ Saved: {filename}")

if __name__ == "__main__":
    main()

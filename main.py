import pandas as pd
from fetcher import get_stock_data

MAX_SHARES = 50
MIN_SHARES = 10
BUDGET_PER_STOCK = 500

def suggest_quantity(price):
    qty = min(MAX_SHARES, max(MIN_SHARES, int(10000 / price)))
    return qty

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
    for s in sorted_results:
        print(s)

if __name__ == "__main__":
    main()

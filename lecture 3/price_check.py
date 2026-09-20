"""Fetch the latest Tesla price from Yahoo Finance."""
import yfinance as yf

def main():
    ticker = yf.Ticker("TSLA")
    history = ticker.history(period="1d", interval="1m")
    if history.empty:
        raise RuntimeError("Yahoo Finance returned no Tesla price data.")
    latest = history.iloc[-1]
    print(f"Tesla (TSLA): ${latest['Close']:,.2f}")
    print(f"Timestamp: {history.index[-1]}")

if __name__ == "__main__":
    main()

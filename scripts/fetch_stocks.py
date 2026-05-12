import json
import datetime
import yfinance as yf

STOCKS = [
    ("AAPL",  "Apple Inc."),
    ("MSFT",  "Microsoft Corp."),
    ("NVDA",  "NVIDIA Corp."),
    ("AMZN",  "Amazon.com Inc."),
    ("GOOGL", "Alphabet Inc."),
    ("META",  "Meta Platforms Inc."),
    ("TSLA",  "Tesla Inc."),
    ("BRK-B", "Berkshire Hathaway"),
    ("LLY",   "Eli Lilly & Co."),
    ("JPM",   "JPMorgan Chase"),
]

def fetch():
    tickers = [t for t, _ in STOCKS]
    data = yf.download(tickers, period="2d", auto_adjust=True, progress=False)

    results = []
    for rank, (ticker, name) in enumerate(STOCKS, start=1):
        try:
            closes = data["Close"][ticker].dropna()
            if len(closes) < 2:
                raise ValueError("Not enough data")
            prev, curr = float(closes.iloc[-2]), float(closes.iloc[-1])
            pct = (curr - prev) / prev * 100
            sign = "+" if pct >= 0 else ""
            results.append({
                "rank": rank,
                "ticker": ticker,
                "name": name,
                "price": round(curr, 2),
                "change": f"{sign}{pct:.2f}%",
                "changePositive": pct >= 0,
            })
            print(f"  {ticker:6s}  ${curr:.2f}  {sign}{pct:.2f}%")
        except Exception as e:
            print(f"  {ticker:6s}  ERROR: {e}")

    today = datetime.date.today().isoformat()
    out = {"updated": today, "stocks": results}

    with open("data/stocks.json", "w") as f:
        json.dump(out, f, indent=2)

    print(f"\n✓ Wrote {len(results)} stocks to data/stocks.json ({today})")

if __name__ == "__main__":
    fetch()

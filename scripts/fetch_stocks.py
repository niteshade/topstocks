import json
import sys
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
    results = []
    errors = []

    for rank, (ticker, name) in enumerate(STOCKS, start=1):
        try:
            t = yf.Ticker(ticker)
            hist = t.history(period="5d")
            closes = hist["Close"].dropna()
            if len(closes) < 2:
                raise ValueError(f"only {len(closes)} trading day(s) returned")
            prev = float(closes.iloc[-2])
            curr = float(closes.iloc[-1])
            pct  = (curr - prev) / prev * 100
            sign = "+" if pct >= 0 else ""
            market_cap = t.info.get("marketCap") or None
            results.append({
                "rank": rank,
                "ticker": ticker,
                "name": name,
                "price": round(curr, 2),
                "change": f"{sign}{pct:.2f}%",
                "changePositive": pct >= 0,
                "marketCap": market_cap,
            })
            cap_str = f"  mktcap ${market_cap/1e12:.2f}T" if market_cap else ""
            print(f"  {ticker:6s}  ${curr:>9.2f}  {sign}{pct:.2f}%{cap_str}", flush=True)
        except Exception as exc:
            msg = f"{ticker}: {exc}"
            print(f"  ERROR  {msg}", flush=True)
            errors.append(msg)

    if errors:
        print(f"\n✗ {len(errors)} ticker(s) failed: {', '.join(errors)}", flush=True)
        sys.exit(1)

    today = datetime.date.today().isoformat()
    payload = {"updated": today, "stocks": results}
    with open("data/stocks.json", "w") as f:
        json.dump(payload, f, indent=2)
    print(f"\n✓ Wrote {len(results)} stocks → data/stocks.json  ({today})", flush=True)

if __name__ == "__main__":
    fetch()

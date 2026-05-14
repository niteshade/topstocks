import json
import sys
import datetime
from zoneinfo import ZoneInfo
import yfinance as yf

TICKERS = [
    ("NVDA",  "NVIDIA Corp."),
    ("GOOGL", "Alphabet Inc. (Class A)"),
    ("GOOG",  "Alphabet Inc. (Class C)"),
    ("AAPL",  "Apple Inc."),
    ("MSFT",  "Microsoft Corp."),
    ("AMZN",  "Amazon.com Inc."),
    ("AVGO",  "Broadcom Inc."),
    ("TSLA",  "Tesla Inc."),
    ("META",  "Meta Platforms Inc."),
    ("WMT",   "Walmart Inc."),
    ("BRK-B", "Berkshire Hathaway (B)"),
    ("BRK-A", "Berkshire Hathaway (A)"),
    ("LLY",   "Eli Lilly & Co."),
    ("MU",    "Micron Technology"),
    ("JPM",   "JPMorgan Chase"),
    ("AMD",   "Advanced Micro Devices"),
    ("XOM",   "Exxon Mobil Corp."),
    ("INTC",  "Intel Corp."),
    ("V",     "Visa Inc."),
    ("JNJ",   "Johnson & Johnson"),
]

THRESHOLD = 1_000_000_000_000  # $1 trillion

def fetch():
    et_now = datetime.datetime.now(ZoneInfo("America/New_York"))
    print(f"  Current ET time: {et_now.strftime('%H:%M %Z')}", flush=True)
    if et_now.hour < 16:
        print("  Market not closed yet — skipping run.", flush=True)
        sys.exit(0)

    qualified = []
    errors = []

    for ticker, name in TICKERS:
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

            if market_cap and market_cap >= THRESHOLD:
                qualified.append({
                    "ticker": ticker,
                    "name": name,
                    "price": round(curr, 2),
                    "change": f"{sign}{pct:.2f}%",
                    "changePositive": pct >= 0,
                    "marketCap": market_cap,
                })
                print(f"  ✓ {ticker:6s}  ${curr:>10.2f}  {sign}{pct:.2f}%  ${market_cap/1e12:.2f}T", flush=True)
            else:
                cap_str = f"${market_cap/1e9:.0f}B" if market_cap else "N/A"
                print(f"  – {ticker:6s}  below threshold ({cap_str})", flush=True)

        except Exception as exc:
            msg = f"{ticker}: {exc}"
            print(f"  ERROR  {msg}", flush=True)
            errors.append(msg)

    if errors:
        print(f"\n✗ {len(errors)} ticker(s) failed: {', '.join(errors)}", flush=True)
        sys.exit(1)

    # Sort by market cap descending and assign ranks
    qualified.sort(key=lambda s: s["marketCap"], reverse=True)
    for i, s in enumerate(qualified, start=1):
        s["rank"] = i

    today = datetime.date.today().isoformat()
    payload = {"updated": today, "stocks": qualified}
    with open("data/stocks.json", "w") as f:
        json.dump(payload, f, indent=2)
    print(f"\n✓ {len(qualified)}/{len(TICKERS)} stocks above $1T → data/stocks.json  ({today})", flush=True)

if __name__ == "__main__":
    fetch()

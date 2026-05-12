# top10stocks

Static site showing the top 10 US stocks by market cap with daily closing prices and % change. No API key required.

**Live at:** `https://niteshade.github.io/top10stocks`

---

## Stack

| Layer | Tool |
|---|---|
| Hosting | GitHub Pages |
| DNS | Cloudflare (optional custom domain) |
| Data pipeline | GitHub Actions + Python + yfinance |
| Schedule | Weekdays at 9:30 PM UTC (5:30 PM ET) |

---

## File structure

```
top10stocks/
├── index.html                   # the site — reads from data/stocks.json
├── data/stocks.json             # updated daily by the Action
├── scripts/fetch_stocks.py      # fetches prices via yfinance, writes stocks.json
└── .github/workflows/update.yml # cron job, runs Mon–Fri after market close
```

---

## Setup

### 1. Enable GitHub Pages

**Settings → Pages → Source → Deploy from branch → `main` / `/ (root)`**

The site will be live at `https://<your-username>.github.io/top10stocks`.

### 2. Trigger the first data fetch

The cron only fires on weekdays. To populate the data immediately:

**Actions → Update Stock Data → Run workflow**

### 3. Custom domain via Cloudflare (optional)

Add a DNS record in Cloudflare:

| Type | Name | Content | Proxy status |
|---|---|---|---|
| CNAME | `@` (or subdomain) | `niteshade.github.io` | **DNS only** (grey cloud) |

> The proxy must be off — GitHub Pages handles TLS itself and won't provision a cert through Cloudflare's proxy.

Then add a `CNAME` file to the repo root containing just your domain:

```
stocks.yourdomain.com
```

And set the custom domain in **Settings → Pages → Custom domain**.

---

## How the data pipeline works

`scripts/fetch_stocks.py` runs inside GitHub Actions on a weekday cron. It fetches the last 5 trading days of history for each ticker via `yfinance`, computes the daily % change between the two most recent closes, and writes `data/stocks.json`. The Action then commits and pushes that file back to `main`, which triggers a Pages redeploy.

Using 5 days of history (instead of 2) ensures the script always has at least 2 data points even after long weekends or market holidays.

If any ticker fails to return data the script exits with a non-zero code, turning the Action red — so failures are visible rather than silently writing bad data.

---

## Manual update

**Actions → Update Stock Data → Run workflow**

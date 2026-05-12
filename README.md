# top10stocks

A simple static site showing the top 10 US stocks by market cap, updated once daily after market close.

**Stack:** GitHub Pages + Cloudflare DNS + GitHub Actions + Anthropic API (web search)

---

## Setup

### 1. Enable GitHub Pages

In your repo: **Settings → Pages → Source → Deploy from branch → `main` / `/ (root)`**

Your site will be live at `https://yourusername.github.io/top10stocks`

### 2. Add your Anthropic API key

In your repo: **Settings → Secrets and variables → Actions → New repository secret**

- Name: `ANTHROPIC_API_KEY`
- Value: your key from [console.anthropic.com](https://console.anthropic.com)

### 3. Point Cloudflare to GitHub Pages

In Cloudflare DNS, add:

| Type  | Name       | Content                          | Proxy |
|-------|------------|----------------------------------|-------|
| CNAME | `@` or subdomain | `yourusername.github.io` | **DNS only** (grey cloud) |

Then in your repo add a file called `CNAME` containing just your domain, e.g.:
```
stocks.yourdomain.com
```

In GitHub Pages settings, set your custom domain to match.

### 4. Trigger the first data fetch

Go to **Actions → Update Stock Data → Run workflow** to populate `data/stocks.json` immediately without waiting for the nightly cron.

---

## How it works

- `index.html` — static page, reads from `data/stocks.json`
- `data/stocks.json` — pre-built data file, committed by the Action
- `scripts/fetch-stocks.js` — calls Anthropic API with web search to get closing prices
- `.github/workflows/update.yml` — runs Mon–Fri at 9:30 PM UTC (5:30 PM ET)

## Manual update

From the Actions tab, click **"Run workflow"** on the Update Stock Data workflow anytime.

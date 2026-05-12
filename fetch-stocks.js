const fs = require("fs");
const path = require("path");

const PROMPT = `Search the web for today's closing prices of the top 10 US stocks by market capitalization.
Return ONLY a raw JSON array — no markdown, no explanation, no backticks. Example format:
[
  {
    "rank": 1,
    "ticker": "AAPL",
    "name": "Apple Inc.",
    "price": 213.45,
    "change": "+1.23%",
    "changePositive": true
  }
]
Use today's end-of-day closing prices. If the market was closed today, use the most recent closing prices. Return exactly 10 entries.`;

async function fetchStocks() {
  const res = await fetch("https://api.anthropic.com/v1/messages", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "x-api-key": process.env.ANTHROPIC_API_KEY,
      "anthropic-version": "2023-06-01",
    },
    body: JSON.stringify({
      model: "claude-sonnet-4-20250514",
      max_tokens: 1000,
      tools: [{ type: "web_search_20250305", name: "web_search" }],
      messages: [{ role: "user", content: PROMPT }],
    }),
  });

  if (!res.ok) {
    const err = await res.text();
    throw new Error(`API error ${res.status}: ${err}`);
  }

  const data = await res.json();
  const textBlock = data.content?.find((b) => b.type === "text");
  const raw = textBlock?.text || "";

  const clean = raw.replace(/```json|```/gi, "").trim();
  const start = clean.indexOf("[");
  const end = clean.lastIndexOf("]");
  if (start === -1 || end === -1) throw new Error("No JSON array found in response");

  const stocks = JSON.parse(clean.slice(start, end + 1));
  if (!Array.isArray(stocks) || stocks.length === 0) throw new Error("Empty or invalid stocks array");

  const today = new Date().toISOString().split("T")[0];
  const output = { updated: today, stocks };

  const outPath = path.join(__dirname, "../data/stocks.json");
  fs.writeFileSync(outPath, JSON.stringify(output, null, 2));
  console.log(`✓ Wrote ${stocks.length} stocks to data/stocks.json (${today})`);
}

fetchStocks().catch((err) => {
  console.error("✗ Failed to fetch stocks:", err.message);
  process.exit(1);
});

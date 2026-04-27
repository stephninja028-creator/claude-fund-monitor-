# claude-fund-monitor

A Claude Code skill that monitors Chinese fund portfolio changes (调仓) and sends WeChat push notifications via Server酱 when holdings change.

## What it does

- Monitors top-10 holdings of any A-share / QDII fund daily
- Detects rebalancing (新进/移出 stock codes)
- Pushes WeChat notification only when changes are detected
- Silent when no changes — no noise

## Installation

```bash
# Clone the repo
git clone https://github.com/stephninja028-creator/claude-fund-monitor-
cd claude-fund-monitor-

# Run setup wizard
python3 scripts/setup.py
```

The setup wizard will:
1. Ask for your fund codes (6-digit, found in Alipay fund detail page)
2. Ask for your Server酱 SendKey (get it at sct.ftqq.com)
3. Set up a daily cron job automatically

## Commands

```bash
# First-time setup
python3 scripts/setup.py

# Run a manual check right now
python3 scripts/monitor.py

# View current holdings snapshot
python3 scripts/snapshot.py
```

## Requirements

- macOS or Linux
- Python 3.8+
- `requests` library (auto-installed by setup.py)
- Server酱 account (free) for WeChat push notifications

## How it works

Holdings data is fetched from 天天基金网 (eastmoney.com) `pingzhongdata` API, which reflects the fund's latest disclosed top-10 stock positions. When the set of stock codes changes between runs, a WeChat notification is sent.

**Note:** ETF index funds and FOF funds may show empty stock holdings — this is expected, as they track indices or hold other funds rather than individual stocks.

## Data source

天天基金网 (eastmoney.com) — no API key required.

## Push notifications

Powered by [Server酱](https://sct.ftqq.com) — a free WeChat push service. Sign up with WeChat scan, get a SendKey, done.

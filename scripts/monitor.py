#!/usr/bin/env python3
"""
基金调仓监控核心脚本
数据来源：天天基金网 (eastmoney.com)
推送方式：Server酱 (sct.ftqq.com)
"""

import json
import os
import re
import time
import requests
from datetime import datetime
from pathlib import Path

CONFIG_FILE = Path(__file__).parent.parent / "config.json"
STATE_FILE  = Path(__file__).parent.parent / "fund_state.json"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36",
    "Referer": "https://fund.eastmoney.com/",
}


def load_config():
    if not CONFIG_FILE.exists():
        print("❌ 未找到配置文件，请先运行 setup.py")
        exit(1)
    return json.loads(CONFIG_FILE.read_text(encoding="utf-8"))


def load_state():
    if STATE_FILE.exists():
        try:
            return json.loads(STATE_FILE.read_text(encoding="utf-8"))
        except Exception:
            return {}
    return {}


def save_state(state):
    STATE_FILE.write_text(
        json.dumps(state, ensure_ascii=False, indent=2), encoding="utf-8"
    )


def fetch_holdings(code):
    url = f"http://fund.eastmoney.com/pingzhongdata/{code}.js"
    try:
        r = requests.get(url, headers=HEADERS, timeout=15)
        r.raise_for_status()
        m = re.search(r'var stockCodes\s*=\s*(\[[^\]]*\])', r.text)
        return json.loads(m.group(1)) if m else []
    except Exception as e:
        print(f"  ⚠️  [{code}] 获取失败: {e}")
        return []


def push_wechat(key, changes_map):
    title = f"基金调仓提醒 · {len(changes_map)} 只 · {datetime.now().strftime('%Y-%m-%d')}"
    lines = []
    for fund_name, items in changes_map.items():
        lines.append(f"**{fund_name}**")
        for item in items:
            lines.append(f"- {item}")
        lines.append("")
    lines += ["---", "数据来源：天天基金网 · 仅供参考"]

    r = requests.post(
        f"https://sctapi.ftqq.com/{key}.send",
        data={"title": title, "desp": "\n".join(lines)},
        timeout=10,
    )
    result = r.json()
    if result.get("code") == 0:
        print("✅ 微信推送成功")
    else:
        print(f"⚠️  推送失败: {result}")


def main():
    config = load_config()
    funds  = config.get("funds", {})
    key    = config.get("serverchan_key", "")

    print(f"\n{'='*52}")
    print(f"基金调仓监控  {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print(f"监控基金数量：{len(funds)}")
    print(f"{'='*52}")

    state = load_state()
    is_first_run = len(state) == 0
    changes_map = {}

    for code, name in funds.items():
        print(f"\n  [{code}] {name}")
        holdings = fetch_holdings(code)
        new_codes = set(holdings)
        old_codes = set(state.get(code, {}).get("stock_codes", []))

        changes = []
        if old_codes and new_codes:
            added   = new_codes - old_codes
            removed = old_codes - new_codes
            if added:
                changes.append(f"➕ 新进：{', '.join(sorted(added))}")
            if removed:
                changes.append(f"➖ 移出：{', '.join(sorted(removed))}")

        if changes:
            changes_map[name] = changes
            for c in changes:
                print(f"    → {c}")
        else:
            print(f"    → 无变动")

        state.setdefault(code, {}).update({
            "stock_codes": list(new_codes),
            "updated_at": datetime.now().isoformat()[:16],
        })
        time.sleep(0.8)

    save_state(state)

    print(f"\n{'='*52}")
    if is_first_run:
        print("✅ 首次运行完成：已记录持仓快照，下次运行开始对比。")
    elif changes_map:
        push_wechat(key, changes_map)
        print(f"共 {len(changes_map)} 只基金有调仓。")
    else:
        print("✅ 无调仓，不推送。")


if __name__ == "__main__":
    main()

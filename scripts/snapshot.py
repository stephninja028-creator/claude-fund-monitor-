#!/usr/bin/env python3
"""
查看当前监控的基金持仓快照
"""

import json
from datetime import datetime
from pathlib import Path

CONFIG_FILE = Path(__file__).parent.parent / "config.json"
STATE_FILE  = Path(__file__).parent.parent / "fund_state.json"


def main():
    if not CONFIG_FILE.exists():
        print("❌ 未找到配置文件，请先运行 setup.py")
        return

    config = json.loads(CONFIG_FILE.read_text(encoding="utf-8"))
    funds  = config.get("funds", {})

    if not STATE_FILE.exists():
        print("❌ 未找到持仓快照，请先运行 monitor.py 一次")
        return

    state = json.loads(STATE_FILE.read_text(encoding="utf-8"))

    print(f"\n{'='*52}")
    print(f"  基金持仓快照  {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print(f"{'='*52}")

    for code, name in funds.items():
        fund_state = state.get(code, {})
        codes = fund_state.get("stock_codes", [])
        updated = fund_state.get("updated_at", "未知")
        print(f"\n📊 {name} ({code})")
        print(f"   最后更新：{updated}")
        if codes:
            print(f"   十大持仓代码：{', '.join(codes)}")
        else:
            print(f"   持仓数据：暂无（ETF/FOF 类基金可能无股票持仓）")

    print(f"\n{'='*52}\n")


if __name__ == "__main__":
    main()

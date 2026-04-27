#!/usr/bin/env python3
"""
基金调仓监控 - 初始化配置向导
"""

import json
import subprocess
import sys
from pathlib import Path

CONFIG_FILE = Path(__file__).parent.parent / "config.json"


def check_dependencies():
    try:
        import requests
    except ImportError:
        print("正在安装依赖...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "requests", "-q"])
        print("✅ 依赖安装完成")


def input_funds():
    print("\n📋 请输入你持有的基金代码（6位数字，每行一个，输入空行结束）：")
    print("   示例：007722")
    print("   基金代码可在支付宝基金详情页找到\n")

    funds = {}
    while True:
        code = input("基金代码：").strip()
        if not code:
            break
        if not code.isdigit() or len(code) != 6:
            print("   ⚠️  格式不对，请输入6位数字")
            continue
        name = input(f"基金名称（可选，直接回车跳过）：").strip()
        if not name:
            name = f"基金{code}"
        funds[code] = name
        print(f"   ✅ 已添加：{name} ({code})\n")

    return funds


def input_serverchan_key():
    print("\n🔑 请输入 Server酱 SendKey：")
    print("   获取方式：打开 sct.ftqq.com，微信扫码登录，复制 SendKey\n")
    key = input("SendKey：").strip()
    return key


def setup_cron(script_path):
    print("\n⏰ 设置每天自动运行时间（24小时制，默认 09:00）：")
    hour = input("小时 [9]：").strip() or "9"
    minute = input("分钟 [0]：").strip() or "0"

    cron_line = (
        f"{minute} {hour} * * * "
        f"/usr/bin/python3 {script_path} "
        f">> {script_path.parent.parent}/monitor.log 2>&1"
    )

    result = subprocess.run("crontab -l", shell=True, capture_output=True, text=True)
    existing = result.stdout if result.returncode == 0 else ""

    if str(script_path) in existing:
        print("   ℹ️  cron 已存在，跳过")
        return

    new_crontab = existing.rstrip() + "\n" + cron_line + "\n"
    subprocess.run(f'echo "{new_crontab}" | crontab -', shell=True)
    print(f"   ✅ 已设置每天 {hour}:{minute.zfill(2)} 自动运行")


def main():
    print("=" * 52)
    print("  基金调仓监控 Agent — 初始化配置")
    print("=" * 52)

    check_dependencies()

    funds = input_funds()
    if not funds:
        print("❌ 未添加任何基金，退出")
        return

    key = input_serverchan_key()
    if not key:
        print("❌ 未输入 SendKey，退出")
        return

    config = {"funds": funds, "serverchan_key": key}
    CONFIG_FILE.write_text(
        json.dumps(config, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    print(f"\n✅ 配置已保存：{CONFIG_FILE}")

    monitor_script = Path(__file__).parent / "monitor.py"
    setup_cron(monitor_script)

    print("\n" + "=" * 52)
    print("✅ 配置完成！")
    print(f"   已添加 {len(funds)} 只基金")
    print("   运行 python3 scripts/monitor.py 立即检查一次")
    print("=" * 52)


if __name__ == "__main__":
    main()

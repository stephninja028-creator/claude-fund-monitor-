# fund-rebalance-monitor

**基金调仓监控** — 自动监控你持有的基金十大持仓变化，有调仓立即推送微信通知。

> 支付宝买基金，基金经理偷偷调仓你不知道？这个工具帮你盯着。

---

## 功能

- 监控任意数量的 A 股 / QDII 基金
- 每天自动检查十大重仓股票代码变化
- **只在发现调仓时推送微信通知**，无变动静默
- 命令行管理基金列表，无需改代码

---

## 安装前准备

你需要准备两样东西：

**1. 基金代码**
在支付宝 → 我的基金 → 点开某只基金 → 详情页可以找到 6 位基金代码。

**2. Server酱 SendKey（免费）**
[Server酱](https://sct.ftqq.com) 是一个微信推送服务：
1. 打开 sct.ftqq.com
2. 用微信扫码登录
3. 关注提示的公众号
4. 复制首页的 **SendKey**

---

## 安装

```bash
# 1. 克隆项目
git clone https://github.com/stephninja028-creator/fund-rebalance-monitor
cd fund-rebalance-monitor

# 2. 安装依赖
pip3 install requests

# 3. 初始化配置
cp config.example.json config.json
# 编辑 config.json，填入你的基金代码和 SendKey
```

---

## 配置

编辑 `config.json`：

```json
{
  "funds": {
    "000001": "基金名称A",
    "000002": "基金名称B"
  },
  "serverchan_key": "你的SendKey"
}
```

---

## 使用

```bash
# 查看当前监控的基金列表
python3 fund_monitor.py --list

# 添加基金
python3 fund_monitor.py --add 000001 "基金名称"

# 删除基金
python3 fund_monitor.py --remove 000001

# 手动立即检查一次
python3 fund_monitor.py
```

---

## 设置每日自动运行

```bash
# 打开 cron 编辑器
crontab -e

# 添加以下一行（每天 09:00 运行）
0 9 * * * /usr/bin/python3 /你的路径/fund_monitor.py >> /你的路径/monitor.log 2>&1
```

---

## 运行效果

**无调仓时（静默）：**
```
====================================================
基金调仓监控  2026-04-25 09:00
监控基金数量：5
====================================================
  [000001] 基金名称A  → 无变动
  [000002] 基金名称B  → 无变动
  ...
✅ 所有基金无调仓，不推送。
```

**发现调仓时（推送微信）：**
```
  [000001] 基金名称A
    → ➕ 新进：XXXXXXX, XXXXXXX
    → ➖ 移出：XXXXXXX, XXXXXXX
✅ 微信推送成功
```

微信收到的消息：

> **基金调仓提醒 · 1 只 · 2026-04-25**
>
> **基金名称A**
> - ➕ 新进：XXXXXXX, XXXXXXX
> - ➖ 移出：XXXXXXX, XXXXXXX

---

## 工作原理

数据来源：[天天基金网](https://fund.eastmoney.com) `pingzhongdata` 接口，实时反映基金最新披露的十大重仓股票代码。两次运行之间代码集合发生变化，即判定为调仓。

**注意：** ETF 指数基金和 FOF 基金持仓可能显示为空，属于正常现象——它们跟踪指数或持有其他基金，没有直接的股票持仓数据。

---

## 系统要求

- macOS 或 Linux
- Python 3.8+
- `requests` 库

---

## 文件说明

```
fund-rebalance-monitor/
├── fund_monitor.py       # 主脚本
├── config.json           # 你的配置（不会上传 GitHub）
├── config.example.json   # 配置模板
├── fund_state.json       # 持仓状态存档（自动生成）
└── monitor.log           # 运行日志（自动生成）
```

---

## 免责声明

本工具数据来源于天天基金网公开数据，仅供参考，不构成投资建议。

---

Made with Claude Code

# financial-expert

> [中文版 / Chinese →](README.zh.md)

Financial data analysis skill powered by **Alibaba Cloud Model Studio MCP** (`bl mcp` + `market-cmapi00073529`) — covering China A-share stocks, mutual funds, bonds, macro indicators, broker research reports, and listed-company filings.

## What it does

Ask your agent financial questions in natural language, and this skill will:

1. **Parse your intent** — identify the target (stock / fund / industry), filters (ROE > 15%, growth > 30%), and data type
2. **Route to the right tool** — stock screening, fund screening, fund manager screening, financial data query, macro/industry time-series, research reports, or company announcements
3. **Call the MCP service** — `bl mcp call market-cmapi00073529.<Tool> --query "..."` and return structured results
4. **Present the data** — formatted tables, charts, or summaries ready for analysis

## When to use

| Scenario | Example |
|----------|---------|
| Stock screening | "Find consumption stocks with ROE > 15% and net profit growth > 30%" |
| Fund screening | "Low-risk bond funds with 3-year annualized return above 5%" |
| Fund manager screening | "Managers with AUM > 10B and top-quartile performance" |
| Financial data | "Kweichow Moutai's net profit for the past 3 years" |
| Macro / industry data | "China GDP quarterly growth for 2023–2025" |
| Research reports | "Latest broker reports on the new energy vehicle sector" |
| Company filings | "PetroChina's recent major-event announcements" |

**Not for this skill:**
- Non-China markets (US stocks, crypto, forex)
- Real-time trading / order execution
- Investment advice — data only, decisions are yours

## Quick examples

```bash
# Stock screening
bl mcp call market-cmapi00073529.SmartStockSelection \
  --query "筛选净利润增速超过 30% 且 ROE 大于 15% 的消费股"

# Fund screening
bl mcp call market-cmapi00073529.SmartFundSelection \
  --query "近三年年化收益超过 10% 的股票型基金"

# Financial data
bl mcp call market-cmapi00073529.FinQuery \
  --query "贵州茅台 2024 年净利润和营收"

# Macro data
bl mcp call market-cmapi00073529.MacroIndustryData \
  --query "2023-2025 中国季度 GDP 增速"

# Research reports
bl mcp call market-cmapi00073529.FinancialResearchReport \
  --query "新能源汽车行业最新券商研报"
```

## Prerequisites

This skill requires Alibaba Cloud Model Studio CLI (`bl`). Before using this skill, check if `bl` is installed:

```bash
bl --version
```

If not installed or the command is not found, follow the install guide:

> https://bailian.aliyun.com/cli/install.md

Also log in to the Bailian console:

```bash
bl auth login --console
```

## Available tools

| Tool | Purpose |
|------|---------|
| `SmartStockSelection` | Multi-dimension A-share stock screening |
| `SmartFundSelection` | Fund screening by performance, risk, holdings, type |
| `SmartFundManagerSelection` | Fund manager screening by AUM, style, track record |
| `FinQuery` | Structured financial data (income, valuation, quotes) |
| `MacroIndustryData` | Macro & industry time-series (GDP, CPI, production) |
| `FinancialResearchReport` | Broker research report search |
| `AnnouncementData` | Listed-company filing / announcement search |

## License

Apache-2.0

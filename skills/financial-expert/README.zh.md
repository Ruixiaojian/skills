# 金融数据分析

> [English →](README.md)

基于**阿里云百炼 MCP**（`bl mcp` + `market-cmapi00073529`）的金融数据分析技能 — 覆盖中国 A 股、基金、债券、宏观指标、券商研报与上市公司公告。

## 功能简介

用自然语言向 Agent 提出金融问题，本技能会：

1. **解析意图** — 识别标的（股票 / 基金 / 行业）、筛选条件（ROE > 15%、增速 > 30%）和数据类型
2. **路由工具** — 选股、基金筛选、基金经理筛选、财务数据、宏观/行业时序、研报、公告
3. **调用 MCP 服务** — `bl mcp call market-cmapi00073529.<工具> --query "..."` 返回结构化结果
4. **呈现数据** — 格式化的表格、图表或摘要，方便分析

## 适用场景

| 场景 | 示例 |
|------|------|
| 选股 | "筛选 ROE > 15% 且净利润增速 > 30% 的消费股" |
| 基金筛选 | "低风险债券基金，近三年年化 > 5%" |
| 基金经理筛选 | "管理规模超百亿、业绩排名前 25% 的经理" |
| 财务数据 | "贵州茅台近三年净利润" |
| 宏观/行业数据 | "2023–2025 中国季度 GDP 增速" |
| 券商研报 | "新能源汽车行业最新研报" |
| 公司公告 | "中国石油最近的重大事项公告" |

**不适用：**
- 非中国市场（美股、港股、加密货币）
- 实时交易 / 下单
- 投资建议 — 仅提供数据，决策由你做

## 快速示例

```bash
# 选股
bl mcp call market-cmapi00073529.SmartStockSelection \
  --query "筛选净利润增速超过 30% 且 ROE 大于 15% 的消费股"

# 基金筛选
bl mcp call market-cmapi00073529.SmartFundSelection \
  --query "近三年年化收益超过 10% 的股票型基金"

# 财务数据
bl mcp call market-cmapi00073529.FinQuery \
  --query "贵州茅台 2024 年净利润和营收"

# 宏观数据
bl mcp call market-cmapi00073529.MacroIndustryData \
  --query "2023-2025 中国季度 GDP 增速"

# 券商研报
bl mcp call market-cmapi00073529.FinancialResearchReport \
  --query "新能源汽车行业最新券商研报"
```

## 前置要求

本技能依赖阿里云百炼 CLI（`bl`）。在使用本技能前，请先检查 `bl` 是否已安装：

```bash
bl --version
```

如果未安装或命令不存在，请阅读以下安装文档并按照说明完成安装：

> https://bailian.aliyun.com/cli/install.md

此外还需登录百炼控制台：

```bash
bl auth login --console
```

## 可用工具

| 工具 | 用途 |
|------|------|
| `SmartStockSelection` | 多维度 A 股选股 |
| `SmartFundSelection` | 按业绩、风险、持仓、类型筛选基金 |
| `SmartFundManagerSelection` | 按管理规模、风格、业绩筛选基金经理 |
| `FinQuery` | 结构化财务数据（利润、估值、行情） |
| `MacroIndustryData` | 宏观与行业时序数据（GDP、CPI、产销价） |
| `FinancialResearchReport` | 券商研报检索 |
| `AnnouncementData` | 上市公司公告检索 |

## License

Apache-2.0

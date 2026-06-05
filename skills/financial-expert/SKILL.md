---
name: financial-expert
description: >-
  金融数据分析技能（基于 `bl mcp` + 阿里云百炼 MCP 市场 `market-cmapi00073529`），
  覆盖中国 A 股、基金、债券等金融标的。支持股票筛选、基金筛选、基金经理筛选、
  财务数据查询（净利润 / 营收 / ROE 等）、宏观与行业时序数据（GDP / CPI / 产销价）、
  券商研报检索、A 股上市公司公告检索。当用户问及以下关键词时务必激活：
  选股 / 股票筛选、基金筛选、基金经理筛选、财务数据 / 净利润 / 营收 / 估值、
  宏观经济 / GDP / CPI、行业产量销量价格、券商研报 / 行业研报、上市公司公告。
  不适用于：通用编程问题、非金融数据、非中国市场标的。
---

# 前置依赖：阿里云百炼 CLI

本技能依赖阿里云百炼 CLI（`bl`）。在使用本技能前，请先检查 `bl` 是否已安装：

```bash
bl --version
```

如果未安装或命令不存在，请阅读以下安装文档并按照说明为用户完成安装：

> https://bailian.aliyun.com/cli/install.md

---

# 金融数据分析 Skill

> 基于 `bl mcp` 调用阿里云百炼 MCP 市场金融数据服务（`market-cmapi00073529`），
> 提供股票 / 基金 / 基金经理筛选、财务与宏观数据查询、研报与公告检索的端到端能力。
> `bl` 内置 MCP 客户端，复用 `DASHSCOPE_API_KEY`,无需额外注册服务。

## 何时使用

满足以下任一条件时激活：

- **股票相关**：选股、股票筛选、A 股财务指标筛选、行业 / 概念股查询
- **基金相关**：基金筛选、按业绩 / 风险 / 持仓 / 类型筛选基金
- **基金经理相关**：按管理规模 / 业绩 / 风格筛选基金经理
- **结构化金融数据**：净利润、营业收入、ROE、市盈率、行情快照、舆情、工商信息
- **宏观 / 行业数据**：GDP、CPI、PPI、行业产量 / 销量 / 价格时序
- **券商研报**：分析师观点、行业格局、公司发展、市场趋势叙述
- **公司公告**:A 股上市公司公告原文（财务、重大事项、权益分派、关联交易）

## 何时**不要**使用

- 非中国市场标的（美股、港股、加密货币等）
- 通用编程 / 框架问题
- 实时行情下单 / 交易接口（本技能仅提供数据查询，不下单）
- 投资建议或荐股 — 仅返回数据，由用户自行决策

## 前置条件

### 1. 安装 `bailian-cli`

```bash
npm install -g bailian-cli
bl --version
```

如果用户尚未安装,引导其访问 https://bailian.aliyun.com/cli/install.md

### 2. 配置百炼 API Key

```bash
# 方式 A：环境变量（推荐）
export DASHSCOPE_API_KEY=sk-你的APIKey

# 方式 B：bl auth
bl auth login --api-key sk-你的APIKey

# 验证
bl auth status
```

获取 API Key:https://bailian.console.aliyun.com/cli?source_channel=key_github&

**注意**：用户已有 `DASHSCOPE_API_KEY` 则跳过配置。仅当 `bl auth status` 显示未登录或调用失败时再询问 Key。

### 3. 确认 MCP 服务可用

```bash
# 在用户百炼账号下查看已激活的 MCP 服务
bl mcp list --name 金融

# 查看具体服务暴露的工具
bl mcp tools market-cmapi00073529
```

如 `bl mcp list` 中没有目标服务，引导用户去百炼控制台「MCP 市场」激活
`market-cmapi00073529`（金融数据分析）。

## 工作流程

### 第一步：解析用户

从用户输入中提取：

- **目标标的** — 具体股票 / 基金名称或品类（如「贵州茅台」「消费板块」「股票型基金」）
- **筛选条件** — 财务指标、业绩阈值、行业筛选、时间窗口等
- **数据类型** — 结构化（财务 / 行情）、时序（宏观）、非结构化（研报 / 公告）
- **时间范围** — 数据或研报的历史区间

### 第二步：选择工具

| 用户意图 | 工具 | 类别 |
|---|---|---|
| 「筛选...股票」「选股」 | `SmartStockSelection` | 候选清单 |
| 「筛选...基金」 | `SmartFundSelection` | 候选清单 |
| 「筛选...基金经理」 | `SmartFundManagerSelection` | 候选清单 |
| 「查 X 公司 / 基金的财务 / 行情 / 估值」 | `FinQuery` | 结构化数据 |
| 「查 GDP / CPI / 行业产销 / 价格走势」 | `MacroIndustryData` | 时序数据 |
| 「找 X 行业 / 公司的券商研报」 | `FinancialResearchReport` | 非结构化研报 |
| 「查 X 公司公告」 | `AnnouncementData` | 非结构化公告 |

### 第三步:调用 `bl mcp call`

所有金融工具都挂在 `market-cmapi00073529` 这一个 MCP server 下,
调用格式统一为：

```bash
bl mcp call market-cmapi00073529.<ToolName> --query "<自然语言查询>"
```

也支持结构化入参:

```bash
# 完整 JSON 入参
bl mcp call market-cmapi00073529.SmartStockSelection \
  --json '{"query":"消费板块","filters":{"roe":">15"}}'

# 多个 K=V（值自动尝试解析为 JSON）
bl mcp call market-cmapi00073529.SmartFundSelection \
  --arg riskLevel=R3 --arg minScale=10
```

输出 JSON 用于 Agent 解析:

```bash
bl mcp call market-cmapi00073529.FinQuery --query "贵州茅台 2024 年净利润" --output json
```

## 工具参考

每个工具的入参 schema 可通过 `bl mcp tools market-cmapi00073529 --output json` 查询。
下面给出**典型调用示例**，所有工具默认接收自然语言 `--query`。

### 1. 股票筛选 — `SmartStockSelection`

按财务、行情、技术、行业 / 概念等多维条件筛选股票。仅返回候选名单，不返回详情。

```bash
bl mcp call market-cmapi00073529.SmartStockSelection \
  --query "筛选净利润增速超过 30% 且 ROE 大于 15% 的消费股"
```

### 2. 基金筛选 — `SmartFundSelection`

按业绩、风险、持仓、基金经理、类型等条件筛选基金。

```bash
bl mcp call market-cmapi00073529.SmartFundSelection \
  --query "筛选近一年收益率排名前 10% 的股票型基金"
```

### 3. 基金经理筛选 — `SmartFundManagerSelection`

按管理规模、业绩、风险控制、投资风格等条件筛选基金经理。

```bash
bl mcp call market-cmapi00073529.SmartFundManagerSelection \
  --query "筛选管理规模超过 100 亿且年化收益超过 15% 的基金经理"
```

### 4. 金融数据查询 — `FinQuery`

查询股票 / 基金 / 债券基本资料、财务数据、行情快照、估值指标等**结构化数据**。
也支持舆情、工商数据。返回表格或叙述文本。

```bash
bl mcp call market-cmapi00073529.FinQuery \
  --query "查询贵州茅台 2020 年至今的净利润数据"
```

### 5. 宏观行业数据 — `MacroIndustryData`

查询宏观经济(GDP、CPI)或行业经济(产量、销量、价格)的**时序数据**。

```bash
bl mcp call market-cmapi00073529.MacroIndustryData \
  --query "查询近五年中国 GDP 同比增速数据"
```

### 6. 研报查询 — `FinancialResearchReport`

检索券商研报中的分析师观点、行业格局判断、公司发展历程、市场趋势叙述等**非结构化内容**。

```bash
bl mcp call market-cmapi00073529.FinancialResearchReport \
  --query "查找最近三个月关于新能源汽车行业的券商研报"
```

### 7. 公告检索 — `AnnouncementData`

检索 A 股上市公司公告原文：财务公告、重大事项、权益分派、关联交易等。

```bash
bl mcp call market-cmapi00073529.AnnouncementData \
  --query "查询贵州茅台 2024 年年度股东大会决议公告"
```

## 输出呈现规范

向用户展示结果时遵循以下结构:

- **筛选类**(股票 / 基金 / 经理)：表格展示，含名称、代码、关键指标值
- **`FinQuery` 结构化数据**:表格展示，列标题需含单位（万元 / %  / 倍 / 元等）
- **`MacroIndustryData` 时序**:时序表格 + 一句话趋势摘要（同比 / 环比方向）
- **`FinancialResearchReport` 研报**:研报标题 + 发布日期 + 券商 + 核心观点摘要（不超过 3 条）
- **`AnnouncementData` 公告**：公告标题 + 发布日期 + 公司名称 + 相关原文片段

**强约束:**

- 始终注明**数据来源**(百炼 MCP 市场 / market-cmapi00073529)和**查询时间**(`date` 命令)。
- 若工具返回为空，**不要编造**数据；建议用户放宽筛选条件或调整关键词后重试。
- 涉及金额、比例时保留原始精度,不要四舍五入到无意义的位数。
- 不要给出投资建议；可总结数据特征，但不得说「建议买入 / 卖出」。

## 错误处理

| 错误现象 | 排查思路 |
|---|---|
| `BailianGateway.Login.NotLogined` / 401 | API Key 缺失或失效 → `bl auth login --api-key sk-...` |
| `bl mcp list` 找不到 `market-cmapi00073529` | 用户未在百炼控制台「MCP 市场」激活该服务,引导其激活 |
| `bl mcp tools` 报 connection 错误 | 检查网络 / 区域(默认 `cn-beijing`);可加 `--region us` 或 `--base-url` 覆盖 |
| 工具返回 `isError: true` | 读取 `result.content[].text` 中的错误描述,常见原因:query 太宽 / 缺少必填实体名 |
| 无返回结果 | 放宽筛选条件、确认实体名称(全称 / 简称 / 代码)是否准确 |

## 完整端到端示例

用户问：「**帮我筛选 ROE > 15% 且近三年净利润复合增速 > 20% 的消费股，再查一下排名前 3 的公司最近的研报观点。**」

```bash
# Step 1: 候选筛选
bl mcp call market-cmapi00073529.SmartStockSelection \
  --query "ROE 大于 15%，近三年净利润复合增速大于 20% 的消费股" \
  --output json

# 假设返回 top 3：贵州茅台、五粮液、伊利股份

# Step 2: 分别拉取最新研报
bl mcp call market-cmapi00073529.FinancialResearchReport \
  --query "贵州茅台近一个月券商研报核心观点"

bl mcp call market-cmapi00073529.FinancialResearchReport \
  --query "五粮液近一个月券商研报核心观点"

bl mcp call market-cmapi00073529.FinancialResearchReport \
  --query "伊利股份近一个月券商研报核心观点"
```

汇总为表格 + 每家 3 条要点 + 数据来源 + 查询时间。

## 与 `bailian-cli` skill 的协同

- 本 skill 专注**金融 MCP 工具调用**;不要在这里调用 `bl text chat` / `bl image` 等。
- 若用户拿到金融数据后想**写研报 / 出图 / 出 PPT**:
  - 文本撰写 → 转给 `bailian-cli` 用 `bl text chat`
  - 可视化图表生成 → 转给 `bailian-cli` 用 `bl image generate`
  - 配音播报 → 转给 `bailian-cli` 用 `bl speech synthesize`

## 备注

- 本 skill 依赖的 `bl mcp` 子命令(`list` / `tools` / `call`)由 `bailian-cli` 提供;
  详细参数见 `bailian-cli` skill 的 `reference/` 目录或 `bl mcp <子命令> --help`。
- 金融 MCP 服务可能按调用计费;首次大批量调用前建议先 `--dry-run` 预览请求。
- 数据准确性以阿里云百炼 MCP 市场提供方为准,本 skill 不对数据准确性背书。

# application monitoring

应用监控（Application Monitoring）是百炼平台提供的可观测性能力，用于端到端追踪应用内部调用链路、分析模型响应延时、观察推理过程及 [Token](../concepts/token.md) 消耗等关键指标。该功能基于 OpenTelemetry 实现，数据同步频率为分钟级，适用于智能体、工作流和高代码三类应用，但暂不提供 API 接口 [应用观测](../../raw/application-user-guide/application-monitoring/application-observation.md)。

## 支持的模型/功能

- **支持的应用类型**：智能体应用、工作流应用、高代码应用（注意：[通过Assistant API创建的智能体应用](../../raw/application-user-guide/application-monitoring/application-observation.md)暂不支持）。
- **可观测节点类型**：
  - `CHAIN`（根节点，如 `AgentApp`/`WorkflowApp`/`FullCodeApp`）
  - `LLM`（大模型调用，含输入/输出 [Token](../concepts/token.md) 统计与首 [Token](../concepts/token.md) 耗时）
  - `RETRIEVER`（含 `TextRetriever` 和 `VectorRetriever`，默认返回 100 个切片）
  - `EMBEDDING`（向量化节点，Token 量指 Embedding 模型处理的输入 Token 数）
  - `RERANKER`、`REWRITER`、`TOOL`、`GUARDRAIL`、`API`、`CLASSIFIER` 等工作流专用节点
- **高级能力**：Span 数据导出（JSONL/Excel）、添加至评测集、多维度标签标注（布尔/分类/数字/文本）、Root/All/Model 三级 Span 筛选模式。

> **注意**：高代码应用仅支持上报 `CHAIN` 节点（名称为 `FullCodeApp`），其内部调用链路不可见；而智能体与工作流应用可展开完整嵌套节点树 [应用观测](../../raw/application-user-guide/application-monitoring/application-observation.md)。

## 关键参数

| 参数 | 说明 | 来源 |
|------|------|------|
| `Request ID` / `Trace ID` / `Span ID` | 用于精准定位单次调用链路，可在节点详情页点击“查看 ID”获取 | [应用观测](../../raw/application-user-guide/application-monitoring/application-observation.md) |
| 延时（毫秒） | LLM 节点延时包含流式响应全过程；平均调用时长、平均首 Token 耗时均在监控统计页展示 | [应用观测](../../raw/application-user-guide/application-monitoring/application-observation.md) |
| Token 总量 | = 输入 Token + 输出 Token；支持按总量、输入、输出分别统计趋势 | [应用观测](../../raw/application-user-guide/application-monitoring/application-observation.md) |
| 标签字段 | 支持布尔值、分类、数字、文本四类标注类型，与评测系统共享标签管理 | [应用观测](../../raw/application-user-guide/application-monitoring/application-observation.md) |

## 使用方式

### 前置配置（必需）
1. 主账号或已授权子账号访问 [应用观测](https://bailian.console.aliyun.com/tab=app?tab=app#/app-observe)，点击右上角「应用观测配置」；
2. 授权 `AliyunBailianFullAccess` 及 `创建服务关联角色` 权限（子账号需额外配置 RAM 策略）；
3. 开通可观测链路 OpenTelemetry 服务并初始化 LogStore。

### 日常操作
- **添加应用**：仅支持已发布的应用；未发布应用需先通过「管理应用 → 发布」启用；
- **观测数据**：自动采集 Prompt、输出、延时、Token 量、状态（正常/错误）等，最长保留 30 天；
- **筛选与搜索**：支持按 `Request ID`/`Trace ID`/`Span ID`、状态、Span Name、输入/输出关键词、延时/Token 区间、自定义标签等条件组合过滤；
- **导出与复用**：Trace 列表页支持 JSONL/Excel 导出；Span 数据可批量导入评测集（支持字段映射与追加/覆盖策略）。

## 限制和注意事项

- **无 API 支持**：当前应用监控功能仅提供控制台界面，不开放 RESTful 或 SDK 接口 [应用观测](../../raw/application-user-guide/application-monitoring/application-observation.md)。
- **存储依赖**：功能本身免费，但底层 OpenTelemetry 存储费用需单独承担，详见 [计费说明](https://help.aliyun.com/zh/arms/tracing-analysis/product-overview/untitled-document-1697525445039)。
- **高代码应用限制**：即使开启观测，也仅上报 `FullCodeApp` 根节点，无法追踪内部函数、LLM 或检索调用；必须在部署时显式添加 `--telemetry enable` 参数，并使用 AgentScope-AI 的 `Tracing` 模块上报数据。
- **[长期记忆](../concepts/long-term-memory.md)不可观测**：知识库检索可观测，但[长期记忆](../concepts/long-term-memory.md)（Long-term Memory）中的检索过程暂不支持。
- **权限时效**：主账号开通后通常分钟级生效，高峰期可能延迟；子账号配置需严格遵循 [常见问题](../../raw/application-user-guide/application-monitoring/application-observation.md) 中的四步权限清单。

## 来源文档

- [应用观测](../../raw/application-user-guide/application-monitoring/application-observation.md)



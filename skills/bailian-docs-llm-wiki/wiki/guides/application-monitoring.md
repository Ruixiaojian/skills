# application monitoring

应用监控（Application Monitoring）是阿里云百炼平台提供的端到端可观测能力，用于追踪智能体、工作流及高代码类应用的内部执行链路，覆盖向量生成、知识检索、大模型调用等关键节点，并采集延时、Token 用量、状态码等核心指标。数据同步频率为分钟级，支持按 Trace ID / Span ID / Request ID 检索与多维筛选，适用于性能分析、成本优化与线上数据回捞。该功能当前**无公开 API 接口**，全部操作需通过控制台完成，详见 [应用观测](../../raw/application-user-guide/application-monitoring/application-observation.md)。

## 支持的模型/功能

- **支持的应用类型**：智能体应用、工作流应用、高代码应用（但高代码应用仅上报 `CHAIN` 根节点，[不支持内部链路追踪](../../raw/application-user-guide/application-monitoring/application-observation.md)）。
- **不支持的应用**：通过 Assistant API 创建的智能体应用（见 [应用观测](../../raw/application-user-guide/application-monitoring/application-observation.md) 中“支持的应用”章节说明）。
- **可观测节点类型**：
  - 通用节点：`CHAIN`（根节点，名称如 `AgentApp`/`WorkflowApp`/`FullCodeApp`）、`LLM`（含输入/输出 Token 统计与首 Token 耗时）、`EMBEDDING`、`RETRIEVER`（含 `TextRetriever`/`VectorRetriever`）、`RERANKER`、`REWRITER`、`GUARDRAIL`、`TOOL`；
  - 工作流专属节点：`START`、`END`、`API`、`CLASSIFIER`、`TEXT_CONVERTER`、`SCRIPT`、`CONDITION`、`FUNCTION_COMPUTE`、`APP_FLOW`；
  - > **注意**：`FullCodeApp` 类型的 `CHAIN` 节点在 [应用观测](../../raw/application-user-guide/application-monitoring/application-observation.md) 文档中明确说明“目前不支持追踪其内部调用链路”，与智能体/工作流的深度可观测能力存在本质差异。

## 关键参数

| 参数 | 说明 | 来源依据 |
|------|------|----------|
| **延时（调用时长）** | LLM 节点延时包含完整响应过程（含[流式输出](../concepts/streaming-output.md)），`平均首Token耗时` 仅对流式调用有效 | [应用观测](../../raw/application-user-guide/application-monitoring/application-observation.md) “监控统计”章节 |
| **Token 量** | `LLM` 节点 = 输入 Token + 输出 Token；`EMBEDDING` 节点 = 向量化输入 Prompt 的 Token 数 | [应用观测](../../raw/application-user-guide/application-monitoring/application-observation.md) 节点说明部分 |
| **状态字段** | 分为 `正常` 与 `错误`；错误可进一步按类型细分（如 `Guardrail` 触发的 `ManualIntervention`） | [应用观测](../../raw/application-user-guide/application-monitoring/application-observation.md) “过滤器”章节 |
| **ID 字段** | 支持按 `Request ID`、`Trace ID`、`Span ID` 搜索；ID 需在节点详情页点击“查看 ID”获取 | [应用观测](../../raw/application-user-guide/application-monitoring/application-observation.md) “使用方法”第2步 |

## 使用方式

1. **前提配置**（仅首次需操作）：
   - 主账号或具备权限的子账号需完成三项开通：授权 OpenTelemetry 服务角色、开通 OpenTelemetry 服务、初始化 LogStore 存储（详见 [应用观测](../../raw/application-user-guide/application-monitoring/application-observation.md) “前提条件”）；
   - 子账号需额外配置 `AliyunBailianFullAccess` + 页面权限 + `CreateServiceLinkedRole` 策略（见文档“常见问题”）。

2. **启用观测**：
   - 应用必须已**发布**且归属当前业务空间；
   - 在 [应用观测](https://bailian.console.aliyun.com/tab=app?tab=app#/app-observe) 页面添加目标应用；
   - 添加后自动开始分钟级数据同步；关闭观测即停止同步（历史数据不删除，但新增数据不再采集）。

3. **数据查看与分析**：
   - 支持三种 Span 筛选模式：`Root Span`（默认）、`All Span`、`Model Span`；
   - 过滤器支持按状态、Span Name、输入/输出关键词、延时、Token 量、标签等条件组合筛选；
   - 可导出 JSONL 或 Excel 格式原始数据；
   - 监控统计页提供调用次数、失败率、Token 趋势、平均延时等聚合图表（时间范围最长 30 天，粒度支持分钟/小时/天）。

4. **高级用法**：
   - **添加到评测集**：支持将 Span 数据批量导入评测集，支持字段映射（最多 50 个字段）与追加/覆盖策略；
   - **数据标注**：支持布尔值、分类、数字、文本四类标签，与评测集标签系统共享。

## 限制和注意事项

- **功能限制**：
  - 当前无 API 接口，所有操作依赖控制台；
  - 不支持[长期记忆](../concepts/long-term-memory.md)（Long-term Memory）中的检索过程观测；
  - 高代码应用仅上报 `FullCodeApp` 根节点，无法展开内部逻辑（见 [应用观测](../../raw/application-user-guide/application-monitoring/application-observation.md) “高代码应用”章节）；
  - `TextRetriever` 与 `VectorRetriever` 均默认返回 100 个切片，暂不支持数量调整。

- **权限与部署要求**：
  - 子账号需主账号显式授权，否则无法完成 OpenTelemetry 开通（详见 [应用观测](../../raw/application-user-guide/application-monitoring/application-observation.md) “常见问题”）；
  - 高代码应用若未在代码中集成 AgentScope-AI Tracing 模块，或部署时未添加 `--telemetry enable` 参数，则无法上报任何可观测数据。

- **计费说明**：
  - 应用监控功能本身免费；
  - 所有追踪数据存储于可观测链路 OpenTelemetry 服务，按该服务计费规则收费（参见官方 [计费说明](https://help.aliyun.com/zh/arms/tracing-analysis/product-overview/untitled-document-1697525445039)）。

## 来源文档

- [应用观测](../../raw/application-user-guide/application-monitoring/application-observation.md)



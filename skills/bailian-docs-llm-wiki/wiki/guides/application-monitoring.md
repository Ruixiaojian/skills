# application monitoring

应用监控（Application Monitoring）是百炼平台提供的端到端可观测能力，用于追踪和分析智能体、工作流及高代码类应用的内部执行链路。它支持查看调用延时、[Token](../concepts/token.md)消耗、模型思考过程、节点状态等关键指标，数据同步频率为分钟级。该功能依赖可观测链路 OpenTelemetry 服务，当前**不提供 API 接口**，所有操作均通过控制台完成 [应用观测](../../raw/application-user-guide/application-monitoring/application-observation.md)。

## 支持的模型/功能

- **支持的应用类型**：智能体应用、工作流应用、高代码应用（仅支持入口级观测，[不支持内部链路追踪](../../raw/application-user-guide/application-monitoring/application-observation.md)）。
- **不支持的应用**：通过 Assistant API 创建的智能体应用（见 [原文标题](../../raw/application-user-guide/application-monitoring/application-observation.md)）。
- **可观测节点类型**：
  - 智能体/工作流：`CHAIN`（根节点，如 `AgentApp`/`WorkflowApp`）、`LLM`、`RETRIEVER`（含 `TextRetriever`/`VectorRetriever`）、`EMBEDDING`、`RERANKER`、`REWRITER`、`TOOL`、`GUARDRAIL`、`AGENT` 等；
  - 工作流特有：`START`、`END`、`API`、`CLASSIFIER`、`TEXT_CONVERTER`、`SCRIPT`、`CONDITION`、`FUNCTION_COMPUTE`、`APP_FLOW`；
  - 高代码：仅 `CHAIN` 类型（名称为 `FullCodeApp`），[无子节点展开能力](../../raw/application-user-guide/application-monitoring/application-observation.md)。
- **附加能力**：Span 数据导出（JSONL/Excel）、添加至评测集、多维度标签标注（与评测系统共享标签体系）、基于 Request ID / Trace ID / Span ID 的精准检索。

> **注意**：文档中明确说明“应用观测目前暂无API”，但部分用户可能误以为可通过 SDK 或 REST API 接入；请以 [原文标题](../../raw/application-user-guide/application-monitoring/application-observation.md) 为准，所有交互必须通过控制台完成。

## 关键参数

| 参数 | 说明 | 备注 |
|------|------|------|
| **延时（调用时长）** | 从请求发起至完整响应返回的总耗时（毫秒）；LLM 节点延时包含[流式输出](../concepts/streaming-output.md)首 [Token](../concepts/token.md) 及全部 [Token](../concepts/token.md) 生成时间 | 可按分钟/小时/天聚合，支持筛选“大于”“小于等于”等条件 |
| **Token 总量** | 输入 Token 数 + 输出 Token 数 | `EMBEDDING` 节点 Token 量指向量化输入长度；`LLM` 节点 Token 量为模型 I/O 总和 |
| **首 Token 耗时** | 流式调用下，从请求发出到首个 Token 返回的时间 | 仅在监控统计页展示，不可在 Span 列表直接筛选 |
| **状态** | `正常` 或 `错误`（含细分错误类型） | 错误类型可用于过滤器精确匹配 |
| **标签（Label）** | 用户自定义标注字段，支持布尔值、分类、数字、文本四类 | 标注后立即生效，支持在过滤器中按类型条件筛选 |

## 使用方式

1. **前提配置**（首次使用必做）：
   - 使用主账号或已授权子账号访问 [应用观测](https://bailian.console.aliyun.com/tab=app?tab=app#/app-observe)；
   - 单击右上角 **应用观测配置**，依次完成：
     - 授权可观测链路 OpenTelemetry 服务角色；
     - 开通 OpenTelemetry 服务；
     - 初始化 LogStore 存储（权限配置详见 [原文标题](../../raw/application-user-guide/application-monitoring/application-observation.md)）。

2. **启用观测**：
   - 在应用观测页面单击 **选择被观测的应用** > **添加**；
   - 应用需已**发布**且属于当前业务空间；
   - 添加后自动开始分钟级数据同步；关闭观测则停止同步（历史数据保留，新增数据不补录）。

3. **查看与分析**：
   - 在 Span 列表页切换筛选模式（`Root Span`/`All Span`/`Model Span`）；
   - 使用过滤器组合条件（状态、Span Name、输入/输出关键词、延时、Token 量、标签等）；
   - 单击节点名称展开详情，查看原始数据、标注记录、ID（Request/Trace/Span）；
   - 在 **监控统计** 页签查看调用趋势、失败率、Token 分布、平均首 Token 耗时等聚合指标。

4. **数据导出与复用**：
   - 支持将当前筛选结果导出为 JSONL 或 Excel；
   - 可批量选中 Span 添加至评测集（支持追加/覆盖、字段映射，最多 50 个字段）；
   - 标注数据实时同步，便于后续评测与归因分析。

## 限制和注意事项

- **功能限制**：
  - 不支持 Assistant API 创建的智能体应用；
  - 高代码应用仅上报 `FullCodeApp` 根节点，[无法观测其内部函数或模型调用](../../raw/application-user-guide/application-monitoring/application-observation.md)；
  - [长期记忆](../concepts/long-term-memory.md)中的检索过程不可观测；
  - 文本/向量检索默认返回 100 个切片，数量不可配置；
  - 数据保留最长 30 天，不支持自定义保留策略。

- **权限与部署要求**：
  - 子账号需额外配置 `CreateServiceLinkedRole` 权限（详见 [原文标题](../../raw/application-user-guide/application-monitoring/application-observation.md)）；
  - 高代码应用需在部署时显式添加 `--telemetry enable` 参数，并在代码中集成 AgentScope-AI Tracing 模块。

- **计费说明**：
  - 应用监控功能本身免费；
  - 所有追踪数据存储于 OpenTelemetry 服务，按该服务计费规则收取存储与写入费用（参见 [OpenTelemetry 计费文档](https://help.aliyun.com/zh/arms/tracing-analysis/product-overview/untitled-document-1697525445039)）。

## 来源文档

- [应用观测](../../raw/application-user-guide/application-monitoring/application-observation.md)



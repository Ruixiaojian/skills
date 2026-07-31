# application monitoring

应用监控（Application Monitoring）是百炼平台提供的可观测性能力，用于端到端追踪智能体、工作流及高代码类应用的内部执行链路，支持查看调用延时、[Token](../concepts/token.md) 消耗、节点状态、模型思考过程等关键指标。数据以分钟级频率同步至可观测链路 OpenTelemetry 服务，所有追踪数据均基于标准 Span 结构组织，便于调试、性能分析与评测集构建。该功能当前仅提供控制台界面，**暂无公开 API 接口**，详见 [应用观测](../../raw/application-user-guide/application-monitoring/application-observation.md)。

## 支持的模型/功能

- **支持的应用类型**：智能体应用、工作流应用、高代码应用（但高代码应用仅上报 `CHAIN` 根节点，[不支持内部链路追踪](../../raw/application-user-guide/application-monitoring/application-observation.md)）。
- **支持的节点类型**：
  - `CHAIN`（根节点，如 `AgentApp`/`WorkflowApp`/`FullCodeApp`）
  - `LLM`（大模型推理，含输入/输出 [Token](../concepts/token.md) 统计与首 [Token](../concepts/token.md) 耗时）
  - `RETRIEVER`（含 `TextRetriever` 和 `VectorRetriever`，默认返回 100 个切片）
  - `EMBEDDING`、`RERANKER`、`REWRITER`、`TOOL`、`GUARDRAIL`、`AGENT` 等
  - 工作流专属节点：`START`、`END`、`API`、`CLASSIFIER`、`CONDITION`、`SCRIPT`、`FUNCTION_COMPUTE`、`APP_FLOW`
- **核心功能**：
  - 多维度 Span 数据筛选（按状态、Span Name、输入/输出关键词、延时、Token 量、标签等）
  - 交互式链路展开与 ID（Request ID / Trace ID / Span ID）提取
  - 监控统计图表（调用次数、失败率、Token 总量、平均调用时长、平均首 Token 耗时）
  - 数据导出（JSONL / Excel）
  - 一键添加 Span 到评测集（支持字段映射与全量/追加导入）
  - 数据标注（布尔值、分类、数字、文本四类标签，与评测系统共享）

> **注意**：[通过 Assistant API 创建的智能体应用](../../raw/application-user-guide/application-monitoring/application-observation.md) **不支持**应用监控，该限制在原始文档中明确声明。

## 关键参数

| 参数名 | 含义 | 说明 |
|--------|------|------|
| `Request ID` | 单次用户请求唯一标识 | 用于跨系统关联日志；可在节点详情页点击“查看 ID”获取 |
| `Trace ID` | 全链路追踪唯一标识 | 同一业务请求下所有 Span 的共用 ID |
| `Span ID` | 单个操作单元唯一标识 | 表示一个节点（如 `LLM` 或 `RETRIEVER`）的执行实例 |
| `延时（ms）` | 节点执行耗时 | `LLM` 节点延时包含流式响应全过程；`EMBEDDING` 延时仅含向量化耗时 |
| `Token总量` | 输入 Token + 输出 Token | `LLM` 和 `EMBEDDING` 节点分别统计，单位为 token 数 |
| `首 Token 耗时` | 流式调用下首个 token 返回时间 | 仅对支持[流式输出](../concepts/streaming-output.md)的 LLM 节点有效，需在监控统计页查看 |

## 使用方式

### 前置配置（仅需一次）
1. 使用主账号访问 [应用观测](https://bailian.console.aliyun.com/tab=app?tab=app#/app-observe)，单击右上角 **应用观测配置**；
2. 授权 `AliyunOpenTelemetryFullAccess` 服务角色权限；
3. 开通可观测链路 OpenTelemetry 服务并初始化 LogStore；
4. 配置完成后通常分钟级生效（高峰期可能延迟），子账号需额外配置 `CreateServiceLinkedRole` 权限 —— 详细步骤见 [应用观测](../../raw/application-user-guide/application-monitoring/application-observation.md)。

### 日常使用流程
1. **添加被观测应用**：在应用观测页面点击 **选择被观测的应用 > 添加**；确保应用已发布且归属当前业务空间；
2. **查看追踪数据**：
   - 在 Span 列表页切换筛选模式（`Root Span` / `All Span` / `Model Span`）；
   - 使用过滤器按状态、关键词、延时、Token 量或标签组合筛选；
   - 单击节点名称展开详情，查看原始输入/输出、标注记录、嵌套子节点；
3. **导出与分析**：
   - 在 Trace 列表页右上角点击 **导出数据**（JSONL 或 Excel）；
   - 在 **监控统计** 页签按时间范围（最长 30 天）和聚合粒度（分钟/小时/天）查看趋势图；
4. **评测集成**：
   - 批量选中 Span → **添加到评测集** → 映射字段（最多 50 个）→ 选择追加或覆盖模式。

## 限制和注意事项

- **API 缺失**：应用监控目前**无开放 API**，所有操作必须通过控制台完成，详见 [应用观测](../../raw/application-user-guide/application-monitoring/application-observation.md)。
- **高代码应用限制**：`FullCodeApp` 类型仅上报根节点，无法观测其内部[函数调用](../concepts/function-calling.md)链路；若需完整追踪，须在代码中集成 `AgentScope-AI` 的 [Tracing 模块](https://github.com/agentscope-ai/agentscope-runtime/tree/main/src/agentscope_runtime/engine/tracing)，并在部署时添加 `--telemetry enable` 参数。
- **数据时效性**：指标同步频率为**分钟级**，不支持实时（秒级）监控。
- **存储与计费**：应用监控本身免费，但底层依赖 OpenTelemetry 服务，产生的日志与链路数据需按 [OpenTelemetry 计费规则](https://help.aliyun.com/zh/arms/tracing-analysis/product-overview/untitled-document-1697525445039) 支付存储与读取费用。
- **[长期记忆](../concepts/long-term-memory.md)不可观测**：知识库检索可追踪，但[长期记忆](../../raw/application-user-guide/application-monitoring/application-observation.md)中的检索过程暂不支持观测。

## 来源文档

- [应用观测](../../raw/application-user-guide/application-monitoring/application-observation.md)



# application monitoring

应用监控（Application Monitoring）是阿里云百炼平台提供的端到端可观测能力，用于追踪智能体、工作流及高代码类应用的内部执行链路，覆盖向量生成、知识检索、大模型调用等关键节点，并采集延时、[Token](../concepts/token.md) 用量、状态码等核心指标。数据同步频率为分钟级，支持按 Trace ID / Span ID / Request ID 检索与多维筛选，适用于性能分析、成本优化与线上数据回捞。该功能当前**无公开 API 接口**，全部操作需通过控制台完成，详见 [应用观测](../../raw/application-user-guide/application-monitoring/application-observation.md)。

## 支持的模型/功能

- **支持的应用类型**：智能体应用、工作流应用、高代码应用（但高代码应用仅上报 `CHAIN` 根节点，[不支持内部链路追踪](../../raw/application-user-guide/application-monitoring/application-observation.md)）。
- **不支持的应用**：通过 Assistant API 创建的智能体应用（见 [应用观测](../../raw/application-user-guide/application-monitoring/application-observation.md) 中的明确限制）。
- **可观测节点类型**：
  - 通用节点：`CHAIN`（根节点，名称如 `AgentApp`/`WorkflowApp`/`FullCodeApp`）、`LLM`、`RETRIEVER`（含 `TextRetriever`/`VectorRetriever`）、`EMBEDDING`、`RERANKER`、`REWRITER`、`TOOL`、`GUARDRAIL`；
  - 工作流专属节点：`START`、`API`、`CLASSIFIER`、`TEXT_CONVERTER`、`SCRIPT`、`CONDITION`、`FUNCTION_COMPUTE`、`APP_FLOW`、`END`；
  - **注意**：`KnowledgeRetriever` 子节点中的 `TextRetriever` 和 `VectorRetriever` 均默认返回 100 个文本切片，且**暂不支持数量调整**（该限制在 [应用观测](../../raw/application-user-guide/application-monitoring/application-observation.md) 的“支持的节点类型”章节中统一说明，无其他文档 contradict）。

## 关键参数

| 参数 | 说明 | 来源依据 |
|------|------|----------|
| **延时（调用时长）** | LLM 节点延时包含完整响应输出过程；平均首 [Token](../concepts/token.md) 耗时仅对流式调用有效 | [应用观测](../../raw/application-user-guide/application-monitoring/application-observation.md) “监控统计”节 |
| **[Token](../concepts/token.md) 量** | `LLM` 节点 = 输入 Token + 输出 Token；`EMBEDDING` 节点 = 向量化输入 Token 数 | [应用观测](../../raw/application-user-guide/application-monitoring/application-observation.md) “附录”节 |
| **状态字段** | 分为 `正常` 与 `错误`；错误可进一步按类型细分（如 `Guardrail` 触发的 `ManualIntervention`） | [应用观测](../../raw/application-user-guide/application-monitoring/application-observation.md) “查看数据”节 |
| **ID 系统** | 支持按 `Request ID`、`Trace ID`、`Span ID` 搜索；ID 需在节点详情页点击“查看 ID”获取 | [应用观测](../../raw/application-user-guide/application-monitoring/application-observation.md) “使用方法 > 2. 开始观测”节 |

## 使用方式

1. **前提配置**（主账号或已授权子账号）：
   - 授权可观测链路 OpenTelemetry 服务角色权限；
   - 开通 OpenTelemetry 服务；
   - 初始化 LogStore 存储（高峰期生效可能延迟）；
   > 子账号需额外配置 `AliyunBailianFullAccess` + `应用观测-操作` 页面权限 + `CreateServiceLinkedRole` 策略（详见 [应用观测](../../raw/application-user-guide/application-monitoring/application-observation.md) “常见问题”）。

2. **启用观测**：
   - 应用必须已**发布**且属于当前业务空间；
   - 在 [应用观测](https://bailian.console.aliyun.com/tab=app?tab=app#/app-observe) 页面添加目标应用；
   - 添加后自动开始分钟级数据同步；关闭观测即停止同步（历史数据不恢复）。

3. **数据查看与操作**：
   - 支持 `Root Span` / `All Span` / `Model Span` 三种视图模式；
   - 过滤器支持按状态、Span Name、输入/输出关键词、延时、Token 量、标签等条件组合筛选；
   - 可导出 JSONL 或 Excel 格式数据；
   - 支持将 Span 数据**批量添加至评测集**（支持字段映射，最多 50 个字段）；
   - 支持对 Span 添加结构化标注（布尔/分类/数字/文本），标注与评测系统共享标签管理。

## 限制和注意事项

> **注意**：应用监控功能本身不计费，但底层依赖可观测链路 OpenTelemetry 服务，其产生的日志、链路数据存储与查询费用需单独承担（参见 [应用观测](../../raw/application-user-guide/application-monitoring/application-observation.md) “计费说明”）。

- **功能限制**：
  - 当前**无 API 接口**，所有操作仅限控制台；
  - 不支持[长期记忆](../concepts/long-term-memory.md)（Long-term Memory）中的检索过程观测；
  - 高代码应用仅暴露 `FullCodeApp` 根节点，内部逻辑不可见（需自行集成 AgentScope-AI Tracing 模块并启用 `--telemetry enable`）；
  - 所有节点默认返回 100 个检索结果，不支持自定义数量。

- **数据时效性**：
  - 数据同步延迟约 1–5 分钟（受服务负载影响）；
  - 最长可查询 30 天内数据；
  - 监控图表聚合粒度支持分钟/小时/天，但原始 Span 数据不支持亚秒级精度。

- **权限与部署要求**：
  - 子账号开通需满足四重权限（全局访问 + 页面操作 + SLR 创建 + OpenTelemetry 服务权限）；
  - 高代码应用若未在启动命令中添加 `--telemetry enable`，即使开启观测也无法上报数据（见 [应用观测](../../raw/application-user-guide/application-monitoring/application-observation.md) “常见问题”）。

## 来源文档

- [应用观测](../../raw/application-user-guide/application-monitoring/application-observation.md)



# application monitoring

应用监控（Application Monitoring）是百炼平台提供的端到端可观测能力，用于追踪智能体、工作流及高代码类应用的内部执行链路，涵盖向量生成、知识检索、大模型调用等关键节点，并提供延时、[Token](../concepts/token.md) 用量、状态码等分钟级指标。该功能不提供 API 接口，所有数据通过控制台交互式查看与导出。详细背景和设计目标参见 [应用观测](../../raw/application-user-guide/application-monitoring/application-observation.md)。

## 支持的模型/功能

- **支持的应用类型**：智能体应用、工作流应用、高代码应用（但高代码应用仅上报根节点 `FullCodeApp`，[不支持内部调用链路追踪](../../raw/application-user-guide/application-monitoring/application-observation.md)）。
- **不支持的应用类型**：通过 Assistant API 创建的智能体应用（[明确排除](../../raw/application-user-guide/application-monitoring/application-observation.md)）。
- **可观测节点类型**：
  - 通用节点：`CHAIN`（根节点，如 `AgentApp`/`WorkflowApp`）、`LLM`（含输入/输出 [Token](../concepts/token.md) 统计）、`EMBEDDING`、`RETRIEVER`（含 `TextRetriever`/`VectorRetriever`）、`RERANKER`、`REWRITER`、`GUARDRAIL`、`TOOL`；
  - 工作流特有节点：`START`、`END`、`API`、`CLASSIFIER`、`TEXT_CONVERTER`、`SCRIPT`、`CONDITION`、`FUNCTION_COMPUTE`、`APP_FLOW`；
  - 高代码应用仅支持 `CHAIN` 类型下的 `FullCodeApp` 节点，无子节点展开能力。

> **注意**：文档中对 `RETRIEVER` 子节点的说明在“智能体应用”和“工作流应用”两节中完全一致，但未提及[长期记忆](../concepts/long-term-memory.md)检索——[原文明确指出目前暂不支持观测在长期记忆中的检索过程](../../raw/application-user-guide/application-monitoring/application-observation.md)，该限制适用于所有应用类型。

## 关键参数

| 参数 | 说明 | 来源 |
|------|------|------|
| `Request ID` / `Trace ID` / `Span ID` | 用于精准定位单次调用链路，可在节点详情页点击“查看 ID”获取 | [应用观测](../../raw/application-user-guide/application-monitoring/application-observation.md) |
| 延时（调用时长） | LLM 节点包含完整流式响应时间；平均首 [Token](../concepts/token.md) 耗时专用于流式场景 | [应用观测](../../raw/application-user-guide/application-monitoring/application-observation.md) |
| Token 总量 | = 输入 Token + 输出 Token；Embedding 节点 Token 量仅统计向量化输入 | [应用观测](../../raw/application-user-guide/application-monitoring/application-observation.md) |
| 状态 | `正常` 或 `错误`（可进一步按错误类型细分） | [应用观测](../../raw/application-user-guide/application-monitoring/application-observation.md) |

## 使用方式

1. **前置配置**（仅需执行一次）：
   - 主账号或已授权子账号访问 [应用观测](https://bailian.console.aliyun.com/tab=app?tab=app#/app-observe)，点击右上角「应用观测配置」；
   - 授权 OpenTelemetry 服务角色、开通服务、初始化 LogStore（[详细步骤见原文](../../raw/application-user-guide/application-monitoring/application-observation.md)）。

2. **启用观测**：
   - 在应用观测页面点击「选择被观测的应用」→「添加」；
   - **必须确保应用已发布且归属当前业务空间**（未发布应用不会出现在列表中）。

3. **数据查看与筛选**：
   - 支持三种 Span 展示模式：`Root Span`（默认）、`All Span`、`Model Span`；
   - 可基于状态、Span Name、输入/输出关键词、延时、Token 量、标签等条件组合过滤；
   - 支持按 Request ID/Trace ID/Span ID 搜索，时间范围最长 30 天。

4. **高级操作**：
   - **导出数据**：Trace 列表页右上角支持 JSONL 或 Excel 格式导出；
   - **添加到评测集**：批量选择 Span，映射字段后导入（最多 50 个字段）；
   - **数据标注**：支持布尔值、分类、数字、文本四类标签，与评测系统共享标签管理。

## 限制和注意事项

- **无 API 接口**：应用监控为纯控制台功能，[暂无 SDK 或 REST API 支持](../../raw/application-user-guide/application-monitoring/application-observation.md)。
- **数据延迟**：所有指标同步频率为分钟级，非实时。
- **高代码应用限制**：
  - 即使开启观测，也仅上报 `FullCodeApp` 根节点，无法展开内部逻辑；
  - 需在部署时显式添加 `--telemetry enable` 参数，并在代码中集成 AgentScope-AI 的 [Tracing 模块](https://github.com/agentscope-ai/agentscope-runtime/tree/main/src/agentscope_runtime/engine/tracing) 才能上报有效数据。
- **权限要求**：
  - 子账号需同时具备 `AliyunBailianFullAccess`、页面级“应用观测-操作”权限，以及 `ram:CreateServiceLinkedRole` 系统策略（[配置步骤详见原文](../../raw/application-user-guide/application-monitoring/application-observation.md)）。
- **计费说明**：应用监控功能本身免费，但底层依赖可观测链路 OpenTelemetry 服务，相关存储与读取费用需单独承担。

## 来源文档

- [应用观测](../../raw/application-user-guide/application-monitoring/application-observation.md)



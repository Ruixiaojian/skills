# application monitoring

应用观测（Application Monitoring）是阿里云百炼平台提供的端到端可观测能力，用于追踪应用内部调用链路、分析模型响应延时、查看推理过程及 [Token](../concepts/token.md) 消耗等关键指标。该功能基于 OpenTelemetry 架构实现，数据同步频率为分钟级，适用于智能体、工作流和高代码三类应用。> **注意：应用观测目前暂无 API 接口**，所有操作均需通过控制台完成，详见 [应用观测](../../raw/application-user-guide/application-monitoring/application-observation.md)。

## 支持的模型/功能

- **支持的应用类型**：智能体应用、工作流应用、高代码应用（但高代码应用仅上报根节点 `FullCodeApp`，不支持内部链路追踪）  
- **可观测节点类型**：涵盖 `CHAIN`、`LLM`、`RETRIEVER`（含 `TextRetriever`/`VectorRetriever`）、`EMBEDDING`、`RERANKER`、`REWRITER`、`TOOL`、`GUARDRAIL`、`API`、`CLASSIFIER`、`CONDITION` 等数十种节点，完整覆盖 RAG、Agent、Workflow 全流程；具体定义参见 [应用观测支持的所有节点类型](../../raw/application-user-guide/application-monitoring/application-observation.md)  
- **核心功能**：
  - 调用链路展开与交互式 Trace 查看（支持 Root Span / All Span / Model Span 三种视图）
  - 基于 Request ID / Trace ID / Span ID 的精准检索
  - 实时标注（布尔值、分类、数字、文本四类标签类型，与评测系统共享标签管理）
  - 数据导出（JSONL 或 Excel 格式）
  - Span 直接导入评测集（支持字段映射与追加/覆盖模式）

## 关键参数

| 参数 | 说明 | 备注 |
|------|------|------|
| **延时（调用时长）** | 从请求发起至完整响应返回的总耗时（毫秒），LLM 节点包含流式首 [Token](../concepts/token.md) 及全文生成时间 | 可按分钟/小时/天聚合统计 |
| **[Token](../concepts/token.md) 总量** | 输入 Token 数 + 输出 Token 数之和 | `EMBEDDING` 节点仅统计输入 Token；`LLM` 节点统计双向 Token |
| **平均首 Token 耗时** | 流式调用场景下，首个 Token 返回所需时间 | 仅对启用[流式输出](../concepts/streaming-output.md)的 LLM 节点有效 |
| **状态** | `正常` 或 `错误`（含细分错误类型，如 `GuardrailBlocked`、`LLMTimeout` 等） | 错误详情可在节点详情页查看原始错误日志 |
| **标签（Label）** | 用户自定义标注字段，支持多类型输入与条件筛选 | 最多支持 50 个字段映射到评测集 |

> **注意**：`TextRetriever` 和 `VectorRetriever` 默认返回 100 个文本切片，且**暂不支持数量调整**；[长期记忆](../concepts/long-term-memory.md)（Long-term Memory）中的检索过程**当前不可观测**，详见 [原文标题](../../raw/application-user-guide/application-monitoring/application-observation.md)。

## 使用方式

1. **前提配置**（仅需执行一次）：
   - 主账号或已授权子账号访问 [应用观测配置](https://bailian.console.aliyun.com/tab=app?tab=app#/app-observe) 页面，完成：
     - 授权可观测链路 OpenTelemetry 服务角色权限
     - 开通 OpenTelemetry 服务
     - 初始化 LogStore 存储（高峰期可能延迟生效）

2. **添加被观测应用**：
   - 应用必须已**发布**且属于当前业务空间；未发布应用需先通过「管理应用 → 发布」操作启用观测。

3. **查看与分析**：
   - 在 Span 列表页使用过滤器（支持状态、Span Name、输入/输出关键词、延时、Token 量、标签等多维条件组合）
   - 单击节点名称展开详情，查看原始输入/输出、上下文、标注记录及嵌套子节点
   - 切换至「监控统计」页签，查看调用次数、失败率、Token 趋势、平均延时等聚合指标（最长回溯 30 天）

4. **高级操作**：
   - 批量选中 Span → 「添加到评测集」→ 配置字段映射（新建或复用已有评测集）
   - 在节点详情页点击「数据标注」添加结构化标签，支持后续按标签筛选与分析

## 限制和注意事项

- **API 限制**：应用观测**暂无开放 API**，所有数据获取与操作必须通过控制台完成，无法集成至自动化运维流程 —— 此限制在 [原文标题](../../raw/application-user-guide/application-monitoring/application-observation.md) 中明确声明。
- **应用兼容性**：不支持通过 Assistant API 创建的智能体应用；高代码应用虽可开启观测，但仅上报 `FullCodeApp` 根节点，内部逻辑需依赖 [AgentScope-AI Tracing 模块](https://github.com/agentscope-ai/agentscope-runtime/tree/main/src/agentscope_runtime/engine/tracing) 并部署时显式启用 `--telemetry enable` 参数。
- **权限要求**：子账号需同时具备 `AliyunBailianFullAccess`、页面级「应用观测-操作」权限，以及 `ram:CreateServiceLinkedRole` 系统策略（否则无法完成服务角色创建）。
- **计费说明**：应用观测功能免费，但底层依赖的 OpenTelemetry 服务（LogStore 存储、Trace 写入/查询）按实际用量计费，费用详情参见 [OpenTelemetry 计费文档](https://help.aliyun.com/zh/arms/tracing-analysis/product-overview/untitled-document-1697525445039)。

## 来源文档

- [应用观测](../../raw/application-user-guide/application-monitoring/application-observation.md)



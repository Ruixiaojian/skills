# application monitoring

应用观测（Application Monitoring）是阿里云百炼平台提供的端到端可观测能力，用于追踪应用内部调用链路、分析模型响应延时、查看推理过程与 [Token](../concepts/token.md) 消耗等关键指标。该功能基于 OpenTelemetry 实现，数据同步频率为分钟级，适用于调试、性能优化与真实场景评测。> **注意：应用观测目前暂无 API 接口**，所有操作均需通过控制台完成，详见 [应用观测](../../raw/application-user-guide/application-monitoring/application-observation.md)。

## 支持的模型/功能

- **支持的应用类型**：智能体应用、工作流应用、高代码应用（[原文标题](../../raw/application-user-guide/application-monitoring/application-observation.md)）。  
- **不支持的应用**：通过 Assistant API 创建的智能体应用（[原文标题](../../raw/application-user-guide/application-monitoring/application-observation.md)）。  
- **可观测节点类型**：覆盖完整 RAG 与编排链路，包括 `CHAIN`（根节点）、`LLM`（大模型调用）、`RETRIEVER`（含 `TextRetriever`/`VectorRetriever`）、`EMBEDDING`、`RERANKER`、`REWRITER`、`TOOL`、`GUARDRAIL`、`API`、`CLASSIFIER` 等；高代码应用仅支持 `CHAIN`（`FullCodeApp`）根节点级别观测，**不支持内部链路追踪**（[原文标题](../../raw/application-user-guide/application-monitoring/application-observation.md)）。  
- **附加能力**：支持 Span 数据导出（JSONL/Excel）、添加至评测集、多维度标签标注（布尔/分类/数字/文本）、基于 Request ID/Trace ID/Span ID 的精准检索。

## 关键参数

| 参数 | 说明 | 来源 |
|------|------|------|
| **延时（调用时长）** | LLM 节点包含首 [Token](../concepts/token.md) 响应及完整输出耗时；CHAIN/WorkflowApp 等根节点反映端到端耗时 | [原文标题](../../raw/application-user-guide/application-monitoring/application-observation.md) |
| **[Token](../concepts/token.md) 总量** | = 输入 Token + 输出 Token；Embedding 节点仅统计向量化输入 Token 数 | [原文标题](../../raw/application-user-guide/application-monitoring/application-observation.md) |
| **平均首 Token 耗时** | 仅对流式调用生效，单位毫秒 | [原文标题](../../raw/application-user-guide/application-monitoring/application-observation.md) |
| **状态** | `正常` 或 `错误`（可进一步按错误类型细分） | [原文标题](../../raw/application-user-guide/application-monitoring/application-observation.md) |

> **注意**：`TextRetriever` 和 `VectorRetriever` 默认返回 100 个文本切片，且**暂不支持数量调整**——该限制在文档中多次强调，开发者不可通过配置绕过。

## 使用方式

### 前置配置（必需）
1. 主账号或已授权子账号访问 [应用观测](https://bailian.console.aliyun.com/tab=app?tab=app#/app-observe)，点击右上角 **应用观测配置**；  
2. 完成三步授权：① 授权可观测链路 OpenTelemetry 服务角色；② 开通 OpenTelemetry 服务；③ 初始化 LogStore 存储；  
3. **子账号需额外配置**：`AliyunBailianFullAccess` + `应用观测-操作` 页面权限 + `CreateServiceLinkedRole` 系统策略（详见 [原文标题](../../raw/application-user-guide/application-monitoring/application-observation.md)）。

### 观测流程
- **添加应用**：仅已**发布**且属于当前业务空间的应用可见；未发布应用需先通过「管理应用 → 发布」启用观测。  
- **数据同步**：Prompt 输入后自动追踪，分钟级同步至观测列表；关闭观测后停止采集，重开仅同步新增数据。  
- **查看详情**：支持 Root Span / All Span / Model Span 三种视图；可通过状态、Span Name、输入/输出关键词、延时、Token 量、标签等条件组合过滤。  
- **导出与评测**：Trace 列表页支持 JSONL/Excel 导出；支持批量 Span 添加至评测集，支持字段映射（最多 50 个）与追加/覆盖导入模式。

## 限制和注意事项

- **无 API 支持**：当前仅提供控制台界面，不开放 RESTful 或 SDK 接口（[原文标题](../../raw/application-user-guide/application-monitoring/application-observation.md)）。  
- **高代码应用限制**：开启观测后仅显示 `FullCodeApp` 根节点，**无法观测其内部函数、HTTP 调用或自定义逻辑链路**；需在代码中集成 `AgentScope-AI` 的 Tracing 模块，并部署时显式启用 `--telemetry enable`（[原文标题](../../raw/application-user-guide/application-monitoring/application-observation.md)）。  
- **[长期记忆](../concepts/long-term-memory.md)不可观测**：知识库检索可观测，但[长期记忆](https://help.aliyun.com/zh/model-studio/long-term-memory)中的检索过程**明确不支持**（[原文标题](../../raw/application-user-guide/application-monitoring/application-observation.md)）。  
- **计费说明**：应用观测功能本身免费，但底层依赖 OpenTelemetry 服务，产生的日志与链路数据存储费用需单独承担。  
- **数据时效性**：指标更新延迟约 1–5 分钟，不适用于毫秒级实时告警场景。

## 来源文档

- [应用观测](../../raw/application-user-guide/application-monitoring/application-observation.md)



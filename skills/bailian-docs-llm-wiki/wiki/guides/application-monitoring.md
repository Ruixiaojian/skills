# application monitoring

应用监控（Application Monitoring）是百炼平台提供的端到端可观测能力，用于追踪智能体、工作流及高代码类应用的内部执行链路，采集延时、[Token](../concepts/token.md) 量、状态、输入输出等关键指标。数据以分钟级频率同步至可观测链路 OpenTelemetry 存储，支持深度下钻分析与导出，但**当前不提供 API 接口**，所有操作需通过控制台完成。详细背景和设计目标参见 [应用观测](../../raw/application-user-guide/application-monitoring/application-observation.md)。

## 支持的模型/功能

- **支持的应用类型**：智能体应用（Single Agent）、工作流应用（Workflow）和高代码应用（Rich Code）。  
- **不支持的应用类型**：通过 Assistant API 创建的智能体应用（[原文标题](../../raw/application-user-guide/application-monitoring/application-observation.md) 明确指出该限制）。  
- **可观测节点类型**：覆盖全链路关键环节，包括 `CHAIN`（根调用）、`LLM`（大模型推理）、`RETRIEVER`（含 `VectorRetriever`/`TextRetriever`）、`EMBEDDING`、`RERANKER`、`REWRITER`、`TOOL`、`GUARDRAIL`、`API`、`CLASSIFIER` 等；工作流还额外支持 `START`、`CONDITION`、`SCRIPT`、`END` 等节点。  
- **高代码应用限制**：仅上报 `CHAIN` 节点（名称为 `FullCodeApp`），**不支持追踪其内部调用链路**（[原文标题](../../raw/application-user-guide/application-monitoring/application-observation.md) 中明确说明）。

> **注意**：文档中对 `RETRIEVER` 子节点的描述在“智能体应用”和“工作流应用”两节中完全一致，但未说明是否复用同一套实现逻辑；实际使用中应以控制台实际展示的节点类型为准，避免依赖文档隐含假设。

## 关键参数

| 参数 | 说明 | 来源依据 |
|------|------|----------|
| **Trace ID / Span ID / Request ID** | 用于跨节点关联与精确检索，可在节点详情页点击“查看 ID”获取 | [原文标题](../../raw/application-user-guide/application-monitoring/application-observation.md) |
| **延时（调用时长）** | LLM 节点延时包含完整响应过程（含流式首 [Token](../concepts/token.md) 及后续 [Token](../concepts/token.md) 输出）；平均首 Token 耗时单独统计 | [原文标题](../../raw/application-user-guide/application-monitoring/application-observation.md) |
| **Token 量** | `LLM` 节点 = 输入 Token + 输出 Token；`EMBEDDING` 节点 = 向量化输入 Prompt 的 Token 数 | [原文标题](../../raw/application-user-guide/application-monitoring/application-observation.md) |
| **状态** | 分为 `正常` 与 `错误`，错误可进一步按类型细分（如 `ManualIntervention`、`SystemIntervention`） | [原文标题](../../raw/application-user-guide/application-monitoring/application-observation.md) |

## 使用方式

1. **前提配置**（仅需一次）：  
   - 主账号或已授权子账号访问 [应用观测](https://bailian.console.aliyun.com/tab=app?tab=app#/app-observe)，点击右上角「应用观测配置」；  
   - 完成三步：授权 OpenTelemetry 服务角色 → 开通 OpenTelemetry 服务 → 初始化 LogStore；  
   - 子账号需额外配置 `AliyunBailianFullAccess`、页面权限及 `ram:CreateServiceLinkedRole` 权限（详见 [原文标题](../../raw/application-user-guide/application-monitoring/application-observation.md) 常见问题章节）。

2. **启用观测**：  
   - 在应用观测页点击「选择被观测的应用」→「添加」；  
   - **仅已发布且归属当前业务空间的应用可见**；未发布应用需先通过「管理应用」→「发布」操作启用。

3. **数据查看与筛选**：  
   - 支持三种 Span 展示模式：`Root Span`（默认）、`All Span`、`Model Span`；  
   - 过滤器支持按状态、Span Name、输入/输出关键词、延时、Token 量、标签等多维条件组合筛选；  
   - 表头可自定义，支持按 `Request ID`/`Trace ID`/`Span ID` 搜索。

4. **高级功能**：  
   - **导出数据**：Trace 列表页右上角支持 JSONL 或 Excel 导出；  
   - **添加到评测集**：批量选中 Span，映射字段后导入（最多 50 字段）；  
   - **数据标注**：支持布尔值、分类、数字、文本四类标签，与评测系统共享标签管理。

## 限制和注意事项

- **无 API 支持**：应用监控功能当前**暂无 API**，所有配置与查询必须通过控制台完成（[原文标题](../../raw/application-user-guide/application-monitoring/application-observation.md) 明确强调）。  
- **数据延迟**：指标同步频率为**分钟级**，不适用于毫秒级实时诊断场景。  
- **存储计费**：功能本身免费，但底层依赖 OpenTelemetry 服务，产生的日志/Trace 数据按 OpenTelemetry 计费规则收费。  
- **高代码应用可观测性局限**：即使开启观测，也仅能捕获顶层 `FullCodeApp` 节点，无法观测其内部函数、模型调用等细节；若需深度追踪，需在代码中集成 AgentScope-AI Tracing 模块并部署时启用 `--telemetry enable` 参数。  
- **[长期记忆](../concepts/long-term-memory.md)不可观测**：知识库检索可观测，但[长期记忆](https://help.aliyun.com/zh/model-studio/long-term-memory)中的检索过程**目前暂不支持观测**（[原文标题](../../raw/application-user-guide/application-monitoring/application-observation.md) 多次提及）。

## 来源文档

- [应用观测](../../raw/application-user-guide/application-monitoring/application-observation.md)



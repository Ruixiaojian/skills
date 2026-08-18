# application monitoring

应用监控（Application Monitoring）是阿里云百炼平台提供的端到端可观测能力，用于追踪智能体、工作流及高代码类应用的内部执行链路。它支持查看调用延时、Token 消耗、模型思考过程、节点状态等关键指标，数据同步频率为分钟级。该功能依赖可观测链路 OpenTelemetry 服务，**当前不提供 API 接口**，所有操作均通过控制台完成。

## 支持的模型/功能

- **支持的应用类型**：  
  - [智能体应用](https://help.aliyun.com/zh/model-studio/single-agent-application)  
  - [工作流应用](https://help.aliyun.com/zh/model-studio/workflow-application/)  
  - [高代码应用](https://help.aliyun.com/zh/model-studio/rich-code-application/)  
  > **注意**：[通过Assistant API创建的智能体应用](https://help.aliyun.com/zh/model-studio/user-guide/what-is-assistant-api) **暂不支持**应用监控，详见 [原文标题](../../raw/application-user-guide/application-monitoring/application-observation.md)。

- **核心可观测能力**：  
  - 完整调用链路（Trace）可视化，支持 `CHAIN`、`LLM`、`RETRIEVER`、`EMBEDDING`、`RERANKER`、`TOOL`、`GUARDRAIL` 等节点类型；  
  - 多维度指标：延时（含首 Token 耗时）、输入/输出 Token 量、调用成功率、错误类型；  
  - 数据标注与标签管理（与评测系统共享标签体系）；  
  - Span 数据一键导出（JSONL / Excel）及批量导入评测集；  
  - 支持按 `Request ID`、`Trace ID`、`Span ID` 精确检索，以及基于状态、Span Name、输入/输出关键词、延时、Token 量、标签等条件的复合过滤。

- **节点说明参考**：  
  各类节点（如 `TextRetriever`、`VectorRetriever`、`WorkflowApp`、`FullCodeApp`）的语义、嵌套关系与限制详见 [原文标题](../../raw/application-user-guide/application-monitoring/application-observation.md) 的「支持的节点类型」章节。

## 关键参数

| 参数 | 说明 | 备注 |
|------|------|------|
| **延时（调用时长）** | 从请求进入应用至完整响应返回的总耗时（毫秒），对 `LLM` 节点包含[流式输出](../concepts/streaming-output.md)全过程 | `平均首Token耗时` 仅在流式调用场景下有效 |
| **Token总量** | `输入Token数 + 输出Token数`，单位为 token | `EMBEDDING` 节点的 Token 量仅统计向量化输入长度 |
| **状态** | `正常` 或 `错误`；错误可进一步细分为 `ManualIntervention`（人工干预）、`SystemIntervention`（系统干预）、插件调用失败等 | 错误详情需展开节点查看原始日志 |
| **Span Name** | 节点逻辑名称，如 `AgentApp`、`WorkflowApp`、`TextRetriever`、`LLM` 等 | 是筛选和分析的关键字段 |
| **标签（Label）** | 用户自定义标注字段，支持布尔值、分类、数字、文本四类类型 | 标签与评测集共用同一管理后台，最大支持 50 个字段映射 |

## 使用方式

1. **前提配置（仅首次）**：  
   - 单击应用观测页右上角「应用观测配置」，完成三步授权：  
     (1) 授权可观测链路 OpenTelemetry 服务角色；  
     (2) 开通 OpenTelemetry 服务；  
     (3) 初始化 LogStore 存储。  
   > **注意**：主账号操作分钟级生效；子账号需额外配置 `AliyunBailianFullAccess`、页面权限及 `CreateServiceLinkedRole` 策略，详见 [原文标题](../../raw/application-user-guide/application-monitoring/application-observation.md)「常见问题」部分。

2. **启用监控**：  
   - 进入 [应用观测](https://bailian.console.aliyun.com/tab=app?tab=app#/app-observe)，点击「选择被观测的应用」→「添加」；  
   - **仅已发布且归属当前业务空间的应用可见**；未发布应用需先通过「管理应用」→「发布」操作启用。

3. **查看与分析**：  
   - 在应用列表中点击「查看详情」，进入 Span 列表页：  
     - 切换 `Root Span` / `All Span` / `Model Span` 视图模式；  
     - 使用「过滤器」添加多条件组合筛选；  
     - 点击 Span 名称展开节点详情，查看原始数据、标注记录、嵌套子节点；  
     - 表头支持自定义显示字段（如延时、Token 总量、标签等）。

4. **高级操作**：  
   - **导出数据**：Trace 列表页右上角「导出数据」，支持 JSONL / Excel；  
   - **添加到评测集**：勾选 Span → 「添加到评测集」→ 映射字段（最多 50 个）→ 选择追加或覆盖；  
   - **数据标注**：在 Span 详情页点击「数据标注」，使用已有标签或跳转新建。

## 限制和注意事项

- **功能限制**：  
  - 应用监控 **无公开 API**，无法程序化接入或自动化触发；  
  - 高代码应用（`FullCodeApp`）仅上报根节点，**不支持内部链路追踪**；  
  - [长期记忆](../concepts/long-term-memory.md)（Long-term Memory）中的检索过程 **不可观测**；  
  - `TextRetriever` 与 `VectorRetriever` 默认返回 100 个切片，**不支持数量调整**。

- **数据时效性与范围**：  
  - 数据同步延迟约 **1–5 分钟**（高峰期可能延长）；  
  - 历史数据最长保留 **30 天**，时间范围筛选不可跨此限制；  
  - 监控统计图表支持按分钟/小时/天聚合，但原始 Span 数据仅保留明细粒度。

- **权限与部署要求**：  
  - 子账号开通需严格遵循权限清单（含 RAM 策略 `CreateServiceLinkedRole`），否则配置失败；  
  - 高代码应用必须在部署时显式添加 `--telemetry enable` 参数，并在代码中集成 AgentScope-AI 的 [Tracing 模块](https://github.com/agentscope-ai/agentscope-runtime/tree/main/src/agentscope_runtime/engine/tracing)，否则无数据上报。

- **计费说明**：  
  - 应用监控功能本身 **不收费**；  
  - 所有追踪数据存储于 OpenTelemetry 服务，按其[计费规则](https://help.aliyun.com/zh/arms/tracing-analysis/product-overview/untitled-document-1697525445039)收取存储与读取费用。

## 来源文档

- [应用观测](../../raw/application-user-guide/application-monitoring/application-observation.md)



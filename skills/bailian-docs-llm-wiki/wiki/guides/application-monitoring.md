# application monitoring

应用监控（Application Monitoring）是百炼平台提供的端到端可观测能力，用于追踪应用内部调用链路、分析模型响应延时、查看 [Token](../concepts/token.md) 消耗及模型思考过程等关键指标。该功能基于 OpenTelemetry 实现，数据同步频率为分钟级，适用于智能体、工作流和高代码三类应用，但暂不提供 API 接口 [应用观测](../../raw/application-user-guide/application-monitoring/application-observation.md)。

## 支持的模型/功能

- **支持的应用类型**：  
  - [智能体应用](https://help.aliyun.com/zh/model-studio/single-agent-application)  
  - [工作流应用](https://help.aliyun.com/zh/model-studio/workflow-application/)  
  - [高代码应用](https://help.aliyun.com/zh/model-studio/rich-code-application/)  
  > **注意**：通过 Assistant API 创建的智能体应用暂不支持 [应用观测](../../raw/application-user-guide/application-monitoring/application-observation.md)。

- **可观测节点类型**（按应用类型区分）：  
  - **智能体/工作流应用**：`CHAIN`（根节点，如 `AgentApp`/`WorkflowApp`）、`LLM`、`RETRIEVER`（含 `TextRetriever`/`VectorRetriever`）、`EMBEDDING`、`RERANKER`、`REWRITER`、`TOOL`、`GUARDRAIL`、`AGENT` 等；  
  - **工作流特有节点**：`START`、`API`、`CLASSIFIER`、`TEXT_CONVERTER`、`SCRIPT`、`CONDITION`、`FUNCTION_COMPUTE`、`APP_FLOW`、`END`；  
  - **高代码应用**：仅支持 `CHAIN` 节点（名称为 `FullCodeApp`），**不支持内部调用链路追踪**，需依赖 AgentScope-AI 的 [Tracing模块](https://github.com/agentscope-ai/agentscope-runtime/tree/main/src/agentscope_runtime/engine/tracing) 手动上报 [应用观测](../../raw/application-user-guide/application-monitoring/application-observation.md)。

## 关键参数

| 参数 | 说明 | 备注 |
|------|------|------|
| **Request ID / Trace ID / Span ID** | 唯一标识一次调用或子操作 | 可在节点详情页点击「查看 ID」获取 |
| **延时（调用时长）** | 从请求发起至响应完成的总耗时（毫秒） | `LLM` 节点延时包含[流式输出](../concepts/streaming-output.md)全过程 |
| **[Token](../concepts/token.md) 总量** | 输入 [Token](../concepts/token.md) 数 + 输出 Token 数 | `EMBEDDING` 节点仅统计输入 Token |
| **首 Token 耗时** | 流式调用下首个 Token 返回时间 | 仅在监控统计页提供聚合值 |
| **状态** | `正常` 或 `错误`（含细分错误类型） | 错误类型可用于过滤与根因分析 |

## 使用方式

1. **前提配置**（首次使用必做）：  
   - 单击应用观测页面右上角「应用观测配置」；  
   - 授权可观测链路 OpenTelemetry 服务角色权限；  
   - 开通 OpenTelemetry 服务并初始化 LogStore；  
   > **注意**：主账号操作分钟级生效；子账号需额外配置 `AliyunBailianFullAccess`、页面权限及 `CreateServiceLinkedRole` 策略 [应用观测](../../raw/application-user-guide/application-monitoring/application-observation.md)。

2. **启用观测**：  
   - 进入 [应用观测](https://bailian.console.aliyun.com/tab=app?tab=app#/app-observe)，点击「选择被观测的应用」→「添加」；  
   - 应用必须已**发布**且属于当前业务空间；  
   - 添加后自动采集 Prompt、输出、延时、Token 量等数据（分钟级同步）。

3. **数据查看与筛选**：  
   - 支持三种 Span 展示模式：`Root Span`（默认）、`All Span`、`Model Span`；  
   - 过滤器支持按状态、Span Name、输入/输出关键词、延时、Token 量、标签等多维条件组合筛选；  
   - 可导出 JSONL 或 Excel 格式原始数据。

4. **高级能力**：  
   - **监控统计页**：查看调用次数、失败率、Token 趋势、平均首 Token 耗时等；  
   - **添加到评测集**：批量选取 Span 数据，映射字段后导入评测集（最多 50 字段）；  
   - **数据标注**：支持布尔值、分类、数字、文本四类标签，与评测集标签系统共享。

## 限制和注意事项

- **功能限制**：  
  - 当前无 API 接口，所有操作需通过控制台完成；  
  - 不支持[长期记忆](../concepts/long-term-memory.md)（Long-term Memory）中的检索过程观测；  
  - 高代码应用无法自动追踪内部逻辑，需手动集成 AgentScope-AI Tracing 模块并部署时启用 `--telemetry enable` 参数。

- **权限与开通**：  
  - 子账号开通需满足四项权限要求（全局访问、页面操作、创建服务关联角色、OpenTelemetry 相关资源权限），缺一不可；  
  - 应用观测本身免费，但底层 OpenTelemetry 存储与计算按量计费。

- **数据时效性与范围**：  
  - 数据同步延迟约 1–5 分钟；  
  - 历史数据最长保留 30 天；  
  - 关闭观测后历史数据仍保留，但新增数据停止采集。

## 来源文档

- [应用观测](../../raw/application-user-guide/application-monitoring/application-observation.md)



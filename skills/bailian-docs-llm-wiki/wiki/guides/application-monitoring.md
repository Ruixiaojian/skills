# application monitoring

应用观测（Application Monitoring）是阿里云百炼平台提供的端到端可观测能力，用于追踪应用内部调用链路、分析模型响应延时、查看推理过程及 [Token](../concepts/token.md) 消耗等关键指标。该功能基于 OpenTelemetry 架构实现，数据同步频率为分钟级，适用于调试、性能优化与真实场景评测。> **注意：应用观测目前暂无 API 接口**，所有操作需通过控制台完成，详见 [应用观测](../../raw/application-user-guide/application-monitoring/application-observation.md)。

## 支持的模型/功能

- **支持的应用类型**：智能体应用、工作流应用、高代码应用（但高代码应用仅上报 `CHAIN` 根节点，[不支持内部链路追踪](../../raw/application-user-guide/application-monitoring/application-observation.md)）。
- **不支持的应用**：通过 Assistant API 创建的智能体应用（[原文明确说明](../../raw/application-user-guide/application-monitoring/application-observation.md)）。
- **可观测节点类型**：
  - 通用节点：`CHAIN`（根节点，名称如 `AgentApp`/`WorkflowApp`/`FullCodeApp`）、`LLM`、`RETRIEVER`（含 `TextRetriever`/`VectorRetriever`）、`EMBEDDING`、`RERANKER`、`REWRITER`、`GUARDRAIL`、`TOOL`；
  - 工作流专属节点：`START`、`END`、`API`、`CLASSIFIER`、`TEXT_CONVERTER`、`SCRIPT`、`CONDITION`、`FUNCTION_COMPUTE`、`APP_FLOW`；
  - 智能体专属节点：`AGENT`；
- **附加能力**：Span 数据导出（JSONL/Excel）、添加至评测集、多维度标签标注（布尔/分类/数字/文本）、交互式展开追踪链路。

> **注意**：文档中关于 `FullCodeApp` 的说明存在潜在矛盾——正文称“不支持追踪其内部调用链路”，但附录又将其列为 `CHAIN` 类型节点。实际行为以 [应用观测](../../raw/application-user-guide/application-monitoring/application-observation.md) 中“高代码应用”章节为准：仅上报根节点，无嵌套子节点。

## 关键参数

| 参数 | 说明 | 来源 |
|------|------|------|
| **Request ID / Trace ID / Span ID** | 用于精确检索单次调用链路，可在节点详情页点击“查看 ID”获取 | [应用观测](../../raw/application-user-guide/application-monitoring/application-observation.md) |
| **延时（ms）** | LLM 节点延时包含完整输出过程；平均首 [Token](../concepts/token.md) 耗时专用于流式调用场景 | [应用观测](../../raw/application-user-guide/application-monitoring/application-observation.md) |
| **[Token](../concepts/token.md) 总量** | = 输入 Token + 输出 Token；Embedding 节点 Token 量仅统计向量化输入 | [应用观测](../../raw/application-user-guide/application-monitoring/application-observation.md) |
| **状态** | `正常` 或 `错误`（含细分错误类型） | [应用观测](../../raw/application-user-guide/application-monitoring/application-observation.md) |

## 使用方式

1. **前提配置**（主账号或已授权子账号操作）：
   - 授权可观测链路 OpenTelemetry 服务角色权限；
   - 开通 OpenTelemetry 服务；
   - 初始化 LogStore 存储（开通后通常分钟级生效）；
   > 子账号需额外配置 `AliyunBailianFullAccess`、页面权限及 `ram:CreateServiceLinkedRole` 策略，详见 [应用观测](../../raw/application-user-guide/application-monitoring/application-observation.md)。

2. **启用观测**：
   - 进入 [应用观测](https://bailian.console.aliyun.com/tab=app?tab=app#/app-observe)，点击“选择被观测的应用” → “添加”；
   - **仅已发布且归属当前业务空间的应用可见**；未发布应用需先通过“管理应用” → “发布”。

3. **数据查看与筛选**：
   - 支持三种 Span 展示模式：`Root Span`（默认）、`All Span`、`Model Span`；
   - 过滤器支持按状态、Span Name、输入/输出关键词、延时、Token 量、标签等条件组合筛选；
   - 可按 Request ID/Trace ID/Span ID 搜索，时间范围最长 30 天。

4. **高级操作**：
   - **导出数据**：Trace 列表页右上角支持 JSONL/Excel 导出；
   - **添加到评测集**：支持批量 Span 导入，字段映射最多 50 个；
   - **数据标注**：与评测系统共享标签体系，支持四类标注类型并实时保存。

## 限制和注意事项

- **功能限制**：
  - 无公开 API，无法程序化接入；
  - 不支持[长期记忆](../concepts/long-term-memory.md)（Long-term Memory）中的检索过程观测；
  - 高代码应用无法观测内部节点，仅上报 `FullCodeApp` 根节点；
  - TextRetriever / VectorRetriever 默认返回 100 个切片，**不支持数量调整**。

- **配置与权限**：
  - 必须使用主账号首次开通，或确保子账号已获完整权限（含创建服务关联角色）；
  - 应用观测本身免费，但底层 OpenTelemetry 存储与计算按量计费，费用独立于百炼资源包。

- **数据时效性**：
  - 指标同步延迟约 1–3 分钟；
  - 监控统计支持按分钟/小时/天聚合，最长回溯 30 天；
  - 关闭观测后历史数据停止同步，重新开启仅采集新增数据。

- **开发适配（高代码应用）**：
  - 需在代码中集成 AgentScope-AI 的 `Tracing` 模块；
  - 部署时必须添加 `--telemetry enable` 启动参数，否则无数据上报。

## 来源文档

- [应用观测](../../raw/application-user-guide/application-monitoring/application-observation.md)



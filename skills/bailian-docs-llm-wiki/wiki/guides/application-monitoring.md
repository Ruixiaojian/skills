# application monitoring

应用观测（Application Monitoring）是阿里云百炼平台提供的端到端可观测能力，用于追踪和分析智能体、工作流及高代码类应用的内部执行链路。它支持查看调用延时、[Token](../concepts/token.md) 消耗、模型思考过程及各节点状态，并提供分钟级指标聚合与原始 Span 数据导出。该功能依赖 OpenTelemetry 服务实现数据采集与存储，**当前不提供 API 接口**，所有操作需通过控制台完成 [应用观测](../../raw/application-user-guide/application-monitoring/application-observation.md)。

## 支持的模型/功能

- **支持的应用类型**：智能体应用、工作流应用、高代码应用（但高代码应用仅上报 `FullCodeApp` 根节点，[不支持内部链路追踪](../../raw/application-user-guide/application-monitoring/application-observation.md)）。
- **不支持的应用**：通过 Assistant API 创建的智能体应用 [应用观测](../../raw/application-user-guide/application-monitoring/application-observation.md)。
- **核心可观测能力**：
  - 完整调用链路（Trace）可视化，支持 Root Span / All Span / Model Span 三种视图模式；
  - 节点级细粒度指标：延时、输入/输出 [Token](../concepts/token.md) 量、状态（正常/错误）、Request ID / Trace ID / Span ID；
  - 内置节点类型覆盖 RAG 全流程（如 `EMBEDDING`、`VectorRetriever`、`RERANKER`、`LLM`、`GUARDRAIL`）及工作流控制节点（如 `CONDITION`、`API`、`CLASSIFIER`）；
  - 支持将 Span 数据一键导入评测集，并与标签管理系统联动进行标注。

> **注意**：文档中明确说明“应用观测目前暂无API”，但部分用户可能误以为可通过 SDK 或 REST API 接入；实际所有数据消费必须经由控制台界面或导出 JSONL/Excel 后离线处理。

## 关键参数

| 参数 | 说明 | 来源 |
|------|------|------|
| `Request ID` / `Trace ID` / `Span ID` | 用于跨系统关联与精准检索，可在节点详情页点击「查看 ID」获取 | [应用观测](../../raw/application-user-guide/application-monitoring/application-observation.md) |
| `延时` | LLM 节点的「调用时长」包含流式响应全过程；CHAIN 级延时为整体端到端耗时 | [应用观测](../../raw/application-user-guide/application-monitoring/application-observation.md) |
| `Token总量` | = 输入 [Token](../concepts/token.md) + 输出 Token；EMBEDDING 节点 Token 量仅统计向量化输入 | [应用观测](../../raw/application-user-guide/application-monitoring/application-observation.md) |
| `平均首Token耗时` | 仅对流式调用生效，反映模型首 token 生成延迟 | [应用观测](../../raw/application-user-guide/application-monitoring/application-observation.md) |

## 使用方式

1. **前提配置**（主账号或已授权子账号）：
   - 授权 `AliyunBailianFullAccess` 及 `应用观测-操作` 页面权限；
   - 开通可观测链路 OpenTelemetry 服务并初始化 LogStore；
   - 高代码应用需在部署时显式添加 `--telemetry enable` 参数，并集成 AgentScope-AI 的 [Tracing 模块](https://github.com/agentscope-ai/agentscope-runtime/tree/main/src/agentscope_runtime/engine/tracing)。

2. **启用观测**：
   - 进入 [应用观测](../../raw/application-user-guide/application-monitoring/application-observation.md) 页面 → 「应用观测配置」完成权限与服务开通；
   - 在「选择被观测的应用」中添加已发布的应用（未发布应用不可见）；
   - 观测开启后，所有 Prompt 请求自动上报，数据同步频率为分钟级。

3. **数据查看与操作**：
   - 在 Span 列表页使用过滤器按状态、Span Name、输入/输出关键词、延时、Token 量或自定义标签筛选；
   - 单击节点名称展开详情，查看原始数据、标注记录及嵌套子节点；
   - 支持导出当前筛选结果为 JSONL 或 Excel；
   - 在「监控统计」页签查看调用次数、失败率、Token 趋势、平均首 Token 耗时等聚合图表（时间范围最长 30 天，粒度支持分钟/小时/天）。

## 限制和注意事项

- **功能限制**：
  - 不支持 Assistant API 创建的智能体应用；
  - 不支持[长期记忆](../concepts/long-term-memory.md)（Long-term Memory）中的检索过程观测；
  - 高代码应用无法追踪内部节点，仅暴露 `FullCodeApp` 根节点；
  - 文档明确指出「应用观测目前暂无API」，所有数据获取必须依赖控制台或导出文件。

- **权限与部署要求**：
  - 子账号需额外配置 `CreateServiceLinkedRole` 策略才能完成服务角色授权；
  - 高代码应用若未启用 `--telemetry enable` 或未集成 Tracing 模块，将无任何可观测数据上报。

- **计费说明**：
  - 应用观测功能本身免费；
  - 所有采集数据存储于 OpenTelemetry 服务，按该服务计费规则收费（详见 [OpenTelemetry 计费说明](https://help.aliyun.com/zh/arms/tracing-analysis/product-overview/untitled-document-1697525445039)）。

## 来源文档

- [应用观测](../../raw/application-user-guide/application-monitoring/application-observation.md)



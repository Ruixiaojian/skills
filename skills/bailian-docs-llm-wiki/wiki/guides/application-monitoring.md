# application monitoring

应用监控（Application Monitoring）是阿里云百炼平台提供的端到端可观测能力，用于追踪智能体、工作流及高代码类应用的内部执行链路，覆盖向量生成、知识检索、大模型调用等关键节点，并采集延时、[Token](../concepts/token.md) 用量、状态码等核心指标。数据同步频率为分钟级，支持按 Trace ID / Span ID / Request ID 快速定位问题，适用于性能分析、成本优化与线上评测样本构建。该功能当前仅提供控制台界面，**暂无公开 API 接口**，详见 [应用观测](../../raw/application-user-guide/application-monitoring/application-observation.md)。

## 支持的模型/功能

- **支持的应用类型**：智能体应用、工作流应用、高代码应用（但高代码应用仅上报 `CHAIN` 根节点，[不支持内部链路追踪](../../raw/application-user-guide/application-monitoring/application-observation.md)）。
- **不支持的应用**：通过 Assistant API 创建的智能体应用（见 [应用观测](../../raw/application-user-guide/application-monitoring/application-observation.md) 中的明确限制说明）。
- **可观测节点类型**：
  - 基础节点：`CHAIN`（根节点，名称如 `AgentApp`/`WorkflowApp`/`FullCodeApp`）、`LLM`、`RETRIEVER`（含 `TextRetriever`/`VectorRetriever`）、`EMBEDDING`、`RERANKER`、`REWRITER`；
  - 工作流专属节点：`START`、`API`、`CLASSIFIER`、`CONDITION`、`FUNCTION_COMPUTE`、`END`；
  - 安全与扩展节点：`TOOL`（[插件](../concepts/plugin.md)调用）、`GUARDRAIL`（绿网内容审核）；
  - 注意：`KnowledgeRetriever` 下的子节点（如 `TextRetriever`）才实际触发可观测行为；[长期记忆](../concepts/long-term-memory.md)中的检索**暂不支持观测**（参见 [应用观测](../../raw/application-user-guide/application-monitoring/application-observation.md) 附录说明）。

> **注意**：文档中对 `FullCodeApp` 的描述存在隐含矛盾——正文称“目前不支持追踪其内部调用链路”，但附录表格又将其列为高代码应用的 `CHAIN` 节点类型。实际行为以控制台表现为准：高代码应用仅上报顶层 `CHAIN` Span，无嵌套子 Span。此为功能限制，非文档错误。

## 关键参数

| 参数名 | 含义 | 说明 |
|--------|------|------|
| `Trace ID` | 全局唯一调用链标识 | 用于跨节点关联同一请求的完整生命周期 |
| `Span ID` | 单个操作单元唯一标识 | 每个节点（如 `LLM`、`RETRIEVER`）对应一个 Span ID |
| `Request ID` | 应用层请求标识 | 通常由百炼网关生成，与用户侧请求强绑定 |
| `延时（ms）` | 节点执行耗时 | `LLM` 节点延时包含流式响应首 [Token](../concepts/token.md) 及全文生成时间；`平均首Token耗时` 仅在流式场景下统计 |
| `Token总量` | 输入 [Token](../concepts/token.md) + 输出 Token 总和 | `EMBEDDING` 节点 Token 量指向量化输入长度；`LLM` 节点指模型侧总 Token 数 |
| `状态` | 执行结果 | `正常` 或 `错误`（错误可进一步细分为 `ManualIntervention`/`SystemIntervention` 等） |

所有字段均支持在 Span 列表页通过**过滤器**进行条件筛选（如“延时 > 5000”、“输出包含‘拒绝’”），也支持导出为 JSONL 或 Excel 进行离线分析。

## 使用方式

1. **前提配置（一次性）**  
   首次使用需完成三项授权与开通：
   - 授权可观测链路 OpenTelemetry 服务角色权限；
   - 开通可观测链路 OpenTelemetry 服务；
   - 初始化 OpenTelemetry 存储 LogStore。  
   > 主账号操作分钟级生效；子账号需额外配置 `AliyunBailianFullAccess` + `应用观测-操作` 页面权限 + `CreateServiceLinkedRole` 系统策略（详细步骤见 [应用观测](../../raw/application-user-guide/application-monitoring/application-observation.md)）。

2. **启用观测**  
   - 进入 [应用观测](https://bailian.console.aliyun.com/tab=app?tab=app#/app-observe)，点击 **选择被观测的应用** → **添加**；
   - 应用必须已**发布**且属于当前业务空间；
   - 添加后自动开始分钟级数据同步；关闭观测则停止同步（历史数据保留，新增数据不再采集）。

3. **查看与分析**  
   - 在 Span 列表页，支持三种视图模式：`Root Span`（默认）、`All Span`（平铺所有节点）、`Model Span`（仅含 `LLM` 节点）；
   - 单击节点名称展开详情，查看原始输入/输出、标注记录、嵌套子 Span；
   - 支持按时间范围（最长 30 天）、聚合粒度（分钟/小时/天）查看**监控统计**页签中的趋势图（调用次数、失败率、Token 总量、平均延时等）。

4. **高级操作**  
   - **导出数据**：Trace 列表页右上角 → 导出 JSONL 或 Excel；
   - **添加到评测集**：批量选中 Span → 映射字段（最多 50 个）→ 追加或覆盖导入；
   - **数据标注**：支持布尔值、分类、数字、文本四类标签，与评测集标签系统共享。

## 限制和注意事项

- **功能限制**：
  - 当前**无 API 接口**，全部操作依赖控制台（见 [应用观测](../../raw/application-user-guide/application-monitoring/application-observation.md) 明确声明）；
  - 不支持 Assistant API 创建的智能体应用；
  - 高代码应用仅上报 `FullCodeApp` 根节点，无法观测内部[函数调用](../concepts/function-calling.md)或自定义逻辑；
  - [长期记忆](../concepts/long-term-memory.md)（Long-term Memory）检索过程不可观测；
  - `TextRetriever`/`VectorRetriever` 默认返回 100 个切片，数量不可配置。

- **数据时效性**：
  - 数据同步延迟为**分钟级**，不适用于毫秒级实时告警场景；
  - 监控统计图表支持最长 30 天历史数据查询，超出范围不可回溯。

- **计费说明**：
  - 应用监控功能本身**不收取额外费用**；
  - 所有追踪数据存储于可观测链路 OpenTelemetry 服务，按该服务标准计费（详见 [计费说明](https://help.aliyun.com/zh/arms/tracing-analysis/product-overview/untitled-document-1697525445039)）。

- **权限与部署要求（高代码应用）**：
  - 必须在代码中集成 AgentScope-AI 的 `Tracing` 模块；
  - 部署时需显式添加 `--telemetry enable` 参数，否则无任何数据上报（见 [应用观测](../../raw/application-user-guide/application-monitoring/application-observation.md) 常见问题）。

## 来源文档

- [应用观测](../../raw/application-user-guide/application-monitoring/application-observation.md)



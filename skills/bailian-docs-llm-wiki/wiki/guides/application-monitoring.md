# application monitoring

应用观测（Application Monitoring）是阿里云百炼平台提供的端到端可观测能力，用于追踪智能体、工作流及高代码类应用的内部执行链路，支持查看调用延时、[Token](../concepts/token.md) 消耗、模型思考过程及各节点状态。数据以分钟级频率同步至可观测链路 OpenTelemetry 服务，当前**不提供 API 接口**，仅通过控制台使用。详细背景与设计目标见 [应用观测](../../raw/application-user-guide/application-monitoring/application-observation.md)。

## 支持的模型/功能

- **支持的应用类型**：智能体应用、工作流应用、高代码应用（但高代码应用仅上报根节点 `FullCodeApp`，[不支持内部链路追踪](../../raw/application-user-guide/application-monitoring/application-observation.md)）。
- **不支持的应用**：通过 Assistant API 创建的智能体应用（[原文明确说明](../../raw/application-user-guide/application-monitoring/application-observation.md)）。
- **核心可观测能力**：
  - 完整调用链路（Trace）可视化，支持 `Root Span` / `All Span` / `Model Span` 三种视图模式；
  - 节点级指标：延时、输入/输出 [Token](../concepts/token.md) 量、状态（正常/错误）、Request ID / Trace ID / Span ID；
  - 交互式展开：支持逐层展开 `CHAIN`、`LLM`、`RETRIEVER` 等嵌套节点；
  - 数据标注：支持布尔值、分类、数字、文本四类标签，与评测集标签系统共享；
  - 评测集集成：可将 Span 数据批量导入评测集，支持字段映射与追加/覆盖策略。

> **注意**：文档中对 `CHAIN` 节点的说明在“智能体应用”和“工作流应用”两节中重复且内容一致，但未明确区分语义差异；实际使用中应以节点 `Name`（如 `AgentApp` vs `WorkflowApp`）和上下文为准，避免误判调用来源。

## 关键参数

| 参数 | 说明 | 来源依据 |
|------|------|----------|
| **Trace ID / Span ID / Request ID** | 用于精准检索与关联分析；需在节点详情页点击“查看 ID”获取 | [应用观测](../../raw/application-user-guide/application-monitoring/application-observation.md) |
| **[Token](../concepts/token.md) 总量** | = 输入 Token + 输出 Token；`EMBEDDING` 节点统计向量化 Token 数，`LLM` 节点统计推理 Token 数 | [附录：名词解释](../../raw/application-user-guide/application-monitoring/application-observation.md) |
| **平均首 Token 耗时** | 仅适用于流式调用场景，衡量首 Token 返回延迟 | [监控统计](../../raw/application-user-guide/application-monitoring/application-observation.md) |
| **Span Name** | 如 `AgentApp`、`WorkflowApp`、`TextRetriever`、`VectorRetriever`、`LLM` 等，用于筛选与分类 | [支持的节点类型](../../raw/application-user-guide/application-monitoring/application-observation.md) |

## 使用方式

1. **前提配置**（主账号或已授权子账号操作）：
   - 授权可观测链路 OpenTelemetry 服务角色权限；
   - 开通 OpenTelemetry 服务；
   - 初始化 LogStore 存储（开通后通常分钟级生效）；
   > 子账号需额外配置 `AliyunBailianFullAccess`、页面权限及 `ram:CreateServiceLinkedRole` 权限，详见 [常见问题](../../raw/application-user-guide/application-monitoring/application-observation.md)。

2. **启用观测**：
   - 进入 [应用观测](https://bailian.console.aliyun.com/tab=app?tab=app#/app-observe)，单击“选择被观测的应用” → “添加”；
   - **仅已发布且归属当前业务空间的应用可见**；未发布应用需先通过“管理应用” → “发布”。

3. **数据查看与分析**：
   - 在 Span 列表页使用过滤器（按状态、Span Name、输入/输出关键词、延时、Token 量、标签等）；
   - 单击节点名称展开详情，查看原始数据、标注记录、下游子节点；
   - 切换至“监控统计”页签，按分钟/小时/天粒度查看调用次数、失败率、Token 趋势、平均延时等。

4. **导出与评测集成**：
   - 支持 JSONL 或 Excel 格式导出当前筛选结果；
   - 可批量选中 Span，映射字段后导入评测集（最多 50 个字段映射）。

## 限制和注意事项

- **无 API 支持**：应用观测目前暂无开放 API，所有操作必须通过控制台完成（[原文标题](../../raw/application-user-guide/application-monitoring/application-observation.md) 明确声明）。
- **高代码应用限制**：虽可开启观测，但仅上报 `FullCodeApp` 根节点，无法追踪其内部逻辑；需在代码中显式集成 AgentScope-AI 的 `Tracing` 模块，并部署时添加 `--telemetry enable` 参数。
- **知识库检索限制**：`KnowledgeRetriever` 下的 `TextRetriever` 和 `VectorRetriever` 默认返回 100 个切片，**不支持数量调整**；[长期记忆](../concepts/long-term-memory.md)中的检索过程**暂不支持观测**。
- **计费说明**：应用观测功能本身免费，但底层依赖 OpenTelemetry 服务存储与计算，相关费用按 [OpenTelemetry 计费说明](https://help.aliyun.com/zh/arms/tracing-analysis/product-overview/untitled-document-1697525445039) 结算。
- **数据时效性**：指标同步频率为**分钟级**，非实时；Trace 数据最长保留 30 天。

## 来源文档

- [应用观测](../../raw/application-user-guide/application-monitoring/application-observation.md)



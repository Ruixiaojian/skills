# application monitoring

应用观测（Application Monitoring）是阿里云百炼平台提供的端到端可观测能力，用于追踪和分析智能体、工作流及高代码类应用的内部执行链路。它支持查看调用延时、Token 消耗、模型思考过程及各节点状态，并提供分钟级指标聚合与原始 Span 数据导出。该功能依赖 OpenTelemetry 服务实现数据采集与存储，**当前不提供 API 接口**，所有操作需通过控制台完成 [应用观测](../../raw/application-user-guide/application-monitoring/application-observation.md)。

## 支持的模型/功能

- **支持的应用类型**：智能体应用、工作流应用、高代码应用（但高代码应用仅上报 `FullCodeApp` 根节点，[不支持内部链路追踪](../../raw/application-user-guide/application-monitoring/application-observation.md)）。
- **不支持的应用**：通过 Assistant API 创建的智能体应用 [应用观测](../../raw/application-user-guide/application-monitoring/application-observation.md)。
- **核心可观测能力**：
  - 调用链路追踪（Root Span / All Span / Model Span 三种视图）
  - 节点级指标：延时、输入/输出 Token 量、状态（正常/错误）、首 Token 耗时
  - 节点类型覆盖全面，包括 `LLM`、`RETRIEVER`（含 `TextRetriever`/`VectorRetriever`）、`EMBEDDING`、`RERANKER`、`TOOL`、`GUARDRAIL`、`CHAIN`、`WORKFLOW` 相关节点（如 `START`/`END`/`CLASSIFIER` 等）
  - 数据标注（布尔/分类/数字/文本类型标签，与评测集标签系统共享）
  - Span 数据一键导入评测集（支持字段映射与追加/覆盖模式）

> **注意**：文档中明确说明“高代码应用目前不支持追踪其内部调用链路”，但同时又列出 `FullCodeApp` 作为 `CHAIN` 类型节点。这与智能体/工作流中 `CHAIN` 可嵌套子节点的语义矛盾，实际使用中高代码应用仅暴露根节点，无子节点展开能力 —— 请以 [应用观测](../../raw/application-user-guide/application-monitoring/application-observation.md) 中“高代码应用”章节描述为准。

## 关键参数

| 参数 | 说明 | 来源 |
|------|------|------|
| **Request ID / Trace ID / Span ID** | 用于精准检索单次调用链路，可在节点详情页点击“查看 ID”获取 | [应用观测](../../raw/application-user-guide/application-monitoring/application-observation.md) |
| **Span Name** | 节点名称，如 `AgentApp`、`WorkflowApp`、`TextRetriever`、`LLM` 等，用于筛选与识别节点类型 | [应用观测](../../raw/application-user-guide/application-monitoring/application-observation.md) |
| **Token 总量 / 输入 Token / 输出 Token** | 均为整型数值，单位为 token 数；`EMBEDDING` 节点的 Token 量指向量化输入长度，`LLM` 节点指 input + output 总和 | [应用观测](../../raw/application-user-guide/application-monitoring/application-observation.md) |
| **延时（调用时长）** | 毫秒级数值，`LLM` 节点延时包含流式响应全过程 | [应用观测](../../raw/application-user-guide/application-monitoring/application-observation.md) |
| **标签（Label）** | 用户自定义标注字段，类型包括布尔、分类、数字、文本；支持在过滤器中按标签类型做条件匹配 | [应用观测](../../raw/application-user-guide/application-monitoring/application-observation.md) |

## 使用方式

1. **前提配置**（仅需一次）：
   - 主账号或具备 `AliyunBailianFullAccess` + `应用观测-操作` + `CreateServiceLinkedRole` 权限的子账号，进入 [应用观测](../../raw/application-user-guide/application-monitoring/application-observation.md) 页面，点击右上角“应用观测配置”，完成 OpenTelemetry 服务授权、开通与 LogStore 初始化。

2. **添加被观测应用**：
   - 应用必须已**发布**且属于当前业务空间；未发布的应用不会出现在添加列表中。

3. **观测与分析**：
   - 在 Span 列表页，可切换 `Root Span`/`All Span`/`Model Span` 视图；
   - 使用过滤器按状态、Span Name、输入/输出关键词、延时、Token 量、标签等条件组合筛选；
   - 单击节点名称展开详情，查看原始请求/响应、上下文、子节点（若存在）；
   - 在“监控统计”页签查看调用次数、失败率、Token 趋势、平均首 Token 耗时等聚合指标（支持分钟/小时/天粒度，最长 30 天）。

4. **数据导出与复用**：
   - 支持 JSONL 或 Excel 格式导出当前筛选结果；
   - 支持将 Span 批量添加至评测集，支持字段映射（最多 50 个字段）与导入策略（追加/覆盖）。

## 限制和注意事项

- **API 限制**：应用观测当前**无开放 API**，所有数据获取与操作均需通过控制台完成 [应用观测](../../raw/application-user-guide/application-monitoring/application-observation.md)。
- **权限要求**：子账号需显式授予 `CreateServiceLinkedRole` 策略才能完成初始配置，详见 [应用观测](../../raw/application-user-guide/application-monitoring/application-observation.md) 中“常见问题”章节。
- **高代码应用限制**：即使开启观测，也**无法看到内部节点与调用量明细**，仅显示 `FullCodeApp` 根节点；需在代码中集成 `AgentScope-AI` 的 Tracing 模块，并部署时启用 `--telemetry enable` 参数才可能上报基础指标。
- **数据延迟**：指标同步频率为**分钟级**，不适用于毫秒级实时诊断。
- **计费说明**：应用观测功能免费，但底层依赖的 OpenTelemetry 服务按日志写入量与存储时长计费，费用归属 OpenTelemetry 产品线。

## 来源文档

- [应用观测](../../raw/application-user-guide/application-monitoring/application-observation.md)



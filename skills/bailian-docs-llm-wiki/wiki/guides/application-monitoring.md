# application monitoring

应用观测（Application Monitoring）是阿里云百炼平台提供的端到端可观测能力，用于追踪智能体、工作流及高代码类应用的内部执行链路，支持查看调用延时、[Token](../concepts/token.md)消耗、模型思考过程及各节点状态。所有数据以分钟级频率同步至可观测链路 OpenTelemetry 服务，当前**不提供 API 接口**，仅通过控制台使用。详细背景与设计目标见 [应用观测](../../raw/application-user-guide/application-monitoring/application-observation.md)。

## 支持的模型/功能

- **支持的应用类型**：智能体应用（Single Agent）、工作流应用（Workflow）和高代码应用（Rich Code），但**不支持通过 Assistant API 创建的智能体应用**（详见 [应用观测](../../raw/application-user-guide/application-monitoring/application-observation.md)）。
- **可观测节点类型**：
  - `CHAIN`（根节点，如 `AgentApp`/`WorkflowApp`/`FullCodeApp`）
  - `LLM`（大模型调用，含输入/输出 [Token](../concepts/token.md) 统计与首 [Token](../concepts/token.md) 耗时）
  - `RETRIEVER`（含 `TextRetriever` 和 `VectorRetriever`，默认返回 100 个切片）
  - `EMBEDDING`、`RERANKER`、`REWRITER`、`TOOL`、`GUARDRAIL`、`API`、`CLASSIFIER` 等工作流专用节点
  - `START`/`END`（工作流生命周期节点）
- **核心功能**：调用链追踪（Trace/Spans）、多维筛选（按状态、Span Name、输入/输出关键词、延时、[Token](../concepts/token.md) 量、标签等）、数据导出（JSONL/Excel）、监控统计（调用次数、失败率、[Token](../concepts/token.md) 趋势、平均延时）、Span 数据一键导入评测集、以及支持布尔/分类/数字/文本四类数据标注。

> **注意**：高代码应用虽可开启观测，但 `FullCodeApp` 节点为黑盒，**不支持展开其内部调用链路**；实际可观测性依赖开发者在代码中集成 AgentScope-AI 的 Tracing 模块并启用 `--telemetry enable` 参数（参见 [应用观测](../../raw/application-user-guide/application-monitoring/application-observation.md) 中“常见问题”部分）。

## 关键参数

| 参数 | 说明 | 备注 |
|------|------|------|
| **Request ID / Trace ID / Span ID** | 用于精准定位单次调用或子链路 | 可在节点详情页点击“查看 ID”获取 |
| **延时（ms）** | LLM 节点延时包含完整响应过程（含流式首 [Token](../concepts/token.md) 时间）；整体应用延时为 Chain 根节点耗时 | “平均首 Token 耗时”仅对流式调用有效 |
| **Token 总量** | = 输入 Token + 输出 Token（LLM 节点）；Embedding 节点 Token 量仅指向量化输入长度 | 所有 Token 统计均基于对应模型 tokenizer 计算 |
| **状态** | `正常` 或 `错误`（后者可进一步按错误类型细分） | 错误类型需结合日志与节点上下文诊断 |
| **标签（Label）** | 支持布尔、分类、数字、文本四类标注，与评测集标签系统共享 | 单个评测集最多支持 50 个字段映射 |

## 使用方式

1. **前提配置**（首次使用必做）：
   - 主账号或已授权子账号访问 [应用观测](https://bailian.console.aliyun.com/tab=app?tab=app#/app-observe)，点击右上角 **应用观测配置**；
   - 完成三步：授权 OpenTelemetry 服务角色 → 开通 OpenTelemetry 服务 → 初始化 LogStore 存储（主账号开通通常分钟级生效；子账号需额外配置 `CreateServiceLinkedRole` 权限，详见 [应用观测](../../raw/application-user-guide/application-monitoring/application-observation.md)）。

2. **启用观测**：
   - 在应用观测页面点击 **选择被观测的应用** > **添加**；
   - 应用必须已**发布**且属于当前业务空间；
   - 添加后自动开始分钟级数据同步；关闭观测则停止同步，重开仅保留新增数据。

3. **查看与分析**：
   - 在 Span 列表页切换筛选模式（`Root Span`/`All Span`/`Model Span`）；
   - 使用过滤器组合条件（如 `状态=错误 AND 延时>5000`）；
   - 点击节点名称展开详情，查看原始数据、标注记录、嵌套子节点；
   - 在 **监控统计** 页签按时间范围（最长 30 天）与粒度（分钟/小时/天）查看趋势图。

4. **扩展操作**：
   - **导出数据**：Trace 列表页右上角支持 JSONL/Excel 导出；
   - **添加到评测集**：批量选择 Span，映射字段后追加或覆盖已有评测集；
   - **数据标注**：在节点详情页点击 **数据标注**，复用统一标签体系。

## 限制和注意事项

- **无 API 支持**：当前仅提供控制台界面，无法通过 SDK 或 HTTP API 集成（明确声明于 [应用观测](../../raw/application-user-guide/application-monitoring/application-observation.md)）。
- **存储与计费**：应用观测功能本身免费，但底层依赖 OpenTelemetry 服务，产生的 Trace 数据存储与查询费用需单独承担（参见 [计费说明](../../raw/application-user-guide/application-monitoring/application-observation.md)）。
- **高代码应用限制**：`FullCodeApp` 节点不可展开，内部逻辑不可见；必须显式集成 AgentScope-AI Tracing 模块并部署时启用 `--telemetry enable`，否则无数据上报。
- **知识库检索盲区**：`KnowledgeRetriever` 下的 `TextRetriever`/`VectorRetriever` 可观测，但**[长期记忆](../concepts/long-term-memory.md)（Long-term Memory）中的检索过程暂不支持观测**。
- **权限要求**：子账号需同时具备 `AliyunBailianFullAccess`、页面级“应用观测-操作”权限及 `ram:CreateServiceLinkedRole` 权限，缺一不可（详细配置步骤见 [应用观测](../../raw/application-user-guide/application-monitoring/application-observation.md)）。

## 来源文档

- [应用观测](../../raw/application-user-guide/application-monitoring/application-observation.md)




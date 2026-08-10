# application monitoring

应用监控（Application Monitoring）是百炼平台提供的可观测性能力，用于端到端追踪智能体、工作流及高代码类应用的内部执行链路，支持查看调用延时、[Token](../concepts/token.md) 消耗、节点状态、模型思考过程等关键指标。数据以分钟级频率同步至可观测链路 OpenTelemetry 存储，所有观测行为均需显式启用且依赖服务关联角色授权。该功能当前**不提供 API 接口**，仅通过控制台交互使用，详见 [应用观测](../../raw/application-user-guide/application-monitoring/application-observation.md)。

## 支持的模型/功能

- **支持的应用类型**：智能体应用（Single Agent）、工作流应用（Workflow）、高代码应用（Rich Code）。  
- **可观测节点类型**：涵盖 `CHAIN`（根节点，如 `AgentApp`/`WorkflowApp`/`FullCodeApp`）、`LLM`（大模型调用）、`RETRIEVER`（含 `TextRetriever`/`VectorRetriever`）、`EMBEDDING`、`RERANKER`、`REWRITER`、`TOOL`、`GUARDRAIL`、`API`、`CLASSIFIER`、`CONDITION` 等数十种节点，完整覆盖 RAG、插件调用、意图识别、安全拦截等典型流程。  
- **核心功能**：  
  - 调用链路展开与节点详情查看（含原始输入/输出、延时、[Token](../concepts/token.md) 量）；  
  - 多维度筛选（按状态、Span Name、输入/输出关键词、延时、[Token](../concepts/token.md) 量、标签等）；  
  - 监控统计（调用次数、失败率、Token 总量、首 Token 耗时、平均调用时长）；  
  - 数据导出（JSONL / Excel）；  
  - Span 数据一键导入评测集（支持字段映射与追加/覆盖）；  
  - 标签标注（布尔值、分类、数字、文本四类标签类型，与评测系统共享标签管理）。  

> **注意**：高代码应用虽可添加至观测列表，但 `FullCodeApp` 类型节点**不支持展开其内部调用链路**，仅显示顶层调用概要；其详细追踪需在代码中集成 AgentScope-AI 的 [Tracing模块](https://github.com/agentscope-ai/agentscope-runtime/tree/main/src/agentscope_runtime/engine/tracing) 并部署时启用 `--telemetry enable` 参数 —— 此要求与 [应用观测](../../raw/application-user-guide/application-monitoring/application-observation.md) 中“高代码应用”章节说明一致。

## 关键参数

| 参数 | 说明 | 来源 |
|------|------|------|
| **Request ID / Trace ID / Span ID** | 唯一标识一次调用或子操作，用于精准检索与问题定位；可通过节点详情页“查看 ID”获取 | [应用观测](../../raw/application-user-guide/application-monitoring/application-observation.md) |
| **延时（调用时长）** | 单位毫秒，LLM 节点延时包含流式响应全过程；CHAIN 节点延时为整个应用执行总耗时 | [应用观测](../../raw/application-user-guide/application-monitoring/application-observation.md) |
| **Token 总量 / 输入 Token / 输出 Token** | LLM 节点中为 `input_tokens + output_tokens`；EMBEDDING 节点中为向量化输入的 Token 数 | [应用观测](../../raw/application-user-guide/application-monitoring/application-observation.md) |
| **状态** | 分为 `正常` 和 `错误`，错误类型可进一步细分（如 Guardrail 拦截、Tool 调用失败等） | [应用观测](../../raw/application-user-guide/application-monitoring/application-observation.md) |

## 使用方式

1. **前提配置**（首次使用必做）：  
   - 主账号或具备 `AliyunBailianFullAccess` + `应用观测-操作` 权限的子账号，进入 [应用观测](../../raw/application-user-guide/application-monitoring/application-observation.md) 页面右上角点击 **应用观测配置**；  
   - 授权 `AliyunServiceRoleForOpenTelemetry` 服务关联角色；  
   - 开通可观测链路 OpenTelemetry 服务，并初始化对应 LogStore（通常分钟级生效）。  

2. **启用观测**：  
   - 在 [应用观测](../../raw/application-user-guide/application-monitoring/application-observation.md) 列表中点击 **选择被观测的应用** > **添加**；  
   - **仅已发布且归属当前业务空间的应用可见**；未发布应用需先通过“管理应用”→“发布”操作启用。  

3. **查看与分析**：  
   - 在 Span 列表页切换 **Root Span / All Span / Model Span** 视图模式；  
   - 使用过滤器添加条件（如 `延时 > 5000`、`状态 = 错误`、`标签 = high_latency`）；  
   - 单击节点名称展开详情，查看原始数据、标注记录及嵌套子节点；  
   - 进入 **监控统计** 页签，按分钟/小时/天粒度查看趋势图表。  

4. **高级操作**：  
   - 导出数据：在 Trace 列表页右上角点击 **导出数据**；  
   - 添加评测集：勾选 Span → **批量操作** → **添加到评测集** → 配置目标集与字段映射（最多 50 个字段）；  
   - 标注数据：在节点详情页点击 **数据标注**，选择或新建标签并填写值（自动保存）。  

## 限制和注意事项

- **功能限制**：  
  - 应用监控**无公开 API**，无法程序化接入或自动化触发；所有操作必须通过控制台完成；  
  - **不支持通过 Assistant API 创建的智能体应用**；  
  - **[长期记忆](../concepts/long-term-memory.md)（Long-term Memory）中的检索过程不可观测**；  
  - 高代码应用内部逻辑需自行集成 Tracing SDK 并启用 `--telemetry enable` 才能上报细粒度数据。  

- **权限与部署注意**：  
  - 子账号开通需额外授予 `ram:CreateServiceLinkedRole` 权限（见 [应用观测](../../raw/application-user-guide/application-monitoring/application-observation.md) “常见问题”章节）；  
  - 观测数据存储于 OpenTelemetry 服务，**产生实际费用**（应用监控功能本身免费，但底层日志存储与分析计费）；  
  - 关闭观测后历史数据**不再新增**，重新启用仅同步后续调用数据。  

- **数据时效性**：  
  - 数据同步延迟约 **1–3 分钟**（高峰期可能延长），不适用于实时告警场景；  
  - 最长可查询 **30 天内** 的历史数据。

## 来源文档

- [应用观测](../../raw/application-user-guide/application-monitoring/application-observation.md)



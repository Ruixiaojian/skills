# application monitoring

应用监控（Application Monitoring）是阿里云百炼平台提供的可观测性能力，用于端到端追踪智能体、工作流及高代码类应用的内部执行链路。它支持可视化查看调用拓扑、节点级延时、[Token](../concepts/token.md) 消耗、模型响应过程等关键指标，数据更新频率为分钟级。该功能依赖 OpenTelemetry 服务进行数据采集与存储，**当前不提供 API 接口**，所有操作需通过控制台完成。

## 支持的模型/功能

- **支持的应用类型**：智能体应用、工作流应用、高代码应用（[原文标题](../../raw/application-user-guide/application-monitoring/application-observation.md)）  
- **可观测节点类型**：
  - `CHAIN`（根节点，如 `AgentApp` / `WorkflowApp` / `FullCodeApp`）
  - `LLM`（大模型推理，含输入/输出 [Token](../concepts/token.md) 统计与首 [Token](../concepts/token.md) 耗时）
  - `RETRIEVER`（含 `TextRetriever` 和 `VectorRetriever`，均默认返回 100 个切片）
  - `EMBEDDING`、`RERANKER`、`REWRITER`、`TOOL`、`GUARDRAIL`、`API`、`CONDITION` 等工作流节点
- **核心功能**：
  - 多维度 Span 数据筛选（按状态、延时、Token 量、标签等）
  - 互动式调用链展开与 ID（Request ID / Trace ID / Span ID）定位
  - 监控统计页（调用次数、失败率、平均延时、Token 趋势等）
  - 数据导出（JSONL / Excel）
  - 直接添加 Span 到评测集（支持字段映射与导入策略）
  - 数据标注（布尔/分类/数字/文本类型，与评测标签系统共享）

> **注意**：高代码应用虽可开启观测，但 `FullCodeApp` 类型节点**不支持内部调用链路追踪**，仅记录顶层调用事件；其统计数据缺失需排查是否在代码中启用 `Tracing` 模块并部署时添加 `--telemetry enable` 参数（[原文标题](../../raw/application-user-guide/application-monitoring/application-observation.md)）。

## 关键参数

| 参数 | 说明 | 来源 |
|------|------|------|
| **延时（调用时长）** | LLM 节点包含完整流式响应时间；CHAIN 节点为端到端耗时 | [原文标题](../../raw/application-user-guide/application-monitoring/application-observation.md) |
| **Token 总量** | = 输入 Token + 输出 Token；Embedding 节点仅统计向量化 Token 数 | [原文标题](../../raw/application-user-guide/application-monitoring/application-observation.md) |
| **首 Token 耗时** | 仅对流式调用生效，定义为首个 Token 返回时间 | [原文标题](../../raw/application-user-guide/application-monitoring/application-observation.md) |
| **Span ID / Trace ID / Request ID** | 用于跨节点关联与问题定位；需点击节点名称 → 展开详情 → “查看 ID” 获取 | [原文标题](../../raw/application-user-guide/application-monitoring/application-observation.md) |

## 使用方式

1. **前提配置**（主账号或已授权子账号）：
   - 授权可观测链路 OpenTelemetry 服务角色权限
   - 开通 OpenTelemetry 服务
   - 初始化 LogStore 存储（高峰期开通可能延迟数分钟）

2. **启用观测**：
   - 进入 [应用观测](https://bailian.console.aliyun.com/tab=app?tab=app#/app-observe) 页面 → 右上角「应用观测配置」完成上述授权
   - 「选择被观测的应用」→ 添加已**发布**且属于当前业务空间的应用

3. **查看与分析**：
   - 在 Span 列表页切换筛选模式（Root Span / All Span / Model Span）
   - 使用过滤器按状态、Span Name、输入/输出关键词、延时、Token 量、标签等条件组合筛选
   - 单击节点名称查看详情、原始数据、标注记录；支持展开嵌套子节点
   - 在「监控统计」页签按分钟/小时/天粒度查看趋势图（最长 30 天）

4. **高级操作**：
   - 批量导出数据（JSONL 或 Excel）
   - 将 Span 添加至评测集（支持追加/覆盖、50 字段映射上限）
   - 对 Span 添加结构化标签（布尔/分类/数字/文本）

## 限制和注意事项

- **不支持的应用**：通过 Assistant API 创建的智能体应用（[原文标题](../../raw/application-user-guide/application-monitoring/application-observation.md)）  
- **无 API 支持**：当前仅提供控制台界面，不可编程调用  
- **数据延迟**：指标同步频率为分钟级，非实时  
- **高代码应用限制**：`FullCodeApp` 节点无法展示内部节点，需自行集成 AgentScope-AI 的 Tracing 模块并启用 `--telemetry enable`  
- **[长期记忆](../concepts/memory.md)不可见**：知识库检索可观测，但[长期记忆](../concepts/memory.md)中的检索过程暂不支持（[原文标题](../../raw/application-user-guide/application-monitoring/application-observation.md)）  
- **计费说明**：应用监控功能本身免费，但底层 OpenTelemetry 存储与计算资源按 [ARMs Tracing Analysis](https://help.aliyun.com/zh/arms/tracing-analysis/product-overview/untitled-document-1697525445039) 计费  

> **注意**：文档中提及“应用观测目前暂无API”，但部分旧版 SDK 文档曾暗示实验性接口存在；请以当前控制台行为为准，避免依赖未公开接口（[原文标题](../../raw/application-user-guide/application-monitoring/application-observation.md)）。

## 来源文档

- [应用观测](../../raw/application-user-guide/application-monitoring/application-observation.md)



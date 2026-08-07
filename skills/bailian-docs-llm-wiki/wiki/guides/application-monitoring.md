# application monitoring

应用观测（Application Monitoring）是阿里云百炼平台提供的端到端可观测能力，用于追踪智能体、工作流及高代码类应用的内部执行链路，支持查看调用延时、[Token](../concepts/token.md) 消耗、模型思考过程等关键指标。数据以分钟级频率同步至可观测链路 OpenTelemetry 服务，当前**不提供 API 接口**，全部操作需通过控制台完成。详细背景与设计目标参见 [应用观测](../../raw/application-user-guide/application-monitoring/application-observation.md)。

## 支持的模型/功能

- **支持的应用类型**：智能体应用、工作流应用、高代码应用（但高代码应用仅上报 `FullCodeApp` 根节点，[不支持内部链路追踪](../../raw/application-user-guide/application-monitoring/application-observation.md)）。
- **不支持的应用**：通过 Assistant API 创建的智能体应用（[明确排除](../../raw/application-user-guide/application-monitoring/application-observation.md)）。
- **可观测节点类型**：
  - 通用节点：`CHAIN`（根节点，如 `AgentApp`/`WorkflowApp`/`FullCodeApp`）、`LLM`、`RETRIEVER`（含 `TextRetriever`/`VectorRetriever`）、`EMBEDDING`、`RERANKER`、`REWRITER`、`GUARDRAIL`、`TOOL`；
  - 工作流专属节点：`START`、`END`、`API`、`CLASSIFIER`、`TEXT_CONVERTER`、`SCRIPT`、`CONDITION`、`FUNCTION_COMPUTE`、`APP_FLOW`；
  - 智能体专属节点：`AGENT`。
- **附加能力**：Span 数据导出（JSONL/Excel）、添加至评测集、多维度标签标注（布尔/分类/数字/文本）、基于 Request ID/Trace ID/Span ID 的精准检索。

> **注意**：文档中对 `CHAIN` 节点的说明在「智能体应用」和「工作流应用」两节中重复且内容一致，属冗余表述；但关于 `FullCodeApp` 的限制描述（“目前不支持追踪其内部调用链路”）与高代码应用章节末尾的排查建议（要求用户在代码中启用 `Tracing` 模块并传入 `--telemetry enable`）存在潜在矛盾——后者暗示高代码应用**可支持深度追踪**，而前者断言不支持。实际能力以 [应用观测](../../raw/application-user-guide/application-monitoring/application-observation.md) 中“高代码应用”小节末尾的部署要求为准。

## 关键参数

| 参数 | 说明 | 备注 |
|------|------|------|
| **延时（调用时长）** | LLM 节点包含完整响应过程（含流式首 [Token](../concepts/token.md) 时间），CHAIN 节点为全链路耗时 | 单位：毫秒 |
| **[Token](../concepts/token.md) 总量** | `输入Token数 + 输出Token数`（LLM 节点）；Embedding 节点仅统计向量化输入 Token 数 | 可按输入/输出/总量分别查看 |
| **平均首 Token 耗时** | 仅在流式调用场景下有效，指从请求发出到首个 Token 返回的时间 | 监控统计页签提供 |
| **状态** | `正常` 或 `错误`；错误类型可进一步细分（如 Guardrail 拦截、LLM 调用失败等） | 支持按状态筛选 |
| **标签（Label）** | 用户自定义标注字段，类型包括布尔值、分类、数字、文本，与评测系统共享 | 最多支持 50 个字段映射 |

## 使用方式

1. **前提配置**（首次使用必做）：
   - 主账号或已授权子账号访问 [应用观测配置](https://bailian.console.aliyun.com/tab=app?tab=app#/app-observe) 页面；
   - 授权可观测链路 OpenTelemetry 服务角色权限；
   - 开通 OpenTelemetry 服务并初始化 LogStore 存储（[详见配置流程](../../raw/application-user-guide/application-monitoring/application-observation.md)）。

2. **启用观测**：
   - 进入应用观测页面 → “选择被观测的应用” → “添加”；
   - **仅已发布且归属当前业务空间的应用可见**（未发布应用需先通过“管理应用”→“发布”操作）；
   - 添加后自动开始分钟级数据同步；关闭观测则停止同步，重开后仅新增数据生效。

3. **查看与分析**：
   - 在 Span 列表页，支持 Root Span / All Span / Model Span 三种视图模式；
   - 使用过滤器按状态、Span Name、输入/输出关键词、延时、Token 量、标签等条件组合筛选；
   - 单击节点名称展开详情，查看原始数据、标注记录、嵌套子节点；
   - 监控统计页签支持按分钟/小时/天粒度查看调用次数、失败率、Token 趋势、平均延时等。

4. **数据导出与复用**：
   - Trace 列表页右上角支持导出 JSONL 或 Excel；
   - 支持批量选中 Span → “添加到评测集”，完成字段映射后追加或覆盖导入。

## 限制和注意事项

- **无 API 支持**：所有功能仅限控制台操作，[应用观测目前暂无 API](../../raw/application-user-guide/application-monitoring/application-observation.md)。
- **数据延迟**：指标同步频率为分钟级，非实时。
- **存储计费**：应用观测功能本身免费，但底层依赖 OpenTelemetry 服务，产生的日志/链路数据需按该服务计费规则付费。
- **权限要求**：
  - 子账号需同时具备 `AliyunBailianFullAccess`、页面级“应用观测-操作”权限，以及 `ram:CreateServiceLinkedRole` 权限（[详细配置步骤见原文](../../raw/application-user-guide/application-monitoring/application-observation.md)）；
- **高代码应用特殊说明**：
  - 若开启观测后无统计数据，需确认两点：① 代码中已集成 AgentScope-AI 的 [Tracing 模块](https://github.com/agentscope-ai/agentscope-runtime/tree/main/src/agentscope_runtime/engine/tracing)；② 部署时显式添加 `--telemetry enable` 参数。

## 来源文档

- [应用观测](../../raw/application-user-guide/application-monitoring/application-observation.md)



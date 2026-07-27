# application monitoring

应用监控（Application Monitoring）是阿里云百炼平台提供的端到端可观测能力，用于追踪智能体、工作流及高代码类应用的内部执行链路，覆盖向量生成、知识检索、大模型调用等关键节点，并采集延时、[Token](../concepts/token.md) 用量、状态码等核心指标。数据同步频率为分钟级，支持按 Trace ID / Span ID / Request ID 检索与多维筛选。该功能当前仅提供控制台界面，**暂无公开 API 接口**，详见 [应用观测](../../raw/application-user-guide/application-monitoring/application-observation.md)。

## 支持的模型/功能

- **支持的应用类型**：智能体应用、工作流应用、高代码应用（但高代码应用仅上报根节点 `FullCodeApp`，[不支持内部链路追踪](../../raw/application-user-guide/application-monitoring/application-observation.md)）。
- **可观测节点类型**：
  - 通用节点：`CHAIN`（根节点，如 `AgentApp`/`WorkflowApp`）、`LLM`（大模型推理）、`RETRIEVER`（含 `TextRetriever`/`VectorRetriever`）、`EMBEDDING`、`RERANKER`、`REWRITER`、`GUARDRAIL`、`TOOL`；
  - 工作流专属节点：`START`、`API`、`CLASSIFIER`、`CONDITION`、`SCRIPT`、`TEXT_CONVERTER`、`FUNCTION_COMPUTE`、`APP_FLOW`、`END`；
  - 高代码专属节点：仅 `CHAIN` 类型下的 `FullCodeApp`（无子节点展开能力）。
- **附加能力**：Span 数据导出（JSONL/Excel）、添加至评测集（支持字段映射与全量/追加导入）、标签标注（布尔/分类/数字/文本类型，与评测集标签共享体系）。

> **注意**：文档中明确指出“应用观测目前暂不支持[通过Assistant API创建的智能体应用](https://help.aliyun.com/zh/model-studio/user-guide/what-is-assistant-api)”，该限制在 [应用观测](../../raw/application-user-guide/application-monitoring/application-observation.md) 中多次强调，需开发者在接入前确认应用创建方式。

## 关键参数

| 参数 | 说明 | 来源依据 |
|------|------|----------|
| **Trace ID / Span ID / Request ID** | 用于跨节点关联与精准检索；可在节点详情页点击“查看 ID”获取 | [应用观测](../../raw/application-user-guide/application-monitoring/application-observation.md) |
| **延时（ms）** | LLM 节点延时包含[流式输出](../concepts/streaming-output.md)全过程；平均首 [Token](../concepts/token.md) 耗时单独统计 | [应用观测](../../raw/application-user-guide/application-monitoring/application-observation.md) |
| **[Token](../concepts/token.md) 总量** | = 输入 Token 数 + 输出 Token 数；Embedding 节点 Token 量仅计向量化输入 | [应用观测](../../raw/application-user-guide/application-monitoring/application-observation.md) |
| **状态** | 分为 `正常` 与 `错误`；错误可进一步细分为 `ManualIntervention`（人工干预）或 `SystemIntervention`（系统干预） | [应用观测](../../raw/application-user-guide/application-monitoring/application-observation.md) |

## 使用方式

1. **前提配置（一次性）**  
   首次使用需完成三项授权：  
   - 授权可观测链路 OpenTelemetry 服务角色权限；  
   - 开通可观测链路 OpenTelemetry 服务；  
   - 初始化其 LogStore 存储（主账号操作，分钟级生效；子账号需额外配置 `CreateServiceLinkedRole` 权限，详见 [应用观测](../../raw/application-user-guide/application-monitoring/application-observation.md)）。

2. **启用观测**  
   - 进入 [应用观测](https://bailian.console.aliyun.com/tab=app?tab=app#/app-observe)，单击“选择被观测的应用” → “添加”；  
   - **仅已发布且归属当前业务空间的应用可见**；未发布应用需先通过“管理应用” → “发布”操作启用。

3. **数据查看与分析**  
   - 在 Span 列表页，支持三种筛选模式：`Root Span`（默认）、`All Span`、`Model Span`；  
   - 使用过滤器按状态、Span Name、输入/输出关键词、延时、Token 量、标签等条件组合筛选；  
   - 单击节点名称可展开查看原始数据、标注记录及嵌套子节点；  
   - “监控统计”页签提供调用次数、失败率、Token 趋势、平均首 Token 耗时、平均调用时长等聚合图表（支持按分钟/小时/天粒度）。

4. **高级操作**  
   - **导出数据**：Trace 列表页右上角支持 JSONL 或 Excel 导出；  
   - **添加到评测集**：批量选中 Span 后配置目标评测集、导入方式与字段映射（最多 50 个字段）；  
   - **数据标注**：在节点详情页点击“数据标注”，支持四类标签类型，标注结果实时生效并显示于列表“标签”列。

## 限制和注意事项

- **API 缺失**：应用监控当前**无开放 API**，所有操作必须通过控制台完成，自动化集成受限；此限制在 [应用观测](../../raw/application-user-guide/application-monitoring/application-observation.md) 中明确声明。
- **高代码应用限制**：虽支持添加高代码应用，但仅能观测 `FullCodeApp` 根节点，无法展开内部调用链路；若需深度追踪，须在代码中集成 AgentScope-AI 的 Tracing 模块，并部署时添加 `--telemetry enable` 参数。
- **[长期记忆](../concepts/long-term-memory.md)不可见**：`RETRIEVER` 节点不支持观测在[长期记忆](https://help.aliyun.com/zh/model-studio/long-term-memory)中的检索过程，该限制在文档附录中重复说明。
- **计费说明**：应用监控功能本身免费，但底层依赖可观测链路 OpenTelemetry 服务，产生的日志与链路数据存储费用需另行支付（参见 OpenTelemetry 计费文档）。
- **子账号权限复杂**：除常规 `AliyunBailianFullAccess` 外，还需显式授予 `创建服务关联角色` 权限（通过自定义 RAM 策略），否则配置步骤将失败 —— 此细节在 [应用观测](../../raw/application-user-guide/application-monitoring/application-observation.md) 的“常见问题”中有完整操作指引。

## 来源文档

- [应用观测](../../raw/application-user-guide/application-monitoring/application-observation.md)



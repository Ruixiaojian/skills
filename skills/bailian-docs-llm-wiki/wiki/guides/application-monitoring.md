# application monitoring

应用监控（Application Monitoring）是阿里云百炼平台提供的端到端可观测能力，用于追踪智能体、工作流及高代码类应用的内部执行链路，覆盖向量生成、知识检索、大模型调用等关键节点，并采集延时、Token 用量、状态码等核心指标。数据同步频率为分钟级，支持按 Trace ID / Span ID / Request ID 检索与多维筛选。该功能当前仅提供控制台界面，**暂无公开 API 接口**，详见 [应用观测](../../raw/application-user-guide/application-monitoring/application-observation.md)。

## 支持的模型/功能

- **支持的应用类型**：智能体应用、工作流应用、高代码应用（但高代码应用仅上报根节点 `FullCodeApp`，[不支持内部链路追踪](../../raw/application-user-guide/application-monitoring/application-observation.md)）。
- **可观测节点类型**：
  - 通用节点：`CHAIN`（根节点，如 `AgentApp`/`WorkflowApp`）、`LLM`（大模型推理）、`RETRIEVER`（含 `TextRetriever`/`VectorRetriever`）、`EMBEDDING`、`RERANKER`、`REWRITER`、`GUARDRAIL`、`TOOL`；
  - 工作流专属节点：`START`、`API`、`CLASSIFIER`、`CONDITION`、`SCRIPT`、`TEXT_CONVERTER`、`FUNCTION_COMPUTE`、`APP_FLOW`、`END`；
  - 高代码专属节点：仅 `CHAIN` 类型下的 `FullCodeApp`（无子节点展开能力）。
- **附加能力**：Span 数据导出（JSONL/Excel）、添加至评测集（支持字段映射与导入策略）、交互式标签标注（布尔/分类/数字/文本类型）、多维度监控统计（调用次数、失败率、Token 趋势、首 Token 耗时等）。

> **注意**：文档中明确指出“应用观测目前暂不支持[通过Assistant API创建的智能体应用](https://help.aliyun.com/zh/model-studio/user-guide/what-is-assistant-api)”，该限制在 [应用观测](../../raw/application-user-guide/application-monitoring/application-observation.md) 中多次强调，需在接入前确认应用创建方式。

## 关键参数

| 参数名 | 说明 | 来源上下文 |
|--------|------|------------|
| `Trace ID` / `Span ID` / `Request ID` | 用于唯一标识一次调用链路或单个节点；可在节点详情页点击“查看 ID”获取 | [应用观测](../../raw/application-user-guide/application-monitoring/application-observation.md) 中“如何获取 ID”小节 |
| `延时（ms）` | 节点执行耗时，LLM 节点包含[流式输出](../concepts/streaming-output.md)全过程；平均调用时长、首 Token 耗时均基于此计算 | [应用观测](../../raw/application-user-guide/application-monitoring/application-observation.md) 的“监控统计”页签说明 |
| `Token总量` / `输入Token` / `输出Token` | LLM 节点中指 `input_tokens + output_tokens`；EMBEDDING 节点中仅指向量化输入 Token 数 | [应用观测](../../raw/application-user-guide/application-monitoring/application-observation.md) 的附录“名词解释”及节点说明 |

## 使用方式

1. **前提配置**（仅首次使用需执行）：
   - 主账号或已授权子账号登录，进入 [应用观测](https://bailian.console.aliyun.com/tab=app?tab=app#/app-observe)，点击右上角「应用观测配置」；
   - 完成三步开通：授权 OpenTelemetry 服务角色 → 开通可观测链路 OpenTelemetry 服务 → 初始化 LogStore 存储；
   - 子账号需额外配置 `AliyunBailianFullAccess`、页面权限及 `ram:CreateServiceLinkedRole` 策略（详见 [应用观测](../../raw/application-user-guide/application-monitoring/application-observation.md) 常见问题）。

2. **启用观测**：
   - 应用必须已**发布**且属于当前业务空间；
   - 在应用观测列表点击「添加」，选择目标应用；
   - 添加后自动开始分钟级数据同步；关闭观测则停止同步，重开后仅新增数据入库。

3. **数据查看与分析**：
   - 切换 Span 筛选模式（Root Span / All Span / Model Span）；
   - 使用过滤器按状态、Span Name、输入/输出关键词、延时、Token 量、标签等条件组合筛选；
   - 单击节点名称展开详情，查看原始请求/响应、标注记录、嵌套子节点；
   - 在「监控统计」页签按时间范围（最长30天）和粒度（分钟/小时/天）查看聚合图表。

4. **进阶操作**：
   - 导出：Trace 列表页右上角「导出数据」→ JSONL 或 Excel；
   - 评测集：批量勾选 Span → 「添加到评测集」→ 映射字段（最多50个）→ 选择追加或覆盖；
   - 标注：在 Span 详情页点击「数据标注」→ 选择预设标签或新建（类型强约束）。

## 限制和注意事项

- **功能限制**：
  - 不支持 Assistant API 创建的智能体应用（[应用观测](../../raw/application-user-guide/application-monitoring/application-observation.md) 明确声明）；
  - 不支持[长期记忆](../concepts/long-term-memory.md)（Long-term Memory）中的检索过程观测；
  - 高代码应用无法展开 `FullCodeApp` 内部节点，仅能观测其整体调用行为；
  - 所有数据存储依赖可观测链路 OpenTelemetry 服务，**应用监控本身不收费，但 OpenTelemetry 存储与传输产生费用**。

- **技术限制**：
  - 文档反复强调“应用观测目前暂无API”，所有操作必须通过控制台完成；
  - TextRetriever / VectorRetriever 默认返回100个切片，**暂不支持数量调整**；
  - 子账号开通需严格遵循权限清单，缺一不可（尤其 `ram:CreateServiceLinkedRole`），否则配置失败。

- **行为注意事项**：
  > **注意**：高代码应用需在部署时显式添加 `--telemetry enable` 参数，并在代码中集成 AgentScope-AI 的 [Tracing 模块](https://github.com/agentscope-ai/agentscope-runtime/tree/main/src/agentscope_runtime/engine/tracing)，否则即使开启观测也无法上报数据 —— 此要求与智能体/工作流应用的零代码接入方式存在显著差异，易被忽略。

## 来源文档

- [应用观测](../../raw/application-user-guide/application-monitoring/application-observation.md)



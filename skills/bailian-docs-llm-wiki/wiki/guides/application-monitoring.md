# application monitoring

应用监控（Application Monitoring）是百炼平台提供的可观测性能力，用于端到端追踪智能体、工作流及高代码类应用的内部执行链路，支持查看调用延时、[Token](../concepts/token.md) 消耗、节点状态、模型思考过程等关键指标。数据采集频率为分钟级，所有观测数据默认存储于可观测链路 OpenTelemetry 服务中，需用户自行开通并承担对应存储与传输费用。该功能当前**不提供 API 接口**，仅支持控制台操作，详见 [应用观测](../../raw/application-user-guide/application-monitoring/application-observation.md)。

## 支持的模型/功能

- **支持的应用类型**：智能体应用、工作流应用、高代码应用（但高代码应用仅上报 `CHAIN` 根节点，[不支持内部链路追踪](../../raw/application-user-guide/application-monitoring/application-observation.md)）。
- **支持的节点类型**：
  - 通用节点：`CHAIN`（根节点，名称如 `AgentApp`/`WorkflowApp`/`FullCodeApp`）、`LLM`（大模型调用）、`RETRIEVER`（含 `TextRetriever`/`VectorRetriever`）、`EMBEDDING`、`RERANKER`、`REWRITER`、`GUARDRAIL`、`TOOL`；
  - 工作流专属节点：`START`、`END`、`API`、`CLASSIFIER`、`TEXT_CONVERTER`、`SCRIPT`、`CONDITION`、`FUNCTION_COMPUTE`、`APP_FLOW`；
  - 智能体专属节点：`AGENT`。
- **核心功能**：
  - 调用链路可视化（Root Span / All Span / Model Span 三种视图模式）；
  - 多维筛选（按状态、Span Name、输入/输出关键词、延时、[Token](../concepts/token.md) 量、标签等）；
  - 数据导出（JSONL / Excel）；
  - 监控统计（调用次数、失败率、[Token](../concepts/token.md) 趋势、首 Token 耗时、平均延时）；
  - 一键添加 Span 到评测集（支持字段映射与导入策略）；
  - 数据标注（布尔值、分类、数字、文本四类标签，与评测系统共享）。

> **注意**：文档中明确指出“应用观测目前暂不支持[通过Assistant API创建的智能体应用](https://help.aliyun.com/zh/model-studio/user-guide/what-is-assistant-api)”，该限制在 [应用观测](../../raw/application-user-guide/application-monitoring/application-observation.md) 中多次强调，开发者需避免对 Assistant API 应用启用监控。

## 关键参数

| 参数 | 说明 | 来源 |
|------|------|------|
| `Request ID` / `Trace ID` / `Span ID` | 用于精准定位单次调用或子链路，可在节点详情页点击“查看 ID”获取 | [应用观测](../../raw/application-user-guide/application-monitoring/application-observation.md) |
| `延时（毫秒）` | LLM 节点延时包含完整响应过程（含[流式输出](../concepts/streaming-output.md)）；整体应用延时为 `CHAIN` 节点耗时 | [应用观测](../../raw/application-user-guide/application-monitoring/application-observation.md) |
| `Token总量` | `LLM` 节点 = 输入 Token + 输出 Token；`EMBEDDING` 节点 = 向量化输入 Prompt 的 Token 数 | [应用观测](../../raw/application-user-guide/application-monitoring/application-observation.md) |
| `平均首Token耗时` | 仅对流式调用生效，指从请求发出到首个 Token 返回的时间 | [应用观测](../../raw/application-user-guide/application-monitoring/application-observation.md) |

## 使用方式

1. **前提配置**（首次使用必做）：
   - 主账号或已授权子账号登录，进入 [应用观测](https://bailian.console.aliyun.com/tab=app?tab=app#/app-observe) 页面，点击右上角 **应用观测配置**；
   - 完成三步：① 授权 OpenTelemetry 服务角色；② 开通可观测链路 OpenTelemetry 服务；③ 初始化 LogStore 存储；
   - 子账号需额外配置 `AliyunBailianFullAccess` + `应用观测-操作` 页面权限 + `ram:CreateServiceLinkedRole` 策略（详见 [应用观测](../../raw/application-user-guide/application-monitoring/application-observation.md)）。

2. **启用监控**：
   - 在应用观测页面点击 **选择被观测的应用** > **添加**；
   - 应用必须已**发布**且属于当前业务空间；
   - 添加后自动开始分钟级数据同步；关闭观测则停止同步，重新添加仅同步新增数据。

3. **查看与分析**：
   - 在 Span 列表页使用过滤器（支持多条件组合），按 `状态`/`输入`/`输出`/`延时`/`标签` 等筛选；
   - 单击 `CHAIN` 或任意节点名称展开详情，查看原始数据、标注记录、嵌套子节点；
   - 切换至 **监控统计** 页签，按时间范围（最长30天）和聚合粒度（分钟/小时/天）查看趋势图表。

4. **高代码应用特殊要求**：
   - 必须在代码中集成 AgentScope-AI 的 `Tracing` 模块；
   - 部署时需显式添加 `--telemetry enable` 参数，否则无法上报数据。

## 限制和注意事项

- **功能限制**：
  - 不支持 Assistant API 创建的智能体应用；
  - 不支持[长期记忆](../concepts/memory.md)（Long-term Memory）中的检索过程观测；
  - 高代码应用仅上报 `FullCodeApp` 根节点，无内部节点追踪能力；
  - 所有数据最长保留 30 天，不可延长；
  - 当前无开放 API，无法程序化接入或自动化告警。

- **技术限制**：
  - `TextRetriever` 和 `VectorRetriever` 默认返回 100 个切片，数量不可配置；
  - `EMBEDDING` 和 `LLM` 节点的 Token 统计逻辑不同，不可直接跨节点加总；
  - 子账号开通依赖主账号预先授予 `CreateServiceLinkedRole` 权限，否则配置会失败。

- **计费说明**：
  - 应用监控功能本身免费；
  - 所有观测数据存储于 OpenTelemetry 服务，按该服务标准计费（日志写入、存储、查询），费用与百炼平台分离，请参考 [OpenTelemetry 计费说明](https://help.aliyun.com/zh/arms/tracing-analysis/product-overview/untitled-document-1697525445039)。

> **注意**：文档中关于“高代码应用开启观测后看不到统计数据”的排查项，与“高代码应用仅上报根节点”的描述存在隐含矛盾——若仅上报 `FullCodeApp` 节点，理论上不应产生 `调用量` 等统计维度。实际行为以 [应用观测](../../raw/application-user-guide/application-monitoring/application-observation.md) 中“已为高代码应用开启观测，但为什么看不到调用量等统计数据？”一节的排查清单为准：必须满足代码埋点 + `--telemetry enable` 两个条件，否则监控数据为空。

## 来源文档

- [应用观测](../../raw/application-user-guide/application-monitoring/application-observation.md)



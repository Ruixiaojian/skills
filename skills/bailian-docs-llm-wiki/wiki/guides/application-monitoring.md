# application monitoring

应用观测（Application Monitoring）是阿里云百炼平台提供的端到端可观测能力，用于追踪和分析智能体、工作流及高代码类应用的内部执行链路。它支持查看调用延时、Token 消耗、模型思考过程及各节点状态，并提供分钟级指标聚合与原始 Span 数据导出能力。该功能基于 OpenTelemetry 构建，需依赖可观测链路服务，**当前不提供 API 接口** [应用观测 (raw/application-user-guide/application-monitoring/application-observation.md)](../../raw/application-user-guide/application-monitoring/application-observation.md)。

## 支持的模型/功能

- **支持的应用类型**：智能体应用、工作流应用、高代码应用（但高代码应用仅上报 `CHAIN` 根节点，**不支持内部链路追踪**）  
- **核心可观测维度**：
  - 调用链路（Root Span / All Span / Model Span 三种视图）
  - 延时（含平均首 Token 耗时、平均调用时长）
  - Token 统计（输入/输出/总量）
  - 状态（正常/错误，含错误类型细分）
  - 节点类型与嵌套关系（如 `LLM`、`RETRIEVER`、`EMBEDDING`、`GUARDRAIL` 等）  
- **扩展能力**：
  - 数据标注（布尔值、分类、数字、文本四类标签）
  - 批量导出（JSONL / Excel）
  - 添加 Span 到评测集（支持字段映射与导入策略配置）  
- **不支持场景**：通过 Assistant API 创建的智能体应用 [应用观测 (raw/application-user-guide/application-monitoring/application-observation.md)](../../raw/application-user-guide/application-monitoring/application-observation.md)；[长期记忆](../concepts/long-term-memory.md)中的检索过程；高代码应用内部节点 [应用观测 (raw/application-user-guide/application-monitoring/application-observation.md)](../../raw/application-user-guide/application-monitoring/application-observation.md)。

## 关键参数

| 参数 | 说明 | 备注 |
|------|------|------|
| `Request ID` / `Trace ID` / `Span ID` | 用于精准定位单次调用或子链路 | 可在节点详情页点击「查看 ID」获取 |
| `Span Name` | 节点逻辑名称（如 `AgentApp`, `TextRetriever`, `LLM`） | 支持模糊匹配筛选 |
| `Status` | `normal` 或 `error`，错误时可进一步区分类型（如 `GuardrailBlocked`, `LLMTimeout`） | — |
| `Latency (ms)` | 节点执行耗时（含网络与模型推理时间） | `LLM` 节点延时包含流式响应全过程 |
| `Input Tokens` / `Output Tokens` | Embedding 或 LLM 调用的 Token 数量 | 定义见 [附录](#f0ed9407canlv)（原文档） |
| `Label` | 用户自定义标注字段（类型强约束） | 与评测系统共享标签管理 |

> **注意**：`TextRetriever` 和 `VectorRetriever` 默认返回 100 个切片，且**暂不支持调整数量**；此限制在文档中被多次强调，属设计约束而非临时限制。

## 使用方式

### 前置配置（仅首次使用需执行）
1. 使用主账号（或已授权子账号）进入 [应用观测配置](https://bailian.console.aliyun.com/tab=app?tab=app#/app-observe) 页面；
2. 授权 `AliyunServiceRoleForOpenTelemetry` 服务关联角色；
3. 开通可观测链路 OpenTelemetry 服务并初始化 LogStore。

> 子账号需额外配置 `CreateServiceLinkedRole` 权限策略，详见 [常见问题](#cd0f1152d50hj)（原文档锚点）。

### 日常操作流程
1. **添加应用**：在应用观测列表中点击「添加」，仅支持已发布且归属当前业务空间的应用；
2. **查看数据**：
   - 在 Span 列表页切换筛选模式（Root/All/Model Span）；
   - 使用过滤器按 `Status`、`Span Name`、`Input`、`Output`、`Latency`、`Tokens` 或 `Label` 组合筛选；
   - 单击节点名称展开详情，查看原始请求/响应、标注记录、子节点等；
3. **导出与复用**：
   - 点击「导出数据」下载 JSONL 或 Excel；
   - 选中 Span 后点击「添加到评测集」，完成字段映射与导入策略配置。

## 限制和注意事项

- **无 API 支持**：应用观测为纯控制台功能，不开放 SDK 或 RESTful 接口 [应用观测 (raw/application-user-guide/application-monitoring/application-observation.md)](../../raw/application-user-guide/application-monitoring/application-observation.md)；
- **数据延迟**：指标同步频率为**分钟级**，不适用于实时告警场景；
- **存储计费**：功能本身免费，但底层 OpenTelemetry 存储费用需单独承担；
- **高代码应用限制**：即使开启观测，也仅上报 `FullCodeApp` 根节点，无法观测其内部[函数调用](../concepts/function-calling.md)或自定义逻辑——若需细粒度追踪，必须在代码中集成 `AgentScope-AI` 的 Tracing 模块并部署时启用 `--telemetry enable` 参数；
- **权限要求**：子账号开通需满足三重权限（`AliyunBailianFullAccess` + 页面写入权限 + `CreateServiceLinkedRole` 策略），缺一不可。

## 来源文档

- [应用观测](../../raw/application-user-guide/application-monitoring/application-observation.md)



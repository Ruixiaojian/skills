# application monitoring

应用观测（Application Monitoring）是阿里云百炼平台提供的端到端可观测能力，用于追踪应用内部调用链路、分析模型响应延时、查看大模型思考过程及 [Token](../concepts/token.md) 消耗等关键指标。该功能面向已发布的智能体、工作流和高代码应用，数据同步频率为分钟级，不提供 API 接口 [应用观测](../../raw/application-user-guide/application-monitoring/application-observation.md)。所有观测数据依赖可观测链路 OpenTelemetry 服务存储与计算，需提前完成权限授权与服务开通。

## 支持的模型/功能

- **支持的应用类型**：  
  - 智能体应用（Single-Agent Application）  
  - 工作流应用（Workflow Application）  
  - 高代码应用（Rich-Code Application）  
  > **注意**：通过 Assistant API 创建的智能体应用暂不支持观测 [应用观测](../../raw/application-user-guide/application-monitoring/application-observation.md)。

- **可观测节点类型**（按应用类型区分）：  
  - **通用节点**：`CHAIN`（根节点，如 `AgentApp`/`WorkflowApp`/`FullCodeApp`）、`LLM`、`RETRIEVER`（含 `TextRetriever`/`VectorRetriever`）、`EMBEDDING`、`RERANKER`、`REWRITER`、`GUARDRAIL`、`TOOL`（插件调用）  
  - **工作流专属节点**：`START`、`API`、`CLASSIFIER`、`TEXT_CONVERTER`、`SCRIPT`、`CONDITION`、`FUNCTION_COMPUTE`、`APP_FLOW`、`END`  
  - **高代码限制**：`FullCodeApp` 节点仅作为入口展示，**不支持追踪其内部调用链路** [应用观测](../../raw/application-user-guide/application-monitoring/application-observation.md)。

- **核心功能**：  
  - Trace 级别 Span 数据浏览（支持 Root/All/Model 三种筛选模式）  
  - 基于 Request ID / Trace ID / Span ID 的精准搜索  
  - 实时监控统计（调用次数、失败率、[Token](../concepts/token.md) 总量、首 [Token](../concepts/token.md) 耗时、平均调用时长）  
  - 数据导出（JSONL / Excel）  
  - Span 直接导入评测集（支持字段映射与全量/追加导入）  
  - 标签标注（布尔值、分类、数字、文本四类标签类型，与评测系统共享）

## 关键参数

| 参数名 | 含义 | 说明 |
|--------|------|------|
| `延时`（调用时长） | Span 执行耗时（毫秒） | LLM 节点延时包含[流式输出](../concepts/streaming-output.md)全过程；首 Token 耗时单独统计 |
| `Token总量` | 输入 Token 数 + 输出 Token 数 | Embedding 节点 Token 量仅计输入；LLM 节点按实际收发统计 |
| `状态` | Span 执行结果 | `正常` 或 `错误`（可进一步按错误类型细分） |
| `Span Name` | 节点逻辑名称 | 如 `AgentApp`、`TextRetriever`、`Qwen-Plus` 等，用于过滤与识别 |
| `标签` | 用户自定义标注字段 | 支持多类型输入，用于后续筛选与评测分析 |

## 使用方式

### 前置配置（仅首次使用需执行）
1. 使用**主账号**访问 [应用观测](https://bailian.console.aliyun.com/tab=app?tab=app#/app-observe)，点击右上角「应用观测配置」；  
2. 授权可观测链路 OpenTelemetry 服务角色权限；  
3. 开通 OpenTelemetry 服务并初始化 LogStore 存储；  
> 子账号需额外配置 `AliyunBailianFullAccess`、页面操作权限及 `ram:CreateServiceLinkedRole` 策略 [应用观测](../../raw/application-user-guide/application-monitoring/application-observation.md)。

### 日常使用流程
1. **添加被观测应用**：在应用观测页点击「选择被观测的应用」→「添加」；确保应用已**发布**且属于当前业务空间；  
2. **查看 Span 列表**：支持按时间范围（最长 30 天）、状态、Span Name、输入/输出关键词、延时、Token 量、标签等条件组合过滤；  
3. **深入分析单个 Span**：点击 Span 名称展开详情，查看原始请求/响应、节点嵌套关系、ID 信息（Request ID / Trace ID / Span ID）；  
4. **导出或评测**：在 Trace 列表页右上角「导出数据」，或通过「批量操作 → 添加到评测集」导入真实线上调用样本。

## 限制和注意事项

- **功能限制**：  
  - 应用观测**无公开 API**，仅支持控制台交互；  
  - 不支持[长期记忆](../concepts/long-term-memory.md)（Long-term Memory）中的检索过程观测；  
  - 高代码应用（`FullCodeApp`）仅上报顶层 Span，**无法观测其内部[函数调用](../concepts/function-calling.md)链**；  
  - TextRetriever / VectorRetriever 默认返回 100 个切片，**不支持数量调整**。

- **数据时效性**：  
  - 数据同步延迟约 **1–5 分钟**（高峰期可能延长）；  
  - 监控统计图表支持按分钟/小时/天聚合，但历史数据最长保留 **30 天**。

- **权限与计费**：  
  - 功能本身免费，但底层 OpenTelemetry 存储与计算按量计费；  
  - 子账号开通需严格遵循权限清单，缺一不可，否则配置失败。

- **开发适配要求（高代码应用）**：  
  - 必须在代码中集成 AgentScope-AI 的 `Tracing` 模块；  
  - 部署时需显式添加 `--telemetry enable` 参数启用上报。

## 来源文档

- [应用观测](../../raw/application-user-guide/application-monitoring/application-observation.md)



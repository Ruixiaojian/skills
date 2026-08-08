# application monitoring

应用观测（Application Monitoring）是阿里云百炼平台提供的端到端可观测能力，用于追踪应用内部调用链路、分析模型响应延时、查看 [Token](../concepts/token.md) 消耗及模型思考过程。该功能基于 OpenTelemetry 构建，支持分钟级指标同步与多维 Span 数据分析，适用于智能体、工作流和高代码三类应用。[应用观测](../../raw/application-user-guide/application-monitoring/application-observation.md) 是当前唯一官方支持的实现方式。

## 支持的模型/功能

- **支持的应用类型**：智能体应用、工作流应用、高代码应用（但高代码应用仅上报根节点 `FullCodeApp`，不支持内部链路追踪）  
- **核心可观测能力**：
  - 调用链路追踪（Root Span / All Span / Model Span 三种视图）
  - 延时指标（平均调用时长、首 [Token](../concepts/token.md) 耗时）
  - [Token](../concepts/token.md) 统计（输入/输出/总量）
  - 节点级详情（含原始数据、标注记录、嵌套关系）
  - 数据导出（JSONL / Excel）、批量导入评测集、标签标注（布尔/分类/数字/文本）
- **节点类型覆盖**：`CHAIN`、`LLM`、`RETRIEVER`（含 `TextRetriever`/`VectorRetriever`）、`EMBEDDING`、`RERANKER`、`REWRITER`、`TOOL`、`GUARDRAIL`、`AGENT` 等；工作流额外支持 `START`、`END`、`API`、`CLASSIFIER`、`CONDITION` 等节点。详见 [应用观测支持的所有节点类型](../../raw/application-user-guide/application-monitoring/application-observation.md)。

> **注意**：[通过Assistant API创建的智能体应用](../../raw/application-user-guide/application-monitoring/application-observation.md) 当前不被支持，此限制在文档中明确标注，且无替代方案。

## 关键参数

| 参数 | 说明 | 来源 |
|------|------|------|
| `Request ID` / `Trace ID` / `Span ID` | 用于精准定位单次调用或节点，可在节点详情页点击「查看 ID」获取 | [应用观测](../../raw/application-user-guide/application-monitoring/application-observation.md) |
| `Token总量` | = 输入 Token 数 + 输出 Token 数（`LLM` 和 `EMBEDDING` 节点分别统计） | [应用观测](../../raw/application-user-guide/application-monitoring/application-observation.md) |
| `延时` | `LLM` 节点延时包含流式响应全过程；`CHAIN` 根节点延时为端到端总耗时 | [应用观测](../../raw/application-user-guide/application-monitoring/application-observation.md) |
| `状态` | 仅 `正常` / `错误` 两类；错误可进一步按类型细分（如 `Guardrail` 触发的 `ManualIntervention`） | [应用观测](../../raw/application-user-guide/application-monitoring/application-observation.md) |

## 使用方式

### 前置配置（必需）
1. 主账号或已授权子账号访问 [应用观测配置](https://bailian.console.aliyun.com/tab=app?tab=app#/app-observe) 页面，完成：
   - 授权可观测链路 OpenTelemetry 服务角色权限
   - 开通 OpenTelemetry 服务
   - 初始化 LogStore 存储（主账号开通通常分钟级生效；子账号需额外配置 `CreateServiceLinkedRole` 权限，详见 [常见问题](../../raw/application-user-guide/application-monitoring/application-observation.md)）

### 启用观测
- 应用必须已**发布**且属于当前业务空间，否则不会出现在「选择被观测的应用」列表中  
- 添加后自动采集：所有 Prompt 输入、输出、延时、Token 量等数据以分钟级频率同步至观测后台  
- 关闭观测后数据停止同步，重新添加仅同步新增数据  

### 数据查看与操作
- **Span 列表页**：支持按 `Request ID`/`Trace ID`/`Span ID` 搜索、时间范围筛选、表头自定义、状态/名称/输入/输出/延时/Token/标签等多条件过滤  
- **节点详情页**：展开嵌套结构，查看原始请求/响应、标注记录、ID 信息  
- **监控统计页**：查看调用次数、失败率、Token 趋势、平均延时等图表（支持按分钟/小时/天聚合，最长30天）  
- **评测集集成**：支持将 Span 批量映射字段导入评测集（最多50个字段），用于真实场景评测  

## 限制和注意事项

- **无 API 接口**：应用观测目前暂无开放 API，所有操作均需通过控制台完成 —— 此限制在 [应用观测](../../raw/application-user-guide/application-monitoring/application-observation.md) 中明确声明  
- **高代码应用限制**：仅上报 `FullCodeApp` 根节点，无法观测其内部逻辑；若需链路追踪，必须在代码中集成 `AgentScope-AI` 的 `Tracing` 模块，并部署时启用 `--telemetry enable` 参数  
- **[长期记忆](../concepts/long-term-memory.md)不可观测**：知识库检索可观测，但[长期记忆](../../raw/application-user-guide/application-monitoring/application-observation.md)中的检索过程暂不支持  
- **计费说明**：功能本身免费，但底层依赖 OpenTelemetry 服务，产生的日志存储与查询费用需单独承担  
- **子账号权限要求严格**：除 `AliyunBailianFullAccess` 外，必须显式授予 `创建服务关联角色` 权限，否则配置步骤会失败（详见 [常见问题](../../raw/application-user-guide/application-monitoring/application-observation.md)）

## 来源文档

- [应用观测](../../raw/application-user-guide/application-monitoring/application-observation.md)



# application monitoring

应用监控（Application Monitoring）是阿里云百炼平台提供的端到端可观测能力，用于追踪智能体、工作流及高代码类应用的内部执行链路，采集延时、[Token](../concepts/token.md) 量、状态、输入/输出等关键指标。数据以分钟级频率同步至控制台，支持按 Trace ID、Span ID 或 Request ID 精准检索，并可导出用于评测与分析。该功能依赖可观测链路 OpenTelemetry 服务，不提供独立 API 接口。

## 支持的模型/功能

- **支持的应用类型**：智能体应用、工作流应用、高代码应用（[原文标题](../../raw/application-user-guide/application-monitoring/application-observation.md)）  
- **可观测节点类型**：涵盖 `CHAIN`、`LLM`、`RETRIEVER`（含 `TextRetriever`/`VectorRetriever`）、`EMBEDDING`、`RERANKER`、`REWRITER`、`TOOL`、`GUARDRAIL`、`START`/`END`、`API`、`CLASSIFIER` 等（详见[原文标题](../../raw/application-user-guide/application-monitoring/application-observation.md)）  
- **核心功能**：调用链路可视化、延时与 [Token](../concepts/token.md) 统计、多维筛选（Root/All/Model Span 模式）、标签标注、数据导出（JSONL/Excel）、一键导入评测集  
- **限制**：暂不支持通过 Assistant API 创建的智能体应用；高代码应用仅上报根节点 `FullCodeApp`，**不支持其内部调用链路追踪**（[原文标题](../../raw/application-user-guide/application-monitoring/application-observation.md)）

> **注意**：文档中“高代码应用”章节明确说明 `FullCodeApp` 节点“目前不支持追踪其内部调用链路”，但同一文档前文“支持的应用”列表又将其列为支持类型。此处以功能描述为准——仅支持根节点观测，无嵌套 Span。

## 关键参数

| 参数 | 说明 | 来源上下文 |
|------|------|------------|
| **Trace ID / Span ID / Request ID** | 用于跨节点关联与精准检索；可在节点详情页点击“查看 ID”获取 | [原文标题](../../raw/application-user-guide/application-monitoring/application-observation.md) |
| **延时（调用时长）** | LLM 节点延时包含流式响应全过程；平均首 [Token](../concepts/token.md) 耗时专用于流式场景 | [原文标题](../../raw/application-user-guide/application-monitoring/application-observation.md) |
| **Token 总量** | = 输入 Token 数 + 输出 Token 数；Embedding 节点 Token 量指向量化输入长度 | [原文标题](../../raw/application-user-guide/application-monitoring/application-observation.md) |
| **状态** | 分为“正常”与“错误”，错误可进一步按类型细分（如 `ManualIntervention`、`SystemIntervention`） | [原文标题](../../raw/application-user-guide/application-monitoring/application-observation.md) |

## 使用方式

1. **前提配置**（主账号或已授权子账号操作）：  
   - 在应用观测页面开启“应用观测配置”，完成三步：① 授权 OpenTelemetry 服务角色；② 开通 OpenTelemetry 服务；③ 初始化 LogStore 存储（[原文标题](../../raw/application-user-guide/application-monitoring/application-observation.md)）  

2. **启用观测**：  
   - 进入 [应用观测控制台](https://bailian.console.aliyun.com/tab=app?tab=app#/app-observe)，点击“选择被观测的应用” → “添加”；**仅已发布的应用可见**（未发布需先在“管理应用”中发布）  

3. **查看与分析**：  
   - 在 Span 列表页使用过滤器（支持状态、Span Name、输入/输出关键词、延时、Token 量、标签等条件组合）  
   - 切换 Span 筛选模式（Root / All / Model Span）快速聚焦目标节点  
   - 单击节点名称展开详情，查看原始数据、标注记录、嵌套子节点  

4. **高级操作**：  
   - **导出数据**：Trace 列表页右上角支持 JSONL/Excel 导出  
   - **添加到评测集**：批量勾选 Span → 配置字段映射（最多 50 个）→ 选择追加或覆盖  
   - **数据标注**：支持布尔值、分类、数字、文本四类标签，与评测系统共享标签管理  

## 限制和注意事项

- **无 API 接口**：应用监控当前仅提供控制台界面，不开放 RESTful 或 SDK 接口（[原文标题](../../raw/application-user-guide/application-monitoring/application-observation.md)）  
- **高代码应用限制**：即使开启观测，也**仅上报 `FullCodeApp` 根节点**，无法观测其内部函数、模型或插件调用（需自行集成 AgentScope-AI Tracing 模块并部署时启用 `--telemetry enable`）  
- **数据延迟**：指标同步频率为分钟级，非实时；关闭观测后历史数据停止更新，重新添加仅同步新增数据  
- **权限要求**：子账号需同时具备 `AliyunBailianFullAccess`、页面操作权限及 `ram:CreateServiceLinkedRole` 权限（详见[原文标题](../../raw/application-user-guide/application-monitoring/application-observation.md)）  
- **计费说明**：应用监控功能本身免费，但底层 OpenTelemetry 存储与计算资源按阿里云 ARMS 计费规则收取（参见官方计费文档）

## 来源文档

- [应用观测](../../raw/application-user-guide/application-monitoring/application-observation.md)



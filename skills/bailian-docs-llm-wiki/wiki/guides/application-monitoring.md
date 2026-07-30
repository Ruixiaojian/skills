# application monitoring

应用监控（Application Monitoring）是阿里云百炼平台提供的端到端可观测能力，用于追踪智能体、工作流及高代码类应用的内部执行链路，覆盖向量生成、知识检索、大模型调用等关键节点，并采集延时、[Token](../concepts/token.md) 用量、状态码等核心指标。数据同步频率为分钟级，支持按 Trace ID / Span ID / Request ID 快速定位问题，适用于性能分析、成本优化与线上数据回流评测。该功能当前仅提供控制台界面，**暂无公开 API 接口**，详见 [应用观测](../../raw/application-user-guide/application-monitoring/application-observation.md)。

## 支持的模型/功能

- **支持的应用类型**：  
  - 智能体应用（Single-Agent Application）  
  - 工作流应用（Workflow Application）  
  - 高代码应用（Rich-Code Application）  
  > **注意**：通过 Assistant API 创建的智能体应用[不被支持](../../raw/application-user-guide/application-monitoring/application-observation.md)，该限制在文档中明确标注。

- **可观测节点类型**（按应用类型区分）：  
  - **通用节点**：`CHAIN`（根节点，名称如 `AgentApp`/`WorkflowApp`/`FullCodeApp`）、`LLM`、`RETRIEVER`（含 `TextRetriever`/`VectorRetriever`）、`EMBEDDING`、`RERANKER`、`REWRITER`、`TOOL`、`GUARDRAIL`  
  - **工作流专属节点**：`START`、`API`、`CLASSIFIER`、`TEXT_CONVERTER`、`SCRIPT`、`CONDITION`、`FUNCTION_COMPUTE`、`APP_FLOW`、`END`  
  - **高代码应用限制**：`FullCodeApp` 节点仅作为入口展示，**不支持展开其内部调用链路**，详见 [应用观测](../../raw/application-user-guide/application-monitoring/application-observation.md) 附录说明。

- **核心功能**：  
  - 多维度 Span 筛选（Root/All/Model 模式 + 自定义过滤器）  
  - 标签标注（与评测系统共享标签体系，支持布尔/分类/数字/文本类型）  
  - 数据导出（JSONL / Excel）  
  - 监控统计看板（调用次数、失败率、[Token](../concepts/token.md) 趋势、首 [Token](../concepts/token.md) 耗时、平均延时）  
  - 一键导入 Span 到评测集（支持字段映射与追加/覆盖策略）

## 关键参数

| 参数 | 说明 | 来源约束 |
|------|------|----------|
| **Trace ID / Span ID / Request ID** | 用于跨节点关联与精确检索；需在节点详情页点击“查看 ID”获取 | 见 [应用观测](../../raw/application-user-guide/application-monitoring/application-observation.md) “使用方法”章节 |
| **延时（ms）** | LLM 节点延时包含完整流式响应过程；其他节点为自身执行耗时 | 文档明确说明：“LLM节点的**延时**（**调用时长**）包括输出回复的过程” |
| **Token 量** | 统一定义为 `输入 Token 数 + 输出 Token 数`（LLM 节点）；Embedding 节点仅计向量化输入 Token | 同上，见 [应用观测](../../raw/application-user-guide/application-monitoring/application-observation.md) 节点说明 |
| **状态字段** | 值为 `正常` 或 `错误`；错误可进一步细分类型（如 Guardrail 拦截、LLM 调用失败） | 过滤器支持按“错误类型”细分筛选 |

## 使用方式

1. **前提配置（一次性）**：  
   - 主账号或已授权子账号访问 [应用观测配置](https://bailian.console.aliyun.com/tab=app?tab=app#/app-observe) 页面，完成：  
     - 授权可观测链路 OpenTelemetry 服务角色  
     - 开通 OpenTelemetry 服务  
     - 初始化 LogStore 存储（主账号开通通常分钟级生效）  
   > 子账号需额外配置 `AliyunBailianFullAccess` + `应用观测-操作` 页面权限 + `CreateServiceLinkedRole` 系统策略，详见 [应用观测](../../raw/application-user-guide/application-monitoring/application-observation.md) 常见问题部分。

2. **启用观测**：  
   - 在应用观测页面 → “选择被观测的应用” → 添加已**发布**且属于当前业务空间的应用  
   - 添加后自动开始分钟级数据同步；关闭观测即停止采集（历史数据保留，新增数据不补录）

3. **数据查看与分析**：  
   - 在 Span 列表页：按时间范围（最长 30 天）、ID、关键词、延时、Token 量、标签等条件筛选  
   - 单击节点名称展开详情：查看原始输入/输出、调用上下文、嵌套子节点、标注记录  
   - 切换至“监控统计”页签：按分钟/小时/天粒度查看聚合指标趋势图（支持下载与放大）

4. **高级操作**：  
   - **导出数据**：Trace 列表页右上角 → “导出数据”（JSONL 或 Excel）  
   - **添加到评测集**：批量勾选 Span → 配置目标评测集、导入方式、字段映射（最多 50 字段）  
   - **数据标注**：在 Span 详情页点击“数据标注”，复用统一标签管理体系  

## 限制和注意事项

- **功能限制**：  
  - ❌ 不提供 API 接口，所有操作必须通过控制台完成  
  - ❌ 不支持[长期记忆](../concepts/memory.md)（Long-Term Memory）中的检索过程观测  
  - ❌ 高代码应用（`FullCodeApp`）仅暴露根节点，无法追踪其内部逻辑（如自定义函数、HTTP 调用等）  
  - ❌ TextRetriever / VectorRetriever 默认返回 100 个切片，**不支持数量调整**  

- **部署要求（高代码应用）**：  
  - 必须在代码中集成 AgentScope-AI 的 [`Tracing` 模块](https://github.com/agentscope-ai/agentscope-runtime/tree/main/src/agentscope_runtime/engine/tracing)  
  - 部署命令需显式添加 `--telemetry enable` 参数，否则无数据上报  

- **权限与计费**：  
  - 应用监控功能本身免费，但底层依赖 OpenTelemetry 服务，产生的日志存储与链路分析费用需单独支付（参见 [OpenTelemetry 计费说明](https://help.aliyun.com/zh/arms/tracing-analysis/product-overview/untitled-document-1697525445039)）  
  - 子账号开通需严格遵循 [权限配置清单](../../raw/application-user-guide/application-monitoring/application-observation.md)，缺一不可  

> **注意**：文档中关于“应用观测目前暂无API”的声明与当前平台能力一致，无矛盾；但需注意该限制直接影响自动化运维集成方案设计。

## 来源文档

- [应用观测](../../raw/application-user-guide/application-monitoring/application-observation.md)



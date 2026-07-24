# application monitoring

应用观测（Application Monitoring）是阿里云百炼平台提供的端到端可观测能力，用于追踪智能体、工作流及高代码应用内部的完整执行链路，包括向量生成、知识检索、大模型调用等关键节点，并采集延时、[Token](../concepts/token.md) 用量、状态码等核心指标。数据同步频率为分钟级，支持按 Trace ID / Span ID / Request ID 精准检索与多维筛选，适用于性能分析、成本优化与真实场景评测数据构建。该功能当前**无公开 API 接口**，全部操作需通过控制台完成 [应用观测](https://bailian.console.aliyun.com/tab=app?tab=app#/app-observe) 页面进行 [原文标题](../../raw/application-user-guide/application-monitoring/application-observation.md)。

## 支持的模型/功能

- **支持的应用类型**：智能体应用、工作流应用、高代码应用（仅上报根节点 `FullCodeApp`，不支持内部链路追踪）  
- **可观测节点类型**：涵盖 `CHAIN`、`LLM`、`RETRIEVER`（含 `TextRetriever`/`VectorRetriever`）、`EMBEDDING`、`RERANKER`、`REWRITER`、`TOOL`、`GUARDRAIL`、`START`/`END`、`CLASSIFIER`、`API`、`CONDITION` 等共 15+ 类节点，详细说明见 [原文标题](../../raw/application-user-guide/application-monitoring/application-observation.md) 的「支持的节点类型」章节  
- **核心功能**：  
  - 调用链路展开与交互式节点详情查看（含原始输入/输出、标注记录）  
  - 按状态（正常/错误）、Span 名称、输入/输出关键词、延时、[Token](../concepts/token.md) 量、标签等条件组合过滤  
  - 监控统计页提供调用次数、失败率、[Token](../concepts/token.md) 总量、平均首 Token 耗时、平均调用时长等趋势图表（支持分钟/小时/天粒度聚合）  
  - 支持将 Span 数据一键导出为 JSONL 或 Excel，或批量导入至评测集（支持字段映射与追加/覆盖模式）  
  - 支持布尔值、分类、数字、文本四类标签标注，标注结果与评测系统共享 [原文标题](../../raw/application-user-guide/application-monitoring/application-observation.md)

## 关键参数

| 参数 | 说明 | 备注 |
|------|------|------|
| **Trace ID / Span ID / Request ID** | 链路唯一标识符，用于跨系统关联与精准定位问题 | 可在节点详情页点击「查看 ID」获取 |
| **延时（ms）** | 节点实际执行耗时，LLM 节点包含流式响应全程 | 不同节点定义一致，但 LLM 延时含输出过程 |
| **Token 总量** | `输入 Token 数 + 输出 Token 数` | Embedding 节点仅统计向量化输入 Token |
| **状态** | `正常` 或 `错误`；错误可进一步细分为 `ManualIntervention`/`SystemIntervention`/其他异常 | Guardrail 节点触发干预时标记为错误 |
| **标签（Label）** | 用户自定义维度，支持四类类型（布尔/分类/数字/文本），用于后续筛选与评测 | 标签管理全局统一，与评测集标签互通 |

> **注意**：`TextRetriever` 和 `VectorRetriever` 默认返回 100 个文本切片，且**暂不支持调整数量**；[长期记忆](../concepts/memory.md)中的检索过程**当前不可观测** —— 这些限制在 [原文标题](../../raw/application-user-guide/application-monitoring/application-observation.md) 中明确声明，未发现与其他文档矛盾。

## 使用方式

### 前置配置（仅需一次）
1. 主账号登录，进入 [应用观测](https://bailian.console.aliyun.com/tab=app?tab=app#/app-observe)，点击右上角「应用观测配置」  
2. 完成三步授权：  
   - 授权可观测链路 OpenTelemetry 服务角色权限  
   - 开通可观测链路 OpenTelemetry 服务  
   - 初始化 OpenTelemetry 存储 LogStore  
3. 子账号需额外配置 `AliyunBailianFullAccess` + `应用观测-操作` 权限 + `CreateServiceLinkedRole` 策略（详见 [原文标题](../../raw/application-user-guide/application-monitoring/application-observation.md)「常见问题」）

### 日常使用流程
1. **添加被观测应用**：在应用观测页点击「选择被观测的应用」→「添加」；**仅已发布且归属当前业务空间的应用可见**  
2. **查看数据**：  
   - 列表页支持 Root Span / All Span / Model Span 三种视图模式  
   - 点击「查看详情」进入 Span 列表，支持按时间范围（最长 30 天）、ID、关键词、延时等条件筛选  
   - 点击节点名称展开详情，查看原始数据、标注、子节点等  
3. **导出与评测集成**：在 Trace 列表页右上角点击「导出数据」，或勾选 Span 后点击「添加到评测集」完成字段映射与导入  

## 限制和注意事项

- **API 缺失**：应用观测**当前无开放 API**，所有数据获取与操作必须通过控制台完成，无法集成至自动化运维流程  
- **应用兼容性限制**：  
  - 不支持通过 Assistant API 创建的智能体应用  
  - 高代码应用仅上报 `FullCodeApp` 根节点，**内部逻辑不可观测**；如需链路追踪，必须在代码中集成 AgentScope-AI 的 `Tracing` 模块并部署时启用 `--telemetry enable` 参数  
- **数据延迟**：指标与日志同步频率为**分钟级**，不适用于毫秒级实时告警场景  
- **计费说明**：应用观测功能本身免费，但底层依赖可观测链路 OpenTelemetry 服务，其存储与查询费用需单独承担  
- **权限要求**：子账号开通需严格满足四重权限（全局访问 + 页面操作 + 角色创建 + 服务关联角色），缺一不可，否则配置失败  

> **注意**：文档中明确指出「应用观测目前暂无API」，而部分旧版 SDK 文档曾提及实验性 tracing 接口，该信息已过时；请以本页引用的 [原文标题](../../raw/application-user-guide/application-monitoring/application-observation.md) 为准。

## 来源文档

- [应用观测](../../raw/application-user-guide/application-monitoring/application-observation.md)



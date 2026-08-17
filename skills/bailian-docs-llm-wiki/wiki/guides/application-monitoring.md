# application monitoring

应用监控（Application Monitoring）是阿里云百炼平台提供的端到端可观测能力，用于追踪智能体、工作流及高代码类应用的内部执行链路，支持查看调用延时、[Token](../concepts/token.md) 消耗、模型思考过程及各节点状态。该功能基于 OpenTelemetry 架构实现，数据同步延迟为分钟级，适用于线上问题排查、性能优化与评测集构建等开发者场景。[应用观测](../../raw/application-user-guide/application-monitoring/application-observation.md) 是其核心控制台入口。

## 支持的模型/功能

- **支持的应用类型**：智能体应用、工作流应用、高代码应用（但高代码应用仅上报 `CHAIN` 根节点，不支持内部链路追踪）  
- **可观测节点类型**：涵盖 `CHAIN`、`LLM`、`RETRIEVER`（含 `TextRetriever`/`VectorRetriever`）、`EMBEDDING`、`RERANKER`、`REWRITER`、`TOOL`、`GUARDRAIL`、`AGENT`、`START`、`END`、`API`、`CLASSIFIER` 等共 15+ 类节点，完整覆盖 RAG、Agent、Workflow 全流程。详细说明见 [应用观测支持的所有节点类型](../../raw/application-user-guide/application-monitoring/application-observation.md)。  
- **核心功能**：调用链路追踪（Root/All/Model Span 三种视图）、多维筛选（按状态、Span Name、输入/输出关键词、延时、[Token](../concepts/token.md) 量、标签等）、ID 搜索（Request ID / Trace ID / Span ID）、数据导出（JSONL / Excel）、监控统计（调用次数、失败率、[Token](../concepts/token.md) 趋势、首 Token 耗时）、添加至评测集、数据标注（布尔/分类/数字/文本四类标签）  

> **注意**：[应用观测](../../raw/application-user-guide/application-monitoring/application-observation.md) 明确指出，**暂不支持通过 Assistant API 创建的智能体应用**，且**目前暂无 API 接口**，所有操作必须通过控制台完成。

## 关键参数

| 参数 | 说明 | 来源依据 |
|------|------|----------|
| **延时（调用时长）** | LLM 节点延时包含流式响应全过程；平均调用时长、平均首 Token 耗时均在「监控统计」页签中聚合展示 | [应用观测](../../raw/application-user-guide/application-monitoring/application-observation.md) |
| **Token 量** | `LLM` 节点 = 输入 Token + 输出 Token；`EMBEDDING` 节点 = 向量化输入 Prompt 的 Token 数；`RETRIEVER` 默认返回 100 个文本切片，不可配置 | [应用观测](../../raw/application-user-guide/application-monitoring/application-observation.md) |
| **数据保留周期** | Span 数据最长可查 30 天；监控统计支持按分钟/小时/天粒度聚合，时间范围上限同为 30 天 | [应用观测](../../raw/application-user-guide/application-monitoring/application-observation.md) |
| **标签字段限制** | 单个评测集最多支持 50 个字段映射；标注类型严格对应标签管理系统的定义（布尔/分类/数字/文本） | [应用观测](../../raw/application-user-guide/application-monitoring/application-observation.md) |

## 使用方式

### 前置配置（仅需执行一次）
1. 使用**主账号**访问 [应用观测](https://bailian.console.aliyun.com/tab=app?tab=app#/app-observe)，点击右上角「应用观测配置」  
2. 依次完成：授权 OpenTelemetry 服务角色 → 开通可观测链路 OpenTelemetry 服务 → 初始化 LogStore 存储  
   > 子账号需额外配置 `AliyunBailianFullAccess`、页面权限及 `ram:CreateServiceLinkedRole` 策略（详见 [常见问题](../../raw/application-user-guide/application-monitoring/application-observation.md)）

### 日常使用流程
1. **添加应用**：在应用列表中选择已**发布**且属于当前业务空间的应用（未发布应用不可见）  
2. **查看追踪**：进入应用详情页 → 「Trace 列表」页签 → 切换 Span 筛选模式（Root/All/Model）→ 使用过滤器按状态、关键词、延时等条件筛选  
3. **深入分析**：点击 Span 名称展开节点详情 → 查看原始数据、标注记录、子节点嵌套结构  
4. **导出与复用**：支持导出 JSONL/Excel；可批量选中 Span → 「添加到评测集」→ 配置字段映射后导入  

## 限制和注意事项

- **功能限制**：  
  - 不支持 Assistant API 创建的智能体应用（[原文标题](../../raw/application-user-guide/application-monitoring/application-observation.md)）  
  - 高代码应用仅上报 `FullCodeApp` 根节点，内部逻辑不可见；需在代码中显式集成 AgentScope-AI Tracing 模块并部署时启用 `--telemetry enable`  
  - 目前无开放 API，所有能力仅限控制台使用  

- **技术限制**：  
  - 数据同步延迟为分钟级，不适用于毫秒级实时诊断  
  - `TextRetriever`/`VectorRetriever` 返回切片数固定为 100，不可调整  
  - [长期记忆](../concepts/long-term-memory.md)（Long-term Memory）中的检索过程不可观测  

- **权限与计费**：  
  - 应用监控功能本身免费，但底层依赖 OpenTelemetry 服务，存储与计算费用需单独承担（参见 [计费说明](../../raw/application-user-guide/application-monitoring/application-observation.md)）  
  - 子账号开通需主账号预先授予 `CreateServiceLinkedRole` 权限，否则配置步骤会失败  

> **注意**：文档中关于「高代码应用可观测性」的描述存在隐含矛盾——正文称“不支持追踪其内部调用链路”，但附录又要求用户“在代码中定义要上报的信息”并启用 `--telemetry enable`。实际效果取决于是否接入 AgentScope-AI Runtime 的 Tracing 模块，而非平台自动注入。开发者应以 [应用观测](../../raw/application-user-guide/application-monitoring/application-observation.md) 中的高代码排查清单为准。

## 来源文档

- [应用观测](../../raw/application-user-guide/application-monitoring/application-observation.md)



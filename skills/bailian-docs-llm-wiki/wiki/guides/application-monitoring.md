# application monitoring

应用监控（Application Monitoring）是百炼平台提供的可观测性能力，用于端到端追踪智能体、工作流及高代码应用的内部执行链路，包括向量生成、知识检索、大模型调用等关键节点，并采集延时、[Token](../concepts/token.md) 用量、状态、输入/输出等指标。数据同步频率为分钟级，支持交互式展开分析、多维筛选、标注与导出。该功能依赖可观测链路 OpenTelemetry 服务，**当前不提供 API 接口**，所有操作需通过控制台完成 [应用观测](../../raw/application-user-guide/application-monitoring/application-observation.md)。

## 支持的模型/功能

- **支持的应用类型**：智能体应用、工作流应用、高代码应用（但高代码应用仅上报根节点 `FullCodeApp`，[不支持内部链路追踪](../../raw/application-user-guide/application-monitoring/application-observation.md)）。
- **不支持的应用**：通过 Assistant API 创建的智能体应用（见 [原文标题](../../raw/application-user-guide/application-monitoring/application-observation.md)）。
- **核心可观测能力**：
  - 调用链路（Trace）可视化：支持 `CHAIN`、`LLM`、`RETRIEVER`、`EMBEDDING`、`RERANKER`、`TOOL`、`GUARDRAIL` 等节点类型；
  - 指标采集：单次请求延时、首 [Token](../concepts/token.md) 耗时、输入/输出/总 [Token](../concepts/token.md) 量、调用成功率；
  - 数据增强：支持 Span 级别标签标注、批量导入评测集、自定义字段映射（最多 50 个）；
  - 多维筛选：支持按状态、Span Name、输入/输出关键词、延时、Token 量、标签等条件组合过滤。

> **注意**：文档中明确说明“应用观测目前暂无API”，但部分开发者可能误以为可通过 SDK 或 REST API 集成。请以 [原文标题](../../raw/application-user-guide/application-monitoring/application-observation.md) 为准，所有能力均仅限控制台使用。

## 关键参数

| 参数 | 说明 | 来源/约束 |
|------|------|-----------|
| `Request ID` / `Trace ID` / `Span ID` | 用于精准定位单次调用或节点；需在节点详情页点击「查看 ID」获取 | 见 [原文标题](../../raw/application-user-guide/application-monitoring/application-observation.md) 中「如何获取 ID」章节 |
| `Span Name` | 如 `AgentApp`、`WorkflowApp`、`TextRetriever`、`QwenPlus` 等，标识节点语义角色 | 参考附录「支持的节点类型」，不同应用类型节点命名规则不同 |
| `Token 量` | 定义为 Embedding 模型向量化 Token 数（Embedding 节点）或 LLM 输入+输出 Token 总和（LLM 节点） | 明确见于 [原文标题](../../raw/application-user-guide/application-monitoring/application-observation.md) 各节点说明 |
| `延时（调用时长）` | LLM 节点延时包含完整响应过程（含[流式输出](../concepts/streaming-output.md)），首 Token 耗时单独统计 | 控制台「监控统计」页签中分项展示 |

## 使用方式

### 前置配置（必需）
1. 主账号（或已授权子账号）访问 [应用观测](https://bailian.console.aliyun.com/tab=app?tab=app#/app-observe)，点击右上角「应用观测配置」；
2. 授权可观测链路 OpenTelemetry 服务角色权限；
3. 开通 OpenTelemetry 服务并初始化 LogStore 存储（开通后通常分钟级生效）。

> 子账号需额外配置 `AliyunBailianFullAccess` + 页面权限 + `CreateServiceLinkedRole` 策略，详见 [原文标题](../../raw/application-user-guide/application-monitoring/application-observation.md)「常见问题」章节。

### 日常使用流程
1. **添加被观测应用**：在应用观测列表点击「添加」，仅已发布且归属当前业务空间的应用可见；
2. **查看 Trace 列表**：支持 Root Span / All Span / Model Span 三种视图模式，可按时间范围（最长 30 天）、ID、关键词、延时、Token 量等筛选；
3. **深入分析单个 Span**：点击节点名称展开详情，查看原始输入/输出、标注记录、嵌套子节点；
4. **导出与复用**：支持 JSONL/EXCEL 导出；支持将 Span 批量导入评测集（支持追加或覆盖，字段映射最多 50 个）；
5. **监控统计**：在「监控统计」页签查看调用趋势、失败率、Token 分布、平均延时等聚合图表（支持按分钟/小时/天粒度切换）。

## 限制和注意事项

- **功能限制**：
  - 不支持 Assistant API 创建的智能体应用；
  - 高代码应用仅上报 `FullCodeApp` 根节点，无法观测其内部逻辑（如[函数调用](../concepts/function-calling.md)、HTTP 请求等）；
  - [长期记忆](../concepts/long-term-memory.md)（Long-term Memory）中的检索过程不可观测；
  - TextRetriever / VectorRetriever 默认返回 100 个切片，数量不可配置；
  - 数据保留周期为 30 天，不可延长。

- **技术限制**：
  - 应用观测本身免费，但底层依赖 OpenTelemetry 服务，存储与查询费用按实际用量计费；
  - 首次配置后数据同步存在分钟级延迟，高峰期可能略有延长；
  - 关闭观测后历史数据停止同步，重新开启仅采集新增数据。

- **权限与部署注意**：
  - 高代码应用需在启动时显式添加 `--telemetry enable` 参数，并在代码中集成 AgentScope-AI 的 Tracing 模块，否则无数据上报；
  - 子账号必须完成 RAM 权限四步配置（全局权限 + 页面权限 + SLR 创建权限 + 角色授权），缺一不可。

## 来源文档

- [应用观测](../../raw/application-user-guide/application-monitoring/application-observation.md)



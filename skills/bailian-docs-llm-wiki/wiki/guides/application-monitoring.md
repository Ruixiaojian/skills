# application monitoring

应用监控（Application Monitoring）是百炼平台提供的可观测性能力，用于端到端追踪应用内部调用链路、分析模型响应延时、查看 [Token](../concepts/token.md) 消耗及推理过程等关键指标。该功能基于 OpenTelemetry 架构实现，数据同步频率为分钟级，适用于智能体、工作流和高代码三类应用，但暂不提供 API 接口 [应用观测](../../raw/application-user-guide/application-monitoring/application-observation.md)。

## 支持的模型/功能

- **支持的应用类型**：智能体应用、工作流应用、高代码应用（仅支持入口观测，[高代码应用](../../raw/application-user-guide/application-monitoring/application-observation.md) 内部链路不可见）  
- **可观测节点类型**：包括 `CHAIN`（根节点，如 `AgentApp`/`WorkflowApp`）、`LLM`（大模型调用）、`RETRIEVER`（含 `TextRetriever`/`VectorRetriever`）、`EMBEDDING`、`RERANKER`、`REWRITER`、`TOOL`、`GUARDRAIL`、`API`、`CLASSIFIER` 等（详见 [应用观测](../../raw/application-user-guide/application-monitoring/application-observation.md) 附录）  
- **核心功能**：  
  - 调用链路展开与交互式 Span 查看  
  - 基于 `Request ID`/`Trace ID`/`Span ID` 的精准检索  
  - 多维度筛选（状态、Span Name、输入/输出关键词、延时、[Token](../concepts/token.md) 量、标签等）  
  - 监控统计（调用次数、失败率、[Token](../concepts/token.md) 总量、首 Token 耗时、平均调用时长）  
  - 数据导出（JSONL / Excel）  
  - Span 数据一键导入评测集（支持字段映射与全量/追加模式）  
  - 标签标注（布尔值、分类、数字、文本四类，与评测标签系统共享）

> **注意**：应用观测目前暂无 API，所有操作均需通过控制台完成 [应用观测](../../raw/application-user-guide/application-monitoring/application-observation.md)；且明确不支持通过 Assistant API 创建的智能体应用。

## 关键参数

| 参数 | 说明 | 来源 |
|------|------|------|
| `延时`（调用时长） | LLM 节点延时包含完整输出过程；CHAIN 节点延时为端到端总耗时 | [应用观测](../../raw/application-user-guide/application-monitoring/application-observation.md) |
| `Token总量` | = 输入 Token 数 + 输出 Token 数（LLM 节点）；Embedding 节点仅统计向量化输入 Token | [应用观测](../../raw/application-user-guide/application-monitoring/application-observation.md) |
| `首 Token 耗时` | 仅对流式调用生效，指从请求发起至首个 Token 返回的时间 | [应用观测](../../raw/application-user-guide/application-monitoring/application-observation.md) |
| `Span ID` / `Trace ID` / `Request ID` | 用于跨节点关联与问题定位；可通过节点详情页「查看 ID」获取 | [应用观测](../../raw/application-user-guide/application-monitoring/application-observation.md) |

## 使用方式

### 前置配置（首次使用必做）
1. 主账号或已授权子账号访问 [应用观测](https://bailian.console.aliyun.com/tab=app?tab=app#/app-observe)，单击右上角「应用观测配置」  
2. 完成三项授权：  
   - 授权可观测链路 OpenTelemetry 服务角色权限  
   - 开通可观测链路 OpenTelemetry 服务  
   - 初始化 OpenTelemetry 存储 LogStore  
> ⚠️ 子账号需额外配置 `AliyunBailianFullAccess` + `应用观测-操作` 页面权限 + `CreateServiceLinkedRole` 系统策略（详见 [应用观测](../../raw/application-user-guide/application-monitoring/application-observation.md) 常见问题）

### 启用与观测
1. **添加应用**：在「选择被观测的应用」中添加已发布、且归属当前业务空间的应用  
2. **查看数据**：  
   - 列表页支持 Root Span / All Span / Model Span 三种视图模式  
   - 支持按时间范围（最长 30 天）、ID、关键词、数值区间、标签等条件组合过滤  
   - 单击 Span 名称可展开节点详情，查看原始输入/输出、标注记录、嵌套子节点  
3. **导出与复用**：  
   - Trace 列表页右上角「导出数据」支持 JSONL/Excel  
   - 「添加到评测集」支持批量 Span 导入，最多映射 50 个字段  

## 限制和注意事项

- **功能限制**：  
  - 不支持 Assistant API 创建的智能体应用 [应用观测](../../raw/application-user-guide/application-monitoring/application-observation.md)  
  - 高代码应用仅上报 `FullCodeApp` 入口节点，内部逻辑不可见；需在代码中集成 AgentScope-AI Tracing 模块，并部署时启用 `--telemetry enable` 参数  
  - [长期记忆](../concepts/long-term-memory.md)中的检索过程不可观测  
  - TextRetriever / VectorRetriever 默认返回 100 个切片，数量不可调  

- **数据时效性**：  
  - 指标更新频率为分钟级，非实时  
  - 关闭观测后历史数据停止同步，重新开启仅同步新增数据  

- **计费说明**：  
  - 应用监控功能本身免费  
  - 底层依赖 OpenTelemetry 服务，存储与查询费用按 [OpenTelemetry 计费说明](https://help.aliyun.com/zh/arms/tracing-analysis/product-overview/untitled-document-1697525445039) 执行  

- **权限与生效**：  
  - 主账号配置通常分钟级生效，高峰期可能延迟  
  - 子账号配置需严格遵循 [应用观测](../../raw/application-user-guide/application-monitoring/application-observation.md) 中的权限清单，缺一不可

## 来源文档

- [应用观测](../../raw/application-user-guide/application-monitoring/application-observation.md)



# application monitoring

应用观测（Application Monitoring）是阿里云百炼平台提供的端到端可观测能力，用于追踪应用内部调用链路、分析模型响应延时、查看大模型思考过程（如 Prompt 重写、检索、重排序、LLM 推理等），并采集 [Token](../concepts/token.md) 用量、耗时等关键指标。数据同步频率为分钟级，支持 30 天内历史数据回溯与多维筛选。该功能依赖可观测链路 OpenTelemetry 服务，[应用观测](../../raw/application-user-guide/application-monitoring/application-observation.md) 页面提供可视化界面与操作入口。

## 支持的模型/功能

- **支持的应用类型**：智能体应用、工作流应用、高代码应用（但高代码应用仅上报 `CHAIN` 根节点 `FullCodeApp`，不支持内部链路追踪）  
- **支持的节点类型**（按应用类型分类）：
  - 智能体应用：`CHAIN`（如 `AgentApp`）、`AGENT`、`RETRIEVER`（含 `TextRetriever`/`VectorRetriever`）、`REWRITER`、`EMBEDDING`、`RERANKER`、`LLM`、`TOOL`、`GUARDRAIL`
  - 工作流应用：除上述外，额外支持 `START`、`API`、`CLASSIFIER`、`TEXT_CONVERTER`、`SCRIPT`、`CONDITION`、`FUNCTION_COMPUTE`、`APP_FLOW`、`END`
  - 高代码应用：仅支持 `CHAIN` 类型节点，名称为 `FullCodeApp`，[原文标题](../../raw/application-user-guide/application-monitoring/application-observation.md) 明确说明“目前不支持追踪其内部调用链路”
- **核心功能**：调用链追踪（Root/All/Model Span 模式）、ID（Request ID / Trace ID / Span ID）搜索、字段自定义、数据导出（JSONL / Excel）、监控统计（调用次数、失败率、[Token](../concepts/token.md) 总量、首 [Token](../concepts/token.md) 耗时、平均调用时长）、Span 数据一键导入评测集、标签化数据标注（布尔/分类/数字/文本）

> **注意**：[原文标题](../../raw/application-user-guide/application-monitoring/application-observation.md) 中明确指出“应用观测目前暂无API”，且不支持通过 Assistant API 创建的智能体应用——该限制在文档中多次强调，开发者需确认应用创建方式是否符合要求。

## 关键参数

| 参数名 | 含义 | 说明 |
|--------|------|------|
| `Request ID` | 单次用户请求唯一标识 | 用于关联前端输入与后端全链路 |
| `Trace ID` | 全链路追踪唯一标识 | 同一请求下所有 Span 共享该 ID |
| `Span ID` | 单个节点唯一标识 | 用于定位具体节点（如 `LLM` 或 `VectorRetriever`） |
| `延时（ms）` | 节点执行耗时 | `LLM` 节点延时包含[流式输出](../concepts/streaming-output.md)全过程；`EMBEDDING` 延时指向量化耗时 |
| `Token总量` | 输入 Token + 输出 Token 总和 | `LLM` 和 `EMBEDDING` 节点均上报，单位为 token 数 |
| `状态` | 节点执行结果 | `正常` 或 `错误`（可进一步按错误类型细分） |

## 使用方式

1. **前提配置**（仅需一次）：
   - 主账号或已授权子账号访问 [应用观测配置](https://bailian.console.aliyun.com/tab=app?tab=app#/app-observe) 页面，完成：
     - 授权可观测链路 OpenTelemetry 服务角色权限
     - 开通可观测链路 OpenTelemetry 服务
     - 初始化 LogStore 存储（主账号开通通常分钟级生效；子账号需额外配置 `CreateServiceLinkedRole` 权限，详见 [原文标题](../../raw/application-user-guide/application-monitoring/application-observation.md)）

2. **启用观测**：
   - 应用必须已**发布**且属于当前业务空间
   - 在应用观测页面点击“选择被观测的应用” → “添加”，应用将自动开始上报数据（分钟级同步）

3. **查看与分析**：
   - 在 Span 列表页使用过滤器（状态、Span Name、输入/输出关键词、延时、Token 量、标签等）快速筛选
   - 点击节点名称展开详情，查看原始数据、标注记录、嵌套子节点
   - 切换至“监控统计”页签，按分钟/小时/天粒度查看趋势图（支持下载与复制）

4. **高级操作**：
   - 批量选中 Span → “添加到评测集”（支持字段映射与追加/覆盖模式）
   - 在节点详情页点击“数据标注”，为 Span 添加结构化标签（与评测系统共享标签管理）

## 限制和注意事项

- **功能限制**：
  - 不支持 Assistant API 创建的智能体应用（[原文标题](../../raw/application-user-guide/application-monitoring/application-observation.md) 明确声明）
  - 高代码应用无法观测内部节点，仅上报 `FullCodeApp` 根节点
  - [长期记忆](../concepts/memory.md)中的检索过程不可观测（仅知识库检索可见）
  - `TextRetriever` 和 `VectorRetriever` 默认返回 100 个切片，暂不支持调整数量

- **技术限制**：
  - 无公开 API，全部操作需通过控制台完成
  - 数据存储依赖 OpenTelemetry 服务，产生额外费用（应用观测功能本身免费）
  - 子账号需显式配置 `AliyunBailianFullAccess` + 页面权限 + `CreateServiceLinkedRole` 策略，否则无法完成初始化

- **使用注意事项**：
  - 关闭观测后历史数据停止同步，重新开启仅同步新增数据
  - 标签最多支持 50 个字段映射；评测集导入时需确保字段类型兼容
  - 高代码应用若未在部署时添加 `--telemetry enable` 参数，或未集成 AgentScope-AI 的 Tracing 模块，则无法上报任何可观测数据

## 来源文档

- [应用观测](../../raw/application-user-guide/application-monitoring/application-observation.md)



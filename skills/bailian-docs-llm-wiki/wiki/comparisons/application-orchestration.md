# 应用编排与调用方案对比：Managed Agents vs Application Call vs Bailian Application Calling

为帮助开发者在百炼平台中高效选型，本文系统对比三种核心应用编排与调用方案：**Managed Agents（托管智能体运行时）**、**Application Call（应用级调用 API）** 和 **Bailian Application Calling（百炼原生应用调用）**。三者定位不同：Managed Agents 面向深度可控的智能体生命周期与沙箱环境管理；Application Call 侧重 OpenAI 兼容性与多模态[异步任务](../concepts/asynchronous-task.md)调度；Bailian Application Calling 则是百炼平台最轻量、最主流的标准化应用集成方式。本对比基于当前（2024 年 Q3）正式发布能力，聚焦技术可行性、开发成本与运维边界，不涉及未来规划或灰度功能。

## 关键维度对比

| 维度 | Managed Agents | Application Call | Bailian Application Calling |
|------|----------------|------------------|----------------------------|
| **定位与角色** | 智能体“运行时基础设施”：提供 Agent/Environment/Session 全生命周期托管与事件驱动交互 | “兼容层网关”：OpenAI Responses API 兼容接口，支持同步/异步/流式调用，面向迁移友好型集成 | “平台原生调用标准”：百炼官方推荐的 SDK/HTTP 调用范式，强调简洁性、一致性与[插件](../concepts/plugin.md)扩展性 |
| **输入格式** | `POST /sessions/{id}/events`，请求体为 `input: [{role: "user", type: "message", content: "..."}]`，支持富媒体数组（含文件引用 ID） | • Responses API：`input` 字段（字符串或消息数组）<br>• DashScope API：`prompt`（单轮）或 `messages`（多轮）<br>• 支持 `input_image`、`input_file`（仅限智能体应用） | `input: {prompt: "..."}` 或 `input: {messages: [...]}`；`biz_params` 用于透传[插件](../concepts/plugin.md)参数；HTTP 请求体需严格包裹于 `input` 对象内 |
| **输出格式** | SSE 事件流（`session_status`, `message`, `tool_call`, `error` 等），需主动订阅 `/sessions/{id}/events/stream`；响应为结构化事件对象 | • 同步：JSON 响应（含 `output.text`/`output.choices`）<br>• 异步：返回 `task_id`，需轮询 `GET /responses/{task_id}`<br>• 流式：SSE 输出 `data: {...}` | JSON 响应统一结构：`{"output": {"text": "..."}, "usage": {...}, "request_id": "...", "debug": {...}}`；支持 `debug` 字段启用执行链路详情 |
| **支持模型** | 仅百炼托管模型：`qwen-plus` 等（通过 `model.id` 指定），**不支持自定义模型接入** | 由所调用的智能体/工作流底层模型决定；若应用配置了 `qwen-vl`，则支持图像输入；**不直接暴露模型选择权** | 同 Application Call —— 模型能力由应用发布时绑定的节点决定；调用方无需关心模型 ID，仅关注应用行为语义 |
| **API 端点** | `https://{workspace_id}.{region}.maas.aliyuncs.com/api/v1/agentstudio`（地域固定为 `cn-beijing`） | • Responses API：<br>`https://dashscope.aliyuncs.com/api/v2/apps/agent/{APP_ID}/compatible-mode/v1/responses`<br>• DashScope API：<br>`https://dashscope.aliyuncs.com/api/v1/apps/{APP_ID}/completion` | `https://dashscope.aliyuncs.com/api/v1/apps/{APP_ID}/completion`（统一 endpoint，自动路由） |
| **会话管理** | 显式 Session 资源：创建 → 发送事件 → 订阅流 → 状态终止；会话状态机清晰（`idle → running → idle/terminated`）；历史保留 7 天 | • DashScope API：支持 `session_id`（有效期 1 小时）<br>• Responses API：**不支持会话上下文**，必须显式传入完整 `input` 消息历史 | 支持 `session_id`（1 小时有效期，最多 50 轮）；若同时提供 `messages`，**优先使用 `messages`，忽略 `session_id`** |
| **多模态支持** | 支持文件上传（≤20 MB，经安全审核后挂载至沙箱），可作为消息内容或工具输入；**不原生支持图像输入** | ✅ 图像（`input_image`）和文件（`input_file`）均支持；文件仅限智能体应用，且需应用内配置检索模式 | ❌ **不支持图像输入**；文件需提前上传至百炼并获取 file_id，再通过 `biz_params` 或消息 content 引用（非直传） |
| **工具/[插件](../concepts/plugin.md)集成** | 通过 Skill（zip 包）封装工具，需安全扫描、版本化挂载；工具执行由平台沙箱隔离，支持复杂工具链编排 | 工作流应用天然支持插件节点；智能体应用可通过插件配置实现；参数通过 `biz_params` 透传 | ✅ 原生支持插件参数透传：`biz_params.user_defined_params.{plugin_code}.{param_key}`；要求插件在控制台配置为“业务透传”模式 |
| **计费方式** | 按 **Agent 运行时资源消耗** 计费（含模型调用 [Token](../concepts/token.md)、沙箱 CPU/内存、文件存储、Skill 扫描等）；费用归属工作空间 | 按 **实际调用次数与 [Token](../concepts/token.md) 消耗** 计费（同普通模型调用）；[异步任务](../concepts/asynchronous-task.md)按完成计费，不因排队等待产生费用 | 按 **应用调用次数与 [Token](../concepts/token.md) 消耗** 计费；`usage` 字段明确返回 `input_tokens`/`output_tokens` 及对应 `model_id`，便于精细化成本核算 |
| **典型场景** | • 需要强沙箱隔离与工具执行审计的金融/政务智能体<br>• 多 Agent 协同编排（如 Planner-Executor 架构）<br>• 长周期、状态敏感的自动化流程（如数据清洗+报告生成） | • 从 OpenAI 生态平滑迁移的客户<br>• 需要异步处理长耗时任务（如视频摘要、批量文档解析）<br>• 需要流式响应但又依赖百炼工作流逻辑的前端应用 | • 快速集成客服问答、知识库检索等标准智能体<br>• 编排含多个插件调用的工作流（如“查订单→调支付→发短信”）<br>• 对 SDK 简洁性与调试信息（`debug`）有强需求的内部系统 |

## 各方案适用场景建议

- **选择 Managed Agents 当且仅当**：  
  ✅ 你需对智能体运行环境进行细粒度控制（如定制沙箱依赖、限制网络访问、审计工具调用日志）；  
  ✅ 你的业务逻辑本质是“多步骤、带状态、需人工干预或外部系统协同”的复杂工作流；  
  ✅ 你已构建或计划构建可复用的 Skill 工具包，并希望平台统一管理其安全扫描与版本分发；  
  ❌ 不适合快速原型验证、简单问答或仅需调用现成应用的场景——开发与运维成本显著更高。

- **选择 Application Call 当且仅当**：  
  ✅ 你正在将现有 OpenAI 兼容应用迁移到百炼，且希望最小化代码改造（尤其是使用 `openai` 官方 SDK 的项目）；  
  ✅ 你需要异步执行长耗时任务（如小时级数据处理），并接受轮询结果的编程模型；  
  ✅ 你的输入必须包含原始图像（如拍照识别），且已配置 VL 模型工作流；  
  ❌ 不适合需要稳定会话上下文的多轮对话（Responses API 不支持）、或追求百炼原生最佳实践的团队。

- **选择 Bailian Application Calling 当且仅当**：  
  ✅ 你是百炼新用户，目标是快速上线一个智能体或工作流应用到业务系统；  
  ✅ 你需要调用含插件的工作流，并动态传递业务参数（如订单号、用户ID）；  
  ✅ 你重视调用可观测性（`debug` 字段）、Token 成本透明（`usage` 结构清晰）、以及 SDK 的持续演进支持；  
  ❌ 不适合需要自定义模型、强沙箱隔离、或必须兼容 OpenAI `chat.completions` 接口规范的遗留系统。

## 技术选型参考（面向开发者）

| 选型考量 | 推荐方案 | 理由 |
|----------|----------|------|
| **首次集成百炼，追求最快上线** | ✅ Bailian Application Calling | SDK 调用一行代码即可（`Application.call()`），文档清晰，错误码统一，社区支持最完善；HTTP 接口结构简单，调试友好。 |
| **已有 OpenAI 应用，需低成本迁移** | ✅ Application Call（Responses API） | 请求/响应格式与 OpenAI 完全一致，只需替换 endpoint 和 API Key；流式与异步能力开箱即用。 |
| **构建企业级 AI Agent 平台，需统一管控与审计** | ✅ Managed Agents | 提供 Agent/Environment/Session 三级资源模型，支持 Skill 版本化、文件安全审核、事件溯源，符合等保与合规要求。 |
| **调用含图像理解的工作流** | ✅ Application Call（DashScope API） | 唯一明确支持 `input_image` 参数的方案；需确保工作流已绑定 `qwen-vl` 等多模态模型。 |
| **需要插件参数动态透传（如调用 CRM 插件传 customer_id）** | ✅ Bailian Application Calling 或 Application Call | 两者均支持 `biz_params`；但 Bailian 方案的 `biz_params.user_defined_params` 结构更规范，且控制台配置指引更明确。 |
| **多轮对话稳定性与上下文长度要求高（>50 轮）** | ✅ Managed Agents | Session 无硬性轮次限制（仅受 Token 与超时约束），且状态机明确；另两种方案 `session_id` 最多支持 50 轮。 |
| **预算敏感，需精确追踪各模型 Token 消耗** | ✅ Bailian Application Calling | `usage.models` 字段直接返回每个模型的 `input_tokens`/`output_tokens`，颗粒度优于其他方案。 |

> **重要提醒**：  
> - 所有方案均需 `DASHSCOPE_API_KEY` 鉴权，**严禁硬编码密钥**，务必使用环境变量或密钥管理服务；  
> - 地域约束以实际 endpoint 为准：Managed Agents 严格限定 `cn-beijing`；Application Call 与 Bailian Calling 默认路由至北京，但跨地域 Workspace ID 需显式传入；  
> - 文件处理能力差异显著：Managed Agents 支持上传→审核→沙箱挂载全流程；Application Call/Bailian Calling 仅支持引用已上传文件（file_id），不提供上传接口；  
> - SDK 版本至关重要：Python SDK ≥1.26.2（Managed Agents）、≥1.14.0（Bailian）、≥1.20.0（Application Call）；Java SDK 同理，请查阅各方案最新文档确认。

## 被对比主题页

- [managed agents api](../api/managed-agents-api.md)
- [application call](../api/application-call.md)
- [bailian application calling](../guides/bailian-application-calling.md)



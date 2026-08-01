# 应用调用方式对比：Application Call vs Bailian Application Calling

为帮助开发者清晰理解百炼平台中两类主流应用调用机制的定位、能力边界与技术差异，本文对 **`Application Call`**（即文档 `api/application-call.md` 所述）与 **`Bailian Application Calling`**（即文档 `guides/bailian-application-calling.md` 所述）进行系统性对比分析。二者虽同属“调用已发布应用”的范畴，但在设计目标、协议抽象层级、功能覆盖范围及适用阶段上存在本质区别：前者是面向多模态、跨地域、高兼容性的**通用企业级调用范式**；后者是聚焦于智能体/工作流核心逻辑、强调插件透传与调试能力的**统一基础调用规范**。本对比旨在为技术选型提供客观、可落地的决策依据。

## 关键维度对比

| 维度 | Application Call | Bailian Application Calling |
|------|------------------|----------------------------|
| **定义与定位** | 百炼平台对外提供的标准化应用调用能力总称，涵盖 DashScope 原生 API 与 OpenAI 兼容 Responses API 两种协议，支持全类型应用（新版智能体、旧版智能体、工作流）及多模态输入 | 百炼平台内部统一的底层应用调用规范，特指基于 `POST /api/v1/apps/{app_id}/completion` 的 SDK/HTTP 调用方式，仅支持智能体应用与工作流应用两类，不包含旧版智能体 |
| **输入格式** | • 支持字符串（单轮文本）或结构化数组（含 `input_text`/`input_image`/`input_file`）<br>• Responses API 支持 `messages` 数组（OpenAI 格式）与 `biz_params` 分离传递<br>• 显式支持图像/文件等多模态输入（需模型与应用配置支持） | • `prompt`（字符串）或 `messages`（OpenAI 风格数组），二者互斥<br>• `input.biz_params.user_defined_params` 专用于插件参数透传<br>• **不原生支持图像/文件输入**；多模态需通过插件或自定义节点间接实现 |
| **输出格式** | • DashScope API 返回 `response.output.text` + `session_id` + `usage`<br>• Responses API 返回 OpenAI 兼容格式（含 `id`, `choices[0].message.content`, `usage` 等）<br>• 支持流式（`stream=true`）与异步（`background=true`）模式，响应结构差异化明显 | • 统一返回 `output.text` + `session_id` + `usage.models`（含 `model_id`, `input_tokens`, `output_tokens`）<br>• 支持 `debug: true` 返回完整执行链路（节点耗时、中间结果）<br>• **不支持流式与异步模式**；所有调用均为同步阻塞式 |
| **支持模型/应用类型** | • 新版智能体（Agent 2.0）<br>• 旧版智能体（Legacy Agent）<br>• 工作流（Workflow）<br>• 多模态模型（如 Qwen-VL）需显式配置启用 | • 智能体应用（Single Agent Application）<br>• 工作流应用（Workflow Application）<br>• **不支持旧版智能体**<br>• 模型能力由应用绑定的底层模型决定，无独立多模态模型声明 |
| **API 端点** | • DashScope 原生：`POST https://dashscope.aliyuncs.com/api/v1/apps/{APP_ID}/completion`<br>• OpenAI 兼容：`POST https://dashscope.aliyuncs.com/api/v2/apps/agent/{APP_ID}/compatible-mode/v1/responses` | • 统一端点：`POST https://dashscope.aliyuncs.com/api/v1/apps/{app_id}/completion`<br>• **仅此一个端点**，无兼容层封装 |
| **计费方式** | • 按实际调用消耗的 token 计费（`input_tokens` + `output_tokens`）<br>• 流式/异步调用不额外计费，但需注意异步任务轮询产生的 HTTP 请求不计费 | • 同样按 token 计费（`usage.models` 中明确统计）<br>• 插件调用产生的费用计入对应插件账单，与主应用 token 分离结算 |
| **会话管理** | • DashScope API：依赖 `session_id`（服务端生成，有效期 1 小时）<br>• Responses API：依赖客户端维护完整 `messages` 数组，**不支持自动上下文延续** | • 支持 `session_id`（服务端生成，有效期 1 小时，最多 50 轮）<br>• 支持 `messages` 数组（优先级高于 `session_id`），客户端完全掌控对话历史 |
| **典型场景** | • 需复用 OpenAI 生态代码（如 LangChain、LlamaIndex）的快速迁移项目<br>• 要求流式响应（如实时聊天界面）或异步处理（如长耗时报告生成）<br>• 涉及图像/文件上传的多模态交互（如文档解析、图文问答） | • 构建轻量级智能体或复杂工作流编排的生产级应用<br>• 需深度调试执行链路（如排查插件失败、节点耗时异常）<br>• 要求严格插件参数透传与业务变量注入（如动态传入用户 ID、地理位置） |

## 适用场景建议

- **选择 `Application Call` 当且仅当满足以下任一条件**：
  - 项目已使用 OpenAI SDK 或生态工具链（如 `openai` Python 包），需最小成本接入百炼；
  - 业务强依赖**[流式输出](../concepts/streaming-output.md)**（如客服对话逐字渲染）或**异步任务**（如批量数据处理后通知）；
  - 输入包含**图像、PDF、Word 等文件**，且应用已配置多模态能力；
  - 需调用**旧版智能体**（遗留系统兼容）；
  - 部署地域为德国（法兰克福）、新加坡、日本（东京）等非北京地域，且应用位于子业务空间（此时 `Workspace ID` 为必需参数）。

- **选择 `Bailian Application Calling` 当且仅当满足以下任一条件**：
  - 开发新智能体或工作流应用，追求**最简、最稳定、最可控的调用路径**；
  - 需要**精确控制插件参数**（如向搜索插件传入 `{"query": "最新财报", "time_range": "2024Q1"}`），且插件配置为“业务透传”；
  - 进行**生产环境问题排查**，依赖 `debug` 字段获取节点级执行详情；
  - 对**SDK 版本有明确要求**（如 Java 项目需 ≥ 2.12.0 以保障稳定性）；
  - 应用部署在华北2（北京）地域，且无需跨地域调用或旧版兼容。

> ⚠️ 注意：二者**非互斥关系**。同一应用可同时支持两种调用方式（只要应用已发布）。例如：前端用 `Application Call`（Responses API）实现流式聊天，后台任务调度用 `Bailian Application Calling`（SDK）执行带插件参数的批量分析。

## 技术选型参考（面向开发者）

| 选型考量 | 推荐方案 | 理由说明 |
|----------|----------|----------|
| **快速集成现有 OpenAI 项目** | ✅ Application Call（Responses API） | 仅需替换 `base_url` 和 API Key，零代码改造即可运行；`messages` 格式与 OpenAI 完全一致，学习成本最低。 |
| **构建高可靠工作流服务（如金融风控引擎）** | ✅ Bailian Application Calling | 统一端点 + 显式 `messages` + `debug` 调试 + 插件参数强校验，便于监控、审计与故障定位；避免兼容层引入的不确定性。 |
| **需要上传图片并让模型理解内容** | ✅ Application Call（DashScope 原生 API） | 唯一支持 `input_image` 字段的调用方式；工作流中需配合 `imageList` 入参与 VL 模型节点，`Bailian Application Calling` 无对应字段。 |
| **跨地域部署（如新加坡客户访问新加坡应用）** | ✅ Application Call（需传 `Workspace ID`） | `Bailian Application Calling` 文档明确限定仅支持北京地域；而 `Application Call` 的 DashScope API 在新加坡、东京等地域均有效（需正确配置 `Workspace ID`）。 |
| **调试插件调用失败原因** | ✅ Bailian Application Calling（启用 `debug: true`） | 可直接返回插件节点的原始请求/响应、错误码、耗时，`Application Call` 的 Responses API 不提供此类深度链路信息。 |
| **避免 SDK 版本碎片化风险** | ✅ Bailian Application Calling | 其文档对各语言 SDK 最低版本有明确要求（Python ≥1.14.0, Java ≥2.12.0），且统一基于 `Application.call()` 方法；`Application Call` 的 Responses API 依赖 OpenAI SDK，版本演进独立于百炼。 |

综上，`Application Call` 是面向**生态兼容性与能力广度**的“高速公路”，适合快速接入与复杂交互；`Bailian Application Calling` 是面向**稳定性、可控性与调试深度**的“专用轨道”，适合核心业务深度集成。开发者应根据项目阶段（MVP 快速验证 vs. 生产长期运维）、技术栈约束（是否已绑定 OpenAI）、以及关键能力需求（流式？多模态？插件调试？）进行理性权衡，而非简单视为“新旧替代”。

## 被对比主题页

- [application call](../api/application-call.md)
- [bailian application calling](../guides/bailian-application-calling.md)



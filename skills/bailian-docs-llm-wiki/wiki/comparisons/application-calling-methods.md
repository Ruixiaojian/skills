# 应用调用方式对比：Application Call vs Bailian Application Calling

本文旨在帮助开发者清晰区分百炼平台两种主流应用调用机制——`Application Call`（官方 API 层能力）与 `Bailian Application Calling`（面向业务集成的标准化调用范式），明确其设计定位、技术边界与适用场景，避免因概念混淆导致集成失败、功能缺失或计费异常。二者虽均用于触发已发布的智能体/工作流应用，但在协议抽象层级、输入范式、多模态支持、会话管理及地域约束等方面存在系统性差异，需结合具体业务需求审慎选型。

## 关键维度对比

| 维度 | Application Call | Bailian Application Calling |
|------|------------------|----------------------------|
| **定位与目标用户** | 百炼平台底层核心 API 能力，面向需要精细控制调用行为（如流式、异步、多模态）的高级开发者或平台集成方 | 百炼推荐的**标准业务集成方式**，面向快速接入、关注易用性与稳定性的应用开发者和业务系统工程师 |
| **输入格式** | 支持两种模式：<br>• 字符串 `input`（单轮文本）<br>• 消息数组 `input`（含 `role`/`content`，支持 `image_url`、`file_url` 等多模态字段） | 主要采用 `prompt`（字符串指令）+ 可选 `messages`（OpenAI 风格数组）；`biz_params` 严格限定为插件透传结构 `{ "user_defined_params": { "<plugin_code>": { ... } } }` |
| **输出格式** | • 同步调用：返回完整响应对象（含 `output.text`、`usage`、`session_id` 等）<br>• 异步调用：返回 `task_id`，需轮询获取结果<br>• 流式响应：逐 chunk 返回 `delta.content`（仅同步支持） | 统一返回结构化 JSON，含 `output.text`、`request_id`、`usage`；**不支持原生[流式输出](../concepts/streaming-output.md)**（无 `stream=true` 参数，响应为完整文本） |
| **支持模型/应用类型** | • 智能体（Agent 2.0 / 旧版）<br>• 工作流（Workflow）<br>• **多模态强支持**：图像（`input_image`）、文件（`input_file`）需满足特定模型与配置条件（如 VL 模型 + “自定义处理”） | • 智能体应用（Single-Agent）<br>• 工作流应用（Workflow）<br>• **纯文本优先**：未提及图像/文件输入支持；`prompt` 和 `messages` 均为文本语义，无原生多模态字段 |
| **API 端点** | • DashScope 原生：`POST https://dashscope.aliyuncs.com/api/v1/apps/{APP_ID}/completion`<br>• OpenAI 兼容（同步）：`POST https://dashscope.aliyuncs.com/api/v2/apps/agent/{APP_ID}/compatible-mode/v1/responses`<br>• **强制要求 `workspace_id`**（非北京地域必须作为 Base URL 或请求参数） | • 统一端点：`POST https://dashscope.aliyuncs.com/api/v1/apps/{APP_ID}/completion`<br>• **默认隐含华北2（北京）地域**；跨地域调用需手动替换 endpoint（如法兰克福需用 `https://dashscope.eu-central-1.aliyuncs.com`），但文档未明确指引 |
| **计费方式** | 按实际调用消耗计费：<br>• 同步/异步调用均计入 `application_call` 调用量<br>• 多模态输入（图像/文件）按对应模型 token + 文件解析量单独计费<br>• 流式响应按实际返回 token 计费 | 按 `application_call` 调用量计费，与 `Application Call` **计费项一致**；无额外多模态费用（因不支持）；`biz_params` 透传不产生额外费用 |
| **会话管理** | • DashScope API：依赖 `session_id`（服务端维护，有效期 1 小时）<br>• [OpenAI 兼容接口](../concepts/openai-compatible-interface.md)：**不支持上下文管理**，必须显式传递完整 `messages` 数组 | • 支持 `session_id`（云端会话，50 轮/1 小时）<br>• 支持 `messages` 数组（OpenAI 格式），**与 `session_id` 共存时以 `messages` 为准**，提供更可控的上下文 |
| **异步能力** | ✅ 原生支持：通过 `background=true` 启用，立即返回 `task_id`，需轮询 `/tasks/{task_id}` 获取结果 | ❌ **不支持异步调用**；所有请求均为同步阻塞式，超时由客户端控制（默认 60s） |
| **典型场景** | • 实时多模态交互（如图文问答、PDF 解析）<br>• 长耗时工作流执行（需异步解耦）<br>• 与 OpenAI 生态深度兼容（如迁移现有 SDK）<br>• 需精确控制流式渲染体验（如聊天界面逐字输出） | • 快速集成问答助手、内容生成等轻量级智能体<br>• 编排复杂工作流（含插件调用、条件分支）并获取结构化结果<br>• 企业内部系统（ERP/CRM）嵌入式调用，强调稳定性与开发效率<br>• 多语言 SDK 快速上手（Python/Java/Node.js 等开箱即用） |

## 适用场景建议

### 选择 `Application Call` 当：
- 你的应用**必须处理图像、上传文件等多模态输入**，且已配置通义千问 VL 模型与对应处理逻辑；
- 业务流程中存在**耗时超过 30 秒的任务**（如大规模数据处理、多步骤外部 API 调用），需通过异步模式避免客户端超时；
- 前端需要**流式响应体验**（如 AI 编程助手逐行生成代码），且能接受 [OpenAI 兼容接口](../concepts/openai-compatible-interface.md)的上下文管理限制；
- 系统已深度集成 OpenAI SDK，希望**最小改造迁移至百炼**，复用现有 `client.responses.create()` 调用逻辑；
- 部署在**德国、新加坡、日本等非北京地域**，且需严格遵循 Workspace ID 的路由规则。

### 选择 `Bailian Application Calling` 当：
- 以**快速上线、降低维护成本**为首要目标，无需定制多模态或异步能力；
- 主要调用**智能体应用**（如客服机器人、营销文案生成器）或**含插件的工作流**（如“查订单→调支付→发短信”流程）；
- 团队熟悉 `prompt` + `biz_params` 的简单范式，或已有基于 `messages` 数组的对话管理逻辑；
- 运维要求**地域收敛**（统一部署在北京），或可接受跨地域调用时手动配置 endpoint；
- 安全合规要求高，需严格遵循 `API Key` 环境变量注入、`biz_params` 插件白名单等最佳实践。

## 技术选型参考（面向开发者）

| 你的需求 | 推荐方案 | 关键理由 |
|----------|----------|----------|
| “我要把 PDF 上传给智能体提取关键信息” | ✅ Application Call | `input_file` 字段 + 工作流中配置“全文引用”是唯一支持路径 |
| “工作流执行可能长达 2 分钟，不能让前端一直等待” | ✅ Application Call | `background=true` 异步模式 + 轮询机制是官方唯一支持方案 |
| “我们用 Python SDK，希望 10 行代码完成智能体调用” | ✅ Bailian Application Calling | `Application.call(prompt=...)` 接口简洁，`biz_params` 插件透传文档清晰 |
| “现有系统用 OpenAI SDK，想无缝切换到百炼” | ✅ Application Call（[OpenAI 兼容接口](../concepts/openai-compatible-interface.md)） | `client.responses.create()` 调用方式完全一致，仅需修改 `base_url` 和 `api_key` |
| “应用部署在新加坡，但控制台只显示北京的 Workspace ID” | ⚠️ Application Call（需谨慎） | 必须从新加坡地域控制台获取对应 `workspace_id`，并拼接正确 endpoint（如 `https://dashscope.ap-southeast-1.aliyuncs.com`），否则 403 |
| “需要保证每轮对话上下文绝对准确，避免 session 过期丢失” | ✅ Bailian Application Calling（使用 `messages`） | 显式传入完整对话历史，彻底规避 `session_id` 时效性风险，控制权在客户端 |

> **重要提醒**：两种方式**并非互斥**，而是互补。一个业务系统可混合使用：对核心多模态模块采用 `Application Call`，对常规问答模块采用 `Bailian Application Calling`。请始终以 [百炼官方错误码文档](https://help.aliyun.com/zh/model-studio/developer-reference/error-code) 为调试依据，并在生产环境启用 `request_id` 日志追踪。

## 被对比主题页

- [application call](../api/application-call.md)
- [bailian application calling](../guides/bailian-application-calling.md)



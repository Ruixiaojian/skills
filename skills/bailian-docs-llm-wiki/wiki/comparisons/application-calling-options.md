# 应用调用方式对比：Application Call、Managed Agents 与 Bailian Application Calling

为帮助开发者在百炼平台中高效选型，本文系统对比三种核心应用调用机制：**Application Call**（新版统一调用能力）、**Managed Agents**（托管式智能体运行时）与**Bailian Application Calling**（经典应用调用方式）。三者定位不同——Application Call 是面向已发布应用的生产级 API 调用范式；Managed Agents 是面向长周期、有状态、需沙箱执行的智能体开发范式；Bailian Application Calling 则是兼容早期 Agent 1.0 和工作流应用的轻量集成方式。理解其差异对架构设计、成本控制、功能实现与运维复杂度评估至关重要。

## 关键维度对比

| 维度 | Application Call | Managed Agents | Bailian Application Calling |
|------|------------------|----------------|----------------------------|
| **定位与本质** | 已发布应用（Agent 2.0 / 旧版 Agent / 工作流）的标准化 API 调用能力，强调**发布即服务（PaaS 层调用）** | 托管式智能体运行时环境，提供沙箱、会话、工具链全生命周期管理，强调**运行时可控性与扩展性（IaaS+Runtime 层）** | 面向 Agent 1.0 及工作流应用的兼容性调用方式，强调**快速集成与低门槛接入（SaaS 层轻量调用）** |
| **输入格式** | • `input`: 字符串（单轮文本）或消息数组（多轮+[多模态](../concepts/multi-modal.md)）<br>• 支持 `input_text`/`input_image`/`input_file`（需模型与配置支持）<br>• Responses API 必须传全量历史；DashScope API 可选 `session_id` | • `POST /sessions/{id}/events`: 事件驱动，支持 `message`（用户输入）、`tool_call`（工具触发）等结构化事件<br>• 输入内容为纯文本（`content` 字段），文件通过预挂载资源路径（如 `/mnt/session/uploads/data.csv`）引用 | • `prompt`: 纯文本指令（单轮）<br>• 或 `messages`: 标准 OpenAI 风格消息数组（多轮）<br>• `biz_params.user_defined_params`: 插件参数透传（仅限已关联插件）<br>• **不支持图像/文件等[多模态](../concepts/multi-modal.md)原生输入** |
| **输出格式** | • 同步：`output.text`（文本）或完整 `output` 对象（含 `session_id`, `task_id` 等）<br>• 异步：返回 `task_id`，需轮询 `retrieve` 接口获取结果<br>• 支持流式（`stream=true`，仅同步且工作流启用流式开关） | • SSE 流式事件响应：<br> - `message`: 模型生成文本<br> - `tool_output`: 工具执行结果<br> - `session_status`: 会话状态变更（如 `completed`, `failed`）<br>• 无统一“最终输出”结构，需按事件类型聚合处理 | • 同步返回 JSON，含 `output.text`（主文本结果）及 `session_id`（若启用）<br>• **不支持异步模式与[流式输出](../concepts/streaming-output.md)** |
| **支持模型** | • Agent 2.0：支持 Qwen 系列（`qwen-max`, `qwen-plus`, `qwen-vl` 等）<br>• 工作流：取决于节点配置（可混合使用文本/[多模态](../concepts/multi-modal.md)模型）<br>• **明确支持多模态模型（如 qwen-vl）及文生图模型（需工作流节点配置）** | • 当前明确支持 `qwen3-max`, `qwen3.7-plus` 等 Qwen 大模型<br>• 模型由 `model.id` 显式指定，独立计费<br>• **不支持多模态输入（图像/文件）**，所有输入均为文本指令，文件操作通过沙箱内路径完成 | • 仅支持文本类大模型（`qwen-max`, `qwen-plus` 等）<br>• **明确不支持 multimodal 模型（如 qwen-vl）及文生图模型** |
| **API 端点** | • Responses API（OpenAI 兼容）：<br> `POST https://dashscope.aliyuncs.com/api/v2/apps/agent/{APP_ID}/compatible-mode/v1/responses`<br>• DashScope API（原生）：<br> `POST https://dashscope.aliyuncs.com/api/v1/apps/{APP_ID}/completion` | • REST + SSE：<br> `POST /v1/agents`（创建 Agent）<br> `POST /v1/environments`（创建环境）<br> `POST /v1/sessions`（启动会话）<br> `POST /v1/sessions/{id}/events`（发送事件）<br> `GET /v1/sessions/{id}/events/stream`（订阅事件流） | • 统一端点：<br> `POST https://dashscope.aliyuncs.com/api/v1/apps/{APP_ID}/completion`<br>• SDK 封装后调用 `Application.call()` |
| **会话管理** | • DashScope API：`session_id` 自动维护（有效期 1 小时，最多 50 轮）<br>• Responses API：**无隐式会话，必须显式传 `messages` 数组**<br>• 工作流应用支持 `session_id`，但上下文持久化依赖应用自身配置 | • 原生会话（Session）抽象，生命周期独立管理<br>• `session_id` 由平台分配，状态（`running`/`completed`/`terminated`）明确<br>• 支持资源挂载（文件）、环境隔离、事件追溯 | • `session_id`：云端加载历史（最多 50 轮，1 小时过期）<br>• `messages`：显式传入，完全由开发者控制上下文<br>• **`session_id` 与 `messages` 互斥，同时存在时后者优先** |
| **异步与长任务支持** | • ✅ 支持 `background=true` 异步调用（返回 `task_id`）<br>• 适用于报告生成、多步骤工作流等耗时场景<br>• **不支持异步[流式输出](../concepts/streaming-output.md)** | • ✅ 原生支持长周期任务<br>• 会话 `running` 状态即持续运行，可处理数分钟至数小时任务<br>• 通过事件流实时感知中间状态（如工具执行中、代码运行日志） | • ❌ **不支持异步调用**<br>• 所有请求为同步阻塞，超时默认 60 秒（受模型与工作流复杂度影响） |
| **多模态支持** | • ✅ 完整支持：<br> - 图像：需 VL 模型 + 应用启用「自定义处理」或工作流配置 `imageList`<br> - 文件：智能体应用支持「全文引用」/「切片检索」 | • ❌ 不支持图像/音视频等原生多模态输入<br>• ✅ 支持文件操作（`read`/`write`/`download_file`），但文件需预先上传并挂载至沙箱路径 | • ❌ **完全不支持多模态输入**（文档明确限制仅文本模型） |
| **计费方式** | • 按调用次数 + 模型 [Token](../concepts/token.md) 消耗计费<br>• 异步任务按实际执行时间与模型消耗计费<br>• APP ID 与 Workspace ID 为静态标识，不计费 | • **三重独立计费**：<br> - 运行时费用：0.5 元/小时（会话 `running` 状态计费）<br> - 模型 [Token](../concepts/token.md) 费：按所选 `model.id` 的公开标准计费<br> - 工具/MCP 调用费：按次计费（如 `bash`, `download_file`） | • 按调用次数 + 模型 [Token](../concepts/token.md) 消耗计费<br>• 无运行时费用、无工具调用费<br>• 计费模型与 Application Call 中的文本类模型一致 |
| **典型场景** | • 生产环境调用已发布的智能体/工作流（如客服机器人、自动化报告生成）<br>• 需要多模态输入（图文问答、文档解析）<br>• 需要[异步处理](../concepts/asynchronous-processing.md)长任务并轮询结果 | • 需要沙箱执行代码（数据分析、脚本自动化）<br>• 多步工具协同（如“下载PDF→提取表格→生成图表→发送邮件”）<br>• 需要细粒度事件监控与中间状态干预 | • 快速集成已有 Agent 1.0 或简单工作流到业务系统（如内部知识库问答）<br>• 单轮问答或短对话场景<br>• 对沙箱、工具、长任务无需求的轻量级应用 |

## 适用场景建议

| 场景描述 | 推荐方案 | 理由说明 |
|----------|----------|----------|
| **需要调用一个已上线、支持图文识别的智能体应用（如合同图像审核）** | ✅ Application Call | 唯一支持 `input_image` 多模态输入的方案，且 DashScope API 提供稳定 `session_id` 上下文管理，适合生产集成。 |
| **构建一个能自动运行 Python 脚本、读写文件、调用外部 API 的数据分析智能体** | ✅ Managed Agents | 唯一提供内置沙箱（`bash`/`read`/`download_file`）、独立会话生命周期与事件流反馈的方案，满足长时、有状态、需干预的复杂任务需求。 |
| **将一个简单的 FAQ 问答工作流快速嵌入企业微信侧边栏，仅需单轮文本交互** | ✅ Bailian Application Calling | 最简集成路径：无需理解会话/环境/事件概念，SDK 一行 `Application.call()` 即可完成，且兼容存量 Agent 1.0 应用。 |
| **需要异步生成一份 10 页 PDF 报告，并在完成后通过 Webhook 通知业务系统** | ⚠️ Application Call（需自行实现轮询+Webhook）<br>✅ Managed Agents（推荐） | Application Call 支持异步但**无 Webhook 回调**，需轮询；Managed Agents 通过 `session_status: completed` 事件天然支持事件驱动通知，更契合该场景。 |
| **已有 OpenAI 生态代码（如 LangChain + OpenAI SDK），希望最小改造接入百炼** | ✅ Application Call（Responses API） | [OpenAI 兼容接口](../concepts/openai-compatible-interface.md)（`/responses`）可直接复用现有 `openai` SDK，仅需更换 `base_url` 与 `api_key`，迁移成本最低。 |
| **应用需频繁上传用户文件并进行全文检索，且要求文件内容不被其他会话访问** | ✅ Application Call（智能体应用 + 「全文引用」）<br>✅ Managed Agents（挂载资源 + 沙箱隔离） | 两者均满足：Application Call 在智能体配置中启用「全文引用」即可安全处理；Managed Agents 通过 `/mnt/session/uploads/` 路径挂载，沙箱天然隔离。 |

## 技术选型参考（致开发者）

- **优先选择 `Application Call` 当**：  
  ✅ 你的应用已在百炼控制台**正式发布**（Agent 2.0 / 工作流）；  
  ✅ 业务需要**图像、文件等多模态输入支持**；  
  ✅ 需要**异步执行长任务**（如批量处理）；  
  ✅ 团队熟悉 OpenAI 生态，追求**快速迁移与标准化 API**；  
  ❌ 避免用于需沙箱执行代码、需实时事件反馈、或需深度定制工具链的场景。

- **优先选择 `Managed Agents` 当**：  
  ✅ 任务本质是**多步骤、有状态、需沙箱环境**（如数据清洗→建模→可视化）；  
  ✅ 需要**精确控制工具调用时机与中间结果**（如根据 `tool_output` 动态决定下一步）；  
  ✅ 要求**运行时资源隔离与安全性**（每个会话独立沙箱）；  
  ✅ 接受更高运维复杂度以换取**极致可控性与扩展性**；  
  ❌ 避免用于简单问答、无工具依赖、或对延迟极度敏感（沙箱启动有毫秒级开销）的场景。

- **优先选择 `Bailian Application Calling` 当**：  
  ✅ 集成对象是**存量 Agent 1.0 或轻量工作流**，且无多模态/长任务需求；  
  ✅ 开发目标是**极简、零配置、快速上线**（如内部工具）；  
  ✅ 团队技术栈较轻，**无需管理会话生命周期或事件流**；  
  ❌ 避免用于新项目开发——因其不

## 被对比主题页

- [application call](../api/application-call.md)
- [managed agents](../guides/managed-agents.md)
- [bailian application calling](../guides/bailian-application-calling.md)



# 应用调用方式对比：Application Call、Bailian 调用与 Managed Agents

本文旨在帮助开发者清晰理解百炼平台三种主流应用调用机制的技术定位、能力边界与适用场景，为 AI 应用集成提供客观、可落地的技术选型参考。随着百炼平台演进，`Application Call`（新版统一调用）、`Bailian 调用`（旧版兼容接口）与 `Managed Agents API`（细粒度托管运行时）已形成分层互补的能力矩阵：前者面向“开箱即用”的应用集成，后者聚焦“深度可控”的智能体工程化交付。本对比基于当前（2024年Q3）正式发布文档与控制台实际能力，不包含灰度或内测特性。

## 关键维度对比

| 维度 | Application Call | Bailian 调用 | Managed Agents API |
|------|------------------|--------------|---------------------|
| **定位与目标用户** | 百炼平台**推荐的标准化应用调用方式**，面向业务系统快速集成已发布智能体/工作流 | **向后兼容的旧版调用入口**，主要服务存量 Agent 1.0 及早期工作流应用迁移过渡 | **面向智能体工程化交付的托管运行时 API**，面向需要全生命周期管控、沙箱隔离与事件驱动架构的高级开发者 |
| **输入格式** | 支持两种结构：<br>• DashScope 风格：`input.prompt` 或 `input.messages`（含 role/content/image_url/file_url）<br>• OpenAI 兼容风格：`messages` 数组（含 `user`/`system`/`assistant` 角色），支持[多模态](../concepts/multimodal.md)嵌套 | 单一结构：`input.prompt`（单轮）或 `input.messages`（多轮），`biz_params.user_defined_params` 用于插件透传；**不支持原生图像/文件 URL 直传**，需预处理为文本描述 | 事件驱动：通过 `POST /sessions/{id}/events` 提交 `input` 消息数组，每条消息含 `role`、`type`（`message`/`file`）、`content`；文件需**预先上传并审核通过**后引用 `file_id` |
| **输出格式** | • 同步调用：JSON 响应体含 `output.text`、`output.choices[0].message.content` 等<br>• 异步调用：返回 `id`（任务ID），后续 `GET /apps/{app_id}/tasks/{id}` 获取结果<br>• 流式响应（仅同步）：SSE 或 chunked JSON，按 token 返回 | 同步 JSON 响应，结构固定：`output.text` + `output.session_id`（若启用会话）；**无异步模式，无流式支持** | 事件流（SSE）：监听 `/sessions/{id}/events/stream`，接收 `session_status`（`running`/`idle`/`terminated`）及 `message` 事件；消息内容在 `data` 字段中，含 `role`、`content`、`tool_calls` 等完整执行轨迹 |
| **支持模型/应用类型** | ✅ 新版智能体（Agent 2.0）<br>✅ 旧版智能体（Agent 1.0）<br>✅ 工作流应用<br>⚠️ 文件输入仅限智能体应用且需配置检索模式；图像输入需 VL 模型 | ✅ 智能体应用（Agent 1.0）<br>✅ 工作流应用<br>❌ 不支持新版智能体（Agent 2.0）<br>❌ 不支持文生图类节点 | ✅ 仅支持百炼平台已发布的模型（如 `qwen-plus`），需在 `Agent` 创建时显式指定<br>✅ 完整支持工具调用、沙箱执行、技能（Skill）挂载<br>❌ 不直接支持工作流编排（需将工作流逻辑封装为 Skill） |
| **API 端点** | • DashScope 原生：`POST https://dashscope.aliyuncs.com/api/v1/apps/{APP_ID}/completion`<br>• OpenAI 兼容：`POST https://dashscope.aliyuncs.com/api/v2/apps/agent/{APP_ID}/compatible-mode/v1/responses` | 统一端点：`POST https://dashscope.aliyuncs.com/api/v1/apps/{app_id}/completion` | 多资源端点：<br>• `POST https://{workspace_id}.cn-beijing.maas.aliyuncs.com/api/v1/agentstudio/sessions`<br>• `POST https://{workspace_id}.cn-beijing.maas.aliyuncs.com/api/v1/agentstudio/sessions/{id}/events`<br>• `GET https://{workspace_id}.cn-beijing.maas.aliyuncs.com/api/v1/agentstudio/sessions/{id}/events/stream` |
| **会话管理** | • DashScope 风格：依赖 `session_id`（服务端生成，有效期1小时）<br>• OpenAI 风格：**必须传全量 `messages` 历史**，无隐式上下文 | • `session_id` 方式（有效期1小时，最多50轮）<br>• `messages` 数组方式（显式传入历史） | **Session 为一级资源**：创建 Session 即启动独立执行实例；状态机驱动（`idle`→`running`→`idle`/`terminated`）；**会话间完全隔离，无共享上下文** |
| **计费方式** | 按调用次数 + 模型 [Token](../concepts/token.md) 消耗计费（与 DashScope 计费体系一致）；异步调用按任务计费 | 同 Application Call（底层复用相同计费通道） | 按 **Session 运行时长（秒） + 模型 [Token](../concepts/token.md) + 文件存储 + 技能执行** 综合计费；沙箱资源消耗单独计量 |
| **地域支持** | 华北2（北京）为默认；德国（法兰克福）、新加坡、日本（东京）等需显式传入 `Workspace ID` 并使用对应 Base URL | 智能体应用：全地域支持；工作流应用：**仅华北2（北京）** | **严格限定 `cn-beijing` 地域**；`workspace_id` 为 URL 必需组成部分，不支持跨地域调用 |
| **典型场景** | • 企业客服机器人对接 CRM 系统<br>• [多模态](../concepts/multimodal.md)内容分析服务（图文混合输入）<br>• 需要流式响应的实时对话界面<br>• 快速集成已发布的工作流审批流程 | • 迁移存量 Agent 1.0 应用，保持代码最小改动<br>• 简单插件调用场景（如天气查询、知识库检索）<br>• 无需流式、无复杂会话状态的轻量级集成 | • 构建高安全要求的金融/政务智能助手（沙箱隔离敏感操作）<br>• 需要完整执行日志与事件溯源的审计场景<br>• 自定义工具链深度集成（如私有 API 封装为 Skill）<br>• 长周期、多步骤、状态可中断的复杂任务编排 |

## 各方案适用场景建议

- **优先选择 `Application Call`**：  
  当您的需求是**快速、稳定、标准化地调用已在百炼控制台发布好的智能体或工作流应用**，且对[多模态](../concepts/multimodal.md)输入（图像/文件）、流式响应、OpenAI 兼容性、跨地域部署有明确要求时。这是百炼当前主推和持续增强的调用范式，覆盖绝大多数业务集成场景。

- **谨慎使用 `Bailian 调用`**：  
  仅适用于**维护存量 Agent 1.0 应用或早期工作流应用**，且短期内无升级计划的情况。新项目开发**强烈不建议选用**，因其功能受限（无流式、无异步、不支持新版智能体），且长期将逐步收敛至 `Application Call` 体系。若需插件透传，务必确认插件配置为“业务透传”且在同一业务空间。

- **选用 `Managed Agents API`**：  
  当您需要**超越“调用一个黑盒应用”的控制粒度**，例如：要求每个用户会话拥有独立沙箱环境、需精确追踪每一步工具调用与状态变迁、需将私有代码封装为可复用技能、或需对执行时长与资源消耗进行精细化成本核算时。它代表了百炼平台最底层、最灵活的智能体运行时能力，但开发与运维复杂度显著更高。

## 技术选型决策指南（面向开发者）

| 您的问题 | 推荐方案 | 理由简述 |
|----------|----------|----------|
| “我有一个在控制台发布好的智能体，想用 Python SDK 快速接入网页聊天框，需要流式返回。” | ✅ Application Call（OpenAI 兼容模式） | 直接复用 `client.responses.create(..., stream=True)`，代码零改造，流式支持完善。 |
| “我正在维护一个用了两年的 Agent 1.0 应用，调用代码是 `Application.call()`，现在只想让它继续跑，不改架构。” | ⚠️ Bailian 调用 | 兼容性最佳，风险最低；但需注意其地域限制（工作流仅北京）及未来停服可能。 |
| “我要构建一个能操作内部 HR 系统的智能助手，所有 API 调用必须在隔离沙箱中执行，并记录每一步操作日志供审计。” | ✅ Managed Agents API | 唯一支持沙箱（`Environment`）、完整事件流（`/events/stream`）与技能（`Skill`）封装的方案。 |
| “我的应用需要同时调用多个不同模型的智能体，并统一管理会话状态。” | ✅ Application Call（DashScope 风格 + `session_id`） | `session_id` 提供跨应用会话粘性，且 `app_id` 可动态切换，比 Managed Agents 的 Session 绑定更轻量。 |
| “我需要异步处理一个耗时 5 分钟的报告生成任务，并在完成后通知用户。” | ✅ Application Call（`background=true`） | 原生支持异步任务提交与轮询，无需自行实现状态机与回调；Managed Agents 需自行监听 `terminated` 事件并触发通知。 |
| “我想把公司内部的 Excel 数据分析脚本封装成一个可被智能体调用的工具。” | ✅ Managed Agents API（Skill） | Skill 机制专为此设计：打包脚本 → 上传 → 扫描 → 挂载到 Agent，安全可控。Bailian/Application Call 仅支持预置插件，无法集成私有脚本。 |

> **重要提醒**：  
> - 所有方案均**禁止硬编码 API Key**，请务必通过环境变量（`DASHSCOPE_API_KEY`）或密钥管理服务注入。  
> - `APP ID` 和 `Workspace ID` **仅可通过百炼控制台手动获取**，无 API 查询接口，请提前规划权限（需 `AliyunBailianFullAccess`）。  
> - 地域选择直接影响可用性：若业务部署在新加坡，`Application Call` 可用，`Managed Agents API` 不可用，`Bailian 调用` 中的工作流应用不可用。  
> - 新项目开发，请以 `Application Call` 为起点；复杂智能体工程化需求，再评估 `Managed Agents API` 的投入产出比。

## 被对比主题页

- [application call](../api/application-call.md)
- [bailian application calling](../guides/bailian-application-calling.md)
- [managed agents api](../api/managed-agents-api.md)



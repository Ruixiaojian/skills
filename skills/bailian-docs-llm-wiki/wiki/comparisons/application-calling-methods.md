# 应用调用方式对比：Bailian 应用调用 vs Application Call API

## 背景与目的  
随着百炼平台能力演进，开发者面临两种主流应用调用路径：**Bailian 应用调用**（即传统 `Application.call` 方式）与 **Application Call API**（新版统一调用接口）。二者在功能覆盖、协议设计、地域支持及工程实践上存在显著差异。本文旨在为开发者提供清晰、可落地的技术选型参考，帮助其根据业务场景（如是否需多模态、异步执行、跨地域部署或 OpenAI 兼容性）选择最适配的调用方案，避免因接口误用导致调用失败、功能缺失或运维复杂度上升。

---

## 关键维度对比

| 维度 | Bailian 应用调用（`dashscope.Application.call`） | Application Call API（`/api/v1/apps/{app_id}/completion` 或 `/api/v2/.../responses`） |
|------|--------------------------------------------------|----------------------------------------------------------------------------------------|
| **输入格式** | 支持 `prompt`（字符串）或 `messages`（标准 ChatML 数组），`input` 为顶层对象；`biz_params` 与 `parameters` 平级 | `input` 为必填字段，类型灵活：可为字符串（纯文本）、消息数组（含 `role`/`content`），亦支持图像（`image_url`）、文件（`file_url`）等多模态结构体；`biz_params` 仅异步调用可用 |
| **输出格式** | 固定结构：`response.output.text`（文本结果）+ `response.session_id`（若启用会话）；调试日志需显式开启 `debug.enable` | 同步调用返回标准 JSON 响应（含 `output.text` 或 `output.choices[0].message.content`）；异步调用返回 `task_id`；Responses API 兼容 OpenAI 格式（`choices[0].message.content`），流式响应遵循 SSE 协议 |
| **支持模型/应用类型** | 仅支持智能体应用（Single Agent）和工作流应用（Workflow）；不支持旧版智能体（Agent 1.0） | 全面支持：新版智能体（Agent 2.0）、旧版智能体（Agent 1.0）、工作流应用；明确兼容历史存量应用 |
| **API 端点** | 统一端点：`https://dashscope.aliyuncs.com/api/v1/apps/{app_id}/completion`（仅限华北2 北京） | 双端点体系：<br>• DashScope 风格：`/api/v1/apps/{app_id}/completion`（同 Bailian）<br>• OpenAI 兼容 Responses API：`/api/v2/apps/agent/{app_id}/compatible-mode/v1/responses`（支持同步/异步） |
| **调用模式** | 仅同步调用；支持 `session_id` 自动上下文恢复（1 小时有效期，最多 50 轮） | 同步 + 异步双模式：<br>• 同步：`background=false`（默认）<br>• 异步：`background=true`，返回 `task_id`，需后续 `retrieve` 查询<br>• 流式支持：`stream=true`（同步下启用，工作流需流程中显式开启） |
| **多模态能力** | ❌ 不支持图像、文件等非文本输入；输入严格限定为 `prompt` 或 `messages` 文本结构 | ✅ 完整支持：<br>• 图像：通过 `input` 中 `{"type":"image_url","image_url":{"url":"..."}}` 传入（需 VL 模型）<br>• 文件：通过 `{"type":"file_url","file_url":{"url":"..."}}`（仅智能体应用支持） |
| **地域与 Workspace 支持** | 明确限定华北2（北京）；未提供 `workspace_id` 参数，无法跨业务空间调用 | 显式支持多地域 & 多业务空间：<br>• 需配合 `workspace_id` 使用（如德国法兰克福、新加坡、日本东京）<br>• Endpoint 构建需嵌入 workspace 信息（如 `https://dashscope.aliyuncs.com/api/v2/apps/agent/{app_id}?workspace_id=xxx`） |
| **计费方式** | 按调用次数 + 模型 token 消耗计费；所有调用统一计入 `bailian_application_call` 计费项 | 计费逻辑一致，但异步调用中任务创建（`background=true`）本身不计费，仅最终执行结果按 token 计费；流式调用按实际返回 token 计费 |
| **SDK 与协议兼容性** | 专用 DashScope SDK（`dashscope.Application`）；无 OpenAI 兼容层 | 提供双 SDK 支持：<br>• DashScope SDK（推荐）<br>• OpenAI 官方 SDK（`openai.OpenAI`）+ 自定义 `base_url`，零代码改造迁移现有 OpenAI 项目 |
| **典型场景** | • 快速集成简单问答/内容生成类智能体<br>• 已有 DashScope SDK 生态且无需多模态/异步能力<br>• 北京地域内轻量级工作流编排 | • 需要图像理解、文档解析等多模态能力<br>• 长耗时任务（如批量报告生成、复杂工具链执行）需异步解耦<br>• 跨地域部署或使用子业务空间（Workspace）<br>• 现有 OpenAI 项目平滑迁移 |

---

## 适用场景建议

### ✅ 推荐使用 **Bailian 应用调用** 的场景：
- 业务系统已深度集成 DashScope SDK，且当前需求仅为**单轮/多轮纯文本交互**（如客服机器人、FAQ 问答）；
- 应用全部部署于**华北2（北京）地域**，无跨地域或 Workspace 管理诉求；
- 对**插件参数透传**（`biz_params.user_defined_params`）有强依赖，且插件已配置“业务透传”；
- 开发团队熟悉 `session_id` 会话管理机制，且能接受 1 小时会话有效期约束。

### ✅ 推荐使用 **Application Call API** 的场景：
- 需要**图像识别、PDF 解析、表格理解等多模态能力**（必须选用 VL 模型并配置对应输入结构）；
- 执行逻辑涉及**长周期操作**（如调用外部 API、等待人工审核、生成万字报告），需通过 `background=true` 实现异步解耦与状态轮询；
- 应用部署在**非北京地域**（如新加坡、德国法兰克福）或归属**特定业务空间（Workspace）**，必须传入 `workspace_id`；
- 工程栈已采用 OpenAI SDK，或希望**最小化改造成本迁移至百炼**（直接复用 `openai.OpenAI` 初始化逻辑）；
- 需要**流式响应实时渲染**（如聊天界面逐字输出），且工作流应用已启用流式开关。

> ⚠️ 注意：若同时存在多模态 + 异步 + 跨地域需求，**Application Call API 是唯一可行方案**；Bailian 应用调用在此类复合场景下功能缺失。

---

## 技术选型参考（面向开发者）

| 选型决策点 | 推荐方案 | 理由说明 |
|------------|----------|----------|
| **是否需要图像/文件输入？** | Application Call API | Bailian 应用调用完全不支持[多模态输入](../concepts/multimodal-input.md)字段，硬编码将导致 400 错误 |
| **是否需异步执行与任务状态管理？** | Application Call API | Bailian 仅提供同步阻塞式调用，无法应对 >30s 耗时任务，易触发客户端超时 |
| **应用是否部署在北京以外地域？** | Application Call API（必须传 `workspace_id`） | Bailian 应用调用未暴露 `workspace_id` 参数，非北京地域调用将返回 `RegionNotSupported` |
| **是否已使用 OpenAI SDK？** | Application Call API（OpenAI 兼容模式） | 仅需替换 `base_url` 和 `api_key`，无需重写调用逻辑，迁移成本趋近于零 |
| **是否仅需轻量级智能体调用且全栈在 DashScope 生态？** | Bailian 应用调用 | SDK 封装更简洁（`Application.call(...)`），参数语义清晰，适合快速原型验证 |
| **是否依赖 `session_id` 自动上下文恢复？** | Bailian 应用调用（或 Application Call API 的 DashScope 端点） | Responses API 不支持 `session_id`，必须手动维护 `messages` 数组，增加客户端状态管理负担 |

**最终建议**：  
- 新项目开发，请**优先评估 Application Call API** —— 其扩展性、兼容性与多模态支持代表百炼平台未来演进方向；  
- 存量 Bailian 应用调用项目，若无上述高级需求，可维持现状，但建议规划向 Application Call API 迁移路径（尤其当需接入多模态或跨地域能力时）；  
- 所有方案均需严格遵循**API Key 安全规范**（环境变量注入）、**错误码处理**（`request_id` 日志追踪）及 **SDK 版本要求**（Python ≥ 1.14.0，Java ≥ 2.12.0）。

## 被对比主题页

- [bailian application calling](../guides/bailian-application-calling.md)
- [application call](../api/application-call.md)



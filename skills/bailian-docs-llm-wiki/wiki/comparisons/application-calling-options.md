# 应用调用方式对比：Application Call vs Bailian Application Calling

本文旨在帮助开发者清晰区分百炼平台中两种主流应用调用机制——`Application Call`（官方 API 规范命名）与 `Bailian Application Calling`（用户侧集成指南命名）——的技术定位、能力边界与适用场景。二者并非互斥方案，而是**同一底层能力在不同抽象层级与文档语境下的表述**：前者是面向 API 设计者与高级集成者的**协议级技术规范**，强调协议兼容性、参数语义与跨地域严谨性；后者是面向业务系统开发者的**集成实践指南**，侧重易用性、SDK 封装与典型用例。正确理解其异同，可避免重复开发、误配参数或地域调用失败等问题，提升集成效率与系统健壮性。

---

## 关键维度对比

| 维度 | `Application Call` | `Bailian Application Calling` |
|------|---------------------|--------------------------------|
| **本质定位** | 百炼平台**标准 API 协议规范**，定义统一的请求结构、认证机制与行为契约，是 SDK 和 HTTP 调用的底层依据。 | 基于 `Application Call` 协议的**用户集成实践指南**，聚焦“如何快速、安全、可靠地将应用接入业务系统”，含 SDK 示例、错误处理建议与最佳实践。 |
| **输入格式** | • 支持双模式：<br>  - 字符串 `input: "text"`（单轮）<br>  - 结构化 `input: { messages: [...] }`（多轮/[多模态](../concepts/multi-modal.md)）<br>• 明确支持 `input_image`、`input_file` 等[多模态](../concepts/multi-modal.md)字段（仅智能体应用）<br>• `biz_params` 为扁平对象，直接透传至应用逻辑层 | • 主推 `prompt: "text"`（字符串）作为默认入口，简洁直观<br>• 支持 `messages` 数组替代 `prompt`，格式兼容 OpenAI `messages`（`role`/`content`）<br>• [多模态](../concepts/multi-modal.md)支持未在文档中显式展开，需回溯至 `Application Call` 规范<br>• `biz_params` 限定为插件参数传递结构：`{ "user_defined_params": { "<plugin_code>": { ... } } }` |
| **输出格式** | • 统一返回 `response.output.text` / `response.output.session_id` 等标准化字段<br>• 流式响应（`stream=true`）返回 `SSE` 格式事件流（仅工作流应用启用流式开关后生效）<br>• 异步调用返回 `task_id`，需主动轮询 `responses.retrieve` | • 输出结构与 `Application Call` 一致（因 SDK 同源），但文档示例仅展示 `response.output.text`<br>• **未提及流式能力**，未提供流式调用示例或配置说明<br>• **未覆盖异步调用流程**（无任务创建、状态轮询等说明） |
| **支持模型/应用类型** | • 全面覆盖：<br>  - 新版智能体（Agent 2.0）<br>  - 旧版智能体<br>  - 工作流应用（Workflow）<br>• 明确区分各类型在流式、多模态、参数传递上的能力差异 | • 明确区分两类应用：<br>  - 智能体应用（Single Agent）：轻量任务导向<br>  - 工作流应用（Workflow）：复杂编排逻辑<br>• **未提及旧版智能体支持**，隐含面向新版架构 |
| **API 端点** | • 提供两套明确 endpoint：<br>  - DashScope 原生：`POST /api/v1/apps/{APP_ID}/completion`<br>  - OpenAI 兼容（Responses API）：`POST /api/v2/apps/agent/{APP_ID}/compatible-mode/v1/responses`<br>• 强调 endpoint 需匹配地域（如 `https://dashscope.aliyuncs.com` 在不同地域路由不同后端） | • 仅列出 DashScope 原生 endpoint：<br>  `POST /api/v1/apps/{APP_ID}/completion`<br>• **未提及 OpenAI 兼容模式 endpoint**<br>• 地域提示模糊：“工作流应用要求华北2（北京）”，但未说明 endpoint 是否需显式替换 |
| **会话管理** | • `session_id`：DashScope 协议核心，服务端自动维护上下文（1 小时有效期）<br>• Responses API：**不支持自动上下文续写**，必须显式传入完整 `messages` 数组 | • `session_id`：作为可选参数，强调“云端维护但有上限（50轮/1小时）”<br>• `messages`：作为 `prompt` 的替代，**推荐自行管理以保障可控性**，格式兼容 OpenAI |
| **计费方式** | • 与调用行为强绑定：<br>  - 同步调用：按 token 或请求次数计费（取决于应用配置）<br>  - 异步调用：按任务执行时长/资源消耗计费<br>• 文档未详述计费规则，但 API 行为直接影响账单 | • **未涉及任何计费说明**，完全聚焦调用流程本身 |
| **典型场景** | • 需要细粒度控制的场景：<br>  - 实时多模态交互（图文混合问答）<br>  - 长耗时任务解耦（异步生成报告+轮询）<br>  - 复用 OpenAI 生态代码（通过 Responses API）<br>  - 跨地域多 Workspace 协同（需精确传 `workspace_id`） | • 快速集成场景：<br>  - Web/App 前端调用轻量智能体（如客服助手）<br>  - 后端服务同步调用工作流完成审批链路<br>  - 需向特定插件透传业务参数（如 `article_index`） |

---

## 适用场景建议

| 场景描述 | 推荐方案 | 理由说明 |
|----------|----------|----------|
| **构建实时多模态对话产品**（如带图片上传的智能客服） | ✅ `Application Call` | 唯一明确支持 `input_image`/`input_file` 字段的规范；`session_id` 会话管理更符合对话连续性需求；DashScope SDK 封装对多模态输入支持最完善。 |
| **复用现有 OpenAI 兼容代码库**（如已用 `openai-python` 开发的 SaaS 插件） | ✅ `Application Call`（OpenAI 兼容模式） | 提供标准 `/v1/responses` endpoint 和 `background=true` 异步能力，最小化代码改造成本；文档明确兼容性边界与限制。 |
| **企业内部系统快速接入智能体**（如 OA 中嵌入政策问答机器人） | ✅ `Bailian Application Calling` | 文档步骤极简（3 步准备 + 1 行 SDK 调用），`prompt` 参数直觉性强；插件参数透传示例清晰，适合业务开发人员快速上手。 |
| **调度复杂工作流并监控执行状态**（如自动生成合规报告+邮件分发） | ✅ `Application Call`（异步模式） | 唯一提供完整异步生命周期管理（`create` → `retrieve` → 状态判断）的规范；支持 `biz_params` 传递全局上下文，满足多节点协同需求。 |
| **跨地域部署且应用位于子业务空间**（如新加坡团队调用德国 Workspace 的应用） | ✅ `Application Call` | 明确要求并解释 `workspace_id` 的必要性与地域关联规则；endpoint 地域适配说明完备，避免“仅北京可用”的误解。 |

---

## 技术选型参考（致开发者）

- **不要将二者视为“二选一”**：`Bailian Application Calling` 是 `Application Call` 协议在用户侧的友好封装。生产环境应以 `Application Call` 规范为权威依据，以 `Bailian Application Calling` 指南为快速入门路径。
  
- **优先使用 DashScope SDK（Python/Java）**：无论选择哪种文档路径，均推荐通过官方 SDK 调用。SDK 已内置：
  - 自动 endpoint 地域适配（基于 `app_id` 或显式配置）
  - `workspace_id` 安全注入
  - `session_id` 生命周期管理
  - 错误码统一解析与重试策略
  > ✳️ 注意：确保 SDK 版本 ≥ Python 1.14.0 / Java 2.12.0，否则 `biz_params` 可能被忽略。

- **关键决策检查清单**：
  - □ 是否需要**多模态输入**？→ 必须用 `Application Call` 规范，检查 `input` 结构。
  - □ 是否需**异步执行+状态追踪**？→ 必须用 `Application Call` 的 Responses API 异步模式。
  - □ 是否在**非北京地域调用工作流**？→ 必须用 `Application Call` 规范，确认 endpoint 与 `workspace_id` 匹配。
  - □ 是否只需**单轮文本问答+插件参数透传**？→ `Bailian Application Calling` 指南足够，代码最简。
  - □ 是否已用 **OpenAI SDK**？→ 直接切换至 `Application Call` 的 OpenAI 兼容 endpoint，零逻辑修改。

- **避坑提醒**：
  - `stream=true` 与 `background=true` **不可共存**，SDK 会报错；
  - `session_id` 在 `Application Call`（DashScope 模式）中有效，在 `Responses API` 中**无效**；
  - `biz_params` 在 `Bailian Application Calling` 中特指插件参数，在 `Application Call` 中可泛用于应用内任意自定义逻辑；
  - 所有调用必须校验 `response.status_code == 200`，非 200 响应体中含 `request_id`，务必记录用于问题排查。

---  
*最后更新：2024年6月*  
*本文档基于百炼平台 v2.3.0 API 规范与用户指南撰写，具体行为请以最新控制台与 SDK 文档为准。*

## 被对比主题页

- [application call](../api/application-call.md)
- [bailian application calling](../guides/bailian-application-calling.md)



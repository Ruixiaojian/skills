# 应用调用方式对比：Application Call、Managed Agents 与 Bailian Application Calling

为帮助开发者在百炼平台中高效选型，本文系统对比三种主流应用调用机制：**Application Call**（原生应用调用）、**Managed Agents API**（托管智能体运行时）与 **Bailian Application Calling**（百炼统一应用调用）。三者虽均用于集成 AI 应用能力，但在架构定位、控制粒度、适用场景及运维复杂度上存在本质差异。本对比聚焦实际开发视角，涵盖接入成本、功能边界、地域约束、[多模态](../concepts/multi-modal.md)支持等关键维度，旨在为技术决策提供清晰、可落地的参考依据。

## 关键维度对比表

| 维度 | Application Call | Managed Agents API | Bailian Application Calling |
|------|------------------|---------------------|------------------------------|
| **定位与角色** | 百炼平台核心应用调用能力，面向已发布（上线）的智能体/工作流应用，强调“即调即用”与业务集成 | 平台级智能体托管运行时服务，面向需深度定制执行生命周期、工具沙箱与事件流的复杂智能体开发场景 | 百炼官方推荐的标准化应用调用方式（SDK 封装层），本质是 Application Call 的易用封装，面向快速集成与统一治理 |
| **输入格式** | 支持 `input.prompt`（字符串）或 `input.messages`（OpenAI 风格数组）；支持[多模态](../concepts/multi-modal.md)输入（图像需 VL 模型+显式配置，文件需启用全文引用） | 严格基于 `events` 消息流：`input` 为消息数组，每条含 `role`（user/assistant/tool）、`type`（message/tool_result）、`content`（支持文本、图像、音频等富媒体） | 同 Application Call：支持 `prompt`（单轮）或 `messages`（多轮）；**不原生支持图像/文件输入**（需通过 `biz_params` 间接透传或依赖应用内预处理） |
| **输出格式** | 同步返回结构化 JSON（含 `output.text` / `output.choices[0].message.content`）；支持 `stream=true` 流式响应（SSE）；异步返回 `task_id` | 基于 SSE 的事件流（`text/event-stream`）：包含 `session_status`（idle/running/terminated）、`content`（模型输出）、`tool_calls`（[工具调用](../concepts/tool-use.md)指令）、`tool_results`（工具回填结果）等细粒度事件 | SDK 返回 `Response` 对象（含 `output.text` / `output.choices[0].message.content`）；HTTP 接口同 Application Call；**不支持[流式输出](../concepts/streaming-output.md)**（SDK 层未暴露 stream 参数） |
| **支持模型** | 由应用发布时绑定的模型决定（如 `qwen-max`, `qwen-plus`, `qwen-vl` 等），调用方无需指定 | **仅支持百炼托管模型**（如 `qwen-plus`），不支持自定义模型或外部模型接入 | 同 Application Call：由应用绑定模型自动执行，响应中 `usage.models[].model_id` 可查实际模型 |
| **API 端点** | DashScope 原生：`POST https://dashscope.aliyuncs.com/api/v1/apps/{APP_ID}/completion`<br>OpenAI 兼容：`POST https://dashscope.aliyuncs.com/api/v2/apps/agent/{APP_ID}/compatible-mode/v1/responses` | `POST https://{workspace_id}.{region}.maas.aliyuncs.com/api/v1/agentstudio/sessions/{session_id}/events`（事件提交）<br>`GET https://{workspace_id}.{region}.maas.aliyuncs.com/api/v1/agentstudio/sessions/{session_id}/events/stream`（SSE 流） | **统一端点**：`POST https://dashscope.aliyuncs.com/api/v1/apps/{APP_ID}/completion`（SDK 内部封装，对外透明） |
| **计费方式** | 按调用次数 + 模型 token 消耗计费（含输入/输出 token）；异步任务按完成计费 | 按 Session 运行时长（秒） + [工具调用](../concepts/tool-use.md)次数 + 模型 token 消耗计费；Environment 和 Skill 存储单独计费 | 同 Application Call：按调用次数 + token 消耗计费；无额外运行时费用 |
| **会话管理** | ✅ DashScope API：`session_id` 自动维护上下文（有效期 1 小时）<br>✅ Responses API：显式传递完整 `messages` 数组 | ✅ Session 级状态机管理（`idle`→`running`→`idle/terminated`）；`session_id` 为必需标识；支持中断、重试、状态查询 | ✅ 支持 `session_id`（云端会话）或 `messages`（本地会话）；**二者共存时以 `messages` 为准**（覆盖云端历史） |
| **[多模态](../concepts/multi-modal.md)支持** | ✅ 图像：需 VL 模型 + 应用配置 `imageList` 或自定义处理<br>✅ 文件：仅智能体应用支持，需启用“全文引用”或“切片检索” | ✅ 全面支持：图像/音频/文本混合输入，通过 `content` 字段以 `{"type": "image_url", "image_url": {"url": "..."} }` 等标准格式传递 | ❌ **不直接支持**：无原生图像/文件字段；需将文件 ID 或 URL 作为 `biz_params` 透传，由应用内逻辑解析处理 |
| **异步执行** | ✅ 支持：`background=true` 返回 `task_id`，需轮询 `GET /tasks/{task_id}` 获取结果 | ✅ 支持：Session 生命周期天然异步；通过 SSE 监听 `session_status` 变更即可获知完成 | ❌ **不支持**：SDK `Application.call()` 为同步阻塞调用；无异步接口封装 |
| **典型场景** | • 快速集成已发布的工作流（如审批流、报告生成）<br>• 需要流式响应的对话类应用（客服、教育）<br>• 多模态输入（图文问答、文档理解） | • 构建具备复杂工具链（代码执行、数据库查询、API 调用）的自主智能体<br>• 需精细控制执行过程（中断、调试、事件审计）<br>• 多租户沙箱隔离要求高的企业级应用 | • 传统业务系统（ERP/CRM）轻量级 AI 增强（如智能搜索、摘要生成）<br>• 团队统一使用 SDK 开发，追求最小学习成本与最大兼容性<br>• 无需流式、无需多模态、无需深度定制的标准化调用 |

## 各方案适用场景建议

- **选择 Application Call 当：**  
  您已构建并发布了成熟的智能体或工作流应用，且需要：
  - **最高灵活性**：自由选择 DashScope 原生 API 或 OpenAI 兼容 API；
  - **关键性能需求**：必须支持流式响应（如实时对话）或异步长任务（如小时级报告生成）；
  - **多模态能力**：需直接传入图像或文件进行分析；
  - **跨地域部署**：应用部署在法兰克福、新加坡等非北京地域，需显式构造带 Workspace ID 的 endpoint。

- **选择 Managed Agents API 当：**  
  您正在从零构建或深度定制一个具备**自主推理与[工具调用](../concepts/tool-use.md)能力**的智能体，且需要：
  - **执行过程完全可控**：需监听每一步工具调用、接收中间结果、支持手动中断；
  - **安全沙箱环境**：代码执行、文件读写等操作需在隔离环境中运行；
  - **版本与环境快照管理**：要求 Agent、Environment、Skill 版本精确锁定，保障生产一致性；
  - **事件驱动架构**：系统已基于事件总线设计，需与 SSE 流无缝集成。

- **选择 Bailian Application Calling 当：**  
  您追求**开箱即用、低维护成本**的集成体验，且满足：
  - **标准化调用即可**：业务逻辑简单，无需流式、异步或多模态；
  - **团队技术栈统一**：已广泛采用 DashScope SDK，希望复用现有工程实践；
  - **快速上线优先**：避免处理 `session_id` 管理、endpoint 构造、Workspace ID 适配等细节；
  - **工作流应用为主**：主要调用预编排的工作流（如审批、数据清洗），对底层执行细节无定制需求。

## 技术选型参考指南（面向开发者）

| 选型考量点 | 推荐方案 | 说明 |
|------------|----------|------|
| **首次集成，求稳求快** | ✅ Bailian Application Calling | SDK 封装完善，文档示例丰富，错误处理友好，适合 PoC 和中小项目快速验证。 |
| **已有成熟工作流，需流式/异步** | ✅ Application Call（DashScope 原生） | Bailian SDK 不支持流式与异步，必须降级使用原生 API 才能解锁核心能力。 |
| **构建“Agent as a Service”平台** | ✅ Managed Agents API | 提供 Session、Environment、Skill 等完备资源模型，是构建多租户智能体平台的唯一官方路径。 |
| **应用部署在新加坡/法兰克福** | ⚠️ Application Call（需手动拼接 Workspace ID）<br>❌ Bailian Application Calling（文档未明确支持）<br>❌ Managed Agents API（仅限北京） | 地域限制是硬约束，务必提前验证 endpoint 构造与凭证有效性。 |
| **需调用自定义模型（非百炼托管）** | ✅ Application Call | Managed Agents API 仅支持百炼托管模型；Bailian Calling 依赖应用绑定模型，无法绕过。 |
| **安全合规要求极高（如金融）** | ✅ Managed Agents API | 提供独立沙箱环境、技能安全扫描、执行过程全事件审计，满足强监管场景。 |
| **团队无后端开发资源，仅前端调用** | ✅ Bailian Application Calling 或 Application Call（Responses API） | OpenAI 兼容 API 与 SDK 最易对接，减少后端适配工作。 |

> **重要提醒**：三者并非互斥关系，而是**分层演进**关系——Bailian Application Calling 是 Application Call 的易用封装；Managed Agents API 则是更底层、更强大的运行时基础设施。建议从 Bailian Calling 入门，当业务复杂度上升（如需工具调用、沙箱隔离、事件追踪）时，再平滑迁移至 Managed Agents API；而 Application Call 始终是底层能力基石，所有高级封装均构建其上。

## 被对比主题页

- [application call](../api/application-call.md)
- [managed agents api](../api/managed-agents-api.md)
- [bailian application calling](../guides/bailian-application-calling.md)



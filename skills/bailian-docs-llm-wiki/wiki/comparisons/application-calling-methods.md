# 应用调用方式对比：Bailian 应用调用、Application Call 与 Managed Agents

为帮助开发者在百炼平台中高效选型，本文系统对比三种主流应用调用机制：**Bailian 应用调用（即传统 Agent 1.0/工作流应用调用）**、**Application Call（统一应用调用协议，覆盖 Agent 2.0/旧版智能体/工作流）** 和 **Managed Agents API（面向细粒度可控智能体生命周期的托管运行时）**。三者定位不同：前两者聚焦「应用级封装调用」，强调开箱即用与业务集成；后者聚焦「智能体基础设施层」，强调可编程性、状态可控性与工具编排深度。本对比基于当前（2024年Q3）正式发布能力，适用于生产环境技术决策参考。

## 关键维度对比

| 维度 | Bailian 应用调用 | Application Call | Managed Agents API |
|------|------------------|-------------------|---------------------|
| **本质定位** | 百炼平台早期发布的标准化应用调用方式（Agent 1.0 & 工作流），面向已发布应用的“黑盒式”调用 | 百炼统一的应用调用抽象层，向上兼容多代应用形态（Agent 2.0 / 旧版智能体 / 工作流），提供双协议支持 | 智能体运行时托管服务，提供资源化、事件驱动、沙箱隔离的智能体执行底座，非应用调用，而是智能体“构建+运行”一体化API |
| **输入格式** | 支持 `prompt`（单轮）或 `messages` 数组（多轮）；`biz_params.user_defined_params` 透传插件参数 | `input` 字段灵活：字符串（单轮文本）、消息数组（含 `role`/`content`）、或结构化对象（如 `{ "input_text": "...", "input_image": [...] }`）；OpenAI 协议下支持 `stream`/`background` 控制流模式 | 以 **Event 驱动**：通过 `POST /sessions/{id}/events` 提交用户消息事件（`input: [{"role":"user","content":"..."}]`）；支持文件引用（`file_id`）、工具调用审批等原子事件 |
| **输出格式** | 同步 JSON 响应，含 `output.text`、`usage`、`request_id`；无原生流式支持 | **双模式**：<br>• DashScope 协议：同步 JSON（类似 Bailian）<br>• OpenAI 协议：支持 `stream=true`（SSE 流式）与 `background=true`（异步任务 ID） | **纯事件流架构**：HTTP 响应仅返回操作结果（如创建成功）；实时执行状态、模型输出、工具调用、函数回填等均通过 `GET /sessions/{id}/events/stream`（SSE）推送，含 `session_status`、`content`、`tool_call`、`function_result` 等事件类型 |
| **支持模型** | 应用发布时绑定固定模型（如 `qwen-max`、`qwen-plus`），调用时不指定；响应中 `usage.models[].model_id` 可查实际执行模型 | 同上：模型由应用配置决定，调用方不可覆盖；支持 VL 模型（需应用内配置图像处理节点）及文件处理模型（仅限智能体应用） | **显式声明模型**：创建 `Agent` 时必须指定 `model.id`（如 `"qwen-plus"`）；当前仅支持百炼托管模型，不支持自定义模型 ID 或外部模型接入 |
| **API 端点** | 统一端点：<br>`POST https://dashscope.aliyuncs.com/api/v1/apps/{app_id}/completion` | **双端点**：<br>• DashScope 协议：`POST https://dashscope.aliyuncs.com/api/v1/apps/{app_id}/completion`<br>• OpenAI 兼容协议：`POST https://dashscope.aliyuncs.com/api/v2/apps/agent/{app_id}/compatible-mode/v1/responses` | **多资源端点**（需 workspace_id + region）：<br>`https://{workspace_id}.cn-beijing.maas.aliyuncs.com/api/v1/agentstudio`<br>典型路径：`/agents`, `/environments`, `/sessions`, `/sessions/{id}/events`, `/sessions/{id}/events/stream` |
| **地域支持** | 工作流应用：仅华北2（北京）；智能体应用：无明确限制（建议与部署地域一致） | **当前仅支持华北2（北京）**；若应用部署于法兰克福/新加坡/东京等非北京地域，必须提供 `Workspace ID` 并拼入 Base URL | **严格限定 `cn-beijing`**；Endpoint 中 `region` 参数仅接受 `cn-beijing`，其他值返回 404 |
| **会话管理** | • `session_id`（客户端维护或服务端生成）<br>• 有效期 1 小时，最多 50 轮<br>• 多轮时 `messages` 优先级高于 `session_id` | • DashScope 协议：同 Bailian，依赖 `session_id`<br>• OpenAI 协议：**不支持隐式会话**，需显式传递完整 `input` 消息数组（含历史 `assistant` 回复） | **全生命周期托管**：<br>• `Session` 是独立资源，有明确状态机（`idle` → `running` → `idle`/`terminated`）<br>• 状态变更仅通过 SSE `session_status` 事件通知，HTTP 响应不保证状态实时性 |
| **多模态支持** | 仅工作流应用支持图像输入（需 VL 模型节点配置）；不支持文件输入 | • 图像输入：支持（需 VL 模型 + 应用内配置）<br>• 文件输入：**仅智能体应用支持**（需配置“全文引用”或“切片检索”） | • 图像/音频：支持（通过 `/files` 上传后，在 `input` 消息中引用 `file_id`）<br>• 文件挂载：支持将文件挂载至沙箱供工具读写（需 Environment 配置） |
| **计费方式** | 按调用次数 + 模型 token 消耗计费（`input_tokens` + `output_tokens`）；计入 DashScope 账户配额 | 同上：按实际模型 token 消耗计费（无论使用 DashScope 或 OpenAI 协议）；计入 DashScope 账户配额 | 按 **Agent 运行时长（秒） + Token 消耗 + 文件存储** 计费；沙箱执行、工具调用、事件流均产生费用；独立于 DashScope 配额体系，属 MaaS（Model-as-a-Service）计费模型 |
| **典型场景** | • 快速集成已上线的客服问答、知识库助手等标准应用<br>• 业务系统嵌入轻量 AI 能力（如订单查询助手）<br>• 对话轮次可控、无需复杂工具链的场景 | • 需要流式响应的前端交互（如聊天窗口逐字输出）<br>• 需要异步处理长耗时任务（如报告生成）<br>• 已有 OpenAI 生态代码需低成本迁移至百炼<br>• 多模态输入（图文混合）的智能体应用调用 | • 构建高可控、可审计的 AI 工作流（如金融风控决策链）<br>• 需深度定制工具调用逻辑与审批流程（如企业内部审批机器人）<br>• 要求沙箱隔离、文件挂载、多技能组合的复杂 Agent<br>• 需要事件溯源、状态可观测、故障可重放的生产级 Agent 运维 |

## 各方案适用场景建议

- **选择 Bailian 应用调用，当您：**  
  ✅ 已在百炼控制台发布成熟应用（尤其是工作流类），追求最简集成路径；  
  ✅ 业务系统对延迟敏感，且对话轮次较短（<50轮）、无需[流式输出](../concepts/streaming-output.md)；  
  ❌ 不适合需要异步执行、多模态强耦合、或需深度干预工具调用流程的场景。

- **选择 Application Call，当您：**  
  ✅ 需要兼顾开发效率与灵活性——既想快速调用新版 Agent 2.0，又希望复用 OpenAI SDK 或需要流式/异步能力；  
  ✅ 应用输入包含图像或文件，且属于智能体类型（非工作流）；  
  ✅ 项目处于快速迭代期，需平衡标准化与扩展性；  
  ❌ 不适合需要精细管理会话状态、自定义沙箱环境或构建可编程 Agent 运行时的场景。

- **选择 Managed Agents API，当您：**  
  ✅ 正在构建企业级、生产就绪的智能体系统，要求：  
  &nbsp;&nbsp;• 完整的资源生命周期管理（Agent/Environment/Session 版本化）；  
  &nbsp;&nbsp;• 事件驱动架构，支持工具调用审批、函数回填、错误重试等原子控制；  
  &nbsp;&nbsp;• 沙箱隔离执行，保障安全与稳定性；  
  &nbsp;&nbsp;• 文件挂载与多技能（Skill）组合编排；  
  ✅ 团队具备较强工程能力，愿意投入资源进行 Agent 基础设施层建设；  
  ❌ 不适合简单调用、低代码集成或对成本极度敏感的轻量级场景（其运维复杂度与计费模型显著高于前两者）。

## 技术选型参考指南（面向开发者）

| 选型考量因素 | 推荐方案 | 说明 |
|--------------|----------|------|
| **上手速度 & 集成成本** | Bailian 应用调用 ≈ Application Call（DashScope 协议） > Managed Agents API | Bailian/Application Call 均只需 `app_id` + `API Key` 即可发起调用；Managed Agents 需创建 Agent/Environment/Session 多级资源，学习曲线陡峭。 |
| **多模态支持广度** | Application Call > Managed Agents API > Bailian 应用调用 | Application Call 明确支持图文混合输入（VL 模型）及文件输入（智能体）；Managed Agents 支持文件上传与引用，但图像处理需自行集成；Bailian 工作流支持图像，但文件输入不支持。 |
| **流式与异步能力** | Application Call（OpenAI 协议） > Bailian 应用调用 ≈ Managed Agents API | OpenAI 协议原生支持 `stream` 与 `background`；Bailian 无流式；Managed Agents 通过 SSE 实现更丰富的事件流，但需自行处理连接与事件解析。 |
| **可控性与可编程性** | Managed Agents API >> Application Call > Bailian 应用调用 | Managed Agents 提供 Agent/Skill/Environment 版本控制、沙箱配置、事件监听、状态机管理；Application Call 为应用级封装，内部逻辑不可见；Bailian 最为封闭。 |
| **生产稳定性与可观测性** | Managed Agents API ≥ Application Call > Bailian 应用调用 | Managed Agents 的事件流、状态机、资源版本化设计天然适配生产监控与审计；Application Call 提供标准日志与 request_id；Bailian 日志能力相对基础。 |
| **长期演进潜力** | Managed Agents API > Application Call > Bailian 应用调用 | Managed Agents 是百炼下一代智能体基础设施，持续增强沙箱、Skill、安全能力；Application Call 作为统一入口将持续演进；Bailian 应用调用定位稳定，新增特性有限。 |

> **总结建议**：  
> - **MVP 验证 / 内部工具 / 标准应用集成 → 优先用 Bailian 应用调用**；  
> - **面向用户的产品（含 Web/APP）/ 多模态需求 / 需要流式或异步 → 选用 Application Call（推荐 OpenAI 协议）**；  
> - **构建企业级 AI 平台 / 高合规要求场景 / 需深度定制 Agent 行为 → 直接采用 Managed Agents API**。  
> 所有方案均需通过 DashScope API Key 鉴权，建议统一使用环境变量管理密钥，并遵循最小权限原则配置应用调用权限。

## 被对比主题页

- [bailian application calling](../guides/bailian-application-calling.md)
- [application call](../api/application-call.md)
- [managed agents api](../api/managed-agents-api.md)



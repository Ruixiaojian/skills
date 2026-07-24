# 应用调用方式对比：Application Call、Managed Agents 与 Bailian Application Calling

为帮助开发者在百炼平台生态中高效选型，本文系统对比三种核心应用调用机制：**Application Call**（原生应用调用）、**Managed Agents API**（托管智能体运行时）与 **Bailian Application Calling**（百炼应用集成标准方式）。三者定位不同：Application Call 是面向已发布应用的通用调用能力；Managed Agents 提供细粒度、可编程的智能体生命周期与沙箱环境管控；Bailian Application Calling 则是面向生产集成的轻量级、SDK 优先的标准化调用范式。理解其差异对架构设计、权限治理、运维可观测性及跨地域部署至关重要。

## 关键维度对比

| 维度 | Application Call | Managed Agents API | Bailian Application Calling |
|------|------------------|---------------------|------------------------------|
| **本质定位** | 百炼平台**已发布应用的统一调用入口**（Agent/Workflow 均适用），强调“调用即服务” | **智能体基础设施层 API**，提供 Agent/Environment/Session 等资源的全生命周期管理，强调“托管+可编程” | **面向业务集成的简化 SDK 封装层**，基于 Application Call 接口构建，强调“开箱即用、快速集成” |
| **输入格式** | 支持双模式：<br>• 字符串 `prompt`（单轮）<br>• 消息数组 `messages`（OpenAI 风格，含 `role`/`content`）<br>• 多模态：`input_image`/`input_file` 数组（需应用配置支持） | 严格结构化事件流：<br>• `/sessions/{id}/events` 接收 `input` 数组，每项含 `role`/`type`（`text`/`image`/`file`）/`content`<br>• 文件需预先上传并审核通过后引用 ID | 同 Application Call：<br>• `prompt`（单轮）或 `messages`（多轮）二选一<br>• `biz_params.user_defined_params` 透传插件参数<br>• **不直接支持多模态输入**（图像/文件需先通过其他接口上传） |
| **输出格式** | • 同步：JSON 响应含 `output.text`、`usage`、`session_id`、`debug_info`（启用时）<br>• 异步：返回 `task_id`，需轮询 `/tasks/{id}`<br>• 流式：SSE 或 chunked JSON（仅同步且工作流启用流式开关） | • 事件驱动响应：<br>  - `/events` 返回执行状态（`session_status`、`event_type`）<br>  - `/events/stream` SSE 流式推送中间结果、工具调用、状态变更<br>• 输出结构深度嵌套，含 `execution_trace`、`sandbox_logs` 等调试字段 | • 标准 JSON 响应，结构与 Application Call 同源：<br>  `output.text`、`usage.models[].model_id`、`session_id`、`debug_info`（启用 `debug: {}`）<br>• **无原生异步或流式支持**（依赖上层封装） |
| **支持模型** | **不限定模型**：由应用在控制台配置决定（如 `qwen-max`、`qwen-vl`、`qwen-audio`），调用方无需感知 | **限定托管模型**：当前仅支持 `qwen-plus` 等百炼平台预置托管大模型（`model.id` 必须显式指定且在白名单内） | **不限定模型**：同 Application Call，由应用配置决定；响应中 `usage.models[].model_id` 可回溯实际模型 |
| **API 端点** | • DashScope 原生：`POST https://dashscope.aliyuncs.com/api/v1/apps/{APP_ID}/completion`<br>• OpenAI 兼容：`POST https://dashscope.aliyuncs.com/api/v2/apps/agent/{APP_ID}/compatible-mode/v1/responses` | • 统一 Base URL：`https://{workspace_id}.{region}.maas.aliyuncs.com/api/v1/agentstudio`<br>• 资源路径：`/agents`、`/environments`、`/sessions/{id}/events` 等 | • **与 Application Call 原生端点完全一致**：<br>`POST https://dashscope.aliyuncs.com/api/v1/apps/{app_id}/completion`<br>• SDK 封装隐藏了底层细节 |
| **认证方式** | Header `Authorization: Bearer {DASHSCOPE_API_KEY}` | Header `Authorization: Bearer {DASHSCOPE_API_KEY}` + Workspace ID 和 Region 内置于 Base URL | Header `Authorization: Bearer {DASHSCOPE_API_KEY}`（SDK 自动注入） |
| **计费方式** | 按**实际调用的模型 [Token](../concepts/token.md) 用量**计费（含输入/输出），与应用类型无关；[异步任务](../concepts/asynchronous-task.md)按完成计费 | 按**托管资源使用时长 + 模型 [Token](../concepts/token.md) 用量**双重计费：<br>• Session 运行时长（秒）<br>• 模型推理 [Token](../concepts/token.md)（输入/输出）<br>• 文件存储（30 天）、沙箱计算资源等附加费用 | **与 Application Call 完全一致**：按模型 Token 用量计费；SDK 封装不产生额外费用 |
| **会话管理** | • `session_id`（云端托管，1 小时/50 轮）<br>• 或显式传入完整 `messages` 数组（推荐生产环境） | • Session 为独立资源，创建时绑定 Agent 快照与 Environment<br>• 会话状态机驱动（`idle`→`running`→`terminated`）<br>• **会话快照固化，不受 Agent 更新影响** | • 同 Application Call：支持 `session_id` 或 `messages`<br>• 文档明确建议生产环境**优先使用 `messages` 自主管理上下文**，规避会话过期风险 |
| **多模态支持** | ✅ 官方支持：<br>• 图像：`input_image` 数组 + VL 模型配置<br>• 文件：智能体应用支持「全文引用」/「切片检索」 | ✅ 官方支持：<br>• 图像/音频：作为 `type: "image"`/`"audio"` 的消息内容<br>• 文件：需先调用 `/files` 上传并等待 `status: available` | ❌ **不直接支持**：<br>• 无 `input_image`/`input_file` 字段<br>• 多模态需先通过其他 API（如 Managed Agents 的 `/files` 或独立文件服务）上传，再以文本描述或 ID 形式在 `prompt`/`messages` 中引用（非原生能力） |
| **调试与可观测性** | • `debug: {}` 返回节点执行路径、插件日志<br>• [异步任务](../concepts/asynchronous-task.md)可通过 `task_id` 查询完整 trace | • 深度可观测：<br>  - `execution_trace` 展示完整决策链<br>  - `sandbox_logs` 输出沙箱内工具执行日志<br>  - SSE 实时推送各阶段事件 | • 同 Application Call：`debug: {}` 启用基础调试信息<br>• **无沙箱日志、无执行链路追踪**（能力弱于前两者） |
| **地域与 Workspace 依赖** | • 跨地域调用需显式传 `workspace_id`（德/京/新/东京必填）<br>• `workspace_id` 可作 Base URL 组成部分或请求参数 | • **强绑定**：Base URL 必须包含 `workspace_id` 和 `region`（当前仅 `cn-beijing`）<br>• 所有资源操作均作用于指定 Workspace | • 文档未明确定义，但实践表明：<br>  - 工作流应用**强制要求华北2（北京）**<br>  - 智能体应用建议部署在北京以确保兼容性<br>  - `workspace_id` 非必需（由 APP_ID 隐式关联） |

## 各方案适用场景建议

| 方案 | 推荐场景 | 不适用场景 |
|------|----------|------------|
| **Application Call** | • **需要最大灵活性的生产集成**：要求同时支持智能体与工作流、多模态输入、[异步任务](../concepts/asynchronous-task.md)、流式响应、精细调试（`debug`）<br>• **混合部署架构**：应用分散在多个地域（如北京+新加坡），需统一 API 调用逻辑<br>• **高性能/低延迟场景**：直接使用 DashScope 原生 API，绕过 SDK 开销 | • 团队缺乏 API 工程能力，需零配置快速上线<br>• 需要深度定制智能体执行环境（如自定义沙箱、特定工具链隔离）<br>• 要求对每个会话的 CPU/内存/网络策略进行精细化管控 |
| **Managed Agents API** | • **构建智能体平台或 PaaS 服务**：需对外提供 Agent 创建、版本管理、沙箱环境配置、会话生命周期控制等能力<br>• **安全敏感型场景**：依赖沙箱隔离执行第三方工具，需审计 `sandbox_logs` 和 `execution_trace`<br>• **复杂事件编排**：需实时响应工具调用结果、动态调整后续步骤（SSE 事件流驱动） | • 简单业务系统集成（如客服机器人嵌入网页）<br>• 无多租户/多环境隔离需求<br>• 对成本极度敏感，无法接受 Session 时长计费模式 |
| **Bailian Application Calling** | • **快速验证与 MVP 开发**：使用 Python/Java SDK 一行代码调用，降低接入门槛<br>• **标准化业务系统集成**：已有成熟 SDK 生态（如电商订单系统、CRM），追求最小改造成本<br>• **纯文本对话场景**：无需多模态、无需深度调试，仅需稳定获取 `output.text` | • 需要异步处理长耗时任务（如批量文档分析）<br>• 要求流式返回提升用户体验（如实时思考过程）<br>• 需要上传图像/文件并直接参与推理（如医疗影像问答） |

## 技术选型参考（面向开发者）

选择依据应围绕 **控制力、复杂度、运维成本、扩展性** 四个维度权衡：

- **选 `Application Call` 当：**  
  你已具备 API 集成经验，业务需要**最高自由度与兼容性**。它是百炼最底层、最完整的调用能力，覆盖所有应用类型与高级特性。若你的系统需对接工作流（尤其涉及异步批处理）、或多模态场景（如图文混合问答），这是**唯一官方支持的方案**。注意：需自行处理 `workspace_id` 地域适配与会话续接逻辑。

- **选 `Managed Agents API` 当：**  
  你正在构建一个**智能体操作系统**，而非简单调用某个应用。你需要像管理 Kubernetes Pod 一样管理每个 Agent 实例——定义环境、挂载技能、观察沙箱日志、响应事件。这适合技术中台团队或 AI Infra 团队，但意味着更高的开发与运维复杂度。**不要为单个业务功能引入此层级**。

- **选 `Bailian Application Calling` 当：**  
  你追求**最快落地、最低维护成本**。SDK 封装屏蔽了协议细节，`Application.call()` 方法语义清晰，错误码和日志规范统一。适用于大多数企业级业务集成（如将智能体嵌入内部 OA、HR 系统）。但请清醒认知其边界：它不是新协议，而是 Application Call 的友好包装；当业务增长到需要异步、流式或多模态时，应平滑升级至 Application Call 原生调用。

> **关键提醒**：三者并非互斥，而是分层演进关系。典型路径为：`Bailian Application Calling`（快速启动） → `Application Call`（增强能力） → `Managed Agents API`（平台化管控）。所有方案均使用同一套 `DASHSCOPE_API_KEY` 认证体系，权限可统一通过 RAM 策略管控。

## 被对比主题页

- [application call](../api/application-call.md)
- [managed agents api](../api/managed-agents-api.md)
- [bailian application calling](../guides/bailian-application-calling.md)



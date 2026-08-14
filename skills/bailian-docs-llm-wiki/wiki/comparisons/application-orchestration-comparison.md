# 应用编排能力对比：Managed Agents API vs Application Component API vs Application Call

## 对比目的与背景

在百炼平台构建企业级 AI 应用时，开发者需根据业务复杂度、控制粒度、运维成本与集成方式，选择合适的应用编排机制。当前平台提供三类核心能力路径：

- **Managed Agents API**：面向需要深度定制智能体行为、精细管控执行环境与生命周期的高阶场景，提供沙箱隔离、工具链编排、事件流驱动等底层能力；
- **Application Component API**：聚焦于**应用数据基础设施**建设，支撑知识库构建、数据连接管理、解析策略配置与 Prompt 模板化，是应用“感知”与“记忆”能力的基石；
- **Application Call**：面向已发布应用的**生产级调用**，强调开箱即用、低门槛集成与多协议兼容（DashScope / OpenAI 兼容），适用于前端接入、SaaS 集成或轻量级服务编排。

本对比旨在为开发者提供清晰的技术选型决策依据，明确各方案的能力边界、适用阶段与协作关系，避免因能力错配导致架构冗余或功能缺失。

---

## 关键维度对比表

| 维度 | Managed Agents API | Application Component API | Application Call |
|------|---------------------|----------------------------|-------------------|
| **定位与角色** | 智能体托管运行时（Runtime）——定义、部署、执行可编程 Agent | 应用数据与知识基础设施（Data & Knowledge Plane）——构建、管理、供给结构化知识与上下文 | 已发布应用的消费接口（Consumption Interface）——调用预置智能体/工作流的标准化入口 |
| **输入格式** | `POST /sessions/{id}/events` 提交结构化事件数组（含 `text`/`image`/`file` 类型消息 + 会话元信息）；支持 SSE 流式提交 | 多样化资源操作请求：<br>• 数据连接：`AddFile`（含 `LeaseId` + `Parser`）<br>• 知识库：`Retrieve`（纯文本 query）<br>• Prompt：`CreatePromptTemplate`（JSON 模板字符串） | `input` 字段支持灵活格式：<br>• 字符串（单轮文本）<br>• 消息数组（`messages: [{role, content}]`，含 `input_image`/`input_file`）<br>• `biz_params`（应用内自定义参数对象） |
| **输出格式** | SSE 流式事件（`event: session_status` / `event: tool_call` / `event: message`）+ JSON 同步响应；含完整执行轨迹、工具调用结果、状态变更通知 | RESTful JSON 响应为主：<br>• 创建类：返回 `Id`（如 `IndexId`, `FileId`）<br>• 查询类：返回结构化资源列表或详情（如 `ListIndexDocuments` 返回文档元数据）<br>• 检索类：`Retrieve` 返回 `chunks` 数组及 `score` | 同步模式：标准 Completion 响应（含 `output.text` / `output.choices[0].message.content`）<br>异步模式：返回 `task_id`，需后续 `GET /tasks/{id}` 获取结果<br>支持 `stream=true` 的逐 token 流式响应（仅同步 + 工作流启用流式开关） |
| **支持模型** | 显式指定 `model.id`（如 `qwen-plus`），模型由平台托管，Agent 创建时绑定 | **不直接调用大模型**；为模型推理提供增强输入（知识库检索结果、结构化数据），模型选择由上层应用（如 Agent 或工作流）决定 | 由被调用的**目标应用内部配置决定**（如新版智能体绑定 `qwen-max`，工作流节点指定模型）；调用方无需关心模型细节 |
| **API 端点特征** | 工作空间专属 Endpoint：<br>`https://{workspace_id}.{region}.maas.aliyuncs.com/api/v1/agentstudio`<br>强绑定 `workspace_id` + `region`（当前仅 `cn-beijing`） | ROA 风格通用 Endpoint：<br>`https://bailian.{region}.aliyuncs.com`<br>路径中嵌入 `WorkspaceId`，支持多地域（北京、新加坡、东京、法兰克福） | 双协议 Endpoint：<br>• DashScope：`https://dashscope.aliyuncs.com/api/v1/apps/{app_id}/completion`（仅北京）<br>• Responses（OpenAI 兼容）：`https://dashscope.aliyuncs.com/api/v2/apps/agent/{app_id}/compatible-mode/v1/`（仅北京）<br>跨地域调用需拼接 `workspace_id` 到 Base URL |
| **计费方式** | 按 **Agent 运行时消耗** 计费：<br>• Session 实例时长（秒）<br>• 工具调用次数<br>• 文件上传/存储（按量）<br>• 沙箱资源使用（CPU/内存） | 按 **数据操作与知识服务** 计费：<br>• 知识库构建任务（`SubmitIndexJob`）<br>• 检索调用次数（`Retrieve`）<br>• 文件解析与存储（按量）<br>• Prompt 模板调用（如有） | 按 **应用调用次数与输出 [Token](../concepts/token.md)** 计费：<br>• 同步/异步调用均计为 1 次请求<br>• 输出 [Token](../concepts/token.md) 量计入模型推理费用<br>• 不单独收取知识库或数据连接费用（已包含在应用内） |
| **典型场景** | • 构建具备复杂工具链（代码执行、数据库查询、第三方 API 调用）的自主智能体<br>• 需要严格沙箱隔离与审计日志的金融/政务场景<br>• 多 Session 并发管理与状态机驱动的对话流程 | • 构建企业级知识库（PDF/Excel/网页批量入库 + 自定义解析）<br>• 管理多源数据连接（OSS 表格、数据库快照、CRM 接口）<br>• 统一维护 Prompt 模板与变量注入规则 | • Web/App 前端集成已上线的客服智能体<br>• 与现有业务系统（ERP/CRM）通过 API 对接工作流<br>• 使用 OpenAI SDK 快速迁移已有应用到百炼平台 |

---

## 各方案适用场景建议

### ✅ 选择 **Managed Agents API** 当：
- 你需要**完全掌控智能体的行为逻辑与执行环境**，例如：  
  - 定义自定义工具（Skill）并进行安全扫描与版本管理；  
  - 要求每个用户会话运行在独立沙箱中，防止内存/文件污染；  
  - 需监听工具调用中间结果、动态调整后续步骤（如“查天气失败 → 切换备用 API”）；  
  - 开发需长期运行、状态持久化的 Agent（如自动化运维助手）。  
- **不适合**：快速验证想法、MVP 原型开发、或仅需简单问答的轻量场景（开发成本过高）。

### ✅ 选择 **Application Component API** 当：
- 你的核心需求是**构建和治理 AI 应用的数据底座**，例如：  
  - 将数百份产品手册 PDF 构建为可检索的知识库，并支持增量更新；  
  - 将 CRM 中的客户数据表接入百炼，作为智能体的实时数据源；  
  - 为不同业务线统一配置文档解析策略（如合同用 `DOCMIND_LLM_VERSION`，发票用 `AUTO_SELECT`）；  
  - 管理多套 Prompt 模板供不同应用复用（如“技术文档摘要模板”、“销售话术生成模板”）。  
- **不适合**：直接实现对话逻辑或模型推理；它不提供“运行智能体”的能力，而是为其他能力提供数据支撑。

### ✅ 选择 **Application Call** 当：
- 你已通过控制台或低代码方式**发布成熟应用**，现在需要**规模化、标准化地调用它**，例如：  
  - 在企业微信机器人中嵌入已审核上线的 HR 政策问答智能体；  
  - 将订单处理工作流接入电商后台系统，通过 `background=true` 异步触发；  
  - 使用 Python 的 `openai` SDK 快速将旧有 LLM 应用迁移到百炼（零代码改造）；  
  - 需要支持多轮对话且不希望自行维护 `session_id` 生命周期（Responses API 直接传 `messages` 数组）。  
- **不适合**：需要修改应用内部逻辑、调试工具调用过程、或对知识库内容做细粒度控制（这些需回退到 Component API 或 Managed Agents API）。

---

## 技术选型参考（面向开发者）

| 选型考量 | 推荐方案 | 说明 |
|----------|-----------|------|
| **我刚有一个想法，想快速验证是否可行** | ➤ Application Call | 使用控制台创建一个简易智能体 → 获取 `app_id` → 3 行代码调用，5 分钟完成 PoC。避免过早陷入环境配置与资源管理。 |
| **我的应用需要访问数据库、执行 Shell 命令、调用内部 API** | ➤ Managed Agents API | 只有该方案支持挂载自定义 Skill（zip 工具包）、声明沙箱类型（`cloud`/`docker`）、接收工具执行原始结果并决策下一步。 |
| **我有大量非结构化文档（PDF/PPT/Word），需让 AI “读懂”它们** | ➤ Application Component API | 通过 `CreateIndex` + `SubmitIndexJob` + `Retrieve` 构建知识增强能力；再将 `Retrieve` 结果作为 `input` 注入到 Application Call 或 Managed Agents 的提示词中。 |
| **我要把百炼智能体集成进现有 Java/Spring Boot 系统** | ➤ Application Call（Responses API） | 使用 Spring AI Alibaba Starter，配置 `spring.ai.alibaba.bailian.app-id` 即可像调用本地 AI 一样使用，自动处理鉴权、重试、超时。 |
| **我需要同时管理 50+ 个知识库、200+ 个数据连接，并实现权限分级** | ➤ Application Component API + RAM 权限策略 | 利用 `WorkspaceId` 隔离租户，结合最小权限 RAM 策略（如 `AliyunBailianDataReadOnlyAccess`）控制子账号操作范围。 |
| **我的智能体需满足等保三级要求：所有执行必须留痕、沙箱不可逃逸、文件上传需病毒扫描** | ➤ Managed Agents API | 原生支持沙箱隔离、文件安全扫描（Skill/File）、完整事件流审计（SSE）、Session 状态机追踪，符合合规基线。 |
| **我想让多个应用共享同一套知识库和 Prompt 模板** | ➤ 组合使用：Application Component API（构建） + Application Call（消费） | 在 Component API 中统一创建 Index 和 Template → 在 Application Call 的 `biz_params` 或 Prompt 中引用其 ID → 实现“一处维护，多处生效”。 |

> 💡 **关键协同原则**：  
> - **Component 是“原料”，Call 是“成品”，Managed Agents 是“中央厨房”**。  
> - 实际项目中三者常组合使用：用 Component API 构建知识库 → 用 Managed Agents API 编排带工具调用的智能体 → 将该智能体发布为 App → 用 Application Call 对外提供服务。  
> - 无银弹：不存在“最好”的 API，只有“最适合当前阶段与约束”的 API。建议从 Application Call 启动，随需求演进逐步下沉至 Component 与 Managed Agents 层。

## 被对比主题页

- [managed agents api](../api/managed-agents-api.md)
- [application component api reference](../api/application-component-api-reference.md)
- [application call](../api/application-call.md)



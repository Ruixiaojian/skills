# 应用编排方案对比：Managed Agents、Application Call 与 Application Component API

> **目的与背景**  
> 在百炼平台构建智能应用时，开发者需根据业务复杂度、控制粒度、运维成本与集成方式，选择合适的应用编排方案。`Managed Agents` 面向高自主性智能体运行时；`Application Call` 聚焦于已发布应用的即用型调用；`Application Component API` 则提供底层能力组件（数据、知识库、Prompt）的精细化编排。本文旨在从技术视角系统对比三者的核心差异，帮助开发者在架构设计初期做出合理选型决策，避免因方案错配导致开发返工、运维负担加重或能力边界受限。

---

## 关键维度对比表

| 维度 | Managed Agents API | Application Call | Application Component API |
|------|---------------------|------------------|----------------------------|
| **定位与角色** | 智能体托管运行时（Runtime-as-a-Service）：平台统一管理会话、沙箱、工具执行与事件流 | 应用级服务网关（Gateway）：调用已发布、已配置的智能体/工作流应用，屏蔽底层实现细节 | 基础能力组件层（Component Layer）：提供[数据连接](../concepts/data-connection.md)、知识库（RAG）、Prompt 工程等可组合原子能力 |
| **输入格式** | JSON 结构化事件（如 `{"type": "user_message", "content": "..."}`），支持多轮状态感知；需显式绑定 `agent_id` + `environment_id` | 简洁输入对象：`input` 字段支持字符串（单轮文本）或消息数组（多模态、多轮对话）；`biz_params` 支持自定义参数透传 | 多样化资源操作请求：按能力域分组（如 `AddFile`, `CreateIndex`, `CreatePromptTemplate`），各接口有独立入参结构，需严格遵循 ROA 规范 |
| **输出格式** | SSE 流式事件流（`session_status`, `tool_call`, `message` 等类型事件）+ 同步状态查询；输出含完整会话上下文快照与中间执行痕迹 | 同步：结构化 `output.text` / `output.choices`；异步：返回 `task_id`；流式：SSE 或 chunked JSON；输出为最终语义结果，不暴露推理过程 | 标准化 OpenAPI 响应：成功返回 `200` + 资源 ID（如 `file_id`, `index_id`）；失败返回标准错误码（如 `InvalidParameter`, `ResourceNotFound`）；无语义内容生成 |
| **支持模型** | 仅限百炼托管模型（如 `qwen-plus`），且必须通过 `{"id": "qwen-plus"}` 对象格式指定；**不支持自定义模型或外部模型接入** | 支持所有已在百炼平台发布并配置的模型（含 Qwen 系列、Qwen-VL、Qwen-Audio 等），由应用发布时绑定；**支持多模态模型与自定义工作流引擎** | **不直接调用大模型**；作为 RAG、数据预处理、Prompt 注入等前置环节，为上层模型调用提供增强输入 |
| **API 端点特征** | RESTful + SSE 流式端点混合：<br>- `/agents`, `/environments`, `/sessions`（资源管理）<br>- `/sessions/{id}/events`（事件触发）<br>- `/sessions/{id}/events/stream`（SSE 订阅） | 协议双轨制：<br>- DashScope 原生：`POST /api/v1/apps/{app_id}/completion`<br>- OpenAI 兼容：`POST /v2/apps/agent/{app_id}/compatible-mode/v1/responses`<br>均以 `app_id` 为核心路由标识 | ROA 风格 OpenAPI：<br>- [数据连接](../concepts/data-connection.md)：`POST /bailian/2023-12-29/categories`<br>- 知识库：`POST /bailian/2023-12-29/indices`<br>- Prompt：`POST /bailian/2023-12-29/prompt-templates`<br>所有接口需签名，路径含 `WorkspaceId` |
| **计费方式** | 按 **Session 运行时长 + 工具调用次数 + 文件存储量** 计费；沙箱环境、事件流、版本管理均计入资源消耗 | 按 **调用次数 + 输出 [Token](../concepts/token.md) 数量** 计费（同步/流式）；异步模式按 **任务执行时长 + 输出 [Token](../concepts/token.md)** 计费；APP 发布本身不产生费用 | 按 **API 调用次数 + 存储容量（文件/知识库） + 构建任务耗时** 计费；知识库切片、Prompt 模板等均为独立计费项；**无模型推理费用** |
| **典型场景** | - 需多步工具协同（如查天气→订机票→发邮件）<br>- 要求沙箱隔离与状态持久化（如代码执行、数据库操作）<br>- 开发者需深度介入推理链路与事件响应逻辑 | - 快速集成已上线客服机器人、营销文案生成器等标准化应用<br>- 需兼容 OpenAI 生态（如迁移现有 LangChain 应用）<br>- 实时对话（同步）、长周期规划（异步）、渐进式反馈（流式） | - 构建企业专属知识库（上传 PDF/Excel → 切片 → 构建索引）<br>- 管理多源异构数据（OSS 表格导入、数据库连接器配置）<br>- 动态注入业务规则到 Prompt（如根据用户等级切换模板） |

---

## 各方案适用场景建议

### ✅ 推荐使用 **Managed Agents API** 当：
- 你需要构建具备**复杂决策逻辑与外部系统交互能力**的智能体（例如：自动化 IT 运维助手、跨系统数据核验 Agent）；
- 要求**强沙箱隔离**（如执行 Python 代码、访问内部 API）且需平台保障安全扫描与资源回收；
- 开发团队具备全栈能力，愿意承担 Agent 版本管理、Session 生命周期监控、事件流解析等运维职责；
- 场景对**中间步骤可观测性**有硬性要求（如审计工具调用记录、回溯某次失败原因）。

### ✅ 推荐使用 **Application Call** 当：
- 你已通过百炼控制台完成应用开发与发布（如训练好一个合同审核 Agent），只需在业务系统中**快速调用其能力**；
- 希望最小化集成成本，尤其已有 OpenAI 客户端代码，可通过兼容协议**零改造接入**；
- 业务对 SLA 和稳定性要求高，依赖百炼平台统一保障应用可用性、扩缩容与故障自愈；
- 场景以**结果导向为主**（如生成报告、回答问题），无需干预模型内部推理过程或工具选择逻辑。

### ✅ 推荐使用 **Application Component API** 当：
- 你需要**自主构建 RAG 流水线**（如从 ERP 导入销售数据 → 清洗 → 构建向量库 → 与 LLM 联合推理）；
- 必须将 Prompt 作为配置项动态管理（如 A/B 测试不同话术模板、按渠道切换品牌语气）；
- 数据源分散且需统一治理（如对接多个 OSS Bucket、MySQL 实例、NAS 文件系统）；
- 架构采用“能力解耦”设计，上层应用（如自研 Agent 框架）需复用百炼的**可信数据处理与知识检索能力**，而非直接调用其封装好的应用。

---

## 技术选型参考指南（面向开发者）

| 选型考量因素 | Managed Agents API | Application Call | Application Component API |
|--------------|---------------------|------------------|----------------------------|
| **开发门槛** | ⚠️ 中高：需理解会话状态机、事件类型、沙箱约束；SDK 封装较新，文档细节需仔细校验（如 model 格式） | ✅ 低：接口简洁，OpenAI 兼容降低学习成本；控制台调试功能完善，错误提示友好 | ⚠️ 中：ROA 签名、权限策略、资源依赖链需严格遵循；建议优先使用官方 SDK，避免手写签名 |
| **控制粒度** | ✅ 最细：可精确控制每一步工具调用、沙箱环境、Agent 版本、Session 超时策略 | ⚠️ 粗：仅能配置输入/输出行为（stream/background），无法干预内部工具选择或模型 [prompt](../guides/prompt.md) | ✅ 细（但非推理层）：对数据、知识、Prompt 的生命周期完全可控，但不涉及模型推理调度 |
| **扩展性** | ⚠️ 有限：仅支持百炼托管模型；技能（Skill）需 zip 打包并通过安全扫描，迭代周期较长 | ✅ 高：应用内可自由组合模型、工具、工作流节点；支持多模态输入与自定义插件 | ✅ 高：各组件可独立演进（如升级知识库切片算法、新增[数据连接](../concepts/data-connection.md)器类型），天然支持微服务化编排 |
| **运维复杂度** | ⚠️ 高：需监控 Session 状态、文件过期、Skill 审核状态、Environment 更新影响范围 | ✅ 低：百炼平台全托管；开发者仅需关注调用成功率与 [Token](../concepts/token.md) 成本 | ⚠️ 中：需自行实现幂等、重试、状态轮询（如知识库构建进度）；注意各接口 QPS 限制与资源依赖约束 |
| **组合使用建议** | ✔️ 可作为 Application Component 的下游：用 Component API 构建知识库后，在 Managed Agents 中挂载为工具；<br>✔️ 不建议与 Application Call 混用同一业务逻辑（易造成能力重叠与权限混乱） | ✔️ 是最常作为前端/业务系统入口：接收用户请求 → 调用 Application Call → 返回结果；<br>✔️ 可调用由 Managed Agents 发布的应用（需先发布为 App） | ✔️ 是其他两者的基础设施：为 Application Call 提供知识增强，为 Managed Agents 提供数据支撑与 Prompt 注入能力；<br>❌ 不可单独用于生成最终用户响应（无模型调用能力） |

> **一句话总结选型原则**：  
> - 要 **“造轮子”**（定制智能体运行时）→ 选 **Managed Agents**；  
> - 要 **“用轮子”**（调用现成智能应用）→ 选 **Application Call**；  
> - 要 **“造零件”**（构建数据、知识、Prompt 底座）→ 选 **Application Component API**。  
> 实际项目中，三者常分层协作：Component 构建能力底座 → Managed Agents 编排复杂智能体 → Application Call 对外提供统一 API 入口。

## 被对比主题页

- [managed agents api](../api/managed-agents-api.md)
- [application call](../api/application-call.md)
- [application component api reference](../api/application-component-api-reference.md)



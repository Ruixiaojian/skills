# 应用开发框架对比：Managed Agents vs Application Component API

本文旨在帮助百炼平台开发者清晰理解两类核心应用开发能力的定位差异与技术边界，辅助在实际项目中做出合理的技术选型。Managed Agents API 面向**端到端智能体（Agent）生命周期编排与运行时交互**，强调会话状态管理、工具协同与事件流驱动；而 Application Component API 则聚焦于**应用基础设施层的能力供给**，提供数据连接、知识库构建与 [Prompt 工程](../concepts/prompt-engineering.md)等可复用、可组合的基础组件服务。二者并非替代关系，而是分层协作：Application Component 为 Managed Agents 提供底层数据与知识支撑，Managed Agents 在其之上构建具备感知-决策-执行闭环的智能应用。

以下从关键工程维度进行结构化对比：

| 维度 | Managed Agents API | Application Component API |
|------|---------------------|----------------------------|
| **核心定位** | 智能体托管运行时：封装模型、提示词、工具、沙箱与会话状态，提供事件驱动的 Agent 执行环境 | 应用基础能力组件：提供数据接入、知识库索引、Prompt 模板等原子化、可复用的服务能力 |
| **输入格式** | `POST /sessions/{id}/events` 接收结构化事件（如 `{"type": "user_message", "input": [...]}`），支持[多模态](../concepts/multi-modal.md)内容（需预上传 File） | 各接口独立定义：文件上传需先申请租约（`ApplyFileUploadLease`）再提交；知识库构建需分步调用 `CreateIndex` + `SubmitIndexJob`；Prompt 操作为标准 CRUD JSON 请求 |
| **输出格式** | SSE 流式响应（`text/event-stream`），含 `session_status`、`tool_call`、`tool_result`、`message` 等事件类型；最终结果通过 `idle` 事件聚合返回 | 同步 HTTP 响应（JSON），含 `RequestId`、业务字段（如 `FileId`、`IndexId`、`PromptTemplateId`）及分页元信息（`NextToken`）；检索类接口（`Retrieve`）直接返回结构化结果列表 |
| **支持模型** | 仅限百炼平台已发布的推理模型（如 `qwen-plus`），通过 `model.id` 显式指定；模型能力由 Agent 快照固化 | **不直接调用大模型**；所有能力均不涉及模型推理调用，仅为数据/知识/Prompt 的管理与调度服务 |
| **API 端点风格** | REST + SSE 流式端点，路径强绑定工作空间与地域（如 `/workspaces/{workspace_id}/regions/{region}/agents`）；需显式传入 `workspace_id` 和 `region`（当前仅 `cn-beijing`） | ROA 风格 OpenAPI，路径含版本号（`/api/v20231229/...`），接入点按地域区分（如 `bailian.cn-beijing.aliyuncs.com`）；`WorkspaceId` 作为通用 Query 或 Body 参数 |
| **鉴权方式** | Bearer [Token](../concepts/token.md)（API Key），通过 `Authorization: Bearer <key>` Header 传递 | ROA 签名机制（Signature），需计算 `Authorization` Header（含 `AccessKeyId`、`Signature`、`Date` 等），推荐使用 SDK 自动处理 |
| **计费方式** | 按 **Agent 会话时长**（秒） + **工具调用次数** + **沙箱资源消耗**（CPU/内存/时长）计费；文件上传、Skill 审核等操作不单独计费 | 按 **调用次数**（如 `AddFile`、`SubmitIndexJob`） + **存储容量**（知识库索引、文件存储） + **检索 QPS** 计费；无会话或运行时费用 |
| **典型场景** | • 多轮对话客服机器人（需维护上下文与状态）<br>• 自动化任务助手（如“分析附件并生成报告”，需调用工具链）<br>• 实时交互式数据分析看板（结合沙箱执行代码） | • 构建企业专属知识库（上传 PDF/Excel → 解析 → 索引 → 检索）<br>• 管理应用级非结构化数据资产（分类、打标、批量导入 OSS）<br>• 统一维护与灰度发布 Prompt 模板（A/B 测试、版本回滚） |

## 各方案适用场景建议

### ✅ 选择 Managed Agents API 当：
- 你需要构建一个**具备完整对话生命周期、状态记忆与工具调用能力的智能体**；
- 业务逻辑涉及**多步骤决策、外部系统集成（如数据库查询、API 调用、代码执行）**，且需沙箱隔离保障安全；
- 要求**实时流式响应**（如思考过程、工具执行进度、逐步生成结果）；
- 开发团队熟悉事件驱动架构，能合理设计 Agent 版本、Environment 复用策略与 Session 生命周期管理。

### ✅ 选择 Application Component API 当：
- 你的核心需求是**构建和管理应用的数据底座与知识中枢**，而非运行一个“会说话的 Agent”；
- 需要**批量、异步、可靠地接入企业内部文档、表格、数据库连接器**，并建立可检索的知识索引；
- 要对 Prompt 进行**集中化、版本化、权限化的治理**，支持运营人员低代码配置；
- 项目以**数据准备、知识沉淀、检索增强（RAG）** 为主要目标，后续可能将检索结果注入到 Managed Agents 的提示词中。

### ⚠️ 注意：二者常协同使用
绝大多数生产级智能应用采用**分层架构**：
- **下层（Infrastructure）**：用 Application Component API 完成：上传客户合同（`AddFile`）→ 创建法律知识库（`CreateIndex` + `SubmitIndexJob`）→ 维护合规问答 Prompt（`CreatePromptTemplate`）；
- **上层（Runtime）**：用 Managed Agents API 构建：创建一个 `legal-assistant` Agent，其系统提示词引用上述 Prompt 模板，技能（Skill）中集成知识库检索（`Retrieve`）接口，并在沙箱中执行合同条款比对脚本。

此时，Application Component 提供“静态能力”，Managed Agents 提供“动态执行”。

## 技术选型参考指南（面向开发者）

| 评估维度 | 推荐动作 |
|----------|-----------|
| **是否需要会话状态管理？** | 若需跨消息保持上下文（如用户说“上一条提到的金额是多少？”），必须选 Managed Agents；若每次请求独立（如单次文档摘要），Application Component + 直接调用模型 API 更轻量。 |
| **是否涉及工具调用或代码执行？** | 只有 Managed Agents 提供沙箱（Environment）与 Skill 挂载机制；Application Component 仅提供数据/知识/Prompt，不执行任何代码。 |
| **数据来源是否已结构化/标准化？** | 若原始数据分散在多个系统（OSS、MySQL、SharePoint），优先用 Application Component 的 Connector 和 `AddFilesFromAuthorizedOss` 统一接入；若数据已就绪且无需索引，Managed Agents 可直接引用 File ID。 |
| **团队 DevOps 能力** | Managed Agents 要求理解事件流、SSE 解析、Session 错误重试；Application Component 更接近传统 REST API，调试门槛较低，但需关注 ROA 签名与 RAM 权限配置。 |
| **长期演进考量** | Application Component 是百炼平台的“能力基座”，接口稳定性高、迭代节奏稳；Managed Agents 是前沿运行时抽象，功能更新快（如新增沙箱类型、事件类型），需关注版本兼容性说明。 |

> 💡 **一句话总结**：  
> **用 Application Component “搭积木”——构建数据、知识与提示的基石；**  
> **用 Managed Agents “跑程序”——在基石之上启动一个会思考、能行动的智能体。**  
> 二者不是二选一，而是“先筑基，再启智”的标准实践路径。

## 被对比主题页

- [managed agents api](../api/managed-agents-api.md)
- [application component api reference](../api/application-component-api-reference.md)



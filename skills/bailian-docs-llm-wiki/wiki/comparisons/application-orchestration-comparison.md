# 应用编排方案对比：Managed Agents vs Application Component API

## 背景与目的  
在百炼平台中，开发者构建智能应用时面临两类核心编排需求：  
- **面向任务执行的智能体运行时编排**（如客服对话、自动化工作流、工具调用型助手）；  
- **面向数据与知识能力的底层组件集成编排**（如知识库构建、多源数据接入、结构化/非结构化内容检索）。  

`Managed Agents API` 与 `Application Component API` 分别服务于上述两类范式，但设计目标、抽象层级和适用边界存在本质差异。本文旨在为开发者提供清晰、可落地的技术选型参考，通过关键维度横向对比，明确各方案的能力边界、约束条件与最佳实践场景，避免因误用导致架构冗余、开发成本上升或功能不可达。

---

## 关键维度对比

| 维度 | Managed Agents API | Application Component API |
|------|---------------------|----------------------------|
| **核心定位** | 托管式智能体（Agent）运行时服务，聚焦「任务驱动的会话式执行」 | 应用级基础能力组件（数据连接、知识库、切片管理等）的原子化接口集合，聚焦「能力供给与数据治理」 |
| **输入格式** | OpenAI-style `messages` 数组（仅支持 `role: "user"`），通过 `/sessions/{id}/events` 提交；支持 ≤20 MB 文件直传（需先上传获 `file_id`） | ROA 风格请求体，按资源类型差异化定义：<br>• 数据连接：`AddFile` 含 `parser`、`category_id` 等<br>• 知识库：`CreateIndex` 含 `type`（文档搜索/数据查询等）、`name`<br>• 检索：`Retrieve` 含纯文本 `query` |
| **输出格式** | SSE 事件流（`text/event-stream`），含 `session_status`（`idle`/`running`/`terminated`）、`message`（模型响应/工具调用结果）、`tool_calls` 等结构化事件；终态后返回 `session_result` JSON 对象 | 标准 HTTP JSON 响应，含 `RequestId`、`Success`、`Data` 字段；列表类接口支持 `NextToken` 分页；状态类接口（如 `GetIndexJobStatus`）需轮询 |
| **支持模型** | 仅限百炼托管白名单模型（当前为 `qwen-plus` 等），**不支持自定义模型或外部模型接入** | **不直接涉及模型调用**；知识库检索结果可被下游模型消费，但本 API 不参与模型推理过程 |
| **API 端点风格** | RESTful + SSE 流式端点（如 `POST /sessions/{id}/events`, `GET /sessions/{id}/events/stream`） | ROA（Resource-Oriented Architecture）风格，统一 `https://bailian.aliyuncs.com` 域名，路径含资源类型（如 `/api/v1/indices`, `/api/v1/files`） |
| **计费方式** | 按 **Session 实际运行时长**（秒级）+ **工具调用次数** + **文件存储量** 计费；沙箱环境资源消耗计入 Session 成本 | 按 **API 调用次数**（如 `AddFile`、`SubmitIndexJob`）+ **知识库存储量**（GB/月）+ **检索 QPS** 计费；无“运行时”概念，无会话生命周期费用 |
| **典型场景** | • 多轮对话型智能客服（需状态保持、工具调用）<br>• 自动化办公流程（如审批+查数据库+发邮件）<br>• 安全沙箱内执行代码/脚本的 AI 助手 | • 构建企业级知识库（PDF/Word/OSS 数据导入 → 解析 → 构建索引）<br>• 接入多源业务数据（MySQL 连接器 + 表同步）<br>• 细粒度管理知识切片（`AddChunk`/`UpdateChunk`）用于 A/B 测试或合规审查 |
| **状态管理** | 强状态机：`idle → running → (idle \| terminated)`；Session 状态由平台严格维护，支持 SSE 实时监听 | 无全局会话状态；各资源（Index/File/Category）独立生命周期，依赖显式状态字段（如 `index.status=BUILDING`）及轮询判断 |
| **扩展性与定制** | Agent 技能（Skill）需 ZIP 包上传+安全扫描；支持版本锁定，但**不支持动态加载/热更新**；模型固定 | 支持灵活的数据源扩展（OSS/MySQL/API Connector）；知识库类型可扩展（文档/数据/图片/音视频）；**解析器（Parser）可动态配置**（如 `DOCMIND_LLM_VERSION`） |
| **安全隔离** | 工作空间级隔离 + 沙箱环境（`cloud` 类型）隔离；Skill 包强制安全扫描；文件审核态（`checking`→`available`） | 工作空间级隔离 + RAM 权限控制；OSS 导入需同账号授权；临时文件租约（`ApplyTempStorageLease`）有明确作用域限制 |

---

## 适用场景建议

### ✅ 选择 **Managed Agents API** 当：
- 你的应用本质是「一个可交互、有状态、需调用工具的智能体」；
- 需要开箱即用的会话管理、低延迟流式响应（SSE）、沙箱安全执行环境；
- 业务逻辑复杂度高（如多步骤决策链、条件分支、循环调用工具），且希望平台托管状态机与错误恢复；
- 模型能力已满足需求（`qwen-plus` 等），无需接入私有模型或外部 LLM；
- 可接受按运行时长计费，且对 Session 生命周期（最长 30 分钟？需查配额）有明确预期。

> ⚠️ 注意：若需高频短时交互（如每秒多次问答），Managed Agents 的 Session 创建/销毁开销可能高于轻量调用；此时应评估是否真需「Agent」而非「模型 API 直调」。

### ✅ 选择 **Application Component API** 当：
- 你的核心需求是「构建和管理知识能力底座」，而非运行一个对话机器人；
- 需要对接企业内部数据源（数据库、OSS、API）、进行文档解析、构建可检索的知识库；
- 要求对知识切片（Chunk）做精细化控制（如人工审核、敏感信息脱敏、版本回滚）；
- 需要将知识检索结果作为输入，喂给自有模型或下游服务（如 RAG Pipeline）；
- 希望按调用次数/存储量付费，且无长期运行成本顾虑。

> ⚠️ 注意：该 API **不提供任何对话能力或模型推理服务**。它产出的是结构化知识（Index）、解析后的文件（File）、可用的连接器（Connector），需配合其他 API（如 Model API 或 Managed Agents）才能形成完整应用。

---

## 技术选型参考（面向开发者）

| 你的问题 | 推荐方案 | 理由 |
|----------|-----------|------|
| “我要做一个能查订单、改地址、发短信的电商客服机器人” | **Managed Agents API** | 符合「多工具调用+状态保持+用户对话」核心特征；沙箱保障短信/订单系统调用安全。 |
| “我要把公司 1000 份产品手册 PDF 导入平台，支持语义搜索” | **Application Component API** | 使用 `AddFile` + `CreateIndex` + `SubmitIndexJob` 流程，是标准知识库构建路径。 |
| “我的 RAG 应用需要动态切换不同知识库，且对 Chunk 准确率要求极高” | **Application Component API** + 自研调度层 | 利用 `ListIndices`/`Retrieve` 管理知识库，用 `AddChunk`/`UpdateChunk` 精细控制切片，再由自有模型调用检索结果。 |
| “我已有私有部署的 Llama3 模型，想封装成带工具调用的 Agent” | **暂不适用任一方案** | Managed Agents 不支持外部模型；Application Component 不提供 Agent 运行时。需使用百炼 **Model API + 自建 Agent 框架**。 |
| “我需要同时实现客服对话（Agent）和后台知识管理（Index）” | **两者组合使用** | Managed Agents 中的 Agent 可调用 Application Component 构建的知识库（通过 Skill 封装 `Retrieve` 调用）；二者通过 `workspace_id` 共享上下文与权限体系。 |

> 💡 **最佳实践提示**：  
> - **不要用 Application Component API 替代 Agent**：它无法处理多轮对话状态、无法发起工具调用、无 SSE 流式响应。  
> - **不要用 Managed Agents API 替代知识库构建**：它不提供文件解析、索引构建、切片管理等能力，强行用 Session 模拟会导致架构脆弱、成本失控。  
> - **组合使用是常态**：90% 的生产级智能应用，既需要 Managed Agents 提供交互入口，也需要 Application Component 提供知识底座——二者是互补关系，而非替代关系。

---  
*最后更新：2024年6月*  
*文档依据：百炼平台 v2.3.x 版本 API 规范*

## 被对比主题页

- [managed agents api](../api/managed-agents-api.md)
- [application component api reference](../api/application-component-api-reference.md)



# 知识管理方案对比：Knowledge API、Knowledge Base 与 Data Connection Overview

## 对比目的与背景

在百炼平台构建 RAG（[检索增强生成](../concepts/rag.md)）应用时，开发者常面临多种知识接入与管理能力的选择：`Knowledge API` 提供轻量级、面向集成的语义检索与问答接口；`Knowledge Base` 是功能完备、开箱即用的全生命周期知识库服务；`Data Connection Overview` 则聚焦于**外部数据源的统一纳管与实时/准实时接入**。三者定位不同、能力边界清晰，但存在功能交叠（如均支持文档检索）和协作关系（如 Data Connection 可作为 Knowledge Base 的数据源）。本页旨在从技术视角系统对比三者的核心差异，帮助开发者基于业务需求、架构约束与运维成本做出理性选型决策。

---

## 关键维度对比表

| 维度 | Knowledge API | Knowledge Base | Data Connection Overview |
|------|----------------|----------------|---------------------------|
| **本质定位** | 面向业务集成的**RAG能力封装层**（HTTP REST 接口），不管理知识本身，仅调度已就绪知识库 | 百炼平台原生的**端到端知识管理服务**，覆盖知识上传、索引、检索、问答、同步、监控全链路 | **外部数据源统一接入通道**，解决“如何安全、可控地把数据接进来”，不提供检索/问答能力本身 |
| **输入格式** | `query`（纯文本，≤2048 字符） + `knowledgeIds`（可选）；不接受原始文件或结构化数据 | 支持多源异构数据：<br>• 非结构化：PDF/DOCX/PPTX/图片/音视频<br>• 结构化：Excel/CSV（表格知识库）<br>• 多模态：图文混合内容 | 按连接器类型区分：<br>• 平台托管型：本地文件 / OSS Bucket 中的 PDF/Word/Excel/Markdown<br>• 流处理型：MySQL/PostgreSQL/PolarDB-X 表数据、语雀文档、OSS 对象元信息或内容（需配置） |
| **输出格式** | • 检索：JSON 数组（含 `content`, `score`, `metadata` 等字段）<br>• 问答：SSE 流式响应（含 `planning`/`tool_calling`/`generation` 阶段事件）或完整 JSON（`stream=false`） | • 检索：控制台可视化结果 + API 返回结构化切片（含高亮、来源锚点）<br>• 问答：自然语言回答 + 引用溯源（支持开启/关闭）<br>• 日志：SLS 投递结构化日志（含 `latency`, `pipeline_id`, `response_code`） | 不直接输出业务数据；通过工具调用返回：<br>• `searchFile`/`searchTable` → JSON 切片列表<br>• `executeSQL` → JSON 格式查询结果集<br>• `searchOSSFile` → 文件元信息或内容摘要（取决于配置） |
| **支持模型** | **不暴露模型选择权**：底层由业务空间绑定的默认推理服务自动调度；不支持透传 `temperature`/`maxTokens` 等参数 | 显式支持多模型：<br>• 预置：Qwen 系列（Qwen3/Qwen2.5/Long/Max/VL-Max/OCR）、DeepSeek-R1、Llama3.1、Yi-Large 等<br>• 自定义：基于预置基座微调后接入<br>• 向量/重排/路由模型可独立配置（如 `text-embedding-v4`, `qwen3-rerank`） | **无模型概念**：仅提供数据访问能力；模型调用发生在上层（如 Knowledge Base 或智能体中），Data Connection 仅负责提供原始数据或结构化结果 |
| **API 端点** | • 检索：`POST https://{workspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/indices/knowledge/search`<br>• 问答：`POST https://{workspaceId}.cn-beijing.maas.aliyuncs.com/api/v2/apps/knowledge/chat` | • 控制台操作为主，配套 SDK/API：<br>– 创建知识库、上传文件、提交索引任务等<br>– 端点分散（如 `/v1/knowledge_bases/{kb_id}/files`, `/v1/knowledge_bases/{kb_id}/search`）<br>• 所有调用需 `workspace_id` 路径参数 | • 连接器管理：`POST /v1/connectors`（创建）<br>• 数据调用：通过内置工具触发（如 `searchFile`, `executeSQL`），非直连 HTTP 端点<br>• 工具调用由百炼运行时解析并路由至对应连接器 |
| **计费方式** | • **按调用次数计费**（QPS 级别）<br>• 无知识库存储费、向量化费、模型调用费（这些费用归属 Knowledge Base 或模型服务）<br>• 属于“能力调用”类计费 | • **规格费 + 模型费分离**：<br>– 规格费：标准版（免费额度）、旗舰版（按 RCU 小时计费）<br>– 模型费：向量模型、重排模型、路由模型、问答模型 [Token](../concepts/token.md) 消耗单独计费，多知识库叠加<br>• 存储费：超出免费额度后按量计费 | • **连接器实例费 + 数据处理费**：<br>– 连接器实例：按小时计费（如 MySQL 连接器）<br>– 数据处理：平台托管型按文件数/大小计费；流处理型按 SQL 查询次数或 API 调用次数计费<br>• 不包含模型推理费用 |
| **典型场景** | • 第三方系统快速集成 RAG 能力（如 CRM 嵌入问答框）<br>• 需要细粒度控制检索阶段（如自定义混排逻辑）<br>• 构建多知识库联合检索中台，对外提供统一检索网关 | • 企业级知识中心建设（如内部文档库、产品手册库）<br>• 多轮对话智能客服（需历史上下文+知识引用）<br>• 定时同步飞书/钉钉/语雀知识并自动更新<br>• 需要 SLS 日志审计与效果分析的生产环境 | • 实时对接业务数据库（如订单库、用户画像库）做动态查询<br>• 将 OSS 中海量历史文档作为知识源批量导入 Knowledge Base<br>• 语雀团队知识库与百炼应用双向联动<br>• 构建跨数据源的统一检索入口（需配合 Knowledge Base 或工作流） |

---

## 各方案适用场景建议

### ✅ 选择 **Knowledge API** 当：
- 你已拥有多个已构建完成的知识库（`Knowledge Base`），只需一个**标准化、低耦合的接口**对外提供检索/问答能力；
- 你的应用是轻量级前端或第三方系统，**不希望管理知识生命周期**（上传、索引、状态监控），只关注“发问题、得答案”；
- 需要**自定义 RAG 流程**（例如：先调用 Knowledge API 检索 → 用自研重排模型排序 → 再送入指定大模型生成），而非开箱即用的问答；
- 对延迟敏感，且能接受流式响应解析（SSE），追求端到端请求链路最短。

### ✅ 选择 **Knowledge Base** 当：
- 你需要从零开始构建一个**完整的私有知识服务**，涵盖数据接入、清洗、索引、检索、问答、同步、监控全流程；
- 业务涉及**多模态知识**（如 PDF 文档 + 产品截图 + 宣传视频），需统一向量化与跨模态理解；
- 要求**开箱即用的生产级能力**：相似度阈值调优、拒答策略、引用溯源、SLS 日志、定时同步、多知识库混排；
- 团队具备一定平台使用经验，愿意接受华北2（北京）地域限制，并能协调模型费用与规格配额。

### ✅ 选择 **Data Connection Overview** 当：
- 你的核心数据**不在百炼平台内，且需实时/准实时访问**（如交易数据库、CRM 系统、语雀最新文档）；
- 需要将**外部结构化数据（SQL 查询结果）或非结构化文件（OSS 中的合同）作为 RAG 的补充数据源**，而非唯一知识源；
- 希望统一管理所有外部数据连接权限、网络策略、健康检测，避免每个应用单独对接；
- 计划构建“数据湖 → Data Connection → Knowledge Base → 应用”的分层架构，实现数据治理与 AI 能力解耦。

> ⚠️ 注意：三者非互斥关系。典型组合模式包括：  
> • **Data Connection + Knowledge Base**：用 Data Connection 将 OSS/语雀数据自动同步至 Knowledge Base；  
> • **Knowledge Base + Knowledge API**：Knowledge Base 构建知识，Knowledge API 对外提供统一服务能力；  
> • **Data Connection + Knowledge API（间接）**：通过工作流或智能体，用 Data Connection 获取数据 → 注入提示词 → 调用 Knowledge API 问答。

---

## 技术选型参考（面向开发者）

| 选型考量因素 | 推荐方案 | 理由说明 |
|--------------|----------|----------|
| **开发效率优先（MVP 快速上线）** | `Knowledge Base` | 控制台向导式创建，支持一键上传、自动索引、即时问答，无需编写索引逻辑或流式解析代码。 |
| **系统解耦与服务复用** | `Knowledge API` | 作为中间能力层，可被多个前端、小程序、内部系统复用；知识库变更不影响调用方，符合微服务设计原则。 |
| **实时性要求高（秒级数据新鲜度）** | `Data Connection Overview`（流处理型） | 直连数据库执行 SQL，或调用语雀 API 获取最新文档，规避知识库向量化延迟（1–3 分钟）。 |
| **成本敏感型项目（预算有限）** | `Knowledge API`（搭配免费知识库） 或 `Knowledge Base`（标准版） | Knowledge API 本身无存储/模型费；Knowledge Base 标准版提供 720 小时/月免费规格，适合中小规模知识库。 |
| **需要深度定制 RAG Pipeline** | `Knowledge API` + 自研组件 | Knowledge API 提供纯净检索结果（chunk），便于接入自研重排、过滤、聚合模块，再送入任意 LLM。 |
| **跨地域部署需求** | ❌ 三者均不支持（`Knowledge Base` 和 `Data Connection` 强制华北2；`Knowledge API` Endpoint 依赖 workspaceId 地域） | 当前百炼知识能力仅限 `cn-beijing`，若业务必须部署在新加坡/法兰克福等区域，需评估代理或数据同步方案。 |
| **安全合规要求严格（如金融、政务）** | `Knowledge Base`（旗舰版） + `Data Connection`（私网连接） | 旗舰版支持 VPC 内网访问、RCU 隔离；PolarDB-X/MySQL 私网连接杜绝公网暴露；所有操作留痕于 SLS 日志。 |

> 💡 **最后建议**：  
> - 新项目起步，**优先尝试 Knowledge Base** —— 它覆盖 90% 的通用 RAG 场景，且文档与控制台体验成熟；  
> - 当 Knowledge Base 无法满足特定流程（如需自定义 chunk 后处理、多阶段决策），再引入 **Knowledge API** 作为增强；  
> - **Data Connection 不是“替代 Knowledge Base”的选项，而是它的“上游数据引擎”** —— 请始终将其视为数据管道，而非知识服务本身。  

---  
*本文档依据百炼平台 2024 Q3 版本功能撰写，具体以控制台实际界面及 OpenAPI 文档为准。*

## 被对比主题页

- [knowledge](../api/knowledge.md)
- [knowledge base](../guides/knowledge-base.md)
- [data connection overview](../guides/data-connection-overview.md)



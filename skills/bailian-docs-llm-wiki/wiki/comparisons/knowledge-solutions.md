# 知识能力方案对比：Knowledge API、Knowledge Base 与 Data Connection

## 对比目的与背景

在百炼平台构建 RAG（[检索增强生成](../concepts/rag.md)）应用时，开发者常面临多种知识接入路径的选择：是直接调用封装好的语义问答服务？还是基于可配置的知识库自主编排检索与生成流程？抑或需要对接实时外部数据源以支撑动态查询？Knowledge API、Knowledge Base 和 Data Connection 是百炼平台提供的三类核心知识能力方案，分别面向**服务化调用**、**RAG 基础设施**和**外部数据集成**三大技术范式。本页旨在从技术定位、能力边界、使用约束与成本模型等维度进行系统性对比，帮助开发者根据业务需求、工程成熟度与运维能力，做出清晰、可落地的技术选型决策。

---

## 关键维度对比表

| 维度 | Knowledge API | Knowledge Base | Data Connection |
|------|----------------|----------------|------------------|
| **本质定位** | 面向终端用户的**托管式知识服务**（SaaS 化 API），提供开箱即用的检索与问答能力 | 百炼平台原生的**RAG 核心基础设施**，为智能体、工作流及自定义应用提供可配置、可编排的知识检索能力 | **外部数据源统一接入层**，实现结构化/非结构化数据的安全、可控接入，支持就地访问或导入处理 |
| **输入格式** | 纯文本 `query`（JSON Body）；支持 `stream`、`top_k`（仅检索）等轻量参数 | 多样化输入：<br>• 文档类：PDF/Word/Excel/Markdown 等原始文件<br>• 结构化：CSV/Excel 表格（单文件）<br>• 多模态：图片、音视频（需对应类型知识库）<br>• 运行时：`query` + `index_id` + 可选 `tags`/`metadata_filter` | 按连接器类型差异显著：<br>• 文件/表格：上传文件或配置 OSS Bucket<br>• 数据库：数据库连接参数（host/port/user/pass）<br>• 语雀/OSS：API [Token](../concepts/token.md) 或 Bucket 名称 |
| **输出格式** | • 检索接口：标准 JSON 数组，含 `chunks` 字段<br>• 问答接口：默认 SSE 流式响应（含 `planning`/`tool calling`/`generation` 三阶段事件）；`stream=false` 时返回完整 JSON，含 `output.choices[0].message.content` | • 检索结果：JSON 格式切片列表（含 `content`、`score`、`metadata` 等）<br>• 智能体/工作流中：自动注入 `{result}` 变量供提示词引用<br>• 支持引用溯源（标注来源文档与页码） | • 平台托管型：通过 `retrieval` 工具返回结构化切片<br>• 流处理型：<br>  - SQL 类：`executeSQL` 返回查询结果集（JSON 数组）<br>  - 语雀/OSS：`searchYuQueDoc` / `searchOSSFile` 返回匹配文档元信息 |
| **支持模型** | **固定模型**：问答阶段强制使用 `qwen-max` 或 `qwen-plus`（由服务端决定，不可指定）；不开放模型选择权 | **全量模型支持**：覆盖 Qwen3/Qwen2.5/Qwen2/QwQ/Long/Max/Plus/Turbo/Coder/Deep-Research、Qwen-VL 系列（Max/Plus/Flash/OCR）、DeepSeek-R1、Llama3.1、Yi-Large 等；模型在应用/工作流节点中显式选择 | **无模型耦合**：本身不执行 LLM 推理，仅为数据通道；实际模型由调用方（智能体/工作流/自定义 API）决定 |
| **API 端点** | • 检索：`POST https://{workspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/indices/knowledge/search`<br>• 问答：`POST https://{workspaceId}.cn-beijing.maas.aliyuncs.com/api/v2/apps/knowledge/chat` | • 检索（Retrieve）：`POST /v1/indices/{index_id}/retrieve`（需鉴权）<br>• 其他能力（如 QA、Search）通过更高层服务（如 `/api/v2/apps/knowledge/chat`）复用，但底层依赖知识库索引 | • 无统一 REST API；通过**工具调用（Tool Calling）** 触发：<br>  - `retrieval`（知识库检索）<br>  - `executeSQL`（DMS 导入的数据库）<br>  - `searchYuQueDoc` / `searchOSSFile` 等<br>• 所有工具均在智能体/工作流上下文中运行 |
| **计费方式** | • **按调用次数计费**（QPS 级别）<br>• 不区分检索/问答，统一计费单元<br>• 限流策略严格（默认 25 QPS），超限返回 `429` | • **双轨计费**：<br>  - **规格费**：按知识库实例小时数计费（标准版/旗舰版）<br>  - **调用费**：按 [Token](../concepts/token.md) 计费（向量化 + Rerank + LLM 生成）<br>• Rerank 费用取决于**初步召回切片总数**（非最终返回数），多知识库绑定费用线性叠加 | • **按连接器类型与用量计费**：<br>  - 文件/表格：平台存储按量付费（超出免费额度后）<br>  - 数据库/OSS/语雀：按**调用次数**或**数据传输量**计费（详见控制台定价页）<br>• DMS 导入的数据库连接器额外产生 DTS 同步费用（若启用） |
| **典型场景** | • 快速上线客服问答机器人（无需搭建 RAG 流程）<br>• 内部知识助手 MVP 验证<br>• 对模型可控性要求低、追求交付速度的轻量级应用 | • 构建高精度专业问答系统（需精细调控相似度阈值、TopK、Meta 过滤）<br>• 多知识库协同的复杂 RAG 应用（如法律条文+判例+内部制度）<br>• 需要审计日志、用量监控与效果优化的生产级 RAG | • 实时查询业务数据库（如订单状态、库存余额）<br>• 动态拉取语雀知识库最新文档<br>• 将 OSS 中的海量报告文件作为“活”知识源接入<br>• 构建混合数据源（数据库+文档+图片）的统一问答入口 |

---

## 适用场景建议

### ✅ 选择 **Knowledge API** 当：
- 你希望**零配置快速上线**一个具备基础语义理解能力的知识问答服务；
- 业务对模型选型无定制需求，接受平台统一调度的 `qwen-max`/`qwen-plus`；
- 团队缺乏 RAG 工程经验，或当前阶段以验证用户价值为优先；
- 请求量稳定且可预测（需注意 25 QPS 默认限流，高并发需申请提升配额）；
- **不**需要深度定制检索逻辑、不关心切片来源细节、不需与自有工作流深度集成。

### ✅ 选择 **Knowledge Base** 当：
- 你需要**完全掌控 RAG 全链路**：从文档解析、切片策略、向量模型、相似度阈值到提示词工程；
- 业务涉及**多源异构知识**（如 PDF 技术文档 + Excel 产品参数 + 图片手册），需分类管理与精准过滤（Meta/Tag）；
- 要求**生产级可观测性**：SLS 日志审计、用量统计、告警监控、效果 A/B 测试；
- 需要与**智能体行为深度耦合**（如拒答、引用溯源、多跳推理）；
- 模型选型关键（如必须使用 `qwen3` 或 `deepseek-r1`），且需灵活切换。

### ✅ 选择 **Data Connection** 当：
- 你的知识**天然存在于外部系统**（MySQL 订单库、语雀团队 Wiki、OSS 归档报告），且要求**实时性或强一致性**；
- 需要**绕过文档解析与向量化环节**，直接执行结构化查询（如 `SELECT * FROM orders WHERE status='pending'`）；
- 数据敏感，**禁止上传至百炼平台存储**，必须就地访问；
- 构建**混合知识源应用**：例如，用知识库回答“产品功能”，用 Data Connection 查询“当前库存”并动态插入答案；
- 需要对接**非标准数据源**（如 PolarDB-X 分布式数据库、特定语雀租户）。

> ⚠️ 注意：三者并非互斥，而是**分层协作关系**。典型架构中：  
> **Data Connection** 提供实时数据通道 → **Knowledge Base** 管理静态/半静态领域知识 → **Knowledge API** 作为面向前端的统一问答网关（其底层可聚合多个 Knowledge Base 与 Data Connection 工具）。

---

## 技术选型参考（面向开发者）

| 选型考量因素 | 推荐方案 | 理由说明 |
|--------------|----------|----------|
| **开发周期 < 1 周** | Knowledge API | 无需创建知识库、无需配置连接器、无需编写工具调用逻辑，仅需构造 URL + API Key 即可发起请求 |
| **需支持多模态（图文/音视频）** | Knowledge Base | 唯一原生支持图片问答、音视频搜索的知识能力；Data Connection 仅支持文件接入，不提供多模态理解能力 |
| **数据更新频率 > 每小时** | Data Connection（流处理型） | 知识库同步存在延迟（分钟至小时级），而 MySQL/语雀/OSS 连接器可实现秒级数据可见 |
| **要求 LLM 模型可自由切换** | Knowledge Base | Knowledge API 固定模型；Data Connection 本身不涉及模型；Knowledge Base 允许在智能体/工作流中任意选择已购模型 |
| **需审计每条检索的原始切片与来源** | Knowledge Base | 提供完整 SLS 日志与切片溯源能力；Knowledge API 仅返回聚合结果；Data Connection 的 SQL 查询结果无语义切片概念 |
| **预算敏感，需精确控制 [Token](../concepts/token.md) 成本** | Knowledge Base | 可精细设置 `top_k`、相似度阈值、初步召回数，直接影响 Rerank 与 LLM 输入 Token；Knowledge API 无此调控粒度 |
| **已有大量结构化数据在 RDS，且需复杂 JOIN 查询** | Data Connection（DMS 导入方式） | Knowledge Base 仅支持单表 CSV/Excel，无法执行跨表关联；Knowledge API 不支持 SQL；唯有 DMS 导入的数据库连接器支持完整 SQL 能力 |

**最终建议**：  
- **MVP 验证期** → 优先试用 Knowledge API，快速验证用户需求；  
- **进入产品化阶段** → 迁移至 Knowledge Base，构建可维护、可观测、可优化的 RAG 基础设施；  
- **出现实时数据需求** → 在 Knowledge Base 架构上，通过 Data Connection 接入数据库/语雀等，形成“静态知识 + 动态数据”的混合增强范式。  

所有方案均需部署于 **华北2（北京）地域**，且依赖有效的 `workspaceId` 与匹配的 `API Key`。请务必在控制台确认业务空间地域与权限策略（如 `AliyunBailianDataFullAccess`）已正确配置。

## 被对比主题页

- [knowledge](../api/knowledge.md)
- [knowledge base](../guides/knowledge-base.md)
- [data connection overview](../guides/data-connection-overview.md)



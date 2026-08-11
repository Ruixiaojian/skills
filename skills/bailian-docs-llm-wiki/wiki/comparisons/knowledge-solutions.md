# 知识管理方案对比：Knowledge API vs Knowledge Base vs Data Connection Overview

为帮助开发者在百炼平台中高效选型知识管理能力，本文系统对比三种核心知识接入与增强方案：**Knowledge API**（面向开发者的轻量级语义检索与问答接口）、**Knowledge Base**（面向RAG场景的全生命周期知识库服务）和**Data Connection Overview**（面向异构数据源的统一连接与实时访问能力）。三者定位互补：Knowledge API 提供即用型能力封装；Knowledge Base 构建可配置、可优化的私有知识中枢；Data Connection 则打通企业内外部数据孤岛，支持结构化与非结构化数据的动态接入。本对比聚焦技术实现差异、集成成本、适用边界及成本模型，旨在为架构设计与工程落地提供明确决策依据。

## 关键维度对比

| 维度 | Knowledge API | Knowledge Base | Data Connection Overview |
|------|----------------|----------------|---------------------------|
| **核心定位** | 面向开发者的 RESTful 语义检索与端到端问答服务（应用网关层能力） | 百炼原生 RAG 核心服务，提供知识上传、索引构建、多路召回、精排与问答生成的完整闭环 | 统一数据接入层，桥接外部数据源（数据库/文档系统/OSS等），支持向量化索引与实时查询 |
| **输入格式** | 纯文本 `query`（如 `"如何申请发票？"`）；支持 `top_k`（仅 `/search`）等轻量参数 | 多样化输入：<br>• 文档类：PDF/Word/Markdown/Excel/PPT/图像/音视频<br>• 结构化：表格（XLSX/XLS）、数据库表（通过 DMS 导入）<br>• 元数据：创建时预设字段（不可修改） | 按连接器类型区分：<br>• 平台托管型：本地文件或 OSS 对象（PDF/DOCX/CSV/XLSX/MP4/JPG 等）<br>• 流处理型：数据库连接参数（地址/账号/SQL）、语雀 [Token](../concepts/token.md)、OSS Bucket 名称等 |
| **输出格式** | • `/search`：JSON 数组，含 `content`、`score`、`metadata` 等字段的文本切片<br>• `/chat`：SSE 流式响应，含 `planning`、`tool_calls`、`generation` 三阶段事件 | • 检索结果：JSON 切片列表（含 `content`、`score`、`source`、`page_number` 等）<br>• 问答结果：自然语言回答（`text` 字段），支持流式 SSE 或同步 JSON | • 向量检索：JSON 切片（`content` + `metadata`）<br>• SQL 查询：JSON 格式结果集（列名+行数据）<br>• 文件搜索：`searchOSSFile` 等工具返回匹配文件路径与元信息 |
| **支持模型** | • 检索：底层固定使用 `text-embedding-v4`（隐式）<br>• 问答：由业务空间内知识应用配置决定，默认 `qwen-max` 或 `qwen-plus`，**不可显式指定** | • 向量模型：`text-embedding-v4`（文本）、`qwen3-vl-embedding`（[多模态](../concepts/multi-modal.md)）<br>• 排序模型：`qwen3-rerank` / `qwen3-vl-rerank`（可选）<br>• 路由模型：`qwen-plus`（启用路由时调用）<br>• 问答模型：所有百炼支持大模型（`Qwen3`、`DeepSeek-R1`、`Llama3.1` 等）均可作为底座 |
| **API 端点** | • Base URL：`https://{workspaceId}.cn-beijing.maas.aliyuncs.com`<br>• 检索：`POST /api/v1/indices/knowledge/search`<br>• 问答：`POST /api/v2/apps/knowledge/chat` | • SDK/API：`Retrieve`（检索）、`CreateIndex`/`AddFile`（管理）等 OpenAPI RPC 接口<br>• 控制台服务入口：知识检索服务（多库混排）、知识问答服务（极速/多轮智能模式） | • 工具调用：在智能体或工作流中通过预置工具名触发（如 `querySQL`、`searchOSSFile`）<br>• SDK：无独立 RESTful API，需通过百炼 SDK 的 `ToolCall` 或工作流节点调用 |
| **计费方式** | • 按调用量计费：`/search` 和 `/chat` 均按 **请求次数 + [Token](../concepts/token.md) 消耗** 计费<br>• 不产生知识库规格费（不依赖知识库实例）<br>• 无存储费用 | • **双轨计费**：<br>  – 规格费：按小时计费（标准版 0.03 元/小时；旗舰版 0.2 元/RCU/小时）<br>  – 模型费：按 [Token](../concepts/token.md) 计费（向量、Rerank、问答生成均单独计费）<br>• Rerank 费用取决于初步召回 TopK，**非最终返回数**，易超支 | • **按使用计费**：<br>  – 向量索引构建：按文档页数/音视频时长计费（见 [计费文档](../../raw/application-user-guide/data-connection-overview/data-connection-billing.md)）<br>  – SQL 查询：按执行次数 + 返回行数计费<br>  – 文件解析：按文件大小/类型计费<br>• 无固定规格费，但自有 OSS 存储费用另计 |
| **典型场景** | • 快速验证知识问答效果（MVP 阶段）<br>• 构建轻量级客服机器人（无需自建知识库）<br>• 在已有系统中嵌入“一键问答”功能（低侵入集成） | • 企业级知识中心建设（如内部 Wiki、产品文档库、法务合规库）<br>• 需精细化控制召回策略（多库路由、标签过滤、相似度阈值调优）<br>• 要求长期知识沉淀、版本管理与权限隔离 | • 实时对接业务数据库（如查订单、查库存）<br>• 动态拉取最新文档（如钉钉/飞书知识库、OSS 中的合同模板）<br>• 多源异构数据融合检索（如“结合销售数据库+产品手册+会议纪要”回答问题） |
| **地域支持** | 仅支持 `cn-beijing`（URL 固定） | 仅支持 `cn-beijing`（明确限制） | 支持 `cn-beijing`；部分连接器（如 OSS）在其他地域可用，但**与百炼知识能力联动时仍需北京地域** |

## 各方案适用场景建议

- **选择 Knowledge API 当：**  
  ✅ 你希望以最小开发成本快速验证语义问答能力，且暂无长期知识运营需求；  
  ✅ 你的知识源已稳定发布在百炼控制台，只需调用其联合检索或问答能力；  
  ❌ 不适合需要自定义切片逻辑、调整向量模型、或对召回结果做深度后处理的场景；  
  ❌ 不支持直接接入外部数据库或实时数据源。

- **选择 Knowledge Base 当：**  
  ✅ 你需要构建一个可长期维护、支持多租户/多权限、具备完整 RAG 优化能力（如 rerank、路由、标签过滤）的知识中枢；  
  ✅ 你的知识以静态文档为主（PDF/Word/Excel），且更新频率可控（天/周级）；  
  ✅ 你愿意承担知识库规格费，并需要精细控制成本（如通过 `top_k` 和相似度阈值平衡效果与开销）；  
  ❌ 不适合需要毫秒级实时数据（如股票行情、IoT 设备状态）的场景；  
  ❌ 不支持创建后修改元数据结构或切换知识库类型。

- **选择 Data Connection Overview 当：**  
  ✅ 你的核心数据分散在 MySQL、PostgreSQL、语雀、OSS 等系统中，且要求**查询结果实时、准确、无需人工同步**；  
  ✅ 你需要混合调用多种数据源（如“查数据库订单 + 读 OSS 合同 + 检索语雀 FAQ”）；  
  ✅ 你已在使用 DMS 或拥有自有 OSS，希望复用现有基础设施；  
  ❌ 不适合纯文本知识库建设（如将 1000 份 PDF 打包成知识库并长期迭代）；  
  ❌ 文件类连接器导入后为独立副本，**不与原始文件自动同步**，需手动重传更新。

## 技术选型参考（面向开发者）

| 选型目标 | 推荐方案 | 关键理由 |
|----------|----------|----------|
| **零配置快速上线问答功能** | ✅ Knowledge API | 仅需 API Key + workspaceId，5 分钟完成 `curl` 调试；无需创建知识库或配置连接器；适合 PoC 或嵌入式小工具。 |
| **构建企业级私有知识中心（文档为主）** | ✅ Knowledge Base | 提供完整的生命周期管理（上传→解析→索引→测试→发布→监控）、多维优化参数、权限体系与配额控制，是 RAG 生产环境首选。 |
| **对接实时业务数据库或动态知识源** | ✅ Data Connection Overview | 唯一支持原生 SQL 执行与跨源混查的能力；语雀/OSS 连接器可自动同步最新内容，避免知识陈旧。 |
| **混合场景：既有静态文档库，又需查实时数据库** | ⚠️ **组合使用** | 推荐：Knowledge Base 管理产品文档/制度文件；Data Connection 接入 MySQL 订单库 + OSS 合同库；在智能体工作流中统一编排调用。 |
| **严格控制成本，避免隐性开销** | ⚠️ **重点规避 Knowledge Base 的 TopK 风险** | 若选用 Knowledge Base，务必将 `初步向量检索 TopK` 设为 ≤20（默认 50），并关闭未使用的 Rerank/路由功能；Knowledge API 无此风险，费用更透明。 |
| **需要[多模态](../concepts/multi-modal.md)理解（图表/公式/音视频）** | ✅ Knowledge Base（旗舰版） + Data Connection（文件类） | Knowledge Base 明确支持 `qwen3-vl-embedding`/`qwen3-vl-rerank`；Data Connection 的“大模型文档解析”支持图表理解，二者能力重叠但 Knowledge Base 配置更集中。 |

> **重要提醒**：三者并非互斥关系。实际项目中，**Knowledge API 的 `/chat` 接口底层即调用 Knowledge Base 提供的服务**；而 Data Connection 创建的连接器，可被 Knowledge Base 的“数据查询类”知识库直接引用。建议以业务需求为起点，优先明确数据时效性、更新频率、来源结构与运维能力，再匹配对应方案——而非从技术名词出发做选择。

## 被对比主题页

- [knowledge](../api/knowledge.md)
- [knowledge base](../guides/knowledge-base.md)
- [data connection overview](../guides/data-connection-overview.md)



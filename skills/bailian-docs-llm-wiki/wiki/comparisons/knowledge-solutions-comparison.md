# 知识管理方案对比：Knowledge API vs Knowledge Base

本文旨在帮助开发者清晰区分百炼平台中两类核心知识管理能力——**Knowledge API**（知识检索与问答接口）与**Knowledge Base**（[知识库](../concepts/knowledge-base.md)服务），明确其定位、能力边界、技术约束与适用场景，为 RAG 架构下的技术选型提供客观、可落地的决策依据。二者虽均服务于“私有知识注入大模型”的目标，但在设计哲学、调用层级、集成深度与运维责任上存在本质差异：Knowledge API 是面向应用层的**托管式语义服务接口**，而 Knowledge Base 是面向数据工程的**可配置知识基础设施**。

---

## 关键维度对比

| 维度 | Knowledge API | Knowledge Base |
|------|----------------|----------------|
| **本质定位** | 应用网关层封装的 RESTful 服务，提供开箱即用的检索/问答能力 | 平台级知识基础设施，需显式创建、索引构建、参数调优与生命周期管理 |
| **输入格式** | 纯文本 `query` 字符串 + `knowledgeIds` 列表（指定已发布[知识库](../concepts/knowledge-base.md) ID）；不直接接收原始文件 | 支持多模态原始数据：PDF/DOCX/TXT/CSV/Excel/图片（JPG/PNG）、音视频（MP4/MOV/WAV）等；需上传并触发索引构建 |
| **输出格式** | • 检索：标准 JSON 数组，含 `text`、`score`、`metadata` 等字段<br>• 问答：默认 SSE 流式响应（含 `planning`/`tool_calling`/`generation` 多阶段事件），亦支持非流式 JSON | • 检索服务：JSON 格式，返回 `nodes[]`（含 `text`、`score`、`metadata`、`source` 引用信息）<br>• 问答服务：JSON 或 SSE（取决于配置），含结构化答案、引用溯源及置信度信息 |
| **支持模型** | • 检索：底层向量模型与重排模型由平台自动绑定，不可选<br>• 问答：固定使用 `qwen3.6-plus` 或 `qwen3.7-plus`（由平台预置，不可自定义） | • 向量模型：可选 `text-embedding-v4`（文本）、`qwen3-vl-embedding`（多模态/视觉理解）<br>• 重排模型：可选 `qwen3-rerank`（文本）或 `qwen3-vl-rerank`（多模态）<br>• 生成模型：自由选择 `qwen3.6-plus`、`qwen3.7-plus` 或用户自定义模型（需已部署） |
| **API 端点** | • 检索：`POST https://{workspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/indices/knowledge/search`<br>• 问答：`POST https://{workspaceId}.cn-beijing.maas.aliyuncs.com/api/v2/apps/knowledge/chat`<br>→ **强依赖 workspaceId 构造专属域名** | • 检索：`POST https://dashscope.aliyuncs.com/api/v1/services/knowledge/retrieval`（需鉴权+Workspace ID）<br>• 问答：`POST https://dashscope.aliyuncs.com/api/v1/services/knowledge/qa`<br>→ 使用统一 DashScope 域名，通过 `x-dashscope-workspace-id` Header 传递上下文 |
| **计费方式** | • 按调用量计费（QPS + 请求次数）<br>• 默认限流 25 QPS/用户，超限返回 429<br>• **无存储费用、无 RCU 概念、无[知识库](../concepts/knowledge-base.md)创建/索引费用** | • **分层计费**：<br>  - 存储：按实际占用 GB/小时（旗舰版 0.012 元/GB/小时）<br>  - 检索并发：RCU 单位（1 RCU ≈ 50 QPS），按小时分段计费<br>  - Rerank 调用：按**初步召回总切片数 × Token 数 × 单价**计费（非最终返回数）<br>  - 向量化：按文档页数/时长计费（PDF/音视频） |
| **典型场景** | • 快速验证 RAG 效果（MVP 阶段）<br>• 轻量级智能客服问答（无需复杂知识治理）<br>• 已有知识库体系下，对特定子集做临时语义查询 | • 企业级知识中枢建设（如产品文档中心、法务合规库、医疗知识图谱）<br>• 多源异构数据（图文音视）统一索引与检索<br>• 需精细控制召回精度、排序策略、元数据过滤与成本优化的生产系统 |

---

## 适用场景建议

### ✅ 推荐选用 **Knowledge API** 当：
- 你已拥有多个**已发布状态的知识库**，仅需快速发起一次语义检索或端到端问答，不关心底层索引细节；
- 项目处于 PoC 或 MVP 阶段，追求最小接入成本，希望绕过知识库创建、上传、切片、重排配置等流程；
- 客户端具备稳定处理 SSE 流的能力（尤其问答场景），且能接受固定模型组合（`qwen3.6-plus` + 平台绑定 embedding/rerank）；
- 对知识库并发、存储容量、长期运维无定制需求，接受平台默认限流（25 QPS）与统一计费模型。

### ✅ 推荐选用 **Knowledge Base** 当：
- 你需要从零构建领域专属知识资产，涉及 PDF 技术手册、Excel 销售报表、产品截图、培训视频等**多模态原始数据**；
- 要求对 RAG Pipeline 全链路可控：例如调整 `初步向量检索 TopK`（1–100）、设置 `相似度阈值`（0.01–1.0）、启用 Query 改写、配置标签过滤或混合检索（向量+关键词）；
- 面临明确的**成本敏感性**，需通过关闭 Rerank、降低 TopK、精细化 RCU 配置等方式优化每千次请求成本；
- 需要与智能体（Agent）、工作流（Workflow）深度集成，或通过 SLS 日志实现全链路审计与效果归因；
- 系统要求高可用、高并发（>50 QPS）、大容量（TB 级存储），且可接受华北2（北京）地域限制。

> ⚠️ 注意：二者**非互斥关系，而是协同关系**。Knowledge API 的底层能力实际由 Knowledge Base 提供支撑——它本质是 Knowledge Base 的“标准化服务封装”。因此，在生产环境，常见模式是：  
> **用 Knowledge Base 构建、治理、优化知识资产 → 用 Knowledge API 实现业务侧轻量调用**。

---

## 开发者技术选型参考

| 决策问题 | Knowledge API | Knowledge Base | 建议动作 |
|----------|----------------|----------------|-----------|
| **是否需要上传原始文件？** | ❌ 不支持（仅接受已发布知识库 ID） | ✅ 支持 PDF/DOCX/图片/音视频等 | 若需导入原始资料，必须选 Knowledge Base |
| **是否需自定义 embedding/rerank 模型？** | ❌ 不可选（平台固化） | ✅ 可选多种模型，支持多模态场景 | 涉及专业领域（如法律文书、医学影像），优先 Knowledge Base |
| **是否需细粒度成本控制？** | ❌ 按请求计费，无 TopK/Rerank 成本拆解 | ✅ Rerank 费用 = 初步召回切片数 × Token × 单价，可精准压降 | 高频调用场景务必评估 Knowledge Base 的 RCU 与 Rerank 成本模型 |
| **是否需与 Agent/Workflow 图形化编排集成？** | ❌ 仅支持代码调用 | ✅ 控制台拖拽绑定「文档知识库」节点，支持权重、阈值可视化配置 | 低代码交付场景首选 Knowledge Base |
| **是否需跨地域部署？** | ✅ 接口调用无地域限制（但 [knowledge](../api/knowledge.md)Ids 必须属同一 workspace） | ❌ 仅支持华北2（北京）地域 | 若业务部署在新加坡/法兰克福，Knowledge Base 不可用，Knowledge API 是唯一选项 |
| **是否需审计每条检索的原始切片与分数？** | ✅ 返回 `score` 和 `metadata`，但无 pipeline_id 等追踪字段 | ✅ SLS 日志完整记录 `pipeline_id`、`nodes[].score`、`nodes[].text`、`request_id` | 合规强监管场景（如金融、政务）推荐 Knowledge Base + 日志审计 |

**一句话总结选型原则**：  
> **用 Knowledge Base “建好知识”，用 Knowledge API “用好知识”**。  
> 初期快速验证选 Knowledge API；中长期规模化、专业化、成本敏感型 RAG 应用，必须基于 Knowledge Base 构建知识底座，并通过 Knowledge API 或原生 SDK 进行服务化调用。

---  
*最后更新：2025年4月*

## 被对比主题页

- [knowledge](../api/knowledge.md)
- [knowledge base](../guides/knowledge-base.md)



# 知识能力方案对比：Knowledge API vs Knowledge Base

为帮助开发者在百炼平台上高效构建 RAG（[检索增强生成](../concepts/rag.md)）应用，本文系统对比两种核心知识能力方案：**Knowledge API**（面向服务调用的轻量级知识网关）与 **Knowledge Base**（面向全生命周期管理的完整知识库平台）。二者定位不同、能力分层、适用场景互补。本对比旨在厘清技术边界、明确选型依据，避免因能力误用导致开发返工或成本失控。

---

## 关键维度对比

| 维度 | Knowledge API | Knowledge Base |
|------|--------------|----------------|
| **本质定位** | **知识能力网关**：提供标准化 RESTful 接口，封装底层知识检索与问答逻辑，聚焦“即用即调”的服务消费 | **知识基础设施**：提供端到端知识管理平台，覆盖数据接入、向量化索引、[多模态](../concepts/multimodal.md)检索、效果调优、监控运维等全链路能力 |
| **输入格式** | - `/search`：纯文本 `query` 字符串（≤8192 字符）<br>- `/chat`：标准 OpenAI-style `messages` 数组（含 role/content），支持单轮或多轮对话结构 | - 支持多源异构数据：PDF/DOCX/MD/Excel/CSV/图片（JPG/PNG）、音视频（MP4/MOV/WAV）、网页链接等<br>- 可配置 Meta 信息抽取规则（如 `product_id`, `department`），作为结构化检索条件 |
| **输出格式** | - `/search`：JSON 格式，返回 `chunks` 数组（含 `content`, `score`, `source` 等字段）<br>- `/chat`：支持 SSE 流式响应（默认）或完整 JSON；输出含三阶段标记（`plan`/`tool_call`/`generate`），最终为自然语言回答 | - 控制台调试页：可视化召回切片列表（含相似度分数、来源文档高亮、Meta 属性）<br>- API 调用（`Retrieve`）：返回带 `metadata` 和 `score` 的结构化 `nodes` 数组<br>- 工作流/智能体集成：自动注入上下文至 LLM 提示词，不暴露原始切片细节 |
| **支持模型** | - 仅限知识增强型模型：<br> • `/chat` 默认 `qwen-plus`，可显式指定 `qwen-max`<br> • **不支持** `qwen-turbo`、`qwen-coder`、[多模态](../concepts/multimodal.md)模型（如 Qwen-VL）及第三方模型<br>- 不开放向量模型（如 `text-embedding-v1`）调用 | - 广泛支持：<br> • 千问全系：`qwen3`, `qwen2.5`, `qwen-max`, `qwen-plus`, `qwen-turbo`, `qwen-coder`, `qwq`, `long` 等<br> • [多模态](../concepts/multimodal.md)：`qwen-vl-max`, `qwen-vl-plus`, `qwen-vl-flash`, OCR 模型<br> • 第三方：`deepseek-r1`, `llama3.1`, `yi-large` 等（以控制台可选为准）<br>- 向量模型、重排（Rerank）模型、OCR 模型均可独立配置与计费 |
| **API 端点** | - 统一网关入口：<br> • 检索：`POST /api/v1/indices/knowledge/search`<br> • 问答：`POST /api/v2/apps/knowledge/chat`<br>- 基于业务空间（Workspace）URL 构造，强绑定 API Key | - 分层 API 体系：<br> • 管理类：`POST /v1/knowledge_bases`（创建）、`PUT /v1/knowledge_bases/{id}/sync`（同步）<br> • 检索类：`POST /v1/knowledge_bases/{id}/retrieve`（单库）、`POST /v1/retrieve`（多库混排）<br> • 高级能力：`POST /v1/knowledge_bases/{id}/query`（富文本搜索）、`POST /v1/knowledge_bases/{id}/video_search`（音视频）<br>- 支持 SDK 封装（Python/Java/Node.js） |
| **计费方式** | - **统一按调用次数计费**：<br> • `/search`：按请求次数计费（无论返回多少 chunk）<br> • `/chat`：按完整问答会话计费（含内部检索+LLM 生成），**不区分向量/Rerank/生成 [Token](../concepts/token.md)**<br>- 无知识库规格费用，无存储费用 | - **分项精细化计费**：<br> • **规格费**：标准版（0.03 元/小时）或旗舰版（0.2 元/RCU/小时）<br> • **存储费**：超出免费额度（标准版 100 GB）后按量计费<br> • **计算费**：<br>  ✓ 向量化：按上传文档 [Token](../concepts/token.md) 数计费<br>  ✓ Rerank：按初步召回切片总数 × 平均切片 [Token](../concepts/token.md) 数计费<br>  ✓ 问答生成：按 LLM 输入（含上下文）+ 输出 Token 计费<br> • 多知识库费用线性叠加 |
| **典型场景** | - 快速验证语义检索效果<br>- 构建轻量级客服机器人（无需复杂知识治理）<br>- 在已有应用中嵌入“一键问答”功能<br>- 对接低代码平台（如宜搭、钉钉宜搭）的简单知识插件 | - 企业级知识中枢建设（如 IT 运维知识库、销售产品手册库）<br>- 多模态知识应用（图文问答、会议纪要音视频检索）<br>- 需要精细调优的 RAG 应用（调整切片策略、相似度阈值、Meta 规则）<br>- 需要 SLS 日志监控、命中率分析、A/B 测试的生产级应用 |

---

## 适用场景建议

### ✅ 选择 **Knowledge API** 当：
- 你已拥有结构清晰、状态稳定的知识库（已在控制台发布），仅需快速调用其检索/问答能力；
- 开发周期紧张，希望绕过知识库创建、索引配置、效果调优等环节，直接集成 RESTful 接口；
- 应用对知识治理要求低（如临时项目、POC 演示、内部工具），无需版本管理、定时同步或 Meta 扩展；
- 团队熟悉 OpenAI-style `messages` 接口，且仅需 `qwen-plus`/`qwen-max` 等主流模型支撑。

### ✅ 选择 **Knowledge Base** 当：
- 你需要从零构建私有知识资产：上传原始文件、定义 Meta 字段、配置智能切分、设置相似度阈值；
- 业务涉及多模态数据（如产品说明书 PDF + 宣传图 + 培训视频），需统一索引与跨模态检索；
- 要求生产环境可观测：通过 SLS 日志分析慢查询、拒答率、召回准确率，并持续优化切片策略；
- 需要灵活调度资源：根据流量峰值动态升降旗舰版 RCU，或为不同知识库分配差异化规格；
- 计费敏感且需精细化控制：例如通过降低 `初步向量检索 TopK` 减少 Rerank 费用，或关闭非必要 Meta 抽取节省向量化成本。

> ⚠️ **重要提醒**：  
> - Knowledge API **不替代** Knowledge Base —— 它依赖后者已发布的知识库作为数据源。未创建/发布知识库时，Knowledge API 调用将返回空结果或 `404`。  
> - Knowledge Base 提供的 `Retrieve` API 与 Knowledge API 的 `/search` 功能存在重叠，但前者支持更细粒度参数（如 `filter`、`rerank_model`），后者更强调开箱即用与协议简洁性。

---

## 技术选型参考（面向开发者）

| 决策问题 | 推荐方案 | 理由说明 |
|----------|----------|----------|
| **是否需要上传/管理原始文档？** | Knowledge Base | Knowledge API 无文档上传接口，所有知识必须预先在 Knowledge Base 中完成入库与发布。 |
| **是否需支持图片/音视频/表格等多模态检索？** | Knowledge Base | Knowledge API 仅支持文本语义检索；Knowledge Base 原生支持图文理解、音视频帧提取与剧情解析。 |
| **是否需在控制台进行可视化调试与命中测试？** | Knowledge Base | Knowledge API 无前端调试界面，问题定位依赖日志与客户端模拟；Knowledge Base 提供实时 Query 测试沙箱。 |
| **是否需对接飞书/钉钉/OSS 等外部系统实现自动同步？** | Knowledge Base | Knowledge Base 支持文件连接器配置分钟级同步；Knowledge API 无同步能力，需自行实现定时任务调用 `Retrieve`。 |
| **是否追求最低接入成本与最快上线速度？** | Knowledge API | 无需创建知识库、无需配置索引、无需学习 Meta 规则，仅需构造 HTTP 请求即可调用，适合 MVP 快速验证。 |
| **是否需严格控制 RAG 各环节成本（向量/Rerank/生成）？** | Knowledge Base | Knowledge Base 提供各环节独立计费明细与调优参数（如 `top_k`, `similarity_threshold`），便于成本建模；Knowledge API 将全部成本封装为单一调用费。 |

> 💡 **最佳实践组合**：  
> 大多数生产级 RAG 应用采用 **Knowledge Base + Knowledge API 混合架构**：  
> - 使用 **Knowledge Base** 完成知识资产建设、多模态索引、效果调优与监控；  
> - 使用 **Knowledge API** 作为对外服务统一入口，简化下游应用集成复杂度，提升网关层可观测性与限流管控能力。  
> 此模式兼顾灵活性与工程效率，是百炼平台推荐的成熟落地范式。

## 被对比主题页

- [knowledge](../api/knowledge.md)
- [knowledge base](../guides/knowledge-base.md)



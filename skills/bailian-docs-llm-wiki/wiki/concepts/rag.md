# 检索增强生成

检索增强生成（Retrieval-Augmented Generation，RAG）是一种将大语言模型（LLM）的生成能力与外部知识源的精准检索能力相结合的技术范式。它通过在生成前动态检索相关知识片段，并将其作为上下文注入提示词，显著提升模型在事实性、时效性和领域专业性任务上的准确性与可靠性。

## 在百炼平台的不同场景中，这个概念如何使用

在百炼平台，RAG 不是抽象技术概念，而是已封装为开箱即用的核心能力，贯穿多个产品模块：

- **知识库（Knowledge Base）**：作为 RAG 的底层基础设施，支持文档、表格、图片、音视频等多模态数据的自动解析、向量化、语义检索与重排。开发者无需部署向量数据库或训练嵌入模型，所有检索逻辑由平台统一托管。
- **知识检索与问答（Knowledge API）**：提供 `/search`（纯检索）和 `/chat`（端到端问答）两类接口。前者返回结构化文本切片（chunk），供自定义生成逻辑调用；后者内置规划→工具调用→生成三阶段流式 pipeline，直接输出最终答案。
- **智能体与工作流应用（Application）**：在应用配置中一键绑定知识库，启用“必定调用”或“按需触发”模式，RAG 结果自动注入系统提示词（如 `{result}` 占位符），与模型生成无缝协同。
- **框架集成（LlamaIndex / Spring AI Alibaba）**：通过官方 SDK 将百炼云端知识库接入主流开发框架，复用 `DashScopeCloudIndex` 或 `DashScopeDocumentRetriever` 等组件，快速构建生产级 RAG 应用。
- **多端业务集成（Website / 企业微信 / 钉钉等）**：AppFlow 提供零代码 RAG 接入路径——上传文件 → 创建知识库 → 关联应用 → 发布，即可在网站悬浮窗、企微机器人等渠道获得知识增强的对话体验。

## 关键参数和配置

RAG 效果可通过以下关键参数精细调控（均在控制台或 API 中显式配置）：

| 参数名 | 作用域 | 类型 | 常用值 | 说明 |
|--------|--------|------|--------|------|
| `retrieval_top_k` / `top_k` | 知识库、API、框架 | int | `3`–`5`（默认） | 最终送入大模型的检索片段数量（经重排+阈值过滤后）。值过大会增加噪声，过小易丢失关键信息。 |
| `similarity_threshold` / `score_threshold` | 知识库、API、应用配置 | float | `0.3`–`0.6` | 过滤低相关性切片的相似度阈值。建议结合业务测试调整，避免漏召或误召。 |
| `initial_retrieval_top_k` | 知识库高级设置 | int | `50`（默认） | 向量召回阶段的初步切片数，影响重排成本与精度平衡。降低可节省费用，但可能牺牲长尾召回率。 |
| `chunk_size` / `chunk_overlap` | **仅本地 RAG 场景** | int | `512`/`128` | 文档切分粒度与重叠长度，适用于基于百炼 Embedding API 的自建轻量 RAG 方案。 |
| `enable_query_rewrite` | 知识库创建时 | bool | `True` | 开启多轮对话改写，自动补全指代（如“它”、“上文提到的”），提升上下文感知能力。 |

> ⚠️ 注意：所有云端 RAG 能力均**不支持自定义嵌入模型、切分逻辑或向量引擎**，全部依赖百炼托管的向量模型（如 `gte-base` 嵌入 + `gte-rerank` 重排）。

## 面向开发者，简洁实用

- ✅ **快速启动**：控制台创建知识库 → 上传 PDF/DOCX/TXT → 在应用中绑定 → 发布 → 调用 `/chat` 接口，5 分钟完成 RAG 上线。
- ✅ **调试优先**：使用 `/search` 接口独立验证检索质量（检查 `score` 和 `content`），再接入生成逻辑，避免混淆检索与生成问题。
- ✅ **参数调优口诀**：  
  - 先调 `similarity_threshold` 控制精度（高阈值 = 更严格，低召回）；  
  - 再调 `retrieval_top_k` 平衡信息量与噪声（通常 `3`–`5` 最佳）；  
  - 最后观察 `latency` 和 `response_code` 日志（开通 SLS 监控），定位瓶颈在检索还是生成。
- ✅ **避坑提醒**：  
  - `workspaceId` 必须与 API Key 所属业务空间完全一致，不可用 Project ID 替代；  
  - `/chat` 接口不接受 `top_k` 参数，其召回策略由绑定的知识应用配置决定；  
  - 音视频类知识库不支持新增切片，仅支持删除；  
  - 多知识库联合检索需在应用配置中显式设置权重，否则默认等权融合。

## 关联主题页

- [knowledge](../api/knowledge.md)
- [knowledge base](../guides/knowledge-base.md)
- [frameworks](../api/frameworks.md)
- [application use cases](../guides/application-use-cases.md)
- [application support](../guides/application-support.md)



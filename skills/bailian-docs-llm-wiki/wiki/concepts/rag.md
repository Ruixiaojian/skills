# 检索增强生成

检索增强生成（Retrieval-Augmented Generation，RAG）是一种将大语言模型（LLM）的生成能力与外部知识源的精准检索能力相结合的技术范式。它通过在模型推理前动态召回相关上下文片段，并将其注入提示词（Prompt），使模型能在私有、领域专属或时效性强的知识基础上生成更准确、可溯源、抗幻觉的回答。

## 在百炼平台的不同场景中，这个概念如何使用

在百炼平台中，RAG 不是单一接口，而是贯穿多个能力层的协同工作模式，核心围绕**知识库**这一基础设施展开，支持三种主流集成路径：

- **应用内嵌 RAG（推荐用于生产级智能体/工作流）**  
  在智能体或工作流应用配置页中直接绑定已创建的知识库，设置“相似度阈值”“权重”和调用策略（如“必定调用”）。工作流中拖入“知识库节点”，配置 `TopK` 和输入变量（如 `query`），再连接至大模型节点；模型提示词中通过 `{result}` 引用召回内容。该方式支持多轮对话改写、Agentic 规划搜索及引用溯源。

- **独立服务形态（适合快速验证与 API 集成）**  
  通过控制台“知识检索”或“知识问答”标签页发布统一服务：可跨最多 15 个知识库联合检索，配置混合检索（向量+关键词）、Rerank 模型（如 `qwen3-rerank`）、拒答与防泄漏策略。发布后通过标准化 HTTP API 调用：
  - 检索：`POST /api/v1/indices/knowledge/search` → 返回结构化切片；
  - 问答：`POST /api/v2/apps/knowledge/chat` → 默认 SSE 流式响应，含 planning、tool calling、generation 三阶段输出。

- **框架集成（面向开发者快速构建）**  
  - **LlamaIndex**：调用 `DashScopeCloudIndex.from_documents()` 构建云端知识库，通过 `SimilarityPostprocessor` + `DashScopeRerank` 控制召回与重排，最终 `query_engine.query()` 触发端到端 RAG。
  - **Spring AI Alibaba**：使用 `DashScopeDocumentRetriever` 按 `INDEX_NAME` 检索上下文，并自动注入提示词交由 `qwen-max` 等模型生成；或通过 `DashScopeAgent` 调用已发布的智能体应用（隐式封装 RAG 逻辑）。

> ⚠️ 注意：所有 RAG 路径均依赖知识库预置——知识库必须部署在华北2（北京）地域，且需完成文档上传、解析、向量化与索引构建；不支持裸知识库 ID 直接调用，问答接口必须传入已绑定知识库的 `app_id`。

## 关键参数和配置

| 参数 | 所属层级 | 类型 | 说明 | 典型值 | 备注 |
|------|----------|------|------|--------|------|
| `retrieval_top_k` / `top_k` | 应用层 / API 层 | integer | 初始召回切片数量（向量/关键词双路） | `3`–`10` | 过高增加 Token 开销，过低影响召回完整性；最大支持 100 |
| `similarity_threshold` | 应用层 / 知识库层 | float (0.01–1.0) | Rerank 后过滤阈值，仅保留得分高于此值的切片 | `0.4`–`0.6` | 值过高易漏召，过低引入噪声；纯文本知识库专用 |
| `max_retrieved_chunks` | 应用层 | integer | 最终传递给大模型的上下文切片总数 | `1`–`20` | 控制 Prompt 长度与成本，建议 ≤10 |
| `weight` | 多知识库混排 | float | 知识库在联合检索中的相对优先级 | `1.0`, `2.0` | 权重越高，同 Query 下该库切片排序越靠前 |
| `tags` | 知识库层 | string array | 单文件最多 32 个标签，用于精准范围过滤 | `["finance", "2024Q3"]` | 支持 `AND` 语义匹配，提升高干扰场景精度 |
| `metadata` 字段 | 索引层 | key-value | 在切片索引时注入结构化信息（如 `filename`, `date`, `author`） | — | 实现“先过滤、再检索”，降低误召率 |

> ✅ 提示：参数生效位置不同——`similarity_threshold` 和 `weight` 在知识库或应用配置页设置；`top_k` 和 `stream` 在 API 请求 Body 或 Header 中指定；`chunk_size`/`chunk_overlap` 仅在知识库创建时一次性配置，不可修改。

## 面向开发者，简洁实用

- **起步最快**：控制台创建知识库 → 上传 PDF/DOCX/TXT → 发布“知识问答”服务 → 调用 `/api/v2/apps/knowledge/chat`，只需 `workspaceId` + `API Key` + `app_id` + `messages`。
- **调试关键**：开启 SLS 日志监控，关注 `data.nodes[]` 字段确认召回质量；流式响应需按 `event: chunk` 解析，末尾 `event: done` 包含完整结果与 `docReferences`。
- **避坑指南**：
  - 域名必须含 `workspaceId`，API Key 必须归属该 workspace，否则 `401`；
  - 知识库类型（文档/图片/表格）决定可用模型：纯文本仅支持 `qwen3-rerank`，多模态知识库才可用 `VL-Max`；
  - 文件上传后需等待解析完成（1–6 分钟），未就绪时检索返回空；
  - 免费额度覆盖全部 RAG 场景，但向量模型与 Rerank 模型按 Token 单独计费，非包含在知识库规格费中。

RAG 的本质是“让模型知道它该知道的”。在百炼，你只需聚焦业务知识——平台负责高效检索、可信增强、稳定生成。

## 关联主题页

- [knowledge](../api/knowledge.md)
- [knowledge base](../guides/knowledge-base.md)
- [frameworks](../api/frameworks.md)
- [application use cases](../guides/application-use-cases.md)
- [data connection overview](../guides/data-connection-overview.md)



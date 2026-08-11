# 检索增强生成

检索增强生成（Retrieval-Augmented Generation，RAG）是百炼平台的核心能力范式，指在大模型生成回答前，先从私有知识库或外部数据源中检索相关上下文片段，并将这些高相关性信息作为提示（Prompt）的一部分注入模型推理过程，从而显著提升回答的准确性、时效性与领域专业性。

## 在百炼平台的不同场景中，这个概念如何使用

RAG 并非单一接口，而是贯穿百炼多层能力的工程化模式，在以下典型场景中以不同形态落地：

- **知识库问答（`/api/v2/apps/knowledge/chat`）**：最简化的 RAG 封装。用户输入问题后，平台自动完成「语义检索 → 排序精调 → 上下文注入 → 大模型生成」全流程，返回结构化 SSE 流式响应。适用于快速上线客服、FAQ 等垂类问答应用。

- **知识检索（`/api/v1/indices/knowledge/search`）**：提供 RAG 的“检索侧”原子能力。开发者可自主控制召回策略（如多库联合、标签过滤、相似度阈值），获取原始文本切片（chunk），再结合自定义 Prompt 工程与模型调用构建端到端 RAG 流水线。

- **数据连接器（Data Connector）**：扩展 RAG 的数据边界。支持对接 MySQL、PostgreSQL、OSS、语雀等结构化与非结构化数据源，部分连接器（如数据库）还支持原生 SQL 查询，实现“检索 + 执行 + 生成”的混合增强。

- **框架集成（LlamaIndex / Spring AI Alibaba）**：面向代码优先的开发者。通过 `DashScopeCloudIndex` 或 `DashScopeDocumentRetriever` 封装云端知识库访问逻辑，复用百炼向量模型与重排能力，同时保留本地 Prompt 编排、后处理（如 `SimilarityPostprocessor`）和流式查询控制权。

- **智能体与工作流应用**：RAG 作为可插拔节点嵌入 Agentic 流程。在工作流中显式添加“知识库节点”，其输出（`{result}`）可被后续大模型节点直接引用；智能体则可通过工具调用（如 `searchKnowledgeBase`）按需触发检索，实现动态上下文感知。

- **[多模态](multi-modal.md) RAG**：支持图像、音视频等非文本数据的语义检索与理解。例如上传含图表的 PDF，经 `qwen3-vl-embedding` 向量化后，用户提问“图3中的趋势是什么？”，系统可精准召回并解析对应图表区域。

## 关键参数和配置

RAG 效果高度依赖以下可调参数，按作用层级分类：

| 类别 | 参数名 | 说明 | 典型取值 | 生效位置 |
|------|--------|------|----------|----------|
| **检索控制** | `top_k` / `similarity_top_k` | 向量检索阶段召回的原始切片数 | `10–50`（默认 `50`） | `/search` API、LlamaIndex、知识库配置页 |
| | `rerank_top_k` | 重排模型输出的最终有效切片数（注入 Prompt 的上下文数量） | `3–10`（默认 `3`） | `/chat` API、知识库配置页、框架后处理器 |
| | `similarity_threshold` | 过滤低相关性切片的相似度阈值 | `0.3–0.7`（数值越高越严格） | 知识库配置页、LlamaIndex `SimilarityPostprocessor` |
| **数据源控制** | `tags` | 按业务标签过滤知识库或文件类目 | `["finance", "2024Q3"]` | `/search` 请求体、API 调用、数据连接器工具参数 |
| | `knowledge_base_ids` | 显式指定参与检索的知识库 ID 列表 | `["kb-xxx", "kb-yyy"]` | `/search` 请求体、工作流节点配置 |
| **生成控制** | `stream` | 是否启用流式响应（影响延迟与前端体验） | `true` / `false` | `/chat` API、框架 `query_engine.query()` |
| | `temperature` | 控制生成结果的随机性（仅本地 RAG 或自定义调用时生效） | `0.1–0.7` | 本地 Gradio 应用、[OpenAI 兼容接口](openai-compatible-api.md) |

> ⚠️ 注意：  
> - `/chat` 接口不接受 `model` 字段——生成模型由业务空间内知识应用的部署配置决定，强行传入将被忽略；  
> - 所有 RAG 场景均强制要求知识库处于「已发布」状态，草稿或下线状态不可见；  
> - 北京地域（`cn-beijing`）为唯一支持地域，URL 中地域字段不可替换。

## 面向开发者，简洁实用

- **快速验证**：先用控制台创建知识库 → 上传 1–2 个测试文档 → 在「知识问答」页试问，观察召回质量与回答准确性；  
- **调试技巧**：开启 `/search` 接口查看原始召回切片，对比 `score` 与 `content`，若相关性低，优先调低 `similarity_threshold` 或检查文档切分粒度；  
- **性能优化**：`top_k` 过大会显著增加 Rerank 费用（按 token 计费），建议先设为 `20`，再根据 `rerank_top_k` 实际需要逐步收窄；  
- **安全边界**：所有知识库内容默认仅对当前业务空间可见，无需额外鉴权；敏感数据请勿上传至共享 workspace；  
- **错误排查**：若 `/search` 返回空结果，请确认：① 知识库已发布；② `workspaceId` 正确；③ 查询词未被过度过滤（尝试更泛关键词）。

## 关联主题页

- [knowledge](../api/knowledge.md)
- [knowledge base](../guides/knowledge-base.md)
- [frameworks](../api/frameworks.md)
- [data connection overview](../guides/data-connection-overview.md)
- [application use cases](../guides/application-use-cases.md)
- [use cases](../guides/use-cases.md)



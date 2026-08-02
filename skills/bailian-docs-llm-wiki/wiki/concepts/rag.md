# 检索增强生成

检索增强生成（Retrieval-Augmented Generation，RAG）是一种将大语言模型（LLM）与外部知识源动态结合的技术范式：在生成回答前，先从结构化或非结构化[知识库](knowledge-base.md)中检索相关片段，再将检索结果作为上下文注入模型提示（[prompt](../guides/prompt.md)），从而提升回答的准确性、时效性与领域专业性。它有效缓解了大模型幻觉、知识固化和私域数据不可用等问题，是百炼平台实现可信、可控、可扩展AI应用的核心技术路径。

## 在百炼平台的不同场景中，这个概念如何使用

RAG 在百炼平台不是单一接口，而是贯穿多个能力层的协同工作模式，开发者可根据需求选择不同抽象层级：

- **低代码/无代码集成（推荐入门）**：在「智能体应用」或「工作流应用」中一键启用[知识库](knowledge-base.md)，配置 `retrieval_mode=must_call` 即可自动触发检索→重排→生成全流程；适用于企业微信、钉钉、网站等渠道的AI助手快速上线。
- **API 直接调用（精细控制）**：
  - 使用 `knowledge/search` 接口执行纯检索（召回+重排），获取带 `score`、`metadata` 的文本切片，再自行拼装 [prompt](../guides/prompt.md) 调用 `qwen-max` 等模型；
  - 使用 `knowledge/chat` 接口启用端到端问答，服务内部自动完成 Query 改写、多库联合检索、SSE 流式三阶段（planning → tool calling → generation），适合需上下文感知与多轮交互的场景。
- **框架集成（工程化落地）**：
  - LlamaIndex：通过 `DashScopeCloudIndex` 绑定云端[知识库](knowledge-base.md)，用 `similarity_top_k` 和 `DashScopeRerank` 控制召回与排序，再接入自定义 LLM；
  - Spring AI Alibaba：使用 `DashScopeDocumentRetriever` 实现 Java 应用的知识检索，无缝对接 `ChatClient`。
- **混合部署（定制化需求）**：本地 RAG 方案（如 `local_rag.zip`）将文档切分与向量化置于本地，仅调用百炼 API 进行生成，适用于需自主控制嵌入模型或敏感数据不出域的场景。

> ⚠️ 注意：所有 RAG 能力均依赖已发布（Published）状态的知识库，草稿或禁用状态不可见；知识库仅支持华北2（北京）地域，跨地域调用将失败。

## 关键参数和配置

| 参数 | 作用 | 取值建议 | 生效位置 |
|------|------|----------|----------|
| `top_k` / `retrieval_top_k` | 最终返回给生成模型的切片数量上限 | `3–5`（平衡精度与成本），最大 `20` | `knowledge/search`、`knowledge/chat`、应用配置、LlamaIndex `similarity_top_k` |
| `score_threshold` / `similarity_threshold` | 过滤重排后低分切片的相似度阈值 | `0.3–0.6`（过高易漏召，过低引入噪声） | `knowledge/chat` 请求体、应用配置、Spring AI Alibaba |
| `initial_retrieval_top_k` | 向量初步召回数（影响 Rerank 费用） | `50`（默认），按需下调以降本 | 知识库控制台「检索设置」 |
| `knowledge_base_ids` | 指定参与检索的知识库 ID 列表 | 最多 `15` 个，支持标签过滤 | `knowledge/chat` 请求体、`knowledge_config` 字段 |
| `stream` | 启用 SSE 流式响应（问答）或逐 token 流式（基础 API） | `true`（默认），设为 `false` 获取完整 JSON | `knowledge/chat`、Assistant API |
| `incremental_output` | 流式下仅返回新增 token（非累积重传） | `true`（需配合 `stream=true`） | Assistant API |

> 💡 提示：Rerank 费用取决于**初步召回总切片数**（`initial_retrieval_top_k × 知识库数量`），而非最终 `top_k`；关闭 Rerank 可显著降本，但排序质量下降。

## 面向开发者，简洁实用

- ✅ **快速验证**：控制台创建知识库 → 上传 PDF/DOCX → 在智能体应用中绑定并启用 → 发布后直接测试，5 分钟完成端到端 RAG。
- ✅ **调试技巧**：开启 SLS 日志后，检索日志中 `response_body.data.nodes[]` 包含每个切片的 `score`、`text`、`metadata`，可用于判断召回质量；若结果不准，优先检查 `score_threshold` 和 `initial_retrieval_top_k`。
- ✅ **性能优化**：高并发场景下，旗舰版知识库需配置足够 RCU（1 RCU ≈ 50 QPS）；对延迟敏感场景（如未认证公众号），选用 `qwen-turbo` 并精简 Prompt。
- ❌ **避坑指南**：
  - 不要硬编码通用域名（如 `maas.aliyuncs.com`），必须用 `https://{workspaceId}.cn-beijing.maas.aliyuncs.com` 构造 Base URL；
  - 文件后缀必须小写（如 `pdf`，非 `PDF`），否则返回错误码 `140010`；
  - 多知识库联合检索时，Query 向量化与 Rerank 调用费用按知识库数量倍增，慎用过多知识库。

RAG 不是“开箱即用”的黑盒，而是需要根据业务精度、延迟、成本三要素权衡配置的工程实践。百炼平台提供从控制台到 API、从框架到本地的全栈支持，让开发者聚焦于知识组织与业务逻辑，而非底层向量基建。

## 关联主题页

- [knowledge](../api/knowledge.md)
- [knowledge base](../guides/knowledge-base.md)
- [frameworks](../api/frameworks.md)
- [application use cases](../guides/application-use-cases.md)
- [application support](../guides/application-support.md)



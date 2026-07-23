# 检索增强生成

检索增强生成（Retrieval-Augmented Generation，简称 RAG）是一种将大语言模型（LLM）与外部知识源动态结合的技术范式：在生成回答前，系统先根据用户查询语义检索相关知识片段，再将检索结果作为上下文注入模型提示（[prompt](../guides/prompt.md)），引导模型生成更准确、可溯源、时效性强的响应。

在百炼平台中，RAG 不是单一接口或模型，而是贯穿知识库、数据连接、智能体应用与框架集成的一套协同能力体系，其核心目标是让大模型“有据可依”，而非仅依赖参数内化知识。

## 在百炼平台的不同场景中，这个概念如何使用

- **知识库问答（/api/v2/apps/[knowledge](../api/knowledge.md)/chat）**：最典型的端到端 RAG 流程。平台自动完成「查询理解 → 多知识库联合检索（向量+关键词+重排）→ 工具调用（Retrieve）→ 上下文拼接 → LLM 生成」，支持 SSE [流式输出](streaming-output.md)，并返回 `docReferences` 等结构化溯源信息。  
- **数据连接（Data Connection）**：为 RAG 提供多样化知识源。平台托管型（如 PDF/Excel）自动构建向量索引；流处理型（如 MySQL/OSS/语雀）则按需实时检索，实现“不入库、可检索”的轻量 RAG。二者均可在智能体或工作流中直接绑定为知识源。  
- **智能体与工作流应用**：RAG 是知识增强的关键开关。可在应用配置中启用“必定调用知识库”，并设置召回数量、相似度阈值、权重等策略；也可通过 `knowledge_sources` 参数在 API 请求中动态指定知识库或数据连接器 ID。  
- **框架集成（LlamaIndex / Spring AI Alibaba）**：面向开发者提供代码级 RAG 构建能力。LlamaIndex 封装云端索引构建与查询引擎；Spring AI Alibaba 提供 `DashScopeDocumentRetriever`，支持显式控制模型（如 `qwen-plus`）、检索参数（`top_k`, `similarity_cutoff`）及流式响应，适用于定制化 RAG 应用开发。  
- **本地 RAG 应用（Python SDK）**：面向高级场景，支持完全自主的文档切分、本地嵌入模型（如 GTE）、自定义检索逻辑，适用于对数据主权、延迟或成本有强约束的私有化部署。

> ⚠️ 注意：所有 RAG 能力均运行于华北2（北京）地域，且必须在业务空间（workspace）中完成知识库/数据连接器的创建与激活，否则请求将静默失败或返回空结果。

## 关键参数和配置

以下参数直接影响 RAG 效果与成本，建议按场景显式配置（默认值可能不满足精度要求）：

| 参数名 | 说明 | 典型取值 | 所属层级 | 备注 |
|--------|------|----------|----------|------|
| `top_k` / `similarity_top_k` | 初步向量/关键词召回的切片数 | `10–50` | 检索层 | 值越大，重排 [Token](token.md) 消耗越高；混合检索时需兼顾两者 |
| `max_retrieval_count` / `max_retrieved_nodes` | 最终送入 LLM 的上下文切片上限 | `3–10` | 检索层 | 直接影响生成质量与 [Token](token.md) 成本，推荐从 `5` 开始调优 |
| `similarity_threshold` / `similarity_cutoff` | 重排后过滤低分切片的阈值 | `0.4–0.7` | 重排层 | 过高易漏召关键信息，过低引入噪声；建议结合日志分析调整 |
| `tags` | 按标签过滤检索范围（支持 `AND`/`OR` 逻辑） | `["faq", "v2.3"]` | 检索层 | 用于多版本、多业务线知识隔离，需在知识库创建时预设 |
| `model_name` / `withModel()` | 生成阶段使用的 LLM | `"qwen-plus"`, `"qwen3.5-plus"` | 生成层 | `/chat` 接口不可覆盖，但框架集成与本地应用可自由指定 |
| `stream` | 是否启用 SSE 流式响应 | `true`（默认） | 传输层 | 仅 `/chat` 接口支持；流式下可实时获取 `thoughts` 和 `docReferences` |

> 💡 提示：Rerank 模型（如 `qwen3-rerank`）费用取决于初步召回总切片数（即 `top_k` 之和），而非最终返回数；多知识库联合检索时，该成本线性增长，请合理设置 `top_k`。

## 面向开发者，简洁实用

- **快速验证**：用控制台创建一个文件知识库 → 绑定至智能体应用 → 启用“必定调用” → 发起测试对话，观察 `docReferences` 字段是否返回非空数组。  
- **调试必查**：若 RAG 返回空或无关内容，优先检查：① 知识库状态是否为 `ACTIVE`；② 查询文本是否触发有效召回（调用 `/search` 接口验证）；③ `similarity_threshold` 是否过高；④ 日志中 `response_body.data.nodes[]` 是否为空。  
- **性能优化**：高频场景建议关闭 Rerank（设 `rerank_enabled: false`）并调高 `similarity_threshold`；对精度敏感场景，启用 hybrid 检索 + `qwen3-rerank` 并将 `top_k` 设为 `30–50`。  
- **安全边界**：所有知识库与数据连接器均按业务空间隔离，API Key 无跨空间访问权限；元数据（Meta）抽取规则在知识库创建后不可修改，请务必在初始化阶段审慎配置。  
- **计费意识**：RAG 成本 = 检索侧（向量化 + Rerank） + 生成侧（LLM 输入/输出 [Token](token.md)）。避免盲目增大 `top_k` 或 `max_retrieval_count`，应以实际召回质量为准。

## 关联主题页

- [knowledge](../api/knowledge.md)
- [knowledge base](../guides/knowledge-base.md)
- [frameworks](../api/frameworks.md)
- [data connection overview](../guides/data-connection-overview.md)
- [application use cases](../guides/application-use-cases.md)



# 检索增强生成

检索增强生成（Retrieval-Augmented Generation，RAG）是一种将大语言模型（LLM）与外部知识源动态结合的技术范式：在生成回答前，先从私有或结构化知识库中检索相关片段，再将检索结果作为上下文注入模型提示（[prompt](../guides/prompt.md)），从而提升回答的准确性、时效性与领域专业性。它本质是“检索 + 生成”的两阶段协同流程，而非单纯依赖模型参数内化知识。

## 在百炼平台的不同场景中，这个概念如何使用

在百炼平台，RAG 不是单一接口，而是贯穿多个能力层的横切架构，开发者可根据需求选择不同抽象层级的实现方式：

- **知识库（Knowledge Base）**：最典型的 RAG 实现。通过控制台或 API 创建知识库后，平台自动完成文档解析、智能切分、向量化、召回、重排与生成四阶段流水线。支持多模态（文本/图片/音视频）、多知识库联合检索、双轨模式（极速单轮 vs 多轮 Agentic 规划），并可精细控制相似度阈值、TopK 数量等关键环节。

- **[knowledge](../api/knowledge.md) API 服务**：面向自定义 RAG 流程的轻量级能力。`/api/v1/indices/knowledge/search` 提供纯语义检索，返回结构化 chunk 列表，供开发者自行拼装 [prompt](../guides/prompt.md)；`/api/v2/apps/knowledge/chat` 则封装完整 RAG 流程（规划 → 工具调用 → 生成），支持 SSE [流式输出](streaming-output.md)，适用于对话式问答场景。

- **数据连接（Data Connection）**：为 RAG 注入实时/动态数据源。文件类连接器（PDF/Excel）构建静态向量索引；数据库/OSS/语雀等流处理连接器则通过工具调用（如 `querySQL`、`searchYuQueDoc`）实现运行时检索，使 RAG 具备“活数据”能力。

- **框架集成（LlamaIndex / Spring AI Alibaba）**：降低工程门槛。LlamaIndex 提供 `DashScopeCloudIndex` 抽象，一键对接云端知识库；Spring AI Alibaba 的 `DashScopeDocumentRetriever` 支持直接检索知识库，并灵活切换生成模型（如 `qwen-plus` 或 `qwen-max`），适合 Java/Spring 生态快速落地。

- **应用集成（Website / 企业微信 / 钉钉等）**：RAG 作为开箱即用的能力模块嵌入业务渠道。在应用配置页绑定知识库后，平台自动注入检索逻辑——支持“必定调用”或“按需触发”，并可设置召回片段数与相似度阈值，无需修改渠道侧代码。

- **应用评测（Application Evaluation）**：RAG 效果可量化验证。评测集可基于知识库自动生成，评估器（LLM 或 Code）能对检索相关性、答案事实性、引用准确性等维度打分，支撑 RAG 系统的持续调优闭环。

## 关键参数和配置

RAG 行为由以下核心参数控制，不同入口配置位置略有差异，但语义一致：

| 参数名 | 作用 | 常见取值 | 配置位置示例 |
|--------|------|----------|--------------|
| `top_k` / `max_retrieved_count` | 控制最终送入大模型的检索片段数量 | 1–20（推荐 3–5） | [knowledge](../api/knowledge.md) API 的 `top_k`；知识库控制台的「最大召回数量」；LlamaIndex 的 `similarity_top_k` |
| `similarity_threshold` | 过滤重排后低相关性片段，避免噪声干扰 | 0.01–1.0（默认约 0.3–0.5） | 知识库控制台「相似度阈值」；Spring AI Alibaba 的 `retriever.threshold` |
| `rerank_top_k` / `initial_top_k` | 控制送入重排模型的候选片段总数（影响费用与精度） | 1–100（推荐 20–50） | 知识库控制台「初步向量 TopK」；LlamaIndex 的 `DashScopeRerank.top_n` |
| `query_rewrite_enabled` | 是否启用多轮对话中的 Query 改写（提升长尾问题召回率） | `true` / `false` | 知识库创建时开启，**创建后不可修改** |
| `model_name` | 指定 RAG 中的生成模型，直接影响响应质量与延迟 | `qwen-plus`（平衡）、`qwen-turbo`（低延迟）、`qwen-max`（高精度） | [knowledge](../api/knowledge.md) API 透明调度；框架中显式指定；应用配置页下拉选择 |

> ⚠️ 注意：`workspaceId` 和 `API Key` 是所有 RAG 能力的统一鉴权基础，必须正确配置；知识库仅在华北2（北京）地域可用，跨地域调用将失败。

## 面向开发者，简洁实用

- **快速验证**：用控制台创建一个标准版知识库 → 上传 1–2 个 PDF → 绑定到智能体应用 → 发布后直接测试问答，5 分钟可见效果。
- **调试技巧**：启用知识库「命中测试」查看原始召回片段；在应用观测中追踪 `request_id`，结合 SLS 日志分析 `response_body.data.nodes[]` 确认哪些 chunk 被实际用于生成。
- **性能优化**：若响应慢，优先检查 `top_k` 是否过大（>8）、`similarity_threshold` 是否过低（<0.2）；高并发场景选用旗舰版知识库并调高 QPS。
- **安全边界**：RAG 默认启用拒答与防泄漏策略，敏感信息不会被检索或生成；如需更强控制，可在 Prompt 中添加明确约束（如 `"不回答未在知识库中明确提及的内容"`）。
- **避坑提醒**：Meta 信息抽取、Query 改写功能仅在知识库创建时配置，**创建后无法修改**；`knowledge/search` 接口不支持流式，`stream` 参数仅对 `/chat` 接口有效。

## 关联主题页

- [knowledge](../api/knowledge.md)
- [knowledge base](../guides/knowledge-base.md)
- [frameworks](../api/frameworks.md)
- [data connection overview](../guides/data-connection-overview.md)
- [application evaluation](../guides/application-evaluation.md)
- [application use cases](../guides/application-use-cases.md)



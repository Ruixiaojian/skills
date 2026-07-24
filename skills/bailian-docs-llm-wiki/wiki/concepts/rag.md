# 检索增强生成

检索增强生成（Retrieval-Augmented Generation，简称 RAG）是一种将大语言模型（LLM）与外部知识源动态结合的技术范式：在模型生成响应前，先从结构化或非结构化知识库中语义检索相关片段，并将其作为上下文注入提示词，从而提升回答的准确性、事实性、专业性与可溯源性。该技术有效缓解大模型幻觉、知识陈旧和领域泛化不足等问题。

## 在百炼平台的不同场景中，这个概念如何使用

在百炼平台，RAG 不是单一功能，而是贯穿多个能力层的横切架构，开发者可根据需求选择不同抽象层级的实现方式：

- **零代码应用层（控制台）**：在智能体或工作流应用中直接绑定已创建的知识库，配置相似度阈值、权重、TopK 等参数；平台自动完成查询改写、多路检索（向量+关键词）、Rerank 排序，并将结果注入模型提示词。适用于快速上线业务问答机器人。
  
- **托管服务层（Knowledge API）**：通过 `/api/v2/apps/knowledge/chat`（知识问答）或 `/api/v1/indices/knowledge/search`（知识检索）等 RESTful 接口调用，无需管理索引生命周期。平台自动完成端到端 RAG 流程（规划→检索→生成），支持 SSE 流式响应，适合需快速集成、轻运维的 SaaS 场景。

- **基础设施层（Application Component API）**：通过 `CreateIndex`、`SubmitIndexJob`、`Retrieve` 等 OpenAPI 手动构建和管理知识库全生命周期，支持自定义文档解析、切片策略、元数据过滤及 Chunk 级精细操作。适用于对数据主权、索引质量、成本控制有强要求的企业级场景。

- **框架集成层（LlamaIndex / Spring AI Alibaba）**：使用官方 SDK 将百炼知识库作为远程检索后端（如 `DashScopeCloudIndex` 或 `DashScopeDocumentRetriever`），复用本地框架的 Query Engine、Postprocessor、Agent 编排能力，实现跨云/混合部署的 RAG 应用开发。

- **数据连接层（Data Connection）**：将文件、表格、数据库、OSS、语雀等外部数据源接入后，自动构建向量索引或提供实时工具调用（如 `searchSQL`），使 RAG 能力延伸至动态、结构化、[多模态](multi-modal.md)数据源，支撑“检索增强 + 工具调用”的 Agentic RAG 架构。

## 关键参数和配置

RAG 效果与成本高度依赖以下关键参数，需按场景合理配置：

| 参数 | 作用域 | 类型 | 常用范围 | 说明 |
|------|--------|------|----------|------|
| `top_k` / `max_retrieve_count` | 知识问答、工作流节点、Retrieve API | integer | 1–20 | 最终送入大模型的文本切片数量。增大可提升答案完整性，但易触发输入 [Token](token.md) 超限（尤其长文档）。建议从 3–5 开始调优。 |
| `initial_retrieve_top_k` | 知识库全局配置（控制台/API） | integer | 1–100 | 向量/关键词初步召回数，直接影响 Rerank 阶段 [Token](token.md) 消耗与延迟。是成本优化核心杠杆。 |
| `similarity_threshold` | 知识库全局配置（控制台/API） | float | 0.01–1.0 | 过滤低相关性切片的阈值。设为 0.4–0.5 可平衡召回率与噪声；设过高（如 >0.6）可能导致空结果。务必通过命中测试验证。 |
| `knowledge_config.indices` | Knowledge API、工作流节点 | array of string | ≤5 个 ID | 指定参与联合检索的知识库 ID 列表。多库场景下支持按权重干预排序（仅同类型知识库间生效）。 |
| `metadata_filter` / `tags` | Retrieve API、工作流节点、数据连接工具 | object / array | — | 结构化过滤条件，用于精准限定检索范围（如 `{"category": "finance", "version": "2024Q3"}`），解决混杂数据召回不相关问题。 |
| `model` | 知识问答、LlamaIndex、Spring AI Alibaba | string | `qwen-max`, `qwen-plus`, `qwen3.7-plus` 等 | 指定生成阶段所用大模型。注意：知识检索接口不接受该参数；部分模型（如 `qwen-turbo`）当前不支持知识问答，以控制台可用列表为准。 |

> ⚠️ 注意：所有 RAG 调用均强制要求知识库状态为 `ACTIVE`；`PENDING` 或 `FAILED` 状态将被静默跳过。地域固定为 `cn-beijing`（华北2），URL 中 region 不可替换。

## 面向开发者，简洁实用

- **快速起步**：优先使用 Knowledge API（`/api/v2/apps/knowledge/chat`），传入 `knowledge_config.indices` 和 `model` 即可获得流式问答响应，无需索引管理。
- **调试技巧**：开启 `stream=false` 获取完整 JSON 响应，检查 `retrieval_results` 字段验证检索质量；若结果为空，先检查知识库状态、`similarity_threshold` 是否过高、`initial_retrieve_top_k` 是否过低。
- **成本控制**：`initial_retrieve_top_k × 平均 chunk token 数` 决定 Rerank 成本；`top_k × 平均 chunk token 数 + query token 数` 决定大模型输入成本。二者需协同压测。
- **安全合规**：所有上传数据独立存储于百炼平台，与原始源无关联；不用于模型训练或商业用途；敏感数据建议启用私有 OSS + STS 临时凭证访问。
- **错误处理**：常见错误包括 `model_not_supported`（模型不在知识问答白名单）、`429 Too Many Requests`（QPS 超限，需指数退避重试）、`index_not_found`（ID 错误或状态非 ACTIVE）。

## 关联主题页

- [knowledge](../api/knowledge.md)
- [knowledge base](../guides/knowledge-base.md)
- [frameworks](../api/frameworks.md)
- [data connection overview](../guides/data-connection-overview.md)
- [application component api reference](../api/application-component-api-reference.md)



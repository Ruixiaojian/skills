# 检索增强生成

检索增强生成（Retrieval-Augmented Generation，RAG）是一种将大语言模型（LLM）与外部知识源动态结合的技术范式。它通过在生成响应前实时检索相关知识片段，并将其作为上下文注入模型提示，显著提升回答的准确性、时效性与领域专业性，同时降低幻觉风险。

## 在百炼平台的不同场景中，这个概念如何使用

在百炼平台中，RAG 不是独立服务，而是贯穿多个能力模块的底层技术架构，具体体现为以下四类典型应用方式：

- **知识库问答（核心 RAG 场景）**：调用 `/api/v2/apps/knowledge/chat` 接口时，平台自动执行「规划 → 检索 → 生成」三阶段流程：先理解用户意图，再从指定 `knowledgeIds` 的已发布知识库中语义召回 TopK 文本切片（chunk），最后将召回结果与原始问题拼接为 Prompt，交由统一调度的问答模型（如 `qwen3.7-plus`）生成最终回复。支持[流式输出](streaming-output.md)（SSE）和多知识库联合检索（最多 15 个）。

- **智能体与工作流集成**：在智能体（Agent）或工作流（Workflow）中添加「文档知识库」节点，RAG 能力以工具调用形式嵌入决策链。例如，当用户提问“如何配置 OSS 权限？”，智能体可自主触发 `searchOSSFile` 工具，从已绑定的 OSS 连接器中检索匹配文档，再将结果送入 LLM 生成操作指南。

- **框架级快速接入**：通过 LlamaIndex 或 Spring AI Alibaba SDK，开发者可零配置接入云端 RAG。例如，LlamaIndex 中使用 `DashScopeCloudIndex.from_documents()` 直接加载百炼知识库，调用 `query_engine.query()` 即完成检索+生成闭环；Spring AI 中通过 `DashScopeDocumentRetriever` 实现知识库直检，无需自建向量库。

- **[多模态](multimodal.md)与结构化数据扩展**：RAG 不仅限于文本。结合数据连接器，可对表格（Excel）、数据库（MySQL/PolarDB-X）、音视频、图片等非文本数据进行向量化索引与语义检索。例如，上传含产品参数的 Excel 表格后，用户提问“哪款服务器支持 RDMA？”，系统可精准召回对应行并生成结构化回答。

> ⚠️ 注意：所有 RAG 场景均强制要求知识库/数据连接器处于 `published` 状态，且仅支持华北2（北京）地域；未发布的资源不会参与检索。

## 关键参数和配置

RAG 效果高度依赖以下可调参数，开发者需根据业务精度与性能权衡设置：

| 参数名 | 所属层级 | 说明 | 推荐值 | 配置位置 |
|--------|----------|------|--------|-----------|
| `top_k` / `similarity_top_k` | 检索层 | 向量召回的初步切片数 | 3–10（默认 5） | API 请求体、LlamaIndex `query_engine`、应用配置页高级设置 |
| `max_retrieved` | 检索层 | 最终送入 LLM 的切片总数（经重排后） | 1–5（默认 3） | 知识库详情页 > 高级设置、SDK `retriever` 构造参数 |
| `similarity_threshold` | 检索层 | 过滤低分切片的相似度阈值 | 0.3–0.7（过高易漏召，过低引入噪声） | 应用配置页 > 知识库 > 高级设置、API 请求体 |
| `stream` | 生成层 | 控制是否启用 SSE 流式响应 | `true`（推荐生产环境启用） | API 请求体、SDK `chat_options` |
| `temperature` | 生成层 | 控制生成结果随机性 | 0.1–0.5（生产环境建议 ≤0.3） | 应用配置页、SDK `llm` 设置、Gradio 界面 |

- **向量与重排模型**：由平台自动绑定，不可手动替换（如文档类知识库默认 `text-embedding-v4` + `qwen3-rerank`），但可通过知识库类型（如图片问答）触发强制切换（如 `qwen3-vl-embedding`）。
- **切片控制**：文本切片长度由平台智能切分策略决定（单切片 ≤6000 [Token](token.md)），不开放 `chunk_size`/`chunk_overlap` 手动配置（仅本地 RAG 支持）。

## 面向开发者，简洁实用

- ✅ **快速验证**：在知识库详情页使用「命中测试」功能，输入 Query 即可查看召回切片、相似度分数及来源文档，无需写代码。
- ✅ **调试技巧**：开通 SLS 日志后，通过 `pipeline_id`（知识库 ID）过滤日志，重点关注 `response_code=200` 但 `retrieved_count=0` 的请求，排查相似度阈值或知识库状态问题。
- ✅ **错误规避**：  
  - `404 Not Found`：检查 `workspaceId` 是否准确（非项目 ID），且 Base URL 固定为 `https://{workspaceId}.cn-beijing.maas.aliyuncs.com`；  
  - `429 Too Many Requests`：客户端需实现指数退避重试（默认 25 QPS 限流）；  
  - `retrieved_count=0`：确认知识库已发布、文档已成功解析（控制台显示「索引构建完成」）、Query 与文档语义匹配度足够。
- ✅ **成本优化**：费用 = 初步召回总切片数 × 平均 [Token](token.md) 数 × 单价，因此优先调小 `top_k` 而非 `max_retrieved`，并在效果达标前提下提高 `similarity_threshold`。

## 关联主题页

- [knowledge](../api/knowledge.md)
- [knowledge base](../guides/knowledge-base.md)
- [frameworks](../api/frameworks.md)
- [application use cases](../guides/application-use-cases.md)
- [data connection overview](../guides/data-connection-overview.md)



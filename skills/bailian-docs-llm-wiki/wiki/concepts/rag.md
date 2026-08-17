# 检索增强生成

检索增强生成（Retrieval-Augmented Generation，RAG）是一种将大语言模型（LLM）的生成能力与外部知识源的精准检索能力相结合的技术范式。它通过在生成前动态检索相关上下文片段，并将其注入提示（[prompt](../guides/prompt.md)），显著提升模型回答的事实准确性、领域专业性和时效性，同时降低幻觉风险。

## 在百炼平台的不同场景中，这个概念如何使用

在百炼平台中，RAG 不是抽象概念，而是已产品化、可开箱即用的核心能力，贯穿于多个技术路径：

- **知识库（Knowledge Base）**：这是 RAG 的基础设施层。开发者上传私有文档（PDF/DOCX/TXT/图片等），平台自动完成智能切分、向量化（默认 `text-embedding-v4` 或 `qwen3-vl-embedding`）、索引构建与多模态语义检索。所有知识库均天然支持 RAG，无需额外编码。
  
- **知识问答服务（`/chat`）**：端到端 RAG 应用接口。用户提问后，系统自动执行「检索 → 重排序（`qwen3-rerank`）→ 上下文注入 → 大模型生成」全流程，输出带引用溯源的流式回答，适用于客服、助手等生产级对话场景。

- **知识检索服务（`/search`）**：面向开发者的 RAG 召回层接口。返回按相关性排序的原始文本切片（chunk），支持跨知识库联合检索、元数据过滤（如 `{"source": "manual"}`）和自定义排序逻辑，便于构建定制化 RAG 流水线。

- **框架集成（LlamaIndex / Spring AI Alibaba）**：提供标准化 SDK 封装，屏蔽底层向量计算与 API 细节。例如 `DashScopeCloudIndex` 或 `DashScopeDocumentRetriever` 可直接对接百炼云端知识库，实现“检索+生成”闭环，加速 RAG 应用落地。

- **智能体与工作流应用**：在低代码编排中，可将知识库作为独立节点接入，配置相似度阈值、召回数量、权重路由等参数，与其他插件（如计算器、搜索）协同，构建具备实时知识感知能力的复合智能体。

> ✅ 关键事实：百炼所有 RAG 能力均由平台托管模型统一支撑，**不开放底层 Embedding 或 LLM 模型选择权**；开发者只需关注知识内容、检索策略与业务逻辑。

## 关键参数和配置

RAG 行为主要通过以下参数控制（按调用层级归类）：

| 参数名 | 所属接口/场景 | 说明 | 典型取值 |
|--------|--------------|------|-----------|
| `top_k` | `/search`, `/chat`, 知识库设置 | 最终返回给生成模型的上下文切片数 | `3`–`20`（默认 `5`） |
| `similarity_threshold` | 知识库控制台 / API 配置 | 重排后过滤低分切片的阈值 | `0.3`–`0.8`（`0.0` 表示不过滤） |
| `vector_top_k` / `keyword_top_k` | 知识库高级设置 | 初步向量/关键词召回数量（影响 rerank 成本） | 各 `10`–`100`（默认 `50`） |
| `filter` | `/search` 请求 Body | JSON 结构化元数据过滤（如 `{"tag": ["faq"]}`） | 支持嵌套字段，需提前在知识库中配置 Meta 抽取规则 |
| `stream` | `/chat`, 应用 SDK | 启用 SSE 流式响应 | `true`（默认）或 `false` |
| `incremental_output` | 应用 SDK / `application support` | 流式下启用增量 token 输出（避免重复发送） | `true`（需 `stream=true`） |

⚠️ 注意：  
- 所有 RAG 检索均依赖知识库状态为 `ACTIVE`；`BUILDING` 或 `FAILED` 状态将导致请求失败，**无降级机制**。  
- 相似度阈值过严（如 >0.7）易漏召，过松（如 <0.2）易引入噪声，建议结合业务效果 A/B 测试调整。  
- `filter` 字段虽未在公开 API 文档明确定义，但实测有效，推荐用于多源知识隔离（如区分“用户手册”与“内部政策”）。

## 面向开发者，简洁实用

- **快速验证**：用 3 行 cURL 即可测试 RAG 效果：
  ```bash
  curl -X POST "https://YOUR-WORKSPACE.cn-beijing.maas.aliyuncs.com/api/v1/indices/knowledge/search" \
    -H "Authorization: Bearer sk-xxx" \
    -d '{"query":"如何申请发票？","top_k":3,"filter":{"tag":["finance"]}}'
  ```

- **避坑指南**：  
  - ✅ 知识库仅支持华北2（北京）地域，其他地域调用会失败；  
  - ✅ 文件上传后需等待状态变为 `ACTIVE`（通常 1–5 分钟），再发起检索；  
  - ❌ 不支持自定义分块大小、嵌入模型或重排序模型（`qwen3-rerank` 为唯一可用 reranker）；  
  - ❌ `/chat` 接口无 `task_id`，连接中断需客户端自行重连，不支持异步轮询。

- **性能提示**：  
  - 若需高并发（>100 QPS），优先选用旗舰版知识库（最高 10,000 QPS）；  
  - 控制 `vector_top_k` ≤ 50 可显著降低 rerank 成本（费用与初步召回总量强相关）；  
  - 中文长尾问题建议搭配 `qwen3.7-plus` 或 `qwen-max` 模型，对检索结果理解更鲁棒。

RAG 是百炼平台最成熟、最易用的增强能力——你只需提供知识，平台负责精准召回与可信生成。

## 关联主题页

- [knowledge](../api/knowledge.md)
- [knowledge base](../guides/knowledge-base.md)
- [frameworks](../api/frameworks.md)
- [application use cases](../guides/application-use-cases.md)
- [application support](../guides/application-support.md)



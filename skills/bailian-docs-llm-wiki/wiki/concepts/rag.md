# 检索增强生成

检索增强生成（Retrieval-Augmented Generation，RAG）是一种将大语言模型（LLM）的生成能力与外部知识源的精准检索能力相结合的技术范式。它通过在生成前动态检索相关知识片段，并将其作为上下文注入模型提示（[prompt](../guides/prompt.md)），显著提升回答的准确性、事实性与领域适应性，避免模型幻觉，同时支持私有数据安全接入。

## 在百炼平台的不同场景中，这个概念如何使用

在百炼平台中，RAG 不是单一接口，而是贯穿多个能力模块的**统一技术底座与工程实践模式**，具体体现为以下三类核心使用方式：

- **知识库问答（端到端 RAG 流程）**：通过 `knowledge/chat` 接口或控制台「智能体应用」启用知识库后，系统自动执行「查询理解 → 多知识库联合检索 → 重排序 → 上下文拼接 → 大模型生成」全流程。支持 SSE [流式输出](streaming-output.md)，且内置多跳推理与 Query 改写能力，适用于客服、文档助手等高可靠性场景。

- **独立检索服务（RAG 的前置阶段）**：通过 `knowledge/search` 接口或 SDK 的 `Retrieve` 方法，仅执行语义检索与重排，返回结构化文本切片（chunk）及元数据（如来源文件、页码、相似度分数）。开发者可自主决定是否送入下游模型，适用于需要自定义生成逻辑、A/B 测试或混合检索策略（如关键词+向量）的场景。

- **数据连接增强（RAG 的扩展数据源）**：结合 `data connection` 能力，RAG 可接入结构化数据库（MySQL/PostgreSQL）、在线知识库（语雀）、对象存储（OSS）等实时或托管数据源。通过工具调用（如 `executeSQL`、`searchFile`）动态获取业务数据，再经向量化或直接注入 [prompt](../guides/prompt.md)，实现“检索+生成”闭环，适用于报表解读、订单查询、内部知识协同等场景。

> ⚠️ 注意：所有 RAG 能力均依赖百炼云端知识库服务（即 `CreateIndex` 创建的向量索引），不支持替换底层嵌入模型或自定义切分逻辑；若需完全自主控制，应选用[基于本地知识库构建RAG应用](https://help.aliyun.com/zh/model-studio/build-rag-application-based-on-local-retrieval)方案。

## 关键参数和配置

RAG 效果高度依赖以下关键参数，需根据场景权衡召回质量与性能成本：

| 类别 | 参数名 | 说明 | 推荐值 | 备注 |
|------|--------|------|--------|------|
| **检索控制** | `top_k` / `retrieval_top_k` | 向量检索初筛返回的切片数（初筛）或重排后最终送入 LLM 的数量（终筛） | 初筛：`50`（默认）；终筛：`3–5` | 初筛值越大，重排精度越高但费用上升；终筛值过大易引入噪声，建议 ≤5 |
| | `similarity_threshold` | 过滤重排后相似度低于该阈值的切片 | `0.3–0.7` | 设为 `0` 表示不过滤；值过高可能导致无结果返回 |
| **性能与规格** | `RCU`（旗舰版知识库） | 控制并发检索能力，1 RCU ≈ 50 QPS | `⌈峰值QPS ÷ 50⌉` | 标准版固定 1 QPS，不支持扩容 |
| **生成控制** | `temperature` | 控制生成随机性，影响答案稳定性 | `0.1–0.3`（RAG 场景推荐低值） | 配合 RAG 使用时，低 temperature 更利于忠实依据检索内容作答 |
| | `max_tokens` | 限制生成响应长度 | `512–1024` | 避免过长响应稀释关键信息，尤其在卡片消息等受限渠道 |

## 面向开发者，简洁实用

- ✅ **快速起步**：控制台创建知识库 → 上传文档 → 在智能体应用中勾选「必定调用」→ 发布即可启用 RAG，无需写一行代码。  
- ✅ **精细调优**：优先检查 `retrieval_top_k=3` 和 `similarity_threshold=0.4` 组合下的召回质量；若结果不相关，先优化知识库文档质量（如清洗、加标签），再调整参数。  
- ✅ **调试技巧**：调用 `knowledge/search` 接口单独测试检索效果；观察返回切片的 `score` 和 `metadata`，确认是否命中预期内容。  
- ✅ **成本意识**：初筛 `top_k` 每增加 10，重排费用约增 20%；终筛 `retrieval_top_k` 每增加 1，LLM 输入 token 增长约 300–800（取决于切片长度）。  
- ✅ **框架集成**：LlamaIndex 使用 `DashScopeCloudIndex` + `DashScopeRerank`；Spring AI Alibaba 使用 `DashScopeDocumentRetriever`；均需预置知识库名称（`INDEX_NAME`）与有效 API Key。  
- ❌ **避坑提醒**：不要尝试用 `chat/completions` 接口硬编码知识片段——这属于 Prompt Engineering，非 RAG；RAG 的本质是**运行时动态检索+上下文注入**，由平台统一调度。

## 关联主题页

- [knowledge](../api/knowledge.md)
- [knowledge base](../guides/knowledge-base.md)
- [frameworks](../api/frameworks.md)
- [data connection overview](../guides/data-connection-overview.md)
- [application use cases](../guides/application-use-cases.md)



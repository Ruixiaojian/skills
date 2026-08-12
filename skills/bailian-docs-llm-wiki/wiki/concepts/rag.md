# 检索增强生成

检索增强生成（Retrieval-Augmented Generation，RAG）是百炼平台的核心能力范式，指在大语言模型生成响应前，先从私有知识库中语义检索相关上下文，并将检索结果作为提示的一部分输入模型，从而提升回答的准确性、事实性与领域专业性。该机制天然融合了结构化/非结构化知识召回与大模型推理能力，是构建可信AI应用的关键技术路径。

## 在百炼平台的不同场景中，这个概念如何使用

RAG 在百炼中并非单一接口，而是贯穿多个层级的协同能力体系，开发者可根据需求选择不同抽象程度的实现方式：

- **开箱即用型（推荐入门）**：通过「知识问答」API（`/api/v2/apps/knowledge/chat`）或控制台智能体/工作流中的「文档知识库」节点，一键启用端到端RAG流程。系统自动完成查询理解、多知识库联合检索、结果重排（Rerank）、防幻觉拒答、引用溯源等环节，无需显式调用检索接口。
  
- **可控编排型（推荐生产）**：在工作流中分离「检索」与「生成」步骤：先调用 `Retrieve` 接口（或知识检索 API `/api/v1/indices/knowledge/search`）获取高相关性文本切片（chunks），再将结果注入自定义Prompt，交由任意支持的LLM（如 `qwen-max`、`qwen-plus`、`deepseek-v3.2`）生成最终回答。此方式支持灵活的元数据过滤（`metadata_filter`）、标签路由（`tags`）和后处理逻辑。

- **框架集成型（推荐快速工程化）**：使用 LlamaIndex 或 Spring AI Alibaba 等主流框架，通过 `DashScopeCloudIndex` 或 `DashScopeDocumentRetriever` 直接对接百炼托管知识库，复用其向量化（`gte-rerank`、`qwen3-vl-embedding` 等）与检索能力，同时保留框架层的Query Engine、Postprocessor等扩展能力。

- **混合部署型（推荐强定制需求）**：本地执行文档解析、切分与向量检索（如使用FAISS+自定义Embedding），仅将检索结果通过百炼API调用LLM生成。适用于需完全控制切分策略、嵌入模型或敏感数据不出域的场景。

> ⚠️ 注意：所有RAG路径均依赖已创建并发布的知识库，且仅支持华北2（北京）地域；知识库类型（文档/表格/图片/音视频）决定可用的解析器、向量模型及检索行为，创建后不可更改。

## 关键参数和配置

RAG效果高度依赖以下可调参数，需根据任务复杂度与成本权衡设置：

| 参数 | 作用 | 典型值范围 | 生效位置 | 说明 |
|------|------|------------|----------|------|
| `top_k` | 最终返回给LLM的召回片段数 | `3–20` | 知识检索API、工作流知识库节点、LlamaIndex Query Engine | 值过小易信息缺失，过大增加[Token](token.md)消耗与噪声；对比类问题建议设为 `8–12` |
| `similarity_threshold` | 过滤低相关性切片的相似度阈值 | `0.01–1.0` | 工作流节点、智能体配置页、Spring AI Alibaba `retriever` | 默认 `0.0`（不过滤）；设为 `0.45` 可显著减少无关内容，但可能漏召；需结合日志分析调整 |
| `rerank_top_k` | 初步向量/关键词检索后送入Rerank模型的切片数 | `1–100` | 知识库高级设置页 | **直接影响费用**：费用按此数量计费，而非最终 `top_k`；建议设为 `top_k × 2` 至 `top_k × 5` |
| `metadata_filter` / `tags` | 运行时动态过滤知识库内容 | JSON对象或字符串数组 | 所有检索接口（API/SDK/框架） | 如 `{"product": "百炼手机X1"}` 或 `["faq", "policy"]`，实现精准场景路由 |
| `stream` | 控制生成阶段是否[流式输出](streaming-output.md) | `true` / `false` | 知识问答API、LLM调用接口 | 流式响应（SSE）适合前端实时渲染；非流式返回完整JSON，便于后处理 |

> ✅ 最佳实践：首次上线建议 `top_k=5`, `similarity_threshold=0.3`，通过SLS日志分析召回质量后再逐步调优；多知识库绑定时，`rerank_top_k` 费用线性叠加，需谨慎评估。

## 面向开发者，简洁实用

- **一句话启动RAG**：上传PDF至控制台 → 创建知识库 → 在智能体中勾选“文档知识库” → 发布应用 → 即可对话。
- **API级最小调用**：
  ```bash
  curl -X POST "https://{workspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/indices/knowledge/search" \
    -H "Authorization: Bearer ${API_KEY}" \
    -H "Content-Type: application/json" \
    -d '{"query":"百炼如何接入钉钉？","top_k":5}'
  ```
- **关键避坑点**：
  - 知识库必须“发布”状态才可被调用，草稿状态返回 `404`；
  - `workspaceId` 与 `API Key` 必须属于同一业务空间，跨空间调用失败；
  - 音视频/图片知识库需启用对应多模态向量模型（如 `multimodal-embedding-v1`），普通文档库不兼容；
  - 所有检索日志默认投递至SLS，开通路径：知识库列表页 → “监控配置” → 开启日志服务。

RAG不是黑盒功能，而是百炼中可观察、可调试、可计量的基础设施——善用SLS日志与用量报表，是持续优化RAG效果的最短路径。

## 关联主题页

- [knowledge](../api/knowledge.md)
- [knowledge base](../guides/knowledge-base.md)
- [application component api reference](../api/application-component-api-reference.md)
- [frameworks](../api/frameworks.md)
- [use cases](../guides/use-cases.md)
- [application use cases](../guides/application-use-cases.md)



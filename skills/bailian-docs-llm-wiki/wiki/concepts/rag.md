# 检索增强生成

检索增强生成（Retrieval-Augmented Generation，RAG）是一种将大语言模型（LLM）的生成能力与外部知识源的精准检索能力相结合的技术范式。它通过在模型推理前动态检索相关上下文片段，并将其注入提示词（Prompt），显著提升回答的事实准确性、领域专业性与时效性，同时降低幻觉风险。

## 在百炼平台的不同场景中，这个概念如何使用

在百炼平台，RAG 不是单一功能，而是贯穿多个服务层级的**核心能力模式**，开发者可根据需求选择不同抽象程度的实现路径：

- **零代码/低代码应用层**：在智能体或工作流应用中，直接绑定已发布的「知识库」节点，配置“必定调用”策略。平台自动完成检索→重排→生成全流程，支持多轮对话改写、文件溯源、拒答控制等生产级特性。适用于客服助手、内部知识问答等快速上线场景。

- **API 直接调用层**：  
  - 使用 `/api/v1/indices/knowledge/search` 接口执行**纯检索**，获取带元信息（如 `file_name`, `cat_name`）的语义切片（chunk），由开发者自主拼装 Prompt 并调用大模型（如 `qwen3.5-plus`）生成答案；  
  - 使用 `/api/v2/apps/knowledge/chat` 接口发起**端到端知识问答**，平台严格按 `plan → tool_call → answer` 三阶段[流式输出](streaming-output.md)，无需手动管理检索与生成逻辑，但必须指定 `app_id` 且仅作用于该应用关联的知识库。

- **框架集成层**：  
  - 通过 **LlamaIndex** 调用 `DashScopeCloudIndex`，利用 `DashScopeRerank` 后处理器和 `SimilarityPostprocessor` 实现可编程的检索链，再注入 `DashScope(model_name="qwen-max")` 进行生成；  
  - 通过 **Spring AI Alibaba** 使用 `DashScopeDocumentRetriever` 直连知识库（非应用），检索结果可自由注入任意兼容模型（如 `qwen-turbo` 或自定义微调模型），适合需要完全掌控 RAG 流程的工程化项目。

- **混合增强层**：在网站、企业微信、钉钉等渠道集成中，RAG 作为默认增强机制——AppFlow 自动将用户 Query 透传至百炼知识库，检索结果与原始 Query 一并送入大模型，实现“开箱即用”的私域知识增强。

## 关键参数和配置

RAG 效果高度依赖以下关键参数，需根据场景权衡精度、延迟与成本：

| 类别 | 参数名 | 说明 | 典型取值 | 注意事项 |
|------|--------|------|----------|----------|
| **检索控制** | `top_k`（初步召回数） | 向量/关键词双路召回的初始切片数量 | `10–50` | 值越大，Rerank [Token](token.md) 消耗越高；建议从 `20` 起调优 |
| | `similarity_threshold` | 过滤低相关性切片的最小相似度得分 | `0.3–0.7` | 过高易漏召，过低引入噪声；[多模态](multi-modal.md)场景建议下调至 `0.25` |
| | `max_retrieved_count` | 最终返回给生成模型的切片总数 | `3–10` | 直接影响 Prompt 长度与模型响应速度，推荐 `5` |
| **排序优化** | `rerank_model` | 重排序模型，决定最终相关性打分质量 | `"qwen3-rerank"`（文本）、`"qwen3-vl-rerank"`（[多模态](multi-modal.md)） | 替代已下线的 `gte-rerank`，必须显式指定 |
| | `instruct`（Rerank） | 自定义排序指令，引导模型理解任务意图 | `"Find the most authoritative technical specification."` | 对专业领域问答效果提升显著 |
| **知识结构** | `meta_extraction` | 为文本切片附加结构化元信息（如 `file_name`, 正则提取字段） | 启用 `file_name` + `cat_name` | 解决同质内容混淆问题的核心手段 |
| | `tag_filter` | 检索时按业务标签（如 `"hardware"`）精确限定范围 | `"hardware"` | 适用于多业务线知识隔离场景 |

> ⚠️ **重要约束**：所有 RAG 能力仅在中国站华北2（北京）地域可用；知识库需处于「已发布」状态方可参与检索；`app_id` 绑定的知识问答接口不支持跨知识库聚合，如需联合检索请使用 `/search` API。

## 面向开发者，简洁实用

- **快速验证**：用 `curl` 直接调用 `/search` 接口，传入 `query` 和 `top_k=5`，观察返回切片的相关性与元信息完整性；
- **调试技巧**：开启知识库的「多轮对话改写」后，在工作流中检查 `query` 变量是否已自动补全指代（如将“它”转为具体产品名）；
- **成本优化**：优先调小 `top_k` 而非 `max_retrieved_count`——前者影响 Rerank 成本，后者影响 LLM 输入 [Token](token.md)；
- **错误排查**：若检索无结果，先确认知识库状态为「已发布」、`workspaceId` 地域为 `cn-beijing`、`similarity_threshold` 未设过高；
- **进阶控制**：需完全自定义切分逻辑或嵌入模型？请使用本地 RAG 方案（文档 `build-rag-application-based-on-local-retrieval.md`），百炼知识库 API 仅支持文档搜索类场景。

## 关联主题页

- [knowledge](../api/knowledge.md)
- [frameworks](../api/frameworks.md)
- [knowledge base](../guides/knowledge-base.md)
- [application use cases](../guides/application-use-cases.md)
- [vector and sort](../api/vector-and-sort.md)



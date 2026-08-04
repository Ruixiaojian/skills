# 检索增强生成

检索增强生成（Retrieval-Augmented Generation，RAG）是一种将外部知识检索与大语言模型生成能力深度融合的架构范式。它通过在模型推理前动态召回相关知识片段，并将其作为上下文注入提示（[prompt](../guides/prompt.md)），显著提升回答的准确性、事实性与领域适配性，同时降低幻觉风险。

## 在百炼平台的不同场景中，这个概念如何使用

在百炼平台中，RAG 不是单一接口或模型，而是贯穿数据接入、知识管理、应用编排与模型调用的端到端能力链路，具体体现为以下四类核心使用方式：

- **知识库驱动的 RAG 应用**：最典型场景。用户上传文档/表格/音视频等私有数据构建知识库 → 平台自动完成解析、智能切分、向量化（`text-embedding-v4` 或 `qwen3-vl-embedding`）与索引 → 在智能体或工作流应用中绑定该知识库 → 用户提问时，系统自动执行语义检索（含可选 rerank 模型如 `qwen3-rerank`）→ 将 Top-K 相关文本切片拼入 [prompt](../guides/prompt.md) → 调用指定生成模型（如 `qwen3.7-plus`）输出答案。全程支持引用溯源、拒答控制与多轮对话改写。

- **数据连接器 + RAG 增强**：适用于需对接企业源系统的场景。通过 MySQL/PostgreSQL/PolarDB-X 等**流处理类连接器**，在运行时实时查询结构化数据；或通过 OSS/语雀/钉钉等**平台托管类连接器**，将外部文件同步至百炼知识库后参与 RAG。两类路径均能为 LLM 提供动态、新鲜的上下文支撑，避免知识固化。

- **框架集成式 RAG**：面向开发者快速构建云端 RAG 应用。使用 LlamaIndex（`DashScopeCloudIndex`）或 Spring AI Alibaba（`DashScopeDocumentRetriever`）等 SDK，以代码方式调用百炼知识库检索服务，并与本地或云端 LLM（如 `qwen-max`）组合成完整 RAG 流水线，支持流式响应与细粒度上下文注入。

- **渠道嵌入式 RAG 助手**：面向业务落地的开箱即用方案。在网站、企业微信、微信公众号、钉钉等渠道，通过 AppFlow 低代码连接流一键集成已配置 RAG 的百炼应用。用户在渠道端提问，请求经 AppFlow 路由至百炼 → 触发知识库检索 + 模型生成 → 结果回传至渠道前端，10 分钟内即可上线具备私域知识能力的 AI 助手。

## 关键参数和配置

RAG 效果高度依赖以下可调参数，开发者应根据精度、延迟与成本权衡配置：

| 参数 | 说明 | 典型取值 | 配置位置 |
|------|------|----------|----------|
| `retrieval_top_k` / `top_k` | 向量检索阶段召回的初始切片数 | 5–20（默认 5） | 知识检索 API 请求体、知识库“知识检索”服务配置页、LlamaIndex/Spring AI SDK 初始化参数 |
| `similarity_threshold` | 重排后过滤低相关切片的相似度阈值 | 0.3–0.5（默认 0.3） | 知识库“知识问答”配置页、应用编辑页“知识库”区域 |
| `max_retrieved_chunks` | 最终送入 LLM 的最大切片数量 | 1–10（需 ≤ 模型上下文窗口） | 知识库“知识问答”配置页、“知识检索”服务全局参数 |
| `rerank_model` | 召回后精排模型（启用时生效） | `qwen3-rerank`, `qwen3-vl-rerank`, `qwen3-rerank(hybrid)` | “知识检索”服务配置页、知识库高级设置 |
| `multi_round_rewrite` | 是否启用多轮对话 Query 改写（提升指代消解） | `true`/`false`（创建知识库时设定） | 知识库初始化配置页（不可修改） |
| `chunk_size` / `chunk_overlap` | **仅本地 RAG 支持**：自定义文档切分粒度 | 如 `chunk_size=512`, `overlap=64` | 本地 RAG 应用代码（如 `local_rag.py`）或 Gradio UI |

> ⚠️ 注意：百炼云端知识库使用平台默认智能切分与嵌入策略，**不支持自定义切分逻辑或替换向量模型**；若需完全可控的切分与 embedding，应选用[本地 RAG 方案](../../raw/application-user-guide/application-use-cases/build-rag-application-based-on-local-retrieval.md)。

## 面向开发者，简洁实用

- **快速验证**：直接在控制台创建知识库 → 上传 PDF/Excel → 绑定至智能体应用 → 发起测试提问，5 分钟内验证 RAG 效果。
- **API 调用**：  
  - 检索：`POST https://{workspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/indices/knowledge/search`，Body 含 `{"query": "xxx", "top_k": 10}`  
  - 问答：`POST https://{workspaceId}.cn-beijing.maas.aliyuncs.com/api/v2/apps/knowledge/chat`，Body 含 `{"app_id": "app-xxx", "messages": [{"role":"user","content":"xxx"}]}`，响应为 SSE 流。
- **SDK 集成**：优先选用 Spring AI Alibaba（`DashScopeDocumentRetriever`）或 LlamaIndex（`DashScopeCloudIndex`），二者均提供统一 `retrieve()` 方法，返回 `List<Doc>`，可直接注入 `ChatClient` 或 `LLMPredictor`。
- **调试技巧**：开启知识库“引用溯源”，查看生成答案对应的具体原文片段；检查 SSE 流中的 `planning` 和 `tool_calling` 事件，确认检索是否触发；监控 `429 Too Many Requests` 错误，按需申请 QPS 配额提升。
- **避坑指南**：确保 `workspaceId` 与 `Authorization` 中的 API Key 属于同一业务空间；知识库功能仅限华北2（北京）地域；OSS 连接器需添加 `bailian-datahub-access:read` 标签方可用于同步。

## 关联主题页

- [knowledge](../api/knowledge.md)
- [knowledge base](../guides/knowledge-base.md)
- [frameworks](../api/frameworks.md)
- [data connection overview](../guides/data-connection-overview.md)
- [application use cases](../guides/application-use-cases.md)
- [use cases](../guides/use-cases.md)



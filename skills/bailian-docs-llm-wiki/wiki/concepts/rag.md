# 检索增强生成

检索增强生成（Retrieval-Augmented Generation，RAG）是一种将大语言模型（LLM）的生成能力与外部知识源的精准检索能力相结合的技术范式。它通过在模型推理前动态召回相关文档片段，并将其作为上下文注入提示词，显著提升回答的准确性、可溯源性与领域适配性，同时规避模型幻觉和知识过期问题。

## 在百炼平台的不同场景中，这个概念如何使用

在百炼平台，RAG 不是单一接口，而是贯穿多个能力层的**统一增强机制**，开发者可根据需求选择不同抽象层级的实现方式：

- **零代码应用层（智能体/工作流）**：在创建智能体（Agent 2.0）或工作流应用时，直接绑定已部署的[知识库](knowledge-base.md)。平台自动完成“查询理解 → 知识路由 → 多库联合检索 → 上下文融合 → 增强生成”全流程。支持配置 `必定调用` 或 `按需调用` 模式，并在对话中实时展示引用来源（docReferences）。

- **API 服务层（[knowledge](../api/knowledge.md) 接口）**：通过 `/api/v1/indices/knowledge/search`（纯检索）或 `/api/v1/indices/knowledge/chat`（端到端问答）调用。后者采用三阶段流式协议（规划→检索→生成），默认使用 `qwen-plus`，支持指定 `model` 参数切换为 `qwen-max` 等兼容模型，适用于构建自定义 RAG 应用。

- **框架集成层（LlamaIndex / Spring AI Alibaba）**：  
  - LlamaIndex：使用 `DashScopeCloudIndex` 构建云端[知识库](knowledge-base.md)，通过 `as_query_engine()` 配置 `similarity_top_k`、`similarity_cutoff` 和重排策略，调用 `.query()` 即完成 RAG；  
  - Spring AI Alibaba：注入 `DashScopeDocumentRetriever`，传入 `INDEX_NAME` 即可检索，结合 `ChatClient` 实现无缝增强生成。

- **本地化 RAG（高代码/私有化场景）**：百炼提供可运行的 Python 示例工程（`local_rag.zip`），支持自定义文本切分、替换嵌入模型（如 `text-embedding-v4`）、调整 TopK 与相似度阈值，适用于对数据不出域、模型可控性要求高的场景。

> ✅ 关键共识：所有路径均依赖**预构建的向量[知识库](knowledge-base.md)**（通过 OpenAPI `CreateIndex` 或控制台上传完成），百炼不提供运行时文档上传或在线索引构建能力。

## 关键参数和配置

| 参数 | 作用 | 典型取值 | 生效位置 | 注意事项 |
|------|------|----------|----------|----------|
| `top_k` / `similarity_top_k` | 控制检索阶段召回的文本切片数量 | `3`–`10`（推荐）；最大 `20` | `/search`, `/chat`, LlamaIndex, 工作流节点 | 数值越大，召回更全但 [Token](token.md) 消耗上升；`/search` 中生效，`/chat` 中影响检索阶段召回数 |
| `similarity_cutoff` / 相似度阈值 | 过滤低相关性切片，提升精度 | `0.4`–`0.7`（文本类）；`0.3`–`0.6`（多模态） | 知识库控制台、LlamaIndex、工作流节点 | 阈值过高易漏召，过低引入噪声；实际效果需结合「命中测试」迭代验证 |
| `indices` / `INDEX_NAME` | 显式指定参与检索的知识库 | `["kb-xxx", "kb-yyy"]` 或 `"销售FAQ"` | `/chat` body、Spring AI Alibaba 配置 | 为空时使用应用默认知识库；多库联合检索需确保各库状态均为 `ACTIVE` |
| `model` | 指定生成阶段使用的 LLM | `"qwen-plus"`, `"qwen-max"`, `"qwen-turbo"` | `/chat` body、LlamaIndex `model_name`、智能体配置 | `qwen-turbo` 在部分 region 不支持 SSE 流式协议，生产环境优先选 `qwen-plus` |
| `enable_thinking` | 启用模型内置规划能力（如判断是否需检索） | `true` / `false` | 智能体参数、第三方模型 `extra_body` | 仅对支持思考模式的模型（如 `qwen-max`）生效；开启后增强 RAG 的自主决策能力 |

## 面向开发者，简洁实用

- **快速起步**：控制台创建知识库 → 上传 PDF/DOCX → 绑定至智能体应用 → 发布 → 调用 API，全程无需写检索逻辑。
- **调试必查项**：  
  - 确认知识库状态为 `ACTIVE`（`PENDING`/`FAILED` 将静默失败）；  
  - 检查 Base URL 是否为 `https://{workspaceId}.cn-beijing.maas.aliyuncs.com`（地域硬编码）；  
  - `/chat` 接口必须使用 SSE 客户端（如 `fetch + ReadableStream`），不可用普通 POST 解析。
- **性能优化**：  
  - 降低 `初步向量检索 TopK`（知识库控制台）可减少 Rerank 费用；  
  - 启用「标签过滤」或结构化字段（如 `filename: "用户手册_v2.pdf"`）提升召回精准度；  
  - 对长文档启用「智能切分」策略，避免单切片过长导致截断。
- **计费提示**：知识库检索返回的文本切片计入模型输入 [Token](token.md)；Rerank 费用按**初步召回总切片数**计算，而非最终返回数。

> 💡 提示：RAG 效果 = 知识库质量 × 检索精度 × 提示词设计。建议优先优化源文件格式（清除水印、合并单元格）和元数据配置，再调参。

## 关联主题页

- [knowledge](../api/knowledge.md)
- [knowledge base](../guides/knowledge-base.md)
- [frameworks](../api/frameworks.md)
- [llm application](../guides/llm-application.md)
- [use cases](../guides/use-cases.md)
- [application use cases](../guides/application-use-cases.md)



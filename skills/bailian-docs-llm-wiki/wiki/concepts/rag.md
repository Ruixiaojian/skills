# 检索增强生成

检索增强生成（Retrieval-Augmented Generation，RAG）是一种将外部知识检索与大语言模型生成能力协同融合的技术范式。它通过在模型推理前动态召回相关知识片段，并将其作为上下文注入提示词，使模型能在不修改参数的前提下，准确、可溯源地回答领域专属、时效性强或事实敏感的问题。

## 在百炼平台的不同场景中，这个概念如何使用

在百炼平台中，RAG 不是抽象技术概念，而是已封装为开箱即用的核心能力，贯穿于多个服务层级：

- **知识库（Knowledge Base）**：这是 RAG 的原生载体。开发者上传文档后，平台自动完成解析、切片、向量化与索引构建；调用 `/search` 接口实现纯检索召回，调用 `/chat` 接口则自动执行「检索 → 重排 → 注入 → 生成」全链路，支持极速模式（单次检索+生成）和多轮智能模式（含规划、[工具调用](tool-use.md)与迭代生成）。

- **数据连接（Data Connection）**：扩展 RAG 的数据源边界。平台托管类连接器（如文件、表格）将数据向量化后纳入知识库统一检索；流处理类连接器（如 MySQL、语雀）则通过专用工具（如 `executeSQL`、`searchYuQue`）在智能体运行时实时拉取结构化数据，实现“检索增强”与“实时查询”的混合增强。

- **框架集成（Frameworks）**：面向开发者提供 RAG 工程化入口。LlamaIndex 通过 `DashScopeCloudRetriever` 和 `DashScopeRerank` 直接对接百炼知识库，支持自定义后处理；Spring AI Alibaba 提供 `DashScopeDocumentRetriever`，底层自动串联检索与 `qwen-max`/`qwen-plus` 等模型生成，无需手动拼装 Prompt。

- **智能体与工作流应用**：RAG 成为应用的默认增强能力。在智能体配置中添加知识库节点，或在工作流中拖入「知识库」节点并绑定 `TopK` 与相似度阈值，即可让整个 Agent 或工作流天然具备私域知识理解与引用能力。

- **文件管理 API**：支撑 RAG 的前置数据准备。通过 `purpose="file-extract"` 上传文件，为后续导入知识库或触发自动解析做准备；该 API 不参与 RAG 推理，但构成 RAG 数据闭环的关键一环。

> ⚠️ 注意：百炼所有 RAG 能力均限定在中国站华北2（北京）地域，且不支持切换底层 Embedding 或排序模型——语义计算由平台统一调度，开发者只需关注业务逻辑与参数配置。

## 关键参数和配置

RAG 效果高度依赖以下关键参数，需根据场景权衡精度、延迟与成本：

| 参数 | 作用范围 | 推荐值 | 说明 |
|------|----------|--------|------|
| `top_k`（或 `similarity_top_k`） | `/search`、工作流知识库节点、LlamaIndex 查询引擎 | `3–5`（平衡精度与 [Token](token.md) 开销） | 最终注入大模型的召回片段数。值过大会增加输入 [Token](token.md) 消耗与幻觉风险；值过小易遗漏关键信息。 |
| 初步检索 TopK | 知识库控制台 / API 创建时 | `10–50` | 控制向量/关键词初步召回数量，直接影响重排序计算量与费用（按此数量计费，非最终 `top_k`）。建议设为 `top_k` 的 2–5 倍。 |
| 相似度阈值（0.01–1.0） | 知识库控制台 / `/chat` 请求体 | `0.3–0.6` | 重排序后过滤低相关性片段的硬性门槛。过高导致召回不足，过低引入噪声；建议从 `0.4` 起调优。 |
| `filter`（元数据过滤） | `/search` 请求体、工作流知识库节点 | `{"source": "manual", "date": ">=2024-01-01"}` | 在检索前按标签、文件名、时间等元数据精准筛选知识库子集，显著提升跨库检索效率与准确性。 |
| `stream` | `/chat` 请求体 | `true`（推荐） | 启用 SSE 流式响应，降低端到端延迟，适用于对话类应用。 |

> 💡 实用提示：  
> - 所有 RAG 请求必须携带有效的 `Authorization: Bearer <API-Key>`，且 Base URL 中需包含正确的 `workspaceId`；  
> - 知识库需处于「已发布」且「active」状态才可被检索；  
> - 元数据 `filter` 字段虽未在官方文档显式声明，但在实际请求中完全可用，是提升精准度的高性价比手段。

## 面向开发者，简洁实用

- **快速验证**：用 `curl` 直接调用 `/search`，确认知识库是否生效；再用 `/chat` 测试端到端问答效果，无需写代码。
- **生产集成**：优先选用 LlamaIndex 或 Spring AI Alibaba 封装好的 `DashScopeDocumentRetriever`，避免重复实现分块、向量、重排逻辑。
- **调试技巧**：开启 `/chat` 的 `stream=false` 非流式模式，查看完整 JSON 响应中的 `retrieval_results` 字段，直接检查召回内容质量。
- **成本控制**：监控「初步检索 TopK」与「最终 `top_k`」的差值——差值越大，重排序开销越高；合理设置相似度阈值可减少无效生成。
- **安全底线**：所有知识库内容默认启用防泄漏与拒答策略，敏感信息无需额外脱敏；引用溯源功能（`citations` 字段）可直接用于前端高亮展示。

## 关联主题页

- [knowledge](../api/knowledge.md)
- [frameworks](../api/frameworks.md)
- [knowledge base](../guides/knowledge-base.md)
- [data connection overview](../guides/data-connection-overview.md)
- [file management api](../api/file-management-api.md)
- [use cases](../guides/use-cases.md)



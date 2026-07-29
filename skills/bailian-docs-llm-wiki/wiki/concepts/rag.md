# 检索增强生成

检索增强生成（Retrieval-Augmented Generation，简称 RAG）是一种将大语言模型（LLM）的生成能力与外部知识源的精准检索能力相结合的技术范式。它通过在生成前动态检索相关上下文片段（chunk），将其注入提示词（[prompt](../guides/prompt.md)），显著提升回答的准确性、可溯源性与领域适配性，同时降低幻觉风险。

## 在百炼平台的不同场景中，这个概念如何使用

在百炼平台，RAG 不是抽象技术概念，而是已深度产品化、开箱即用的核心能力，贯穿于多个服务层级：

- **知识库（Knowledge Base）**：这是百炼 RAG 的基础设施层。开发者上传文档（PDF/DOCX/表格等），平台自动完成切分、向量化、索引构建与混合检索（向量 + 关键词）。所有检索调用均默认启用 Rerank 排序，并支持多库联合、标签过滤、相似度阈值控制等精细化策略。

- **知识检索与问答（`/search` 和 `/chat` API）**：这是 RAG 的标准服务接口层。`/search` 提供纯语义检索结果（top_k 切片数组）；`/chat` 实现端到端 RAG 闭环：自动执行 Query 改写 → 多库并行检索 → 上下文注入 → LLM 生成，并支持 SSE 流式响应（含 `plan`/`tool_call`/`answer` 三阶段事件）。

- **智能体与工作流应用（Application / Workflow）**：在低代码编排中，RAG 以“文档知识库”节点形式集成。开发者只需拖拽连接知识库与大模型节点，并在提示词中引用 `{result}` 变量，即可完成私有知识注入，无需编写检索逻辑。

- **框架集成（LlamaIndex / Spring AI Alibaba）**：面向开发者，百炼提供 SDK 封装的 RAG 调用能力。例如，LlamaIndex 中使用 `DashScopeCloudRetriever` 直接对接云端知识库；Spring AI Alibaba 中通过 `INDEX_NAME` 指定知识库，自动完成检索+生成链路，默认使用 `qwen-max`，也可显式指定 `withModel("qwen-plus")`。

- **多渠道 AI 助手（AppFlow）**：RAG 是网站、企业微信、钉钉等渠道智能客服的底层支撑。配置时启用“必定调用”知识库，所有用户提问均自动触发检索，确保回答始终基于最新、最相关的私有资料。

> ✅ 注意：百炼 RAG 默认不暴露底层 embedding 模型或切分逻辑——所有向量化、Rerank、混排均由平台统一调度，开发者只需关注业务参数（如 `top_k`、`similarity_threshold`）和结果质量。

## 关键参数和配置

RAG 行为由以下关键参数控制，按作用域分为全局、知识库级和请求级：

| 参数类别 | 参数名 | 作用域 | 典型取值 | 说明 |
|----------|--------|--------|-----------|------|
| **请求级（API / SDK）** | `top_k` | `/search` 请求体 | 1–20（默认 5） | 最终返回的检索切片数量，直接影响 LLM 输入长度与 [Token](token.md) 消耗。 |
| | `stream` | `/chat` 请求体 | `true`/`false`（默认 `true`） | 启用 SSE [流式输出](streaming-output.md)，便于前端实时渲染。 |
| **知识库级（控制台配置）** | 初步向量检索 TopK | 知识库设置页 | 1–100（默认 50） | 向量检索首轮召回数，**计入 Rerank 计费**（费用 = 召回切片数 × 平均切片 [Token](token.md) 数 × 单价）。 |
| | 初步关键词检索 TopK | 知识库设置页 | 1–100（默认 50） | 关键词检索首轮召回数，同样计入 Rerank 计费。 |
| | 相似度阈值 | 知识库设置页 | 0.01–1.0（默认 0.3） | 过滤低相关性切片；值过高易漏召，过低引入噪声。 |
| | 检索模式 | 知识库设置页 | `vector` / `full_text` / `hybrid` | 控制底层检索策略，`hybrid` 为默认推荐模式。 |
| **应用级（智能体/工作流）** | `retrieval_top_k` | 应用配置或 Prompt 变量 | 3–5 | 工作流中知识库节点输出的切片数，与 API 的 `top_k` 语义一致。 |
| | `similarity_threshold` | 应用配置 | 0.3–0.8 | 应用层二次过滤阈值，作用于知识库返回结果。 |

> ⚠️ 重要限制：  
> - 所有 RAG 能力**仅在中国站华北2（北京）地域可用**；  
> - `/chat` 接口**不接受 `model` 字段**，模型由业务空间绑定的默认推理引擎自动调度；  
> - 知识库必须处于 `Published` 状态，草稿或禁用状态将导致空结果或 `404`。

## 面向开发者，简洁实用

- **快速验证**：用 `curl` 直接调用 `/search`，确认知识库是否生效：
  ```bash
  curl -X POST "https://{workspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/indices/knowledge/search" \
    -H "Authorization: Bearer {api-key}" \
    -H "Content-Type: application/json" \
    -d '{"query":"百炼支持哪些文件格式？", "top_k":3}'
  ```

- **生产集成建议**：  
  - 优先使用 `/chat` 接口而非自行拼接 [prompt](../guides/prompt.md) —— 它已内置 Query 改写、多轮上下文补全与拒答保护；  
  - 若需更高可控性，用 LlamaIndex 的 `DashScopeCloudRetriever` + 自定义 LLM 节点，保留 `qwen-plus` 等低成本高效果模型；  
  - 对延迟敏感场景（如客服首响），将 `top_k` 设为 3–5，`similarity_threshold` 提至 0.5+，避免低质上下文拖慢生成。

- **调试技巧**：  
  - 查看 SLS 日志中的 `retrieval_result` 字段，确认召回内容是否相关；  
  - 若结果不准，先检查知识库是否发布、文档是否被正确解析（控制台“预览切片”功能可验证）；  
  - 使用 AppFlow 的“对话测试”面板，开启“显示检索结果”开关，直观比对检索与最终回答的匹配度。

RAG 在百炼不是附加选项，而是默认增强路径。聚焦业务问题，让平台处理检索复杂性——这是你高效落地可信 AI 应用的关键起点。

## 关联主题页

- [knowledge](../api/knowledge.md)
- [knowledge base](../guides/knowledge-base.md)
- [frameworks](../api/frameworks.md)
- [application support](../guides/application-support.md)
- [use cases](../guides/use-cases.md)
- [application use cases](../guides/application-use-cases.md)



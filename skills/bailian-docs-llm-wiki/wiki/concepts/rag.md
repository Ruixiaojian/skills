# 检索增强生成

检索增强生成（Retrieval-Augmented Generation，RAG）是百炼平台的核心范式，指在大语言模型（LLM）生成响应前，先从私有或结构化知识源中实时检索相关上下文片段，并将检索结果与用户查询共同输入模型，从而提升回答的准确性、时效性与事实一致性。该范式天然解耦“知识存储”与“推理生成”，使模型无需微调即可动态接入最新业务数据。

## 在百炼平台的不同场景中，这个概念如何使用

RAG 在百炼平台并非单一接口，而是贯穿多个能力层的架构模式，开发者可根据需求选择不同抽象层级的实现方式：

- **知识库（Knowledge Base）**：最标准的 RAG 实现。通过控制台或 API 创建知识库（支持文档、表格、图片、音视频），系统自动完成解析、切片、向量化与索引构建；后续检索调用 `qwen3-rerank` 等重排模型优化召回质量，最终将 Top-K 片段注入 LLM 上下文生成答案。适用于客服问答、产品手册查询等强知识依赖场景。

- **知识检索与问答（`/knowledge/search` & `/knowledge/chat`）**：面向快速集成的托管式 RAG 服务。无需管理知识库生命周期，只需传入 `workspaceId` 和 `API Key`，即可发起语义检索或端到端流式问答（含规划→检索→生成三阶段事件）。底层固定使用百炼 RAG 专用推理栈，不暴露模型选择参数。

- **智能体应用（Agent Application）**：将 RAG 作为可规划工具嵌入自主决策链路。新版 Agent 2.0 支持将知识库与 MCP 工具统一注册为 `tool`，由模型根据用户意图动态决定是否调用、调用哪个知识库，并支持多轮检索-反思闭环。文件处理中的“切片检索”模式即为此类 RAG 的典型用法。

- **工作流应用（Workflow Application）**：通过可视化节点编排实现确定性 RAG 流程。拖入“知识库”节点，配置 `TopK`、相似度阈值、标签过滤等参数，输出检索结果后连接至“大模型”节点，手动拼接提示词（如 `"基于以下信息回答：{result} \n\n问题：{query}"`），完全掌控上下文构造逻辑。

- **框架集成（LlamaIndex / Spring AI Alibaba）**：面向代码优先开发者的低代码 RAG 方案。LlamaIndex 封装云端知识库为 `DashScopeCloudIndex`，自动处理向量检索与重排；Spring AI Alibaba 提供 `DashScopeDocumentRetriever`，支持流式响应与自定义提示模板，二者均复用百炼托管的向量化与排序能力，不开放嵌入模型替换。

- **应用级集成（网站/企微/钉钉助手）**：RAG 作为开箱即用的业务能力交付。通过 AppFlow 连接流，将百炼智能体应用与知识库绑定，配置“必定调用”或“按需调用”策略，即可在企业微信对话、网站悬浮窗等渠道提供私有知识问答服务，全程无需编写推理逻辑。

## 关键参数和配置

RAG 效果受多层级参数协同影响，关键配置如下（按作用域分组）：

| 作用域 | 参数名 | 类型 | 说明 | 典型取值 |
|--------|--------|------|------|----------|
| **全局检索控制** | `top_k` / `max_retrieval_count` | int | 检索返回的文本切片数量 | 3–5（平衡精度与噪声）；最大支持 20（知识 API）、100（知识库级） |
| | `similarity_threshold` | float | 相似度过滤阈值（0.01–1.0） | 0.3–0.6（默认 0.4）；设为 0 表示不过滤 |
| | `knowledge_routing` | boolean | 启用知识库路由（调用 `qwen-plus` 判断应查哪个库） | `true`（多库场景推荐） |
| **重排序（Rerank）** | `rerank_model` | string | 排序模型 ID | `qwen3-rerank`（文本）、`qwen3-vl-rerank`（多模态） |
| | `top_n` | int | 重排后返回前 N 条结果 | 默认返回全部；建议显式设为 `top_k` 值保持一致 |
| **知识库构建** | `chunk_strategy` | string | 切片策略 | `"smart_split"`（推荐，保障语义完整性） |
| | `vector_model` | string | 向量模型（创建知识库时指定） | `qwen3.7-text-embedding`（长文本）、`qwen3-vl-embedding`（图文混合） |
| **智能体/工作流** | `retrieval_max_chunk_length` | int | 单个检索片段最大 token 数 | 512–2048（避免截断关键信息） |
| | `enable_thinking` | boolean | 是否开启模型思考模式（影响检索意图理解） | `true`（Agent 2.0 强烈推荐） |

> ⚠️ 注意：  
> - 所有 RAG 能力严格限定于 **中国站华北2（北京）地域**，Endpoint 必须为 `https://{workspaceId}.cn-beijing.maas.aliyuncs.com`；  
> - 知识库检索不支持跨 Region 调用，且 `workspaceId` 是业务空间 ID（非 UID 或租户 ID），需从控制台获取；  
> - `model` 参数在 `/knowledge/*` 接口**不可用**（会被忽略），仅在智能体、工作流、框架集成等场景生效。

## 面向开发者，简洁实用

- **快速验证**：用 `curl` 直接调用知识检索 API，确认知识库已发布且 `workspaceId`/`API Key` 正确：
  ```bash
  curl -X POST "https://YOUR_WORKSPACE_ID.cn-beijing.maas.aliyuncs.com/api/v1/indices/knowledge/search" \
    -H "Authorization: Bearer YOUR_API_KEY" \
    -H "Content-Type: application/json" \
    -d '{"query":"百炼平台如何上传PDF？", "top_k":3}'
  ```

- **效果调优三步法**：  
  1. **查得准**：调高 `similarity_threshold`（如 0.5→0.6）或启用 `qwen3-rerank`；  
  2. **召得全**：增大 `top_k`（如 3→5），并检查知识库切片策略是否为 `smart_split`；  
  3. **答得好**：在智能体/工作流中增加系统提示词约束，例如 `"请严格依据检索结果作答，未知信息请明确回复'未找到相关信息'"`。

- **避坑指南**：  
  - 不要尝试在 `/knowledge/chat` 请求中传入 `model` 字段——该接口无此参数；  
  - 多知识库联合检索时，务必开启 `knowledge_routing`，否则可能漏检；  
  - 视频/图片类 RAG 必须使用 `qwen3-vl-*` 系列模型（向量+重排），通用文本模型无法处理多模态内容；  
  - 生产环境优先选用 `qwen3-rerank`（替代已下线的 `gte-rerank`），其性能与兼容性已全面验证。

## 关联主题页

- [knowledge](../api/knowledge.md)
- [knowledge base](../guides/knowledge-base.md)
- [frameworks](../api/frameworks.md)
- [llm application](../guides/llm-application.md)
- [use cases](../guides/use-cases.md)
- [application use cases](../guides/application-use-cases.md)
- [vector and sort](../api/vector-and-sort.md)



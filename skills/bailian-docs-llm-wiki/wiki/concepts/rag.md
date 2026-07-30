# 检索增强生成

检索增强生成（Retrieval-Augmented Generation，RAG）是百炼平台的核心能力范式，指在大语言模型生成响应前，先从私有或领域知识库中动态检索相关片段，并将检索结果作为上下文注入提示词，从而提升回答的准确性、事实性与专业性。它不是独立模型，而是一种可复用、可配置、端到端集成的增强架构。

## 在百炼平台的不同场景中，这个概念如何使用

RAG 在百炼中以**知识库（Knowledge Base）**为载体，贯穿多种产品形态和接入路径，开发者可根据业务复杂度与控制粒度需求灵活选用：

- **零代码应用集成**：在智能体或工作流应用中添加「文档知识库」节点，绑定已发布知识库并配置相似度阈值、权重等参数；系统自动完成检索→引用→生成全流程，适用于客服助手、内部知识问答等标准场景。
  
- **API 直接调用**：
  - `knowledge` 服务（`/api/v2/apps/knowledge/chat`）：面向终端用户的端到端问答，强制绑定 `app_id`，返回结构化 SSE 流（`plan` → `tool_call` → `answer`），支持多轮对话与溯源引用；
  - `application component` API（`Retrieve` 接口）：面向开发者的底层检索能力，可自由组合检索结果与任意模型（如 `qwen3.7-plus`）进行自主生成，适用于需精细控制 RAG 链路的定制化系统。

- **框架集成**：
  - **LlamaIndex**：通过 `DashScopeCloudIndex` 构建云端知识库，调用 `as_query_engine()` 自动集成检索与生成，支持 `DashScopeRerank` 后处理；
  - **Spring AI Alibaba**：使用 `DashScopeDocumentRetriever` 直接对接知识库，配合 `ChatClient` 实现“检索+生成”解耦编排，适合 Java 生态项目。

- **渠道嵌入场景**：在网站、企业微信、钉钉、微信公众号等渠道通过 AppFlow 接入百炼应用时，启用「必定调用知识库」策略，所有用户提问均自动触发 RAG 增强，无需修改渠道侧逻辑。

> ⚠️ 注意：所有 RAG 能力仅在中国站华北2（北京）地域可用；知识库必须处于「已发布」状态才参与检索；未发布的草稿或下线知识库不可见。

## 关键参数和配置

RAG 效果高度依赖以下三类可调参数，建议按阶段优化：

### 1. 检索阶段（影响召回质量与成本）
| 参数 | 说明 | 推荐值 | 备注 |
|------|------|--------|------|
| `top_k`（向量/关键词召回数） | 控制双路初始召回切片数量 | 20–50 | 默认 50；值越大 Rerank [Token](token.md) 消耗越高，但漏召风险降低 |
| `similarity_threshold` | 过滤低于该相似度的切片 | 0.3–0.6 | 过高易漏召，过低引入噪声；建议从 0.45 开始调优 |
| `max_retrieve_count` | 最终返回给生成模型的切片总数 | 3–10 | 直接影响 [prompt](../guides/prompt.md) 长度与生成质量，推荐 ≤8 |

### 2. 知识库构建与元数据（影响检索精准度）
| 参数 | 说明 | 用法示例 |
|------|------|----------|
| `Meta信息抽取` | 为文本切片附加结构化上下文（如 `file_name`, `cat_name`, 正则提取字段） | 解决“同名文件内容混杂”问题，支持在 Prompt 中通过 `{meta.file_name}` 引用 |
| `标签过滤` | 上传文件时打标（如 `硬件`/`软件`），检索时指定 `tag=硬件` 精确限定范围 | 适用于多业务域隔离场景 |

### 3. 高级策略（提升多轮体验）
| 参数 | 说明 | 注意事项 |
|------|------|----------|
| `多轮对话改写` | 创建知识库时启用，基于历史对话自动补全当前 Query | 创建后不可修改，建议新知识库默认开启 |
| `权重` | 多知识库绑定时分配数值权重（如 `权重=3` > `权重=1`） | 仅对同类型知识库（如均为文档搜索类）生效 |

## 面向开发者，简洁实用

- ✅ **快速起步**：控制台创建知识库 → 上传 PDF/DOCX/TXT → 发布 → 在智能体应用中绑定 → 启用「必定调用」→ 即可上线。
- ✅ **调试技巧**：调用 `/api/v1/indices/knowledge/search` 接口单独测试检索效果，验证 `query` 是否能召回预期切片。
- ✅ **成本优化**：优先调小 `top_k` 和 `max_retrieve_count`；启用 `similarity_threshold` 过滤低质切片；避免在 Prompt 中重复粘贴冗余检索结果。
- ✅ **错误排查**：
  - 返回空结果？检查知识库状态是否为「已发布」、`workspaceId` 地域是否为 `cn-beijing`、`query` 是否含敏感词被拒答；
  - 流式响应中断？确认客户端正确解析 SSE event 类型（`plan`/`tool_call`/`answer`），勿假设单次响应即完成；
  - 限流 `429`？实现指数退避重试，或升级至旗舰版知识库（支持更高 QPS）。

RAG 不是黑盒魔法，而是可控的数据增强管道——掌握检索参数、善用元数据、分阶段验证，即可稳定交付高可信 AI 服务。

## 关联主题页

- [knowledge](../api/knowledge.md)
- [knowledge base](../guides/knowledge-base.md)
- [application component api reference](../api/application-component-api-reference.md)
- [frameworks](../api/frameworks.md)
- [application use cases](../guides/application-use-cases.md)
- [use cases](../guides/use-cases.md)



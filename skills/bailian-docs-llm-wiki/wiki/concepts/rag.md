# 检索增强生成

检索增强生成（Retrieval-Augmented Generation，RAG）是一种将大语言模型（LLM）的生成能力与外部知识源的精准检索能力相结合的技术范式。它通过在模型推理前动态检索相关上下文片段，并将其注入提示（[prompt](../guides/prompt.md)）中，显著提升回答的事实准确性、领域专业性和可解释性，同时降低幻觉风险。

## 在百炼平台的不同场景中如何使用

RAG 是百炼平台的核心能力底座，贯穿于多个产品层级和集成路径，具体体现为以下三类典型用法：

- **端到端知识问答服务**：调用 `/api/v2/apps/knowledge/chat` 接口，系统自动完成「语义检索 → 重排序 → 规划/工具调用 → 增强生成」全流程，适用于客服对话、智能助手等开箱即用场景。该接口不维护会话状态，需客户端传入完整 `messages` 历史实现多轮交互。

- **底层可控检索 + 自定义生成**：调用 `/api/v1/indices/knowledge/search` 获取原始召回切片（chunk），再结合自有模型（如 `qwen-max`、`qwen-plus` 或第三方模型）进行 [prompt](../guides/prompt.md) 工程与生成。适用于需精细控制检索逻辑、上下文拼接策略或后处理流程的开发者。

- **框架级集成 RAG 应用**：  
  - 使用 **LlamaIndex**：通过 `DashScopeCloudIndex` 直接对接百炼托管知识库，支持 `similarity_top_k`、`similarity_cutoff` 及 `DashScopeRerank` 等参数调节；  
  - 使用 **Spring AI Alibaba**：选择 `DashScopeDocumentRetriever`（知识库检索模式）或 `DashScopeAgent`（应用调用模式），前者直接绑定 `INDEX_NAME`，后者通过 `APP_ID` 调用已配置 RAG 的智能体/工作流。

所有路径均依赖百炼统一的知识库基础设施——无论通过控制台上传、数据连接器同步（OSS/语雀/MySQL等），还是 SDK/API 创建，最终都转化为向量化索引供 RAG 流程调用。

## 关键参数和配置

RAG 效果由检索层与生成层协同调控，核心可配参数如下：

| 层级 | 参数名 | 说明 | 典型取值范围 | 生效位置 |
|------|--------|------|--------------|----------|
| **检索层** | `retrieval_top_k` / `max_retrieved_count` | 最终送入 LLM 的上下文切片数量 | `1–20`（默认 `3`） | 知识库配置、API 请求 body、框架初始化参数 |
| | `similarity_threshold` | 相似度过滤阈值（0.01–1.0），低于此值的切片被丢弃 | `0.3–0.7`（值越高越严格） | 知识库配置、API 请求 body |
| | `weight` | 多知识库联合检索时的加权系数（仅同类型间生效） | `0.1–10.0`（默认 `1.0`） | 控制台知识库绑定页 |
| **生成层** | `temperature` | 控制输出随机性，低值更确定 | `0.0–0.7`（客服建议 ≤0.3） | API 请求 body、框架 `withModel()` 配置 |
| | `max_tokens` | 生成内容最大 token 数 | `256–2048`（简短回复推荐 `256–512`） | 同上 |
| | `context_window` | 携带的历史对话轮数（影响 [prompt](../guides/prompt.md) 长度） | `1–5`（单轮问答设为 `1`） | 客户端 `messages` 构造逻辑 |

> ⚠️ 注意：`TopK` 参数在不同环节含义不同——知识库配置中的「初步向量/关键词检索 TopK」（默认各 `50`）影响召回广度；而 `retrieval_top_k` 是最终交付给 LLM 的切片数，直接影响 [Token](token.md) 消耗与费用。

## 面向开发者，简洁实用

- ✅ **快速起步**：控制台创建知识库 → 绑定至智能体应用 → 发布 → 用 `/api/v2/apps/knowledge/chat` 直接调用，5 分钟验证 RAG 效果。  
- ✅ **精细调优**：若发现答案不准确，优先检查 `similarity_threshold`（过低易引入噪声，过高易漏检）和 `retrieval_top_k`（过小信息不足，过大增加成本）。  
- ✅ **生产就绪**：  
  - 多轮对话？自行维护 `messages` 数组并按时间倒序传入；  
  - 需要审计？在 AppFlow 中接入 SLS 日志节点，记录 `retrieved_docs` 字段；  
  - 成本敏感？监控 `rerank` 阶段 [Token](token.md) 消耗（与 `retrieval_top_k` 强相关），合理设置上限。  
- ❌ **避坑提示**：  
  - 知识库仅支持华北2（北京）地域，跨 Region 请求将失败；  
  - `/api/v2/apps/knowledge/chat` 的 Base URL 必须含 `{workspaceId}`，且 `Authorization` 中 API Key 必须与 workspace 匹配；  
  - 元数据（metadata）抽取规则在知识库创建时固化，后续不可修改——务必在上传前规划好 `file_name`、`cat_name` 等字段。

## 关联主题页

- [knowledge](../api/knowledge.md)
- [knowledge base](../guides/knowledge-base.md)
- [frameworks](../api/frameworks.md)
- [data connection overview](../guides/data-connection-overview.md)
- [application use cases](../guides/application-use-cases.md)



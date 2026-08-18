# 检索增强生成

检索增强生成（Retrieval-Augmented Generation，简称 RAG）是百炼平台实现“用私有知识提升大模型回答准确性”的核心范式。它通过在大模型生成前动态检索相关知识片段，并将其作为上下文注入 Prompt，使模型输出兼具事实性、专业性与可溯源性。

## 在百炼平台的不同场景中，这个概念如何使用

RAG 在百炼中不是单一功能，而是贯穿多个能力层的统一技术底座，开发者可根据需求选择不同抽象层级的使用方式：

- **开箱即用的端到端问答服务**：调用 `/api/v2/apps/knowledge/chat` 接口，平台自动完成查询改写 → 多知识库联合检索 → 重排精筛 → 上下文融合 → 大模型生成，并通过 SSE 流式返回「规划→工具调用→生成」三阶段结果。适用于快速上线客服、文档助手等业务。

- **灵活可控的检索+生成分离链路**：  
  - 先调用 `/api/v1/indices/knowledge/search` 或 `Retrieve` API 获取语义检索结果（含 chunk 文本、来源、相似度）；  
  - 再自行构造 Prompt（如拼接 top_k 个 chunk），送入任意支持的模型（`qwen3`, `deepseek-r1`, `llama3.1` 等）进行生成。  
  适用于需定制化上下文组装、引用标注、拒答策略或集成自有推理服务的场景。

- **低代码编排中的 RAG 节点**：在工作流应用中拖入「知识库」节点，配置输入变量（如 `query`）、目标知识库、`top_k` 及元数据过滤条件（`tags` / `metadata_filter`），其输出可直接连接至后续大模型节点的 `{result}` 变量，实现可视化 RAG 编排。

- **框架级集成**：通过 LlamaIndex 的 `DashScopeCloudIndex` 或 Spring AI Alibaba 的 `DashScopeDocumentRetriever`，以标准 SDK 方式接入百炼云端知识库，复用其向量化、混合检索与重排能力，无需管理底层索引构建与 API 调用细节。

> ✅ 关键提示：所有 RAG 能力均依赖已构建完成且状态为 `ACTIVE` 的知识库；知识库可接入多模态数据源（PDF/Word/Excel/图片/音视频），并支持 OSS、语雀、钉钉等外部系统定时同步。

## 关键参数和配置

| 参数 | 所属场景 | 说明 | 常用值 | 注意事项 |
|------|----------|------|--------|----------|
| `top_k` | 检索接口（`/search`, `Retrieve`） | 返回给下游的最高相关性文本切片数量 | `3`, `5`, `10` | 默认 `5`，最大 `20`；值过大可能引入噪声，过小易漏关键信息 |
| `similarity_threshold` | 知识库控制台/API 配置 | Rerank 后过滤低分切片的相似度阈值 | `0.35`, `0.5`, `0.7` | 范围 `0.01–1.0`；建议通过[命中测试](https://help.aliyun.com/zh/model-studio/rag-knowledge-base#81f57beb71zs1)调优 |
| `tags` / `metadata_filter` | 检索请求体 | 按用户定义标签或结构化元数据（如 `product=Qwen3`, `region=cn`）精准过滤知识库内容 | `["faq", "v3.6"]`, `{"version": "3.6"}` | 标签需在上传文件或创建知识库时预设；元数据键名不可动态新增 |
| `stream=true` | 问答接口（`/knowledge/chat`） | 启用 SSE 流式响应，获取三阶段中间结果 | `true`（推荐） | 非流式仅返回最终答案，丢失规划与工具调用过程，不利于调试与用户体验优化 |
| `pipeline_id` | 底层 API（`Retrieve`） | 知识库唯一标识符（即 `IndexId`） | `idx-abc123` | 必须通过 `CreateIndex` 创建后获取，非控制台显示的“知识库名称” |

## 面向开发者，简洁实用

- ✅ **首选方案**：新项目优先使用 `/api/v2/apps/knowledge/chat`（流式 + 三阶段），开发快、效果稳、自带拒答与引用溯源。
- ✅ **需要控制权**：用 `/api/v1/indices/knowledge/search` + 自选模型组合，可自由设计 Prompt 模板、添加系统指令、控制 token 截断与引用格式。
- ✅ **避免踩坑**：  
  - 所有 RAG 请求必须使用 `cn-beijing` 地域 Base URL（国际站用 `ap-southeast-1`）；  
  - 知识库未就绪（状态非 `ACTIVE`）时会返回 `400 index not ready`；  
  - 不要尝试在问答接口中传 `model` 参数——该接口模型由平台统一分配（当前为 `qwen-max` 或 `qwen-plus`），如需指定模型，请走分离链路或工作流节点。  
- ✅ **调试建议**：利用 OpenAPI Explorer 直接调试检索接口，观察返回的 `chunks` 内容与 `score` 分布，验证知识覆盖度与切分质量。

## 关联主题页

- [knowledge](../api/knowledge.md)
- [knowledge base](../guides/knowledge-base.md)
- [data connection overview](../guides/data-connection-overview.md)
- [application component api reference](../api/application-component-api-reference.md)
- [frameworks](../api/frameworks.md)



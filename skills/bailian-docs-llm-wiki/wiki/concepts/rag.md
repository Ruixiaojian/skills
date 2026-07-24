# 检索增强生成

检索增强生成（Retrieval-Augmented Generation，RAG）是一种将大语言模型（LLM）的生成能力与外部知识源的精准检索能力相结合的技术范式。它通过在模型推理前动态召回相关知识片段，并将其作为上下文注入提示词，显著提升回答的准确性、时效性、可解释性与领域专业性，同时降低幻觉风险。

## 在百炼平台的不同场景中，这个概念如何使用

在百炼平台中，RAG 不是单一接口，而是贯穿多个能力层的**统一技术架构**，支持从底层基础设施到上层应用的全栈集成：

- **知识库服务（核心 RAG 实现）**：  
  通过「知识库」功能，将 PDF/DOCX/XLSX/PPTX/图片/音视频等多模态数据解析、切片、向量化并构建语义索引；在问答时自动执行“检索 → 重排 → 注入 → 生成”四步流程，支持极速模式（单次检索+生成）和智能模式（Agentic 规划式多轮检索）。

- **应用级知识问答（面向业务）**：  
  使用 `/api/v2/apps/knowledge/chat` 接口，以流式 SSE 方式返回 `plan`（规划）、`tool_call`（检索调用）、`answer`（生成结果）三阶段事件，天然支持引用溯源、拒答控制与上下文感知，适用于客服、文档助手等生产场景。

- **框架集成（开发者友好）**：  
  LlamaIndex 和 Spring AI Alibaba 提供开箱即用的 `DashScopeCloudIndex` / `DashScopeDocumentRetriever`，自动对接云端知识库，无需管理向量模型或重排逻辑，仅需配置 `cloud_index_name` 和 `model_name` 即可启用 RAG。

- **低代码渠道集成（快速落地）**：  
  在网站、企业微信、钉钉、微信公众号等渠道中，通过 AppFlow 连接流一键绑定已发布的百炼应用与知识库，启用「必定调用」策略，实现零代码 RAG 助手部署。

- **本地 RAG 扩展（灵活可控）**：  
  对于有自定义需求的场景（如私有嵌入模型、特殊切分逻辑），平台提供基于 Gradio 的本地 RAG 模板，支持替换 `text-embedding-v4` 为开源模型（如 `gte-chinese-large`），并精细调节 `chunk_size`、`chunk_overlap` 等参数。

> ⚠️ 注意：所有 RAG 能力均依赖「已发布」状态的知识库；草稿或停用的知识库不参与检索。当前仅华北2（北京）地域可用。

## 关键参数和配置

RAG 效果由检索与生成两个环节协同决定，以下为开发者最常调整的核心参数（按作用域分类）：

| 类别 | 参数名 | 说明 | 推荐值范围 | 生效位置 |
|------|--------|------|-------------|-----------|
| **检索控制** | `retrieval_top_k` / `max_retrieved_chunks` | 最终注入 LLM 的知识片段数量 | `3–5`（平衡精度与 token 开销） | 应用配置页、API 请求体、LlamaIndex `similarity_top_k` |
| | `similarity_threshold` | 过滤重排后分数低于该阈值的片段 | `0.2–0.6`（过低引入噪声，过高漏召） | 控制台知识库设置、API 请求体 |
| | `vector_top_k` / `keyword_top_k` | 向量/关键词初检召回数（影响重排 [Token](token.md) 消耗） | `10–50` | 控制台高级设置、`application-component-api-reference` 中 `Retrieve` 接口 |
| **生成控制** | `temperature` | 控制生成随机性（越低越确定） | `0.1–0.5`（RAG 场景建议偏保守） | 所有生成接口通用参数 |
| | `max_tokens` | 限制输出长度，避免截断关键信息 | `512–2048` | 所有生成接口通用参数 |
| **知识库元数据** | `weight` | 多知识库联合检索时的优先级权重 | 数值型（如 `1.0`, `2.0`） | 控制台知识库绑定页（仅同类型知识库间生效） |
| | `meta_filters` | 基于预设 Meta 字段（如 `filename`, `date`）结构化过滤 | JSON 对象，如 `{"filename": "user_manual_v2.pdf"}` | API 请求体（`/api/v1/indices/knowledge/search`） |

> ✅ 提示：`qwen3-rerank` 是百炼默认且唯一支持的文本重排模型；第三方生成模型（如 DeepSeek-R1）可作为 LLM 使用，但**不可替代重排模型**。

## 面向开发者，简洁实用

- **快速起步**：  
  1. 在控制台创建并发布一个知识库（支持 15 个知识库联合检索）；  
  2. 创建智能体应用 → 绑定该知识库 → 启用「必定调用」；  
  3. 调用 `/api/v2/apps/knowledge/chat`，传入 `query` 即可获得带溯源的流式回答。

- **调试技巧**：  
  - 先用 `/api/v1/indices/knowledge/search` 单独测试检索质量，确认 `chunks` 内容相关；  
  - 若召回不准，优先检查 `similarity_threshold` 和 `meta_filters`，而非直接调高 `retrieval_top_k`；  
  - 流式响应中 `event: tool_call` 消息包含实际召回的 `chunk_ids`，可用于日志分析与效果归因。

- **避坑指南**：  
  - API Key 必须与 `workspaceId` 绑定，跨 workspace 调用必失败；  
  - Base URL 固定为 `https://{workspaceId}.cn-beijing.maas.aliyuncs.com`，不可替换地域；  
  - 第三方模型仅支持作为生成器，向量/重排模型必须使用百炼官方 `qwen3-*` 系列。

- **进阶优化**：  
  - 利用 Meta 信息抽取（如正则提取 `version`、`author`）实现精准过滤；  
  - 在 Prompt 中显式声明“请严格依据以下知识片段作答，并标注来源编号”，强化模型遵循性；  
  - 结合 `enable_thinking` 参数开启推理模式，让模型对检索结果进行交叉验证与逻辑整合。

## 关联主题页

- [knowledge](../api/knowledge.md)
- [knowledge base](../guides/knowledge-base.md)
- [application component api reference](../api/application-component-api-reference.md)
- [frameworks](../api/frameworks.md)
- [use cases](../guides/use-cases.md)
- [application use cases](../guides/application-use-cases.md)



# 检索增强生成

检索增强生成（Retrieval-Augmented Generation，RAG）是一种将大语言模型（LLM）与外部知识源动态结合的技术范式。它通过在模型推理前实时检索相关知识片段，并将其作为上下文注入提示（[prompt](../guides/prompt.md)），使模型在生成回答时既具备通用语言能力，又严格依据可信、最新的私有或领域数据，显著提升回答的准确性、可追溯性与专业性。

## 在百炼平台的不同场景中如何使用

RAG 在百炼平台不是单一接口，而是贯穿多个能力层的协同机制，开发者可根据需求选择不同抽象层级的实现方式：

- **知识库（Knowledge Base）**：最常用、最完整的 RAG 实现。支持文档、表格、图片、音视频等多模态数据接入，提供语义检索 + 排序 + 重排 + 生成一体化流程。适用于构建企业知识助手、客服问答系统等生产级应用。  
- **[knowledge](../api/knowledge.md) API**：面向开发者提供的轻量级 RAG 能力封装。分为 `检索`（`/search`）和 `问答`（`/chat`）两类接口：前者返回原始召回切片（chunk），供自定义编排；后者端到端完成「规划→检索→生成」三阶段，直接输出自然语言回答，支持流式响应（SSE）。  
- **数据连接（Data Connection）**：扩展 RAG 的数据源边界。除静态文件外，支持对接 MySQL、PostgreSQL、OSS、语雀等实时或托管数据源，通过工具调用（如 `queryMySQL`、`searchOSSFile`）实现“按需拉取+即查即用”，适用于需要强时效性的业务场景（如订单查询、政策更新通知）。  
- **框架集成（LlamaIndex / Spring AI Alibaba）**：面向代码优先开发者的 RAG 快速接入方案。LlamaIndex SDK 直接对接百炼云端知识库，支持灵活配置检索参数与后处理逻辑；Spring AI Alibaba 则侧重与百炼预置智能体/工作流应用集成，适合已有 Java 生态的企业快速复用业务编排能力。  
- **低代码应用（智能体/工作流/AppFlow）**：面向非开发人员的 RAG 落地路径。在控制台拖拽配置知识库节点、设置“必定调用”开关、调整相似度阈值与召回数量，即可将私有知识无缝注入对话流，5 分钟完成微信/钉钉/企业微信等渠道的智能助手部署。

## 关键参数和配置

RAG 效果高度依赖以下核心参数，建议按场景分层配置：

| 类别 | 参数名 | 常用值/范围 | 说明 | 适用场景 |
|------|--------|-------------|------|----------|
| **检索控制** | `top_k` / `similarity_top_k` | 3–10（默认 5） | 最终送入大模型的召回片段数。值过小易遗漏关键信息，过大增加噪声与 Token 开销。 | 所有场景必调 |
| **检索质量** | `similarity_threshold` | 0.3–0.7（默认 0.3） | 过滤低相关性切片的相似度下限。对噪声敏感场景（如法律/医疗）建议提高至 0.5+。 | 知识库控制台、API 请求体、LlamaIndex `NodePostprocessor` |
| **性能与精度平衡** | `vector_retrieval_top_k`（初步向量召回） | 20–100（默认 50） | 向量库首轮召回数量，影响后续重排精度与延迟。高精度场景可设为 100，低延迟场景可降至 20。 | 知识库创建/编辑页高级配置 |
| **元数据过滤** | `metadata_filter` | JSON 对象（如 `{"tag": "hr_policy"}`） | 基于上传时抽取的元数据（文件名、日期、正则字段等）进行精准过滤，避免无关内容干扰。 | [knowledge](../api/knowledge.md) API、知识库 API、LlamaIndex 查询参数 |
| **生成控制** | `temperature`、`max_tokens` | `temperature=0.3`、`max_tokens=1024` | 控制生成结果的确定性与长度。RAG 场景推荐低 temperature（0.1–0.5）以确保答案忠实于检索内容。 | 仅本地 RAG 或自定义 LLM 调用时显式设置；百炼 [knowledge](../api/knowledge.md) API 与知识库问答由平台自动优化 |

> ⚠️ 注意：`top_k` 是最终生效的关键上限——即使 `vector_retrieval_top_k=100`，若 `top_k=5`，也仅取排序后前 5 片段送入大模型。务必确认各层级参数的优先级与作用域。

## 面向开发者，简洁实用

- **快速验证**：用控制台「知识库 → 命中测试」输入问题，实时查看召回片段与分数，无需写代码即可调参。  
- **最小可行集成**：  
  ```bash
  curl -X POST "https://YOUR_WORKSPACE_ID.cn-beijing.maas.aliyuncs.com/api/v2/apps/knowledge/chat" \
    -H "Authorization: Bearer YOUR_API_KEY" \
    -H "Content-Type: application/json" \
    -d '{"query":"公司年假政策是什么？","index_ids":["idx-abc123"],"top_k":3}'
  ```  
- **避免常见坑**：  
  - ✅ 显式传 `index_ids`：即使配置了默认知识库，也建议强制传入，规避 400 错误；  
  - ✅ 流式解析用平台格式：`event: chunk` + `data: {...}`，勿套用 OpenAI SSE 客户端；  
  - ✅ OSS/Bucket 权限检查：确保 Bucket 已添加 `bailian-datahub-access: read` 标签；  
  - ❌ 不跨 workspace：所有 `index_ids` 必须归属同一业务空间。  
- **调试利器**：开通 SLS 日志投递后，用 `select data.nodes[*].score, data.nodes[*].text from log` 快速分析召回质量。  

RAG 不是黑盒魔法，而是可控的数据管道。从知识入库、检索调优到生成约束，百炼提供全链路可观测、可配置的能力，让开发者聚焦业务逻辑，而非基础设施。

## 关联主题页

- [knowledge](../api/knowledge.md)
- [knowledge base](../guides/knowledge-base.md)
- [frameworks](../api/frameworks.md)
- [data connection overview](../guides/data-connection-overview.md)
- [application use cases](../guides/application-use-cases.md)



# 检索增强生成

检索增强生成（Retrieval-Augmented Generation，RAG）是一种将大语言模型（LLM）的生成能力与外部知识源的精准检索能力相结合的技术范式。它通过在模型推理前动态召回相关上下文片段，并将其注入提示词（[prompt](../guides/prompt.md)），显著提升回答的事实准确性、领域专业性和可解释性，同时降低幻觉风险。

## 在百炼平台的不同场景中，这个概念如何使用

在百炼平台中，“检索增强生成”不是单一接口，而是贯穿多个能力层的**核心架构模式**，具体体现为以下三类协同使用的实践路径：

- **知识库（Knowledge Base）作为 RAG 底座**  
  知识库是百炼 RAG 的基础设施：上传文档 → 自动智能切分 + 向量化索引 → 支持语义检索。所有 RAG 应用均依赖已发布的知识库（状态为 `Active`），其检索结果（文本切片）作为上下文输入给大模型。支持[多模态](multimodal.md)知识源（PDF/DOCX/Excel/图片/音视频），并提供“相似度阈值”“初步召回 TopK”“最大返回数量”等精细化控制参数。

- **知识问答 API（`/chat`）作为端到端 RAG 封装**  
  `/api/v2/apps/knowledge/chat` 接口隐式执行完整 RAG 流程：自动提取用户 query → 联合检索指定知识库 → 融合 top_k 切片与对话历史 → 调用指定模型（如 `qwen-plus` 或 `qwen-max`）生成答案。开发者无需实现检索逻辑，仅需传入 `messages` 和可选 `model`、`top_k` 参数，即可获得流式或同步的增强回答。

- **智能体/工作流/框架集成作为 RAG 编排层**  
  - **智能体应用**：将知识库作为“工具”由 Agent 自主调用，支持标签过滤、混合文件与知识库内容；  
  - **工作流应用**：通过“知识库”节点显式配置 `content`（查询语句）、`top_k` 和动态知识库变量；  
  - **LlamaIndex / Spring AI Alibaba 框架**：提供 `DashScopeCloudIndex` 或 `DashScopeDocumentRetriever`，实现代码级 RAG 集成，复用百炼云端索引与重排能力，无需自建向量库。

> ✅ 关键共识：百炼所有 RAG 场景均**强制使用平台预置向量模型与索引策略**，不支持替换嵌入模型（如 `text-embedding-v1`）或自定义切分逻辑——这是平台托管型 RAG 的设计边界，确保效果稳定与计费透明。

## 关键参数和配置

| 参数 | 所属层级 | 类型 | 默认值 | 说明 | 生效范围 |
|------|----------|------|--------|------|-----------|
| `top_k` | `/chat` API、工作流节点、LlamaIndex | integer | `5` | 最终送入大模型的检索切片数量 | `/chat` 中影响内部 Retrieve 阶段；工作流/LlamaIndex 中直接控制输出节点数 |
| `similarity_cutoff` | LlamaIndex | float | — | 相似度后过滤阈值（如 `0.4`），低于此值的切片被丢弃 | 仅 LlamaIndex 可控，非百炼原生 API 参数 |
| `similarity_top_k` | LlamaIndex | integer | `5` | 向量召回阶段返回的原始切片数 | 影响重排费用（费用 = 召回数 × 平均切片 [Token](token.md) 数 × 单价） |
| `index_ids` | `/search` API | string[] | — | 显式指定参与检索的知识库 ID 列表；为空时检索当前应用绑定的所有知识库 | 仅 `/search` 接口可用，用于调试或自定义 RAG 流程 |
| `model` | `/chat` API、框架集成 | string | `qwen-plus` | 指定生成模型；必须为支持知识增强的模型（如 `qwen-plus`/`qwen-max`），`qwen-turbo` 等不支持 | 不同场景均生效，但模型必须在控制台应用中已启用 |

> ⚠️ 注意事项：  
> - `top_k` 在 `/chat` 中**不控制最终回答长度**，仅控制检索上下文数量；回答长度由模型自身的 `max_tokens` 参数控制。  
> - “相似度阈值”（`similarity_cutoff`）在知识库控制台和命中测试页可配置，但**不暴露为 API 参数**，需通过控制台调整后生效。  
> - 所有 RAG 调用均计入模型输入 [Token](token.md)（含检索切片内容），请合理设置 `top_k` 以平衡效果与成本。

## 面向开发者，简洁实用

- ✅ **快速上手**：优先使用 `/chat` 接口 + 已发布知识库，3 行代码即可完成 RAG 问答（见 [knowledge.md](../../raw/application-api-reference/knowledge.md) 示例）。  
- ✅ **调试必做**：在知识库详情页使用「命中测试」功能，输入真实 query，验证切片召回质量、来源文档与相似度分数，再上线。  
- ✅ **成本优化**：  
  - 降低 `top_k`（如从 `10` → `5`）可减少输入 [Token](token.md)；  
  - 提高「相似度阈值」可减少低质切片引入噪声；  
  - 使用「切片检索」模式（而非全文引用）可大幅节省 Token。  
- ✅ **避坑指南**：  
  - 确保知识库状态为 `Published` 且 `Active`，草稿/禁用库不会被检索；  
  - 文件上传后需等待「索引构建完成」（控制台显示绿色对勾），否则检索为空；  
  - 第三方框架（LlamaIndex/Spring AI）调用时，务必使用 `DASHSCOPE_API_KEY` 和 `WORKSPACE_ID` 环境变量（兼容性最佳）。  

RAG 是百炼平台最成熟、开箱即用的增强能力。聚焦知识库质量、合理配置 `top_k`、善用命中测试，即可在分钟级构建高准确率的专业问答系统。

## 关联主题页

- [knowledge](../api/knowledge.md)
- [knowledge base](../guides/knowledge-base.md)
- [frameworks](../api/frameworks.md)
- [llm application](../guides/llm-application.md)
- [application evaluation](../guides/application-evaluation.md)
- [use cases](../guides/use-cases.md)
- [application support](../guides/application-support.md)



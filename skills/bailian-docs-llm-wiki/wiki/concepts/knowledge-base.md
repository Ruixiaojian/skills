# 知识库

知识库是百炼平台实现[检索增强生成](rag.md)（RAG）的核心基础设施，指经过向量化处理、可被语义检索的结构化或非结构化数据集合。它不直接提供模型推理能力，而是作为外部知识源，通过与大语言模型协同工作，为问答、摘要、推理等任务注入私有、领域专属或时效性强的信息。

## 在百炼平台的不同场景中，这个概念如何使用

- **API 直接调用**：开发者可通过 `/knowledge/search`（语义检索）和 `/knowledge/chat`（端到端问答）两类 RESTful 接口消费已就绪的知识库；接口不支持上传或建索引，仅依赖 OpenAPI（如 `CreateIndex`）预先构建完成且状态为 `ACTIVE` 的知识库。
- **智能体（Agent）与工作流（Workflow）**：在控制台创建应用时，可绑定一个或多个知识库作为「工具」；新版 Agent 2.0 将知识库统一纳入可规划工具链，支持自动判断是否检索、触发召回并融合结果生成回答，同时返回引用切片（`docReferences`）。
- **框架集成**：LlamaIndex 和 Spring AI Alibaba 提供官方封装，例如 `DashScopeCloudIndex`（Python）或 `DashScopeDocumentRetriever`（Java），允许开发者在自有代码中声明式调用云端知识库，复用其向量索引与检索逻辑，无需自建向量数据库。
- **数据连接器联动**：文件（PDF/Word/图像/音视频）、表格（CSV/Excel）、OSS、语雀等数据源通过「数据连接器」接入后，系统自动完成解析、切分、向量化，并注册为知识库实例；知识库本身不感知原始数据位置，只暴露统一的语义检索能力。
- **独立服务形态**：可在知识库控制台单独发布「知识检索」或「知识问答」HTTP 服务，获取专属 Endpoint，供第三方系统轻量集成，无需构建完整 LLM 应用。

## 关键参数和配置

| 参数 | 作用 | 取值范围 | 说明 |
|------|------|-----------|------|
| `indices`（请求体） | 指定参与检索的知识库 ID 列表 | 字符串数组，如 `["idx-abc123", "idx-def456"]` | 空则使用应用默认知识库；多库联合检索时按相关性混排返回 |
| `top_k`（请求体） | 最终返回的文本切片数量 | 1–20（默认 5） | 影响 [Token](token.md) 消耗与回答完整性；`/search` 与 `/chat` 均生效 |
| `similarity_threshold`（控制台/SDK） | 过滤低相似度切片的阈值 | 0.01–1.0（默认约 0.3） | 过高易漏召，过低引入噪声；建议结合「命中测试」调优 |
| `vector_top_k`（控制台/SDK） | 向量初检阶段召回数 | 1–100（默认 50） | **计费关键项**：费用 = 此值 × 切片平均 [Token](token.md) 数；关闭 Rerank 可降本 |
| `enable_rerank`（控制台/SDK） | 是否启用 GTE 等重排模型精排 | `true` / `false` | 开启后提升排序质量，但增加延迟与费用；默认开启 |
| `model`（仅 `/chat` 请求体） | 指定问答生成所用大模型 | `qwen-plus`（推荐）、`qwen-max`、`qwen-turbo` | `qwen-turbo` 在部分 region 不支持 SSE 流式协议，慎用 |

> ⚠️ 注意：所有知识库功能**仅支持华北2（北京）地域**；Base URL 必须为 `https://{workspaceId}.cn-beijing.maas.aliyuncs.com`，即使 workspace 部署在其他 region，也需硬编码此域名。

## 面向开发者，简洁实用

- ✅ **快速验证**：先确认知识库状态为 `ACTIVE`，且至少含 1 条有效切片（控制台「命中测试」可验证）；首次调用失败请优先排查状态与地域。
- ✅ **调试技巧**：`/chat` 接口必须用支持 SSE 的客户端（如 `fetch` + `ReadableStream`）；普通 POST 会静默失败；响应中 `docReferences` 字段即为溯源依据。
- ✅ **成本控制**：降低 `vector_top_k`、关闭 `enable_rerank`、设置合理 `similarity_threshold` 是三大降本手段；避免盲目提高 `top_k`。
- ✅ **开发选型**：
  - 零代码/低代码 → 控制台直接绑定知识库到智能体或工作流；
  - Python 工程 → 用 LlamaIndex `DashScopeCloudIndex`；
  - Java 工程 → 用 Spring AI Alibaba `DashScopeDocumentRetriever`；
  - 自定义流程 → 调用 `/knowledge/search` 或 `/knowledge/chat` REST API。
- ❌ **禁止操作**：知识库创建后无法修改元数据抽取规则；不支持上传 JSON/CSV/YAML 原生格式（需转 XLSX）；不支持跨地域知识库共享。

## 关联主题页

- [knowledge](../api/knowledge.md)
- [knowledge base](../guides/knowledge-base.md)
- [data connection overview](../guides/data-connection-overview.md)
- [frameworks](../api/frameworks.md)
- [llm application](../guides/llm-application.md)



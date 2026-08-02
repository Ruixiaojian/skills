# 知识库

知识库是百炼平台实现[检索增强生成](rag.md)（RAG）的核心数据基础设施，用于将私有、结构化或非结构化知识（如文档、表格、图片、音视频）向量化并建立可语义检索的索引，从而为大模型提供精准、可控、可溯源的上下文支持。

## 在百炼平台的不同场景中，这个概念如何使用

- **RAG 应用构建**：知识库作为「外部知识源」直接注入智能体或工作流应用。在应用配置中启用知识库后，每次用户提问会自动触发语义检索，召回相关切片并送入大模型生成阶段，显著提升领域问答准确性与事实一致性。
- **API 直接调用**：通过 `knowledge/search`（检索）和 `knowledge/chat`（问答）两类 REST 接口，开发者可绕过低代码界面，以编程方式集成知识能力。前者返回原始文本切片（chunk），后者封装完整 RAG 流程（含规划、工具调用、生成），支持 SSE 流式响应。
- **框架集成**：LlamaIndex 和 Spring AI Alibaba 提供开箱即用的 SDK 封装（如 `DashScopeCloudIndex`、`DashScopeDocumentRetriever`），只需传入 `cloud_index_name` 或 `INDEX_NAME` 即可绑定已创建的知识库，自动完成向量检索与结果重排。
- **多模态扩展**：支持文档、表格、图片、音视频等多类型数据源。启用「视觉理解」后，系统自动切换至 `qwen3-vl-embedding` 向量模型，并支持图文混合检索与引用溯源。
- **数据连接协同**：知识库可作为「平台托管类数据连接器」的输出目标——上传的文件/表格经 DocMind 解析后，自动构建为知识库；也可与 MySQL、OSS 等流处理连接器配合，在智能体中按需调用不同数据源。

## 关键参数和配置

| 参数 | 说明 | 取值范围/默认值 | 生效位置 |
|------|------|------------------|-----------|
| `knowledgeIds` | 指定参与检索的知识库 ID 列表（最多 15 个） | 字符串数组，如 `["kb-abc", "kb-def"]` | API 请求 Body、智能体节点配置 |
| `top_k`（检索） | 最终返回给模型的切片数量上限 | 1–20，默认 5 | `knowledge/search` API、智能体知识库节点 |
| `similarity_threshold` | 重排后切片的最低相似度阈值 | 0.01–1.0，默认 0.3 | 控制台知识库设置、API 请求 Body |
| `retrieval_mode` | 知识调用策略 | `must_call`（必调用）、`auto`（按置信度触发） | 智能体/工作流应用配置 |
| `RCU`（旗舰版） | 检索并发能力单位（1 RCU ≈ 50 QPS） | 1–200 | 控制台知识库变配页，影响计费与性能 |
| `初步向量检索 TopK` | 向量召回阶段返回的切片数（供 Rerank 模型处理） | 1–100，默认 50 | 控制台高级设置，直接影响 Rerank 费用 |

> ⚠️ 注意：所有知识库操作仅对 **Published（已发布）状态** 的知识库生效；草稿、禁用或删除状态不可被检索或问答服务访问。

## 面向开发者，简洁实用

- **快速验证**：用 `curl` 直接测试检索接口（替换 `ws-xxx` 和 `ak-xxx`）：
  ```bash
  curl -X POST "https://ws-xxx.cn-beijing.maas.aliyuncs.com/api/v1/indices/knowledge/search" \
    -H "Authorization: Bearer ak-xxx" \
    -H "Content-Type: application/json" \
    -d '{"query":"产品售后政策","knowledgeIds":["kb-123"],"top_k":3}'
  ```

- **关键约束牢记**：
  - ✅ 地域限定：知识库功能**仅支持华北2（北京）地域**，其他地域（如新加坡）不可用；
  - ✅ 域名动态：Base URL 必须由 `workspaceId` 拼接（如 `https://{workspaceId}.cn-beijing.maas.aliyuncs.com`），**禁止硬编码通用域名**；
  - ✅ 文件限制：PDF/DOCX ≤ 150 MB 且 ≤ 1000 页；图片短边 > 15px、长边 < 8192px；音视频 ≤ 512 MB；
  - ✅ 计费敏感点：Rerank 费用按「初步召回总切片数 × Token 数」计算，**非最终返回数**；关闭 Rerank 可降本，但排序精度下降。

- **调试建议**：
  - 开通 SLS 日志后，检索日志中 `response_body.data.nodes[]` 包含每个切片的 `score`、`text`、`metadata`，可用于分析召回质量；
  - 多知识库联合检索时，Query 向量化与 Rerank 调用费用按知识库数量线性叠加，建议按业务场景合理分库；
  - 使用 `qwen3-rerank`（文本）或 `qwen3-vl-rerank`（多模态）时，务必确保知识库创建时选择的向量模型与之兼容（如 `qwen3-vl-embedding` 对应 `qwen3-vl-rerank`）。

## 关联主题页

- [knowledge](../api/knowledge.md)
- [knowledge base](../guides/knowledge-base.md)
- [data connection overview](../guides/data-connection-overview.md)
- [frameworks](../api/frameworks.md)
- [application use cases](../guides/application-use-cases.md)



# [knowledge](../api/knowledge.md) base

知识库是阿里云百炼平台提供的 RAG（[检索增强生成](../concepts/rag.md)）核心能力，用于为大语言模型注入私有数据与领域知识，提升回答的准确性与专业性。它支持文档、表格、音视频、图片等多种数据源的语义检索，并通过向量化、召回、重排、生成四阶段流水线完成端到端问答。知识库功能仅在中国站华北2（北京）地域可用，需在业务空间内创建并绑定至智能体、工作流或外部应用。

## 支持的模型/功能

- **支持的生成模型**：千问系列（QwQ/Long/Max/Plus/Turbo/Coder/Deep-Research、VL-Max/Plus/Flash/OCR、开源版 Qwen3/Qwen2.5/Qwen2）、第三方模型（DeepSeek-R1/V3.1、abab6.5s、Llama3.1、Yi-Large）等；自定义调优模型同样支持 [知识库](../../raw/application-user-guide/knowledge-base/rag-knowledge-base.md)。
- **核心功能**：
  - 多知识库联合检索（最多 15 个）与独立参数配置；
  - 双检索模式：极速模式（单轮检索+生成）与多轮智能模式（Agentic 规划搜索）[知识问答](../../raw/application-user-guide/knowledge-base/rag-knowledge-qa.md)；
  - [多模态](../concepts/multi-modal.md)支持：文本、图片、音视频内容的统一索引与检索；
  - 文件预解析：对话中实时上传并解析文档/图片，无需预先入库；
  - 标签过滤与元数据结构化检索，提升召回精准度 [RAG效果优化](../../raw/application-user-guide/knowledge-base/rag-optimization.md)。

> **注意**：文档 2 和文档 7 对“向量模型”支持存在表述差异——文档 2 仅列出 `text-embedding-v4` 和 `qwen3-vl-embedding`，而文档 7 明确补充 `text-embedding-v3` 和 `multimodal-embedding-v1`。以文档 7 的[知识库配额与限制](../../raw/application-user-guide/knowledge-base/rag-knowledge-base-specifications.md)为准，因其明确区分了知识库类型与对应向量模型。

## 关键参数

| 参数 | 取值范围 | 说明 | 来源 |
|------|----------|------|------|
| **初步向量检索 TopK** | 1–100（默认 50） | 向量语义召回切片数，直接影响 Rerank 模型 [Token](../concepts/token.md) 消耗量 | [知识问答](../../raw/application-user-guide/knowledge-base/rag-knowledge-qa.md)、[知识检索](../../raw/application-user-guide/knowledge-base/rag-knowledge-retrieval.md) |
| **相似度阈值** | 0.01–1.0 | 过滤重排后低分切片，过高易漏召，过低引入噪声 | [知识库](../../raw/application-user-guide/knowledge-base/rag-knowledge-base.md)、[知识问答](../../raw/application-user-guide/knowledge-base/rag-knowledge-qa.md) |
| **最大召回数量** | 1–20 | 最终返回给大模型的切片数，受模型输入长度限制 | [知识问答](../../raw/application-user-guide/knowledge-base/rag-knowledge-qa.md)、[知识检索](../../raw/application-user-guide/knowledge-base/rag-knowledge-retrieval.md) |
| **RCU（旗舰版）** | 1–200 | 检索并发能力单位（1 RCU ≈ 50 QPS），决定知识库吞吐上限 | [知识库计费说明](../../raw/application-user-guide/knowledge-base/billing-for-knowledge-base.md) |
| **标签数量/文件** | ≤32 | 单文件可附加标签上限，用于标签过滤召回范围 | [知识库配额与限制](../../raw/application-user-guide/knowledge-base/rag-knowledge-base-specifications.md) |

## 使用方式

- **控制台快速接入**：在[知识库](../../raw/application-user-guide/knowledge-base/rag-knowledge-base.md)页面创建标准版/旗舰版知识库 → 上传文件（支持 PDF/DOCX/Markdown/图片等）→ 配置索引（启用 Meta 信息抽取、智能切分等）→ 绑定至智能体/工作流应用，在“文档知识库”节点中选择并设置权重、相似度阈值等。
- **API 集成**：使用 Bailian SDK 调用 `CreateIndex`、`AddFile`、`Retrieve` 等接口，完整流程见 [知识库API指南](../../raw/application-user-guide/knowledge-base/rag-knowledge-base-api-guide.md)；注意子账号需授予 `AliyunBailianDataFullAccess` 权限并加入业务空间。
- **调试与验证**：所有知识库均支持“命中测试”，可输入 Query 查看原始召回切片、相似度分数及元数据；日志服务（SLS）自动投递检索日志，用于审计与问题排查 [知识库日志与监控](../../raw/application-user-guide/knowledge-base/rag-knowledge-base-log-monitoring.md)。

## 限制和注意事项

- **地域限制**：知识库功能仅支持中国站华北2（北京）地域，新加坡、法兰克福等国际地域不可用 [知识库](../../raw/application-user-guide/knowledge-base/rag-knowledge-base.md)、[知识库API指南](../../raw/application-user-guide/knowledge-base/rag-knowledge-base-api-guide.md)。
- **配额硬限制**：
  - 单知识库文件数无硬上限（非结构化），但单次控制台导入上限为 50 个；
  - 文本切片长度上限 6000 字符，单文件切片数无限制；
  - 音视频搜索类知识库**不支持新增切片**，仅支持编辑与删除 [知识库配额与限制](../../raw/application-user-guide/knowledge-base/rag-knowledge-base-specifications.md)。
- **关键约束**：
  - Meta 信息抽取必须在创建知识库时配置，**创建后无法追加**；
  - “多轮对话改写”功能仅在创建知识库时开启，后续无法补开 [RAG效果优化](../../raw/application-user-guide/knowledge-base/rag-optimization.md)；
  - 标准版知识库固定 1 QPS 并发，不可调整；旗舰版 RCU 可调但需按小时分段计费。
- **成本提示**：模型调用费用（向量、Rerank、路由、问答）与规格费用（知识库运行时长）**独立计费**；Rerank 费用取决于初步召回总切片数（而非最终返回数），关闭排序或降低 TopK 是主要优化手段 [知识库计费说明](../../raw/application-user-guide/knowledge-base/billing-for-knowledge-base.md)。

## 来源文档

- [RAG效果优化](../../raw/application-user-guide/knowledge-base/rag-optimization.md)
- [知识库](../../raw/application-user-guide/knowledge-base/rag-knowledge-base.md)
- [知识库日志与监控](../../raw/application-user-guide/knowledge-base/rag-knowledge-base-log-monitoring.md)
- [知识库API指南](../../raw/application-user-guide/knowledge-base/rag-knowledge-base-api-guide.md)
- [知识库计费说明](../../raw/application-user-guide/knowledge-base/billing-for-knowledge-base.md)
- [知识问答](../../raw/application-user-guide/knowledge-base/rag-knowledge-qa.md)
- [知识库配额与限制](../../raw/application-user-guide/knowledge-base/rag-knowledge-base-specifications.md)
- [知识检索](../../raw/application-user-guide/knowledge-base/rag-knowledge-retrieval.md)



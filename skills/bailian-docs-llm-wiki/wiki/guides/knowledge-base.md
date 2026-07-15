# [knowledge](../api/knowledge.md) base

知识库是阿里云百炼平台提供的核心 RAG（[检索增强生成](../concepts/rag.md)）能力组件，用于为大模型注入私有数据与领域知识，提升回答的准确性与专业性。它支持文档、表格、图片、音视频等多模态数据的语义索引与检索，并可灵活集成至智能体、工作流或外部应用中。所有知识库功能目前仅在中国站华北2（北京）地域可用。

## 支持的模型/功能

知识库支持与多种预置及自定义大模型协同工作，包括千问系列（QwQ/Long/Max/Plus/Turbo/Coder/Deep-Research）、千问VL系列（Max/Plus/Flash/OCR）、开源版（Qwen3、Qwen2.5、Qwen2）以及第三方模型（DeepSeek-R1、Llama3.1、Yi-Large 等）[知识库](../../raw/application-user-guide/knowledge-base/rag-knowledge-base.md)。  
功能层面，知识库提供**文档搜索**（含基础问答、图文并茂、视觉理解、极速问答四类场景）、**数据查询**（结构化表格）、**图片问答**和**音视频搜索**四类知识库类型，分别适配不同数据形态与业务需求 [知识库](../../raw/application-user-guide/knowledge-base/rag-knowledge-base.md)。  
此外，平台还提供上层服务封装：**知识检索**服务支持多知识库联合检索与精细化参数控制；**知识问答**服务则进一步整合大模型生成能力，支持极速模式与多轮智能（Agentic）模式，实现端到端自然语言问答 [知识检索](../../raw/application-user-guide/knowledge-base/rag-knowledge-retrieval.md)。

> **注意**：文档 2 中列出的“千问-开源版（Qwen3、Qwen2.5、Qwen2等）”在文档 8 的问答服务模型列表中具体体现为 `qwen3.6-plus`、`qwen3.7-plus` 等版本号命名方式，二者指向同一模型族，但文档 8 的命名更精确反映当前控制台实际可选项，建议以控制台实时列表为准。

## 关键参数

知识库的核心行为由以下关键参数控制：

- **切片策略**：推荐使用“智能切分”，该策略基于语义相关性自适应划分文本，优于固定长度切分，能有效避免语义截断或信息混杂 [RAG效果优化](../../raw/application-user-guide/knowledge-base/rag-optimization.md)。
- **Meta信息抽取**：可在创建知识库时配置，将 `file_name`、`date`、正则匹配结果等作为元数据嵌入文本切片，显著提升定向检索精度（如按产品型号精准召回其功能概述）[知识库](../../raw/application-user-guide/knowledge-base/rag-knowledge-base.md)。
- **相似度阈值**（0.01–1.0）：作用于重排（Rerank）后结果，过滤低分切片。设置过高易导致漏召回，过低则引入噪声；需通过命中测试反复调优 [RAG效果优化](../../raw/application-user-guide/knowledge-base/rag-optimization.md)。
- **召回数量**：单次查询最多返回 20 个文本切片（`max_retrieve_count`），而初步向量/关键词检索 TopK 可设为 1–100，直接影响 Rerank 模型的 [Token](../concepts/token.md) 消耗与费用 [知识库配额与限制](../../raw/application-user-guide/knowledge-base/rag-knowledge-base-specifications.md)。
- **标签过滤**：支持为文件添加最多 32 个标签，并在检索时通过 `tags` 参数（API）或调试界面（控制台）指定，实现基于业务维度的精准筛选 [RAG效果优化](../../raw/application-user-guide/knowledge-base/rag-optimization.md)。

## 使用方式

知识库可通过三种方式集成：

1. **控制台快速构建**：进入[知识库](https://bailian.console.aliyun.com/?tab=app#/knowledge-base)页面，选择标准版或旗舰版，上传文件（支持 PDF/DOCX/TXT/图片等，详见[知识库配额与限制](../../raw/application-user-guide/knowledge-base/rag-knowledge-base-specifications.md)），完成索引配置后，即可绑定至智能体或工作流应用。
2. **API 集成**：通过阿里云百炼 SDK 调用完整生命周期 API，包括 `ApplyFileUploadLease`、`AddFile`、`CreateIndex`、`SubmitIndexJob` 等，适用于自动化部署与复杂数据管道 [知识库API指南](../../raw/application-user-guide/knowledge-base/rag-knowledge-base-api-guide.md)。
3. **上层服务调用**：
   - **知识检索服务**：创建后可统一管理多个知识库的联合检索逻辑，支持 Query 改写、混合检索与混排模型。
   - **知识问答服务**：在检索基础上叠加大模型生成，支持拒答、防泄漏、引用溯源等生产级控制能力 [知识问答](../../raw/application-user-guide/knowledge-base/rag-knowledge-qa.md)。

## 限制和注意事项

- **地域限制**：知识库功能**仅限华北2（北京）地域**，其他地域（如新加坡、法兰克福）不支持，此限制同时适用于控制台操作与 API 调用 [知识库](../../raw/application-user-guide/knowledge-base/rag-knowledge-base.md)。
- **配额硬限**：单个知识库文件数量无硬上限，但单个文件大小受限（如 PDF 最大 150MB，图片最大 20MB）；文本切片长度上限为 6,000 [Token](../concepts/token.md)；检索并发方面，标准版固定为 1 QPS，旗舰版可调范围为 50–10,000 QPS [知识库配额与限制](../../raw/application-user-guide/knowledge-base/rag-knowledge-base-specifications.md)。
- **元数据不可变**：知识库创建后，**无法再配置或修改 Meta 信息抽取规则**，必须在创建阶段一次性设定 [知识库](../../raw/application-user-guide/knowledge-base/rag-knowledge-base.md)。
- **计费要点**：自 2026 年 1 月 4 日起正式计费，费用分为规格费（按小时）与模型调用费（按 [Token](../concepts/token.md)）。其中，Rerank 排序费用取决于**初步召回总切片数**，而非最终返回数，调整 `TopK` 是成本优化关键 [知识库计费说明](../../raw/application-user-guide/knowledge-base/billing-for-knowledge-base.md)。
- **日志监控**：所有检索请求自动投递至 SLS 日志服务，字段包含 `request_id`、`pipeline_id`（即知识库 ID）、`latency`、`response_code` 等，可用于审计、问题排查与用量分析 [知识库日志与监控](../../raw/application-user-guide/knowledge-base/rag-knowledge-base-log-monitoring.md)。

## 来源文档

- [RAG效果优化](../../raw/application-user-guide/knowledge-base/rag-optimization.md)
- [知识库](../../raw/application-user-guide/knowledge-base/rag-knowledge-base.md)
- [知识库日志与监控](../../raw/application-user-guide/knowledge-base/rag-knowledge-base-log-monitoring.md)
- [知识库API指南](../../raw/application-user-guide/knowledge-base/rag-knowledge-base-api-guide.md)
- [知识库配额与限制](../../raw/application-user-guide/knowledge-base/rag-knowledge-base-specifications.md)
- [知识检索](../../raw/application-user-guide/knowledge-base/rag-knowledge-retrieval.md)
- [知识库计费说明](../../raw/application-user-guide/knowledge-base/billing-for-knowledge-base.md)
- [知识问答](../../raw/application-user-guide/knowledge-base/rag-knowledge-qa.md)



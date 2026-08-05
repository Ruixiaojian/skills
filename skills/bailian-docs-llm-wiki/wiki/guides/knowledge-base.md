# [knowledge](../api/knowledge.md) base

知识库是阿里云百炼平台提供的 RAG（[检索增强生成](../concepts/rag.md)）核心能力，用于为大语言模型注入私有、结构化或非结构化数据，提升其在垂直领域回答的准确性与时效性。它支持文档、表格、图片、音视频等多种数据源，并通过语义检索、多模态向量化与重排序等技术实现高质量召回。知识库功能仅在中国站华北2（北京）地域可用。

## 支持的模型/功能

知识库支持与多种预置及自定义模型协同工作。预置模型包括千问系列（QwQ/Long/Max/Plus/Turbo/Coder/Deep-Research、VL-Max/Plus/Flash/OCR、开源版 Qwen3/Qwen2.5/Qwen2 等），以及第三方模型（DeepSeek-R1、Llama3.1、Yi-Large 等）；自定义模型需基于上述基座调优后方可使用 [知识库 (raw/application-user-guide/knowledge-base/rag-knowledge-base.md)](../../raw/application-user-guide/knowledge-base/rag-knowledge-base.md)。  
知识库本身不直接提供生成能力，而是作为检索服务被集成至智能体应用、工作流应用或外部系统中，支持单库检索、多知识库联合检索 [知识检索 (raw/application-user-guide/knowledge-base/rag-knowledge-retrieval.md)](../../raw/application-user-guide/knowledge-base/rag-knowledge-retrieval.md) 和端到端问答服务 [知识问答 (raw/application-user-guide/knowledge-base/rag-knowledge-qa.md)](../../raw/application-user-guide/knowledge-base/rag-knowledge-qa.md)。  
> **注意**：文档 1 中列出的“千问-开源版（Qwen3、Qwen2.5、Qwen2等）”在文档 6 的模型调用费用章节中被明确限定为 `qwen3.6-plus`、`qwen3.7-plus` 等具体版本号，且 `qwen3-rerank`、`qwen3-vl-rerank` 等排序模型亦为独立计费项，表明“Qwen3”等泛称在实际部署中需对应具体模型 ID，不可直接等同使用。

## 关键参数

知识库检索效果受多个可配置参数影响，分为全局与知识库级两类：
- **全局参数**（适用于多知识库联合检索）：`最大召回数量`（1–20）、`知识库路由`（开/关，启用后调用 `qwen-plus` 进行意图判断）、`混排模型`（如 `qwen3-rerank` 或 `qwen3-vl-rerank`）及 `混排模型模式`（问答模式/相似模式）。
- **知识库级参数**：`初步向量检索 TopK`（1–100，默认 50）、`初步关键词检索 TopK`（1–100，默认 50）、`相似度阈值`（0.01–1.0，控制召回精度）、`标签过滤`（按业务标签筛选文件）、`结构化字段过滤`（仅表格库支持）[知识检索 (raw/application-user-guide/knowledge-base/rag-knowledge-retrieval.md)](../../raw/application-user-guide/knowledge-base/rag-knowledge-retrieval.md)。  
此外，创建知识库时需选择 `解析方式`（电子文档/文档智能/大模型文档/Qwen VL/音视频解析）和 `切片策略`（推荐“智能切分”以保障语义完整性）[RAG效果优化 (raw/application-user-guide/knowledge-base/rag-optimization.md)](../../raw/application-user-guide/knowledge-base/rag-optimization.md)。

## 使用方式

知识库可通过控制台可视化操作或 API 编程集成两种方式使用：
- **控制台集成**：在智能体应用中，于“文档知识库”模块点击 `+` 添加知识库，并配置相似度阈值与权重；在工作流应用中，拖入“知识库”节点，配置 `content` 输入变量（通常为 `query`）、选择知识库（固定或动态）、设置 `TopK`，再连接大模型节点并插入 `{result}` 变量 [知识库 (raw/application-user-guide/knowledge-base/rag-knowledge-base.md)](../../raw/application-user-guide/knowledge-base/rag-knowledge-base.md)。
- **API 集成**：通过百炼 SDK 调用知识库 API，支持创建、上传文件、构建索引及检索。需完成前置步骤：子账号获取 `AliyunBailianDataFullAccess` 权限、加入业务空间、配置 AccessKey 与 `WORKSPACE_ID`，且仅支持文档搜索类知识库 [知识库API指南 (raw/application-user-guide/knowledge-base/rag-knowledge-base-api-guide.md)](../../raw/application-user-guide/knowledge-base/rag-knowledge-base-api-guide.md)。  
定时同步能力可通过[数据连接](../concepts/data-connection.md)器配置 OSS/飞书/钉钉等来源的同步规则，支持分钟/小时/日级周期 [知识库定时数据同步指南 (raw/application-user-guide/knowledge-base/data-sync-guide.md)](../../raw/application-user-guide/knowledge-base/data-sync-guide.md)。

## 限制和注意事项

- **地域限制**：知识库功能严格限定于中国站华北2（北京）地域，新加坡、法兰克福等国际地域均不支持 [知识库 (raw/application-user-guide/knowledge-base/rag-knowledge-base.md)](../../raw/application-user-guide/knowledge-base/rag-knowledge-base.md)。
- **配额与规格**：标准版知识库最高 1 QPS 并限 100 GB 存储；旗舰版支持 50–10,000 QPS（按 RCU 计费）及最高 9,999 GB 存储；单次导入文件上限 50 个，单文件最大 150 MB（PDF/DOCX）或 20 MB（图片）[知识库配额与限制 (raw/application-user-guide/knowledge-base/rag-knowledge-base-specifications.md)](../../raw/application-user-guide/knowledge-base/rag-knowledge-base-specifications.md)。
- **计费说明**：费用由两部分构成——知识库规格费用（标准版 0.03 元/小时，旗舰版 0.2 元/RCU/小时）与模型调用费用（向量模型 `text-embedding-v4`、排序模型 `qwen3-rerank`、问答模型如 `qwen3.7-plus` 等均按 [Token](../concepts/token.md) 单独计费）。特别注意：Rerank 排序费用取决于**初步召回总切片数**，而非最终返回数量 [知识库计费说明 (raw/application-user-guide/knowledge-base/billing-for-knowledge-base.md)](../../raw/application-user-guide/knowledge-base/billing-for-knowledge-base.md)。
- **元数据与标签**：`Meta信息抽取` 必须在创建知识库时配置，创建后无法追加；而 `标签` 可在上传时或后续编辑，用于运行时过滤 [RAG效果优化 (raw/application-user-guide/knowledge-base/rag-optimization.md)](../../raw/application-user-guide/knowledge-base/rag-optimization.md)。

## 来源文档

- [知识库](../../raw/application-user-guide/knowledge-base/rag-knowledge-base.md)
- [RAG效果优化](../../raw/application-user-guide/knowledge-base/rag-optimization.md)
- [知识库API指南](../../raw/application-user-guide/knowledge-base/rag-knowledge-base-api-guide.md)
- [知识库日志与监控](../../raw/application-user-guide/knowledge-base/rag-knowledge-base-log-monitoring.md)
- [知识库定时数据同步指南](../../raw/application-user-guide/knowledge-base/data-sync-guide.md)
- [知识库计费说明](../../raw/application-user-guide/knowledge-base/billing-for-knowledge-base.md)
- [知识检索](../../raw/application-user-guide/knowledge-base/rag-knowledge-retrieval.md)
- [知识问答](../../raw/application-user-guide/knowledge-base/rag-knowledge-qa.md)
- [知识库配额与限制](../../raw/application-user-guide/knowledge-base/rag-knowledge-base-specifications.md)



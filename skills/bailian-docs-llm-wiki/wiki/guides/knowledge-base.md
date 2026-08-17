# [knowledge](../api/knowledge.md) base

知识库是阿里云百炼平台提供的核心 RAG（[检索增强生成](../concepts/rag.md)）能力组件，用于为大模型注入私有、结构化或非结构化领域知识，从而提升回答的准确性与专业性。其本质是将文档解析、向量化、语义检索与大模型生成进行端到端集成，支持从单知识库问答到多知识库联合检索与智能问答的完整链路。所有知识库功能仅在中国站华北2（北京）地域可用。

## 支持的模型与功能

知识库支持与多种预置及自定义模型协同工作。预置模型包括千问全系列（QwQ/Long/Max/Plus/Turbo/Coder/Deep-Research、VL-Max/Plus/Flash/OCR、开源版 Qwen3/Qwen2.5/Qwen2）及第三方模型（DeepSeek-R1、Llama3.1、Yi-Large 等）；自定义模型需基于上述模型调优后方可使用 [知识库](../../raw/application-user-guide/knowledge-base/rag-knowledge-base.md)。知识库本身不直接参与生成，而是通过以下两类服务提供能力：

- **知识检索**：支持单/多知识库联合检索（最多 15 个），具备 Query 改写、混合检索（向量 + 关键词）、Rerank 排序及精细化参数控制，适用于需要返回原始切片的下游系统集成场景 [知识检索](../../raw/application-user-guide/knowledge-base/rag-knowledge-retrieval.md)。
- **知识问答**：在检索基础上，自动调用大模型生成自然语言回答，支持极速模式（单轮）与多轮智能模式（Agentic 规划搜索），并提供拒答、防泄漏、引用溯源、[多模态](../concepts/multi-modal.md)回复等生成控制能力 [知识问答](../../raw/application-user-guide/knowledge-base/rag-knowledge-qa.md)。

> **注意**：文档 2 中列出的“千问-开源版（Qwen3、Qwen2.5、Qwen2等）”在文档 7 的模型调用费用说明中被具体化为 `qwen3.6-plus` 和 `qwen3.7-plus` 等实际可选型号，且明确指出问答模型费用独立于知识库规格费用。开发者应以控制台实际可选模型为准，避免依赖文档中未更新的泛称。

## 关键参数

知识库效果高度依赖以下可配置参数，需根据业务场景权衡精度与性能：

- **相似度阈值（0.01–1.0）**：过滤排序后低分切片。值过高易漏召回，过低则引入噪声。建议通过命中测试反复验证 [RAG效果优化](../../raw/application-user-guide/knowledge-base/rag-optimization.md)。
- **召回片段数（TopK）**：控制最终返回给大模型的切片数量（上限 20）。复杂问题（如对比、总结）需适当提高，但会增加 [Token](../concepts/token.md) 消耗。
- **初步向量/关键词检索 TopK（1–100）**：影响 Rerank 阶段的输入规模，直接决定排序模型调用费用（费用 = 初步召回总切片数 × 平均切片 [Token](../concepts/token.md) 数 × 单价）[知识库计费说明](../../raw/application-user-guide/knowledge-base/billing-for-knowledge-base.md)。
- **标签过滤与元数据（metadata）**：用于结构化筛选。标签可在上传时或数据管理页设置；元数据需在创建知识库时配置，创建后不可修改，是解决“召回不相关”问题的核心手段 [RAG效果优化](../../raw/application-user-guide/knowledge-base/rag-optimization.md)。
- **多轮对话改写**：在创建知识库的索引设置中启用，可自动补全用户查询中的指代与上下文省略，显著提升多轮对话下的检索准确率，但仅对当前知识库生效且创建后不可追加 [RAG效果优化](../../raw/application-user-guide/knowledge-base/rag-optimization.md)。

## 使用方式

知识库可通过控制台、工作流/智能体应用或 API 三种方式集成：

- **控制台快速构建**：进入知识库页面，选择标准版/旗舰版 → 填写基础信息 → 上传文件（支持 PDF/DOCX/TXT/图片/音视频等）→ 设置索引（含解析方式、Meta 信息抽取、多轮改写等）→ 完成创建。随后可在知识检索或知识问答标签页创建对应服务并发布 [知识库](../../raw/application-user-guide/knowledge-base/rag-knowledge-base.md)。
- **集成至智能体/工作流应用**：在应用配置中添加“文档知识库”节点，选择知识库并配置相似度阈值、权重（多知识库时生效）；或在工作流画布中拖入“知识库”节点，配置 `content` 输入（通常为 `query`）、TopK 及动态知识库选择逻辑 [知识库](../../raw/application-user-guide/knowledge-base/rag-knowledge-base.md)。
- **API 集成**：通过百炼 SDK 调用 `CreateIndex`、`AddFile`、`Retrieve` 等接口实现自动化管理与检索。注意：API 仅适用于文档搜索类知识库，且需完成子账号权限配置、AccessKey 设置及业务空间 ID 注入 [知识库API指南](../../raw/application-user-guide/knowledge-base/rag-knowledge-base-api-guide.md)。

## 限制和注意事项

- **地域限制**：知识库功能仅限中国站华北2（北京）地域，其他地域（如新加坡、法兰克福）完全不可用，此限制同时适用于控制台操作与 API 调用 [知识库](../../raw/application-user-guide/knowledge-base/rag-knowledge-base.md)、[知识库API指南](../../raw/application-user-guide/knowledge-base/rag-knowledge-base-api-guide.md)。
- **配额与存储**：标准版知识库免费存储上限 100 GB，旗舰版为 9,999 GB；单个知识库文件数量无硬性上限（非结构化），但单次控制台导入上限 50 个文件；文本切片长度上限 6,000 字符 [知识库配额与限制](../../raw/application-user-guide/knowledge-base/rag-knowledge-base-specifications.md)。
- **计费关键点**：费用分为规格费（按小时）与模型调用费（按 [Token](../concepts/token.md)）。规格费取决于知识库类型（标准版 0.03 元/小时，旗舰版按 RCU 计费）；模型调用费包含向量模型（text-embedding-v4/qwen3-vl-embedding）、Rerank 模型（qwen3-rerank/qwen3-vl-rerank）及问答模型（qwen3.7-plus 等）三类，其中 Rerank 费用与初步召回切片总数强相关，而非最终返回数 [知识库计费说明](../../raw/application-user-guide/knowledge-base/billing-for-knowledge-base.md)。
- **同步与更新**：通过 OSS/飞书/钉钉等来源的定时同步规则，可实现增量更新；但同步文件为独立副本，源文件删除不影响百炼平台内数据，需手动清理 [知识库定时数据同步指南](../../raw/application-user-guide/knowledge-base/data-sync-guide.md)。
- **日志与监控**：所有检索请求日志默认投递至 SLS，字段包含 `request_id`、`pipeline_id`（知识库 ID）、`latency`、`response_code` 及 `response_body.data.nodes[]`（含召回切片文本与分数），可用于审计、排查与用量分析 [知识库日志与监控](../../raw/application-user-guide/knowledge-base/rag-knowledge-base-log-monitoring.md)。

## 来源文档

- [RAG效果优化](../../raw/application-user-guide/knowledge-base/rag-optimization.md)
- [知识库](../../raw/application-user-guide/knowledge-base/rag-knowledge-base.md)
- [知识库定时数据同步指南](../../raw/application-user-guide/knowledge-base/data-sync-guide.md)
- [知识库日志与监控](../../raw/application-user-guide/knowledge-base/rag-knowledge-base-log-monitoring.md)
- [知识库配额与限制](../../raw/application-user-guide/knowledge-base/rag-knowledge-base-specifications.md)
- [知识库API指南](../../raw/application-user-guide/knowledge-base/rag-knowledge-base-api-guide.md)
- [知识库计费说明](../../raw/application-user-guide/knowledge-base/billing-for-knowledge-base.md)
- [知识检索](../../raw/application-user-guide/knowledge-base/rag-knowledge-retrieval.md)
- [知识问答](../../raw/application-user-guide/knowledge-base/rag-knowledge-qa.md)



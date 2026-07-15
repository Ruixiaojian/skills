# [knowledge](../api/knowledge.md) base

知识库是阿里云百炼平台提供的 RAG（[检索增强生成](../concepts/rag.md)）核心能力，用于为大模型注入私有、领域专属或时效性强的结构化与非结构化数据。它通过语义检索从文档、表格、音视频等多源内容中精准召回相关信息，并将其作为上下文输入大模型，从而显著提升回答的准确性、专业性与可溯源性。知识库功能仅在中国站华北2（北京）地域可用，且需在业务空间内完成创建与集成。

## 支持的模型/功能

知识库支持与阿里云百炼平台上的多种预置及自定义模型协同工作。预置模型包括千问全系列（QwQ/Long/Max/Plus/Turbo/Coder/Deep-Research、VL-Max/Plus/Flash/OCR、开源版 Qwen3/Qwen2.5/Qwen2 等），以及第三方文本模型（如 DeepSeek-R1、Llama3.1、Yi-Large 等）。经调优的自定义模型（如千问-Plus/Turbo、Qwen3 开源版调优模型等）同样支持 [原文标题](../../raw/application-user-guide/knowledge-base/rag-knowledge-base.md)。

除基础文档问答外，知识库还提供面向不同场景的专用能力：  
- **知识检索服务**：支持最多 15 个知识库联合检索，具备 Query 改写、混合检索（向量+关键词）、Rerank 排序及精细化参数控制；  
- **知识问答服务**：在检索基础上叠加大模型生成，支持极速模式（单轮）与多轮智能模式（Agentic 规划搜索），并提供拒答、防泄漏、引用溯源等生成控制能力 [原文标题](../../raw/application-user-guide/knowledge-base/rag-knowledge-qa.md)。  
> **注意**：文档 1 中列出的“千问VL-Max/Plus/OCR”等视觉模型，在文档 7 和 8 的检索/问答服务配置项中明确限定为“多模态知识库（图片知识库、视觉理解知识库）”专用，不可用于纯文本知识库的排序（rerank）；而纯文本知识库仅支持 `qwen3-rerank` 系列模型。该差异表明模型支持范围需严格按知识库类型和功能模块区分，不可跨类型泛化使用。

## 关键参数

知识库的核心行为由以下关键参数控制：  
- **相似度阈值（0.01–1.0）**：作用于 Rerank 排序后结果，仅保留得分高于该阈值的切片。值过高易漏召，过低则引入噪声；  
- **初步向量/关键词检索 TopK（1–100）**：分别控制向量与关键词双路召回的初始切片数，直接影响 Rerank 模型的 Token 消耗与最终精度；  
- **最大召回数量（1–20）**：指最终返回给下游（大模型节点或问答服务）的切片总数；  
- **权重与标签过滤**：多知识库场景下，权重影响混排优先级；标签（单文件最多 32 个）支持按业务维度（如 `bailian_mobile`）进行精准范围过滤 [原文标题](../../raw/application-user-guide/knowledge-base/rag-optimization.md)；  
- **元数据（metadata）抽取**：在索引阶段为文本切片注入 `filename`、`date`、`author` 等结构化信息，实现“先过滤、再检索”，大幅提升高相似度干扰场景下的准确率。

## 使用方式

知识库可通过三种方式集成到应用中：  
1. **智能体/工作流应用内嵌**：在应用配置页点击“文档知识库”旁的 `+` 添加知识库，设置相似度阈值与权重；工作流中需拖入“知识库节点”，配置 `content` 输入变量（通常为 `query`）及 `TopK`，再连接至大模型节点，并在提示词中引用 `{result}` 变量；  
2. **独立服务形态**：通过控制台“知识检索”或“知识问答”标签页创建服务，绑定多个知识库并统一配置混排模型、路由策略与生成参数，发布后即可通过 API 或调试窗口直接调用；  
3. **外部系统集成**：使用阿里云百炼 SDK（Python/Java 等）调用知识库 API，完成创建、上传、索引、检索全流程自动化。API 调用需子账号具备 `AliyunBailianDataFullAccess` 权限，并配置 `ALIBABA_CLOUD_ACCESS_KEY_ID` 等环境变量 [原文标题](../../raw/application-user-guide/knowledge-base/rag-knowledge-base-api-guide.md)。

## 限制和注意事项

- **地域限制**：知识库功能仅支持中国站华北2（北京）地域，新加坡、法兰克福等其他地域不支持，此限制在文档 1 与文档 4 中均被明确强调；  
- **配额约束**：标准版知识库并发固定为 1 QPS，旗舰版为 50–10,000 QPS（按 RCU 计费）；单次控制台导入文件上限 50 个，单个文件最大 150MB（PDF/DOCX）；文本切片长度上限 6,000 Token；  
- **计费要点**：费用分为两部分——**规格费用**（按知识库运行时长，标准版 0.03 元/小时，旗舰版 0.2 元/RCU/小时）与**模型调用费用**（向量模型与 Rerank 模型按实际 Token 消耗计费，不包含在规格费中）；  
- **配置不可逆性**：知识库创建后，类型（如“文档搜索”）、元数据抽取配置、多轮对话改写开关均无法修改，需重建知识库；  
- **日志监控**：所有检索请求自动投递至 SLS 日志服务，字段如 `pipeline_id`（知识库 ID）、`response_code`（业务响应码）、`data.nodes[]`（召回切片）可用于审计与问题排查 [原文标题](../../raw/application-user-guide/knowledge-base/rag-knowledge-base-log-monitoring.md)。

## 来源文档

- [知识库](../../raw/application-user-guide/knowledge-base/rag-knowledge-base.md)
- [RAG效果优化](../../raw/application-user-guide/knowledge-base/rag-optimization.md)
- [知识库日志与监控](../../raw/application-user-guide/knowledge-base/rag-knowledge-base-log-monitoring.md)
- [知识库API指南](../../raw/application-user-guide/knowledge-base/rag-knowledge-base-api-guide.md)
- [知识库配额与限制](../../raw/application-user-guide/knowledge-base/rag-knowledge-base-specifications.md)
- [知识库计费说明](../../raw/application-user-guide/knowledge-base/billing-for-knowledge-base.md)
- [知识检索](../../raw/application-user-guide/knowledge-base/rag-knowledge-retrieval.md)
- [知识问答](../../raw/application-user-guide/knowledge-base/rag-knowledge-qa.md)



# [knowledge](../api/knowledge.md) base

知识库是阿里云百炼平台提供的 RAG（[检索增强生成](../concepts/rag.md)）核心能力，用于为大语言模型注入私有数据与领域知识，提升回答的准确性、时效性与专业性。其本质是将非结构化/半结构化数据（文档、表格、图片、音视频等）解析、切片、向量化并建立可检索索引，再在推理时动态召回相关片段供大模型参考。该功能仅在中国站华北2（北京）地域可用。

## 支持的模型/功能

知识库支持与多种预置及自定义模型协同工作。预置模型包括千问全系列（QwQ/Long/Max/Plus/Turbo/Coder/Deep-Research、VL-Max/Plus/Flash/OCR、开源版 Qwen3/Qwen2.5/Qwen2 等），以及第三方文本模型（DeepSeek-R1、Llama3.1、Yi-Large 等）。自定义模型需基于上述基座调优后方可使用 [知识库 (raw/application-user-guide/knowledge-base/rag-knowledge-base.md)](../../raw/application-user-guide/knowledge-base/rag-knowledge-base.md)。

知识库提供三类核心服务：**知识问答**（端到端问答应用）、**知识检索**（返回原始切片结果）和**知识库 API**（供外部系统集成）。其中，知识问答支持极速模式（单轮检索+生成）与多轮智能模式（Agentic 规划搜索）；知识检索支持多知识库联合检索与混排；API 服务则面向开发者提供完整的生命周期管理能力 [知识问答 (raw/application-user-guide/knowledge-base/rag-knowledge-qa.md)](../../raw/application-user-guide/knowledge-base/rag-knowledge-qa.md)。

> **注意**：文档 1 中列出的“千问-开源版（Qwen3、Qwen2.5、Qwen2等）”与文档 5 中计费说明里明确提及的 `qwen3.6-plus`、`qwen3.7-plus` 存在版本命名不一致问题。实际选型应以控制台应用配置页中实时可选的模型为准，且 `qwen3.7-plus` 等已明确用于知识问答服务，建议优先采用该命名体系。

## 关键参数

知识库效果高度依赖以下关键参数配置：

- **相似度阈值（0.01–1.0）**：过滤排序后低分切片。值过高易漏召，过低则引入噪声。该阈值作用于重排（Rerank）后的最终分数 [知识库 (raw/application-user-guide/knowledge-base/rag-knowledge-base.md)](../../raw/application-user-guide/knowledge-base/rag-knowledge-base.md)。
- **TopK（初步向量/关键词检索）**：控制各阶段初步召回数量（默认均为 50）。增大可提升召回完整性，但会显著增加 Rerank 模型 Token 消耗与延迟 [知识问答 (raw/application-user-guide/knowledge-base/rag-knowledge-qa.md)](../../raw/application-user-guide/knowledge-base/rag-knowledge-qa.md)。
- **最大召回数量（1–20）**：决定最终返回给大模型的切片数。此值直接影响输入 Token 量与回答质量平衡点。
- **元数据（Metadata）与标签（Tags）**：用于结构化过滤。元数据在索引创建时配置且不可修改，适用于文件级属性（如 `filename`, `date`）；标签可在上传或后续编辑时设置，适用于分类筛选（如 `bailian_mobile`），支持“与/或”逻辑匹配 [RAG效果优化 (raw/application-user-guide/knowledge-base/rag-optimization.md)](../../raw/application-user-guide/knowledge-base/rag-optimization.md)。

## 使用方式

知识库可通过三种方式集成：
1. **控制台可视化配置**：在应用管理页为智能体或工作流应用添加“文档知识库”节点，或直接创建知识问答/知识检索服务；
2. **SDK/API 集成**：使用百炼 SDK 调用 `CreateIndex`、`Retrieve` 等接口，实现自动化知识库管理与检索 [知识库API指南 (raw/application-user-guide/knowledge-base/rag-knowledge-base-api-guide.md)](../../raw/application-user-guide/knowledge-base/rag-knowledge-base-api-guide.md)；
3. **日志监控**：开通 SLS 日志服务后，可基于 `request_id`、`pipeline_id`、`latency` 等字段进行用量统计、错误排查与性能分析 [知识库日志与监控 (raw/application-user-guide/knowledge-base/rag-knowledge-base-log-monitoring.md)](../../raw/application-user-guide/knowledge-base/rag-knowledge-base-log-monitoring.md)。

## 限制和注意事项

- **地域限制**：知识库功能严格限定于中国站华北2（北京）地域，新加坡、法兰克福等国际地域均不支持 [知识库 (raw/application-user-guide/knowledge-base/rag-knowledge-base.md)](../../raw/application-user-guide/knowledge-base/rag-knowledge-base.md)。
- **配额限制**：单账号标准版知识库数量无硬上限，但旗舰版受 RCU 并发配额约束；单个知识库平台存储上限为标准版 100 GB、旗舰版 9,999 GB；单次控制台导入文件数上限为 50 个 [知识库配额与限制 (raw/application-user-guide/knowledge-base/rag-knowledge-base-specifications.md)](../../raw/application-user-guide/knowledge-base/rag-knowledge-base-specifications.md)。
- **计费要点**：费用由两部分构成——**规格费用**（按知识库运行时长计费，标准版 0.03 元/小时，旗舰版按 RCU 计费）和**模型调用费用**（独立计费，含向量模型、Rerank 模型、路由模型及问答模型的 Token 消耗）。特别注意：Rerank 费用取决于初步召回总切片数，而非最终返回数 [知识库计费说明 (raw/application-user-guide/knowledge-base/billing-for-knowledge-base.md)](../../raw/application-user-guide/knowledge-base/billing-for-knowledge-base.md)。
- **配置不可变性**：知识库类型（如文档搜索/视觉理解）与元数据抽取配置在创建后无法修改，需谨慎选择；多轮对话改写功能也必须在创建时开启，后续无法补开 [RAG效果优化 (raw/application-user-guide/knowledge-base/rag-optimization.md)](../../raw/application-user-guide/knowledge-base/rag-optimization.md)。

## 来源文档

- [知识库](../../raw/application-user-guide/knowledge-base/rag-knowledge-base.md)
- [RAG效果优化](../../raw/application-user-guide/knowledge-base/rag-optimization.md)
- [知识库日志与监控](../../raw/application-user-guide/knowledge-base/rag-knowledge-base-log-monitoring.md)
- [知识库API指南](../../raw/application-user-guide/knowledge-base/rag-knowledge-base-api-guide.md)
- [知识库计费说明](../../raw/application-user-guide/knowledge-base/billing-for-knowledge-base.md)
- [知识问答](../../raw/application-user-guide/knowledge-base/rag-knowledge-qa.md)
- [知识检索](../../raw/application-user-guide/knowledge-base/rag-knowledge-retrieval.md)
- [知识库配额与限制](../../raw/application-user-guide/knowledge-base/rag-knowledge-base-specifications.md)



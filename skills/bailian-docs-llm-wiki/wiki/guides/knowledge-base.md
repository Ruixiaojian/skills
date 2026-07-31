# [knowledge](../api/knowledge.md) base

知识库是阿里云百炼平台提供的 RAG（[检索增强生成](../concepts/rag.md)）核心能力，用于为大语言模型注入私有、领域专属或时效性强的结构化与非结构化数据，从而提升模型回答的准确性、专业性与事实一致性。其本质是将用户数据通过解析、切片、向量化、索引与语义检索等环节，构建可被大模型动态引用的外部知识源。所有知识库功能仅在中国站华北2（北京）地域可用。

## 支持的模型/功能

知识库支持与多种预置及自定义模型协同工作。预置模型包括千问全系列（QwQ/Long/Max/Plus/Turbo/Coder/Deep-Research、VL-Max/Plus/Flash/OCR、开源版 Qwen3/Qwen2.5/Qwen2 等），以及第三方文本模型（DeepSeek-R1、Llama3.1、Yi-Large 等）。自定义模型需基于上述基座调优后方可使用 [知识库 (raw/application-user-guide/knowledge-base/rag-knowledge-base.md)](../../raw/application-user-guide/knowledge-base/rag-knowledge-base.md)。

知识库提供三类核心服务：**知识检索**（纯召回）、**知识问答**（检索+生成）和**知识库 API**（程序化集成）。其中，知识检索支持多知识库联合检索（最多 15 个）、混合检索（向量+关键词）与重排序；知识问答支持极速模式与多轮智能（Agentic）模式，并具备文件预解析、拒答、防泄漏、[多模态](../concepts/multi-modal.md)回复与引用溯源等生成控制能力 [知识检索 (raw/application-user-guide/knowledge-base/rag-knowledge-retrieval.md)](../../raw/application-user-guide/knowledge-base/rag-knowledge-retrieval.md)。API 方式仅适用于文档搜索类知识库，不支持数据查询、图片问答或音视频搜索类 [知识库API指南 (raw/application-user-guide/knowledge-base/rag-knowledge-base-api-guide.md)](../../raw/application-user-guide/knowledge-base/rag-knowledge-base-api-guide.md)。

> **注意**：文档 1 中列出的“千问-开源版（Qwen3、Qwen2.5、Qwen2等）”在文档 6 的模型调用费用部分被明确列为问答阶段可选模型（如 `qwen3.7-plus`），但文档 1 同时将 `Qwen3` 列为预置模型，而文档 6 的计费说明中未提及 `Qwen3` 本身作为向量或排序模型。实际支持情况应以控制台创建应用时可选模型为准，且 `Qwen3` 系列模型的向量化能力需依赖专用嵌入模型（如 `qwen3-vl-embedding`），而非 `Qwen3` 自身。

## 关键参数

知识库的核心行为由以下关键参数控制：

- **相似度阈值（0.01–1.0）**：作用于重排序后结果，仅保留得分高于该阈值的切片。值过高易漏召，过低则引入噪声。
- **召回片段数（1–20）**：最终返回给大模型的切片数量上限，直接影响输入 [Token](../concepts/token.md) 消耗与回答完整性。
- **初步向量/关键词检索 TopK（1–100）**：控制初步召回切片数量，直接决定后续重排序的计算量与费用（费用按初步召回总量计费，而非最终返回量）[知识库计费说明 (raw/application-user-guide/knowledge-base/billing-for-knowledge-base.md)](../../raw/application-user-guide/knowledge-base/billing-for-knowledge-base.md)。
- **权重与标签过滤**：多知识库场景下，权重影响同类型知识库间召回顺序；标签则用于在检索前对文件进行结构化筛选，提升精准度。
- **元数据（Metadata）**：在创建知识库时配置，可嵌入 `file_name`、`date`、正则匹配结果等，用于检索前的结构化过滤，显著改善多文件同质内容下的召回精度。

## 使用方式

知识库可通过控制台、工作流/智能体应用或 API 三种方式集成：

- **控制台快速构建**：进入「知识库」页面，选择标准版或旗舰版，上传文件（支持 PDF/DOCX/TXT/图片/音视频等），配置解析方式（电子文档/文档智能/大模型文档解析）与索引参数（如启用多轮对话改写、Meta 信息抽取）后完成创建 [知识库 (raw/application-user-guide/knowledge-base/rag-knowledge-base.md)](../../raw/application-user-guide/knowledge-base/rag-knowledge-base.md)。
- **集成到应用**：
  - *智能体应用*：在应用配置中点击「文档知识库」旁的 `+`，添加知识库并设置相似度阈值与权重。
  - *工作流应用*：拖入「知识库」节点，配置输入（如 `query`）、知识库选择方式（固定或动态）与 `TopK`，再连接至大模型节点，并在提示词中引用 `{result}` 变量。
- **API 集成**：通过百炼 SDK 调用 `ApplyFileUploadLease`、`AddFile`、`CreateIndex` 等接口实现自动化知识库生命周期管理，适用于 DevOps 或大规模知识同步场景 [知识库API指南 (raw/application-user-guide/knowledge-base/rag-knowledge-base-api-guide.md)](../../raw/application-user-guide/knowledge-base/rag-knowledge-base-api-guide.md)。

## 限制和注意事项

- **地域限制**：知识库功能严格限定于中国站华北2（北京）地域，其他地域（如新加坡、法兰克福）完全不可用，此限制在文档 1 和文档 3 中均被强调。
- **规格与配额**：标准版知识库最大并发为 1 QPS（固定），旗舰版为 50–10,000 QPS（可调）；单个知识库文件数量无硬性上限（文档搜索类），但单次控制台导入上限为 50 个文件；文本切片长度上限为 6000 字符 [知识库配额与限制 (raw/application-user-guide/knowledge-base/rag-knowledge-base-specifications.md)](../../raw/application-user-guide/knowledge-base/rag-knowledge-base-specifications.md)。
- **计费要点**：费用分为两部分——**规格费用**（按知识库运行时长计费，标准版 0.03 元/小时，旗舰版 0.2 元/RCU/小时）与**模型调用费用**（独立计费，含向量模型、排序模型、路由模型及问答模型的 [Token](../concepts/token.md) 消耗）。特别注意：排序费用取决于初步召回的总切片数，而非最终返回数；关闭排序可降低成本但降低精度 [知识库计费说明 (raw/application-user-guide/knowledge-base/billing-for-knowledge-base.md)](../../raw/application-user-guide/knowledge-base/billing-for-knowledge-base.md)。
- **元数据与切片限制**：知识库创建后无法再配置 Meta 信息抽取；音视频搜索类知识库不支持新增切片，仅支持编辑与删除 [知识库配额与限制 (raw/application-user-guide/knowledge-base/rag-knowledge-base-specifications.md)](../../raw/application-user-guide/knowledge-base/rag-knowledge-base-specifications.md)。
- **效果优化**：若召回不理想，优先检查源文件格式（避免复杂表格、水印）、启用元数据/标签过滤、调整切片策略（推荐「智能切分」）及通过命中测试迭代相似度阈值与 TopK 参数 [RAG效果优化 (raw/application-user-guide/knowledge-base/rag-optimization.md)](../../raw/application-user-guide/knowledge-base/rag-optimization.md)。

## 来源文档

- [知识库](../../raw/application-user-guide/knowledge-base/rag-knowledge-base.md)
- [RAG效果优化](../../raw/application-user-guide/knowledge-base/rag-optimization.md)
- [知识库API指南](../../raw/application-user-guide/knowledge-base/rag-knowledge-base-api-guide.md)
- [知识库日志与监控](../../raw/application-user-guide/knowledge-base/rag-knowledge-base-log-monitoring.md)
- [知识库配额与限制](../../raw/application-user-guide/knowledge-base/rag-knowledge-base-specifications.md)
- [知识库计费说明](../../raw/application-user-guide/knowledge-base/billing-for-knowledge-base.md)
- [知识检索](../../raw/application-user-guide/knowledge-base/rag-knowledge-retrieval.md)
- [知识问答](../../raw/application-user-guide/knowledge-base/rag-knowledge-qa.md)



# [knowledge](../api/knowledge.md) base

知识库是阿里云百炼平台提供的 RAG（[检索增强生成](../concepts/rag.md)）核心能力，用于为大语言模型注入私有、领域专属或时效性强的结构化与非结构化数据。它通过语义检索从文档、表格、音视频等多源数据中召回相关内容，并与大模型协同生成准确、可溯源的回答。该功能目前仅在中国站华北2（北京）地域可用。

## 支持的模型/功能

知识库支持与多种预置及自定义模型协同工作。**预置模型**包括千问全系列（QwQ/Long/Max/Plus/Turbo/Coder/Deep-Research、VL-Max/Plus/Flash/OCR、开源版 Qwen3/Qwen2.5/Qwen2 等）以及第三方文本模型（DeepSeek-R1、Llama3.1、Yi-Large 等）；**自定义模型**指在百炼平台调优后的千问系列模型（如 Plus/Turbo/VL-Max 等）[配置千问使用知识库教程](../../raw/application-user-guide/knowledge-base/rag-knowledge-base.md)。此外，知识库本身支持多模态处理：文档搜索类知识库可选「视觉理解」场景，自动启用 `qwen3-vl-embedding` 向量模型；图片问答类知识库则强制使用 `multimodal-embedding-v1` [知识库配额与限制](../../raw/application-user-guide/knowledge-base/rag-knowledge-base-specifications.md)。

功能层面，知识库提供三类服务形态：  
- **知识检索**：面向开发者，支持单/多知识库联合检索、Query 改写、混合检索（向量+关键词）与 Rerank 排序，最多绑定 15 个知识库 [知识检索](../../raw/application-user-guide/knowledge-base/rag-knowledge-retrieval.md)；  
- **知识问答**：面向终端用户，集成检索与生成，支持极速模式（单轮）与多轮智能模式（Agentic 规划），并提供文件预解析、拒答、防泄漏、引用溯源等生成控制能力；  
- **日志与监控**：所有检索调用实时投递至 SLS 日志服务，支持用量统计、错误排查与性能告警。

> **注意**：文档 1 中列出的“第三方文本生成模型”支持范围较宽泛，但文档 5 明确指出向量模型仅限 `text-embedding-v4/v3`（文本类）和 `qwen3-vl-embedding`（多模态类），且 `multimodal-embedding-v1` 仅用于图片问答类知识库。实际可用模型应以控制台创建应用时的下拉选项为准，避免依赖过时列表。

## 关键参数

| 参数类别 | 参数名 | 取值范围 | 说明 |
|----------|--------|-----------|------|
| **全局检索** | 最大召回数量 | 1–20 | 混排后最终返回的切片总数，影响 [Token](../concepts/token.md) 消耗与回答完整性 |
| | 知识库路由 | 开/关 | 开启后调用 `qwen-plus` 判断查询应路由至哪些知识库，产生额外模型费用 |
| **单知识库** | 初步向量检索 TopK | 1–100 | 向量阶段初步召回切片数，默认 50；**费用取决于此值 × 切片平均 [Token](../concepts/token.md) 数** [知识库计费说明](../../raw/application-user-guide/knowledge-base/billing-for-knowledge-base.md) |
| | 相似度阈值 | 0.01–1.0 | 过滤排序后低分切片，过高易漏召，过低引入噪声 |
| | 标签过滤 / 结构化字段过滤 | — | 基于元数据或预设标签进行前置筛选，提升精准度 |
| **生成控制** | 温度（temperature） | 0–2 | 控制回答随机性，问答服务中可为每个模型单独配置 |

## 使用方式

知识库可通过三种方式集成：  
1. **控制台零代码集成**：在[应用管理](https://bailian.console.aliyun.com/#/app-center)中为智能体或工作流应用添加「文档知识库」节点，配置相似度阈值、权重及 TopK；工作流中需在大模型节点提示词内插入 `{知识库1/result}` 变量引用检索结果。  
2. **API 调用**：通过百炼 SDK（Python/Java 等）调用 `CreateIndex`、`Retrieve` 等接口实现自动化知识库创建与检索，适用于外部系统集成 [知识库API指南](../../raw/application-user-guide/knowledge-base/rag-knowledge-base-api-guide.md)。  
3. **独立服务形态**：在知识库控制台直接创建「知识检索」或「知识问答」服务，发布后通过 HTTP API 或调试窗口测试，无需构建完整应用。

## 限制和注意事项

- **地域限制**：知识库功能**仅支持华北2（北京）地域**，新加坡、法兰克福等其他地域不可用，此限制在文档 1 和文档 4 中均被强调。  
- **配额硬性约束**：标准版知识库存储上限 100 GB，旗舰版 9,999 GB；单次控制台导入文件数上限 50 个；音视频搜索类知识库**不支持新增切片**，仅支持编辑与删除 [知识库配额与限制](../../raw/application-user-guide/knowledge-base/rag-knowledge-base-specifications.md)。  
- **元数据与切片变更限制**：知识库创建后，**无法再配置 Meta 信息抽取**；文本切片编辑仅作用于当前知识库，重新导入源文件时需再次人工修正。  
- **计费关键点**：规格费用按小时计费（标准版 0.03 元/小时，旗舰版 0.2 元/RCU/小时）；模型费用独立计算，其中 Rerank 排序费用取决于**初步召回总切片数**，而非最终返回数，关闭排序可显著降本 [知识库计费说明](../../raw/application-user-guide/knowledge-base/billing-for-knowledge-base.md)。  
- **效果优化建议**：若召回不理想，优先检查源文件格式（避免合并单元格、水印）、启用「智能切分」策略、配置元数据（如 `filename` 或 `date`）进行结构化过滤，并通过「命中测试」迭代调整相似度阈值与 TopK [RAG效果优化](../../raw/application-user-guide/knowledge-base/rag-optimization.md)。

## 来源文档

- [知识库](../../raw/application-user-guide/knowledge-base/rag-knowledge-base.md)
- [RAG效果优化](../../raw/application-user-guide/knowledge-base/rag-optimization.md)
- [知识库日志与监控](../../raw/application-user-guide/knowledge-base/rag-knowledge-base-log-monitoring.md)
- [知识库API指南](../../raw/application-user-guide/knowledge-base/rag-knowledge-base-api-guide.md)
- [知识库配额与限制](../../raw/application-user-guide/knowledge-base/rag-knowledge-base-specifications.md)
- [知识库计费说明](../../raw/application-user-guide/knowledge-base/billing-for-knowledge-base.md)
- [知识检索](../../raw/application-user-guide/knowledge-base/rag-knowledge-retrieval.md)
- [知识问答](../../raw/application-user-guide/knowledge-base/rag-knowledge-qa.md)



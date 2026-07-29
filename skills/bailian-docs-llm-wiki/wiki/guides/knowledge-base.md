# [knowledge](../api/knowledge.md) base

知识库是阿里云百炼平台提供的 RAG（[检索增强生成](../concepts/rag.md)）核心能力，用于为大语言模型注入私有、领域专属或时效性强的结构化与非结构化数据。其通过语义检索从用户上传的文档、表格、音视频等数据中精准召回相关内容，并交由大模型生成准确、可溯源的回答。该功能仅在中国站华北2（北京）地域可用，其他地域（如新加坡、德国法兰克福）暂不支持 [知识库 (raw/application-user-guide/knowledge-base/rag-knowledge-base.md)](../../raw/application-user-guide/knowledge-base/rag-knowledge-base.md)。

## 支持的模型/功能

知识库支持与多种预置及自定义模型协同工作：
- **预置模型**：千问全系（QwQ/Long/Max/Plus/Turbo/Coder/Deep-Research）、千问VL系列（Max/Plus/Flash/OCR）、Qwen3/Qwen2.5/Qwen2 等开源模型，以及第三方模型（DeepSeek-R1、Llama3.1、Yi-Large 等）。
- **自定义模型**：基于上述基础模型调优后的版本，同样支持知识库集成 [知识库 (raw/application-user-guide/knowledge-base/rag-knowledge-base.md)](../../raw/application-user-guide/knowledge-base/rag-knowledge-base.md)。

知识库提供三类核心服务：
- **知识检索**：支持单库或多库（最多 15 个）联合检索，具备 Query 改写、混合检索（向量+关键词）、Rerank 排序及精细化参数控制能力 [知识检索 (raw/application-user-guide/knowledge-base/rag-knowledge-retrieval.md)](../../raw/application-user-guide/knowledge-base/rag-knowledge-retrieval.md)。
- **知识问答**：在检索基础上，调用大模型生成自然语言回答，支持极速模式（单轮）与多轮智能模式（Agentic 规划），并提供拒答、防泄漏、引用溯源等生成控制能力 [知识问答 (raw/application-user-guide/knowledge-base/rag-knowledge-qa.md)](../../raw/application-user-guide/knowledge-base/rag-knowledge-qa.md)。
- **日志与监控**：所有检索调用自动投递至 SLS 日志服务，支持用量统计、错误排查与性能分析 [知识库日志与监控 (raw/application-user-guide/knowledge-base/rag-knowledge-base-log-monitoring.md)](../../raw/application-user-guide/knowledge-base/rag-knowledge-base-log-monitoring.md)。

> **注意**：文档 1 中列出的“千问-开源版（Qwen3、Qwen2.5、Qwen2等）”在文档 6 的模型调用费用部分被明确限定为 `qwen3.6-plus` 和 `qwen3.7-plus` 等具体版本；实际支持列表应以控制台创建应用时可选模型为准，且 Qwen3 系列模型的向量化与排序能力（如 `qwen3-vl-embedding`）已深度集成，而非泛指所有开源变体。

## 关键参数

知识库行为高度依赖以下关键参数配置：

| 参数类别 | 参数名 | 取值范围 | 说明 |
|----------|--------|----------|------|
| **全局检索** | 最大召回数量 | 1–20 | 混排后最终返回的切片总数，影响下游模型输入长度与 [Token](../concepts/token.md) 消耗。 |
| **知识库独立配置** | 初步向量检索 TopK | 1–100 | 向量检索阶段初步召回的切片数，默认 50；**直接影响 Rerank 模型费用**（费用 = 初步召回总切片数 × 平均切片 [Token](../concepts/token.md) 数 × 单价）[知识库计费说明 (raw/application-user-guide/knowledge-base/billing-for-knowledge-base.md)](../../raw/application-user-guide/knowledge-base/billing-for-knowledge-base.md)。 |
| | 初步关键词检索 TopK | 1–100 | 关键词检索阶段初步召回的切片数，默认 50；同上，计入 Rerank 费用。 |
| | 相似度阈值 | 0.01–1.0 | 过滤排序后低分切片；值过高易漏召，过低引入噪声。 |
| | 标签过滤 / 结构化字段过滤 | — | 用于精准限定检索范围，提升准确率与效率。 |
| **高级能力** | 多轮对话改写 | 开/关 | 在创建知识库时启用，仅对当前知识库生效，不可事后修改；用于补全多轮对话中的上下文信息 [RAG效果优化 (raw/application-user-guide/knowledge-base/rag-optimization.md)](../../raw/application-user-guide/knowledge-base/rag-optimization.md)。 |

## 使用方式

知识库可通过三种方式集成到业务中：
1. **控制台零代码集成**：在[应用管理](https://bailian.console.aliyun.com/#/app-center)中，为智能体或工作流应用添加“文档知识库”节点，选择知识库并配置相似度阈值、权重等参数；工作流中需将知识库节点与大模型节点串联，并在提示词中引用 `{result}` 变量。
2. **API 集成**：通过百炼 SDK 调用知识库 API，适用于外部系统对接。**注意：API 仅支持文档搜索类知识库** [知识库API指南 (raw/application-user-guide/knowledge-base/rag-knowledge-base-api-guide.md)](../../raw/application-user-guide/knowledge-base/rag-knowledge-base-api-guide.md)。
3. **独立服务化**：在知识库控制台创建“知识检索”或“知识问答”服务，发布后获得独立 endpoint，供自有应用直接调用，支持多库联合、路由、混排等高级能力。

## 限制和注意事项

- **地域限制**：知识库功能**仅限中国站华北2（北京）地域**，其他地域（含国际站）完全不可用，此限制在文档 1 和文档 5 中均被明确强调。
- **配额与规格**：
  - 标准版知识库：1 QPS 固定并发，100 GB 免费存储；旗舰版：50–10,000 QPS 可调（对应 1–200 RCU），9,999 GB 存储。
  - 单次导入文件上限 50 个；单个文件最大 150 MB（PDF/DOCX）或 512 MB（音视频）；单个文本切片最长 6000 字符。
- **模型费用独立计费**：知识库运行时长（规格费用）与模型调用（向量化、Rerank、问答生成）费用**完全分离**。例如，一次检索会同时产生 `text-embedding-v4`（Query 向量化）、`qwen3-rerank`（排序）和所选问答模型（如 `qwen3.7-plus`）三笔费用，均按实际 [Token](../concepts/token.md) 计费 [知识库计费说明 (raw/application-user-guide/knowledge-base/billing-for-knowledge-base.md)](../../raw/application-user-guide/knowledge-base/billing-for-knowledge-base.md)。
- **元数据与切片操作限制**：知识库创建后，**无法再配置 Meta 信息抽取**；音视频搜索类知识库**不支持新增切片**，仅支持编辑与删除 [知识库配额与限制 (raw/application-user-guide/knowledge-base/rag-knowledge-base-specifications.md)](../../raw/application-user-guide/knowledge-base/rag-knowledge-base-specifications.md)。
- **调试即计费**：在控制台进行“命中测试”或“调试问答”时，所有模型调用（向量、Rerank、生成）均会产生真实费用，需谨慎操作。

## 来源文档

- [知识库](../../raw/application-user-guide/knowledge-base/rag-knowledge-base.md)
- [RAG效果优化](../../raw/application-user-guide/knowledge-base/rag-optimization.md)
- [知识库日志与监控](../../raw/application-user-guide/knowledge-base/rag-knowledge-base-log-monitoring.md)
- [知识库配额与限制](../../raw/application-user-guide/knowledge-base/rag-knowledge-base-specifications.md)
- [知识库API指南](../../raw/application-user-guide/knowledge-base/rag-knowledge-base-api-guide.md)
- [知识库计费说明](../../raw/application-user-guide/knowledge-base/billing-for-knowledge-base.md)
- [知识检索](../../raw/application-user-guide/knowledge-base/rag-knowledge-retrieval.md)
- [知识问答](../../raw/application-user-guide/knowledge-base/rag-knowledge-qa.md)



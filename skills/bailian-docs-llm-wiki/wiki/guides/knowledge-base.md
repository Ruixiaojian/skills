# [knowledge](../api/knowledge.md) base

知识库是阿里云百炼平台提供的 RAG（[检索增强生成](../concepts/rag.md)）核心能力，用于为大语言模型注入私有、结构化或非结构化数据，提升其在垂直领域回答的准确性与时效性。它支持文档、表格、图片、音视频等多模态数据源，并通过语义检索、向量索引与重排机制实现高精度召回。知识库功能仅在中国站华北2（北京）地域可用，其他地域（如新加坡、法兰克福）暂不支持。

## 支持的模型/功能

知识库本身不直接运行生成模型，而是作为数据增强层，与下游大模型协同工作。其能力覆盖以下关键模型与功能：

- **向量模型**：用于文本/多模态内容向量化，包括 `text-embedding-v4`（文档搜索、音视频搜索类）、`qwen3-vl-embedding`（图片问答类、视觉理解场景）[知识库计费说明](../../raw/application-user-guide/knowledge-base/billing-for-knowledge-base.md)；
- **排序模型（Rerank）**：对初步召回结果进行精排，包括 `qwen3-rerank`（纯文本）、`qwen3-vl-rerank`（多模态）及 `qwen3-rerank(hybrid)` [知识检索](../../raw/application-user-guide/knowledge-base/rag-knowledge-retrieval.md)；
- **路由模型**：当应用绑定多个知识库时，可选 `qwen-plus` 自动判断查询应路由至哪些知识库 [知识库计费说明](../../raw/application-user-guide/knowledge-base/billing-for-knowledge-base.md)；
- **生成模型**：由用户在智能体/工作流应用中自行选择（如 `qwen3.7-plus`、`qwen2.5`、`DeepSeek-R1` 等），知识库提供检索结果作为上下文输入 [知识库 (raw/application-user-guide/knowledge-base/rag-knowledge-base.md)](../../raw/application-user-guide/knowledge-base/rag-knowledge-base.md)。

> **注意**：文档 1 中列出的“千问-QwQ/Long/Max/Plus/Turbo/Coder/Deep-Research”等模型属于**生成模型范畴**，并非知识库内置组件；知识库仅依赖向量与排序模型完成检索流程。混淆二者可能导致架构设计偏差。

## 关键参数

知识库检索效果高度依赖以下可调参数，需结合业务场景权衡精度与成本：

| 参数 | 取值范围 | 说明 | 影响 |
|------|----------|------|------|
| **相似度阈值** | 0.01–1.0 | 过滤重排后得分低于该值的切片 | 阈值过高易漏召，过低引入噪声；默认值通常为 0.3–0.5 [知识库 (raw/application-user-guide/knowledge-base/rag-knowledge-base.md)](../../raw/application-user-guide/knowledge-base/rag-knowledge-base.md) |
| **初步向量检索 TopK** | 1–100 | 向量检索阶段召回的切片数 | 直接影响 Rerank 模型 [Token](../concepts/token.md) 消耗量，是主要成本杠杆 [知识检索](../../raw/application-user-guide/knowledge-base/rag-knowledge-retrieval.md) |
| **最大召回数量** | 1–20 | 最终返回给大模型的切片数 | 决定 LLM 输入长度上限，需匹配所选模型的上下文窗口 |
| **权重（多知识库）** | 数值型 | 同类型知识库间优先级排序依据 | 仅在同类型知识库（如均为文档搜索）间生效，跨类型无效 [知识库 (raw/application-user-guide/knowledge-base/rag-knowledge-base.md)](../../raw/application-user-guide/knowledge-base/rag-knowledge-base.md) |
| **多轮对话改写** | 开/关 | 基于历史会话自动补全当前 Query | 提升多轮指代消解能力，但创建后不可修改，需在知识库初始化时启用 [RAG效果优化](../../raw/application-user-guide/knowledge-base/rag-optimization.md) |

## 使用方式

知识库可通过三种路径集成到业务中，均需先在控制台或 API 创建知识库实例：

- **控制台快速集成**：适用于 PoC 或轻量应用。在[应用管理](https://bailian.console.aliyun.com/#/app-center)中配置智能体或工作流应用，点击“文档知识库”+号添加知识库，设置相似度阈值与权重即可 [知识库 (raw/application-user-guide/knowledge-base/rag-knowledge-base.md)](../../raw/application-user-guide/knowledge-base/rag-knowledge-base.md)；
- **知识检索服务**：面向多知识库联合检索场景。在知识库页面切换至“知识检索”标签页，创建服务并绑定最多 15 个知识库，统一配置混排模型、最大召回数等全局参数 [知识检索](../../raw/application-user-guide/knowledge-base/rag-knowledge-retrieval.md)；
- **知识问答服务**：面向端到端问答场景。在知识库页面切换至“知识问答”标签页，选择生成模型、检索模式（极速/多轮智能），并绑定知识库，支持文件预解析、拒答、引用溯源等高级生成控制 [知识问答](../../raw/application-user-guide/knowledge-base/rag-knowledge-qa.md)；
- **API 集成**：适用于外部系统对接。使用阿里云百炼 SDK 调用 `Retrieve` 接口，需提前完成权限配置、AccessKey 设置及业务空间 ID 注入 [知识库API指南](../../raw/application-user-guide/knowledge-base/rag-knowledge-base-api-guide.md)。

## 限制和注意事项

- **地域限制**：知识库功能**仅支持华北2（北京）地域**，新加坡、德国（法兰克福）等国际站点暂未开放，此限制在多篇文档中反复强调 [知识库 (raw/application-user-guide/knowledge-base/rag-knowledge-base.md)](../../raw/application-user-guide/knowledge-base/rag-knowledge-base.md)、[知识库API指南](../../raw/application-user-guide/knowledge-base/rag-knowledge-base-api-guide.md)；
- **配额约束**：标准版知识库并发固定为 1 QPS，旗舰版支持 50–10,000 QPS（按 RCU 调整）；单次召回切片上限为 20 条；音视频搜索类知识库**不支持新增切片**，仅支持编辑与删除 [知识库配额与限制](../../raw/application-user-guide/knowledge-base/rag-knowledge-base-specifications.md)；
- **元数据与标签**：`Meta信息抽取` 必须在知识库创建时配置，创建后无法追加；标签过滤需在上传文件时或数据管理页手动设置，调试时可在智能体应用的“召回策略”中临时指定 [RAG效果优化](../../raw/application-user-guide/knowledge-base/rag-optimization.md)；
- **计费要点**：知识库费用 = **规格费用（按小时） + 模型调用费用（按 [Token](../concepts/token.md)）**；其中 Rerank 排序费用取决于**初步召回总切片数**，而非最终返回数，关闭排序可显著降本 [知识库计费说明](../../raw/application-user-guide/knowledge-base/billing-for-knowledge-base.md)；
- **日志监控**：检索日志默认投递至 SLS，字段含 `pipeline_id`（知识库 ID）、`latency`（毫秒级耗时）、`response_code`（业务码）等，可用于审计与性能分析 [知识库日志与监控](../../raw/application-user-guide/knowledge-base/rag-knowledge-base-log-monitoring.md)。

## 来源文档

- [知识库](../../raw/application-user-guide/knowledge-base/rag-knowledge-base.md)
- [RAG效果优化](../../raw/application-user-guide/knowledge-base/rag-optimization.md)
- [知识库API指南](../../raw/application-user-guide/knowledge-base/rag-knowledge-base-api-guide.md)
- [知识库日志与监控](../../raw/application-user-guide/knowledge-base/rag-knowledge-base-log-monitoring.md)
- [知识库配额与限制](../../raw/application-user-guide/knowledge-base/rag-knowledge-base-specifications.md)
- [知识库计费说明](../../raw/application-user-guide/knowledge-base/billing-for-knowledge-base.md)
- [知识检索](../../raw/application-user-guide/knowledge-base/rag-knowledge-retrieval.md)
- [知识问答](../../raw/application-user-guide/knowledge-base/rag-knowledge-qa.md)



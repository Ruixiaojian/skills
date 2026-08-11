# [knowledge](../api/knowledge.md) base

知识库是阿里云百炼平台提供的 RAG（[检索增强生成](../concepts/rag.md)）核心能力，用于为大模型注入私有、结构化或非结构化数据，提升其在垂直领域回答的准确性与时效性。它支持文档搜索、数据查询、图片问答、音视频搜索等多种知识类型，并可通过控制台、工作流、智能体或 API 多种方式集成。知识库功能仅在中国站华北2（北京）地域可用。

## 支持的模型/功能

知识库本身不直接运行模型，但其检索流程和上层问答服务深度依赖以下模型：

- **向量模型**：`text-embedding-v4`（默认文本类）、`qwen3-vl-embedding`（[多模态](../concepts/multi-modal.md)/视觉理解场景），用于文档切片与用户 Query 的向量化；详见 [知识库计费说明](../../raw/application-user-guide/knowledge-base/billing-for-knowledge-base.md) 中 2.2.1 节。
- **排序模型（Rerank）**：`qwen3-rerank`（文本类）、`qwen3-vl-rerank`（[多模态](../concepts/multi-modal.md)类），用于对初步召回结果进行精排；该能力在 [知识检索](../../raw/application-user-guide/knowledge-base/rag-knowledge-retrieval.md) 和 [知识问答](../../raw/application-user-guide/knowledge-base/rag-knowledge-qa.md) 中均作为可选配置项。
- **路由模型**：`qwen-plus`，仅在启用“知识库路由”时调用，用于判断多知识库场景下应检索哪些库。
- **问答生成模型**：所有百炼支持的预置及自定义大模型（如 `Qwen3`、`Qwen2.5`、`DeepSeek-R1`、`Llama3.1` 等）均可作为问答服务的底座模型；具体支持列表以 [知识库 (raw/application-user-guide/knowledge-base/rag-knowledge-base.md)](../../raw/application-user-guide/knowledge-base/rag-knowledge-base.md) 中“支持的模型”章节为准。

> **注意**：文档 1 列出的“千问VL-Max/Plus/Flash/OCR”等视觉语言模型，仅适用于**图片问答类知识库**或**文档搜索类中选择“视觉理解”场景**；而文档 7 明确指出 `qwen3-vl-embedding` 是此类场景的**唯一支持向量模型**，二者逻辑一致。但文档 1 中将“千问VL-Max/Plus/Flash/OCR”列为“支持使用知识库的模型”，易引发歧义——这些模型是**问答生成端**可选模型，**非知识库向量化/排序所用模型**。开发者需区分“知识库依赖模型”与“应用调用模型”。

## 关键参数

知识库检索效果高度依赖以下可配置参数，分为全局与知识库级两类：

| 参数类别 | 参数名 | 取值范围 | 说明 |
|----------|--------|----------|------|
| **全局（检索/问答服务）** | 最大召回数量 | 1–20 | 混排后最终返回给大模型的切片总数；直接影响 [Token](../concepts/token.md) 消耗与回答完整性。 |
| | 知识库路由 | 开/关 | 开启后调用 `qwen-plus` 进行路由判断，产生额外模型费用；适用于绑定 ≥2 个知识库的场景。 |
| **知识库级（独立配置）** | 初步向量检索 TopK | 1–100 | 向量检索阶段召回的切片数（默认 50）；增大可提升召回率，但显著增加 Rerank 费用（见[知识库计费说明](../../raw/application-user-guide/knowledge-base/billing-for-knowledge-base.md) 2.2.2 节）。 |
| | 相似度阈值 | 0.01–1.0 | 过滤排序后低分切片；过高易漏召，过低引入噪声；建议通过[命中测试](https://help.aliyun.com/zh/model-studio/rag-optimization#3.4)调优。 |
| | 权重 | 数值（无固定范围） | 仅在**同类型知识库间生效**（如文档搜索类之间），用于干预多路召回顺序；权重越高，该库切片在加权排序中越靠前。 |

此外，`标签过滤` 和 `结构化字段过滤` 是精准控制检索范围的关键手段，尤其适用于含多品类文件的知识库；其配置与使用详见 [RAG效果优化](../../raw/application-user-guide/knowledge-base/rag-optimization.md) 中 3.2 节。

## 使用方式

知识库可通过三种主要路径集成到业务中：

1. **控制台快速集成（零代码）**：  
   在 [知识库](https://bailian.console.aliyun.com/?tab=app#/knowledge-base) 页面创建标准版/旗舰版知识库 → 上传文件或配置同步规则（OSS/飞书/钉钉等）→ 在 [应用管理](https://bailian.console.aliyun.com/#/app-center) 中为智能体或工作流应用添加该知识库节点。工作流中需显式连接“知识库节点”与“大模型节点”，并在提示词中引用 `{result}` 变量。

2. **API 集成（自动化）**：  
   通过百炼 SDK 调用 `Retrieve` 接口实现检索，或调用 `CreateIndex`/`AddFile` 等接口完成知识库全生命周期管理；完整示例见 [知识库API指南](../../raw/application-user-guide/knowledge-base/rag-knowledge-base-api-guide.md)。**注意**：该指南明确限定“仅适用于文档搜索类知识库”。

3. **高级服务封装**：  
   - **知识检索服务**：在知识库页面切换至“知识检索”标签页，创建支持多库联合、混排、路由的统一检索入口，适合需精细化控制召回策略的场景。  
   - **知识问答服务**：切换至“知识问答”标签页，绑定知识库并选择 `极速`（单轮低延时）或 `多轮智能`（Agentic 自动规划）模式，直接生成自然语言回答。

## 限制和注意事项

- **地域限制**：知识库功能**仅在中国站华北2（北京）地域开通和使用**，新加坡、德国（法兰克福）等其他地域均不支持；此限制在 [知识库 (raw/application-user-guide/knowledge-base/rag-knowledge-base.md)](../../raw/application-user-guide/knowledge-base/rag-knowledge-base.md) 和 [知识库API指南](../../raw/application-user-guide/knowledge-base/rag-knowledge-base-api-guide.md) 中被反复强调。
  
- **配额与规格**：  
  - 标准版知识库：1 QPS 固定并发，100 GB 存储，0.03 元/小时；旗舰版：50–10,000 QPS 可调（1–200 RCU），9,999 GB 存储，0.2 元/RCU/小时；详情见 [知识库配额与限制](../../raw/application-user-guide/knowledge-base/rag-knowledge-base-specifications.md)。  
  - 单次查询最多召回 **20 个切片**；单个知识库文件数量无硬上限（非结构化类），但单个 Excel 文件限 10 万行；音视频类知识库**不支持新增切片**（仅支持编辑与删除）。

- **关键行为约束**：  
  - **元数据（Metadata）**：必须在创建知识库时一次性配置，**创建后无法再添加或修改**；但可通过 API 更新单个文件的标签（见 [RAG效果优化](../../raw/application-user-guide/knowledge-base/rag-optimization.md) 3.2 节）。  
  - **知识库类型不可变**：创建时选定“文档搜索”“数据查询”等类型后，后续无法更改。  
  - **多轮对话改写**：仅能在创建知识库时开启，**创建后无法补开**，需重新创建知识库。

- **计费提醒**：  
  自 2026 年 1 月 4 日起正式计费，费用由**规格费用**（按小时）和**模型调用费用**（按 [Token](../concepts/token.md)）两部分构成；其中 Rerank 排序费用取决于**初步召回总切片数**，而非最终返回数，极易因 TopK 设置过高导致成本激增；务必参考 [知识库计费说明](../../raw/application-user-guide/knowledge-base/billing-for-knowledge-base.md) 中 2.2.2 节的计费公式进行预估。

## 来源文档

- [知识库](../../raw/application-user-guide/knowledge-base/rag-knowledge-base.md)
- [RAG效果优化](../../raw/application-user-guide/knowledge-base/rag-optimization.md)
- [知识库定时数据同步指南](../../raw/application-user-guide/knowledge-base/data-sync-guide.md)
- [知识库API指南](../../raw/application-user-guide/knowledge-base/rag-knowledge-base-api-guide.md)
- [知识库日志与监控](../../raw/application-user-guide/knowledge-base/rag-knowledge-base-log-monitoring.md)
- [知识库配额与限制](../../raw/application-user-guide/knowledge-base/rag-knowledge-base-specifications.md)
- [知识库计费说明](../../raw/application-user-guide/knowledge-base/billing-for-knowledge-base.md)
- [知识检索](../../raw/application-user-guide/knowledge-base/rag-knowledge-retrieval.md)
- [知识问答](../../raw/application-user-guide/knowledge-base/rag-knowledge-qa.md)



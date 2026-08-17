# [knowledge](../api/knowledge.md) base

知识库是百炼平台基于 RAG（[检索增强生成](../concepts/rag.md)）技术构建的核心能力，用于为大模型注入私有数据和最新业务知识，显著提升其在垂直领域回答的准确性与可靠性。它支持多模态内容理解、语义检索、多知识库联合召回与精细化排序，并可通过控制台、工作流、智能体或 API 多种方式集成。知识库功能目前仅在中国站华北2（北京）地域可用。

## 支持的模型/功能

知识库支持阿里云百炼提供的全部预置与自定义文本及多模态模型，包括千问系列（QwQ/Long/Max/Plus/Turbo/Coder/Deep-Research、VL-Max/Plus/Flash/OCR、Qwen3/Qwen2.5/Qwen2等）、第三方模型（DeepSeek-R1、Llama3.1、Yi-Large等），以及配套的向量模型（`text-embedding-v4`、`qwen3-vl-embedding`）和排序模型（`qwen3-rerank`、`qwen3-vl-rerank`）[原文标题](../../raw/application-user-guide/knowledge-base/rag-knowledge-base.md)。  
知识库类型覆盖**文档搜索**（含基础问答、视觉理解、极速问答）、**数据查询**（结构化表格）、**图片问答**和**音视频搜索**四类，分别适配不同数据形态与性能需求 [原文标题](../../raw/application-user-guide/knowledge-base/rag-knowledge-base.md)。  
此外，知识库可与**知识问答服务**和**知识检索服务**解耦使用：前者面向端到端自然语言问答（支持拒答、防泄漏、引用溯源），后者面向开发者级精准片段召回（支持多库混排、路由、字段过滤）[原文标题](../../raw/application-user-guide/knowledge-base/rag-knowledge-qa.md)。

> **注意**：文档 1 中列出的“千问-开源版（Qwen3、Qwen2.5、Qwen2等）”在文档 7 的问答服务模型列表中具体体现为 `qwen3.6-plus`、`qwen3.7-plus` 等命名形式，实际选型应以控制台创建应用时实时可选模型为准，避免依赖过时枚举。

## 关键参数

| 参数类别 | 参数名 | 取值范围/说明 | 作用 |
|----------|--------|----------------|------|
| **检索控制** | 相似度阈值 | `0.01–1.0` | 过滤重排后低分切片；值过高易漏召，过低引入噪声 [原文标题](../../raw/application-user-guide/knowledge-base/rag-knowledge-base.md) |
| | 初步向量/关键词 TopK | `1–100`（默认各50） | 控制初步召回切片数量，直接影响 Rerank 模型调用成本 [原文标题](../../raw/application-user-guide/knowledge-base/rag-knowledge-qa.md) |
| | 最大召回数量 | `1–20` | 最终返回给下游（如大模型节点）的切片数上限 |
| **排序与路由** | 排序模型 | `qwen3-rerank`（文本）、`qwen3-vl-rerank`（多模态）等 | 对初步召回结果精排，费用取决于初步召回总量而非最终返回量 [原文标题](../../raw/application-user-guide/knowledge-base/billing-for-knowledge-base.md) |
| | 知识库权重 | 数值型（越大优先级越高） | 仅在同类型知识库间生效，用于干预多库召回顺序 [原文标题](../../raw/application-user-guide/knowledge-base/rag-knowledge-base.md) |
| **元数据与过滤** | Meta信息抽取 | 创建时配置，不可修改 | 为文本切片注入 `filename`、`date`、`author` 等上下文，实现结构化过滤 [原文标题](../../raw/application-user-guide/knowledge-base/rag-knowledge-base.md) |
| | 标签过滤 | 单文件最多32个标签 | 在检索前按标签筛选文件，提升准确率与效率 |

## 使用方式

知识库可通过三种主要路径集成：  
1. **控制台零代码集成**：在[智能体应用](../../raw/application-user-guide/knowledge-base/rag-knowledge-base.md)或[工作流应用](../../raw/application-user-guide/knowledge-base/rag-knowledge-base.md)配置页，通过 UI 拖拽节点或点击“+”添加知识库，设置相似度阈值、权重、TopK 等参数；  
2. **知识问答/检索服务**：独立创建服务，绑定最多15个知识库，统一配置混排模型、路由开关与全局参数，适用于需标准化输出的业务场景；  
3. **API 集成**：通过百炼 SDK 调用 `CreateIndex`、`Retrieve` 等接口实现自动化管理与检索，适用于外部系统深度集成 [原文标题](../../raw/application-user-guide/knowledge-base/rag-knowledge-base-api-guide.md)。  
所有方式均支持定时数据同步（OSS/飞书/钉钉等来源），确保知识库内容自动更新 [原文标题](../../raw/application-user-guide/knowledge-base/data-sync-guide.md)。

## 限制和注意事项

- **地域限制**：知识库功能**仅支持华北2（北京）地域**，新加坡、法兰克福等其他地域不提供服务，此限制在文档 1 和文档 5 中均被明确强调；  
- **配额硬限**：单知识库文件数无硬限（非结构化），但单次控制台导入上限为50个；单个文本切片长度上限为6000字符；标准版知识库并发固定为1 QPS，旗舰版可调但最高10,000 QPS [原文标题](../../raw/application-user-guide/knowledge-base/rag-knowledge-base-specifications.md)；  
- **计费关键点**：费用由**规格费**（按小时，标准版0.03元/小时，旗舰版0.2元/RCU/小时）和**模型调用费**（向量化、Rerank、路由、问答生成）两部分构成，其中 Rerank 费用取决于初步召回切片总数，而非最终返回数 [原文标题](../../raw/application-user-guide/knowledge-base/billing-for-knowledge-base.md)；  
- **不可逆操作**：删除知识库将**永久清除所有数据且无法恢复**，务必谨慎操作；知识库类型（如文档搜索→数据查询）创建后不可更改；  
- **日志监控**：检索调用日志默认投递至 SLS，需手动开通并配置 LogStore，关闭开关仅停止新日志投递，历史日志仍计费 [原文标题](../../raw/application-user-guide/knowledge-base/rag-knowledge-base-log-monitoring.md)。

## 来源文档

- [知识库](../../raw/application-user-guide/knowledge-base/rag-knowledge-base.md)
- [RAG效果优化](../../raw/application-user-guide/knowledge-base/rag-optimization.md)
- [知识库定时数据同步指南](../../raw/application-user-guide/knowledge-base/data-sync-guide.md)
- [知识库日志与监控](../../raw/application-user-guide/knowledge-base/rag-knowledge-base-log-monitoring.md)
- [知识库API指南](../../raw/application-user-guide/knowledge-base/rag-knowledge-base-api-guide.md)
- [知识库配额与限制](../../raw/application-user-guide/knowledge-base/rag-knowledge-base-specifications.md)
- [知识问答](../../raw/application-user-guide/knowledge-base/rag-knowledge-qa.md)
- [知识库计费说明](../../raw/application-user-guide/knowledge-base/billing-for-knowledge-base.md)
- [知识检索](../../raw/application-user-guide/knowledge-base/rag-knowledge-retrieval.md)



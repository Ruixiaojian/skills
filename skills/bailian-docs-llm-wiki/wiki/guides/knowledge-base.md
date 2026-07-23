# [knowledge](../api/knowledge.md) base

知识库（Knowledge Base）是阿里云百炼平台提供的 RAG（[检索增强生成](../concepts/rag.md)）核心能力，用于为大模型注入私有、结构化或非结构化数据，提升其在垂直领域回答的准确性与时效性。它通过索引构建、语义检索与结果重排三阶段 pipeline 实现高效知识召回，并支持文档搜索、数据查询、图片问答、音视频搜索等多种类型。知识库需部署于华北2（北京）地域，且所有操作均基于业务空间隔离。

## 支持的模型/功能

知识库本身不直接运行模型，但其检索流程深度依赖以下模型能力，并与多种大模型协同工作：

- **向量模型**：文档搜索类知识库默认使用 `text-embedding-v4` 或 `text-embedding-v3`（512维）；图片问答与音视频搜索类必须使用 `qwen3-vl-embedding`（1024维）[原文标题](../../raw/application-user-guide/knowledge-base/rag-knowledge-base-specifications.md)。  
- **排序模型（Rerank）**：文档类支持 `qwen3-rerank`（含 hybrid 模式），[多模态](../concepts/multi-modal.md)类支持 `qwen3-vl-rerank`，可选关闭以降低成本 [原文标题](../../raw/application-user-guide/knowledge-base/billing-for-knowledge-base.md)。  
- **路由模型**：当应用挂载多个知识库并启用路由时，调用 `qwen-plus` 判断目标知识库，产生独立 [Token](../concepts/token.md) 费用 [原文标题](../../raw/application-user-guide/knowledge-base/billing-for-knowledge-base.md)。  
- **问答模型**：知识问答服务中由用户自主选择（如 `qwen3.7-plus`），费用按输入/输出 [Token](../concepts/token.md) 单独计费，不包含在知识库规格费中。  

> **注意**：文档 8 中列出的“预置模型”（如 QwQ/Long/Max 等）仅表示**可绑定知识库的大模型列表**，并非知识库自身使用的模型；而文档 4 明确规定向量模型与排序模型的选择范围及维度限制，二者存在功能层级差异，不可混淆。

## 关键参数

知识库效果高度依赖以下可配置参数，需结合场景权衡精度与成本：

| 参数 | 取值范围 | 说明 | 关联环节 |
|------|----------|------|----------|
| `初步向量检索 TopK` | 1–100 | 向量召回阶段返回的切片数，默认 50；直接影响 Rerank 模型 [Token](../concepts/token.md) 消耗量 [原文标题](../../raw/application-user-guide/knowledge-base/rag-knowledge-retrieval.md) | 检索 |
| `初步关键词检索 TopK` | 1–100 | 关键词召回阶段返回的切片数，默认 50；混合检索时与向量结果合并去重 | 检索 |
| `相似度阈值` | 0.01–1.0 | 过滤 Rerank 后低分切片；值过高易漏召，过低引入噪声 | 检索 |
| `最大召回数量` | 1–20 | 最终返回给大模型的切片数上限；影响下游 Token 成本与回答完整性 | 检索 |
| `标签过滤` | — | 通过 `tags` 参数限定检索范围，支持单标签、多标签“或”/“与”逻辑 [原文标题](../../raw/application-user-guide/knowledge-base/rag-optimization.md) | 检索 |
| `Meta信息抽取` | — | 在创建知识库时配置，支持常量、变量、大模型、正则、关键词五种提取方式；**创建后不可修改** | 索引 |

## 使用方式

知识库可通过控制台、API 或集成至应用三种方式使用：

- **控制台快速接入**：在知识库页面创建后，直接绑定至智能体应用（配置权重与相似度阈值）或工作流应用（拖拽知识库节点），无需编码即可启用 [原文标题](../../raw/application-user-guide/knowledge-base/rag-knowledge-base.md)。  
- **API 集成**：调用 `Retrieve` 接口进行单次检索；需子账号具备 `AliyunBailianDataFullAccess` 权限，且**仅支持华北2（北京）地域** [原文标题](../../raw/application-user-guide/knowledge-base/rag-knowledge-base-api-guide.md)。  
- **日志与监控**：开通 SLS 日志服务后，每条检索请求生成完整日志（含 `request_body`、`response_body.data.nodes[]` 等字段），可用于审计、召回分析与性能排查 [原文标题](../../raw/application-user-guide/knowledge-base/rag-knowledge-base-log-monitoring.md)。  

## 限制和注意事项

- **地域限制**：知识库功能**仅在中国站华北2（北京）地域可用**，其他地域（如新加坡、法兰克福）完全不支持，此限制在文档 2 和文档 8 中一致强调。  
- **存储与配额**：标准版免费额度仅抵扣**标准版知识库规格费用**，不覆盖模型调用费；旗舰版存储上限 9,999 GB，标准版为 100 GB；单个知识库文件数量无硬性上限（非结构化类），但单次控制台上传上限为 50 个文件 [原文标题](../../raw/application-user-guide/knowledge-base/rag-knowledge-base-specifications.md)。  
- **元数据与切片**：`Meta信息抽取` 必须在创建知识库时完成配置，**创建后无法追加或修改**；文本切片长度上限为 6,000 Token，编辑切片内容长度限制为 10–6000 字符。  
- **计费关键点**：Rerank 费用取决于**初步召回总切片数**（即 `TopK` 之和），而非最终返回数；多知识库联合检索时，Query 向量化与 Rerank 调用量按知识库数量线性倍增 [原文标题](../../raw/application-user-guide/knowledge-base/billing-for-knowledge-base.md)。

## 来源文档

- [RAG效果优化](../../raw/application-user-guide/knowledge-base/rag-optimization.md)
- [知识库API指南](../../raw/application-user-guide/knowledge-base/rag-knowledge-base-api-guide.md)
- [知识库日志与监控](../../raw/application-user-guide/knowledge-base/rag-knowledge-base-log-monitoring.md)
- [知识库配额与限制](../../raw/application-user-guide/knowledge-base/rag-knowledge-base-specifications.md)
- [知识库计费说明](../../raw/application-user-guide/knowledge-base/billing-for-knowledge-base.md)
- [知识检索](../../raw/application-user-guide/knowledge-base/rag-knowledge-retrieval.md)
- [知识问答](../../raw/application-user-guide/knowledge-base/rag-knowledge-qa.md)
- [知识库](../../raw/application-user-guide/knowledge-base/rag-knowledge-base.md)



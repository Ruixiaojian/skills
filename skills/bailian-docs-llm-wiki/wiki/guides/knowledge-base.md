# [knowledge](../api/knowledge.md) base

知识库是阿里云百炼平台基于 RAG（[检索增强生成](../concepts/rag.md)）技术构建的核心能力，用于为大模型注入私有数据与领域知识，提升回答的准确性与专业性。它支持文档搜索、数据查询、图片问答、音视频搜索等多种知识类型，并提供从数据同步、索引构建、检索服务到问答生成的全链路能力。所有功能均需在中国站华北2（北京）地域使用。

## 支持的模型/功能

知识库本身不依赖特定模型运行，但其向量化、排序与生成环节需调用对应模型。支持的模型分为两类：

- **向量模型**：文档搜索类、音视频搜索类知识库默认使用 `text-embedding-v4` 或 `text-embedding-v3`；图片问答类及启用「视觉理解」场景的文档搜索类知识库强制使用 `qwen3-vl-embedding`（创建时自动切换，不可更改）[原文标题](../../raw/application-user-guide/knowledge-base/rag-knowledge-base.md)。  
- **排序模型**：文本类知识库可选 `qwen3-rerank`，[多模态](../concepts/multimodal.md)类知识库可选 `qwen3-vl-rerank`，均支持「问答模式」与「相似模式」[原文标题](../../raw/application-user-guide/knowledge-base/rag-knowledge-retrieval.md)。  
- **问答模型**：用户在智能体或工作流应用中自主选择（如 `qwen3.7-plus`），知识库仅提供检索结果作为上下文输入 [原文标题](../../raw/application-user-guide/knowledge-base/rag-knowledge-qa.md)。

> **注意**：文档 9 中列出的“预置模型”与“自定义模型”均为**可挂载知识库的大模型**，而非知识库内部使用的向量/排序模型。二者职责不同，不可混淆。知识库的向量化与重排能力由专用模型提供，且部分模型（如 `qwen3-vl-embedding`）在特定知识库类型下为强制绑定，不支持手动替换。

核心功能包括：
- **多源数据接入**：支持本地上传、OSS、飞书、钉钉、语雀、SharePoint 等六类数据源的定时同步或即时导入 [原文标题](../../raw/application-user-guide/knowledge-base/data-sync-guide.md)；
- **多知识库联合检索**：最多支持 15 个知识库并行检索，支持权重配置与路由判断；
- **知识问答服务**：提供极速模式（单轮检索+生成）与多轮智能模式（Agentic 规划搜索）两种策略；
- **效果优化工具**：支持标签过滤、元数据抽取、切片编辑、相似度阈值调优等精细化控制。

## 关键参数

| 参数类别 | 参数名 | 取值范围 | 说明 |
|----------|--------|----------|------|
| **检索控制** | 初步向量检索 TopK | 1–100 | 向量召回阶段初步返回的切片数，默认 50；影响 Rerank 模型费用（费用 = 初步召回总切片数 × 平均 [Token](../concepts/token.md) 数 × 单价）[原文标题](../../raw/application-user-guide/knowledge-base/rag-knowledge-retrieval.md) |
| | 初步关键词检索 TopK | 1–100 | 关键词匹配召回数，默认 50；仅基础文档问答与表格库可用 |
| | 相似度阈值 | 0.01–1.0 | 过滤排序后低分切片；值过高易漏召，过低引入噪声 |
| | 最大召回数量 | 1–20 | 最终返回给大模型的切片总数（混排后） |
| **索引配置** | 文本切片长度 | — | 单切片最大 [Token](../concepts/token.md) 数为 6000，但推荐启用「智能切分」策略以保障语义完整性 [原文标题](../../raw/application-user-guide/knowledge-base/rag-optimization.md) |
| | Meta信息抽取 | — | 创建知识库时一次性配置，后续不可修改；用于结构化过滤与精准召回 |
| **配额限制** | 单知识库文件数 | 无硬性上限（文档搜索类） | 结构化知识库（如 Excel）仅支持 1 个文件 [原文标题](../../raw/application-user-guide/knowledge-base/rag-knowledge-base-specifications.md) |
| | 标签数量/文件 | ≤32 | 单文件最多附加 32 个标签，用于标签过滤 |

## 使用方式

### 数据接入
- **定时同步**：通过「文件连接器 → 同步数据规则」配置 OSS/飞书/钉钉等来源，支持分钟级、小时级、日级周期 [原文标题](../../raw/application-user-guide/knowledge-base/data-sync-guide.md)；
- **即时上传**：控制台直接上传本地文件（≤150MB），或通过 API 调用 `ApplyFileUploadLease` + `AddFile` 流程完成 [原文标题](../../raw/application-user-guide/knowledge-base/rag-knowledge-base-api-guide.md)。

### 服务集成
- **智能体应用**：在「文档知识库」节点添加知识库，配置相似度阈值与权重；
- **工作流应用**：拖入「知识库」节点，配置 `content` 输入（通常为 `query`）、TopK 及知识库选择方式（固定 or 动态）；
- **外部系统**：使用百炼 SDK 调用 `Retrieve` 接口，或直接构造 HTTP 请求（需签名）[原文标题](../../raw/application-user-guide/knowledge-base/rag-knowledge-base-api-guide.md)。

### 效果调试
- **命中测试**：在知识库详情页输入 Query，查看召回切片、相似度分数及来源文档；
- **日志分析**：开通 SLS 监控后，通过 `pipeline_id`（知识库 ID）、`response_code`、`latency` 等字段定位慢查、失败请求与用量分布 [原文标题](../../raw/application-user-guide/knowledge-base/rag-knowledge-base-log-monitoring.md)。

## 限制和注意事项

- **地域限制**：知识库功能**仅支持华北2（北京）地域**，其他地域（如新加坡、法兰克福）不可用，此限制同时适用于控制台操作与 API 调用 [原文标题](../../raw/application-user-guide/knowledge-base/rag-knowledge-base-api-guide.md)。
- **存储与配额**：
  - 标准版知识库免费存储 ≤100 GB，旗舰版 ≤9,999 GB；超出需配置自购 ADB-PG 实例并额外付费；
  - 单业务空间最多 100,000 个文件、500 个类目、1,000 个数据表；
  - 音视频搜索类知识库**不支持新增切片**，仅支持删除 [原文标题](../../raw/application-user-guide/knowledge-base/rag-knowledge-base-specifications.md)。
- **计费关键点**：
  - 规格费用按小时出账（标准版 0.03 元/小时，旗舰版按 RCU 计费）；
  - **模型调用费用独立计费**：Query 向量化、Rerank 排序、知识库路由（`qwen-plus`）、问答生成均按实际 [Token](../concepts/token.md) 消耗计费，不包含在规格费中 [原文标题](../../raw/application-user-guide/knowledge-base/billing-for-knowledge-base.md)；
  - Rerank 费用取决于**初步召回总切片数**，而非最终返回数，调高 TopK 将显著增加成本。
- **同步行为**：同步规则创建的文件为**独立副本**，源文件删除后百炼平台内副本不会自动清除，需手动删除 [原文标题](../../raw/application-user-guide/knowledge-base/data-sync-guide.md)。

## 来源文档

- [知识库定时数据同步指南](../../raw/application-user-guide/knowledge-base/data-sync-guide.md)
- [知识库API指南](../../raw/application-user-guide/knowledge-base/rag-knowledge-base-api-guide.md)
- [知识库日志与监控](../../raw/application-user-guide/knowledge-base/rag-knowledge-base-log-monitoring.md)
- [知识库配额与限制](../../raw/application-user-guide/knowledge-base/rag-knowledge-base-specifications.md)
- [知识库计费说明](../../raw/application-user-guide/knowledge-base/billing-for-knowledge-base.md)
- [知识检索](../../raw/application-user-guide/knowledge-base/rag-knowledge-retrieval.md)
- [知识问答](../../raw/application-user-guide/knowledge-base/rag-knowledge-qa.md)
- [RAG效果优化](../../raw/application-user-guide/knowledge-base/rag-optimization.md)
- [知识库](../../raw/application-user-guide/knowledge-base/rag-knowledge-base.md)



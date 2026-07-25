# [knowledge](../api/knowledge.md) base

知识库是阿里云百炼平台提供的 RAG（[检索增强生成](../concepts/rag.md)）核心能力，用于为大语言模型注入私有数据与领域知识，提升回答的准确性、时效性与专业性。它支持文档、表格、图片、音视频等多模态数据的语义检索，并通过向量化、召回、重排、生成四阶段流水线完成端到端问答。知识库功能仅在中国站华北2（北京）地域可用，需在业务空间内创建与管理。

## 支持的模型/功能

- **支持的生成模型**：千问系列（QwQ/Long/Max/Plus/Turbo/Coder/Deep-Research、VL-Max/Plus/Flash/OCR、开源版 Qwen3/Qwen2.5/Qwen2）、第三方模型（DeepSeek-R1/V3.1、abab6.5s、Llama3.1、Yi-Large）及其调优后的自定义版本 [知识库](../../raw/application-user-guide/knowledge-base/rag-knowledge-base.md)。  
- **核心功能**：  
  - 多模态检索：支持文本、图片、音视频内容的联合检索与理解；  
  - 多知识库联合检索与问答：最多绑定 15 个知识库，支持权重配置与路由判断；  
  - 检索模式双轨制：极速模式（单轮检索+生成）与多轮智能模式（Agentic 规划搜索）；  
  - 精细控制能力：Query 改写、标签/元数据/结构化字段过滤、双路召回（向量+关键词）、Rerank 排序、拒答与防泄漏策略 [知识问答](../../raw/application-user-guide/knowledge-base/rag-knowledge-qa.md)。  
> **注意**：文档 2 中“支持的模型”列表称“千问-Plus/Turbo”等为“自定义模型”，但文档 7 的计费说明中明确将 `qwen-plus` 列为知识库路由调用的**标准模型**，且其调用费用独立于知识库规格费用。这表明 `qwen-plus` 是平台预置服务模型，非用户调优所得——此处应以文档 7 的模型分类为准，文档 2 的表述易引发歧义。

## 关键参数

| 参数类别 | 参数名 | 取值范围 | 说明 |
|----------|--------|----------|------|
| **检索控制** | 相似度阈值 | 0.01–1.0 | 过滤重排后低分切片；过高易漏召，过低引入噪声 [知识库](../../raw/application-user-guide/knowledge-base/rag-knowledge-base.md) |
| | 初步向量/关键词 TopK | 1–100 | 控制送入 Rerank 模型的切片总数，直接影响排序费用与效果 [知识检索](../../raw/application-user-guide/knowledge-base/rag-knowledge-retrieval.md) |
| | 最大召回数量 | 1–20 | 最终返回给大模型的切片数，受模型输入长度限制约束 |
| **元数据与结构** | Meta信息抽取 | — | 在创建知识库时一次性配置，支持常量/变量/大模型/正则/关键词五种提取方式；**创建后不可修改** [知识库](../../raw/application-user-guide/knowledge-base/rag-knowledge-base.md) |
| | 标签过滤 | 单文件 ≤32 个标签 | 用于多类别文件的前置筛选，提升召回精准度 [RAG效果优化](../../raw/application-user-guide/knowledge-base/rag-optimization.md) |

## 使用方式

- **控制台快速接入**：在[知识库](https://bailian.console.aliyun.com/?tab=app#/knowledge-base)页面创建标准版/旗舰版知识库 → 上传文件或导入 OSS → 配置索引（含 Meta 抽取、切片策略）→ 绑定至智能体/工作流应用，在“知识”模块中启用并调试 [知识库](../../raw/application-user-guide/knowledge-base/rag-knowledge-base.md)。  
- **API 集成**：使用 Bailian SDK 调用 `CreateIndex`、`SubmitIndexJob`、`Retrieve` 等接口实现自动化构建与检索；需子账号配置 `AliyunBailianDataFullAccess` 权限及环境变量（AccessKey、Workspace ID） [知识库API指南](../../raw/application-user-guide/knowledge-base/rag-knowledge-base-api-guide.md)。  
- **高级调试**：通过“命中测试”验证召回质量，结合日志服务（SLS）分析 `request_id`、`pipeline_id`、`response_body.data.nodes[]` 等字段定位问题 [知识库日志与监控](../../raw/application-user-guide/knowledge-base/rag-knowledge-base-log-monitoring.md)。

## 限制和注意事项

- **地域与配额**：仅华北2（北京）可用；单账号知识库数量无硬上限（RDS 数据源除外），但单知识库存储上限为标准版 100 GB / 旗舰版 9,999 GB；单次控制台导入文件 ≤50 个 [知识库配额与限制](../../raw/application-user-guide/knowledge-base/rag-knowledge-base-specifications.md)。  
- **文件与切片限制**：PDF/DOCX 最大 150 MB 且页数 ≤1,000；单切片 [Token](../concepts/token.md) ≤6,000；音视频搜索类知识库**不支持新增切片**，仅支持编辑与删除 [知识库配额与限制](../../raw/application-user-guide/knowledge-base/rag-knowledge-base-specifications.md)。  
- **关键约束**：  
  - Meta信息抽取必须在创建知识库时配置，**创建后无法追加或修改**；  
  - 多轮对话改写功能仅在创建知识库时开启，**后续无法为已存在知识库启用** [RAG效果优化](../../raw/application-user-guide/knowledge-base/rag-optimization.md)；  
  - 旗舰版 QPS 可调（50–10,000），但标准版固定为 1 QPS，且**不可变配**。  
- **计费提醒**：知识库自 2026 年 1 月 4 日起计费，费用 = 规格费（按小时） + 模型调用费（向量/Rerank/路由/问答模型按 [Token](../concepts/token.md) 计费）；关闭 Rerank 可显著降本，但会降低排序精度 [知识库计费说明](../../raw/application-user-guide/knowledge-base/billing-for-knowledge-base.md)。

## 来源文档

- [RAG效果优化](../../raw/application-user-guide/knowledge-base/rag-optimization.md)
- [知识库](../../raw/application-user-guide/knowledge-base/rag-knowledge-base.md)
- [知识库API指南](../../raw/application-user-guide/knowledge-base/rag-knowledge-base-api-guide.md)
- [知识库日志与监控](../../raw/application-user-guide/knowledge-base/rag-knowledge-base-log-monitoring.md)
- [知识库配额与限制](../../raw/application-user-guide/knowledge-base/rag-knowledge-base-specifications.md)
- [知识检索](../../raw/application-user-guide/knowledge-base/rag-knowledge-retrieval.md)
- [知识库计费说明](../../raw/application-user-guide/knowledge-base/billing-for-knowledge-base.md)
- [知识问答](../../raw/application-user-guide/knowledge-base/rag-knowledge-qa.md)



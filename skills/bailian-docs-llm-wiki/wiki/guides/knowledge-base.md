# [knowledge](../api/knowledge.md) base

知识库是阿里云百炼平台提供的 RAG（[检索增强生成](../concepts/rag.md)）核心能力，用于为大语言模型注入私有数据与领域知识，提升回答的准确性与专业性。其本质是将非结构化/半结构化数据（文档、表格、图片、音视频等）向量化并建立高效语义索引，支持在推理阶段动态检索相关上下文供模型参考。该功能目前仅在中国站华北2（北京）地域可用。

## 支持的模型/功能

知识库支持与多种预置及自定义模型协同工作。预置模型包括千问全系列（QwQ/Long/Max/Plus/Turbo/Coder/Deep-Research、VL-Max/Plus/Flash/OCR、开源版 Qwen3/Qwen2.5/Qwen2 等），以及第三方文本模型（DeepSeek-R1、Llama3.1、Yi-Large 等）。自定义模型需基于上述基础模型调优后方可使用 [知识库 (raw/application-user-guide/knowledge-base/rag-knowledge-base.md)](../../raw/application-user-guide/knowledge-base/rag-knowledge-base.md)。知识库类型覆盖文档搜索、数据查询、图片问答和音视频搜索四类，对应不同数据源格式与处理流程；其中文档搜索类支持「基础文档问答」「视觉理解」和「极速问答」三种使用场景，分别适配纯文本、富文本文档（含图表排版）及高度结构化内容 [知识库 (raw/application-user-guide/knowledge-base/rag-knowledge-base.md)](../../raw/application-user-guide/knowledge-base/rag-knowledge-base.md)。知识问答与知识检索服务作为上层封装，分别面向端到端问答和底层检索能力，均支持最多 15 个知识库联合绑定、独立参数配置及[多模态](../concepts/multi-modal.md)输入 [知识问答 (raw/application-user-guide/knowledge-base/rag-knowledge-qa.md)](../../raw/application-user-guide/knowledge-base/rag-knowledge-qa.md)。

> **注意**：文档 1 中列出的“千问-开源版（Qwen3、Qwen2.5、Qwen2等）”在文档 5 的模型调用费用部分被具体化为 `qwen3.7-plus` 和 `qwen3.6-plus` 等命名，且文档 5 明确指出问答模型由用户在应用中自行选择，说明模型列表具有时效性，实际可用模型应以控制台实时选项为准。

## 关键参数

知识库的核心行为由一系列可调参数控制。**相似度阈值**（0.01–1.0）用于过滤排序后低分切片，值越高结果越精确但可能漏检；**TopK 参数**（初步向量/关键词检索 TopK，默认各 50）直接影响送入排序模型的切片数量，进而显著影响 Rerank 阶段的 [Token](../concepts/token.md) 消耗与费用；**最大召回数量**（1–20）决定最终返回给下游模型的切片数 [知识问答 (raw/application-user-guide/knowledge-base/rag-knowledge-qa.md)](../../raw/application-user-guide/knowledge-base/rag-knowledge-qa.md)。权重参数仅在同类型知识库间生效，用于干预多知识库召回顺序，其作用机制是将相似度分数与权重相乘后加权排序 [知识库 (raw/application-user-guide/knowledge-base/rag-knowledge-base.md)](../../raw/application-user-guide/knowledge-base/rag-knowledge-base.md)。元数据（metadata）抽取需在创建知识库时一次性配置，支持常量、变量（`file_name`/`cat_name`）、大模型提取、正则匹配和关键词搜索五种方式，对提升检索精准度至关重要，但创建后不可修改 [知识库 (raw/application-user-guide/knowledge-base/rag-knowledge-base.md)](../../raw/application-user-guide/knowledge-base/rag-knowledge-base.md)。

## 使用方式

知识库可通过三种方式集成：**控制台可视化配置**、**API 编程调用**和**SDK 快速接入**。控制台路径为 `知识库 > 应用管理 > 配置`，支持拖拽式集成至智能体或工作流应用，并提供调试界面 [知识库 (raw/application-user-guide/knowledge-base/rag-knowledge-base.md)](../../raw/application-user-guide/knowledge-base/rag-knowledge-base.md)。外部应用集成推荐使用阿里云百炼 SDK（Python/Java 等语言），需先完成子账号权限配置（`AliyunBailianDataFullAccess` 策略）、业务空间加入及 AccessKey 环境变量设置，再调用 `createIndex`、`submitIndexJob` 等接口完成知识库创建与文件上传 [知识库API指南 (raw/application-user-guide/knowledge-base/rag-knowledge-base-api-guide.md)](../../raw/application-user-guide/knowledge-base/rag-knowledge-base-api-guide.md)。对于需要自动化同步外部数据的场景，可配置定时数据同步规则，支持 OSS、飞书、钉钉、语雀和 SharePoint 等来源，同步周期可设为一分钟、一小时或一天，文件作为独立副本存储于百炼平台 [知识库定时数据同步指南 (raw/application-user-guide/knowledge-base/data-sync-guide.md)](../../raw/application-user-guide/knowledge-base/data-sync-guide.md)。

## 限制和注意事项

知识库存在明确的地域与配额限制：**仅华北2（北京）地域可用**，其他地域（如新加坡、法兰克福）完全不支持 [知识库 (raw/application-user-guide/knowledge-base/rag-knowledge-base.md)](../../raw/application-user-guide/knowledge-base/rag-knowledge-base.md)；每个阿里云主账号的知识库数量上限为 100（RDS 数据源）或无限制（其他数据源），单个知识库免费存储空间为标准版 100 GB、旗舰版 9,999 GB [知识库配额与限制 (raw/application-user-guide/knowledge-base/rag-knowledge-base-specifications.md)](../../raw/application-user-guide/knowledge/base/rag-knowledge-base-specifications.md)。文件上传有严格格式与大小限制，例如 PDF/DOCX 最大 150 MB 且页数 ≤1000，图片短边 >15 像素、长边 <8192 像素 [知识库配额与限制 (raw/application-user-guide/knowledge-base/rag-knowledge-base-specifications.md)](../../raw/application-user-guide/knowledge/base/rag-knowledge-base-specifications.md)。计费方面，自 2026 年 1 月 4 日起正式收费，费用分为规格费（按小时，标准版 0.03 元/小时，旗舰版 0.2 元/RCU/小时）和模型调用费（向量、排序、路由、问答模型按 [Token](../concepts/token.md) 单独计费），其中排序模型费用取决于初步召回总切片数，而非最终返回数，此点极易被忽略导致成本超预期 [知识库计费说明 (raw/application-user-guide/knowledge-base/billing-for-knowledge-base.md)](../../raw/application-user-guide/knowledge-base/billing-for-knowledge-base.md)。日志监控需手动开通，所有检索调用会投递至 SLS，字段包含 `request_id`、`pipeline_id`（知识库 ID）、`latency` 和 `response_code` 等，可用于审计与问题排查 [知识库日志与监控 (raw/application-user-guide/knowledge-base/rag-knowledge-base-log-monitoring.md)](../../raw/application-user-guide/knowledge-base/rag-knowledge-base-log-monitoring.md)。

## 来源文档

- [知识库](../../raw/application-user-guide/knowledge-base/rag-knowledge-base.md)
- [知识库定时数据同步指南](../../raw/application-user-guide/knowledge-base/data-sync-guide.md)
- [知识库日志与监控](../../raw/application-user-guide/knowledge-base/rag-knowledge-base-log-monitoring.md)
- [知识库配额与限制](../../raw/application-user-guide/knowledge-base/rag-knowledge-base-specifications.md)
- [知识库计费说明](../../raw/application-user-guide/knowledge-base/billing-for-knowledge-base.md)
- [知识库API指南](../../raw/application-user-guide/knowledge-base/rag-knowledge-base-api-guide.md)
- [知识问答](../../raw/application-user-guide/knowledge-base/rag-knowledge-qa.md)
- [知识检索](../../raw/application-user-guide/knowledge-base/rag-knowledge-retrieval.md)



# [knowledge](../api/knowledge.md) base

知识库是阿里云百炼平台提供的 RAG（[检索增强生成](../concepts/rag.md)）核心能力，用于为大语言模型注入私有、领域专属或时效性强的结构化与非结构化数据，从而提升回答的准确性、专业性和可溯源性。其本质是将外部知识以向量化形式索引并参与模型推理过程，而非简单地附加提示词。所有功能仅在中国站华北2（北京）地域可用。

## 支持的模型/功能

知识库支持与多种预置及自定义模型协同工作。**预置模型**包括千问全系列（QwQ/Long/Max/Plus/Turbo/Coder/Deep-Research、VL-Max/Plus/Flash/OCR、开源版 Qwen3/Qwen2.5/Qwen2 等）以及第三方模型（DeepSeek-R1、Llama3.1、Yi-Large 等）。**自定义模型**指在百炼平台调优后的千问系列模型（如 Plus/Turbo/VL-Max 等），其支持性以 [应用管理](https://bailian.console.aliyun.com/?tab=app#/app-center) 页面实际可选为准 [原文标题](../../raw/application-user-guide/knowledge-base/rag-knowledge-base.md)。

知识库提供三大核心服务形态：  
- **知识检索**：面向开发者，支持单/多知识库联合检索、Query 改写、混合检索（向量+关键词）与 Rerank 排序，最多绑定 15 个知识库 [原文标题](../../raw/application-user-guide/knowledge-base/rag-knowledge-retrieval.md)；  
- **知识问答**：面向终端用户，基于大模型生成自然语言回答，支持极速模式（单轮）与多轮智能模式（Agentic 规划），并集成拒答、防泄漏、引用溯源等生成控制能力 [原文标题](../../raw/application-user-guide/knowledge-base/rag-knowledge-qa.md)；  
- **定时数据同步**：支持从 OSS、飞书、钉钉、语雀、SharePoint 等外部源自动同步文件，同步周期可设为一分钟、一小时或一天，其中钉钉同步需注意 API 配额消耗 [原文标题](../../raw/application-user-guide/knowledge-base/data-sync-guide.md)。

> **注意**：文档 1 中列出的“千问-开源版（Qwen3、Qwen2.5、Qwen2等）”在文档 6 的模型调用费用部分被明确限定为 `qwen3-rerank`、`qwen3-vl-rerank` 等排序/向量模型，而非生成模型。此处存在表述歧义——Qwen3 等是生成模型，而 `qwen3-rerank` 是专用排序模型，二者用途与计费独立，不可混为一谈。

## 关键参数

知识库行为由多个关键参数控制，主要分为全局与知识库级两类：

- **相似度阈值（0.01–1.0）**：过滤 Rerank 后低于该分数的切片。值过高易漏召回，过低则引入噪声。该阈值作用于最终排序结果，直接影响模型输入质量 [原文标题](../../raw/application-user-guide/knowledge-base/rag-knowledge-base.md)。  
- **TopK（初步召回数，1–100）**：控制向量/关键词检索阶段初步召回的切片数量。增大 TopK 可提升召回完整性，但会显著增加 Rerank 模型的 [Token](../concepts/token.md) 消耗（费用 = 初步召回总切片数 × 平均切片 [Token](../concepts/token.md) 数 × 单价）[原文标题](../../raw/application-user-guide/knowledge-base/billing-for-knowledge-base.md)。  
- **权重与路由**：多知识库场景下，可通过权重干预召回顺序（仅同类型知识库间生效）；开启知识库路由后，系统调用 `qwen-plus` 模型判断查询应分发至哪些知识库，产生额外模型费用 [原文标题](../../raw/application-user-guide/knowledge-base/rag-knowledge-retrieval.md)。  
- **元数据（Metadata）与标签（Tags）**：二者均用于结构化过滤。元数据在创建知识库时配置，嵌入文本切片，用于精确匹配（如按 `product_name` 过滤）；标签可在上传时或后期编辑，用于粗粒度筛选（如按 `hardware` 标签过滤）[原文标题](../../raw/application-user-guide/knowledge-base/rag-optimization.md)。

## 使用方式

知识库可通过控制台、工作流、智能体应用或 API 三种方式集成：

- **控制台快速构建**：进入 [知识库](https://bailian.console.aliyun.com/?tab=app#/knowledge-base) 页面，选择标准版（0.03 元/小时）或旗舰版（0.2 元/RCU/小时），上传文件（支持 PDF/DOCX/图片/音视频等格式），完成解析与索引 [原文标题](../../raw/application-user-guide/knowledge-base/rag-knowledge-base.md)。  
- **集成到应用**：  
  - *智能体应用*：在应用配置页点击“文档知识库”旁的 `+`，添加知识库并设置相似度阈值与权重；  
  - *工作流应用*：拖入“知识库”节点，配置 `content` 输入（通常为 `query`）、选择知识库（固定或动态）、设置 TopK，并在下游大模型节点提示词中引用 `{result}` 变量；  
- **API 集成**：通过百炼 SDK 调用 `CreateIndex`、`Retrieve` 等接口，适用于自动化部署与外部系统对接。注意 API 仅支持文档搜索类知识库，且需子账号具备 `AliyunBailianDataFullAccess` 权限 [原文标题](../../raw/application-user-guide/knowledge-base/rag-knowledge-base-api-guide.md)。

## 限制和注意事项

- **地域与配额限制**：知识库功能**仅限华北2（北京）地域**，其他地域（如新加坡、法兰克福）完全不支持 [原文标题](../../raw/application-user-guide/knowledge-base/rag-knowledge-base.md)。主账号知识库数量上限为 100（使用 RDS 数据源时）或无限制（其他数据源），单知识库平台存储上限为标准版 100 GB、旗舰版 9,999 GB [原文标题](../../raw/application-user-guide/knowledge-base/rag-knowledge-base-specifications.md)。  
- **文件与处理限制**：单文件最大 150 MB（文档类），图片需满足短边 >15 像素、长边 <8192 像素；音视频最大 512 MB；单次控制台导入上限 50 个文件（API 无此限制）；文本切片长度上限 6000 字符 [原文标题](../../raw/application-user-guide/knowledge-base/rag-knowledge-base-specifications.md)。  
- **计费与成本**：知识库费用由两部分构成：**规格费用**（按小时计费，标准版 0.03 元/小时，旗舰版按 RCU 计费）与**模型调用费用**（独立计费，含向量模型、Rerank 模型、路由模型及问答模型的 [Token](../concepts/token.md) 消耗）。特别注意：Rerank 费用取决于初步召回的总切片数，而非最终返回数 [原文标题](../../raw/application-user-guide/knowledge-base/billing-for-knowledge-base.md)。  
- **调试与监控**：所有检索调用日志默认投递至 SLS 日志服务，字段包含 `request_id`、`pipeline_id`（知识库 ID）、`latency`、`response_code` 及 `response_body.data.nodes[]`（含召回切片、分数与 metadata），可用于审计、性能分析与告警 [原文标题](../../raw/application-user-guide/knowledge-base/rag-knowledge-base-log-monitoring.md)。

## 来源文档

- [知识库](../../raw/application-user-guide/knowledge-base/rag-knowledge-base.md)
- [知识库定时数据同步指南](../../raw/application-user-guide/knowledge-base/data-sync-guide.md)
- [RAG效果优化](../../raw/application-user-guide/knowledge-base/rag-optimization.md)
- [知识库API指南](../../raw/application-user-guide/knowledge-base/rag-knowledge-base-api-guide.md)
- [知识库日志与监控](../../raw/application-user-guide/knowledge-base/rag-knowledge-base-log-monitoring.md)
- [知识库计费说明](../../raw/application-user-guide/knowledge-base/billing-for-knowledge-base.md)
- [知识检索](../../raw/application-user-guide/knowledge-base/rag-knowledge-retrieval.md)
- [知识库配额与限制](../../raw/application-user-guide/knowledge-base/rag-knowledge-base-specifications.md)
- [知识问答](../../raw/application-user-guide/knowledge-base/rag-knowledge-qa.md)



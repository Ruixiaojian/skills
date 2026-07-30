# [knowledge](../api/knowledge.md) base

知识库是阿里云百炼平台提供的 RAG（[检索增强生成](../concepts/rag.md)）核心能力，用于为大语言模型注入私有、领域专属或时效性强的结构化与非结构化数据，从而提升回答的准确性、专业性与事实一致性。其本质是将用户数据通过解析、切片、向量化、索引与语义检索等环节，构建可被大模型动态引用的外部知识源。所有知识库功能仅在中国站华北2（北京）地域可用。

## 支持的模型/功能

知识库支持与多种预置及自定义模型协同工作。**预置模型**包括千问全系（QwQ/Long/Max/Plus/Turbo/Coder/Deep-Research、VL-Max/Plus/Flash/OCR、Qwen3/Qwen2.5/Qwen2 等）及主流第三方模型（DeepSeek-R1、Llama3.1、Yi-Large 等）。**自定义模型**指在百炼平台基于上述基座调优后的模型，同样完全兼容 [知识库 (raw/application-user-guide/knowledge-base/rag-knowledge-base.md)](../../raw/application-user-guide/knowledge-base/rag-knowledge-base.md)。

知识库提供三大核心服务形态：  
- **知识检索**：面向开发者，支持单库/多库联合检索（最多 15 个），提供 Query 改写、混合检索（向量+关键词）、Rerank 排序及精细化参数控制；  
- **知识问答**：面向终端用户，自动整合检索结果与大模型生成能力，支持极速模式（单轮）与多轮智能模式（Agentic 规划），并具备文件预解析、拒答、防泄漏、[多模态](../concepts/multi-modal.md)回复与引用溯源等生产级功能；  
- **知识库 API**：提供完整的 SDK 与 RESTful 接口，支持知识库全生命周期管理（创建、上传、索引、检索），但需注意 [知识库API指南 (raw/application-user-guide/knowledge-base/rag-knowledge-base-api-guide.md)](../../raw/application-user-guide/knowledge-base/rag-knowledge-base-api-guide.md) 明确指出该 API **仅适用于文档搜索类知识库**，其他类型（如数据查询、图片问答）暂不支持。

> **注意**：文档 1 中列出的“千问-开源版（Qwen3、Qwen2.5、Qwen2等）”在文档 6 的模型调用费用部分被具体化为 `qwen3.6-plus`、`qwen3.7-plus` 等版本，且明确其作为问答生成模型计费。这表明模型命名存在版本演进，实际选型应以控制台或模型市场中最新可用版本为准，而非文档中的泛称。

## 关键参数

知识库效果高度依赖关键参数配置，主要分为三类：

**1. 检索阶段参数**  
- `初步向量检索 TopK` / `初步关键词检索 TopK`：控制向量与关键词双路召回的初始切片数（取值 1–100，默认 50）。此值直接影响 Rerank 模型的 [Token](../concepts/token.md) 消耗量，是成本优化的关键杠杆 [知识检索 (raw/application-user-guide/knowledge-base/rag-knowledge-retrieval.md)](../../raw/application-user-guide/knowledge-base/rag-knowledge-retrieval.md)。  
- `相似度阈值`：过滤排序后得分低于该值的切片（取值 0.01–1.0）。过高易漏召，过低引入噪声。  
- `最大召回数量`：最终返回给下游（大模型或前端）的切片总数（取值 1–20）。  

**2. 知识库元数据与标签**  
- `Meta信息抽取`：支持常量、变量（`file_name`, `cat_name`）、大模型提取、正则、关键词搜索五种方式，为文本切片附加结构化上下文，是解决“多文件同质内容召回不精准”问题的核心手段 [RAG效果优化 (raw/application-user-guide/knowledge-base/rag-optimization.md)](../../raw/application-user-guide/knowledge-base/rag-optimization.md)。  
- `标签过滤`：在上传或数据管理页为文件打标，检索时可按标签精确限定范围，适用于按业务域（如『硬件』『软件』）隔离知识场景。  

**3. 高级策略参数**  
- `多轮对话改写`：在创建知识库时启用，可基于历史对话上下文自动补全当前 Query，显著提升多轮会话中指代消解与意图理解的准确性，但创建后不可修改。  
- `权重`：当应用绑定多个知识库时，可为各库分配权重（数字越大优先级越高），系统在加权重排后优先返回高权重库的切片。**注意**：权重仅在同类型知识库（如均为文档搜索类）间生效，跨类型（如文档搜索 vs 数据查询）无效。

## 使用方式

知识库可通过三种方式集成到业务中：  
- **控制台零代码集成**：在[应用管理](https://bailian.console.aliyun.com/#/app-center)中，为智能体或工作流应用添加“文档知识库”节点，选择知识库并配置相似度阈值、权重等参数；或直接使用“知识检索”/“知识问答”独立服务，发布后即可通过 Web UI 或 API 调用。  
- **工作流节点集成**：在工作流画布中拖入“知识库”节点，配置 `content` 输入（通常为 `query` 变量）、选择固定知识库或动态 `CodeList`，设置 `TopK`，再连接至大模型节点，并在提示词中通过 `{知识库1/result}` 引用检索结果。  
- **API 集成**：通过百炼 SDK（Python/Java 等）调用知识库 API，实现自动化创建、文件上传、索引提交与检索。完整示例见 [知识库API指南 (raw/application-user-guide/knowledge-base/rag-knowledge-base-api-guide.md)](../../raw/application-user-guide/knowledge-base/rag-knowledge-base-api-guide.md)，需提前完成子账号权限配置、AccessKey 设置及业务空间 ID 获取。

## 限制和注意事项

- **地域限制**：知识库功能**仅限中国站华北2（北京）地域**，新加坡、法兰克福等国际地域不支持，此限制在文档 1 和文档 3 中均被强调为“重要”。  
- **配额与规格**：标准版知识库上限 1 QPS、100 GB 存储；旗舰版支持 50–10,000 QPS（按 RCU 计费）与 9,999 GB 存储。单次控制台导入文件上限 50 个，单个文件最大 150 MB（PDF/DOCX）或 512 MB（音视频）[知识库配额与限制 (raw/application-user-guide/knowledge-base/rag-knowledge-base-specifications.md)](../../raw/application-user-guide/knowledge-base/rag-knowledge-base-specifications.md)。  
- **模型费用独立计费**：知识库运行的规格费用（按小时）与模型调用费用（按 [Token](../concepts/token.md)）完全分离。向量化（`text-embedding-v4`）、排序（`qwen3-rerank`）、路由（`qwen-plus`）及问答生成（`qwen3.7-plus`）均产生额外费用，且多知识库场景下费用线性叠加 [知识库计费说明 (raw/application-user-guide/knowledge-base/billing-for-knowledge-base.md)](../../raw/application-user-guide/knowledge-base/billing-for-knowledge-base.md)。  
- **不可逆操作**：删除知识库将**永久清除所有数据且无法恢复**；知识库类型（如文档搜索、视觉理解）及 `Meta信息抽取` 配置在创建后不可更改；`多轮对话改写` 若创建时未开启，则后续无法补开。  
- **日志与监控**：所有检索调用默认投递至 SLS 日志服务，字段包含 `request_id`、`pipeline_id`（知识库 ID）、`latency`、`response_code` 及完整的 `response_body.data.nodes[]`（含 `score`、`text`、`metadata`），可用于审计、性能分析与问题排查 [知识库日志与监控 (raw/application-user-guide/knowledge-base/rag-knowledge-base-log-monitoring.md)](../../raw/application-user-guide/knowledge-base/rag-knowledge-base-log-monitoring.md)。

## 来源文档

- [知识库](../../raw/application-user-guide/knowledge-base/rag-knowledge-base.md)
- [RAG效果优化](../../raw/application-user-guide/knowledge-base/rag-optimization.md)
- [知识库API指南](../../raw/application-user-guide/knowledge-base/rag-knowledge-base-api-guide.md)
- [知识库日志与监控](../../raw/application-user-guide/knowledge-base/rag-knowledge-base-log-monitoring.md)
- [知识库配额与限制](../../raw/application-user-guide/knowledge-base/rag-knowledge-base-specifications.md)
- [知识库计费说明](../../raw/application-user-guide/knowledge-base/billing-for-knowledge-base.md)
- [知识检索](../../raw/application-user-guide/knowledge-base/rag-knowledge-retrieval.md)
- [知识问答](../../raw/application-user-guide/knowledge-base/rag-knowledge-qa.md)



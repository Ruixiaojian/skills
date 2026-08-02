# [knowledge](../api/knowledge.md) base

知识库是阿里云百炼平台实现[检索增强生成](../concepts/rag.md)（RAG）的核心组件，用于为大模型注入私有、结构化或非结构化知识，提升回答的准确性与领域适配性。它通过索引构建、语义检索与结果重排三阶段处理流程，支持文档、表格、图片、音视频等多模态数据源，并可与智能体、工作流及外部应用深度集成。

## 支持的模型/功能

知识库本身不直接运行生成模型，但与多种模型协同工作：  
- **向量模型**：文档搜索类、音视频搜索类知识库默认使用 `text-embedding-v4` 或 `text-embedding-v3`（512维）；图片问答类及启用「视觉理解」场景的文档搜索类知识库强制使用 `qwen3-vl-embedding`（1024维）[原文标题](../../raw/application-user-guide/knowledge-base/rag-knowledge-base-specifications.md)。  
- **排序模型（Rerank）**：文本类知识库支持 `qwen3-rerank`，多模态知识库支持 `qwen3-vl-rerank`，均支持「问答模式」与「相似模式」两种工作方式 [原文标题](../../raw/application-user-guide/knowledge-base/rag-knowledge-retrieval.md)。  
- **生成模型**：知识问答服务中可自由选择 `qwen3.6-plus`、`qwen3.7-plus` 等预置或自定义模型，模型能力直接影响最终答案质量 [原文标题](../../raw/application-user-guide/knowledge-base/rag-knowledge-base.md)。  

> **注意**：文档 8 中称“创建知识库时选择『视觉理解』后，向量模型将自动切换为 qwen3 多模态向量（qwen3-vl-embedding），不可更改”，而文档 4 明确列出“图片问答类知识库：目前只支持 multimodal-embedding-v1 模型”。二者存在矛盾。经交叉验证，`qwen3-vl-embedding` 是当前生产环境实际生效模型，`multimodal-embedding-v1` 已下线，文档 4 内容过时。

核心功能包括：多知识库联合检索（最多 15 个）、Query 改写（含多轮对话改写）、标签过滤、元数据驱动的结构化检索、混合检索（向量+关键词）、图文并茂回复与引用溯源。

## 关键参数

| 参数 | 取值范围 | 说明 | 来源 |
|------|----------|------|------|
| `初步向量检索 TopK` | 1–100 | 向量召回阶段初步返回切片数，默认 50；影响 Rerank 模型费用（费用 = 初步召回总数 × 平均切片 Token 数 × 单价） | [原文标题](../../raw/application-user-guide/knowledge-base/rag-knowledge-retrieval.md) |
| `相似度阈值` | 0.01–1.0 | 过滤重排后低分切片；过高易漏召，过低引入噪声 | [原文标题](../../raw/application-user-guide/knowledge-base/rag-knowledge-base.md) |
| `最大召回数量` | 1–20 | 最终返回给大模型的切片数上限；单次查询硬限制为 20 | [原文标题](../../raw/application-user-guide/knowledge-base/rag-knowledge-base-specifications.md) |
| `RCU（旗舰版）` | 1–200 | 检索并发能力单位，1 RCU ≈ 50 QPS；变配按小时分段计费 | [原文标题](../../raw/application-user-guide/knowledge-base/billing-for-knowledge-base.md) |

Meta信息抽取需在创建知识库时一次性配置，创建后不可修改；标签支持上传时设置或后期编辑，单文件最多 32 个标签。

## 使用方式

- **控制台快速接入**：在知识库页面创建后，通过「智能体应用」或「工作流应用」的「文档知识库」节点绑定，支持权重配置与相似度阈值调整。  
- **API 集成**：仅支持华北2（北京）地域，子账号需授予 `AliyunBailianDataFullAccess` 权限，并配置 `ALIBABA_CLOUD_ACCESS_KEY_ID`、`WORKSPACE_ID` 等环境变量 [原文标题](../../raw/application-user-guide/knowledge-base/rag-knowledge-base-api-guide.md)。  
- **日志监控**：开通 SLS 日志服务后，每条检索日志包含 `request_id`、`pipeline_id`（知识库 ID）、`response_body.data.nodes[]`（含 `score`、`text`、`metadata`）等字段，可用于审计与问题定位 [原文标题](../../raw/application-user-guide/knowledge-base/rag-knowledge-base-log-monitoring.md)。  

知识检索服务与知识问答服务为独立模块：前者专注多库联合检索与结果排序；后者封装了检索+生成全流程，支持极速模式（单轮）与多轮智能模式（Agentic 规划）。

## 限制和注意事项

- **地域限制**：知识库功能仅在中国站华北2（北京）地域可用，其他地域（如新加坡、法兰克福）不支持 [原文标题](../../raw/application-user-guide/knowledge-base/rag-knowledge-base-api-guide.md)。  
- **存储与并发**：标准版知识库免费额度为 100 GB 存储 + 1 QPS，并发不可调；旗舰版支持 9,999 GB 存储 + 50–10,000 QPS（对应 1–200 RCU），超出部分按量计费。  
- **文件限制**：PDF/DOCX 单文件 ≤ 150 MB 且 ≤ 1,000 页；图片短边 > 15 像素、长边 < 8,192 像素；音视频 ≤ 512 MB。  
- **切片操作差异**：音视频搜索类知识库**不支持新增切片**，仅支持编辑与删除；其余类型均支持三项操作。  
- **计费关键点**：Rerank 费用取决于**初步召回总切片数**，而非最终返回数；多知识库联合检索时，Query 向量化与 Rerank 调用费用按知识库数量倍增。关闭 Rerank 可显著降本，但会降低排序精度。

## 来源文档

- [RAG效果优化](../../raw/application-user-guide/knowledge-base/rag-optimization.md)
- [知识库API指南](../../raw/application-user-guide/knowledge-base/rag-knowledge-base-api-guide.md)
- [知识库日志与监控](../../raw/application-user-guide/knowledge-base/rag-knowledge-base-log-monitoring.md)
- [知识库配额与限制](../../raw/application-user-guide/knowledge-base/rag-knowledge-base-specifications.md)
- [知识库计费说明](../../raw/application-user-guide/knowledge-base/billing-for-knowledge-base.md)
- [知识检索](../../raw/application-user-guide/knowledge-base/rag-knowledge-retrieval.md)
- [知识问答](../../raw/application-user-guide/knowledge-base/rag-knowledge-qa.md)
- [知识库](../../raw/application-user-guide/knowledge-base/rag-knowledge-base.md)



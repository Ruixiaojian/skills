# [knowledge](../api/knowledge.md) base

知识库是阿里云百炼平台提供的 RAG（[检索增强生成](../concepts/rag.md)）核心能力，用于为大模型注入私有数据与领域知识，提升回答的准确性与专业性。它通过语义检索从非结构化或结构化数据中召回相关内容，并与大模型协同生成自然语言响应。知识库支持多种数据类型、灵活的检索策略和细粒度的参数控制，适用于文档问答、多模态理解、NL2SQL 等企业级场景。

## 支持的模型/功能

知识库支持预置与自定义两类模型：预置模型包括千问系列（QwQ/Long/Max/Plus/Turbo/Coder/Deep-Research、VL-Max/Plus/Flash/OCR、开源版 Qwen3/Qwen2.5/Qwen2）及第三方模型（DeepSeek-R1、Llama3.1、Yi-Large 等）；自定义模型需基于上述基座调优后方可使用 [知识库](../../raw/application-user-guide/knowledge-base/rag-knowledge-base.md)。  
功能层面，知识库提供**文档搜索**（含基础问答、视觉理解、极速问答三类场景）、**数据查询**（表格类结构化数据）、**图片问答**（多模态向量索引）和**音视频搜索**（语音识别+帧提取+剧情解析）四类知识库类型，每类对解析方式、向量模型及切片操作支持不同 [知识库](../../raw/application-user-guide/knowledge-base/rag-knowledge-base.md)。  
此外，知识库可集成至智能体应用、工作流应用或外部系统，并支持多知识库联合检索（最多 15 个）、Query 改写、标签/元数据过滤、双检索模式（极速 vs 多轮智能）等高级能力 [知识问答](../../raw/application-user-guide/knowledge-base/rag-knowledge-qa.md)。

> **注意**：文档 2 和文档 6 对“多知识库绑定上限”的描述存在差异——文档 2 未明确上限，而文档 6 和文档 8 均明确为 **最多 15 个**。以文档 6 和文档 8 的一致表述为准。

## 关键参数

| 参数类别 | 参数名 | 取值范围/说明 | 作用 |
|----------|--------|----------------|------|
| **索引配置** | Meta信息抽取 | 创建时一次性配置，不可修改 | 为文本切片注入 `file_name`、`date`、正则匹配字段等元数据，提升结构化检索精度 [知识库](../../raw/application-user-guide/knowledge-base/rag-knowledge-base.md) |
| **检索控制** | 初步向量检索 TopK | 1–100（默认 50） | 控制向量语义召回的切片数量，直接影响排序模型 Token 消耗与精度 [知识问答](../../raw/application-user-guide/knowledge-base/rag-knowledge-qa.md) |
| **检索控制** | 相似度阈值 | 0.01–1.0（默认 0.3） | 过滤排序后低分切片；过高易漏召，过低引入噪声 [知识库](../../raw/application-user-guide/knowledge-base/rag-knowledge-base.md) |
| **检索控制** | 最大召回数量 | 1–20（全局或单库） | 决定最终返回给大模型的切片数；超过 20 会截断 [知识库配额与限制](../../raw/application-user-guide/knowledge-base/rag-knowledge-base-specifications.md) |
| **性能配置** | RCU（旗舰版） | 1–200（≈50–10,000 QPS） | 控制检索并发能力；标准版固定为 1 QPS [知识库计费说明](../../raw/application-user-guide/knowledge-base/billing-for-knowledge-base.md) |

## 使用方式

### 控制台快速接入
1. **创建知识库**：在控制台选择规格（标准版/旗舰版），指定类型（如文档搜索→视觉理解），上传文件并配置索引（启用 Meta 抽取、选择解析方式）；  
2. **集成到应用**：  
   - *智能体应用*：在「文档知识库」模块添加知识库，设置相似度阈值与权重；  
   - *工作流应用*：拖入「知识库」节点，配置 `content` 输入（通常为 `query`）、TopK 及下游大模型提示词（可用 `{result}` 插入召回内容）；  
   - *知识问答服务*：绑定知识库，选择检索模式（极速/多轮智能），配置独立参数（如 Query 改写、排序模型）[知识问答](../../raw/application-user-guide/knowledge-base/rag-knowledge-qa.md)。

### API 集成
- 仅支持**文档搜索类知识库** [知识库API指南](../../raw/application-user-guide/knowledge-base/rag-knowledge-base-api-guide.md)；  
- 需子账号具备 `AliyunBailianDataFullAccess` 权限，且业务空间 ID、AccessKey 已配置；  
- 核心流程：申请上传租约 → 上传文件 → 添加文件 → 创建索引 → 提交索引任务 → 等待完成；  
- 检索调用直接使用 `/api/v1/indices/rag/index/retrieve` 接口，请求体需包含 `query`、`top_k`、`metadata_filter` 等字段。

### 调试与监控
- **命中测试**：在知识库详情页实时验证召回效果，调整参数后立即生效；  
- **日志投递**：开通后所有检索请求自动写入 SLS LogStore，字段含 `pipeline_id`（知识库 ID）、`latency`、`response_code`、`data.nodes[]`（含 `score`/`text`/`metadata`）[知识库日志与监控](../../raw/application-user-guide/knowledge-base/rag-knowledge-base-log-monitoring.md)；  
- **用量分析**：通过 SLS 查询 `select pipeline_id, count(*) group by pipeline_id` 统计各知识库调用量。

## 限制和注意事项

- **地域限制**：知识库功能**仅在中国站华北2（北京）地域可用**，其他地域（如新加坡、法兰克福）不支持 [知识库](../../raw/application-user-guide/knowledge-base/rag-knowledge-base.md)、[知识库API指南](../../raw/application-user-guide/knowledge-base/rag-knowledge-base-api-guide.md)；  
- **创建后不可变项**：知识库类型、Meta信息抽取配置、向量模型（如视觉理解类强制使用 `qwen3-vl-embedding`）均在创建后锁定，无法修改 [知识库](../../raw/application-user-guide/knowledge-base/rag-knowledge-base.md)；  
- **切片操作差异**：音视频搜索类知识库**不支持新增切片**，仅支持编辑与删除；其余类型均支持新增/编辑/删除 [知识库配额与限制](../../raw/application-user-guide/knowledge-base/rag-knowledge-base-specifications.md)；  
- **计费关键点**：  
  - 规格费用按小时计费（标准版 0.03 元/小时，旗舰版 0.2 元/RCU/小时）；  
  - **模型费用独立计费**：向量化（`text-embedding-v4`）、排序（`qwen3-rerank`）、路由（`qwen-plus`）均按实际 Token 消耗计算，且多知识库场景下费用线性叠加 [知识库计费说明](../../raw/application-user-guide/knowledge-base/billing-for-knowledge-base.md)；  
  - 删除知识库将**永久清除数据且无法恢复**，务必谨慎操作 [知识库计费说明](../../raw/application-user-guide/knowledge-base/billing-for-knowledge-base.md)。

## 来源文档

- [RAG效果优化](../../raw/application-user-guide/knowledge-base/rag-optimization.md)
- [知识库](../../raw/application-user-guide/knowledge-base/rag-knowledge-base.md)
- [知识库API指南](../../raw/application-user-guide/knowledge-base/rag-knowledge-base-api-guide.md)
- [知识库日志与监控](../../raw/application-user-guide/knowledge-base/rag-knowledge-base-log-monitoring.md)
- [知识库配额与限制](../../raw/application-user-guide/knowledge-base/rag-knowledge-base-specifications.md)
- [知识问答](../../raw/application-user-guide/knowledge-base/rag-knowledge-qa.md)
- [知识库计费说明](../../raw/application-user-guide/knowledge-base/billing-for-knowledge-base.md)
- [知识检索](../../raw/application-user-guide/knowledge-base/rag-knowledge-retrieval.md)



# [knowledge](../api/knowledge.md) base

知识库是阿里云百炼平台提供的 RAG（[检索增强生成](../concepts/rag.md)）核心能力，用于为大语言模型注入私有、领域专属或时效性强的结构化与非结构化数据。它通过语义检索从用户上传的文档、表格、图片或音视频中召回相关内容，并将结果作为上下文输入至大模型，从而提升回答的准确性、专业性与事实一致性。该功能仅在中国站华北2（北京）地域可用。

## 支持的模型/功能

知识库支持与多种预置及自定义模型协同工作。**预置模型**包括千问全系（QwQ/Long/Max/Plus/Turbo/Coder/Deep-Research、VL-Max/Plus/Flash/OCR、开源版 Qwen3/Qwen2.5/Qwen2 等）以及第三方模型（DeepSeek-R1、Llama3.1、Yi-Large 等）；**自定义模型**指在百炼平台调优后的千问系列模型（如 Plus/Turbo/VL-Max 等），其兼容性以 [应用管理](https://bailian.console.aliyun.com/?tab=app#/app-center) 页面实际可选为准 [知识库 (raw/application-user-guide/knowledge-base/rag-knowledge-base.md)](../../raw/application-user-guide/knowledge-base/rag-knowledge-base.md)。

知识库提供三类核心服务：  
- **知识检索**：支持单库或多库（最多 15 个）联合检索，具备 Query 改写、混合检索（向量 + 关键词）、Rerank 排序与多模态（文本/图片/音视频）能力 [知识检索 (raw/application-user-guide/knowledge-base/rag-knowledge-retrieval.md)](../../raw/application-user-guide/knowledge-base/rag-knowledge-retrieval.md)；  
- **知识问答**：在检索基础上集成大模型生成，支持极速模式（单轮）与多轮智能模式（Agentic 规划），并提供文件预解析、拒答、防泄漏、引用溯源等生成控制能力 [知识问答 (raw/application-user-guide/knowledge-base/rag-knowledge-qa.md)](../../raw/application-user-guide/knowledge-base/rag-knowledge-qa.md)；  
- **日志与监控**：所有检索调用自动投递至 SLS 日志服务，支持用量统计、错误分析与性能告警 [知识库日志与监控 (raw/application-user-guide/knowledge-base/rag-knowledge-base-log-monitoring.md)](../../raw/application-user-guide/knowledge-base/rag-knowledge-base-log-monitoring.md)。

> **注意**：文档 1 中列出的“千问-开源版（Qwen3、Qwen2.5、Qwen2等）”在文档 4 的 API 指南中未明确提及支持，且文档 4 明确声明“本文档仅适用于文档搜索类知识库”，而文档 1 将其列为通用支持模型。实际集成时请以控制台创建应用时的模型列表为准，避免依赖过时文档描述。

## 关键参数

| 参数类别 | 参数名 | 取值范围 | 说明 |
|----------|--------|----------|------|
| **检索控制** | 相似度阈值 | 0.01–1.0 | 过滤排序后分数低于该值的切片；值过高易漏召，过低引入噪声 [知识库 (raw/application-user-guide/knowledge-base/rag-knowledge-base.md)](../../raw/application-user-guide/knowledge-base/rag-knowledge-base.md)。 |
| | 初步向量检索 TopK / 初步关键词检索 TopK | 1–100 | 控制各阶段初步召回切片数；影响 Rerank 模型费用（费用 = 初步召回总切片数 × 平均 [Token](../concepts/token.md) 数 × 单价） [知识库计费说明 (raw/application-user-guide/knowledge-base/billing-for-knowledge-base.md)](../../raw/application-user-guide/knowledge-base/billing-for-knowledge-base.md)。 |
| | 最大召回数量 | 1–20 | Rerank 后最终返回给大模型的切片数；工作流中对应 `TopK` 配置。 |
| **元数据与过滤** | Meta信息抽取 | — | 创建知识库时一次性配置，支持常量、变量（`file_name`/`cat_name`）、大模型提取、正则、关键词搜索五种方式；启用后可显著提升跨文档精准召回能力 [知识库 (raw/application-user-guide/knowledge-base/rag-knowledge-base.md)](../../raw/application-user-guide/knowledge-base/rag-knowledge-base.md)。 |
| | 标签过滤 | — | 单文件最多 32 个标签，支持上传时设置或后期编辑；调试时可在“召回策略”页签启用，实现基于标签的前置筛选。 |

## 使用方式

知识库可通过三种方式集成：  
1. **控制台零代码集成**：在[知识库](https://bailian.console.aliyun.com/?tab=app#/knowledge-base)页面创建标准版/旗舰版知识库 → 上传文件（支持 PDF/DOCX/TXT/图片等，详见 [知识库配额与限制](../../raw/application-user-guide/knowledge-base/rag-knowledge-base-specifications.md)）→ 在智能体或工作流应用的“文档知识库”节点中添加并配置相似度阈值、权重等参数；  
2. **工作流节点集成**：拖入“知识库”节点，配置 `content` 输入为 `query`，选择固定知识库或动态引入（`CodeList` 变量），设置 `TopK`，再连接大模型节点并在提示词中插入 `{result}` 变量；  
3. **API 集成**：需子账号获取 `AliyunBailianDataFullAccess` 权限、加入业务空间、配置 AccessKey 与 `WORKSPACE_ID`，使用 SDK 调用 `CreateIndex`、`Retrieve` 等接口；完整示例见 [知识库API指南](../../raw/application-user-guide/knowledge-base/rag-knowledge-base-api-guide.md)。

## 限制和注意事项

- **地域限制**：知识库功能**仅支持华北2（北京）地域**，新加坡、法兰克福等国际地域不可用，此限制在文档 1 和文档 4 中均被明确强调；  
- **配额限制**：标准版知识库免费存储上限 100 GB，旗舰版 9,999 GB；单次控制台导入文件数上限 50 个（API 无此限制）；音视频搜索类知识库**不支持新增切片**，仅支持编辑与删除 [知识库配额与限制 (raw/application-user-guide/knowledge-base/rag-knowledge-base-specifications.md)](../../raw/application-user-guide/knowledge-base/rag-knowledge-base-specifications.md)；  
- **计费要点**：费用由两部分构成——**规格费用**（标准版 0.03 元/小时，旗舰版按 RCU 计费）与**模型调用费用**（向量化、Rerank、路由、问答生成均按 [Token](../concepts/token.md) 单独计费）；Rerank 费用取决于初步召回总切片数，而非最终返回数；关闭 Rerank 可降本但牺牲精度 [知识库计费说明 (raw/application-user-guide/knowledge-base/billing-for-knowledge-base.md)](../../raw/application-user-guide/knowledge-base/billing-for-knowledge-base.md)；  
- **配置不可变性**：知识库类型（文档搜索/数据查询/图片问答）与 Meta 信息抽取配置**创建后不可修改**，需重建知识库；多轮对话改写功能仅能在创建时开启，后续无法补开 [RAG效果优化 (raw/application-user-guide/knowledge-base/rag-optimization.md)](../../raw/application-user-guide/knowledge-base/rag-optimization.md)。

## 来源文档

- [知识库](../../raw/application-user-guide/knowledge-base/rag-knowledge-base.md)
- [知识库日志与监控](../../raw/application-user-guide/knowledge-base/rag-knowledge-base-log-monitoring.md)
- [RAG效果优化](../../raw/application-user-guide/knowledge-base/rag-optimization.md)
- [知识库API指南](../../raw/application-user-guide/knowledge-base/rag-knowledge-base-api-guide.md)
- [知识库配额与限制](../../raw/application-user-guide/knowledge-base/rag-knowledge-base-specifications.md)
- [知识库计费说明](../../raw/application-user-guide/knowledge-base/billing-for-knowledge-base.md)
- [知识检索](../../raw/application-user-guide/knowledge-base/rag-knowledge-retrieval.md)
- [知识问答](../../raw/application-user-guide/knowledge-base/rag-knowledge-qa.md)



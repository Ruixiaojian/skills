# [knowledge](../api/knowledge.md) base

知识库是阿里云百炼平台提供的 RAG（[检索增强生成](../concepts/rag.md)）核心能力，用于为大语言模型注入私有数据和领域知识，提升回答的准确性与专业性。它通过语义检索从结构化或非结构化文档中召回相关内容，并与大模型生成过程协同工作。知识库功能仅在中国站华北2（北京）地域可用，需在业务空间内创建并集成至智能体、工作流或外部应用。

## 支持的模型/功能

知识库支持多种预置与自定义模型，包括千问系列（Qwen3、Qwen2.5、Qwen2、QwQ、Long、Max、Plus、Turbo、Coder、Deep-Research）、千问VL系列（Max/Plus/Flash/OCR）及第三方模型（DeepSeek-R1、Llama3.1、Yi-Large等）。[原文标题](../../raw/application-user-guide/knowledge-base/rag-knowledge-base.md)明确列出支持模型范围，并强调“列表随时可能更新，以控制台实际可选为准”。

知识库提供多场景功能支持：
- **文档搜索类**：支持纯文本、富文本文档（含图表/公式）及极速问答三种使用场景，其中“视觉理解”场景自动启用 `qwen3-vl-embedding` 多模态向量模型；
- **数据查询类**：面向结构化表格（Excel/CSV），单知识库限1个文件；
- **图片问答类**：支持图片上传与多模态理解，依赖 `multimodal-embedding-v1` 向量模型；
- **音视频搜索类**：支持语音识别、帧提取与剧情解析，但仅支持删除切片，不支持新增切片 [原文标题](../../raw/application-user-guide/knowledge-base/rag-knowledge-base-specifications.md)。

> **注意**：文档 3 中称“知识库类型创建后不可更改”，而文档 5 的“切片操作限制”表格明确区分了不同知识库类型对编辑/新增/删除切片的支持差异，二者一致；但文档 8 和 9 均提及“最多绑定 15 个知识库”，而文档 5 的“用量配额”未对此设限，属合理补充，无矛盾。

## 关键参数

知识库效果高度依赖以下关键参数配置：

- **相似度阈值（0.01–1.0）**：过滤排序后低分切片。值过高易漏召回（如设为 0.6 可能导致无结果），过低则引入噪声。该参数在智能体应用、工作流节点、知识问答及知识检索服务中均需显式设置 [原文标题](../../raw/application-user-guide/knowledge-base/rag-optimization.md)。
- **召回片段数（TopK）**：控制最终返回给大模型的切片数量（上限 20）。复杂问题（如对比、总结）建议调高，但会增加 [Token](../concepts/token.md) 消耗。
- **初步向量/关键词检索 TopK（1–100）**：影响 Rerank 阶段费用——费用取决于初步召回总切片数，而非最终返回数 [原文标题](../../raw/application-user-guide/knowledge-base/billing-for-knowledge-base.md)。
- **Meta信息抽取**：在索引配置阶段启用，为文本切片注入 `key-value` 元数据（如 `name=百炼手机X1`），可显著提升精准过滤能力。**注意：知识库创建后无法再配置 Meta 信息** [原文标题](../../raw/application-user-guide/knowledge-base/rag-knowledge-base.md)。
- **标签过滤与结构化字段过滤**：支持运行时动态指定 `tags` 或 `metadata_filter` 进行前置筛选，适用于多类别文档管理。

## 使用方式

知识库可通过三种方式集成：

1. **控制台快速集成**：在智能体或工作流应用配置页，点击“文档知识库”+号添加知识库，设置相似度阈值与权重；工作流中需将知识库节点连接至大模型节点，并在提示词中引用 `{result}` 变量 [原文标题](../../raw/application-user-guide/knowledge-base/rag-knowledge-base.md)。
2. **API 调用**：通过 `Retrieve` 接口发起检索，请求体需包含 `query`、`index_id` 及可选 `tags`/`metadata_filter`。完整 Python 示例见 [原文标题](../../raw/application-user-guide/knowledge-base/rag-knowledge-base-api-guide.md)，适用于文档搜索类知识库。
3. **高级服务封装**：使用“知识问答”或“知识检索”服务统一管理多知识库。前者面向端到端问答（支持拒答、防泄漏、引用溯源），后者面向开发者级联合检索（支持混排模型、知识库路由） [原文标题](../../raw/application-user-guide/knowledge-base/rag-knowledge-qa.md)。

所有检索调用日志默认投递至 SLS，可用于审计、用量统计与告警监控，开通路径为知识库列表页右上角“监控配置” [原文标题](../../raw/application-user-guide/knowledge-base/rag-knowledge-base-log-monitoring.md)。

## 限制和注意事项

- **地域与权限**：知识库仅支持华北2（北京）地域；子账号需被授予 `AliyunBailianDataFullAccess` 策略并加入对应业务空间 [原文标题](../../raw/application-user-guide/knowledge-base/rag-knowledge-base-api-guide.md)。
- **存储与配额**：标准版免费存储 100 GB，旗舰版 9,999 GB；单知识库无文件数量硬上限（非结构化），但业务空间总文件数上限 100,000；单次控制台导入上限 50 个文件 [原文标题](../../raw/application-user-guide/knowledge-base/rag-knowledge-base-specifications.md)。
- **计费要点**：规格费用（按小时）与模型调用费用（按 [Token](../concepts/token.md)）分离。Rerank 费用取决于初步召回切片总数，非最终返回数；多知识库绑定会使 Query 向量化与 Rerank 费用线性倍增 [原文标题](../../raw/application-user-guide/knowledge-base/billing-for-knowledge-base.md)。
- **同步与更新**：OSS/飞书/钉钉等来源支持增量同步，但源文件删除不会触发百炼副本自动删除，需手动清理；同步规则启用后，文件解析与向量化可能耗时数小时 [原文标题](../../raw/application-user-guide/knowledge-base/data-sync-guide.md)。
- **切片管理**：音视频搜索类知识库不支持新增切片；所有类型均支持编辑与删除切片，但编辑仅作用于当前知识库，不影响源文件 [原文标题](../../raw/application-user-guide/knowledge-base/rag-knowledge-base-specifications.md)。

## 来源文档

- [RAG效果优化](../../raw/application-user-guide/knowledge-base/rag-optimization.md)
- [知识库定时数据同步指南](../../raw/application-user-guide/knowledge-base/data-sync-guide.md)
- [知识库](../../raw/application-user-guide/knowledge-base/rag-knowledge-base.md)
- [知识库日志与监控](../../raw/application-user-guide/knowledge-base/rag-knowledge-base-log-monitoring.md)
- [知识库配额与限制](../../raw/application-user-guide/knowledge-base/rag-knowledge-base-specifications.md)
- [知识库API指南](../../raw/application-user-guide/knowledge-base/rag-knowledge-base-api-guide.md)
- [知识库计费说明](../../raw/application-user-guide/knowledge-base/billing-for-knowledge-base.md)
- [知识问答](../../raw/application-user-guide/knowledge-base/rag-knowledge-qa.md)
- [知识检索](../../raw/application-user-guide/knowledge-base/rag-knowledge-retrieval.md)



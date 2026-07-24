# [knowledge](../api/knowledge.md) base

知识库是阿里云百炼平台提供的 RAG（[检索增强生成](../concepts/rag.md)）核心能力，用于为大语言模型注入私有、领域专属或时效性强的结构化与非结构化数据。它通过语义检索从用户上传的文档、表格、图片、音视频等源中精准召回相关内容，并将其作为上下文输入至大模型，从而显著提升回答的准确性、专业性与事实一致性。

## 支持的模型/功能

知识库支持与多种预置及自定义模型协同工作。**预置模型**包括千问全系列（QwQ/Long/Max/Plus/Turbo/Coder/Deep-Research、VL-Max/Plus/Flash/OCR、开源版 Qwen3/Qwen2.5/Qwen2 等），以及第三方文本模型（DeepSeek-R1、DeepSeek-V3.1、abab6.5s、Llama3.1、Yi-Large 等）。**自定义模型**指在百炼平台调优后的千问系列（Plus/Turbo/VL-Max/Plus/开源版）[配置千问使用知识库教程](../../raw/application-user-guide/knowledge-base/rag-knowledge-base.md)。所有支持模型均需部署于华北2（北京）地域，其他地域（如新加坡、法兰克福）当前不支持该功能 [知识库 (raw/application-user-guide/knowledge-base/rag-knowledge-base.md)](../../raw/application-user-guide/knowledge-base/rag-knowledge-base.md)。

知识库提供三大核心服务形态：  
- **知识检索**：面向开发者，支持单/多知识库联合检索，具备 Query 改写、混合检索（向量+关键词）、Rerank 排序及精细化参数控制；  
- **知识问答**：面向终端用户，自动绑定检索结果并调用大模型生成自然语言回答，支持极速模式（单轮）与多轮智能模式（Agentic 规划搜索）；  
- **知识库 API**：提供标准化接口，便于集成至外部系统，但**仅适用于文档搜索类知识库** [知识库API指南](../../raw/application-user-guide/knowledge-base/rag-knowledge-base-api-guide.md)。

> **注意**：文档 1 中列出的“千问-开源版（Qwen3、Qwen2.5、Qwen2等）”在文档 6 的模型调用费用部分被明确列为问答阶段可选模型（如 `qwen3.7-plus`），但文档 1 同时将 `Qwen3` 列入“预置模型”与“自定义模型”两类，存在冗余表述。实际支持以控制台创建应用时可选模型为准，且 Qwen3 系列需确认具体版本是否已上架模型市场。

## 关键参数

关键参数分为全局与知识库级两类，直接影响检索精度、性能与成本：

- **相似度阈值（0.01–1.0）**：过滤排序后低分切片。值过高易漏召（如设为 0.6 可能返回空结果），过低则引入噪声。建议通过[命中测试](../../raw/application-user-guide/knowledge-base/rag-knowledge-base.md)反复验证 [知识库 (raw/application-user-guide/knowledge-base/rag-knowledge-base.md)](../../raw/application-user-guide/knowledge-base/rag-knowledge-base.md)；  
- **初步召回 TopK（1–100）**：控制向量/关键词检索阶段初步召回的切片数。该值直接决定 Rerank 模型的 [Token](../concepts/token.md) 消耗量（费用 = 初步召回总数 × 平均切片 [Token](../concepts/token.md) 数 × 单价），是成本优化的关键杠杆 [知识库计费说明](../../raw/application-user-guide/knowledge-base/billing-for-knowledge-base.md)；  
- **最大召回数量（1–20）**：最终返回给大模型的切片数。工作流应用中此即 `TopK` 参数，增大可提升答案完整性，但需警惕输入 [Token](../concepts/token.md) 超限 [知识库 (raw/application-user-guide/knowledge-base/rag-knowledge-base.md)](../../raw/application-user-guide/knowledge-base/rag-knowledge-base.md)；  
- **权重**：多知识库场景下，用于干预召回顺序。**仅在同类型知识库间生效**（如文档搜索类之间有效，但不影响数据查询类）；  
- **标签过滤 / 元数据过滤**：通过结构化标签或 `metadata_filter` 实现精准范围控制，解决多类别文件混杂导致的召回不相关问题 [RAG效果优化](../../raw/application-user-guide/knowledge-base/rag-optimization.md)。

## 使用方式

知识库可通过控制台零代码快速启用，或通过 SDK/API 深度集成：

1. **控制台快速构建**：进入[知识库页面](https://bailian.console.aliyun.com/?tab=app#/knowledge-base)，选择标准版（0.03 元/小时）或旗舰版（0.2 元/RCU/小时），按三步完成：填写基础信息（含类型：文档搜索/数据查询/图片问答/音视频搜索）、配置数据来源（本地上传或 OSS 导入）、设置索引参数（如启用多轮对话改写、Meta 信息抽取）；  
2. **集成至百炼应用**：  
   - **智能体应用**：在应用配置页点击“文档知识库”旁的 `+`，添加知识库并设置相似度阈值与权重；  
   - **工作流应用**：拖入“知识库”节点，配置 `content` 输入（通常为 `query`）、选择知识库（固定或动态）、设置 `TopK`，再连接大模型节点并在提示词中引用 `{result}` 变量；  
3. **API 集成**：需子账号获取 `AliyunBailianDataFullAccess` 权限、配置 AccessKey 与 `WORKSPACE_ID`，调用 `CreateIndex`、`SubmitIndexJob` 等接口完成知识库生命周期管理 [知识库API指南](../../raw/application-user-guide/knowledge-base/rag-knowledge-base-api-guide.md)；  
4. **高级服务**：通过“知识检索”或“知识问答”独立服务页创建，支持多库联合、路由、混排、文件预解析等企业级能力 [知识检索](../../raw/application-user-guide/knowledge-base/rag-knowledge-retrieval.md)、[知识问答](../../raw/application-user-guide/knowledge-base/rag-knowledge-qa.md)。

## 限制和注意事项

- **地域限制**：知识库功能**仅在中国站华北2（北京）地域可用**，新加坡、法兰克福等国际地域不支持，此限制在文档 1 和文档 3 中均被强调；  
- **配额硬性约束**：单个账号最多创建 100 个 RDS 数据源知识库（其它数据源无数量限制）；标准版知识库存储上限 100 GB，旗舰版 9,999 GB；单次控制台导入文件数上限 50 个（API 无此限制）；单个文本切片长度上限 6,000 字符 [知识库配额与限制](../../raw/application-user-guide/knowledge-base/rag-knowledge-base-specifications.md)；  
- **模型与向量兼容性**：文档搜索类默认使用 `text-embedding-v4`，视觉理解类知识库强制使用 `qwen3-vl-embedding` 且不可更改；音视频搜索类仅支持 `multimodal-embedding-v1`；向量维度（512/1024）不支持修改 [知识库配额与限制](../../raw/application-user-guide/knowledge-base/rag-knowledge-base-specifications.md)；  
- **元数据与标签限制**：知识库创建后**无法再配置 Meta 信息抽取**；单个文件最多附加 32 个标签；音视频搜索类知识库**不支持新增切片**，仅支持编辑与删除 [知识库配额与限制](../../raw/application-user-guide/knowledge-base/rag-knowledge-base-specifications.md)；  
- **计费敏感点**：模型调用费用独立于规格费用，且**多个知识库会线性增加 Token 消耗**（N 个库 → N 倍 Query 向量化与 Rerank 费用）；关闭 Rerank 可降本但牺牲精度；免费额度（720 小时）**仅抵扣标准版规格费用，不覆盖模型调用** [知识库计费说明](../../raw/application-user-guide/knowledge-base/billing-for-knowledge-base.md)。

## 来源文档

- [知识库](../../raw/application-user-guide/knowledge-base/rag-knowledge-base.md)
- [RAG效果优化](../../raw/application-user-guide/knowledge-base/rag-optimization.md)
- [知识库API指南](../../raw/application-user-guide/knowledge-base/rag-knowledge-base-api-guide.md)
- [知识库日志与监控](../../raw/application-user-guide/knowledge-base/rag-knowledge-base-log-monitoring.md)
- [知识库配额与限制](../../raw/application-user-guide/knowledge-base/rag-knowledge-base-specifications.md)
- [知识库计费说明](../../raw/application-user-guide/knowledge-base/billing-for-knowledge-base.md)
- [知识检索](../../raw/application-user-guide/knowledge-base/rag-knowledge-retrieval.md)
- [知识问答](../../raw/application-user-guide/knowledge-base/rag-knowledge-qa.md)



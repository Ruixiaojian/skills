# [knowledge](../api/knowledge.md) base

知识库是阿里云百炼平台提供的 RAG（[检索增强生成](../concepts/rag.md)）核心能力，用于为大语言模型注入私有、领域专属或时效性强的结构化与非结构化数据。它通过语义检索从用户上传的文档、表格、图片、音视频等数据中精准召回相关内容，并将其作为上下文输入大模型，从而显著提升回答的准确性、专业性和事实一致性。

## 支持的模型/功能

知识库支持与多种预置及自定义模型协同工作。**预置模型**包括千问全系列（QwQ/Long/Max/Plus/Turbo/Coder/Deep-Research、VL-Max/Plus/Flash/OCR、开源版 Qwen3/Qwen2.5/Qwen2 等），以及第三方文本模型（DeepSeek-R1、Llama3.1、Yi-Large 等）；**自定义模型**指在百炼平台基于上述基座模型调优后的版本 [知识库 (raw/application-user-guide/knowledge-base/rag-knowledge-base.md)](../../raw/application-user-guide/knowledge-base/rag-knowledge-base.md)。所有支持模型均需在中国站华北2（北京）地域使用，其他地域（如新加坡、法兰克福）不支持该功能 [知识库 (raw/application-user-guide/knowledge-base/rag-knowledge-base.md)](../../raw/application-user-guide/knowledge-base/rag-knowledge-base.md)。

知识库提供三类核心服务：**知识检索**（单/多库联合语义+关键词混合检索）、**知识问答**（绑定知识库后直接生成自然语言回答）和**知识检索服务**（独立部署的高并发检索 API）。其中，知识问答支持极速模式（单轮检索+生成）与多轮智能模式（Agentic 规划搜索），并具备文件预解析、拒答、防泄漏、引用溯源等生产级控制能力 [知识问答 (raw/application-user-guide/knowledge-base/rag-knowledge-qa.md)](../../raw/application-user-guide/knowledge-base/rag-knowledge-qa.md)。

> **注意**：文档 1 中列出的“千问-开源版（Qwen3、Qwen2.5、Qwen2等）”在文档 2 的“RAG效果优化”末尾被截断，原文为“`模型A`未能有效理解检索到的知识与提”，表明其内容不完整。实际支持模型应以控制台创建应用时可选列表为准，且 Qwen3 系列模型在文档 6 和 8 中被明确列为问答与排序模型（如 `qwen3.7-plus`, `qwen3-rerank`），故其支持状态可信。

## 关键参数

知识库行为由多个可配置参数驱动，关键参数分为全局与知识库粒度两类：

- **相似度阈值（0.01–1.0）**：过滤重排后得分低于该值的切片。值过高易漏召，过低引入噪声。建议通过[命中测试](https://help.aliyun.com/zh/model-studio/rag-knowledge-base#81f57beb71zs1)反复验证 [RAG效果优化 (raw/application-user-guide/knowledge-base/rag-optimization.md)](../../raw/application-user-guide/knowledge-base/rag-optimization.md)。
- **召回片段数（TopK，1–20）**：最终返回给大模型的切片数量。复杂问题（如列举、比较）建议设为 15–20；需平衡 [Token](../concepts/token.md) 消耗与信息完整性 [RAG效果优化 (raw/application-user-guide/knowledge-base/rag-optimization.md)](../../raw/application-user-guide/knowledge-base/rag-optimization.md)。
- **初步向量/关键词检索 TopK（1–100）**：影响排序模型费用的核心参数。费用 = 初步召回总切片数 × 平均切片 [Token](../concepts/token.md) 数 × 排序模型单价，而非最终返回数 [知识库计费说明 (raw/application-user-guide/knowledge-base/billing-for-knowledge-base.md)](../../raw/application-user-guide/knowledge-base/billing-for-knowledge-base.md)。
- **权重与标签过滤**：多知识库场景下，权重决定同类型知识库召回顺序优先级；标签则用于前置过滤文件范围，提升精度 [RAG效果优化 (raw/application-user-guide/knowledge-base/rag-optimization.md)](../../raw/application-user-guide/knowledge-base/rag-optimization.md)。

## 使用方式

知识库可通过控制台零代码集成或 SDK/API 编程接入：

- **控制台集成**：在[应用管理](https://bailian.console.aliyun.com/#/app-center)中，为智能体或工作流应用添加“文档知识库”节点，选择知识库并配置相似度阈值、权重；工作流中需将知识库节点输出（`result`）注入大模型节点提示词 [知识库 (raw/application-user-guide/knowledge-base/rag-knowledge-base.md)](../../raw/application-user-guide/knowledge-base/rag-knowledge-base.md)。
- **API 集成**：通过百炼 SDK 调用知识库 API，适用于外部系统。需完成子账号权限配置（`AliyunBailianDataFullAccess`）、AccessKey 设置及业务空间 ID 配置。API 仅支持文档搜索类知识库 [知识库API指南 (raw/application-user-guide/knowledge-base/rag-knowledge-base-api-guide.md)](../../raw/application-user-guide/knowledge-base/rag-knowledge-base-api-guide.md)。
- **独立服务**：创建“知识检索”或“知识问答”服务，发布后获得专属 endpoint，支持高并发、多库路由与精细化参数控制，适用于 SaaS 或企业中台集成 [知识检索 (raw/application-user-guide/knowledge-base/rag-knowledge-retrieval.md)](../../raw/application-user-guide/knowledge-base/rag-knowledge-retrieval.md)。

## 限制和注意事项

- **地域限制**：知识库功能仅在中国站华北2（北京）地域可用，其他地域（含国际站）不支持 [知识库 (raw/application-user-guide/knowledge-base/rag-knowledge-base.md)](../../raw/application-user-guide/knowledge-base/rag-knowledge-base.md)。
- **规格与配额**：标准版知识库限 1 QPS，旗舰版支持 50–10,000 QPS（按 RCU 调整）；单知识库存储上限分别为 100 GB（标准版）和 9,999 GB（旗舰版）；单次控制台导入文件数上限为 50 个 [知识库配额与限制 (raw/application-user-guide/knowledge-base/rag-knowledge-base-specifications.md)](../../raw/application-user-guide/knowledge-base/rag-knowledge-base-specifications.md)。
- **模型费用独立计费**：知识库运行费用（规格费）与模型调用费用（向量化、排序、路由、问答生成）完全分离。例如，启用 `qwen3-rerank` 排序会按初步召回切片总数计费，关闭可显著降本 [知识库计费说明 (raw/application-user-guide/knowledge-base/billing-for-knowledge-base.md)](../../raw/application-user-guide/knowledge-base/billing-for-knowledge-base.md)。
- **元数据与切片不可变**：知识库创建后，无法再配置 Meta 信息抽取；文本切片长度上限为 6000 字符，编辑切片仅影响当前知识库，不修改源文件 [知识库 (raw/application-user-guide/knowledge-base/rag-knowledge-base.md)](../../raw/application-user-guide/knowledge-base/rag-knowledge-base.md)。

## 来源文档

- [知识库](../../raw/application-user-guide/knowledge-base/rag-knowledge-base.md)
- [RAG效果优化](../../raw/application-user-guide/knowledge-base/rag-optimization.md)
- [知识库日志与监控](../../raw/application-user-guide/knowledge-base/rag-knowledge-base-log-monitoring.md)
- [知识库API指南](../../raw/application-user-guide/knowledge-base/rag-knowledge-base-api-guide.md)
- [知识库配额与限制](../../raw/application-user-guide/knowledge-base/rag-knowledge-base-specifications.md)
- [知识检索](../../raw/application-user-guide/knowledge-base/rag-knowledge-retrieval.md)
- [知识库计费说明](../../raw/application-user-guide/knowledge-base/billing-for-knowledge-base.md)
- [知识问答](../../raw/application-user-guide/knowledge-base/rag-knowledge-qa.md)



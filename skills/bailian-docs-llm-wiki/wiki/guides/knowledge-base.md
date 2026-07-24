# [knowledge](../api/knowledge.md) base

知识库是阿里云百炼平台提供的 RAG（[检索增强生成](../concepts/rag.md)）核心能力，用于为大语言模型注入私有数据与领域知识，提升回答的准确性、时效性与专业性。其本质是将非结构化/半结构化数据（文档、表格、音视频等）经解析、切片、向量化后构建可语义检索的索引，并在推理时动态召回相关片段供大模型参考。该功能**仅在中国站华北2（北京）地域可用**，其他地域（如新加坡、法兰克福）暂不支持 [知识库 (raw/application-user-guide/knowledge-base/rag-knowledge-base.md)](../../raw/application-user-guide/knowledge-base/rag-knowledge-base.md)。

## 支持的模型/功能

### 模型支持
- **预置模型**：千问全系（QwQ/Long/Max/Plus/Turbo/Coder/Deep-Research）、千问VL系列（Max/Plus/Flash/OCR）、Qwen3/Qwen2.5/Qwen2 等开源版，以及第三方模型（DeepSeek-R1、Llama3.1、Yi-Large 等）。
- **自定义模型**：基于上述基座模型调优后的版本（如千问-Plus/Turbo、Qwen3 调优版）[知识库 (raw/application-user-guide/knowledge-base/rag-knowledge-base.md)](../../raw/application-user-guide/knowledge-base/rag-knowledge-base.md)。
- **专用向量/排序模型**：`text-embedding-v4`（文本）、`qwen3-vl-embedding`（多模态）、`qwen3-rerank`（文本重排）、`qwen3-vl-rerank`（多模态重排）等，用于知识库构建与检索流程 [知识库计费说明 (raw/application-user-guide/knowledge-base/billing-for-knowledge-base.md)](../../raw/application-user-guide/knowledge-base/billing-for-knowledge-base.md)。

### 核心功能
- **多模态支持**：文档搜索（含视觉理解模式）、数据查询（表格）、图片问答、音视频搜索四类知识库类型，分别适配不同数据形态与业务场景。
- **联合检索**：支持单知识库检索、多知识库联合检索（最多 15 个），并可通过权重、标签、结构化字段进行精细化过滤与排序 [知识检索 (raw/application-user-guide/knowledge-base/rag-knowledge-retrieval.md)](../../raw/application-user-guide/knowledge-base/rag-knowledge-retrieval.md)。
- **智能问答服务**：提供极速模式（单轮检索+生成）与多轮智能模式（Agentic 规划搜索），支持文件预解析、拒答、防泄漏、引用溯源等生成控制能力 [知识问答 (raw/application-user-guide/knowledge-base/rag-knowledge-qa.md)](../../raw/application-user-guide/knowledge-base/rag-knowledge-qa.md)。

> **注意**：文档 1 中“支持的模型”列表称“第三方文本生成模型（DeepSeek-R1、DeepSeek-V3.1、abab6.5s……）”支持知识库，但文档 7 和 8 的检索/问答配置参数中仅列出 `qwen3-rerank` 等阿里云自有排序模型，未提及第三方模型作为排序器选项。实际使用中，排序模型必须选用百炼平台提供的 `qwen3-*` 系列，第三方模型仅可作为问答生成模型。

## 关键参数

| 参数类别 | 参数名 | 取值范围 | 作用说明 |
|----------|--------|----------|----------|
| **检索控制** | 相似度阈值 | 0.01–1.0 | 过滤重排后分数低于阈值的切片；值过高易漏召，过低引入噪声 [知识库 (raw/application-user-guide/knowledge-base/rag-knowledge-base.md)](../../raw/application-user-guide/knowledge-base/rag-knowledge-base.md) |
| | 初步向量/关键词 TopK | 1–100 | 控制向量/关键词检索阶段初步召回切片数；影响重排模型 [Token](../concepts/token.md) 消耗与精度 [知识检索 (raw/application-user-guide/knowledge-base/rag-knowledge-retrieval.md)](../../raw/application-user-guide/knowledge-base/rag-knowledge-retrieval.md) |
| | 最大召回数量 | 1–20 | 重排后最终返回给大模型的切片数；工作流中 `TopK` 即为此参数 [知识库 (raw/application-user-guide/knowledge-base/rag-knowledge-base.md)](../../raw/application-user-guide/knowledge-base/rag-knowledge-base.md) |
| **知识库管理** | 权重 | 数值型 | 多知识库场景下，决定同分切片的优先级；**仅同类型知识库间生效**（如文档搜索类权重不影响数据查询类） [知识库 (raw/application-user-guide/knowledge-base/rag-knowledge-base.md)](../../raw/application-user-guide/knowledge-base/rag-knowledge-base.md) |
| | Meta信息抽取 | — | 为文本切片注入元数据（如 `filename`, `date`, 正则提取值），实现结构化过滤，显著提升精准召回率 [RAG效果优化 (raw/application-user-guide/knowledge-base/rag-optimization.md)](../../raw/application-user-guide/knowledge-base/rag-optimization.md) |

## 使用方式

### 控制台集成
- **智能体应用**：在应用配置页 → “文档知识库” → 点击 `+` 添加知识库，设置相似度阈值与权重；调试时可启用标签过滤、调整召回数 [知识库 (raw/application-user-guide/knowledge-base/rag-knowledge-base.md)](../../raw/application-user-guide/knowledge-base/rag-knowledge-base.md)。
- **工作流应用**：拖入“知识库”节点 → 配置输入（如 `query`）、选择知识库（固定或动态）、设置 `TopK` → 连接大模型节点 → 在提示词中插入 `{result}` 变量引用检索结果 [知识库 (raw/application-user-guide/knowledge-base/rag-knowledge-base.md)](../../raw/application-user-guide/knowledge-base/rag-knowledge-base.md)。
- **独立服务**：通过“知识检索”或“知识问答”标签页创建服务，绑定知识库并配置全局/独立参数，发布后即可调用 [知识检索 (raw/application-user-guide/knowledge-base/rag-knowledge-retrieval.md)](../../raw/application-user-guide/knowledge-base/rag-knowledge-retrieval.md)。

### API 集成
- 使用 [阿里云百炼 SDK](https://api.aliyun.com/api-tools/sdk/bailian?version=2023-12-29&language=python-tea&tab=primer-doc) 调用知识库 API，完整流程包括：申请上传租约 → 上传文件 → 添加文件 → 创建索引 → 提交索引任务 [知识库API指南 (raw/application-user-guide/knowledge-base/rag-knowledge-base-api-guide.md)](../../raw/application-user-guide/knowledge-base/rag-knowledge-base-api-guide.md)。
- **重要限制**：API 仅支持**文档搜索类知识库**，其他类型（数据查询、图片问答等）暂无对应 API [知识库API指南 (raw/application-user-guide/knowledge-base/rag-knowledge-base-api-guide.md)](../../raw/application-user-guide/knowledge-base/rag-knowledge-base-api-guide.md)。

## 限制和注意事项

- **地域限制**：知识库功能**仅限华北2（北京）地域**，新加坡、法兰克福等国际地域不可用，此限制在文档 1 和文档 4 中均被明确强调 [知识库 (raw/application-user-guide/knowledge-base/rag-knowledge-base.md)](../../raw/application-user-guide/knowledge-base/rag-knowledge-base.md)。
- **配额约束**：
  - 单知识库文件数无硬上限（文档搜索类），但单次控制台导入上限为 50 个文件；API 批量导入无此限制 [知识库配额与限制 (raw/application-user-guide/knowledge-base/rag-knowledge-base-specifications.md)](../../raw/application-user-guide/knowledge-base/rag-knowledge-base-specifications.md)。
  - 文本切片长度上限为 6000 字符；音视频搜索类知识库**不支持新增切片**，仅支持编辑与删除 [知识库配额与限制 (raw/application-user-guide/knowledge-base/rag-knowledge-base-specifications.md)](../../raw/application-user-guide/knowledge-base/rag-knowledge-base-specifications.md)。
- **计费要点**：
  - 规格费用（标准版 0.03 元/小时，旗舰版 0.2 元/RCU/小时）与模型调用费用（向量化、重排、问答生成）**完全分离**，后者按实际 [Token](../concepts/token.md) 消耗计费 [知识库计费说明 (raw/application-user-guide/knowledge-base/billing-for-knowledge-base.md)](../../raw/application-user-guide/knowledge-base/billing-for-knowledge-base.md)。
  - 排序模型费用取决于**初步召回总切片数**，而非最终返回数；关闭排序可降低成本但降低精度 [知识库计费说明 (raw/application-user-guide/knowledge-base/billing-for-knowledge-base.md)](../../raw/application-user-guide/knowledge-base/billing-for-knowledge-base.md)。
- **效果优化关键**：
  - 元数据（Metadata）与标签（Tags）必须在知识库创建时或文件上传时配置，**创建后无法追加 Metadata 抽取规则** [知识库 (raw/application-user-guide/knowledge-base/rag-knowledge-base.md)](../../raw/application-user-guide/knowledge-base/rag-knowledge-base.md)。
  - “多轮对话改写”功能需在创建知识库时开启，**后续无法为已存在知识库启用** [RAG效果优化 (raw/application-user-guide/knowledge-base/rag-optimization.md)](../../raw/application-user-guide/knowledge-base/rag-optimization.md)。

## 来源文档

- [知识库](../../raw/application-user-guide/knowledge-base/rag-knowledge-base.md)
- [RAG效果优化](../../raw/application-user-guide/knowledge-base/rag-optimization.md)
- [知识库日志与监控](../../raw/application-user-guide/knowledge-base/rag-knowledge-base-log-monitoring.md)
- [知识库API指南](../../raw/application-user-guide/knowledge-base/rag-knowledge-base-api-guide.md)
- [知识库配额与限制](../../raw/application-user-guide/knowledge-base/rag-knowledge-base-specifications.md)
- [知识库计费说明](../../raw/application-user-guide/knowledge-base/billing-for-knowledge-base.md)
- [知识检索](../../raw/application-user-guide/knowledge-base/rag-knowledge-retrieval.md)
- [知识问答](../../raw/application-user-guide/knowledge-base/rag-knowledge-qa.md)



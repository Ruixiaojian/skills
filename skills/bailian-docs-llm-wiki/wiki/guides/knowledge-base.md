# [knowledge](../api/knowledge.md) base

知识库是阿里云百炼平台提供的 RAG（[检索增强生成](../concepts/rag.md)）核心能力，用于为大语言模型注入私有数据与领域知识，提升其在垂直场景下的回答准确性与专业性。它通过解析、向量化、检索与重排等环节，将非结构化或结构化数据转化为可被模型高效利用的语义片段。知识库功能仅在中国站华北2（北京）地域可用，且需配合支持的模型与正确配置的索引策略才能发挥最佳效果。

## 支持的模型/功能

知识库支持多种预置与自定义模型，包括千问系列（QwQ/Long/Max/Plus/Turbo/Coder/Deep-Research）、千问VL系列（Max/Plus/Flash/OCR）、开源版（Qwen3/Qwen2.5/Qwen2）及第三方模型（DeepSeek-R1、Llama3.1、Yi-Large等）[原文标题](../../raw/application-user-guide/knowledge-base/rag-knowledge-base.md)。  
功能层面覆盖**文档搜索**（支持富文本文档、视觉理解、极速问答）、**数据查询**（结构化表格）、**图片问答**（[多模态](../concepts/multimodal.md)理解）和**音视频搜索**（语音识别+帧提取+剧情解析）四类知识库类型 [原文标题](../../raw/application-user-guide/knowledge-base/rag-knowledge-base.md)。  
此外，平台提供**知识检索服务**（多知识库联合检索、混排模型统一排序）和**知识问答服务**（极速/多轮智能模式、文件预解析、拒答与防泄漏控制）两大高级能力 [原文标题](../../raw/application-user-guide/knowledge-base/rag-knowledge-retrieval.md)。

> **注意**：文档 3 中列出的“千问-QwQ/Long/Max/Plus/Turbo/Coder/Deep-Research”等模型名称与文档 7 中计费章节提及的 `qwen3.7-plus` 等存在命名不一致现象；实际开发中应以控制台创建应用时可选模型列表为准，且模型调用费用独立于知识库规格费用 [原文标题](../../raw/application-user-guide/knowledge-base/rag-knowledge-base.md)。

## 关键参数

| 参数类别 | 参数名 | 取值范围 | 说明 |
|----------|--------|----------|------|
| **索引配置** | 切片方式 | 智能切分（推荐）/固定长度 | “智能切分”基于语义自适应划分，避免语义截断，优于人工设定固定长度 [原文标题](../../raw/application-user-guide/knowledge-base/rag-optimization.md) |
| | Meta信息抽取 | 开启后不可修改 | 为文本切片附加 key-value 元数据（如 `name=百炼手机X1`），显著提升结构化检索精度；创建知识库时必须配置，后续无法追加 [原文标题](../../raw/application-user-guide/knowledge-base/rag-knowledge-base.md) |
| **检索控制** | 相似度阈值 | 0.01–1.0 | 过高导致漏召回（如设为 0.6 可能返回空结果），过低引入噪声；需结合命中测试反复调整 [原文标题](../../raw/application-user-guide/knowledge-base/rag-optimization.md) |
| | 初步向量检索 TopK | 1–100（默认 50） | 控制向量召回数量；该值直接影响 Rerank 模型费用——费用 = 初步召回总切片数 × 平均切片 [Token](../concepts/token.md) 数 × 单价 [原文标题](../../raw/application-user-guide/knowledge-base/billing-for-knowledge-base.md) |
| | 最大召回数量 | 1–20 | 排序后最终返回给大模型的切片数；增大可提升复杂问题回答完整性，但增加 [Token](../concepts/token.md) 消耗 [原文标题](../../raw/application-user-guide/knowledge-base/rag-knowledge-base.md) |

## 使用方式

### 创建与集成
1. **创建知识库**：在控制台选择标准版（0.03 元/小时）或旗舰版（0.2 元/RCU/小时），上传文件（支持 PDF/DOCX/MD/Excel/图片/音视频等格式），配置索引参数（含智能切分、Meta 抽取）[原文标题](../../raw/application-user-guide/knowledge-base/rag-knowledge-base.md)。  
2. **定时同步**：通过文件连接器配置 OSS/飞书/钉钉/语雀/SharePoint 同步规则，支持分钟级至日级周期，同步文件作为独立副本存储 [原文标题](../../raw/application-user-guide/knowledge-base/data-sync-guide.md)。  
3. **集成到应用**：  
   - **智能体应用**：在“文档知识库”节点添加知识库，设置相似度阈值与权重；  
   - **工作流应用**：拖入“知识库”节点，配置 `content` 输入（通常为 `query`）、TopK 及动态知识库变量；  
   - **外部应用**：调用 `Retrieve` API 或使用 SDK（如 Python 示例代码）实现自动化检索 [原文标题](../../raw/application-user-guide/knowledge-base/rag-knowledge-base-api-guide.md)。

### 调试与监控
- **命中测试**：在知识库详情页直接输入 Query，查看召回切片、相似度分数及来源文档，用于诊断检索效果 [原文标题](../../raw/application-user-guide/knowledge-base/rag-optimization.md)。  
- **日志监控**：开通 SLS 日志服务后，可分析 `request_id`、`latency`、`response_code`、`data.nodes[]` 等字段，定位慢查询或业务错误 [原文标题](../../raw/application-user-guide/knowledge-base/rag-knowledge-base-log-monitoring.md)。

## 限制和注意事项

- **地域限制**：知识库功能仅限华北2（北京）地域，其他地域（如新加坡、法兰克福）不可用 [原文标题](../../raw/application-user-guide/knowledge-base/rag-knowledge-base.md)。  
- **配额限制**：标准版知识库免费存储上限 100 GB，旗舰版 9,999 GB；单次控制台导入文件数 ≤50；单个文本切片长度 ≤6,000 字符；音视频搜索类知识库不支持新增切片 [原文标题](../../raw/application-user-guide/knowledge-base/rag-knowledge-base-specifications.md)。  
- **计费关键点**：  
  - 规格费用按小时计费（标准版固定 1 QPS，旗舰版按 RCU 可调）；  
  - **模型费用独立计费**：Query 向量化、Rerank 排序（费用取决于初步召回切片总数，非最终返回数）、问答生成均按 [Token](../concepts/token.md) 计费；多知识库场景下费用线性叠加 [原文标题](../../raw/application-user-guide/knowledge-base/billing-for-knowledge-base.md)。  
- **配置不可逆项**：知识库类型、Meta 信息抽取配置、多轮对话改写开关（创建时启用，后续无法开启）均不可修改，需谨慎设置 [原文标题](../../raw/application-user-guide/knowledge-base/rag-optimization.md)。

## 来源文档

- [RAG效果优化](../../raw/application-user-guide/knowledge-base/rag-optimization.md)
- [知识库定时数据同步指南](../../raw/application-user-guide/knowledge-base/data-sync-guide.md)
- [知识库](../../raw/application-user-guide/knowledge-base/rag-knowledge-base.md)
- [知识库日志与监控](../../raw/application-user-guide/knowledge-base/rag-knowledge-base-log-monitoring.md)
- [知识库API指南](../../raw/application-user-guide/knowledge-base/rag-knowledge-base-api-guide.md)
- [知识库配额与限制](../../raw/application-user-guide/knowledge-base/rag-knowledge-base-specifications.md)
- [知识库计费说明](../../raw/application-user-guide/knowledge-base/billing-for-knowledge-base.md)
- [知识检索](../../raw/application-user-guide/knowledge-base/rag-knowledge-retrieval.md)
- [知识问答](../../raw/application-user-guide/knowledge-base/rag-knowledge-qa.md)



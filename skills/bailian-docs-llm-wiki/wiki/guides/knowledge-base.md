# [knowledge](../api/knowledge.md) base

知识库是阿里云百炼平台基于 RAG（[检索增强生成](../concepts/rag.md)）技术构建的核心能力，用于为大语言模型注入私有数据与领域知识，提升其在特定业务场景下的回答准确性与专业性。它支持文档、表格、音视频、图片等[多模态](../concepts/multi-modal.md)数据的解析、切片、向量化与语义检索，并可灵活集成至智能体、工作流及外部应用中。知识库功能仅在中国站华北2（北京）地域可用。

## 支持的模型/功能

知识库支持预置与自定义两类模型：预置模型包括千问系列（QwQ/Long/Max/Plus/Turbo/Coder/Deep-Research、VL-Max/Plus/Flash/OCR、开源版 Qwen3/Qwen2.5/Qwen2 等）及第三方模型（DeepSeek-R1、Llama3.1、Yi-Large 等）；自定义模型指在百炼平台调优后的千问 Plus/Turbo、VL-Max/Plus 或开源版本 [知识库](../../raw/application-user-guide/knowledge-base/rag-knowledge-base.md)。所有支持模型均需在华北2（北京）地域部署方可使用。

知识库提供三大核心服务形态：
- **知识检索**：支持单库或多库（最多 15 个）联合检索，具备 Query 改写、混合检索（向量+关键词）、Rerank 排序及精细化参数配置能力 [知识检索](../../raw/application-user-guide/knowledge-base/rag-knowledge-retrieval.md)；
- **知识问答**：在检索基础上叠加大模型生成，支持极速模式（单轮）与多轮智能模式（Agentic 规划），并提供拒答、防泄漏、引用溯源、[多模态](../concepts/multi-modal.md)回复等生成控制能力 [知识问答](../../raw/application-user-guide/knowledge-base/rag-knowledge-qa.md)；
- **定时数据同步**：通过文件连接器自动从 OSS、飞书、钉钉、语雀、SharePoint 等外部源按分钟/小时/天周期同步增量内容，确保知识新鲜度 [知识库定时数据同步指南](../../raw/application-user-guide/knowledge-base/data-sync-guide.md)。

> **注意**：文档 3 明确指出“知识库功能仅能在中国站华北2（北京）地域开通和使用”，而文档 6 和文档 7 的“重要”声明重复强调此限制，但文档 4（日志监控）未提及地域约束。实际部署时必须严格遵循地域要求，否则 API 调用或控制台操作将失败。

## 关键参数

| 参数类别 | 参数名 | 取值范围/说明 | 作用 |
|----------|--------|----------------|------|
| **索引配置** | 切片方式 | 智能切分（推荐）、固定长度 | 影响语义完整性，智能切分基于段落语义自适应划分，避免截断 [RAG效果优化](../../raw/application-user-guide/knowledge-base/rag-optimization.md) |
| | Meta信息抽取 | 创建知识库时配置，不可后续修改 | 为文本切片附加 `filename`、`date` 等 key-value 元数据，用于结构化过滤，显著提升召回精度 |
| | 向量模型 | `text-embedding-v4/v3`（文本类）、`qwen3-vl-embedding`（[多模态](../concepts/multi-modal.md)） | 决定向量维度（512/1024）及语义表征能力，不可更改 |
| **检索控制** | 相似度阈值 | 0.01–1.0 | 过滤排序后低分切片；设过高易漏召，设过低引入噪声 |
| | 初步向量 TopK | 1–100（默认 50） | 控制向量检索阶段召回数量，直接影响 Rerank 模型费用（费用 = 召回数 × 平均切片 [Token](../concepts/token.md) × 单价） |
| | 最大召回数量 | 1–20 | 最终返回给大模型的切片数，影响 [Token](../concepts/token.md) 消耗与回答质量 |
| | 标签过滤 | 单文件最多 32 个标签 | 在检索前按标签筛选文件，适用于多类别知识隔离场景 |

## 使用方式

### 创建与配置
1. **创建知识库**：进入控制台 [知识库](https://bailian.console.aliyun.com/?tab=app#/knowledge-base) 页面，选择标准版（0.03 元/小时）或旗舰版（0.2 元/RCU/小时），指定类型（如文档搜索 → 视觉理解/极速问答）并上传文件或配置数据连接器；
2. **配置同步**：若需自动更新，需先在 [数据连接](https://bailian.console.aliyun.com/cn-beijing/?tab=app#/connector/list) 中创建对应连接器（OSS/飞书等），再于文件管理页点击“同步数据规则”创建定时任务 [知识库定时数据同步指南](../../raw/application-user-guide/knowledge-base/data-sync-guide.md)；
3. **集成应用**：
   - *智能体应用*：在应用配置页添加“文档知识库”节点，设置相似度阈值与权重；
   - *工作流应用*：拖入“知识库”节点，配置 `content` 输入（通常为 `query`）、TopK 及知识库选择方式（固定或动态）；
   - *外部应用*：使用百炼 SDK 调用 `Retrieve`、`CreateIndex` 等 API，需子账号授权 `AliyunBailianDataFullAccess` 策略 [知识库API指南](../../raw/application-user-guide/knowledge-base/rag-knowledge-base-api-guide.md)。

### 调试与监控
- **效果调试**：使用控制台“命中测试”验证召回质量，结合 [RAG效果优化](../../raw/application-user-guide/knowledge-base/rag-optimization.md) 文档中的评测集构建、元数据配置、切片修正等方法迭代改进；
- **日志监控**：开通 SLS 日志服务后，可查询 `request_id`、`latency`、`response_code` 及 `response_body.data.nodes[]` 中的召回切片与分数，用于审计与问题排查 [知识库日志与监控](../../raw/application-user-guide/knowledge-base/rag-knowledge-base-log-monitoring.md)。

## 限制和注意事项

- **地域与配额**：知识库仅限华北2（北京），且受硬性配额约束——单账号最多 100 个 RDS 数据源知识库、标准版存储上限 100 GB、旗舰版 9,999 GB；单知识库无文件数量硬限，但业务空间总文件数上限 100,000 [知识库配额与限制](../../raw/application-user-guide/knowledge-base/rag-knowledge-base-specifications.md)；
- **文件格式与大小**：文档搜索类支持 PDF/DOCX（≤150 MB，≤1000 页）、TXT/MD（≤10 MB）；音视频类支持 MP4/MP3 等（≤512 MB）；表格类 Excel 需避免合并单元格与首行备注 [知识库配额与限制](../../raw/application-user-guide/knowledge-base/rag-knowledge-base-specifications.md)；
- **计费关键点**：
  - 规格费用按小时计费（标准版 0.03 元/小时，旗舰版按 RCU 计费）；
  - **模型费用独立计费**：向量模型按输入 [Token](../concepts/token.md) 计费；Rerank 费用取决于初步召回切片总数（非最终返回数），多知识库绑定时费用线性叠加；
  - 免费额度（720 小时）仅抵扣标准版规格费，不覆盖模型调用 [知识库计费说明](../../raw/application-user-guide/knowledge-base/billing-for-knowledge-base.md)；
- **同步与删除行为**：同步规则创建后，源文件删除不影响百炼平台副本，需手动删除；同步文件作为独立副本存储，与原始数据无关联 [知识库定时数据同步指南](../../raw/application-user-guide/knowledge-base/data-sync-guide.md)。

## 来源文档

- [知识库定时数据同步指南](../../raw/application-user-guide/knowledge-base/data-sync-guide.md)
- [RAG效果优化](../../raw/application-user-guide/knowledge-base/rag-optimization.md)
- [知识库](../../raw/application-user-guide/knowledge-base/rag-knowledge-base.md)
- [知识库日志与监控](../../raw/application-user-guide/knowledge-base/rag-knowledge-base-log-monitoring.md)
- [知识库配额与限制](../../raw/application-user-guide/knowledge-base/rag-knowledge-base-specifications.md)
- [知识库API指南](../../raw/application-user-guide/knowledge-base/rag-knowledge-base-api-guide.md)
- [知识库计费说明](../../raw/application-user-guide/knowledge-base/billing-for-knowledge-base.md)
- [知识检索](../../raw/application-user-guide/knowledge-base/rag-knowledge-retrieval.md)
- [知识问答](../../raw/application-user-guide/knowledge-base/rag-knowledge-qa.md)



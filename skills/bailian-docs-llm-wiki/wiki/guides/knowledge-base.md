# [knowledge](../api/knowledge.md) base

知识库是阿里云百炼平台提供的 RAG（[检索增强生成](../concepts/rag.md)）核心能力，用于为大语言模型注入私有、结构化或非结构化数据，从而提升其在垂直领域回答的准确性与时效性。它支持文档、表格、图片、音视频等多种数据源，并通过向量化、语义检索、重排序与大模型生成的完整流水线实现端到端知识增强。该功能**仅在中国站华北2（北京）地域可用**，其他地域（如新加坡、德国法兰克福）暂不支持 [知识库 (raw/application-user-guide/knowledge-base/rag-knowledge-base.md)](../../raw/application-user-guide/knowledge-base/rag-knowledge-base.md)。

## 支持的模型/功能

- **支持的模型类型**：  
  - 预置模型：千问全系（QwQ/Long/Max/Plus/Turbo/Coder/Deep-Research、VL-Max/Plus/Flash/OCR、Qwen3/Qwen2.5/Qwen2等）；  
  - 第三方模型：DeepSeek-R1、DeepSeek-V3.1、abab6.5s、Llama3.1、Yi-Large 等；  
  - 自定义模型：基于上述基座模型调优后的版本（需在[模型训练](https://help.aliyun.com/zh/model-studio/model-training-overview)中完成）[知识库 (raw/application-user-guide/knowledge-base/rag-knowledge-base.md)](../../raw/application-user-guide/knowledge-base/rag-knowledge-base.md)。  
  > **注意**：文档1中列出的“千问-Plus/Turbo”等重复项属冗余描述，实际以控制台应用创建页可选模型为准；且“千问VL-Max/Plus”在文档6中明确对应[多模态](../concepts/multimodal.md)向量模型 `qwen3-vl-embedding`，而文档1未说明此绑定关系，存在隐含不一致。

- **核心功能能力**：  
  - 多知识库联合检索（最多 15 个）与问答；  
  - [多模态](../concepts/multimodal.md)支持：文本、富文本文档（PDF/DOCX）、图片（含视觉理解）、音视频（语音识别+帧提取+剧情解析）；  
  - 检索服务（独立于应用）与问答服务（集成生成）双模式；  
  - 动态标签过滤、元数据（metadata）结构化检索、多轮对话 Query 改写；  
  - 文件预解析（调试时上传即用）、图文并茂回复、引用溯源、拒答与防泄漏策略 [知识问答 (raw/application-user-guide/knowledge-base/rag-knowledge-qa.md)](../../raw/application-user-guide/knowledge-base/rag-knowledge-qa.md)。

## 关键参数

| 参数类别 | 参数名 | 取值范围 | 说明 |
|----------|--------|----------|------|
| **检索控制** | 相似度阈值 | 0.01–1.0 | 过滤重排后得分低于该值的切片；值过高易漏召，过低引入噪声 [知识检索 (raw/application-user-guide/knowledge-base/rag-knowledge-retrieval.md)](../../raw/application-user-guide/knowledge-base/rag-knowledge-retrieval.md)。 |
| | 初步向量检索 TopK | 1–100（默认 50） | 向量召回阶段返回的切片数，直接影响 Rerank 费用（费用 = 初步召回总数 × 平均切片 [Token](../concepts/token.md) 数 × 单价）[知识库计费说明 (raw/application-user-guide/knowledge-base/billing-for-knowledge-base.md)](../../raw/application-user-guide/knowledge-base/billing-for-knowledge-base.md)。 |
| | 最大召回数量 | 1–20 | 重排后最终返回给大模型的切片数（单知识库上限为 20）[知识库配额与限制 (raw/application-user-guide/knowledge-base/rag-knowledge-base-specifications.md)](../../raw/application-user-guide/knowledge-base/rag-knowledge-base-specifications.md)。 |
| **性能与规格** | RCU（旗舰版） | 1–200 | 1 RCU ≈ 支撑 50 QPS 检索并发；RCU 数 = ⌈峰值 QPS ÷ 50⌉；标准版固定 1 QPS [知识库计费说明 (raw/application-user-guide/knowledge-base/billing-for-knowledge-base.md)](../../raw/application-user-guide/knowledge-base/billing-for-knowledge-base.md)。 |
| **数据处理** | 文本切片长度 | ≤ 6000 字符 | 单切片最大 [Token](../concepts/token.md) 容量；超长内容将被截断 [知识库配额与限制 (raw/application-user-guide/knowledge-base/rag-knowledge-base-specifications.md)](../../raw/application-user-guide/knowledge-base/rag-knowledge-base-specifications.md)。 |

## 使用方式

- **控制台快速集成**：  
  1. 在[知识库页面](https://bailian.console.aliyun.com/?tab=app#/knowledge-base)创建标准版/旗舰版知识库，选择「文档搜索」等类型并上传文件（支持本地/OSS）；  
  2. 在智能体或工作流应用配置中，通过「+ 文档知识库」按钮关联；工作流需拖入「知识库节点」并配置 `query` 输入变量与 `TopK`；  
  3. 对于外部系统，使用[百炼 SDK](https://api.aliyun.com/api-tools/sdk/bailian?version=2023-12-29&language=python-tea&tab=primer-doc)调用 `Retrieve` 或 `QA` 接口 [知识库API指南 (raw/application-user-guide/knowledge-base/rag-knowledge-base-api-guide.md)](../../raw/application-user-guide/knowledge-base/rag-knowledge-base-api-guide.md)。

- **自动化同步**：  
  通过「数据连接器」配置定时同步规则（OSS/飞书/钉钉/语雀/SharePoint），支持分钟级至日级增量同步，文件作为独立副本存储 [知识库定时数据同步指南 (raw/application-user-guide/knowledge-base/data-sync-guide.md)](../../raw/application-user-guide/knowledge-base/data-sync-guide.md)。

- **效果优化路径**：  
  建立评测集 → 执行自动评测 → 根据失败用例诊断（检索无效/不相关/切片不完整/重排不佳）→ 对应调整：补充知识、启用元数据/标签、切换「智能切分」、调低相似度阈值或增大 TopK [RAG效果优化 (raw/application-user-guide/knowledge-base/rag-optimization.md)](../../raw/application-user-guide/knowledge-base/rag-optimization.md)。

## 限制和注意事项

- **地域与权限限制**：  
  知识库功能**仅限华北2（北京）地域**，其他地域不可用；子账号需授予 `AliyunBailianDataFullAccess` 策略并加入业务空间方可调用 API [知识库API指南 (raw/application-user-guide/knowledge-base/rag-knowledge-base-api-guide.md)](../../raw/application-user-guide/knowledge-base/rag-knowledge-base-api-guide.md)。

- **配额硬性约束**：  
  - 单知识库文件数无硬上限（非结构化），但业务空间总文件数上限为 100,000；  
  - 单次控制台导入最多 50 个文件（API 无此限制）；  
  - 音视频搜索类知识库**不支持新增切片**，仅支持编辑与删除 [知识库配额与限制 (raw/application-user-guide/knowledge-base/rag-knowledge-base-specifications.md)](../../raw/application-user-guide/knowledge-base/rag-knowledge-base-specifications.md)。

- **计费关键点**：  
  - 规格费用（按小时）与模型调用费用（按 [Token](../concepts/token.md)）**完全分离**；后者包含向量模型（`text-embedding-v4`/`qwen3-vl-embedding`）、排序模型（`qwen3-rerank`/`qwen3-vl-rerank`）、路由模型（`qwen-plus`）及问答模型调用；  
  - Rerank 费用取决于**初步召回总切片数**，而非最终返回数；挂载 N 个知识库时，Query 向量化与 Rerank 费用均 ×N；  
  - 免费额度（720 小时）**仅抵扣标准版规格费用**，不覆盖任何模型调用 [知识库计费说明 (raw/application-user-guide/knowledge-base/billing-for-knowledge-base.md)](../../raw/application-user-guide/knowledge-base/billing-for-knowledge-base.md)。

- **运维与可观测性**：  
  开通日志服务（SLS）后，所有检索请求投递至 `bailian-rag-retrieve-log` LogStore，字段含 `pipeline_id`（知识库 ID）、`latency`、`response_code`、`data.nodes[]`（召回切片及 score）等，可用于审计、慢查询分析与错误定位 [知识库日志与监控 (raw/application-user-guide/knowledge-base/rag-knowledge-base-log-monitoring.md)](../../raw/application-user-guide/knowledge-base/rag-knowledge-base-log-monitoring.md)。

## 来源文档

- [知识库](../../raw/application-user-guide/knowledge-base/rag-knowledge-base.md)
- [RAG效果优化](../../raw/application-user-guide/knowledge-base/rag-optimization.md)
- [知识库定时数据同步指南](../../raw/application-user-guide/knowledge-base/data-sync-guide.md)
- [知识库日志与监控](../../raw/application-user-guide/knowledge-base/rag-knowledge-base-log-monitoring.md)
- [知识库API指南](../../raw/application-user-guide/knowledge-base/rag-knowledge-base-api-guide.md)
- [知识库计费说明](../../raw/application-user-guide/knowledge-base/billing-for-knowledge-base.md)
- [知识库配额与限制](../../raw/application-user-guide/knowledge-base/rag-knowledge-base-specifications.md)
- [知识检索](../../raw/application-user-guide/knowledge-base/rag-knowledge-retrieval.md)
- [知识问答](../../raw/application-user-guide/knowledge-base/rag-knowledge-qa.md)



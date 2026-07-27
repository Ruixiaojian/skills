# [knowledge](../api/knowledge.md) base

知识库是阿里云百炼平台提供的 RAG（[检索增强生成](../concepts/rag.md)）核心能力，用于为大模型注入私有数据与领域知识，提升回答的准确性与专业性。其本质是将非结构化/半结构化数据（文档、表格、图片、音视频等）解析、切片、向量化后构建可语义检索的索引，并在推理时动态召回相关片段供大模型参考。该功能**仅在中国站华北2（北京）地域可用**，其他地域（如新加坡、德国法兰克福）不支持 [知识库 (raw/application-user-guide/knowledge-base/rag-knowledge-base.md)](../../raw/application-user-guide/knowledge-base/rag-knowledge-base.md)。

## 支持的模型/功能

- **支持的模型类型**：  
  - 预置模型：千问全系列（QwQ/Long/Max/Plus/Turbo/Coder/Deep-Research、VL-Max/Plus/Flash/OCR、Qwen3/Qwen2.5/Qwen2 等）；  
  - 第三方模型：DeepSeek-R1、DeepSeek-V3.1、abab6.5s、Llama3.1、Yi-Large 等；  
  - 自定义模型：基于上述基座模型调优后的版本（需在百炼 Model Studio 中完成训练）[知识库 (raw/application-user-guide/knowledge-base/rag-knowledge-base.md)](../../raw/application-user-guide/knowledge-base/rag-knowledge-base.md)。  
  > **注意**：文档1中列出的“千问-开源版”与文档7中问答服务实际可选模型（如 `qwen3.6-plus`、`qwen3.7-plus`）存在命名粒度差异，开发时请以控制台创建应用时下拉菜单中实时可选的模型为准，避免硬编码过时别名。

- **核心功能场景**：  
  - **文档搜索**：支持 PDF/DOCX/PPTX/TXT/Markdown/HTML/XLSX 等格式，含视觉理解（富文本文档）、极速问答等子模式；  
  - **数据查询**：结构化数据（Excel/CSV），支持 NL2SQL；  
  - **图片问答**：支持 PNG/JPG/BMP/GIF，结合多模态向量模型理解图文；  
  - **音视频搜索**：支持 MP3/MP4/AVI 等格式，含语音识别、帧提取与剧情解析；  
  - **知识检索服务**：多知识库联合检索（最多 15 个），支持 Query 改写、混合检索（向量+关键词）、Rerank 排序；  
  - **知识问答服务**：绑定知识库后自动生成自然语言回答，支持极速模式（单轮）与多轮智能模式（Agentic 规划）[知识问答 (raw/application-user-guide/knowledge-base/rag-knowledge-qa.md)](../../raw/application-user-guide/knowledge-base/rag-knowledge-qa.md)。

## 关键参数

| 参数类别 | 参数名 | 取值范围 | 说明 |
|----------|--------|----------|------|
| **检索控制** | 相似度阈值 | 0.01–1.0 | 过滤排序后分数低于该值的切片；值过高易漏召，过低引入噪声。默认值通常为 `0.3`–`0.4`，需通过[命中测试](https://help.aliyun.com/zh/model-studio/rag-knowledge-base#81f57beb71zs1)调优 [RAG效果优化 (raw/application-user-guide/knowledge-base/rag-optimization.md)](../../raw/application-user-guide/knowledge-base/rag-optimization.md)。 |
| | 初步向量检索 TopK | 1–100 | 向量阶段初步召回切片数（默认 50）；直接影响 Rerank 模型 [Token](../concepts/token.md) 消耗与延迟。 |
| | 初步关键词检索 TopK | 1–100 | 关键词匹配阶段初步召回切片数（默认 50）；与向量 TopK 共同决定 Rerank 输入总量。 |
| | 最大召回数量 | 1–20 | 最终返回给大模型的切片总数（经 Rerank 后截取）。 |
| **元数据与过滤** | Meta信息抽取 | — | 创建知识库时配置，支持常量、变量（`file_name`/`cat_name`）、大模型提取、正则、关键词搜索五种方式；启用后可在 API 请求中通过 `metadata_filter` 精准筛选 [知识库 (raw/application-user-guide/knowledge-base/rag-knowledge-base.md)](../../raw/application-user-guide/knowledge-base/rag-knowledge-base.md)。 |
| | 标签过滤 | 单文件 ≤32 个标签 | 上传文件时或数据管理页设置，API 调用时通过 `tags` 参数生效，用于粗粒度文件筛选。 |
| **性能与规格** | 并发能力（旗舰版） | 50–10,000 QPS（对应 1–200 RCU） | RCU（Retrieval Compute Unit）为计量单位，1 RCU ≈ 50 QPS；标准版固定为 1 QPS。 |

## 使用方式

- **控制台集成**：  
  - **智能体应用**：在应用配置页 → “文档知识库” → 点击 `+` 添加知识库，可设置相似度阈值、权重（仅同类型知识库间生效）；调试时可通过“召回策略”页签配置标签过滤、TopK 等 [知识库 (raw/application-user-guide/knowledge-base/rag-knowledge-base.md)](../../raw/application-user-guide/knowledge-base/rag-knowledge-base.md)。  
  - **工作流应用**：拖入“知识库”节点，配置输入（如 `query`）、知识库选择方式（固定/动态）、TopK；下游大模型节点提示词中通过 `{result}` 插入检索结果。  
  - **独立服务**：通过“知识检索”或“知识问答”标签页创建服务，支持多库绑定、混排模型、路由开关等高级配置 [知识检索 (raw/application-user-guide/knowledge-base/rag-knowledge-retrieval.md)](../../raw/application-user-guide/knowledge-base/rag-knowledge-retrieval.md)。

- **API 集成**：  
  - 仅支持**文档搜索类知识库**（其他类型暂未开放 API）[知识库API指南 (raw/application-user-guide/knowledge-base/rag-knowledge-base-api-guide.md)](../../raw/application-user-guide/knowledge-base/rag-knowledge-base-api-guide.md)；  
  - 前置条件：子账号需授予 `AliyunBailianDataFullAccess` 权限并加入业务空间；  
  - 关键流程：申请上传租约 → 上传文件 → 添加文件 → 创建索引 → 提交索引任务 → 等待完成；  
  - 检索调用：使用 `/api/v1/indices/rag/index/retrieve` 接口，请求体需包含 `index_id`、`query`、`top_k` 及可选 `metadata_filter`/`tags`。

- **日志监控**：  
  - 开通后所有检索日志投递至 SLS，关键字段包括 `pipeline_id`（知识库 ID）、`latency`（毫秒）、`response_code`（业务码）、`response_body.data.nodes[]`（召回切片及 `score`/`text`/`metadata`）；  
  - 建议搭建仪表盘监控“调用量趋势”、“TopN 知识库排名”，并设置 `response_code != Success` 的告警 [知识库日志与监控 (raw/application-user-guide/knowledge-base/rag-knowledge-base-log-monitoring.md)](../../raw/application-user-guide/knowledge-base/rag-knowledge-base-log-monitoring.md)。

## 限制和注意事项

- **地域限制**：知识库功能**仅限华北2（北京）地域**，新加坡、法兰克福等国际地域不可用，且控制台 URL 必须包含 `cn-beijing` [知识库 (raw/application-user-guide/knowledge-base/rag-knowledge-base.md)](../../raw/application-user-guide/knowledge-base/rag-knowledge-base.md)。  
- **配额硬限制**：  
  - 单知识库文件数无硬上限（非结构化），但单次控制台导入 ≤50 个；  
  - 文本切片长度上限 6000 字符；音视频搜索类知识库**不支持新增切片**（仅支持编辑/删除）；  
  - ADB-PG 向量存储单表最大 10,000,000 行，单行 ≤100 KB [知识库配额与限制 (raw/application-user-guide/knowledge-base/rag-knowledge-base-specifications.md)](../../raw/application-user-guide/knowledge-base/rag-knowledge-base-specifications.md)。  
- **计费关键点**：  
  - 规格费用按小时出账（标准版 0.03 元/小时，旗舰版 0.2 元/RCU/小时）；  
  - **模型费用独立计费**：Query 向量化、Rerank 排序（费用 = 初步召回总切片数 × 平均切片 [Token](../concepts/token.md) 数 × 单价）、知识库路由（qwen-plus）、问答生成模型均按 [Token](../concepts/token.md) 用量结算，不包含在规格费中 [知识库计费说明 (raw/application-user-guide/knowledge-base/billing-for-knowledge-base.md)](../../raw/application-user-guide/knowledge-base/billing-for-knowledge-base.md)；  
  - **Rerank 费用陷阱**：费用取决于“初步召回总切片数”（向量 TopK + 关键词 TopK），而非最终返回数，调低 TopK 是最直接的成本优化手段。  
- **配置不可变性**：知识库创建后，**类型、Meta信息抽取配置、多轮对话改写开关均不可修改**，需重建知识库 [RAG效果优化 (raw/application-user-guide/knowledge-base/rag-optimization.md)](../../raw/application-user-guide/knowledge-base/rag-optimization.md)。

## 来源文档

- [知识库](../../raw/application-user-guide/knowledge-base/rag-knowledge-base.md)
- [RAG效果优化](../../raw/application-user-guide/knowledge-base/rag-optimization.md)
- [知识库日志与监控](../../raw/application-user-guide/knowledge-base/rag-knowledge-base-log-monitoring.md)
- [知识库API指南](../../raw/application-user-guide/knowledge-base/rag-knowledge-base-api-guide.md)
- [知识库配额与限制](../../raw/application-user-guide/knowledge-base/rag-knowledge-base-specifications.md)
- [知识检索](../../raw/application-user-guide/knowledge-base/rag-knowledge-retrieval.md)
- [知识问答](../../raw/application-user-guide/knowledge-base/rag-knowledge-qa.md)
- [知识库计费说明](../../raw/application-user-guide/knowledge-base/billing-for-knowledge-base.md)



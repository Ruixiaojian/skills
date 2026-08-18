# [knowledge](../api/knowledge.md) base

知识库是阿里云百炼平台提供的 RAG（[检索增强生成](../concepts/rag.md)）核心能力，用于为大模型注入私有数据与领域知识，提升回答的准确性与专业性。其工作流程涵盖知识导入、语义索引、多路检索、重排精筛及大模型生成，支持文档、表格、图片、音视频等多模态数据源。知识库功能仅在中国站华北2（北京）地域可用，国际站仅支持新加坡地域 [知识库 (raw/application-user-guide/knowledge-base/rag-knowledge-base.md)](../../raw/application-user-guide/knowledge-base/rag-knowledge-base.md)。

## 支持的模型/功能

- **支持的模型类型**：  
  - 预置模型：千问全系（QwQ/Long/Max/Plus/Turbo/Coder/Deep-Research、VL-Max/Plus/Flash/OCR、Qwen3/Qwen2.5/Qwen2 等）；  
  - 第三方模型：DeepSeek-R1、DeepSeek-V3.1、abab6.5s、Llama3.1、Yi-Large 等；  
  - 自定义调优模型（基于上述基座模型微调）[知识库 (raw/application-user-guide/knowledge-base/rag-knowledge-base.md)](../../raw/application-user-guide/knowledge-base/rag-knowledge-base.md)。  
  > **注意**：文档1中“支持的模型”列表与文档7中问答服务实际可选模型（如 `qwen3.6-plus`、`qwen3.7-plus`）存在粒度差异，且文档7明确限定知识问答服务仅支持部分最新版本模型。开发者应以控制台创建应用时实时下拉菜单为准，而非静态列表。

- **核心功能模块**：  
  - **知识检索服务**：支持单/多知识库联合检索（最多15个），提供 Query 改写、混合检索（向量+关键词）、Rerank 排序、标签/元数据过滤；  
  - **知识问答服务**：绑定知识库后自动生成自然语言回答，支持极速模式（单轮检索+生成）与多轮智能模式（Agentic 规划搜索）；  
  - **定时数据同步**：通过 OSS、飞书、钉钉、语雀、SharePoint 等连接器自动同步外部数据，支持分钟级至日级同步周期 [知识库定时数据同步指南 (raw/application-user-guide/knowledge-base/data-sync-guide.md)](../../raw/application-user-guide/knowledge-base/data-sync-guide.md)；  
  - **多模态能力**：视觉理解（富文本文档版面保留）、图片问答、音视频内容检索与剧情解析。

## 关键参数

| 参数类别 | 参数名 | 取值范围 | 说明 |
|----------|--------|----------|------|
| **检索控制** | 相似度阈值 | 0.01–1.0 | 过滤 Rerank 后低分切片；值过高易漏召回，过低引入噪声；建议通过[命中测试](https://help.aliyun.com/zh/model-studio/rag-knowledge-base#81f57beb71zs1)调优 [RAG效果优化 (raw/application-user-guide/knowledge-base/rag-optimization.md)](../../raw/application-user-guide/knowledge-base/rag-optimization.md)。 |
| | 最大召回数量 | 1–20 | 混排后最终返回给大模型的切片总数（全局或单库独立配置）。 |
| | 初步向量/关键词 TopK | 1–100 | 向量/关键词阶段初步召回数，直接影响 Rerank 费用（费用 = 初步召回总数 × 平均切片 Token 数 × 单价）[知识库计费说明 (raw/application-user-guide/knowledge-base/billing-for-knowledge-base.md)](../../raw/application-user-guide/knowledge-base/billing-for-knowledge-base.md)。 |
| **知识库配置** | 多轮对话改写 | 开/关 | 创建知识库时启用，不可事后修改；用于补全历史上下文，提升多轮检索准确率。 |
| | Meta信息抽取 | 自定义键值对 | 创建时配置，不可追加；用于结构化过滤（如 `name=百炼手机X1`），显著提升跨相似文档场景的召回精度。 |
| | 标签过滤 | 用户定义字符串 | 支持上传时或管理页编辑；可在 API 请求 `tags` 参数或调试界面中指定，实现轻量级文件分组检索。 |

## 使用方式

- **控制台集成**：  
  - **智能体应用**：在应用配置页 → 文档知识库 → `+` 添加知识库，设置相似度阈值与权重（权重仅同类型知识库间生效）；  
  - **工作流应用**：拖入「知识库」节点，配置输入变量（如 `query`）、选择知识库（固定或动态）、设置 TopK，再连接大模型节点并引用 `{result}` 变量；  
  - **知识检索/问答服务**：独立创建服务，绑定多个知识库，配置混排模型、路由策略、生成控制（拒答/防泄漏/引用）等。

- **API 集成**：  
  - 仅支持**文档搜索类知识库**（见文档8明确声明）；  
  - 需子账号具备 `AliyunBailianDataFullAccess` 权限并加入业务空间；  
  - 典型流程：申请上传租约 → 上传文件 → 添加文件到类目 → 创建索引 → 提交索引任务 → 等待完成 [知识库API指南 (raw/application-user-guide/knowledge-base/rag-knowledge-base-api-guide.md)](../../raw/application-user-guide/knowledge-base/rag-knowledge-base-api-guide.md)；  
  - 检索调用需传入 `pipeline_id`（知识库ID）、`query` 及可选 `metadata_filter` / `tags`。

- **外部应用接入**：  
  - 通过百炼 SDK 调用 `retrieve` 接口获取检索结果，自行拼接 Prompt 后送入任意大模型；  
  - 或直接调用知识问答服务 API，端到端获取生成答案（含引用溯源）。

## 限制和注意事项

- **地域限制**：知识库功能仅在中国站**华北2（北京）**地域开通；国际站仅支持**新加坡**地域。文档1与文档8对此表述不一致（文档1称国际站不支持，文档8称新加坡支持），以文档8为准 [知识库API指南 (raw/application-user-guide/knowledge-base/rag-knowledge-base-api-guide.md)](../../raw/application-user-guide/knowledge-base/rag-knowledge-base-api-guide.md)。  
- **配额硬限**：  
  - 单知识库文件数无硬限（非结构化），但单业务空间文件上限 100,000；  
  - 单次控制台导入 ≤ 50 文件；API 无此限制；  
  - 单文本切片长度 ≤ 6,000 字符；  
  - ADB-PG 向量存储单表 ≤ 10,000,000 行，单行 ≤ 100 KB。  
- **关键不可变项**：知识库类型（文档搜索/数据查询等）、Meta信息抽取配置、多轮对话改写开关，均**创建后不可修改**，需重建知识库。  
- **计费要点**：  
  - 规格费用按小时出账（标准版 0.03 元/小时，旗舰版 0.2 元/RCU/小时）；  
  - **模型调用费用独立计费**：Query 向量化、Rerank 排序、路由判断、问答生成均按 Token 计费，且多知识库场景费用线性叠加；  
  - 免费额度（720 小时）**仅抵扣标准版规格费**，不覆盖任何模型调用费用。  
- **同步行为**：同步规则导入的文件为**独立副本**，源文件删除不影响百炼内数据；需手动删除已同步文件。

## 来源文档

- [知识库](../../raw/application-user-guide/knowledge-base/rag-knowledge-base.md)
- [知识库定时数据同步指南](../../raw/application-user-guide/knowledge-base/data-sync-guide.md)
- [RAG效果优化](../../raw/application-user-guide/knowledge-base/rag-optimization.md)
- [知识库日志与监控](../../raw/application-user-guide/knowledge-base/rag-knowledge-base-log-monitoring.md)
- [知识库配额与限制](../../raw/application-user-guide/knowledge-base/rag-knowledge-base-specifications.md)
- [知识检索](../../raw/application-user-guide/knowledge-base/rag-knowledge-retrieval.md)
- [知识问答](../../raw/application-user-guide/knowledge-base/rag-knowledge-qa.md)
- [知识库API指南](../../raw/application-user-guide/knowledge-base/rag-knowledge-base-api-guide.md)
- [知识库计费说明](../../raw/application-user-guide/knowledge-base/billing-for-knowledge-base.md)



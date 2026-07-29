# [knowledge](../api/knowledge.md) base

知识库是阿里云百炼平台提供的 RAG（[检索增强生成](../concepts/rag.md)）核心能力，用于为大语言模型注入私有、结构化或非结构化数据，提升其在垂直领域问答的准确性与时效性。它支持文档、表格、图片、音视频等多模态数据源，并通过向量化、语义检索、重排与生成协同工作。知识库功能**仅在中国站华北2（北京）地域可用**，其他地域（如新加坡、法兰克福）暂不支持 [知识库 (raw/application-user-guide/knowledge-base/rag-knowledge-base.md)](../../raw/application-user-guide/knowledge-base/rag-knowledge-base.md)。

## 支持的模型/功能

- **支持的模型类型**：  
  - 预置模型：千问系列（QwQ/Long/Max/Plus/Turbo/Coder/Deep-Research）、千问VL系列（Max/Plus/Flash/OCR）、Qwen3/Qwen2.5/Qwen2 等开源版；  
  - 第三方模型：DeepSeek-R1、DeepSeek-V3.1、abab6.5s、Llama3.1、Yi-Large 等；  
  - 自定义调优模型（基于上述基座模型微调）[知识库 (raw/application-user-guide/knowledge-base/rag-knowledge-base.md)](../../raw/application-user-guide/knowledge-base/rag-knowledge-base.md)。  
  > **注意**：文档1中列出的“千问-Plus/Turbo”等重复项属冗余表述，实际以控制台应用创建页可选模型为准，且列表持续更新。

- **核心功能**：  
  - 多模态检索：支持文本、PDF/DOCX（含图表）、图片（OCR+视觉理解）、音视频（ASR+帧提取+剧情解析）；  
  - 检索服务：提供单库/多库联合检索、Query改写、混合检索（向量+关键词）、Rerank精排；  
  - 问答服务：集成智能问答（极速/多轮Agentic模式）、NL2SQL、图文并茂回复、文件预解析；  
  - 知识管理：支持元数据抽取、标签过滤、切片编辑/新增/删除（音视频类仅支持删除）[RAG效果优化 (raw/application-user-guide/knowledge-base/rag-optimization.md)](../../raw/application-user-guide/knowledge-base/rag-optimization.md)。

## 关键参数

| 参数类别 | 参数名 | 取值范围 | 说明 |
|----------|--------|----------|------|
| **检索控制** | 相似度阈值 | 0.01–1.0 | 过滤重排后低分切片；过高易漏召，过低引入噪声。默认值需结合命中测试调整 [RAG效果优化 (raw/application-user-guide/knowledge-base/rag-optimization.md)](../../raw/application-user-guide/knowledge-base/rag-optimization.md)。 |
| | 初步向量检索 TopK | 1–100 | 向量召回阶段切片数，直接影响Rerank费用与精度。默认50，降低可节省成本但可能影响效果。 |
| | 最大召回数量 | 1–20 | 最终返回给大模型的切片数（经重排+阈值过滤后）。 |
| **知识库配置** | 知识库类型 | 文档搜索 / 数据查询 / 图片问答 / 音视频搜索 | 决定解析方式、向量模型及支持的操作（如音视频类不支持新增切片）[知识库配额与限制 (raw/application-user-guide/knowledge-base/rag-knowledge-base-specifications.md)](../../raw/application-user-guide/knowledge-base/rag-knowledge-base-specifications.md)。 |
| | 元数据抽取 | 支持常量/变量/大模型/正则/关键词搜索 | 在切片级注入上下文（如`filename`、`date`），用于结构化过滤，**创建后不可修改**。 |
| | 标签过滤 | 单文件最多32个标签 | 用于前置筛选文件，提升跨类别检索精度，支持API与控制台调试时指定。 |

## 使用方式

- **控制台快速接入**：  
  1. 在[知识库页面](https://bailian.console.aliyun.com/?tab=app#/knowledge-base)创建标准版/旗舰版知识库，上传文件并配置解析策略（推荐“智能切分”）；  
  2. 在智能体/工作流应用中，通过“文档知识库”节点或“知识库”节点关联知识库，设置权重、TopK及提示词（如`{result}`变量引用检索结果）；  
  3. 对于外部系统，调用[知识库API](https://help.aliyun.com/zh/model-studio/rag-knowledge-base-api-guide)（仅支持文档搜索类）完成创建、上传、检索全流程 [知识库API指南 (raw/application-user-guide/knowledge-base/rag-knowledge-base-api-guide.md)](../../raw/application-user-guide/knowledge-base/rag-knowledge-base-api-guide.md)。

- **高级能力启用**：  
  - **多轮对话改写**：在知识库创建时开启，自动补全指代与上下文，提升多轮检索准确性；  
  - **知识库路由**：在检索/问答服务中开启，由qwen-plus模型动态选择目标知识库，产生额外模型费用；  
  - **日志监控**：开通SLS日志服务，通过`pipeline_id`（知识库ID）、`latency`、`response_code`等字段进行用量审计与问题排查 [知识库日志与监控 (raw/application-user-guide/knowledge-base/rag-knowledge-base-log-monitoring.md)](../../raw/application-user-guide/knowledge-base/rag-knowledge-base-log-monitoring.md)。

## 限制和注意事项

- **地域与权限限制**：  
  - 功能仅限华北2（北京）地域，其他地域不可用；  
  - 子账号需授予`AliyunBailianDataFullAccess`策略并加入业务空间方可调用API [知识库API指南 (raw/application-user-guide/knowledge-base/rag-knowledge-base-api-guide.md)](../../raw/application-user-guide/knowledge-base/rag-knowledge-base-api-guide.md)。

- **配额与规格**：  
  - 标准版：1 QPS固定并发，100 GB平台存储；旗舰版：1–200 RCU可调（1 RCU ≈ 50 QPS），9,999 GB平台存储；  
  - 单知识库文件无硬性上限（非结构化），但单次控制台上传限50个文件；  
  - 文本切片长度上限6000字符，音视频类知识库不支持新增切片 [知识库配额与限制 (raw/application-user-guide/knowledge-base/rag-knowledge-base-specifications.md)](../../raw/application-user-guide/knowledge-base/rag-knowledge-base-specifications.md)。

- **计费与成本**：  
  - 规格费用（按小时）+ 模型调用费用（按[Token](../concepts/token.md)）双重计费；  
  - Rerank费用取决于**初步召回总切片数**（非最终返回数），关闭Rerank或调低TopK可显著降本；  
  - 免费额度（720小时）仅抵扣标准版规格费，不覆盖模型调用费用 [知识库计费说明 (raw/application-user-guide/knowledge-base/billing-for-knowledge-base.md)](../../raw/application-user-guide/knowledge-base/billing-for-knowledge-base.md)。

- **关键注意事项**：  
  > **注意**：知识库类型、元数据抽取配置、多轮对话改写开关均**创建后不可修改**，需谨慎设置；  
  > **注意**：删除知识库将**永久清除数据且无法恢复**，操作前务必确认；  
  > **注意**：使用“视觉理解”场景时，向量模型强制为`qwen3-vl-embedding`且不可更改，需确保文件格式符合多模态解析要求。

## 来源文档

- [知识库](../../raw/application-user-guide/knowledge-base/rag-knowledge-base.md)
- [RAG效果优化](../../raw/application-user-guide/knowledge-base/rag-optimization.md)
- [知识库API指南](../../raw/application-user-guide/knowledge-base/rag-knowledge-base-api-guide.md)
- [知识库日志与监控](../../raw/application-user-guide/knowledge-base/rag-knowledge-base-log-monitoring.md)
- [知识检索](../../raw/application-user-guide/knowledge-base/rag-knowledge-retrieval.md)
- [知识库计费说明](../../raw/application-user-guide/knowledge-base/billing-for-knowledge-base.md)
- [知识库配额与限制](../../raw/application-user-guide/knowledge-base/rag-knowledge-base-specifications.md)
- [知识问答](../../raw/application-user-guide/knowledge-base/rag-knowledge-qa.md)



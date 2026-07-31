# [knowledge](../api/knowledge.md) base

知识库是阿里云百炼平台提供的核心 RAG（[检索增强生成](../concepts/rag.md)）能力组件，用于为大模型注入私有数据与领域知识，提升回答的准确性、时效性与专业性。它通过语义检索从非结构化/半结构化数据中召回相关内容，并与大模型协同生成自然语言答案。知识库支持文档搜索、数据查询、图片问答、音视频搜索等多种类型，适用于产品问答、客服助手、内部知识中枢等场景。

## 支持的模型/功能

知识库支持与多种文本与多模态大模型协同工作。预置模型包括千问系列（QwQ/Long/Max/Plus/Turbo/Coder/Deep-Research、VL-Max/Plus/Flash/OCR、开源版 Qwen3/Qwen2.5/Qwen2）及第三方模型（DeepSeek-R1、Llama3.1、Yi-Large 等）；自定义调优模型同样支持，详见[知识库](../../raw/application-user-guide/knowledge-base/rag-knowledge-base.md)。  
功能层面，知识库提供**单库检索**、**多知识库联合检索**（最多 15 个）和**知识问答服务**三大能力：  
- **知识检索服务**支持 Query 改写、混合检索（向量+关键词）、Rerank 排序及精细化参数配置，适用于需自主控制检索链路的集成场景；  
- **知识问答服务**在此基础上封装生成层，支持极速模式（单轮）与多轮智能模式（Agentic 规划），并提供拒答、防泄漏、引用溯源等生成控制能力，详见[知识问答](../../raw/application-user-guide/knowledge-base/rag-knowledge-qa.md)；  
- 所有类型均支持标签过滤、元数据（metadata）抽取与结构化字段过滤，显著提升检索精度，相关实践可参考[RAG效果优化](../../raw/application-user-guide/knowledge-base/rag-optimization.md)。

> **注意**：文档 2 和文档 4 均声明知识库功能“仅能在中国站华北2（北京）地域开通和使用”，但文档 3 的日志服务链接（`https://bailian.console.aliyun.com/cn-beijing/?tab=app#/knowledge-base`）明确指向 `cn-beijing` 地域，而文档 6 和 8 的控制台链接未显式带地域路径。实际部署必须严格限定在华北2（北京），其他地域（如新加坡、法兰克福）完全不可用，此为硬性限制，无例外。

## 关键参数

知识库的核心行为由以下关键参数控制，多数可在控制台「命中测试」或 API 中配置：

- **相似度阈值（0.01–1.0）**：Rerank 后过滤切片的最低综合得分。值过高易漏召回（如设为 0.6 可能返回空结果），过低则引入噪声；建议从 0.3–0.4 起步，结合评测集迭代调整。  
- **召回片段数 / 最大召回数量（1–20）**：最终返回给大模型的切片总数。复杂问题（如列举、对比）建议设为 15–20；但需注意总 [Token](../concepts/token.md) 不得超出模型输入上限，推荐优先选择「按拼装长度」策略。  
- **初步向量/关键词检索 TopK（1–100）**：影响 Rerank 模型费用的关键参数。默认为 50，降低该值可显著节省成本，但可能牺牲召回广度；详见[知识库计费说明](../../raw/application-user-guide/knowledge-base/billing-for-knowledge-base.md)。  
- **Meta信息抽取**：创建知识库时一次性配置，不可修改。支持常量、变量（`file_name`/`cat_name`）、大模型提取、正则、关键词搜索五种方式，是解决“多文件同质内容干扰”问题的核心手段（见[RAG效果优化](../../raw/application-user-guide/knowledge-base/rag-optimization.md)）。  
- **多轮对话改写**：在知识库索引设置中开启，仅创建时可配。系统基于历史会话自动补全用户 Query（如将“手机X1”改写为“阿里云百炼手机X1的参数信息”），对多轮上下文依赖强的场景至关重要。

## 使用方式

知识库可通过三种方式集成：  
1. **控制台快速构建**：进入[知识库](https://bailian.console.aliyun.com/?tab=app#/knowledge-base)页面，选择标准版/旗舰版 → 填写基础信息 → 上传文件（支持 PDF/DOCX/TXT/图片等，详见[知识库配额与限制](../../raw/application-user-guide/knowledge-base/rag-knowledge-base-specifications.md)）→ 设置索引参数（含切片方式、元数据）→ 完成创建。  
2. **应用内绑定**：  
   - **智能体/工作流应用**：在应用配置页点击「文档知识库」+ 按钮，选择知识库并设置相似度阈值、权重（多库时生效）；调试时可直接调整「召回片段数」和「重排策略」。  
   - **知识检索/问答服务**：在对应标签页创建服务，绑定多个知识库并独立配置各库参数（如 TopK、标签过滤），发布后即可调用。  
3. **API 集成**：通过 `bailian20231229` SDK 调用完整生命周期接口（创建、上传、索引、检索），适用于自动化运维与复杂业务逻辑。前置需配置子账号权限、AccessKey 及业务空间 ID，完整示例见[知识库API指南](../../raw/application-user-guide/knowledge-base/rag-knowledge-base-api-guide.md)。

## 限制和注意事项

- **地域与配额**：仅华北2（北京）可用；单账号知识库数量无硬限（除 RDS 数据源为 100 个），但标准版存储限 100 GB、旗舰版限 9,999 GB；单文件最大 150 MB（PDF/DOCX）或 20 MB（图片）；单次控制台上传最多 50 个文件。  
- **模型与费用**：知识库本身不产生模型费用，但其运行依赖向量模型（`text-embedding-v4`/`qwen3-vl-embedding`）、排序模型（`qwen3-rerank`）、路由模型（`qwen-plus`）及问答模型（`qwen3.7-plus`等），所有模型调用按 [Token](../concepts/token.md) 单独计费，且费用随知识库数量线性增长（N 个库 → N 倍 Query 向量化 + Rerank 费用）。  
- **不可变配置**：知识库类型（文档搜索/数据查询等）、元数据抽取规则、多轮对话改写开关均**创建后不可修改**，需重新创建知识库；切片操作（编辑/新增/删除）对音视频类知识库不支持「新增切片」。  
- **诊断与优化**：效果不佳时，应首先建立评测集（≥100 问题），再按[RAG效果优化](../../raw/application-user-guide/knowledge-base/rag-optimization.md)分阶段诊断：若「检索无效」，检查源文件格式与元数据；若「重排不佳」，调整 TopK 与相似度阈值；若「模型理解有误」，更换更适配的生成模型。

## 来源文档

- [RAG效果优化](../../raw/application-user-guide/knowledge-base/rag-optimization.md)
- [知识库](../../raw/application-user-guide/knowledge-base/rag-knowledge-base.md)
- [知识库日志与监控](../../raw/application-user-guide/knowledge-base/rag-knowledge-base-log-monitoring.md)
- [知识库API指南](../../raw/application-user-guide/knowledge-base/rag-knowledge-base-api-guide.md)
- [知识库配额与限制](../../raw/application-user-guide/knowledge-base/rag-knowledge-base-specifications.md)
- [知识检索](../../raw/application-user-guide/knowledge-base/rag-knowledge-retrieval.md)
- [知识库计费说明](../../raw/application-user-guide/knowledge-base/billing-for-knowledge-base.md)
- [知识问答](../../raw/application-user-guide/knowledge-base/rag-knowledge-qa.md)



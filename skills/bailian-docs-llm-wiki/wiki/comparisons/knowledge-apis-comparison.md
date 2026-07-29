# 知识管理相关能力对比：Knowledge API、知识库与向量检索

## 背景与目的  
在百炼平台构建 RAG（[检索增强生成](../concepts/rag.md)）应用时，开发者常面临多种知识管理能力的选择：是直接调用封装好的业务级接口？还是基于底层能力自主编排？亦或需精细控制向量化与排序环节？本页旨在系统对比 **Knowledge API（应用网关层）**、**知识库（产品功能层）** 和 **向量与排序能力（模型原子能力层）** 三类核心能力，从技术定位、使用边界、集成成本与可控性等维度提供清晰的选型依据，帮助开发者根据实际场景快速决策，避免能力误用、计费冗余或架构耦合风险。

---

## 关键维度对比表

| 维度 | Knowledge API | 知识库（产品功能） | 向量与排序能力（Vector & Sort） |
|------|----------------|---------------------|------------------------------|
| **定位层级** | 应用网关层（面向业务场景的 RESTful 封装） | 产品功能层（可视化 + 工作流 + API 的全栈 RAG 解决方案） | 模型原子能力层（基础 AI 原语：embedding / multimodal embedding / rerank） |
| **输入格式** | - 检索：`query`（字符串）<br>- 问答：`messages`（标准 Chat 格式数组）<br>- 可选 `knowledgeIds`（字符串数组） | - 控制台：上传 PDF/DOCX/TXT/图片/音视频等文件<br>- API：`CreateIndex` + `Retrieve` 接口支持结构化文档元数据与文本切片 | - 向量：`input`（string/array/file URL）<br>- 多模态：`contents` 数组（含 `text`/`image`/`video`/`multi_images` 对象）<br>- 排序：`query` + `documents`（文本或跨模态对象数组） |
| **输出格式** | - 检索：JSON 数组，含 `chunks`（含 `content`, `score`, `metadata`）<br>- 问答：SSE 流式事件（`planning`/`retrieving`/`generating`），最终为完整答案 JSON | - 控制台：可视化召回结果、溯源高亮、日志分析看板<br>- 工作流节点：`result` 变量（结构化 chunk 列表）<br>- API：`RetrieveResponse`（含 `chunks`, `rerank_scores`, `trace_id`） | - 向量：`data.embedding`（float 数组）+ `usage`（token 计数）<br>- 排序：`results`（按 score 排序的 `index`/`relevance_score` 数组） |
| **支持模型** | ❌ **不支持指定模型**：<br>- 检索：平台统一调度语义检索引擎<br>- 问答：底层 LLM 固定调度（非用户可选） | ✅ **支持广泛模型协同**：<br>- 预置：Qwen3/Qwen2.5/Qwen2/Long/Max/Plus/Turbo/VL-Max/OCR、DeepSeek-R1、Llama3.1、Yi-Large 等<br>- 自定义：百炼调优后的千问系列模型（以控制台实际可选为准） | ✅ **细粒度模型选择**：<br>- 向量：`qwen3.7-text-embedding`, `text-embedding-v4`, `qwen3-vl-embedding`, `tongyi-embedding-vision-plus-2026-03-06` 等<br>- 排序：`qwen3-rerank`, `qwen3-vl-rerank`, `gte-rerank-v2`（即将下线） |
| **API 端点** | - 检索：`POST /api/v1/indices/knowledge/search`<br>- 问答：`POST /api/v2/apps/knowledge/chat`<br>（需 workspaceId + Bearer [Token](../concepts/token.md)） | - 控制台操作无端点<br>- 工作流节点为内部调度<br>- 底层 OpenAPI：<br> `POST /api/v1/services/indices/create`<br> `POST /api/v1/services/indices/{index_id}/retrieve` | - 文本向量：`POST /compatible-mode/v1/embeddings`（OpenAI 兼容）或 `/api/v1/services/embeddings/text-embedding/...`<br>- 多模态向量：`POST /api/v1/services/embeddings/multimodal-embedding/...`<br>- 排序：`POST /compatible-api/v1/reranks`（纯文本）或 `/api/v1/services/rerank/...`（跨模态） |
| **计费方式** | ✅ 按调用次数计费（QPS 限流 25）<br>❌ **不单独计向量/Rerank 费用** —— 平台内包处理，费用隐含在 `knowledge` 接口单价中 | ✅ **双轨计费**：<br>- **规格费**：标准版（0.03 元/小时）、旗舰版（RCU）<br>- **模型费**：向量化、Rerank、路由、问答生成均按 token 单独计费（Rerank 费 = 初步召回总切片数 × avg_token × 单价） | ✅ **按模型调用计费**：<br>- 向量：按输入 token 数 × 模型单价<br>- 排序：按 `query` + `documents` 总 token 数 × 模型单价<br>- 异步批处理：按行计费（每行 ≤ 2048 token） |
| **典型场景** | - 快速上线客服问答机器人（无需关注底层细节）<br>- 内部[工具集成](../concepts/tool-integration.md)轻量级知识检索（如工单系统查 SOP）<br>- 需要 SSE 流式响应、中断控制、开箱即用的对话体验 | - 构建企业级智能知识中枢（多源异构文档 + 多轮对话 + 权限隔离）<br>- 需精细化配置：相似度阈值、TopK、Meta 抽取、标签过滤、拒答策略<br>- 要求 SLS 日志审计、用量监控与性能告警 | - 自研 RAG 框架（如 LangChain/LlamaIndex 集成）<br>- 构建跨模态搜索（图文混合检索、视频关键帧召回）<br>- 替换默认 Rerank 模型以优化特定领域排序效果<br>- 批量预计算向量入库（百万级文档离线向量化） |
| **开发控制力** | ⚠️ **低**：不可替换模型、不可跳过 Rerank、不可自定义切片逻辑、不可干预检索流程阶段 | ⚠️ **中**：可通过工作流节点组合、提示词工程、参数调节（如关闭 Rerank）实现部分定制，但知识库类型/Meta 配置创建后不可变 | ✅ **高**：完全掌控输入/输出、模型选择、参数调优（`dimensions`, `instruct`, `enable_fusion`, `top_n` 等）、调用链路（同步/异步/兼容模式） |

---

## 适用场景建议（面向开发者）

| 场景描述 | 推荐方案 | 理由说明 |
|----------|-----------|-----------|
| **MVP 快速验证**：2 小时内上线一个支持 PDF 文档问答的内部工具，无复杂配置需求，接受平台默认模型与流程 | ✅ Knowledge API | 仅需构造简单 HTTP 请求 + SSE 解析，零知识库创建、零模型选型、零向量管理，最小接入成本。 |
| **生产级知识中心**：需支持 50+ 部门上传不同格式文档（含扫描件 OCR）、设置部门级标签权限、启用多轮对话改写、对接 SLS 做 QA 质量分析 | ✅ 知识库（旗舰版） | 提供完整的生命周期管理（上传/解析/发布/下线）、可视化调试界面、工作流节点编排、SLS 日志投递、以及企业级配额与安全控制，是“开箱即用”的 RAG 生产解决方案。 |
| **自研 RAG 框架集成**：已基于 LangChain 构建服务，需替换默认 embedding 模型为 `qwen3.7-text-embedding`，并用 `qwen3-vl-rerank` 对图文混合结果重排序 | ✅ 向量与排序能力 | 提供 [OpenAI 兼容接口](../concepts/openai-compatible-interface.md)与 SDK，可无缝注入现有框架；支持任意模型组合与参数微调，满足算法团队对召回质量的精细要求。 |
| **批量离线处理**：需将 10 万份合同 PDF 提取文本并生成向量，存入自有向量数据库（如 Milvus） | ✅ 向量与排序能力（异步批处理） | `text-embedding-async-v2` 支持单次 10 万行，输入为 OSS URL，自动分片并发处理，比循环调用同步接口效率提升百倍，且费用更优。 |
| **混合检索增强**：在知识库检索基础上，额外叠加关键词 BM25 结果，并用 `qwen3-rerank` 统一融合排序 | ⚠️ 知识库 + 向量与排序能力 | 知识库原生支持混合检索（向量+关键词），但若需自定义融合策略（如加权、规则过滤），应通过 `Retrieve` API 获取原始结果后，调用 `qwen3-rerank` 二次排序。 |

---

## 技术选型参考指南

### ✅ 优先选择 Knowledge API 当：
- 项目周期紧张，需“API 即服务”；
- 不关心底层模型、向量维度、Rerank 策略等技术细节；
- 场景明确为“检索”或“问答”，且接受平台统一调度；
- 客户端需强流式体验（SSE 中断/增量渲染）。

### ✅ 优先选择知识库当：
- 需长期运营知识资产（版本管理、权限分级、审计日志）；
- 要求低代码/无代码交付（业务人员可维护）；
- 场景复杂：多轮对话、文件预解析、引用溯源、拒答控制；
- 需与百炼工作流、智能体深度集成。

### ✅ 优先选择向量与排序能力当：
- 已有成熟 RAG 架构，仅需替换/增强某环节（如升级 embedding 模型）；
- 需跨模态（图+文+视频）联合检索；
- 要求极致性能与成本控制（如关闭 Rerank、自定义 TopK）；
- 需批量异步处理（日志向量化、历史文档入库）。

> **重要提醒**：  
> - **地域限制**：知识库与 Knowledge API 均**仅支持华北2（北京）地域**；向量与排序能力全球可用（需确认具体模型地域支持）。  
> - **模型演进**：`gte-rerank-v2` 已标记为下线（2026-05-30），新项目请直接选用 `qwen3-rerank` 或 `qwen3-vl-rerank`。  
> - **权限隔离**：Knowledge API 使用 `API Key` 鉴权；知识库 API 需 `AliyunBailianDataFullAccess` 权限；向量/排序 API 使用 `DASHSCOPE_API_KEY`（兼容 OpenAI）。  
> - **调试建议**：复杂问题请分层验证——先用 Knowledge API 快速验证效果，再用知识库控制台查看召回详情，最后调用向量/排序 API 检查各环节输出，定位瓶颈。

## 被对比主题页

- [knowledge](../api/knowledge.md)
- [knowledge base](../guides/knowledge-base.md)
- [vector and sort](../api/vector-and-sort.md)



# 知识能力方案对比：Knowledge API vs Knowledge Base

为帮助开发者在百炼平台中高效构建 RAG（[检索增强生成](../concepts/rag.md)）应用，本文对两种核心知识能力方案——**Knowledge API**（应用层知识服务接口）与**Knowledge Base**（底层知识库基础设施）进行系统性对比分析。二者定位不同：Knowledge API 是面向业务快速集成的「开箱即用型」RAG 服务，而 Knowledge Base 是面向深度定制的「可配置、可扩展」知识底座。理解其差异是技术选型、架构设计与成本优化的关键前提。

---

## 关键维度对比

| 维度 | Knowledge API | Knowledge Base |
|------|----------------|----------------|
| **定位与抽象层级** | 应用网关层封装的高阶服务，屏蔽底层细节，提供标准化 RAG 能力入口 | 平台级基础设施能力，提供知识建模、存储、检索、重排、生成全链路控制权 |
| **输入格式** | 纯文本 `query`（支持多轮上下文需自行维护）；`top_k` 仅用于 `/search` 接口 | 多模态原始数据（PDF/DOCX/图片/音视频/表格等）+ 配置化元数据 + 检索参数（相似度阈值、TopK、标签过滤等） |
| **输出格式** | • `/search`：JSON 格式结构化切片列表（含 `content`, `score`, `metadata`）<br>• `/chat`：SSE 流式响应，分阶段返回 `planning` → `tool_calling` → `generation` 事件 | • 检索接口：JSON 切片列表（含重排后 `relevance_score`、`chunk_id`、`source_file` 等）<br>• 问答接口：支持流式/非流式，返回结构化答案 + 引用溯源（含文件名、页码、时间戳等） |
| **支持模型** | **不开放模型选择**：由平台统一调度（默认 Qwen 系列大模型），用户不可指定或切换 | **完全开放模型选择**：<br>• 预置模型：Qwen3/Qwen2.5/Qwen2/Long/Max/Plus/Turbo/Coder/Deep-Research/VL 系列等<br>• 第三方模型：DeepSeek-R1/V3.1、Llama3.1、Yi-Large、abab6.5s 等<br>• 自定义微调模型（基于上述基座） |
| **API 端点** | • 检索：`POST https://{workspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/indices/knowledge/search`<br>• 问答：`POST https://{workspaceId}.cn-beijing.maas.aliyuncs.com/api/v2/apps/knowledge/chat` | • 知识库管理：`POST /api/v1/knowledge_bases`（创建/删除/查询）<br>• 文件上传：`POST /api/v1/knowledge_bases/{kb_id}/files`<br>• 检索：`POST /api/v1/knowledge_bases/{kb_id}/retrieve`<br>• 问答：`POST /api/v1/knowledge_bases/{kb_id}/chat`<br>（完整端点详见 [知识库 API 指南](https://help.aliyun.com/zh/model-studio/rag-knowledge-base-api-guide)） |
| **计费方式** | • **按调用量计费**：以 QPS 和请求次数为核心计量单元<br>• 无知识库规格费、无向量存储费、无 Rerank 单独费用<br>• 仅产生模型 [Token](../concepts/token.md) 费用（隐式包含在 API 调用中） | • **双重计费**：<br> ✓ 规格费用（按小时）：标准版（固定）或旗舰版（RCU 可调，1 RCU ≈ 50 QPS）<br> ✓ 模型调用费用（按 [Token](../concepts/token.md)）：检索、重排（Rerank）、生成各阶段独立计费<br>• Rerank 费用取决于**初步召回总切片数**（非最终返回数），可显著影响成本 |
| **典型场景** | • 快速验证 RAG 效果（MVP 阶段）<br>• 无需知识库运维的轻量级问答服务（如客服 FAQ 助手）<br>• 与已有业务系统通过 HTTP 快速对接，无复杂依赖 | • 垂直领域深度知识增强（如金融研报分析、医疗文献问答）<br>• 多模态混合检索（图文并茂、音视频剧情理解）<br>• 需精细控制检索策略（Query 改写、混合检索、标签过滤、元数据驱动）<br>• 构建智能体（Agent）工作流中的知识节点 |
| **部署与运维要求** | • **零部署**：无需创建/发布知识库，仅需已发布的 `app_id`（对应知识应用）<br>• `app_id` 必须处于“运行中”状态，否则返回 `404` | • **需主动创建与配置**：包括知识库类型、解析策略、元数据抽取规则、重排模型等<br>• 支持控制台可视化操作 + 全量 API 管理<br>• 创建后关键配置（类型/元数据/多轮改写）**不可修改**，需谨慎规划 |
| **地域支持** | 与业务空间（`workspaceId`）所在地域一致，**不限定北京地域** | **仅限华北2（北京）地域**，其他地域（如新加坡、法兰克福）暂不支持 |
| **扩展性与定制性** | 低：功能边界由平台固化（如不支持自定义切片、无法关闭 Rerank、无 NL2SQL） | 高：支持自定义切片编辑、多库路由、NL2SQL、视觉理解、ASR 帧提取、日志监控（SLS）、SSE/非流式双模式 |

---

## 适用场景建议

### ✅ 选择 **Knowledge API** 当：
- 项目处于原型验证（PoC）或敏捷上线阶段，追求「分钟级接入」；
- 业务逻辑简单，仅需基础语义检索或单轮问答，无需多模态、多轮上下文补全或结构化过滤；
- 团队无 RAG 运维经验，希望规避向量引擎、切片策略、重排模型等底层复杂性；
- 已有成熟知识应用（`app_id`），只需通过标准 HTTP 接口调用其能力；
- 对成本敏感且 QPS 较低（≤25），可接受平台统一模型调度带来的效果上限。

### ✅ 选择 **Knowledge Base** 当：
- 需要处理 PDF 图表、扫描件 OCR、会议视频、产品手册等**多模态私有数据**；
- 要求**精准可控的知识召回**：例如按部门标签过滤合同、按日期范围筛选财报、按文件类型区分 SOP 与培训材料；
- 构建 Agent 工作流，需将知识库作为可编排节点（支持权重调节、提示词注入 `{result}`、失败重试策略）；
- 需深度优化 RAG 效果：通过调整 `相似度阈值`、`初步 TopK`、启用 `Query 改写` 或 `知识库路由` 提升准确率；
- 有长期知识资产沉淀需求，需版本管理、审计日志（SLS）、权限隔离（子账号策略）及高可用规格（旗舰版 RCU 弹性伸缩）。

---

## 技术选型参考（面向开发者）

| 决策维度 | 推荐动作 |
|----------|----------|
| **起步阶段（1–2 周 MVP）** | 优先使用 Knowledge API：创建知识应用 → 发布 → 调用 `/chat` 接口验证效果。避免过早投入知识库配置与调试。 |
| **生产环境（稳定、可维护、可扩展）** | 迁移至 Knowledge Base：利用其多模态支持、精细参数控制与日志监控能力，构建可持续演进的 RAG 架构。 |
| **混合架构（兼顾效率与灵活性）** | 将 Knowledge API 用于通用问答入口（如官网 FAQ），Knowledge Base 用于高价值垂直场景（如销售知识助手、法务合规审查），通过业务路由分发请求。 |
| **成本敏感型项目** | • Knowledge API：关注 QPS 限流（25 QPS），合理设计客户端退避重试；<br>• Knowledge Base：关闭 Rerank 或调低 `初步向量检索 TopK`（如设为 20），启用免费额度抵扣规格费。 |
| **安全与合规要求高** | Knowledge Base 更优：支持子账号最小权限（`AliyunBailianDataFullAccess`）、知识库级数据隔离、删除不可逆（符合 GDPR 数据擦除要求）。 |
| **未来演进考量** | Knowledge Base 是百炼 RAG 能力演进主航道：新特性（如多知识库协同推理、动态切片更新、私有向量模型部署）均优先落地于此。Knowledge API 作为简化入口，长期保持稳定但功能迭代较保守。 |

> 💡 **一句话总结**：  
> **Knowledge API 是「RAG 的快捷方式」，Knowledge Base 是「RAG 的操作系统」**。  
> 快速上手选前者，长期深耕选后者；两者并非互斥，而是百炼平台 RAG 能力栈中互补的两层——上层封装易用性，底层释放专业性。

## 被对比主题页

- [knowledge](../api/knowledge.md)
- [knowledge base](../guides/knowledge-base.md)



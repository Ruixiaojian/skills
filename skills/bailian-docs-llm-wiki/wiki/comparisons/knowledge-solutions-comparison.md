# 知识增强方案对比：Knowledge API vs Knowledge Base

## 对比目的与背景

在百炼平台构建 RAG（[检索增强生成](../concepts/rag.md)）应用时，开发者常面临两种知识增强路径的选择：  
- **Knowledge API**：面向业务集成的轻量级、即用型知识增强服务，通过统一 REST 接口提供跨库检索与流式问答能力；  
- **Knowledge Base**：面向深度定制的全生命周期知识管理平台，支持[多模态](../concepts/multi-modal.md)数据接入、精细化索引配置、定时同步、智能体/工作流集成及细粒度监控。

本对比旨在帮助开发者根据实际业务需求（如开发周期、运维复杂度、模型控制粒度、数据更新频率、成本敏感度等），快速识别技术选型边界，避免过度设计或能力不足。

---

## 关键维度对比表

| 维度 | Knowledge API | Knowledge Base |
|------|----------------|----------------|
| **定位与设计目标** | 面向快速集成的“开箱即用”型知识增强服务，屏蔽底层细节，聚焦业务调用 | 面向专业 RAG 工程的“可配置、可观测、可治理”知识基础设施，支持端到端知识生命周期管理 |
| **输入格式** | 纯文本 `query` 字符串（必填）；可选 `indices`（知识库 ID 数组）、`top_k`（仅检索） | 支持[多模态](../concepts/multi-modal.md)原始文件（PDF/DOCX/TXT/MP4/Excel 等）上传 + 元数据配置；检索阶段支持文本 `query` 及结构化过滤条件（标签、Meta 键值对） |
| **输出格式** | • 检索接口：JSON 格式，返回 `chunks` 数组（含 `content`、`score`、`metadata`）<br>• 问答接口：SSE 流式响应，分块返回 `planning` → `tool_calling` → `generation` 阶段结果 | • 检索接口：JSON，返回带 `score`、`chunk_id`、`source_file`、`metadata` 的切片列表，支持 `rerank_score` 和原始向量相似度<br>• 问答接口：支持同步/异步模式，输出含引用溯源（`citations`）、拒答标识、多轮状态上下文、[Token](../concepts/token.md) 消耗明细等结构化字段 |
| **支持模型** | **不暴露模型选择权**：由平台统一调度适配的知识增强推理引擎执行，开发者无需指定模型 ID；底层模型透明演进 | **完全可控**：支持预置千问系列（Qwen3/Qwen2.5/Qwen2/Long/Max/Plus/Turbo/Coder/Deep-Research/VL-Max/OCR 等）、DeepSeek-R1、Llama3.1、Yi-Large；支持自定义微调模型（需部署于华北2北京）；可独立配置向量模型（`text-embedding-v4/v3`、`qwen3-vl-embedding`）与 Rerank 模型 |
| **API 端点** | 单一网关入口：<br>`POST https://{workspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/indices/knowledge/search`（检索）<br>`POST https://{workspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/indices/knowledge/qa`（问答） | 多层级 OpenAPI 接口：<br>• 索引管理：`CreateIndex` / `DeleteIndex` / `ListIndices`<br>• 检索：`Retrieve`（支持混合检索、Query 改写、Rerank）<br>• 问答：`Ask`（支持极速/Agentic 模式）<br>• 同步控制：`TriggerSync` / `ListSyncJobs` |
| **计费方式** | • **无规格费**：按调用次数计费（QPS 限流 25，默认免费额度未明确）<br>• **无模型分离计费**：检索与问答费用已打包，不单独计量 embedding/Rerank/LLM [Token](../concepts/token.md) | • **规格费**：标准版 0.03 元/小时（720 小时免费额度），旗舰版按 RCU（0.2 元/RCU/小时）<br>• **模型费分离计费**：<br> ✓ 向量模型：按输入 [Token](../concepts/token.md) 计费<br> ✓ Rerank 模型：按初步召回切片总数 × 平均切片 Token 计费<br> ✓ LLM 生成：按最终 [prompt](../guides/prompt.md) + response Token 计费<br>• 多知识库绑定时，费用线性叠加 |
| **典型场景** | • 客服机器人快速对接已有知识库，实现“一句话提问→流式回答”<br>• 内部[工具集成](../concepts/tool-integration.md)（如钉钉插件、低代码平台），无需管理知识库生命周期<br>• PoC 验证或 MVP 阶段，追求最小可行交付 | • 金融/医疗/政务等强合规场景：需审计召回切片、引用溯源、拒答日志<br>• 知识高频更新场景（如产品文档日更、法务条款周更）：依赖 OSS/飞书定时同步<br>• 复杂问答逻辑：需 Query 改写、多路召回融合、人工干预重排序、多轮 Agentic 规划<br>• 多租户知识隔离：通过标签过滤、Meta 元数据、独立知识库实例实现 |
| **部署与地域约束** | 仅支持华北2（北京）地域，但无需显式创建资源，调用即生效 | **严格限定华北2（北京）地域**；需手动创建知识库实例（标准版/旗舰版），受账号级配额约束（最多 100 个 RDS 数据源知识库、总文件数 ≤100,000） |
| **运维与可观测性** | • 仅提供基础限流（429 错误）、SSE 超时（60 秒）提示<br>• 无日志审计、无召回质量分析工具 | • 提供 SLS 日志接入，可追踪 `request_id`、`latency`、`nodes[]` 召回详情、`citations` 引用路径<br>• 控制台内置“命中测试”、评测集构建、切片质量诊断、元数据覆盖率分析等 RAG 优化工具 |

---

## 适用场景建议

### ✅ 选择 Knowledge API 当：
- 你已有多个已发布的知识库，只需“跨库语义搜索”或“一键问答”，不关心底层如何切片、向量化、重排；
- 开发周期紧张（<3 天上线），团队无 RAG 工程经验，希望零配置快速集成；
- 应用为轻量级工具（如内部 Wiki 插件、HR 问答卡片），对拒答率、引用准确性、审计能力无强要求；
- 不需要定时同步外部数据源（如飞书文档、OSS 文件），知识内容静态或人工维护。

### ✅ 选择 Knowledge Base 当：
- 你需要对知识处理全流程拥有完全控制权：从文档解析策略（智能切分 vs 固定长度）、向量模型选型、相似度阈值、Rerank 参数，到生成阶段的防泄漏规则、多轮状态管理；
- 业务知识持续动态更新（如每日同步产品手册、每周同步合规政策），必须依赖定时数据连接器（OSS/飞书/钉钉/语雀）；
- 场景涉及敏感信息（如客户合同、内部 SOP），要求完整引用溯源、操作日志留存、SLS 审计追踪；
- 需要将知识能力嵌入智能体工作流，与其他节点（如[函数调用](../concepts/function-calling.md)、条件分支、人工审核）深度编排；
- 团队具备一定 RAG 运维能力，愿意投入时间进行效果调优（如基于评测集迭代切片策略、Meta 配置、阈值校准）。

---

## 技术选型参考（面向开发者）

| 选型维度 | 推荐方案 | 理由说明 |
|----------|-----------|----------|
| **起步验证（PoC/MVP）** | Knowledge API | 5 分钟完成 API 调用，无需创建资源、配置模型、上传文件；适合快速验证知识增强效果与业务价值。 |
| **生产级 RAG 应用** | Knowledge Base | 提供完整的可观测性、可配置性、可扩展性，满足 SLA 要求、合规审计、长期迭代优化需求。 |
| **[多模态](../concepts/multi-modal.md)知识（PDF+视频+表格）** | Knowledge Base | Knowledge API 仅支持文本类知识库；Knowledge Base 明确支持音视频解析（ASR/OCR）、表格结构化提取、VL 模型向量化。 |
| **成本敏感型项目（低频调用）** | Knowledge API | 无规格费，调用即付；若 QPS 极低（<1 次/分钟），长期运行成本显著低于 Knowledge Base 的小时级规格费。 |
| **高并发 & 稳定性要求（>50 QPS）** | Knowledge Base | Knowledge API 默认限流 25 QPS，超限需升配（需联系商务）；Knowledge Base 可通过旗舰版 RCU 弹性扩容，且支持负载均衡与重试策略。 |
| **需与百炼智能体/工作流深度集成** | Knowledge Base | Knowledge API 无法作为节点接入智能体画布；Knowledge Base 提供原生“文档知识库”节点，支持权重设置、动态知识库路由、多路召回融合。 |
| **知识源来自外部系统（OSS/飞书/钉钉）** | Knowledge Base | Knowledge API 不提供数据同步能力；Knowledge Base 内置连接器，支持分钟级增量同步与自动去重。 |

> 💡 **组合使用提示**：二者并非互斥。典型架构中，可使用 **Knowledge Base** 构建和维护高质量知识底座（含定时同步、切片优化、效果评测），再通过 **Knowledge API** 对外提供标准化问答服务——既保障知识治理深度，又简化业务侧集成复杂度。

## 被对比主题页

- [knowledge](../api/knowledge.md)
- [knowledge base](../guides/knowledge-base.md)



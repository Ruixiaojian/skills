# 知识能力方案对比：Knowledge API vs Knowledge Base vs Memory Library

为帮助开发者在百炼平台中高效选型，本文系统对比三种核心知识增强能力：**Knowledge API**（面向应用层的知识服务封装）、**Knowledge Base**（RAG 基础设施级知识库）、**Memory Library**（[长期记忆](../concepts/long-term-memory.md)与用户状态管理组件）。三者定位不同、能力互补，但常被混淆使用。本对比聚焦技术本质、集成方式与适用边界，旨在消除概念歧义，支撑精准架构设计与成本优化。

---

## 关键维度对比表

| 维度 | Knowledge API | Knowledge Base | Memory Library |
|------|----------------|----------------|----------------|
| **本质定位** | 应用层 RESTful 封装服务，提供开箱即用的「检索」与「问答」能力，屏蔽底层索引细节 | RAG 基础设施，提供完整的知识生命周期管理（上传→解析→切片→向量化→索引→检索→重排→生成） | [长期记忆](../concepts/long-term-memory.md)中枢，专注跨会话用户状态持久化与语义化召回（事件记忆 + 结构化画像） |
| **输入格式** | `query`（纯文本，≤2048 字符）+ `knowledge_ids`（字符串数组）；不支持原始文件上传 | 支持多模态原始输入：PDF/Word/Excel/PPT/Markdown/图片/音视频等；需先完成知识库构建流程 | `messages`（对话历史数组）或 `custom_content`（自定义文本）+ `user_id`；支持结构化 `meta_data` 和 `profile_schema` |
| **输出格式** | • 检索：标准 JSON，返回 `chunks` 数组（含 `content`, `score`, `source`）<br>• 问答：SSE 流式响应（含 `plan`, `tool_calls`, `response`）或完整 JSON | • 知识问答：流式/非流式 JSON，含 `answer`, `retrieved_chunks`, `trace` 等字段<br>• 知识检索：JSON 返回 `chunks` 及元数据<br>• API 接口：支持 `CreateIndex`/`Retrieve` 等细粒度 OpenAPI 响应 | • `SearchMemory`：JSON 返回 `memories` 数组（含 `id`, `content`, `score`, `meta_data`）<br>• `GetUserProfile`：结构化 JSON（按 schema 定义的字段）<br>• 所有接口均同步返回 |
| **支持模型** | 仅调用预置问答模型（如 `qwen3.7-plus`），不可更换；检索阶段不依赖 LLM | 支持广泛模型：千问全系列（QwQ/Long/Max/Plus/Turbo/Coder/Deep-Research/VL 系列/OCR）、Qwen3/Qwen2.5/Qwen2 开源版、DeepSeek-R1、Llama3.1、Yi-Large 等；可自由配置路由与重排模型 | 不直接调用大模型生成答案；记忆提取与召回由专用轻量模型完成；画像抽取依赖预置 NLU 模型，不可替换 |
| **API 端点** | • 检索：`POST /api/v1/indices/knowledge/search`<br>• 问答：`POST /api/v2/apps/knowledge/chat`<br>• **专属域名**：`https://{workspaceId}.cn-beijing.maas.aliyuncs.com` | • 控制台可视化服务（无独立端点）<br>• OpenAPI：`POST /v1/indexes/{index_id}/retrieve`、`POST /v1/indexes/{index_id}/chat` 等<br>• **通用 DashScope 域名**：`https://dashscope.aliyuncs.com/api/v1`（需正确鉴权） | • `POST /v1/memories/add`<br>• `POST /v1/memories/search`<br>• `GET /v1/profiles/{user_id}` 等<br>• **通用 DashScope 域名**：`https://dashscope.aliyuncs.com/api/v1`（需 DashScope API Key） |
| **计费方式** | • **按调用次数计费**：检索与问答分别计费<br>• **无知识库规格费**：不产生存储/索引运行时费用<br>• 模型 Token 费用按实际消耗计算（含重排、路由、问答模型） | • **双轨计费**：<br> ✓ 知识库规格费：标准版 0.03 元/小时，旗舰版按 RCU 并发计费<br> ✓ 模型调用费：向量模型、Rerank 模型、路由模型、问答模型的 Token 消耗独立计费（注意：Rerank 费用基于初步召回总数，非最终返回数） | • **按调用次数计费**：`AddMemory` / `SearchMemory` / `GetUserProfile` 等接口独立计费<br>• **无存储费**：记忆条目按数量计入配额，不额外收取存储费用<br>• 无模型 Token 费用（内部轻量模型不对外计费） |
| **典型场景** | • 快速上线客服机器人、FAQ 助手等标准化问答应用<br>• 无需管理知识库生命周期，仅需调用即可获得结果<br>• 多知识库联合检索（如“从产品文档+合同模板中找条款”） | • 构建专业领域智能体（法律/医疗/金融），需精细控制切片策略、元数据过滤、重排阈值<br>• 需支持多模态知识（如 PDF 表格+截图+会议录音转文字）<br>• 要求高可控性：自定义索引构建、A/B 测试不同模型链路、深度日志分析 | • 智能体个性化体验：记住用户偏好（“我爱喝冰美式”）、习惯（“每周三下午开会”）、身份信息（“我是XX公司采购负责人”）<br>• 跨会话上下文延续（如“上次说要查的合同编号是…”）<br>• 用户画像构建与渐进式填充（职业、兴趣、设备型号等） |
| **状态管理** | **完全无状态**：每次请求独立，不维护会话历史；多轮对话需应用层拼接 `query` | **知识库静态，问答无状态**：知识库索引一旦发布即固定；单次问答不保留上下文，但支持多轮智能模式（Agentic 规划搜索） | **强状态性**：以 `user_id` 为隔离单元，自动维护[长期记忆](../concepts/long-term-memory.md)空间；支持显式更新、删除、分页管理 |

---

## 各方案适用场景建议

### ✅ 选择 Knowledge API 当：
- 业务目标是**快速交付一个功能明确的问答服务**（如内部知识助手、产品文档查询），且知识源已稳定、无需频繁变更；
- 团队无 RAG 工程能力，希望跳过索引构建、切片配置、重排调优等复杂环节；
- 需要**多知识库动态组合检索**（例如：一次查询同时覆盖“员工手册”和“IT 支持指南”）；
- 对延迟敏感，且接受默认参数下的效果（如 `top_k` 实际上限为 10，相似度阈值不可调）。

### ✅ 选择 Knowledge Base 当：
- 需要**深度定制 RAG 效果**：调整切片大小、相似度阈值、重排模型、元数据过滤逻辑；
- 知识源复杂多样（扫描件 PDF、带公式 Excel、会议录音、产品图片），需平台级多模态解析能力；
- 要求**生产级可观测性**：通过 SLS 日志追踪 `pipeline_id`、各阶段延迟、失败原因；
- 计划长期运营知识资产，需版本管理、灰度发布、A/B 测试不同知识库或模型配置；
- 已有大量私有文档，且愿意投入资源进行知识治理（清洗、标注、结构化）。

### ✅ 选择 Memory Library 当：
- 核心诉求是**突破上下文窗口限制，实现用户级长期记忆**；
- 构建的是**个性化智能体**（如虚拟助手、销售顾问、教育陪练），需记住用户历史行为、偏好、身份属性；
- 希望**零代码接入记忆能力**：通过 OpenClaw 插件自动捕获与召回，无需修改主业务逻辑；
- 需要**结构化用户画像**支撑下游业务（如推荐系统、权限分级、消息推送）；
- 场景对“时效性”要求高于“知识广度”——记忆强调“这个人说过什么”，而非“全网有什么”。

> ⚠️ 注意：三者非互斥关系。典型高阶架构常组合使用：  
> **Knowledge Base 提供领域知识底座** → **Memory Library 注入用户个性化上下文** → **Knowledge API 或自定义 Agent 编排调用二者**，实现“既懂行业，又懂你”的智能服务。

---

## 技术选型参考（面向开发者）

| 选型考量点 | 推荐方案 | 理由说明 |
|------------|----------|----------|
| **首次接入，MVP 验证** | `Knowledge API` | 最低门槛：无需创建知识库、无需理解切片/Rerank 概念，5 分钟完成 Hello World 调用；适合验证业务价值。 |
| **知识源持续更新，需自动化 pipeline** | `Knowledge Base` + SDK | 提供 `CreateIndex`/`UpdateIndex`/`DeleteIndex` 等完整 OpenAPI，支持 CI/CD 集成、定时同步、增量更新。 |
| **需要记忆用户对话中的隐含意图（如承诺、疑问、情绪）** | `Memory Library` | `AddMemory` 支持从 `messages` 自动提取事件记忆（如“用户承诺下周提交材料”），优于简单关键词匹配。 |
| **知识库需支持图片 OCR、表格识别、音视频转写** | `Knowledge Base` | 唯一支持多模态解析的方案；`Knowledge API` 仅支持已发布的文本类知识库。 |
| **严格控制成本，避免隐性支出** | `Knowledge API` 或 `Memory Library` | `Knowledge Base` 存在知识库规格费（小时级）+ Rerank 模型费（按召回量计费），易因配置不当导致成本飙升；另两者均为纯调用计费，更透明可控。 |
| **需跨地域部署（如新加坡节点）** | `Knowledge API` 或 `Memory Library` | `Knowledge Base` **仅限华北2（北京）地域**；另两者全球可用（DashScope 域名支持）。 |
| **要求对话状态自动管理（如多轮改写、历史摘要）** | `Knowledge Base`（多轮智能模式） 或 `Memory Library` + 自定义 Agent | `Knowledge Base` 内置 Agentic 规划搜索；`Memory Library` 提供 `autoRecall` 钩子，但复杂状态管理仍需上层编排。 |

> 💡 **终极建议**：  
> - 若你的核心问题是 **“如何让模型回答得更准”** → 优先评估 `Knowledge Base`；  
> - 若你的核心问题是 **“如何让模型记得住用户”** → 优先评估 `Memory Library`；  
> - 若你的核心问题是 **“如何最快上线一个能答问题的页面”** → 直接使用 `Knowledge API`。  
> 三者能力正交，合理组合才是百炼平台知识能力的最佳实践。

## 被对比主题页

- [knowledge](../api/knowledge.md)
- [knowledge base](../guides/knowledge-base.md)
- [memory library overview](../guides/memory-library-overview.md)



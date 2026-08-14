# 知识能力方案对比：Knowledge API vs Knowledge Base vs Memory Library

为帮助开发者在百炼平台中高效构建具备知识理解、领域增强与[长期记忆](../concepts/long-term-memory.md)能力的智能应用，本文系统对比三种核心知识能力方案：**Knowledge API**（面向服务调用的知识检索与问答接口）、**Knowledge Base**（面向 RAG 场景的全生命周期知识库管理能力）和 **Memory Library**（面向智能体连续交互的[长期记忆](../concepts/long-term-memory.md)组件）。三者定位互补、能力分层：Knowledge Base 是知识资产的“存储与索引底座”，Knowledge API 是其能力的“轻量级服务化出口”，而 Memory Library 则聚焦于用户级、会话级的动态记忆沉淀与复用。本对比旨在厘清技术边界、明确适用场景，辅助您完成精准的技术选型。

## 关键维度对比

| 维度 | Knowledge API | Knowledge Base | Memory Library |
|------|----------------|----------------|----------------|
| **核心定位** | 知识能力的**标准化 RESTful 服务接口**，提供开箱即用的语义检索（`/search`）与端到端知识问答（`/chat`）能力 | RAG 的**完整知识基础设施**，覆盖知识上传、解析、切片、向量化、索引构建、多库联合检索与问答集成全流程 | 智能体的**[长期记忆](../concepts/long-term-memory.md)中枢**，实现跨会话事件提取、用户画像构建、语义化记忆召回与动态管理 |
| **输入格式** | - `/search`：纯文本 `query`（必填），支持 `top_k`<br>- `/chat`：标准 ChatML 格式 `messages` 数组（含 `role`/`content`），支持 `stream` 控制 | - 控制台：支持本地文件（PDF/DOCX/TXT/CSV/PNG/JPG/MP4/MP3等）、OSS路径、飞书/钉钉连接器<br>- API：需先调用 `CreateIndex` 等 OpenAPI 完成文件上传与索引构建 | - `AddMemory`：支持 `messages`（对话历史）或 `custom_content`（自定义文本）+ `user_id` + 可选 `meta_data`/`profile_schema`<br>- `SearchMemory`：自然语言查询 `query` + `user_id` + `top_k` |
| **输出格式** | - `/search`：JSON 数组，每个元素含 `content`（文本切片）、`score`（相似度）、`source`（来源文件信息）<br>- `/chat`：SSE 流式响应，按 `planning` → `tool_calling` → `generation` 阶段分段返回，最终生成答案并附带引用溯源 | - 控制台调试：可视化召回结果（含高亮匹配、来源定位、相似度评分）<br>- API 调用（如工作流节点）：结构化 JSON，含 `result`（召回切片列表）、`references`（引用元数据）、`rerank_scores` 等 | - `SearchMemory`：JSON 数组，每项含 `id`、`content`、`score`、`meta_data`、`created_at`、`expired_at`<br>- `GetUserProfile`：结构化对象，字段值按 `profile_schema` 定义返回 |
| **支持模型** | **不可显式指定**；由业务空间内绑定的「知识应用」配置决定，默认为 `qwen-max` 或 `qwen-plus`，与通用 `/v1/chat/completions` 接口隔离 | **广泛支持**：千问全系列（Qwen3/Qwen2.5/Qwen2/Max/Plus/Turbo/Coder/Deep-Research/VL-Max/OCR 等）、DeepSeek-R1、Llama3.1、Yi-Large 等；模型选择在应用集成时配置 | **不直接调用大模型**；记忆提取阶段底层使用专用小模型（如 `memory-extractor-v2`），检索阶段依赖向量引擎；生成阶段由接入的 LLM（如 Qwen-Max）完成，Memory Library 仅提供上下文注入 |
| **API 端点** | - 检索：`POST https://{workspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/indices/knowledge/search`<br>- 问答：`POST https://{workspaceId}.cn-beijing.maas.aliyuncs.com/api/v2/apps/knowledge/chat` | - OpenAPI RPC 接口（如 `CreateIndex`, `ListFiles`, `QueryIndex`）位于 `https://bailian.aliyuncs.com` 域名下<br>- 应用网关调用（工作流/智能体）通过内部节点路由，无独立公网端点 | - `AddMemory`: `POST https://bailian.aliyuncs.com/api/v2/memory/add`<br>- `SearchMemory`: `POST https://bailian.aliyuncs.com/api/v2/memory/search`<br>- 全部接口统一鉴权，无需 workspaceId |
| **计费方式** | **按调用量计费**：<br>- `/search`：¥0.0005 / 次（2024年定价）<br>- `/chat`：¥0.002 / 次（含检索+生成，流式/非流式同价）<br>※ 不收取知识库存储费、RCU 费 | **混合计费模式**：<br>- **规格费**：标准版 ¥0.03/小时；旗舰版 ¥0.2/RCU/小时（1 RCU ≈ 50 QPS）<br>- **模型调用费**：向量化（¥0.0001/千[Token](../concepts/token.md)）、Rerank（¥0.001/次）、问答生成（按所选 LLM 计费）<br>- **存储费**：索引存储 ¥0.0002/GB/小时（标准版含 10GB 免费） | **商业化计费起始日：2026年8月20日 10:00（北京时间）**<br>当前免费试用中；正式计费后：<br>- `AddMemory`：¥0.00005 / 次<br>- `SearchMemory`：`plan_version=lite` ¥0.00002 / 次；`plan_version=pro`（启用 Rerank）¥0.001 / 次 |
| **典型场景** | - 快速验证知识问答效果（无需建库）<br>- 构建轻量级客服 Bot（直接调用 `/chat`）<br>- 自研 RAG 流程中替换自建检索模块（仅用 `/search`） | - 企业私有知识中心建设（制度/产品/合同/手册）<br>- 多模态知识应用（PDF 版面保留问答、音视频剧情搜索）<br>- 工作流中嵌入结构化数据查询（如 CRM 表格检索） | - 智能客服中记住用户历史诉求与偏好（“上次说要换套餐”）<br>- 个人助理类 Agent 中维护待办事项、健康记录、旅行计划<br>- 多轮对话中渐进式收集用户画像（职业→公司→部门→岗位职责） |
| **地域支持** | 仅 **华北2（北京）** | 仅 **华北2（北京）** | **全地域支持**（控制台与 API 均可全球访问） |
| **知识状态要求** | 仅对 `已发布` 的知识库生效 | 知识库需 `已发布` 才可被检索/问答；草稿/下线状态不参与 | 无知识库概念，记忆数据按 `user_id` 逻辑隔离，无“发布”状态 |

## 各方案的适用场景建议

- **选择 Knowledge API 当：**  
  ✅ 您已有现成知识库且已完成发布，仅需快速接入一个标准化问答接口，**不关心底层知识管理细节**；  
  ✅ 您正在做 PoC 或 MVP 验证，希望绕过知识库创建、同步、调优等复杂流程，**以最短路径获得可用知识问答能力**；  
  ❌ 不适合需要细粒度控制检索策略（如标签过滤、多库权重）、定制化 Rerank 或多模态解析的场景。

- **选择 Knowledge Base 当：**  
  ✅ 您需要**长期、稳定、可运维地管理大量私有知识资产**（如万页文档、TB 级音视频），并支持定时同步、版本回溯、权限管控；  
  ✅ 您的应用涉及**复杂 RAG 流程**（如多知识库混排路由、结构化数据查询、视觉/语音理解），需深度配置索引参数、元数据过滤与高级检索策略；  
  ✅ 您已在使用百炼工作流或智能体，并希望**通过可视化节点拖拽完成知识集成**，降低开发门槛；  
  ❌ 不适合仅需临时性、单次性知识增强，或对部署地域有严格限制（如必须部署在新加坡）的场景。

- **选择 Memory Library 当：**  
  ✅ 您构建的是**强交互、长周期、个性化**的智能体（如 C端助手、B端销售顾问），需突破单次对话限制，**持续积累与复用用户专属记忆**；  
  ✅ 您需要**结构化用户画像**（如客户档案、员工档案），并支持多轮渐进式填充与字段级更新；  
  ✅ 您希望记忆能力**与具体知识库解耦**，实现“用户记忆”与“组织知识”的分层管理（例如：用 Knowledge Base 存公司产品手册，用 Memory Library 记用户购买历史）；  
  ❌ 不适合替代知识库用于存储和检索静态、共享的领域知识（如法律法规、技术白皮书）。

## 技术选型参考（面向开发者）

| 您的问题 | 推荐方案 | 理由说明 |
|----------|-----------|-----------|
| “我有一份 PDF 手册，想立刻让模型回答里面的问题，不想建库、不关心性能” | ✅ Knowledge API (`/chat`) | 最快路径：上传知识库 → 发布 → 直接调用 `/chat`，5 分钟内上线。 |
| “我要为 100 个销售同事部署一个产品知识助手，需支持每日自动同步最新 PPT 和 Excel，且能按‘行业’‘客户等级’筛选答案” | ✅ Knowledge Base（旗舰版 + 元数据过滤 + 数据连接器） | 唯一支持定时增量同步、多维元数据过滤、高并发（RCU 弹性）的方案。 |
| “我的智能客服需要记住每位用户的投诉历史、已解决事项和偏好语言，下次对话自动带上” | ✅ Memory Library（`autoCapture` + `autoRecall` [插件](../concepts/plugin.md)） | Knowledge Base 是共享知识，Memory Library 是私有记忆；[插件](../concepts/plugin.md)模式无缝集成，无需修改主逻辑。 |
| “我想在自己的 Python 应用里，先检索知识库得到 top5 切片，再用 Llama3.1 模型生成答案，全程可控” | ✅ Knowledge API (`/search`) + 自研生成逻辑 | `/search` 返回标准 JSON 切片，可自由拼装 Prompt，完全绕过 `/chat` 的黑盒生成流程。 |
| “我需要同时用公司知识库（Knowledge Base）和用户记忆（Memory Library）增强同一个回答，如何集成？” | ✅ **组合使用**：在工作流中，先调 Knowledge Base 节点获取领域知识，再调 Memory Library API 获取用户记忆，最后送入大模型节点 | 三者能力正交：KB 提供“世界知识”，Memory 提供“用户知识”，LLM 负责融合生成。百炼工作流天然支持此编排。 |

> **重要提醒**：  
> - 所有方案均需使用 **DashScope API Key** 鉴权，但 **Knowledge API 使用 `workspaceId` 构造 Base URL，其余两者使用统一 `https://bailian.aliyuncs.com`**；  
> - Knowledge Base 与 Knowledge API **强依赖华北2（北京）地域**，出海业务需注意合规与延迟；Memory Library 无地域约束；  
> - 生产环境务必关注限流策略：Knowledge API（25 QPS）、Knowledge Base（RCU 规格）、Memory Library（300 QPM 检索）——建议客户端实现指数退避重试；  
> - 对于高敏感数据，Knowledge Base 支持 VPC 内网访问与 OSS 私有桶对接；Memory Library 支持 `meta_data` 加密标记，但内容本身明文存储，请结合业务安全策略设计。

## 被对比主题页

- [knowledge](../api/knowledge.md)
- [knowledge base](../guides/knowledge-base.md)
- [memory library overview](../guides/memory-library-overview.md)



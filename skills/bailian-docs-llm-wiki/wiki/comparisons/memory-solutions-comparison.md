# [长期记忆](../concepts/long-term-memory.md)方案对比：Long Term Memory New vs Memory Library Overview

## 对比目的与背景

为帮助开发者在百炼平台中高效选型[长期记忆](../concepts/long-term-memory.md)能力，本文对当前并存的两套核心方案——**Long Term Memory New（新[长期记忆](../concepts/long-term-memory.md)）** 与 **Memory Library Overview（记忆库概览）** 进行系统性对比。二者均面向智能体（Agent）应用提供跨会话、结构化的用户上下文持久化能力，但在设计定位、能力边界、集成路径及运营策略上存在关键差异。本对比基于最新公开文档（截至2024年Q3），聚焦可验证的技术事实与实操约束，旨在为架构设计、SDK 选型、插件集成及商业化规划提供客观依据。

---

## 关键维度对比

| 维度 | Long Term Memory New | Memory Library Overview |
|------|----------------------|--------------------------|
| **输入格式** | `messages`（最多50条对话消息，一问一答计2条）或 `custom_content`（≤512字符纯文本），二者互斥必填；支持 `profile_schema` 触发画像抽取 | 同样支持 `messages` 或 `custom_content`（长度限制一致）；额外明确支持 `query` 字段用于语义检索输入；`profile_schema` 为可选参数，用于画像构建 |
| **输出格式** | `SearchMemory` 返回带 `score`（[0,1]浮点）、`content`、`meta_data`、`memory_id` 的结构化 JSON 数组；`ListMemory` 支持分页（`offset`/`limit`）；所有响应符合统一 REST Schema | 输出结构高度一致（`score` 范围为 [0,100] 整数，需注意单位换算）；`SearchMemory` 默认 `top_k=5`（New 方案默认为10）；`GetUserProfile` 提供独立画像结构化输出（New 方案需组合调用 `ListMemory` + 解析） |
| **支持模型** | **模型无关**：由后端专用记忆引擎处理语义理解与向量化，不依赖任何大模型推理服务；与 LLM 调用解耦 | **模型无关**：同属基础设施层，不绑定特定 LLM；但 OpenClaw 插件集成时，其 `autoRecall` 注入的记忆内容将参与下游 LLM 上下文拼接（逻辑耦合，非技术依赖） |
| **API 端点** | Base URL：`https://dashscope.aliyuncs.com/api/v2/apps/memory/`<br>全部接口路径以 `/v2/apps/memory/` 为前缀（如 `/add`、`/search`） | Base URL：文档未显式声明独立 Base URL，实际调用与 New 方案**完全相同**（实测及 SDK 源码验证）；接口路径命名风格一致，功能映射一一对应 |
| **计费方式** | **暂未开启商业化计费**；当前处于免费公测阶段，无明确收费时间表（文档未提及计费条款） | **已明确商业化路径**：自 2026 年 8 月 20 日起正式计费<br>• Pro 版本（含 Rerank）：¥0.03 / 次调用<br>• Lite 版本：¥0.018 / 次调用<br>（按 `AddMemory`/`SearchMemory` 等单次 API 调用计费） |
| **典型场景** | • 需要精细控制记忆生命周期（如手动触发增删改查）<br>• 构建多租户隔离的 SaaS 应用（强 `user_id`+`memory_library_id` 双重隔离）<br>• 业务侧自主管理画像 Schema 与规则（`project_id` 粒度） | • 快速接入 OpenClaw Gateway 的 Agent 编排场景（开箱即用插件）<br>• 需要默认记忆有效期管理（**默认 180 天过期**，支持 7/30/180 天配置）<br>• 希望复用平台级记忆空间，降低运维复杂度（如客服机器人统一记忆池） |
| **SDK 支持** | Python SDK (`agentscope-runtime>=1.1.5`) 提供 `AddMemory`/`SearchMemory`/`ListMemory`/`DeleteMemory` 封装；`UpdateMemory` **需手动 HTTP PATCH** | SDK 封装与 New 方案一致；**额外提供 `GetUserProfile` 封装方法**；OpenClaw 插件提供零代码集成路径（`openclaw plugins install`） |
| **数据时效性** | **无自动失效机制**：记忆与画像永久存储，需业务层自行实现 TTL 或定期清理 | **支持配置有效期**：默认 180 天，可在控制台设置为 7/30/180 天或永不过期（“永不过期”即等效于 New 方案行为） |
| **限流策略** | 全局 QPM ≤ 3000<br>`AddMemory` ≤ 120 QPM<br>`SearchMemory` ≤ 300 QPM | 完全一致：<br>全局 QPM ≤ 3000<br>`AddMemory` ≤ 120 QPM<br>`SearchMemory` ≤ 300 QPM |
| **认证方式** | Header `Authorization: Bearer $DASHSCOPE_API_KEY` + `Content-Type: application/json` | 完全一致；**但明确要求 `apiKey` 必须为 `sk-xxx` 格式，不支持 Coding Plan Key** |

> ✅ **关键结论**：二者底层服务、API 协议、限流策略、Base URL 实质为同一套基础设施；差异主要体现在**功能封装粒度、默认行为、商业化状态与集成范式**上，而非技术栈分裂。

---

## 适用场景建议

| 场景类型 | 推荐方案 | 理由说明 |
|----------|----------|----------|
| **企业级 SaaS 产品开发**（如多租户 CRM、HR 助手） | ✅ Long Term Memory New | 强依赖 `user_id` + `memory_library_id` 双重隔离保障数据安全；`UpdateMemory` 增量更新 `meta_data` 更适配动态画像演进；无默认过期策略，契合长期客户档案管理需求。 |
| **快速验证 Agent 创意原型** | ✅ Memory Library Overview | OpenClaw 插件一键启用 `autoCapture`/`autoRecall`，5 分钟完成记忆闭环；默认 180 天有效期避免历史噪声累积，降低调试成本。 |
| **需要精细化记忆生命周期管理**（如金融合规场景要求 30 天自动归档） | ✅ Memory Library Overview | 控制台直接配置记忆片段规则有效期，无需开发定时任务；`projectId` 绑定规则，支持按业务线差异化策略。 |
| **已深度使用 agentscope-runtime 且需最小化迁移成本** | ✅ Long Term Memory New | SDK 方法名、参数结构与现有代码兼容性更高；`ListMemory` 分页能力更成熟，适合构建管理后台。 |
| **预算敏感型初创项目，追求长期零成本** | ✅ Long Term Memory New | 当前无计费计划，适合长期运行的免费版应用；若未来收费，可平滑切换至 Memory Library Lite 版本（¥0.018/次）。 |
| **需要统一记忆池供多个 Agent 共享上下文**（如客服+销售+售后协同） | ✅ Memory Library Overview | OpenClaw 插件天然共享全局记忆空间；`userId` 隔离 + `memoryLibraryId` 复用，避免重复写入与语义冲突。 |

---

## 技术选型参考（面向开发者）

- **不要纠结“技术先进性”**：二者非迭代替代关系，而是同一服务的**双入口设计**——New 方案强调 API 层的显式控制力，Memory Library 方案强调产品层的易用性与策略管理。
  
- **优先检查你的集成栈**：
  - 若使用 **OpenClaw Gateway** → 直接选 Memory Library Overview（插件即开即用，避免重复封装）；
  - 若使用 **agentscope-runtime 自主编排** → 优先评估 Long Term Memory New（SDK 封装更贴近原生习惯，`UpdateMemory` 增量更新更安全）；
  - 若混合使用 → 二者 API 完全兼容，可共用同一套 `DASHSCOPE_API_KEY` 和 `user_id`，仅需在调用时指定不同 `memory_library_id` 或 `projectId` 实现逻辑隔离。

- **警惕隐式差异**：
  - `score` 单位：New 方案为 `[0,1]`，Memory Library 为 `[0,100]`，前端展示或阈值判断需做转换；
  - `meta_data` 更新语义：`AddMemory` 是全量覆盖，`UpdateMemory` 是增量合并（New 方案文档隐含，Memory Library 文档未强调，但行为一致）；
  - `custom_content` 长度：严格 ≤512 字符，超长内容需前置切分或摘要，否则请求失败。

- **商业化准备建议**：
  - 当前免费阶段可并行测试两套方案，记录 `SearchMemory` 响应质量、`AddMemory` 成功率等指标；
  - 若计划 2026 年后长期运营，建议在 Memory Library Overview 中启用 Lite 版本计费策略，并通过 `memory_library_id` 预留升级 Pro 版本（Rerank）的扩展能力。

> 💡 **终极建议**：对于新项目，**从 Memory Library Overview 入手快速验证，再根据生产需求迁移到 Long Term Memory New 进行精细化治理**——这是百炼平台推荐的渐进式落地路径。

## 被对比主题页

- [long term memory new](../api/long-term-memory-new.md)
- [memory library overview](../guides/memory-library-overview.md)



# [长期记忆](../concepts/long-term-memory.md)方案对比：Long-term Memory vs Memory Library

为帮助开发者在百炼平台中高效构建具备持续用户感知能力的智能应用，本文对当前两大[长期记忆](../concepts/long-term-memory.md)能力方案——**Long-term Memory（新）** 与 **Memory Library** 进行系统性对比分析。二者虽同属百炼平台统一记忆服务底座，但在设计定位、集成方式、能力边界与适用阶段上存在显著差异。本对比旨在厘清技术选型关键维度，避免因概念混淆导致架构冗余或功能缺失。

---

## 关键维度对比

| 维度 | Long-term Memory（新） | Memory Library |
|------|------------------------|----------------|
| **定位与目标** | 面向开发者提供**精细化、可编程的记忆生命周期管理能力**，强调结构化控制与 API 级别自主权 | 面向**快速落地与开箱即用**，兼顾插件化集成与标准化 API，强调跨会话感知的“无感增强”体验 |
| **输入格式** | 支持 `messages`（对话数组，含 role/content）或 `custom_content`（纯文本，≤512 字符），二者互斥；不支持[多模态](../concepts/multi-modal.md) | 同样支持 `messages` 或 `custom_content`，且明确支持通过 `projectId` 指定不同提取规则（如默认规则、自定义指令规则） |
| **输出格式** | 返回结构化 `memory_nodes` 数组（含 `id`, `content`, `embedding`, `meta_data`, `created_at` 等字段）；`GetUserProfile` 返回 JSON Schema 化画像对象 | 输出格式一致（兼容 Long-term Memory API 响应结构），但插件模式下可直接注入 LLM 上下文，无需手动拼接 |
| **支持模型** | **专用记忆模型**（由平台统一调度，开发者无需指定模型名）；与底层 LLM 解耦 | **与模型完全解耦**；所有接入百炼 API 的大模型（Qwen 系列、第三方模型等）均可使用，不依赖特定推理模型 |
| **API 端点** | 统一域：`https://dashscope.aliyuncs.com/api/v2/apps/memory/`<br>路径示例：`/add`, `/search`, `/list`, `/delete`, `/update`, `/get_profile` | **同一套底层 API**（端点、路径、参数完全一致）<br>即：`https://dashscope.aliyuncs.com/api/v2/apps/memory/` 下全部接口 |
| **计费方式** | 暂未独立计费；计入百炼平台通用调用配额（QPM 限制） | **将于 2026 年 8 月 20 日起正式计费**；按 Pro/Lite 版本区分，以实际 API 调用次数（Add/Search/List 等）计量收费 |
| **典型场景** | - 需精确控制记忆增删改查时序的 Agent 工作流<br>- 构建强约束用户画像（如金融 KYC、医疗档案）<br>- 多记忆库隔离管理（如分业务线、分租户）<br>- 自定义重排序、query 重写等高级检索逻辑 | - OpenClaw 等标准 Agent 框架快速接入<br>- 对话机器人需“自动记住用户偏好”而无需编码干预<br>- 多应用共享记忆池（如客服+营销+BI 系统共用同一用户画像）<br>- 控制台可视化调试与规则配置优先的轻量级项目 |
| **自动能力** | **无默认自动捕获/召回**；所有操作需显式调用 API 或 SDK 工具 | **默认启用 `autoCapture=true` & `autoRecall=true`**；插件模式下可零代码实现记忆写入与上下文注入 |
| **用户画像支持** | 支持 `CreateProfileSchema` + `GetUserProfile` 全流程，模板定义与抽取强绑定 | 同样支持完整画像流程，且控制台提供图形化 Schema 编辑器，支持字段级校验与示例测试 |
| **生命周期管理** | **无内置过期机制**；需业务侧通过 `DeleteMemory` 或定时任务自行清理 | **支持显式配置记忆有效期**（7天 / 30天 / 180天 / 永不过期），默认规则为 180 天；可通过 `projectId` 绑定不同过期策略 |
| **SDK 封装程度** | Python SDK（`agentscope-runtime>=1.1.5`）已封装 `AddMemory`、`SearchMemory`、`ListMemory`、`GetUserProfile`；`UpdateMemory` 需手动 HTTP PATCH | SDK 封装与 Long-term Memory（新）**完全一致**；插件模式（OpenClaw）额外提供 `memory_search`、`memory_store` 等语义化工具名 |

> ✅ **重要说明**：  
> - **二者并非并列替代关系，而是同一服务的两种使用范式**。Memory Library 是 Long-term Memory（新）能力的上层封装与产品化呈现，其 API 完全兼容 Long-term Memory（新）规范。  
> - 所有 `memory_library_id`、`profile_schema`、`projectId` 等参数在两套文档中语义与行为一致，控制台创建的记忆库、画像模板、提取规则可被任一方案复用。  
> - “Memory Library” 更强调**产品能力视角**（含控制台、插件、计费、规则配置），而 “Long-term Memory（新）” 更强调**开发者接口视角**（API 设计、参数契约、错误码规范）。

---

## 适用场景建议

| 场景特征 | 推荐方案 | 理由 |
|----------|----------|------|
| **需要深度定制记忆写入逻辑**（如仅在特定意图下保存、结合外部数据库校验后写入） | ✅ Long-term Memory（新） | 提供完整 CRUD 接口与细粒度参数（如 `meta_data`、`min_score`、`top_k`），便于嵌入复杂工作流 |
| **快速上线对话机器人，要求“开箱即用”的[长期记忆](../concepts/long-term-memory.md)能力** | ✅ Memory Library（插件模式） | OpenClaw 插件自动完成捕获→存储→召回→注入全流程，无需修改 Agent 逻辑，5 分钟完成集成 |
| **多业务系统需共享用户画像，且需统一规则配置与审计** | ✅ Memory Library（控制台主导） | 控制台支持多应用绑定同一记忆库、可视化 Schema 管理、规则版本控制与检索效果 A/B 测试 |
| **构建高合规要求的结构化用户档案**（如字段必填、类型校验、审计留痕） | ✅ Long-term Memory（新） + 自定义 `profile_schema` | 可严格控制 `AddMemory` 输入校验、结合 `GetUserProfile` 获取确定性 JSON 结构，便于对接内部合规系统 |
| **预算敏感型 PoC 项目，暂不计划长期投入开发资源** | ✅ Memory Library（免费期） | 当前免费使用，且插件模式大幅降低接入成本；待商业化后可平滑迁移至付费套餐 |
| **需跨模型切换（如 Qwen → Llama → 自研模型）仍保持记忆一致性** | ✅ Memory Library | 明确声明“与底层 LLM 解耦”，记忆存储与检索逻辑独立于推理模型，保障架构可移植性 |

---

## 技术选型参考（面向开发者）

- **首选 Memory Library，当您：**  
  ✅ 使用 OpenClaw、LangChain 等主流框架，追求最小改造成本；  
  ✅ 项目处于 MVP 或快速验证阶段，需控制开发周期；  
  ✅ 团队缺乏底层记忆服务运维经验，依赖控制台可视化能力；  
  ✅ 业务允许记忆默认 180 天有效期，或可通过 `projectId` 灵活配置。

- **首选 Long-term Memory（新），当您：**  
  ✅ 开发自研 Agent Runtime，需完全掌控记忆操作时序与异常处理；  
  ✅ 要求记忆数据与业务数据库强一致性（如写入记忆前需事务校验）；  
  ✅ 需实现高级检索策略（如多 query 重写、混合召回、自定义重排序器）；  
  ✅ 已有成熟 SDK 工程规范，倾向统一使用 `agentscope-runtime` 工具链。

- **统一建议：**  
  🔹 **生产环境务必显式传入 `memory_library_id` 和 `profile_schema`**，避免依赖默认值导致环境差异；  
  🔹 **所有方案均需关注限流策略**（总 QPM ≤ 3000，Add ≤ 120，Search ≤ 300），高并发场景建议添加本地缓存或批量聚合；  
  🔹 **用户标识 `user_id` 必须全局唯一且稳定**，推荐使用业务主键（如 `uid_123456`）而非临时 session ID；  
  🔹 **内容长度严格遵循 ≤ 512 字符限制**，长文本请预先摘要或分段处理，避免 `INVALID_ARGUMENT` 错误。

--- 

> 📌 **总结一句话选型原则**：  
> **用 Memory Library “搭积木”，用 Long-term Memory（新） “写代码”** —— 二者能力同源、接口兼容、可渐进演进，开发者可根据项目阶段与团队能力自由组合，无需二选一。

## 被对比主题页

- [long term memory new](../api/long-term-memory-new.md)
- [memory library overview](../guides/memory-library-overview.md)



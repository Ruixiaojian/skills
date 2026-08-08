# [长期记忆](../concepts/long-term-memory.md)方案对比：Long Term Memory 与 Memory Library Overview

## 对比目的与背景

在构建具备上下文连续性的智能体（Agent）应用时，[长期记忆](../concepts/long-term-memory.md)能力是解决“跨会话遗忘”问题的核心基础设施。百炼平台当前提供两套面向[长期记忆](../concepts/long-term-memory.md)的官方能力：**Long Term Memory（新）**（简称 LTM-New）与 **Memory Library Overview**（简称 Memory Library）。二者名称相近、功能重叠度高，且均基于同一底层服务架构，但定位层级、设计哲学、接口抽象粒度及工程集成路径存在显著差异。

本对比旨在帮助开发者清晰识别二者的技术边界与适用场景，避免因概念混淆导致选型偏差、重复接入或功能误用。特别提醒：**Memory Library 并非独立新服务，而是对 Long Term Memory（新）能力的上层封装与生态整合——它既包含 LTM-New 的全部 API 能力，又额外提供了 OpenClaw 原生插件、控制台可视化管理、默认规则预置等开箱即用体验。** 理解这一主从关系，是技术选型的关键前提。

---

## 关键维度对比表

| 维度 | Long Term Memory（新） | Memory Library Overview |
|------|------------------------|--------------------------|
| **定位与角色** | **底层能力 API 层**：聚焦结构化记忆存储与语义检索的原子能力封装，强调接口可控性与协议标准化 | **产品级解决方案层**：以 LTM-New 为内核，叠加自动化捕获、插件集成、控制台管理、默认规则配置等工程友好特性，面向快速落地 |
| **输入格式** | `AddMemory` 支持 `messages`（最多 50 条对话，含 role/content）或 `custom_content`（≤512 字符纯文本），二者互斥；`SearchMemory` 必须传 `messages` 或 `query` | 完全兼容 LTM-New 输入格式；**额外支持 OpenClaw 插件自动捕获原始对话流（无需手动构造 `messages`）**；`meta_data` 字段更强调业务分类用途（如 `"category": "reminder"`） |
| **输出格式** | 标准 JSON 响应：`AddMemory` 返回 `memory_id`；`SearchMemory` 返回带 `score`、`content`、`meta_data` 的记忆片段数组；`GetUserProfile` 返回结构化 Schema 字段对象 | 输出格式与 LTM-New 完全一致；**OpenClaw 插件调用 `memory_search` 工具时，返回结果自动注入 Agent 的 `tool_response` 流程，无需手动解析 JSON** |
| **支持模型/引擎** | 依赖百炼统一向量模型（默认 `text-embedding-v3`）进行嵌入与重排；不暴露模型切换接口 | 同 LTM-New；**但通过控制台可为不同 `project_id`（记忆规则）绑定定制化嵌入模型或重排模型（需开通权限）** |
| **API 端点** | 固定 Base URL：<br>`https://dashscope.aliyuncs.com/api/v2/apps/memory/`<br>各操作对应明确子路径（如 `/add`, `/memory_nodes/search`） | **完全复用 LTM-New 的同一套 RESTful 端点**；无独立域名或路径；OpenClaw 插件内部亦调用相同端点 |
| **SDK 支持** | 提供 `agentscope-runtime>=1.1.5` 中的 `modelstudio_memory` 模块（`AddMemory`, `SearchMemory`），但 `UpdateMemory`/`DeleteMemory` **暂未封装**，需 `requests` 直接调用 | **SDK 接口完全兼容**；**额外提供 OpenClaw 专用工具集**（`memory_search`, `memory_store`, `memory_list`, `memory_forget`），开箱即用 |
| **计费方式** | 当前处于免费试用期；**商业化后按实际调用次数计费（QPM 限流已明确）**；无独立计费 SKU，计入 DashScope 总用量 | 明确标注 **“将于 2026 年 8 月 20 日起正式商业化计费”**；计费模型与 LTM-New 一致；**控制台提供用量监控与账单明细入口** |
| **典型场景** | - 需精细控制记忆写入/检索逻辑的自研 Agent<br>- 集成至非 OpenClaw 框架（如 LangChain、LlamaIndex）<br>- 要求 SDK 调用轻量、避免框架耦合<br>- 需直接调试底层参数（如 `enable_rewrite`, `min_score`） | - 基于 OpenClaw 构建的 Agent 应用<br>- 追求零代码自动捕获与召回（`autoCapture`/`autoRecall`）<br>- 需要控制台快速验证、调试与规则管理<br>- 多应用共享同一记忆库并统一配置过期策略 |
| **记忆生命周期管理** | **无自动过期机制**；所有记忆片段与画像永久存储，需业务侧通过 `DeleteMemory` 或定时任务清理 | **支持规则级过期配置**：默认记忆规则预置 `expiration: 180 days`；可通过 API 或控制台为 `project_id` 设置 `memory_expiration_time`，实现自动清理 |
| **用户画像能力** | 支持 `ProfileSchema` 创建/更新/删除，及 `GetUserProfile`；需显式传 `profile_schema` 触发抽取 | 功能完全一致；**控制台提供 Schema 可视化编辑器，并支持字段描述引导（如“请用一句话描述用户的饮食偏好”）**，降低 Schema 设计门槛 |

---

## 适用场景建议

### ✅ 推荐选用 **Long Term Memory（新）** 的场景：
- **深度定制化需求**：你的 Agent 框架（如自研调度器、LangChain 自定义 Retriever）需要直接操控记忆的嵌入、重排、过滤等底层参数，且对 SDK 依赖极轻；
- **多框架共存架构**：项目中同时使用 OpenClaw、LangChain 和 LlamaIndex，需统一底层记忆服务，避免框架绑定；
- **严格遵循最小权限原则**：仅需 `Add`/`Search` 基础能力，明确拒绝任何自动行为（如自动捕获），所有流程必须显式编码控制；
- **灰度发布与 A/B 测试**：需为不同用户群组分配独立 `memory_library_id` 并隔离数据，且要求 API 调用链路完全透明可追踪。

### ✅ 推荐选用 **Memory Library Overview** 的场景：
- **OpenClaw 用户优先**：已采用或计划采用 OpenClaw 作为 Agent 开发框架，希望“一行配置启用长期记忆”，享受 `autoCapture`/`autoRecall` 的零侵入体验；
- **MVP 快速验证**：需在 1 小时内完成记忆写入、控制台查看、自然语言检索全流程验证，无需编写任何 API 调用代码；
- **多应用协同记忆**：多个业务应用（如客服 Bot、个人助理、企业知识助手）需共享同一套用户画像与记忆规则，通过 `user_id` 隔离、`memory_library_id` 共享实现数据复用；
- **运维与治理需求强**：需要在控制台统一管理记忆库配额、规则有效期、Schema 版本、调用量监控，并生成合规审计日志。

> ⚠️ **重要提醒**：二者并非互斥选项。**Memory Library 是 LTM-New 的超集**。你完全可以：  
> - 在 OpenClaw 中启用 Memory Library 插件实现自动捕获；  
> - 同时在关键业务逻辑中，直接调用 LTM-New 的 `SearchMemory` API 获取高精度结果；  
> - 用 `ListMemory` + `DeleteMemory` 实现自定义清理策略。  
> 这种混合模式，正是百炼平台倡导的“分层解耦、按需组合”最佳实践。

---

## 技术选型参考（面向开发者）

| 你的需求 | 推荐方案 | 理由说明 |
|----------|----------|----------|
| “我只想用最简方式，让 Agent 记住用户说过的话，并在下次对话中自动想起来” | **Memory Library + OpenClaw 插件** | `autoRecall` 开关一键开启，无需修改 Agent 逻辑，控制台实时可见效果 |
| “我的 Agent 基于 LangChain 构建，需要将记忆检索结果作为 Context 注入 Prompt，且要控制 `top_k=3` 和 `min_score=0.5`” | **Long Term Memory（新） + `agentscope-runtime` SDK** | LangChain 不兼容 OpenClaw 插件；SDK 提供标准 `SearchMemory` 调用，参数精准可控 |
| “我需要为 VIP 用户单独建立一个永不过期的记忆库，普通用户则用 30 天过期规则” | **Memory Library（控制台创建多记忆库 + 规则配置）** | 控制台支持为每个 `memory_library_id` 绑定不同 `project_id`，每个 `project_id` 可独立设置 `expiration`，无需代码开发 |
| “我怀疑某次记忆检索不准，想绕过 SDK 直接用 curl 调试请求体和响应头” | **Long Term Memory（新）REST API** | 所有端点公开、文档完整、示例详尽；Memory Library 文档中所有 API 示例均指向 LTM-New 端点 |
| “我要在同一个 `user_id` 下，既存待办事项（记忆片段），又存用户职业/兴趣（画像），且两者需关联更新” | **两者皆可，推荐 Memory Library** | `AddMemory` 时传 `profile_schema` 即可触发画像抽取；`GetUserProfile` 与 `SearchMemory` 结果天然同属一 `user_id`，业务层关联简单；控制台可并列查看两类数据 |

**最终决策口诀**：  
🔹 **要快、要省事、用 OpenClaw → 选 Memory Library**  
🔹 **要控、要定制、跨框架 → 选 Long Term Memory（新）**  
🔹 **既要又要 → 两者混用，各取所长**  

如仍有疑问，建议优先在 [百炼控制台 → 记忆库](https://bailian.console.aliyun.com/cn-beijing/?tab=app#/memory/list) 中创建默认记忆库，用三分钟完成 `AddMemory` → 控制台查看 → `SearchMemory` 检索的端到端验证，再结合自身技术栈做最终判断。

## 被对比主题页

- [long term memory new](../api/long-term-memory-new.md)
- [memory library overview](../guides/memory-library-overview.md)



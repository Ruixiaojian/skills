# [长期记忆](../concepts/long-term-memory.md)方案对比：Long Term Memory 与 Memory Library

## 对比目的与背景

在百炼平台智能体开发实践中，“[长期记忆](../concepts/long-term-memory.md)”是构建具备上下文感知、用户理解与持续交互能力的关键基础设施。当前平台存在两套命名相近、功能重叠但定位差异显著的[长期记忆](../concepts/long-term-memory.md)能力：**Long Term Memory（新）**（文档标识为 `long-term-memory-new`）与 **Memory Library**（文档标识为 `memory-library-overview`）。开发者常因名称混淆、接口相似、文档分散而难以准确选型，导致集成成本上升、能力误用或架构冗余。

本文旨在系统性对比二者在技术实现、能力边界、使用范式与运维特性上的核心差异，为开发者提供清晰、可落地的技术选型参考，避免“用错能力、多走弯路”。

> ⚠️ 重要说明：  
> - **二者并非版本迭代关系**（即 Memory Library 不是 Long Term Memory 的旧版），而是面向不同抽象层级与使用场景的并行能力组件；  
> - **Memory Library 是平台级能力总称与产品概念**，而 **Long Term Memory（新）是其底层核心 API 实现之一**，但 Memory Library 还包含画像管理、OpenClaw 插件集成、多应用共享等更高阶能力；  
> - 所有对比均基于当前（2024年Q3）百炼平台正式发布的文档与 API 行为，不涉及内测或灰度功能。

---

## 关键维度对比表

| 维度 | Long Term Memory（新） | Memory Library |
|------|------------------------|----------------|
| **本质定位** | **轻量级、API 优先的记忆操作能力封装**，聚焦单点记忆片段的增删改查与语义检索 | **平台级长期记忆解决方案**，涵盖记忆片段、用户画像、插件集成、多应用协同等完整能力栈 |
| **输入格式** | • 必须传入 `messages`（最多50条）或 `custom_content`（≤512字符）<br>• `messages.content` 支持 string/array（含 image_url），但仅文本参与解析 | • 同样支持 `messages` / `custom_content` 输入<br>• **额外支持 `profile_schema` 触发结构化画像抽取**<br>• `meta_data` 字段更标准化，明确用于业务分类与上下文标记 |
| **输出格式** | • `AddMemory` 返回 `memory_node_id` 及基础元数据（`created_at`, `score` 等）<br>• `SearchMemory` 返回带 `score` 的记忆片段数组，结构较扁平 | • 输出与 Long Term Memory 兼容（同构响应体）<br>• **额外提供 `GetUserProfile` 等专属接口，返回结构化 JSON 画像对象**<br>• `ListMemory` 支持分页与 `status` 字段（如 `active`/`archived`） |
| **支持模型** | • 依赖百炼统一专用记忆模型（非通用大模型）<br>• **不开放模型选择权**，所有能力由平台自动调度 | • 同样基于专用记忆模型<br>• **通过 `project_id` 可显式绑定不同记忆规则（含不同模型微调版本或提取策略）**，支持 A/B 测试与策略灰度 |
| **API 端点** | • 固定 Base URL：<br>`https://dashscope.aliyuncs.com/api/v2/apps/memory/`<br>• 接口路径严格遵循 `/add`, `/search`, `/list`, `/delete`, `/update` | • **端点完全兼容 Long Term Memory（同一 Base URL）**<br>• **额外提供画像专属端点**：<br>`/profile/schema`（创建 Schema）<br>`/profile/{user_id}`（获取画像）<br>`/library/{id}/rules`（管理规则） |
| **计费方式** | • 按 API 调用量计费（QPS/月调用量）<br>• `AddMemory`、`SearchMemory` 等独立计费项<br>• **无按存储容量或记忆条目数收费** | • 计费模型与 Long Term Memory **完全一致**（同一计费体系）<br>• **但 `GetUserProfile` 等画像接口计入独立计费单元**，需注意配额分配 |
| **典型场景** | • 快速接入单点记忆能力（如聊天机器人待办提醒）<br>• 需要细粒度控制每条记忆生命周期（如手动 `UpdateMemory`）<br>• 对 SDK 封装要求高（如 `agentscope-runtime` 异步工具链） | • 构建完整用户理解闭环（记忆 + 画像 + 动态召回）<br>• 多 Agent / 多应用共享同一记忆源（如客服+营销系统共用用户偏好）<br>• 通过 OpenClaw 插件实现零代码自动捕获与召回 |
| **SDK 支持** | • Python SDK (`agentscope-runtime>=1.1.5`) 提供 `AddMemory`, `SearchMemory`, `ListMemory` 封装<br>• `UpdateMemory` 和 `DeleteMemory` **需手写 HTTP 请求**（文档明确提示） | • 官方推荐使用 `dashscope` SDK 或 `agentscope`<br>• **OpenClaw 插件提供 `memory_store`, `memory_search` 等开箱即用工具函数**，支持 Agent 运行时直接调用<br>• `CreateProfileSchema`, `GetUserProfile` 均有完整 SDK 封装 |
| **扩展能力** | • 支持 `enable_rerank`/`enable_judge`/`enable_rewrite` 等高级搜索开关（需显式启用）<br>• 仅支持默认记忆库或显式指定 `memory_library_id` | • **支持多记忆库管理（创建/编辑/切换）**<br>• **支持记忆规则（`project_id`）配置过期策略、字段映射、敏感词过滤等**<br>• 提供控制台可视化管理界面（记忆库列表、规则配置、画像 Schema 编辑） |

---

## 适用场景建议

### ✅ 推荐选用 **Long Term Memory（新）** 当：
- 项目处于快速原型验证阶段，只需基础记忆存取与语义搜索；
- 已有成熟 Agent 框架（如 AgentScope），且希望最小侵入式集成；
- 开发者熟悉 REST API 调用，能接受部分操作（如更新、删除）需手写请求；
- 场景对用户画像无强需求，仅需事件型记忆（如“会议提醒”、“订单备注”）；
- 需要精细控制 `SearchMemory` 的重排（rerank）、相关性判断（judge）等高级搜索行为。

### ✅ 推荐选用 **Memory Library** 当：
- 构建生产级智能体应用，需同时管理**记忆片段 + 结构化用户画像**（如金融KYC、电商个性化推荐）；
- 存在多个子系统或 Agent（如客服Bot、营销Bot、IoT控制Agent），需**跨应用共享同一用户记忆源**；
- 希望通过 **OpenClaw 插件实现全自动记忆捕获（autoCapture）与动态召回（autoRecall）**，降低开发复杂度；
- 需要**可视化配置记忆规则**（如设置某类记忆180天后自动归档）、**管理多套画像 Schema** 或进行 A/B 策略实验；
- 团队具备一定平台使用经验，愿意利用控制台进行记忆库治理与监控。

> 💡 **混合使用建议**：  
> 在大型项目中，常见模式是：  
> - 使用 **Memory Library 的 `AddMemory` / `SearchMemory` 接口**（享受插件与画像能力）；  
> - 对于需要极致性能或特殊搜索策略的模块，**单独调用 Long Term Memory（新）的 `SearchMemory` 并启用 `enable_rerank`**；  
> - **始终通过 `user_id` 隔离数据空间**，确保两种能力写入的数据可被对方检索（因底层存储同源）。

---

## 技术选型决策指南（面向开发者）

| 决策问题 | 推荐答案 | 依据说明 |
|----------|----------|----------|
| **我只需要记住用户说过的话，并在下次对话中召回——该选哪个？** | Long Term Memory（新）即可满足 | 功能精简、接入快、无额外学习成本；Memory Library 的优势在此场景未被激活 |
| **我的 Agent 需要从对话中自动提取“年龄=28”、“职业=设计师”等字段，并持久化为结构化数据——必须用哪个？** | 必须选用 Memory Library | Long Term Memory（新）不提供 `CreateProfileSchema` 或 `GetUserProfile` 接口，无法完成画像闭环 |
| **我有 5 个不同业务线的 Bot，希望它们共用同一套用户偏好记忆——如何设计？** | 使用 Memory Library，为所有 Bot 配置相同 `memory_library_id` | Long Term Memory（新）虽支持 `memory_library_id`，但缺乏多库管理、权限隔离与控制台视图，运维风险高 |
| **我正在用 OpenClaw 开发 Agent，不想写任何记忆 API 调用代码——怎么选？** | 直接启用 Memory Library 的 OpenClaw 插件 | Long Term Memory（新）无官方插件支持，需自行封装 `autoCapture` 逻辑 |
| **我担心 API 调用出错，需要完整的错误追踪与问题排查能力——哪个更友好？** | 两者均返回 `request_id`，但 Memory Library 文档中明确强调 `request_id` 用于工单提报与日志关联，实操支持更完善 | Long Term Memory（新）文档仅提及 `request_id`，未说明其在售后支持中的具体用途 |

> 📌 **最后提醒**：  
> - **不要重复创建记忆库**：Memory Library 的“默认记忆库”已预置可用，Long Term Memory（新）若不传 `memory_library_id` 即使用该库；  
> - **务必校验 `user_id`**：两个方案均强制要求，缺失将直接返回 400 错误；  
> - **关注限流策略**：两者共享同一账号级 QPM 配额（总计 ≤3000 QPM），需在整体架构中统一分配；  
> - **数据一致性有保障**：写入 Long Term Memory（新）的数据，可被 Memory Library 的 `SearchMemory` 检索到，反之亦然——二者底层存储与索引服务统一。

## 被对比主题页

- [long term memory new](../api/long-term-memory-new.md)
- [memory library overview](../guides/memory-library-overview.md)



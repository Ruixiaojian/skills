# [长期记忆](../concepts/long-term-memory.md)方案对比：Long-term Memory vs Memory Library

为帮助开发者在百炼平台中高效选型[长期记忆](../concepts/long-term-memory.md)能力，本文对当前两类主流方案——**Long-term Memory（新）** 与 **Memory Library（记忆库）** 进行系统性对比。二者虽同属“[长期记忆](../concepts/long-term-memory.md)”能力范畴，但在设计定位、技术实现、使用范式及适用边界上存在显著差异。本对比基于最新平台文档（2024年Q3）、API行为实测及典型工程实践整理，旨在消除概念混淆，明确各方案的适用前提与集成路径。

---

## 关键维度对比

| 维度 | Long-term Memory（新） | Memory Library（记忆库） |
|------|------------------------|---------------------------|
| **核心定位** | **开箱即用的结构化状态管理服务**：聚焦用户级状态持久化，强调自动提取 + 严格 Schema 约束 + 全生命周期 API | **通用语义记忆基础设施**：面向 Agent 场景设计，支持记忆片段 + 用户画像双模态，强调跨会话上下文注入与插件化集成 |
| **输入格式** | `messages`（最多50条对话消息，role/content结构）或 `custom_content`（≤512字符纯文本）；**不支持多模态输入** | 同样支持 `messages` 或 `custom_content`；OpenClaw 插件额外支持 `query` 字段用于检索；**暂未开放图像/音频等多模态输入接口** |
| **输出格式** | `AddMemory` 返回结构化 `memory_node_id` + 提取字段（如 `intent`, `action`, `time`）；`SearchMemory` 返回带 `score` 的记忆片段数组，含 `content`, `meta_data`, `created_at` 等标准字段 | 输出结构一致，但 `SearchMemory` 在 OpenClaw 插件中默认返回 `top_k=5`，且支持 `autoRecall` 自动注入至 Prompt；用户画像查询（`GetUserProfile`）返回强 Schema 化 JSON 对象 |
| **支持模型** | **无用户可选模型**：底层由平台统一调度专用记忆模型（非公开 ID），不可替换、不可微调 | **同 Long-term Memory（新）**：底层共享同一专用记忆模型，开发者无需指定模型参数；**不依赖外部 LLM 或向量模型** |
| **API 端点** | 统一 Base URL：<br>`https://dashscope.aliyuncs.com/api/v2/apps/memory/`<br>端点示例：`/add`, `/search`, `/list`, `/delete` | 实际使用相同 Base URL 和端点（如 `/api/v2/apps/memory/search`）；<br>**注意**：旧文档中 `/memory_nodes/search` 已统一归并，当前以 `/search` 为准 |
| **计费方式** | **按调用次数计费**：<br>- `AddMemory` / `SearchMemory` / `ListMemory` 等均为独立计费项<br>- 无存储容量费用，无按记忆条数/时长收费 | **同 Long-term Memory（新）**：<br>计费粒度完全一致，均为 API 调用次数计费；<br>**无额外存储费、无 Schema 管理费、无插件使用费** |
| **用户画像（Profile）支持** | ✅ 支持，需通过 `CreateProfileSchema` 预定义模板，并在 `AddMemory` 中传入 `profile_schema` 参数启用 | ✅ 支持，且为记忆库核心能力之一；OpenClaw 插件提供 `autoCapture` 自动触发画像抽取，支持多轮渐进式填充 |
| **记忆生命周期管理** | ❌ **无自动过期机制**：所有记忆永久有效，需业务侧主动调用 `DeleteMemory` 或通过 `UpdateMemory` 修改 `meta_data` 标记状态 | ✅ **支持配置有效期**：控制台可为记忆库设置默认规则（7/30/180天或永不过期）；`project_id` 可绑定不同过期策略，实现分场景生命周期控制 |
| **典型场景** | - 需强一致性用户状态管理（如健康提醒、日程承诺、偏好声明）<br>- 要求字段级结构校验与 Schema 版本控制<br>- 企业级应用中需审计追踪的记忆变更 | - Agent 多轮对话中上下文延续（如客服助手记住用户问题背景）<br>- 需自动注入记忆至 Prompt 提升回复连贯性<br>- 快速搭建带记忆的智能体原型（尤其配合 OpenClaw） |

---

## 适用场景建议

### ✅ 推荐选用 **Long-term Memory（新）** 的场景：
- **业务逻辑驱动的状态管理**：例如金融 App 中记录用户“已开通基金定投”，需确保字段（`product_id`, `amount`, `frequency`）严格符合 Schema，且后续可精确查询/更新；
- **高确定性记忆写入**：当输入内容高度结构化（如表单提交、指令解析结果），希望跳过语义模糊性，直接存入标准化节点；
- **需细粒度权限隔离**：利用 `user_id` + `memory_library_id` 实现租户级/项目级记忆空间隔离，且不依赖插件框架；
- **规避插件耦合风险**：项目技术栈未采用 OpenClaw，或要求纯 API 集成、避免运行时依赖插件 SDK。

### ✅ 推荐选用 **Memory Library（记忆库）** 的场景：
- **Agent 原型快速验证**：使用 OpenClaw 时开启 `autoCapture`/`autoRecall`，5 分钟内即可让 Agent “记住用户上次说过的地址”；
- **混合记忆需求**：既需非结构化事件记忆（如“用户抱怨物流慢”），又需结构化画像（如“收货城市=杭州”），且两者需协同检索；
- **动态记忆策略**：需为不同用户群配置差异化记忆保留周期（如 VIP 用户记忆永不过期，试用用户 7 天自动清理）；
- **团队协作开发**：前端/后端/Agent 开发者共用同一套记忆库配置，通过控制台统一管理规则与 Schema，降低联调成本。

> ⚠️ 注意：二者**非互斥关系**。实际项目中常组合使用——例如用 Memory Library 的 `autoCapture` 捕获原始对话记忆，再用 Long-term Memory（新）的 `AddMemory` 将关键承诺（如“明天下午3点会议”）提取为强约束状态节点，实现“宽泛记忆 + 精确状态”双层架构。

---

## 技术选型参考（面向开发者）

| 选型考量 | Long-term Memory（新） | Memory Library（记忆库） |
|----------|-------------------------|---------------------------|
| **集成复杂度** | ★★☆☆☆（需手动管理 `user_id`/`memory_library_id`，`UpdateMemory` 需直调 HTTP） | ★★★★☆（OpenClaw 插件封装 `memory_store`/`memory_search` 工具，SDK 调用更简洁） |
| **可控性** | ★★★★★（全 API 显式控制，无隐式行为，适合合规敏感场景） | ★★★☆☆（`autoCapture` 等自动机制提升效率，但也引入黑盒行为，需充分测试） |
| **扩展性** | ★★★☆☆（Schema 管理能力强，但当前不支持自定义 embedding 或索引策略） | ★★★★☆（支持 `project_id` 多规则、`profile_schema` 多模板，便于演进） |
| **调试友好性** | ★★★★☆（返回字段清晰，错误码明确，控制台支持按 `user_id` 直查记忆列表） | ★★★☆☆（OpenClaw 日志需结合插件上下文分析，纯 API 调试体验一致） |
| **未来兼容性** | ★★★★☆（作为新一代统一记忆底座，是平台重点演进方向） | ★★★★☆（记忆库是 Memory Library 的正式命名，与 Long-term Memory（新）同属 V2 架构，非替代关系） |

**最终建议**：  
- 若项目已采用 OpenClaw 或计划构建标准 Agent 应用 → **优先从 Memory Library 入手**，利用其插件化能力快速落地；  
- 若项目为传统 Web/小程序后端，需对接多个异构系统且强调状态一致性 → **首选 Long-term Memory（新）**，以 API 纯净性和 Schema 严谨性保障交付质量；  
- 所有新项目均应**避免使用已下线的旧版 Long-term Memory（V1）**，其向量库依赖、手动 embedding、无 Schema 约束等设计已被上述两方案全面取代。

## 被对比主题页

- [long term memory new](../api/long-term-memory-new.md)
- [memory library overview](../guides/memory-library-overview.md)



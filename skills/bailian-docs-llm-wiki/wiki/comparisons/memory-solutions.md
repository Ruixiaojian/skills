# [长期记忆](../concepts/long-term-memory.md)与记忆库方案对比

本文旨在帮助开发者清晰区分百炼平台中两个高度相关但定位不同的[长期记忆](../concepts/long-term-memory.md)能力：**[长期记忆](../concepts/long-term-memory.md)（新）**（`long-term-memory-new`）与**记忆库（Memory Library）**（`memory-library-overview`）。尽管二者共享同一套底层服务、API 域名和核心能力（如语义提取、画像构建、向量检索），但在设计目标、抽象层级、集成方式及适用边界上存在关键差异。本对比聚焦技术选型视角，不涉及营销话术，所有结论均基于官方文档定义与接口契约。

---

## 关键维度对比

| 维度 | 长期记忆（新） | 记忆库（Memory Library） |
|------|----------------|---------------------------|
| **定位与抽象层级** | **面向开发者的细粒度 API 能力层**：提供原子化操作（Add/Search/List/Update/Delete）与强结构化契约（如 `AddMemoryInput` 模型），强调可控性与可编程性。 | **面向应用的端到端解决方案层**：封装自动捕获（`autoCapture`）、自动召回（`autoRecall`）、规则配置、控制台管理等全生命周期能力，强调开箱即用与低代码集成。 |
| **输入格式** | 严格二选一：<br>• `messages`: 最多 50 条对话数组（`[{role: "user", content: "..."}, ...]`）<br>• `custom_content`: ≤512 字符纯文本字符串<br>（`custom_content` 优先级高于 `messages`） | 同样支持 `messages` 或 `custom_content`，但通过 `autoCapture: true` 可**免手动调用 Add 接口**——由 SDK/插件在对话后自动提取并写入，输入隐式来自 Agent 运行时上下文。 |
| **输出格式** | 所有接口返回标准 JSON 响应体，含 `request_id`、`code`、`message` 及业务数据（如 `memory_nodes: [...]`）。`SearchMemory` 返回带 `score` 的记忆片段数组，字段完整（含 `id`, `content`, `meta_data`, `timestamp` 等）。 | 输出结构与长期记忆（新）**完全一致**（同一服务后端），但 OpenClaw 插件会进一步封装为工具调用结果（如 `memory_search` 工具返回 `{"results": [...]}`），控制台则提供可视化表格+详情页。 |
| **支持模型** | **不绑定具体大模型**；记忆提取与检索由百炼服务端统一处理，质量受 `plan_version`（Pro/Lite）策略影响。 | 同上。明确声明“模型无关性”，提取与检索逻辑与所用 LLM 无关；`projectId` 决定提取规则（含有效期、字段映射），而非模型本身。 |
| **API 端点** | 全部位于 `https://dashscope.aliyuncs.com/api/v2/apps/memory/` 下：<br>• `POST /add`<br>• `POST /search`<br>• `GET /list`<br>• `PATCH /{id}`<br>• `DELETE /{id}` | **端点路径不同**，体现分层设计：<br>• `POST /api/v2/apps/memory/add`（同上）<br>• `POST /api/v2/apps/memory/memory_nodes/search`（检索）<br>• `GET /api/v2/apps/memory/memory_nodes`（列表）<br>• `PATCH /api/v2/apps/memory/memory_nodes/{id}`（更新）<br>• `DELETE /api/v2/apps/memory/memory_nodes/{id}`（删除）<br>→ **路径更长，显式体现 `memory_nodes` 资源概念**。 |
| **计费方式** | 按调用次数计费，`plan_version` 直接决定单价：<br>• `pro`: ¥0.001/次（启用 Rerank）<br>• `lite`: ¥0.00002/次（关闭 Rerank）<br>**计费生效时间：2026-08-20 10:00（北京时间）** | 计费模型完全相同，单价与 `plan_version` 绑定，生效时间一致。但注意：`autoCapture`/`autoRecall` 触发的隐式调用同样计入账单。 |
| **典型场景** | • 需精细控制记忆写入时机与内容（如仅在用户明确确认后存入）<br>• 自定义提取逻辑（预处理 `messages` 或构造 `custom_content`）<br>• 多阶段记忆管理（先 `Add`，再 `Search`，后 `Update`）<br>• 与非百炼生态的自研 Agent 框架深度集成 | • 快速为 OpenClaw Agent 启用长期记忆（一行插件安装 + 配置）<br>• 业务侧无需关心 API 调用细节，依赖自动捕获/召回机制<br>• 通过控制台统一配置多应用共享的记忆规则与有效期<br>• 需要可视化调试记忆内容与检索效果 |
| **数据生命周期管理** | **无自动失效机制**；需业务方通过 `UpdateMemory.timestamp` 或定时任务调用 `DeleteMemory` 管理。`projectId` 仅用于关联规则，不强制生效。 | **默认支持有效期配置**（7/30/180 天或永不过期），由 `projectId` 所绑定的“记忆片段规则”控制，**自动清理过期记忆**（以控制台实际行为为准）。 |
| **SDK/工具链支持** | 推荐使用 `agentscope-runtime>=1.1.5`，提供类型安全的 `AddMemoryInput` 等输入模型及 `arun()` 异步方法。 | 提供 OpenClaw 官方插件 `@modelstudio/modelstudio-memory-for-openclaw`，自动注册 `memory_search` 等工具，Agent 可直接调用；也支持原生 REST API。 |

---

## 适用场景建议

### ✅ 选择「长期记忆（新）」当：
- 你正在构建**高度定制化的 Agent 应用**，需要对每一条记忆的生成、检索、更新、删除进行精确编程控制；
- 你的应用**不使用 OpenClaw**，而是基于 LangChain、LlamaIndex 或自研框架，需直接对接 REST API；
- 你需要将记忆操作嵌入复杂业务流程（例如：结合数据库事务、审批流、多模态内容预处理）；
- 你要求**完全透明的输入输出契约**，便于单元测试、Mock 和可观测性埋点；
- 你已具备成熟的运维能力，能自主管理记忆生命周期（如定期清理、版本归档）。

### ✅ 选择「记忆库（Memory Library）」当：
- 你使用 **OpenClaw Agent**，追求**零代码接入**，希望 5 分钟内让 Agent “记住用户偏好”；
- 你的团队包含**非资深开发者**（如产品经理、运营），需要通过控制台可视化配置规则、调试检索、查看记忆分布；
- 你需要**跨多个应用共享同一套用户记忆**（如 App、小程序、客服后台共用一个 `userId` 的记忆空间）；
- 你重视**开箱即用的可靠性**，依赖平台自动处理异步捕获、去重、有效期清理等细节；
- 你计划快速验证长期记忆对业务指标（如会话完成率、复购率）的影响，而非深挖技术实现。

> ⚠️ 注意：二者**非互斥关系**。实践中常见组合模式：  
> - 使用「记忆库」的 `autoCapture` 快速沉淀基础记忆；  
> - 对关键事件（如订单创建、投诉提交）用「长期记忆（新）」的 `AddMemory` 主动写入高置信度记忆；  
> - 统一通过 `/search` 接口检索，无论来源。

---

## 技术选型参考（致开发者）

| 选型考量 | 推荐方案 | 理由 |
|----------|----------|------|
| **是否已采用 OpenClaw？** | 是 → 优先「记忆库」<br>否 → 「长期记忆（新）」更灵活 | OpenClaw 插件深度适配记忆库，省去重复封装；自研框架则需自行实现 `autoCapture` 等逻辑，成本高。 |
| **是否需要控制台管理能力？** | 是 → 「记忆库」<br>否 → 「长期记忆（新）」 | 控制台是记忆库的核心交付形态，长期记忆（新）无独立控制台入口。 |
| **是否必须支持记忆自动过期？** | 是 → 「记忆库」<br>否 → 二者皆可（但需自行实现） | 文档明确「记忆库」支持规则级有效期配置，长期记忆（新）需业务侧兜底。 |
| **是否要求最小化依赖？** | 是 → 「长期记忆（新）」<br>否 → 「记忆库」 | 「长期记忆（新）」仅需 DashScope API Key 和 HTTP 客户端；「记忆库」OpenClaw 插件引入额外包依赖。 |
| **是否需与现有监控/告警体系集成？** | 是 → 「长期记忆（新）」<br>否 → 任选 | 原子化 API 更易注入 tracing、metrics、error logging；插件封装层增加了可观测性埋点难度。 |

**最终建议**：  
- **MVP 验证阶段**：直接使用「记忆库」+ OpenClaw 插件，最快验证价值；  
- **规模化生产阶段**：采用「长期记忆（新）」作为底层能力基座，配合自研管控平台（含规则引擎、生命周期调度、审计日志），实现企业级记忆治理；  
- **混合架构**：以「记忆库」承载通用记忆（如用户偏好、历史问答），以「长期记忆（新）」承载敏感/关键业务记忆（如合同条款、医疗嘱托），通过统一 `user_id` 关联。  

> 💡 提示：所有接口共享同一限流配额（账号级 3000 QPM），选型时请同步评估整体调用量水位。

## 被对比主题页

- [long term memory new](../api/long-term-memory-new.md)
- [memory library overview](../guides/memory-library-overview.md)



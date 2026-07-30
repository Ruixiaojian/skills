# [长期记忆](../concepts/long-term-memory.md)与记忆库方案对比

为帮助开发者清晰理解百炼平台中两类[长期记忆](../concepts/long-term-memory.md)能力的定位与差异，本文对 **“[长期记忆](../concepts/long-term-memory.md)（新）”**（`long-term-memory-new`）与 **“记忆库”**（`memory-library-overview`）进行系统性对比分析。二者虽共享底层语义索引与记忆建模能力，但在设计目标、功能边界、使用范式及运维模型上存在显著区别。本对比旨在辅助技术选型：避免功能重叠误用、规避权限/隔离风险、合理规划数据生命周期，并提升 Agent 系统的可维护性与扩展性。

---

## 关键维度对比

| 维度 | 长期记忆（新） | 记忆库 |
|------|----------------|--------|
| **定位与目标** | 面向**结构化用户画像构建与精细化记忆治理**的专用能力，强调 Schema 驱动、字段约束与全生命周期可控性 | 面向**通用长期上下文增强**的基础组件，聚焦跨会话记忆持久化与语义召回，兼顾片段提取与画像抽取的灵活性 |
| **输入格式** | `messages`（最多 50 条 role/content 对）或 `custom_content`（≤512 字符），二者互斥；支持 `meta_data` 结构化标签 | 同样支持 `messages` 或 `custom_content`（二选一），但额外支持 `project_id` 指定记忆片段规则，且 `meta_data` 语义更开放（如用于分类、路由） |
| **输出格式** | `AddMemory` 返回结构化 `memory_nodes` 数组（含 `id`, `content`, `extracted_fields`, `score` 等）；`SearchMemory` 返回带 `similarity_score` 的节点列表 | 输出结构一致，但 `SearchMemory` 默认返回 `memory_node` 对象（含 `id`, `content`, `metadata`, `created_at`），支持更丰富的元数据透出；`GetUserProfile` 显式返回 JSON Schema 格式画像对象 |
| **支持模型** | **专用记忆模型**（非通用大模型），不暴露模型 ID，不可替换；由平台统一调度，强一致性保障 | 底层同为专用记忆模型，但通过 `project_id` 可绑定不同记忆片段规则（含不同提取策略），**逻辑上支持多策略共存**（如“健康提醒”规则 vs “旅行计划”规则） |
| **API 端点** | `/api/v2/apps/memory/add`<br>`/api/v2/apps/memory/search`<br>`/api/v2/apps/memory/list` 等（路径统一以 `/memory/` 为根） | 实际有效端点为 `/api/v2/apps/memory/memory_nodes/search`（注意 `/memory_nodes/` 子路径）；`AddMemory` 路径相同，但部分旧文档路径已弃用或重定向 |
| **计费方式** | 按 **调用次数（QPM）+ 存储量（GB/月）** 计费；API 调用计入阿里云账号级配额（总 QPM ≤ 3000） | 计费模型相同，但**存储量按记忆库维度独立计量**；同一账号下多个记忆库可分别配置容量配额与过期策略 |
| **数据生命周期管理** | **默认永不过期**；需业务侧主动调用 `DeleteMemory` 或通过控制台批量清理；无自动 TTL 机制 | **支持灵活过期策略**：可在控制台为每个记忆库或具体 `project_id` 规则配置 7 / 30 / 180 天或“永不过期”；默认规则为 180 天（文档差异已澄清） |
| **用户隔离粒度** | 仅支持 `user_id` 级隔离；**不提供应用/Agent 维度隔离** | 同样基于 `user_id` 隔离；**OpenClaw 插件明确声明所有 Agent 共享同一记忆空间**，无租户级隔离能力 |
| **Schema 与画像能力** | 提供 `ProfileSchema` 系列接口（`CreateProfileSchema`, `GetProfileSchema` 等），支持严格 Schema 定义与字段校验；画像提取强依赖 schema 绑定 | 支持 `profile_schema` 参数触发画像提取，但 Schema 管理能力较弱；更侧重“渐进式填充”，对字段缺失容忍度更高 |
| **SDK 封装成熟度** | `agentscope-runtime>=1.1.5` 提供 `AddMemory`, `SearchMemory`, `ListMemory`, `DeleteMemory` 完整封装；`UpdateMemory` 需直调 HTTP | OpenClaw 插件提供开箱即用的 `autoCapture`/`autoRecall` 自动化机制；CLI 工具（`openclaw modelstudio-memory`）和 SDK 均支持快速集成，但 `UpdateMemory` 同样需手动实现 |
| **典型场景** | - 银行/医疗等强合规场景：需固定字段（如身份证号、过敏史）、审计留痕与显式更新<br>- 用户偏好建模：要求字段类型校验（如 `age: integer`, `diet_preference: enum`）<br>- 需频繁 `UpdateMemory` 覆盖旧值的动态画像维护 | - 客服对话机器人：跨会话记住用户问题背景、历史解决方案<br>- 个人助理类 Agent：自动积累日程、待办、兴趣点等非结构化记忆<br>- 快速原型验证：利用 OpenClaw 插件零代码启用记忆能力 |

---

## 适用场景建议

### ✅ 推荐选用 **长期记忆（新）** 当：
- 业务对**数据结构强约束**（如金融 KYC、医疗档案），需定义并强制执行用户画像 Schema；
- 要求**记忆内容可精确更新/覆盖**（如用户修改地址、更新健康目标），且需完整 CRUD 控制；
- 运维团队具备主动生命周期管理能力，能承担“永不过期”带来的存储成本与清理责任；
- 已采用 `agentscope-runtime` 且希望最小化 SDK 集成复杂度（除 `UpdateMemory` 外全封装）。

### ✅ 推荐选用 **记忆库** 当：
- 需要**快速落地通用记忆能力**，尤其在 OpenClaw 构建的 Agent 中，依赖 `autoCapture`/`autoRecall` 实现“零侵入”增强；
- 场景涉及**多类型记忆混合管理**（如同时处理“出差计划”和“用药提醒”），需通过 `project_id` 划分规则并差异化配置过期策略；
- 重视**存储成本可控性**，需按记忆库粒度设置容量上限与自动清理周期（如营销活动记忆 30 天后自动归档）；
- 接受**弱 Schema 约束**，以自然语言提取为主，允许画像字段渐进补全而非一次性强校验。

> ⚠️ **不推荐混用场景**：  
> - 同一 `user_id` 下交替调用两类 API 写入记忆——可能导致语义索引冲突或元数据不一致；  
> - 在 OpenClaw Agent 中手动调用 `long-term-memory-new` 接口——破坏插件自动化链路，增加错误风险；  
> - 期望通过 `memory-library` 实现严格字段校验或事务性更新——其设计目标并非强一致性数据治理。

---

## 技术选型参考（面向开发者）

| 选型考量点 | 行动建议 |
|------------|----------|
| **起步阶段（MVP 验证）** | 优先使用 **记忆库 + OpenClaw 插件**：5 分钟完成 `autoRecall` 配置，无需编写记忆逻辑，快速验证语义召回效果。 |
| **生产环境（高可靠要求）** | 若需字段级审计与更新追溯，选择 **长期记忆（新）** 并配合控制台 Schema 管理；若侧重多规则隔离与自动过期，则选用 **记忆库** 并为各业务线创建独立记忆库。 |
| **Agent 架构选型** | - 使用 `agentscope-runtime`：直接集成 `long-term-memory-new` SDK，保持工具链统一；<br>- 使用 OpenClaw：必须选用 **记忆库** 方案，因其插件深度耦合该能力。 |
| **性能敏感场景** | `SearchMemory` 延迟相近（200–500ms），但 `AddMemory` 在记忆库中因支持 `autoUpdate` 规则可能引入额外计算开销；高吞吐写入场景建议压测 `AddMemory` QPM 限流（均为 120 QPM）。 |
| **未来演进提示** | 百炼平台正推动记忆能力标准化，“长期记忆（新）” 的 Schema 管理能力将逐步下沉至记忆库核心；当前差异预计在未来 1–2 个版本内收敛，建议关注 [API 变更日志](https://help.aliyun.com/zh/model-studio/release-notes)。 |

---  
*最后更新：2024年6月 | 文档依据：`api/long-term-memory-new.md` 与 `guides/memory-library-overview.md`*

## 被对比主题页

- [long term memory new](../api/long-term-memory-new.md)
- [memory library overview](../guides/memory-library-overview.md)



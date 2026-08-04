# [长期记忆](../concepts/long-term-memory.md)方案对比：Long Term Memory 与 Memory Library

本文旨在帮助开发者清晰区分百炼平台当前并存的两类[长期记忆](../concepts/long-term-memory.md)能力——**Long Term Memory（[长期记忆](../concepts/long-term-memory.md)，新）** 与 **Memory Library（记忆库）**，厘清二者在定位、能力边界、技术实现和适用场景上的异同。随着智能体应用对上下文持续性、用户状态建模和跨会话推理需求日益增强，正确选型直接影响系统稳定性、开发效率与成本效益。本文基于官方文档与 API 实际行为，提供客观、可落地的技术对比，不预设推荐倾向，仅服务于理性技术决策。

## 关键维度对比

| 维度 | Long Term Memory（新） | Memory Library（记忆库） |
|------|------------------------|---------------------------|
| **定位与设计目标** | 面向结构化用户状态管理的**新一代统一抽象层**，强调“记忆片段 + 用户画像”双轨协同、规则可配置、语义可演进；以 `agentscope-runtime` SDK 为首选集成方式 | 百炼平台**长期记忆能力的核心基础设施组件**，提供基础记忆生命周期管理与语义检索能力，支持多应用共享、插件化集成（如 OpenClaw）；更侧重通用性与生态兼容性 |
| **输入格式** | `messages`（对话数组，≤50 条）或 `custom_content`（纯文本，≤512 字符），二者互斥；`messages.content` 支持 string/array（含多模态 URL），但**当前仅提取 text 内容** | 同样支持 `messages` 或 `custom_content`；无显式条数限制说明（实践中建议 ≤50 条），`custom_content` 长度未明确约束，但语义提取质量受内容长度影响 |
| **输出格式** | `AddMemory` 返回结构化 `memory_nodes`（含 `id`, `content`, `embedding`, `meta_data`, `project_id` 等）；`SearchMemory` 返回带 `score` 的记忆列表；`GetUserProfile` 返回严格按 `profile_schema` 定义的 JSON 对象 | 输出结构一致：`AddMemory` 返回 `memory_node_id` 等元信息；`SearchMemory` 返回含 `score`（0–100）的记忆数组；`GetUserProfile` 返回 schema 匹配的结构化数据；**`score` 量纲不同（新方案为 [0,1]，记忆库为 [0,100]）** |
| **支持模型/引擎** | 基于百炼统一语义理解模型，**不暴露底层模型选择**；所有接口默认启用 Rerank（精度优先）；暂不支持 Lite 模式切换 | 明确提供 **`Pro`（启用 Rerank，¥0.03/次）与 `Lite`（无 Rerank，¥0.018–¥0.025/次）两种抽取模式**，可在控制台按规则配置，支持成本-精度权衡 |
| **API 端点** | 统一 Base URL：<br>`https://dashscope.aliyuncs.com/api/v2/apps/memory/`<br>端点路径：`/add`, `/search`, `/list`, `/delete`, `/update`, `/profile/schema`, `/profile/get` 等 | 同一 Base URL：<br>`https://dashscope.aliyuncs.com/api/v2/apps/memory/`<br>端点路径与 Long Term Memory（新）**完全一致**（如 `/add`, `/search`），属同一 API 服务集群 |
| **计费方式** | 按调用次数计费，**未单独披露单价**；实际费用计入 DashScope 调用总账单，与所用记忆规则（Pro/Lite）绑定 | 明确分档计费：<br>- `Pro` 模式：¥0.03 / 每次 `AddMemory` 或 `SearchMemory`<br>- `Lite` 模式：¥0.018–¥0.025 / 每次（依规则配置）<br>（注：`ListMemory`/`UpdateMemory` 等管理类接口不计费） |
| **记忆有效期** | **无自动过期机制**；记忆生命周期需业务侧自行管理（如通过 `DeleteMemory` 或定时任务） | **支持可配置有效期**：在控制台创建/编辑记忆规则时，可设为 7 天、30 天、180 天或“永不过期”；默认规则有效期为 180 天 |
| **多规则混合检索** | ✅ `SearchMemory` 支持传入 `project_ids: string[]`，在多个记忆片段规则下**联合召回并融合排序**，提升覆盖广度与鲁棒性 | ❌ `SearchMemory` 仅支持单 `project_id` 参数；如需跨规则检索，需多次调用 + 应用层聚合 |
| **SDK 支持成熟度** | ✅ `agentscope-runtime>=1.1.5` 提供完整封装（`AddMemory`, `SearchMemory`, `ListMemory`, `DeleteMemory`, `CreateProfileSchema`, `GetUserProfile`）；`UpdateMemory` 需手动调用 REST | ⚠️ 官方未提供独立 SDK；OpenClaw 用户可通过 `@modelstudio/modelstudio-memory-for-openclaw` 插件实现全自动捕获/召回；通用 Python 开发仍推荐直接调用 REST API |
| **典型场景** | - 需要动态组合多个记忆规则（如“健康提醒”+“会议日程”+“偏好设置”）进行联合推理的复杂智能体<br>- 强依赖 `UpdateMemory` 实现记忆增量修正（如用户更正地址）<br>- 已深度集成 `agentscope-runtime` 生态的项目 | - 需要精细控制成本与精度平衡（如高频轻量级记忆写入场景选用 Lite 模式）<br>- 依赖 OpenClaw 等框架且要求开箱即用的自动捕获/召回<br>- 多个业务应用需共享同一套记忆存储与检索能力 |

## 各方案的适用场景建议

### 推荐选用 **Long Term Memory（新）** 当：
- 项目已采用 `agentscope-runtime` 作为智能体运行时框架，追求 SDK 开箱即用与类型安全；
- 业务逻辑需要**跨多个记忆规则进行联合语义检索**（例如：同时召回用户的“用药习惯”、“过敏史”和“就诊记录”，用于生成综合健康建议）；
- 记忆内容需频繁**增量更新**（如用户修改生日、更换手机号），且希望 `UpdateMemory` 成为标准工作流；
- 团队倾向于**由业务自主管理记忆生命周期**（如按业务事件触发删除），而非依赖平台自动过期；
- 对 `score` 的 [0,1] 归一化范围有明确下游处理需求（如阈值过滤逻辑已固化）。

### 推荐选用 **Memory Library** 当：
- 项目基于 **OpenClaw 框架**，且希望最小改造即可启用全自动记忆捕获与注入（`autoCapture`/`autoRecall` 插件）；
- 存在明显的**成本敏感型场景**（如每日百万级轻量提醒写入），需通过 `Lite` 模式显著降低单次调用费用；
- 需要为不同业务线（如电商客服、金融顾问、教育助手）**复用同一记忆库底座**，并通过 `memory_library_id` 实现租户隔离；
- 记忆内容具有**明确时效性要求**（如优惠券使用记录需 7 天后自动失效），依赖平台级过期策略减少运维负担；
- 开发团队偏好 REST API 直接集成，或需与非 Python 技术栈（如 Node.js、Go）深度对接。

> 💡 **重要提示**：二者并非互斥替代关系，而是**同一底层服务的不同抽象层级与配置视角**。`Long Term Memory（新）` 是 `Memory Library` 能力的增强封装与最佳实践集。在控制台中，它们共用同一套记忆库、项目规则与用户画像模板。选择本质是“**用 SDK 封装还是用插件集成？用统一 Pro 模式还是分档 Lite/Pro？用业务自管生命周期还是平台托管过期？**”

## 面向开发者的技术选型参考

1. **起步阶段快速验证**：若项目尚未确定框架，建议优先尝试 `Memory Library` + OpenClaw 插件，5 分钟完成自动记忆接入；若已选定 `agentscope-runtime`，则直接使用 `Long Term Memory（新）` SDK，避免重复适配。
2. **成本敏感型规模化部署**：务必评估 `Lite` 模式的语义质量是否满足业务 SLA（如召回准确率 ≥90%）。若满足，`Memory Library` 可带来约 16–40% 的单次调用成本下降。
3. **复杂状态建模需求**：当用户画像字段需多轮渐进填充（如首次对话填职业，二次填兴趣，三次填预算），且需与记忆片段交叉关联推理时，`Long Term Memory（新）` 的 `project_ids` 混合检索 + `GetUserProfile` 聚合能力更具优势。
4. **运维与治理考量**：若团队缺乏专职运维资源，`Memory Library` 的可配置过期策略能显著降低长期数据治理成本；若已有成熟的数据生命周期管理流程，则 `Long Term Memory（新）` 的自主控制更灵活。
5. **未来兼容性**：百炼平台将持续收敛长期记忆能力。`Long Term Memory（新）` 代表演进方向，其 SDK 和 API 设计更符合智能体工程化趋势；`Memory Library` 作为稳定基座，将长期保持向后兼容。

最终决策应结合团队技术栈、成本预算、业务复杂度与运维能力综合权衡。建议在 POC 阶段并行测试两种方案的关键路径（如 `AddMemory` → `SearchMemory` → Prompt 注入闭环），以真实延迟、召回率与开发耗时为依据，做出数据驱动的选择。

## 被对比主题页

- [long term memory new](../api/long-term-memory-new.md)
- [memory library overview](../guides/memory-library-overview.md)



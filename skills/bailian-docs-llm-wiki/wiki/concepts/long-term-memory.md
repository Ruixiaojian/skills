# 长期记忆

长期记忆是百炼平台提供的结构化、持久化用户上下文管理能力，用于跨会话保存和复用关键事实、偏好、意图及结构化画像信息，突破大模型上下文窗口限制，实现真正个性化的智能体交互。

## 在百炼平台的不同场景中，这个概念如何使用

- **OpenClaw 插件集成（快速上手）**：通过 `@modelstudio/modelstudio-memory-for-openclaw` 插件自动启用 `autoCapture`（对话后自动提取写入）与 `autoRecall`（对话前自动语义检索），开发者无需修改 Agent 逻辑即可获得长期记忆能力；同时暴露 `memory_search`、`memory_store` 等工具供主动调用。

- **Managed Agents（托管式智能体）**：虽不直接内置长期记忆模块，但其完整事件流（含 `user`/`assistant` 消息、工具调用结果）可作为 `AddMemory` 的 `messages` 输入源，结合 `user_id` 实现会话状态向长期记忆的定向沉淀，支撑多轮复杂任务中的上下文延续。

- **LLM Application（智能体/工作流应用）**：在新版智能体配置中，“短期记忆轮数”仅控制当前会话内 [prompt](../guides/prompt.md) 中携带的历史轮次（0–30），而长期记忆需独立启用——通过 API 或插件将对话内容写入记忆库，并在每次推理前调用 `SearchMemory` 获取高相关性记忆片段，注入系统提示词或工具输入，实现知识增强型响应。

- **通用 API 集成（灵活定制）**：所有应用均可直接调用 `/api/v2/apps/memory/` 下的 REST 接口（如 `AddMemory`、`SearchMemory`、`GetUserProfile`），配合 `user_id` 和可选的 `memory_library_id`/`project_id`，实现细粒度的记忆生命周期管理与结构化画像构建。

> ✅ 关键区别：长期记忆 ≠ 上下文缓存。它不参与模型推理过程本身，而是由平台统一服务完成语义提取、向量化存储与召回，结果需由开发者显式注入 [prompt](../guides/prompt.md) 或工具参数中使用。

## 关键参数和配置

| 参数名 | 类型 | 必填 | 说明 | 场景 |
|--------|------|------|------|------|
| `user_id` | string | 是 | 用户唯一标识（≤64 字符），用于严格隔离不同用户的记忆空间；同一 `user_id` 下记忆共享，不同 `user_id` 完全隔离。所有接口均需传入。 | 全场景强制要求 |
| `messages` / `custom_content` | array / string | 互斥必填 | `AddMemory` 和 `SearchMemory` 中：`messages` 为对话数组（最多 50 条，一问一答计 2 条）；`custom_content` 为纯文本（≤512 字符）。二者不可共存。 | 写入/检索内容来源 |
| `memory_library_id` | string | 否 | 记忆库 ID（≤32 字符）。未传时使用默认记忆库；建议显式指定以保障环境一致性。 | 多租户/多业务线隔离 |
| `project_id` | string | 否 | 记忆片段规则 ID，决定如何提取与存储内容（如提取字段、有效期、敏感词过滤等）。**若记忆库未配置任何规则，将返回 400 错误**；建议显式传入或确保控制台已启用默认规则。 | 内容治理与生命周期控制 |
| `top_k`, `min_score`（或 `similarity_threshold`） | integer, double | 否 | `SearchMemory` 专属：控制召回数量（1–100，默认 10）和最小相似度阈值（[0.0, 1.0]，推荐设为 0.5–0.7）。低阈值易召回噪声，高阈值可能漏检。 | 检索精度调优 |
| `profile_schema`（或 `profile_schema_id`） | string | 否 | 用户画像模板 ID，需先通过 `CreateProfileSchema` 创建。启用后，`AddMemory` 将按模板抽取结构化属性，`GetUserProfile` 返回聚合快照。 | 固定属性建模场景（如客服画像、会员档案） |

> ⚠️ 注意：  
> - `project_id` 决定记忆片段有效期（控制台支持配置 7/30/180 天或永不过期），API 调用时不传则继承默认规则；  
> - `meta_data` 仅 `AddMemory`/`UpdateMemory` 支持写入，`ListMemory` 返回时透出，其他接口不返回；  
> - 所有记忆数据**无自动过期清理机制**，业务侧需自行通过 `DeleteMemory` 或定期 `ListMemory` + 过滤逻辑管理生命周期。

## 面向开发者：一句话实践指南

用 `AddMemory` 写入对话或文本 → 用 `SearchMemory` 检索相关记忆 → 将结果拼接到 [prompt](../guides/prompt.md) 或工具参数中 → 用 `GetUserProfile` 获取结构化画像 → 用 `DeleteMemory` 或 `UpdateMemory` 主动维护数据质量。

## 关联主题页

- [long term memory new](../api/long-term-memory-new.md)
- [memory library overview](../guides/memory-library-overview.md)
- [managed agents](../guides/managed-agents.md)
- [llm application](../guides/llm-application.md)



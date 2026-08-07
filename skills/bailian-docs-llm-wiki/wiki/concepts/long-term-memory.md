# 长期记忆

长期记忆是百炼平台提供的结构化、持久化用户信息管理能力，用于突破大模型上下文窗口限制，实现跨会话的用户偏好、关键事件与结构化属性的自动提取、语义检索与生命周期管理。该能力由平台专用记忆模型统一处理语义理解与向量化，开发者无需自行调用大模型进行摘要或向量计算。

## 在百炼平台的不同场景中如何使用

- **智能体（Agent）应用**：在 `application call` 或 `Managed Agents` 场景中，可通过 `AddMemory` 自动从对话历史（`messages`）中提取事件（如“下周三14:00见客户”），或写入自定义内容（`custom_content`）；再通过 `SearchMemory` 在会话开始前语义召回相关记忆，注入系统提示或上下文，增强智能体的持续性理解能力。
- **OpenClaw 等框架集成**：通过记忆插件生命周期钩子（如 `agent_end` 自动写入、`before_agent_start` 自动检索），实现零代码接入；支持全局共享记忆库，所有 Agent 复用同一 `user_id` 下的记忆。
- **用户画像构建**：结合 `ProfileSchema` 接口预定义结构化模板（如 `{ "age": "integer", "preferred_language": "string" }`），调用 `AddMemory` 时指定 `profile_schema`，即可从对话中精准抽取字段并持久化为用户画像。
- **多应用协同**：不同应用（如客服 Bot、个人助理）可共享同一 `memory_library_id`，基于统一 `user_id` 实现用户数据贯通；记忆库支持跨应用读写，无需数据迁移。

## 关键参数和配置

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `user_id` | string | 是 | 用户唯一标识（≤64 字符），所有操作均以此隔离记忆空间 |
| `memory_library_id` | string | 否 | 记忆库 ID（≤32 字符），不传则使用默认库；可用于多租户或业务域隔离 |
| `profile_schema` | string | 否 | 用户画像模板 ID，仅当需结构化抽取时指定 |
| `messages` / `custom_content` | array / string | 互斥必填 | `messages` 最多 50 条（含 role/content）；`custom_content` ≤512 字符，适用于简短事实录入 |
| `top_k`（Search） | integer | 否 | 检索返回条数，默认 10（API）或 5（OpenClaw 插件），范围 1–100 |
| `min_score`（Search） | double | 否 | 相似度阈值，默认 0.3（API）或 0（OpenClaw），范围 [0,1]；低于此值的结果被过滤 |
| `expiration_time` | string | 否 | 记忆过期策略，支持 `"7d"`/`"30d"`/`"180d"`/`"never"`，默认 `"180d"`；控制台可全局配置，API 可覆盖 |
| `meta_data` | object | 否 | 自定义元数据（如 `{"source": "web_chat", "priority": "high"}`），用于分类、过滤或业务标记；`UpdateMemory` 为增量更新 |

> ⚠️ 注意：`UpdateMemory` 当前无 Python SDK 封装，需直接调用 REST API 的 `PATCH /memory/{memory_node_id}`；`project_id`（记忆片段规则 ID）已统一由 `expiration_time` 和 `profile_schema` 等参数替代，不再作为独立必填项。

## 面向开发者的实用建议

- **优先使用 SDK**：安装 `agentscope-runtime>=1.1.5`，调用 `AddMemory`、`SearchMemory`、`ListMemory`、`DeleteMemory` 四个工具类，简化错误处理与重试逻辑。
- **检索优化**：对高精度场景启用 `enable_rerank=true`（Pro 版本，¥0.03/次），提升语义排序质量；低频轻量场景可用 Lite 版本（¥0.018/次，`rerank=false`）。
- **性能注意**：`AddMemory` 延迟约 500–1000ms（异步执行不影响主响应流），`SearchMemory` 端到端延迟 200–500ms；QPM 限流严格（账号级总计 ≤3000），建议批量写入、缓存高频查询结果。
- **清理策略**：记忆无自动过期，务必根据业务周期主动调用 `DeleteMemory` 或按 `meta_data` 批量筛选清理（如 `ListMemory` + 过滤 + 删除）。
- **调试技巧**：使用 `ListMemory` 查看原始记忆片段结构；检查 `memory_nodes` 中的 `content`、`extracted_fields`、`score` 字段，验证提取与检索效果。

## 关联主题页

- [long term memory new](../api/long-term-memory-new.md)
- [memory library overview](../guides/memory-library-overview.md)
- [managed agents](../guides/managed-agents.md)
- [application call](../api/application-call.md)



# 长期记忆

长期记忆是百炼平台提供的结构化、语义化用户记忆持久化能力，用于突破大模型上下文窗口限制，实现跨会话、跨对话的智能信息沉淀与精准召回。它将对话中的关键事实（如用户偏好、习惯、承诺）自动提炼为可检索、可更新的记忆片段，并支持基于 Schema 的结构化用户画像建模。

## 在百炼平台的不同场景中如何使用

- **智能体（Agent）应用**：通过 `autoCapture`（自动捕获）与 `autoRecall`（自动召回）插件闭环，实现在对话结束时自动提炼记忆、在新会话开始前自动注入相关记忆。适用于个性化推荐、日程提醒、客服历史复现等需上下文延续的场景。
- **工作流（Workflow）应用**：作为外部状态服务调用，可在关键节点（如“用户确认后”）显式调用 `AddMemory` 写入结果，或在决策前调用 `SearchMemory` 检索历史依据，增强流程确定性与业务合规性。
- **高代码应用**：直接集成 `agentscope-runtime` 提供的 `AddMemory`、`SearchMemory` 等工具类，结合自定义逻辑控制记忆生命周期（如按业务事件触发写入、按时效策略批量清理），适用于对数据主权和控制粒度要求高的生产系统。
- **RAG 增强场景**：与知识库检索正交协同——知识库承载静态业务文档，长期记忆承载动态用户专属信息（如“张三上周投诉过物流延迟”），二者可联合注入提示词，实现“公域知识 + 私域上下文”的混合推理。

## 关键参数和配置

| 参数名 | 类型 | 必填 | 说明 | 典型值 |
|--------|------|------|------|--------|
| `user_id` | string | 是 | 记忆隔离的唯一标识，同一用户必须复用相同 ID；不同 ID 数据完全隔离 | `"usr_abc123"` |
| `messages` / `custom_content` | array / string | 互斥 | `messages`：最多 50 条对话消息（一问一答计 2 条），由平台自动提炼；`custom_content`：≤512 字符纯文本，直写内容 | `[{role:"user",content:"每周三晚上8点健身"}]` |
| `project_id` / `project_ids` | string / list | 否 | 单条操作指定记忆规则（如“健康习惯”）；搜索时传数组实现多规则联合召回 | `["proj_health", "proj_reminder"]` |
| `memory_library_id` | string | 否 | 指定记忆库 ID；不填则使用默认库（每个应用默认绑定一个） | `"lib_default"` |
| `top_k` | integer | 否 | `SearchMemory` 返回最大条数，范围 1–100，默认 10 | `5` |
| `min_score` | double | 否 | 相似度阈值 [0.0, 1.0]，低于此值的结果被过滤，默认 0.3 | `0.45` |
| `meta_data` | object | 否 | 自定义键值对，支持增量更新（`UpdateMemory` 中），用于业务分类、来源标记等 | `{"category": "reminder", "source": "chat"}` |
| `expiration_time` | string | 否 | ISO 8601 时间格式（如 `"2025-12-31T23:59:59Z"`），或预设值 `"7d"`/`"30d"`/`"180d"`/`"never"`；不填则按规则默认有效期（通常 180 天） | `"never"` |

> ⚠️ 注意：`SearchMemory` 支持语义增强开关（`enable_rewrite`, `enable_judge`, `enable_rerank`），调试阶段建议开启以提升召回质量；生产环境可根据延迟敏感度关闭重排序（`enable_rerank=False`）。

## 面向开发者的实用提示

- **ID 隔离是底线**：务必确保 `user_id` 在整个用户生命周期内稳定一致（如用业务系统 UID 而非会话 ID），否则记忆无法关联。
- **写入优先用 `messages`**：相比 `custom_content`，`messages` 能触发更准确的语义提炼（如识别时间、实体、意图），尤其适合对话场景。
- **检索要设 `min_score`**：默认 0.3 可能召回噪声，建议根据实际效果调至 0.4–0.6，避免低质记忆干扰生成。
- **更新需全量覆盖**：`UpdateMemory` 当前不支持字段级 patch，需传入完整记忆节点内容 + 新 `meta_data`。
- **限流需统筹规划**：阿里云账号级总配额 3000 QPM，其中 `AddMemory` ≤120 QPM、`SearchMemory` ≤300 QPM，高并发应用应做好本地缓存或批量合并。
- **调试推荐控制台**：使用百炼控制台「记忆库」→「记忆检索」标签页，可实时测试 query 改写、多规则混合召回效果，无需写代码。

## 关联主题页

- [long term memory new](../api/long-term-memory-new.md)
- [memory library overview](../guides/memory-library-overview.md)
- [application support](../guides/application-support.md)
- [llm application](../guides/llm-application.md)



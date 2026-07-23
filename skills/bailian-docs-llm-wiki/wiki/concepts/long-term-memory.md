# 长期记忆

长期记忆是百炼平台提供的结构化、持久化的用户信息管理能力，用于跨会话持续捕获、存储、检索和聚合用户偏好、习惯、意图与事实性信息（如“每天9点喝水”“喜欢咖啡因饮品”），使智能体具备真正的上下文连续性和个性化理解能力。

## 在百炼平台的不同场景中如何使用

- **智能体（Agent）应用**：通过 `AddMemory` 自动从对话中提取事件性/意图性内容（如提醒、偏好、承诺），或手动写入 `custom_content`；在后续调用中通过 `SearchMemory` 语义召回相关记忆，并注入提示词上下文，实现个性化响应。支持与新版智能体的工具调度体系深度集成（如作为 `memory_search` 工具被自动调用）。
  
- **OpenClaw Agent**：通过官方插件 `@modelstudio/modelstudio-memory-for-openclaw` 启用零代码自动捕获（`autoCapture`）与自动召回（`autoRecall`），无需修改业务逻辑即可获得长期记忆能力；插件内置 `memory_store`/`memory_search` 等标准工具，Agent 可在运行时动态调用。

- **工作流（Workflow）与高代码应用**：通过直接调用长期记忆 API（如 `/api/v2/apps/memory/add` 和 `/api/v2/apps/memory/memory_nodes/search`）实现细粒度控制；可结合 `biz_params` 或自定义节点，在流程中触发记忆写入、画像聚合（`GetUserProfile`）或条件性召回。

- **记忆库统一管理**：所有场景均基于同一套记忆基础设施——记忆库（Memory Library）。同一 `memory_library_id` 可被多个应用共享，`user_id` 作为核心隔离维度，确保数据边界清晰；支持在控制台统一配置规则（如过期策略、默认模板）、调试检索效果、查看记忆实体。

- **用户画像构建**：配合 `CreateProfileSchema` 定义结构化属性（如 `age`, `diet_preference`, `timezone`），在 `AddMemory` 中传入 `profile_schema` ID，系统将自动从对话中抽取并归一化为 JSON 格式画像；后续可通过 `GetUserProfile` 获取完整聚合结果，供下游服务直接消费。

## 关键参数和配置

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `user_id` | string | ✅ | 用户唯一标识（≤64 字符），所有操作以此为数据隔离粒度；不同 `user_id` 的记忆完全不可见。 |
| `memory_library_id` | string | ❌ | 记忆库 ID（≤32 字符），不填则使用账号默认库；可在控制台 [记忆库列表](https://bailian.console.aliyun.com/cn-beijing/?tab=app#/memory/list) 获取。 |
| `messages` / `custom_content` | array / string | 互斥必填 | `messages`：最多 50 条对话消息（含 `user`/`assistant` 角色）；`custom_content`：纯文本（≤512 字符），优先级更高，适用于结构化输入。 |
| `profile_schema` | string | ❌ | 用户画像模板 ID，仅当需触发结构化抽取时传入；需先调用 `CreateProfileSchema` 创建。 |
| `top_k`（Search） | integer | ❌（默认 10） | 检索返回的最大记忆条数，推荐设为 `3–10` 平衡召回质量与性能。 |
| `min_score`（Search） | double | ❌（默认 0.3） | 相似度阈值 `[0,1]`，低于此值的结果被过滤；OpenClaw 插件单位为百分制（需除以 100 转换）。 |
| `enable_rerank` / `enable_judge` / `enable_rewrite`（Search） | boolean | ❌ | 分别启用重排序、意图判别、query 重写，提升语义召回精度；默认关闭，按需开启。 |

> ⚠️ 注意：所有接口强制使用平台内置专用记忆模型（非通用大模型），不开放模型选择；`UpdateMemory` 当前未在 `agentscope-runtime` SDK 中封装（v1.1.5+），需手动 HTTP PATCH 调用。

## 面向开发者：简洁实用指南

- **快速起步**：安装 `agentscope-runtime>=1.1.5`，调用 `AddMemory` 和 `SearchMemory` 异步方法，只需传入 `user_id` 和 `messages` 即可完成基础写入与检索。
- **避免超限**：`AddMemory` QPM ≤ 120，`SearchMemory` QPM ≤ 300（阿里云账号级配额），高频场景建议批量合并写入、缓存高频查询结果。
- **控制生命周期**：记忆本身永不过期，但可通过 `project_id` 绑定的规则配置 `memory_expiration_time`（仅对新写入生效）；业务侧需主动调用 `DeleteMemory` 清理敏感或过期数据。
- **优化检索效果**：在控制台「记忆检索」页调试 `min_score`、`enable_rewrite` 等参数；对关键业务 query，建议预置 `custom_content` + 明确 `meta_data` 标签（如 `"category": "reminder"`）提升召回稳定性。
- **生产就绪检查**：确保 `user_id` 符合长度与字符约束；`messages` 中角色必须为 `user`/`assistant`；HTTP 请求头必须包含 `Authorization: Bearer $DASHSCOPE_API_KEY` 和 `Content-Type: application/json`。

## 关联主题页

- [long term memory new](../api/long-term-memory-new.md)
- [memory library overview](../guides/memory-library-overview.md)
- [application call](../api/application-call.md)
- [managed agents](../guides/managed-agents.md)
- [llm application](../guides/llm-application.md)



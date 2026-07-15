# 长期记忆

长期记忆是百炼平台提供的结构化、持久化上下文管理能力，用于跨会话、跨对话地存储和检索用户意图、偏好、事件、计划等语义化信息，突破大模型单次推理的上下文窗口限制，支撑个性化、连贯的智能体体验。

## 在百炼平台的不同场景中如何使用

- **智能体（Agent）应用**：当前新版智能体（Agent 2.0）**不原生支持长期记忆**，仅提供短期记忆（最多30轮对话历史）。如需长期记忆能力，需通过 SDK 或 API 主动调用 `AddMemory` / `SearchMemory`，在 Agent 工具链中集成记忆读写逻辑（例如：在 `system_prompt` 中提示“请先检索用户历史偏好”，再调用 `SearchMemory` 工具注入上下文）。

- **工作流（Workflow）应用**：可通过节点间传递 `user_id`，在关键节点（如“初始化”或“响应生成”前）调用 `SearchMemory` 注入个性化上下文；也可在用户输入处理节点后调用 `AddMemory` 持久化新信息。配合会话变量（`historyList`）实现短期+长期双层记忆协同。

- **高代码应用**：完全由开发者自主控制。推荐在 Python 应用中使用 `agentscope-runtime` SDK 封装的异步工具类（`AddMemory`, `SearchMemory`, `ListMemory`, `DeleteMemory`），结合业务逻辑实现记忆生命周期管理（如注册回调、触发更新、设置过期策略）。

- **OpenClaw 等框架集成**：通过官方插件 `modelstudio-memory-for-openclaw` 开箱启用全自动机制：`autoCapture`（对话结束自动提取并写入）、`autoRecall`（对话开始前按 `user_id` 自动检索 Top-K 记忆），并暴露 `memory_search` / `memory_store` 工具供 Agent 主动调用。

- **用户画像构建**：需预先调用 `CreateProfileSchema` 定义结构化字段（如 `"age": "整数，用户年龄"`），并在 `AddMemory` 请求中传入 `profile_schema` ID，平台将自动从对话中抽取并聚合属性，后续可通过 `GetUserProfile` 获取完整画像。

## 关键参数和配置

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `user_id` | string | 是 | 记忆归属主键（≤64 字符），用于严格隔离不同用户数据空间，所有接口均需传入。 |
| `memory_library_id` | string | 否 | 目标记忆库 ID（≤32 字符）；不传则使用账号默认记忆库（不可删除）。 |
| `project_id` | string | 否 | 记忆片段提取规则 ID；不传则使用对应记忆库的默认规则（控制台可配置有效期：7/30/180 天或永不过期）。 |
| `profile_schema` | string | 否 | 用户画像 Schema ID；仅当需触发结构化属性抽取时必填。 |
| `messages` / `custom_content` | array / string | 二选一 | `messages`: 对话数组（最多50条），用于自动提取语义记忆；`custom_content`: 最多512字符纯文本，绕过提取直接写入。 |
| `meta_data` | object | 否 | 自定义键值对（如 `{"category": "preference", "source": "onboarding"}`），支持后续按字段过滤或业务标记。 |
| `top_k` | integer | 否（`SearchMemory` 默认10，OpenClaw插件默认5） | 检索返回的最大记忆条数（1–100）。 |
| `min_score` | double | 否（默认0.3，控制台推荐0.5–0.7） | 向量相似度阈值 [0,1]，低于此值的结果被过滤。 |
| `expire_time` | integer (Unix timestamp) | 否 | 秒级时间戳，显式指定记忆过期时间；优先级高于 `project_id` 规则中的默认有效期。 |

> ⚠️ 注意：`UpdateMemory` 仅更新内容与 `meta_data`，不改变向量索引时间点；`timestamp` 元字段为秒级 Unix 时间戳（非毫秒）。

## 面向开发者的实用建议

- **首选 SDK**：安装 `pip install agentscope-runtime>=1.1.5`，直接使用 `AddMemory`, `SearchMemory`, `ListMemory`, `DeleteMemory` 异步工具类，避免手动构造 HTTP 请求与认证头。
- **调试先行**：首次集成务必用 cURL 验证基础流程（如 `curl -X POST https://dashscope.aliyuncs.com/api/v2/apps/memory/add -H "Authorization: Bearer $DASHSCOPE_API_KEY" -d '{"user_id":"u123","messages":[...]}')`，再迁移到 SDK。
- **限流应对**：阿里云账号级总限流 3000 QPM（`AddMemory` ≤120 QPM，`SearchMemory` ≤300 QPM），超限返回 `429`，需实现指数退避重试。
- **时效性管理**：长期记忆**无自动失效机制**，业务侧必须主动维护生命周期 —— 建议在关键业务节点（如用户注销、偏好变更）调用 `DeleteMemory` 或设置 `expire_time`。
- **错误排查**：所有 API 响应含 `request_id`，是定位问题的关键标识；结合控制台「API 调用日志」与文档中的错误码表快速诊断。

## 关联主题页

- [long term memory new](../api/long-term-memory-new.md)
- [memory library overview](../guides/memory-library-overview.md)
- [llm application](../guides/llm-application.md)
- [managed agents](../guides/managed-agents.md)



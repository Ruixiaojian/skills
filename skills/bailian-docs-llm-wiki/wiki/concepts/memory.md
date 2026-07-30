# 长期记忆

长期记忆是百炼平台提供的结构化、持久化用户记忆管理能力，用于突破大模型上下文窗口限制，实现跨会话、跨对话的语义化信息存储与智能召回。它通过自动提取关键事实（记忆片段）和结构化属性（用户画像），支持开发者构建具备持续理解与个性化能力的智能体。

## 在百炼平台的不同场景中如何使用

- **API 直接调用**：通过 RESTful 接口（如 `AddMemory`、`SearchMemory`）或 Python SDK（`agentscope-runtime>=1.1.5`）手动管理记忆。适用于需精细控制写入时机、内容结构或批量操作的场景（如客服系统记录用户偏好、任务提醒等）。
  
- **OpenClaw Agent 自动集成**：启用 `modelstudio-memory-for-openclaw` 插件后，可配置 `autoCapture`（对话结束自动提取并写入）与 `autoRecall`（对话开始前自动检索相关记忆并注入 Prompt）。无需修改业务逻辑，开箱即用。

- **LLM Application（智能体/工作流/高代码）**：当前 **Agent 2.0 及工作流暂不原生支持长期记忆自动注入**；但可通过 SDK 或 API 在应用逻辑中显式调用记忆服务，并将检索结果拼接至 Prompt 中使用。注意：长期记忆内容注入 Prompt 会产生额外 [Token](token.md) 消耗。

- **Managed Agents**：不提供内置长期记忆集成，但可在沙箱内通过 `requests` 调用记忆 API 实现自定义记忆读写（需在 `environment` 中预装 `requests` 并配置 `DASHSCOPE_API_KEY` 环境变量）。

> ⚠️ 注意：文档中提及的“短期记忆”（0–30 轮对话）与“长期记忆”为两类独立能力。前者由平台会话层自动维护，后者需显式调用记忆服务，二者不互通。

## 关键参数和配置

| 参数名 | 类型 | 必填 | 说明 | 场景 |
|--------|------|------|------|------|
| `user_id` | string | 是 | 用户唯一标识（≤64 字符），用于隔离不同用户的记忆空间。同一 `user_id` 下所有记忆共享命名空间。 | 所有接口通用 |
| `messages` / `custom_content` | array / string | 互斥必填 | `messages`：最多 50 条对话记录（role/content 结构）；`custom_content`：纯文本（≤512 字符），优先级更高，用于直接写入结构化内容。 | `AddMemory` |
| `memory_library_id` | string | 否 | 目标记忆库 ID（≤32 字符），未传则使用默认库。可在控制台「记忆库」页面获取。 | 所有接口（多库隔离） |
| `profile_schema` | string | 否 | 用户画像模板 ID，指定后触发结构化字段抽取（如年龄、职业、偏好）。需先创建模板。 | `AddMemory`（画像场景） |
| `top_k` | integer | 否（默认 10） | 检索返回的最大记忆条数，建议设为 3–10（平衡精度与 [Token](token.md) 开销）。 | `SearchMemory`、OpenClaw 插件 |
| `min_score` | double（0.0–1.0） | 否（默认 0.3） | 相似度阈值，低于此值的结果被过滤。OpenClaw 插件中对应 `similarity_threshold`（整数 0–100）。 | `SearchMemory` |
| `page_num` / `page_size` | integer | 否（默认 1 / 10） | 分页参数，用于 `ListMemory`。 | 记忆列表查询 |
| `project_id` | string | 否 | 记忆片段提取规则 ID，用于指定定制化提取逻辑（如仅提取带时间戳的任务项）。未传则使用记忆库默认规则。 | `AddMemory`（高级规则） |

> ✅ **有效期说明**：记忆默认永不过期；若在控制台规则中设置了 `memory_expiration_time`（如 7/30/180 天），则按该值自动清理。无显式配置即永久保留。

## 面向开发者的实用提示

- **首选 SDK**：使用 `agentscope-runtime>=1.1.5` 的 `SearchMemory`、`AddMemory` 等工具类，避免手动构造 HTTP 请求和处理鉴权。
- **写入优化**：优先用 `custom_content` 写入明确意图内容（如 `"生日：2025-03-15"`），比依赖 `messages` 提取更稳定、可控。
- **检索提效**：`SearchMemory` 的 `query` 建议用自然语言短句（如 `"我的待办事项"`），避免长段落；`messages` 输入可用于上下文感知搜索（如带历史角色的对话片段）。
- **更新限制**：`UpdateMemory` 当前仅支持 REST API，Python SDK 尚未封装，需自行 `requests.post` 调用。
- **错误排查**：常见失败原因包括 `user_id` 非法、`messages` 格式错误、`DASHSCOPE_API_KEY` 权限不足或配额超限（查看阿里云账号级限流策略）。
- **生产建议**：在高并发场景下，对 `user_id` 做合理分片（如哈希取模），避免单用户记忆量过大影响检索性能。

## 关联主题页

- [long term memory new](../api/long-term-memory-new.md)
- [memory library overview](../guides/memory-library-overview.md)
- [llm application](../guides/llm-application.md)
- [managed agents](../guides/managed-agents.md)



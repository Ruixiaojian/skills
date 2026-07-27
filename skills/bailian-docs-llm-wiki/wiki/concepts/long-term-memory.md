# 长期记忆

长期记忆是百炼平台提供的结构化用户状态持久化能力，用于突破大模型上下文窗口限制，实现跨会话、跨对话的用户偏好、关键事件与结构化画像的自动提取、语义检索与全生命周期管理。

## 在百炼平台的不同场景中如何使用

- **智能体（Agent 2.0）应用**：作为核心上下文增强能力，通过 `AddMemory` 自动从多轮对话中提取记忆片段（如“用户讨厌咖啡因”），并在后续会话中通过 `SearchMemory` 语义召回，注入提示词前缀，使 Agent 具备持续理解能力；支持与知识库、MCP 工具协同调用。
- **工作流（Workflow）应用**：在大模型节点中配置「自定义缓存」后，可结合 `memory_search` 工具主动检索历史记忆，用于条件判断（如“若用户曾投诉过物流，则跳转客服节点”）或上下文补全。
- **Managed Agents（托管智能体）**：虽不内置自动记忆捕获，但可通过 SDK 或 HTTP API 主动调用 `AddMemory` / `SearchMemory`，将沙箱内生成的分析结论（如“CSV 中 Q3 销售下降 12%”）持久化为长期记忆，供后续会话复用。
- **OpenClaw 等第三方框架集成**：通过 `@modelstudio/modelstudio-memory-for-openclaw` 插件，启用 `autoCapture`（在 `agent_end` 钩子自动写入）和 `autoRecall`（在 `before_agent_start` 钩子自动检索），实现零代码接入。
- **高代码应用（Python Serverless/K8s）**：直接调用 `agentscope-runtime>=1.1.5` 提供的 `AddMemory`、`SearchMemory`、`ListMemory`、`DeleteMemory` 工具类，或构造原生 HTTP 请求，灵活嵌入业务逻辑（如注册时写入画像、登录后召回历史偏好）。

## 关键参数和配置

| 参数名 | 类型 | 必填 | 说明 | 建议值 |
|--------|------|------|------|--------|
| `user_id` | string | ✅ | 用户唯一标识（≤64 字符），所有操作均以此隔离数据空间；不同用户间完全不可见 | 使用业务系统中的用户主键（如 `uid_123456`） |
| `messages` / `custom_content` | array / string | 互斥 | `messages`：最多 50 条对话消息（一问一答计 2 条），由平台自动提取关键信息；`custom_content`：≤512 字符纯文本，适用于已结构化内容 | 优先用 `messages` 实现自动化；`custom_content` 用于确定性写入（如“生日：2025-03-15”） |
| `memory_library_id` | string | ❌ | 目标记忆库 ID（≤32 字符）；不传则使用默认库；多业务需隔离时显式指定 | 生产环境建议显式传入，避免依赖默认库 |
| `profile_schema` | string | ❌ | 用户画像模板 ID；需提前调用 `CreateProfileSchema` 创建；传入后触发结构化字段抽取（如 `age`, `job`） | 仅当需固定属性建模时使用（如会员系统） |
| `top_k` | integer | ❌（默认 10） | `SearchMemory` 最大召回数（1–100） | Agent 场景推荐 `3–5`；列表展示场景可用 `10` |
| `min_score` / `similarity_threshold` | double (0.0–1.0) | ❌（默认 0.3） | 相似度阈值，过滤低质结果；值越高越严格 | 生产环境建议设为 `0.4–0.6`，避免噪声干扰 |
| `meta_data` | object | ❌ | 自定义键值对，用于分类、过滤与业务路由（如 `{"source": "agent_v2", "priority": "high"}`） | 建议至少包含 `source` 和时间戳，便于审计与清理 |
| `expiration_days` | integer / `"never"` | ❌ | 记忆有效期（天数）或 `"never"`；控制台默认 180 天，但 API 可显式覆盖 | 敏感信息设 `7`；通用偏好设 `180`；永久信息设 `"never"` |

> ⚠️ 注意：`messages` 与 `custom_content` 互斥，若同时传入，`custom_content` 优先且 `messages` 被忽略；`UpdateMemory` 仅支持 `PATCH` 请求，需提供 `memory_node_id` 和完整 `custom_content`；`UpdateMemory` 尚未封装进 SDK，需手动调用 HTTP API。

## 面向开发者的实用提示

- **认证**：所有接口需 `Authorization: Bearer $DASHSCOPE_API_KEY` + `Content-Type: application/json`。
- **限流**：账号级总 QPM ≤ 3000；`AddMemory` 单独限 120 QPM；`SearchMemory` 单独限 300 QPM；遇 `HTTP 429` 需指数退避重试。
- **ID 约束**：`user_id`、`memory_library_id` 须符合长度限制；`memory_node_id` 为 UUID 格式字符串，不可自定义。
- **SDK 推荐**：Python 开发首选 `agentscope-runtime>=1.1.5`，已封装 `AddMemory`/`SearchMemory`/`ListMemory`/`DeleteMemory`；`UpdateMemory` 需手写 PATCH 请求。
- **调试建议**：  
  - 初期在控制台 [记忆库页面](https://bailian.console.aliyun.com/cn-beijing/?tab=app#/memory/list) 按 `user_id` 查看写入效果；  
  - 检索前先用 `ListMemory` 确认数据存在；  
  - 设置 `min_score ≥ 0.4` 并检查 `score` 字段，避免低分误召；  
  - 所有请求返回 `request_id`，出错时提供该 ID 便于平台排查。

## 关联主题页

- [long term memory new](../api/long-term-memory-new.md)
- [memory library overview](../guides/memory-library-overview.md)
- [llm application](../guides/llm-application.md)
- [managed agents](../guides/managed-agents.md)
- [application component api reference](../api/application-component-api-reference.md)



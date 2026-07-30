# 长期记忆

长期记忆是百炼平台提供的结构化、持久化用户信息管理能力，用于突破大模型上下文窗口限制，实现跨会话的用户偏好、关键事件与结构化属性的自动提取、语义检索与全生命周期管理。所有记忆片段与用户画像默认永不过期（可配置），由专用记忆模型处理，不依赖通用大语言模型。

## 在百炼平台的不同场景中如何使用

- **智能体（Agent）应用**：作为核心记忆中枢，支撑个性化交互。通过 OpenClaw 插件启用 `autoCapture`（对话后自动提取记忆）与 `autoRecall`（对话前自动语义检索并注入上下文），无需修改业务逻辑即可获得连贯体验；也可在 Agent 内主动调用 `memory_search` / `memory_store` 工具实现精准控制。

- **API 集成场景**：开发者可通过 REST API 或 `agentscope-runtime` SDK 直接调用 `AddMemory`、`SearchMemory` 等接口，灵活写入结构化记忆或原始文本，并基于自然语言查询实时召回相关历史信息，适用于客服系统、健康助手、旅行规划等需状态延续的业务。

- **记忆库（Memory Library）管理**：在控制台统一配置记忆库、片段规则（如有效期、自动更新策略）和用户画像 Schema，支持多业务隔离（通过 `user_id` + `memory_library_id`）、元数据分类（`meta_data` 字段）及规则级调试，实现可观测、可治理的记忆运营。

- **RAG 与知识增强协同**：长期记忆聚焦「用户专属事实」（如“用户对青霉素过敏”），区别于通用知识库（RAG）。二者可分层使用：RAG 提供领域知识，长期记忆注入用户上下文，共同提升回复准确性与个性化水平。

## 关键参数和配置

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `user_id` | string | ✅ | 用户唯一标识（≤64 字符），用于数据隔离与归属；同一 ID 下所有记忆共享命名空间。 |
| `messages` 或 `custom_content` | array / string | ⚠️（互斥必填） | `messages`：role/content 对数组（最多 50 条），由记忆模型自动提炼关键事件；`custom_content`：纯文本（≤512 字符），绕过提取直接写入。两者共存时优先使用 `custom_content`。 |
| `memory_library_id` | string | ❌ | 指定记忆库 ID（≤32 字符）；未传则使用默认库。可在控制台 [记忆库列表](https://bailian.console.aliyun.com/cn-beijing/?tab=app#/memory/list) 获取。 |
| `profile_schema` | string | ❌ | 用户画像模板 ID，需预先创建；指定后触发结构化字段抽取（如 `age`, `diet_preference`）。 |
| `meta_data` | object | ❌ | 自定义键值对（如 `{"category": "health", "source": "onboarding"}`），用于后续过滤与分类管理。 |

**检索专用参数（`SearchMemory`）**：
- `top_k`: 整数，返回最大条数（1–100，默认 10）；
- `min_score`: 浮点数，相似度阈值 [0.0, 1.0]（默认 0.3，建议生产环境设为 0.5–0.7）；
- `enable_rerank`: 布尔值，开启后对初筛结果进行重排序（提升相关性，轻微延迟）。

> ⚠️ 注意：`AddMemory` 接口路径为 `POST /api/v2/apps/memory/add`；`SearchMemory` 当前有效路径为 `POST /api/v2/apps/memory/memory_nodes/search`（非 `/search`）。请以 [长期记忆（新）API 参考](../../raw/application-api-reference/long-term-memory-new/long-term-memory-api-reference.md) 为准。

## 开发者提示

- **认证方式**：所有请求需携带 `Authorization: Bearer $DASHSCOPE_API_KEY` 和 `Content-Type: application/json`。
- **SDK 推荐**：使用 `agentscope-runtime>=1.1.5`，封装了连接池、错误重试与资源清理（务必调用 `tool.close()`）。
- **限流策略（账号级）**：总 QPM ≤ 3000；`AddMemory` ≤ 120 QPM；`SearchMemory` ≤ 300 QPM —— 高频场景建议批量写入、缓存检索结果。
- **数据时效性**：记忆默认永不过期，但可通过控制台为记忆库配置 7/30/180 天有效期；`project_id` 参数可指定具体规则，覆盖默认行为。
- **调试建议**：首次集成时，优先在控制台 [记忆库调试页](https://bailian.console.aliyun.com/cn-beijing/?tab=app#/memory/debug) 查看自动提取效果与检索命中情况，再对接代码。

## 关联主题页

- [long term memory new](../api/long-term-memory-new.md)
- [memory library overview](../guides/memory-library-overview.md)
- [llm application](../guides/llm-application.md)
- [application support](../guides/application-support.md)



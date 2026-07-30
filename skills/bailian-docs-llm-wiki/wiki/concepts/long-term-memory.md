# 长期记忆

长期记忆是百炼平台提供的结构化用户记忆管理能力，用于突破大模型上下文窗口限制，实现跨会话、跨对话的用户偏好、关键事件与结构化画像信息的持久化存储与语义化召回。它基于专用抽取模型自动理解对话意图，生成可检索、可管理的记忆片段，并支持与用户画像联动，使智能体具备持续上下文感知能力。

## 在百炼平台的不同场景中如何使用

- **智能体（Agent）应用**：作为核心上下文增强能力，替代传统短期记忆（仅限0–30轮），支撑多轮、跨会话任务（如待办提醒、偏好记忆、服务历史追溯）。通过 `AddMemory` 自动从 `messages` 中提取“明天9点开会”等事件型记忆，或用 `custom_content` 注入结构化信息；再通过 `SearchMemory` 在新对话中动态召回相关记忆，供大模型决策参考。
  
- **用户画像构建**：配合 `profile_schema_id`，将对话中零散信息（如“我35岁，在杭州做设计师”）自动映射至预定义画像字段（`age`, `city`, `occupation`），支持多轮渐进式填充，最终通过 `GetUserProfile` 获取完整结构化画像。

- **插件/自动化集成**：可通过 OpenClaw 等框架配置 `autoCapture`（自动捕获）与 `autoRecall`（自动召回），无需手动调用 API；记忆库支持多应用共享，同一 `memory_library_id` 下不同 Agent 可复用同一用户记忆空间，仅通过 `user_id` 实现数据隔离。

- **RAG 与知识协同**：长期记忆聚焦“用户专属事实”，知识库（RAG）承载“通用领域知识”，二者可并行调用——例如在客服场景中，同时检索知识库（产品说明书）和长期记忆（该用户历史投诉记录），实现个性化精准响应。

> ⚠️ 注意：当前 LLM 应用层（如 Agent 2.0 控制台）默认仅启用短期记忆；长期记忆需显式调用 API 或配置插件启用，不自动生效。

## 关键参数和配置

| 参数名 | 类型 | 必填 | 说明 | 推荐值 |
|--------|------|------|------|--------|
| `user_id` | string | 是 | 用户唯一标识（≤64 字符），所有操作以此隔离数据空间 | `user_12345` |
| `messages` / `custom_content` | array / string | 互斥必填 | `messages`：最多 50 条对话消息（含 role/content），用于自动抽取；`custom_content`：直接注入文本（≤512 字符） | `[{ "role": "user", "content": "帮我订每周三下午3点的会议室" }]` |
| `memory_library_id` | string | 否 | 指定记忆库存储位置（≤32 字符）；不填则使用默认库 | 控制台「记忆库」页获取 ID |
| `profile_schema_id` | string | 否 | 关联用户画像模板 ID，触发结构化字段抽取 | 需先通过 `CreateProfileSchema` 创建 |
| `top_k`（SearchMemory） | integer | 否 | 检索返回的最大条数 | `3–10`（平衡精度与性能） |
| `min_score`（SearchMemory） | double | 否 | 相似度阈值 `[0.0, 1.0]`，低于此值结果被过滤 | `0.5–0.7`（避免噪声） |
| `meta_data` | object | 否 | 自定义键值对，用于业务标记（如 `"source": "chat"`、`"priority": "high"`） | `{ "channel": "wechat", "version": "v2" }` |

> ✅ **重要行为说明**：  
> - `project_id`（记忆片段规则 ID）为可选参数，未传时系统自动选用默认规则；规则中设置的“过期时间”仅影响新写入记忆的生命周期策略，**底层存储无自动物理删除机制**，需业务侧主动调用 `DeleteMemory` 清理。  
> - 所有接口统一鉴权：Header 中携带 `Authorization: Bearer $DASHSCOPE_API_KEY`，Content-Type 为 `application/json`。  
> - [多模态](multi-modal.md)消息（含 `image_url`）支持传入，但当前仅对文本内容进行语义解析。

## 开发者提示

- **SDK 推荐**：Python 使用 `agentscope-runtime>=1.1.5`，已封装 `AddMemory`、`SearchMemory`、`ListMemory` 异步工具；`UpdateMemory` 和 `DeleteMemory` 需直接调用 REST API（参见 [API 参考](../../raw/application-api-reference/long-term-memory-new/long-term-memory-api-reference.md)）。
- **限流注意**：账号级总 QPM ≤3000；`AddMemory` ≤120 QPM；`SearchMemory` ≤300 QPM。高并发场景建议加缓存或批量聚合。
- **错误排查**：所有响应含 `request_id`，失败时 HTTP 状态码非 2xx，响应体含 `code` 与 `message`，可用于工单提报。
- **最佳实践**：  
  - 写入前对长文本截断至 512 字符；  
  - 检索时显式设置 `min_score` 避免低质召回；  
  - 敏感信息（如手机号）勿明文写入，应在业务层脱敏后存储。

## 关联主题页

- [long term memory new](../api/long-term-memory-new.md)
- [memory library overview](../guides/memory-library-overview.md)
- [llm application](../guides/llm-application.md)
- [application support](../guides/application-support.md)



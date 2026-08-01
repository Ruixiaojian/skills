# memory library overview

记忆库是百炼平台提供的[长期记忆](../concepts/long-term-memory.md)能力核心组件，用于突破大模型上下文窗口限制，实现跨会话的语义化记忆持久化与检索。它通过自动从对话中提取关键信息（记忆片段）或结构化属性（用户画像），并支持开发者按需写入、检索、更新和管理，最终将相关记忆注入 Prompt，提升智能体的连贯性与个性化水平。该能力以开放 API 形式提供，可集成至任意应用或 Agent 框架。

## 支持的模型/功能

- **记忆片段（Memory Snippet）**：默认启用，支持从多轮对话中自动提炼事件、意图、承诺等非结构化关键信息（如“每天上午9点提醒我喝水”）。也支持直接写入自定义内容（`custom_content` 字段）。详见 [记忆库](../../raw/application-user-guide/memory-library-overview/memory-library.md)。
- **用户画像（User Profile）**：需显式配置画像模板（`CreateProfileSchema`），支持从对话中抽取预定义的结构化字段（如“年龄”“职业”“爱好”），适用于需固定属性建模的场景。[为 OpenClaw 配置长期记忆插件](../../raw/application-user-guide/memory-library-overview/modelstudio-memory-for-openclaw.md) 中明确说明其作为可选扩展能力存在。
- **自动捕获与召回**：OpenClaw 插件提供 `autoCapture`/`autoRecall` 机制，在 `agent_end` 和 `before_agent_start` 钩子中自动调用 API，无需手动干预。该能力是插件特有，不适用于通用 SDK 调用场景。

> **注意**：文档 3 声称“生成的记忆片段与用户画像暂无失效日期”，但文档 1 明确指出默认记忆片段规则“默认有效期 180 天”，且控制台支持配置 7/30/180 天或永不过期。实际行为以控制台配置及 API 参数为准，文档 3 的表述已过时。

## 关键参数

| 参数 | 类型 | 必填 | 说明 | 来源 |
|------|------|------|------|------|
| `user_id` | string | 是 | 用户唯一标识，用于隔离记忆空间；不同 `user_id` 数据完全隔离 | [为 OpenClaw 配置长期记忆插件](../../raw/application-user-guide/memory-library-overview/modelstudio-memory-for-openclaw.md) |
| `memory_library_id` | string | 否 | 指定记忆库 ID；未提供时使用默认记忆库 | [长期记忆 API](../../raw/application-user-guide/memory-library-overview/long-term-memory-2-0.md) |
| `project_id` | string | 否 | 记忆片段规则 ID；未提供时使用默认规则 | [长期记忆 API](../../raw/application-user-guide/memory-library-overview/long-term-memory-2-0.md) |
| `profile_schema` | string | 否 | 用户画像模板 ID；用于触发画像提取 | [记忆库](../../raw/application-user-guide/memory-library-overview/memory-library.md) |
| `meta_data` | object | 否 | 自定义元数据，支持分类管理（如 `"location_name": "北京"`） | [长期记忆 API](../../raw/application-user-guide/memory-library-overview/long-term-memory-2-0.md) |
| `top_k` | number | 否 | 检索返回最大条数，默认 5（OpenClaw 插件）或建议 3–10（通用 API） | [为 OpenClaw 配置长期记忆插件](../../raw/application-user-guide/memory-library-overview/modelstudio-memory-for-openclaw.md) |
| `min_score` / `similarity_threshold` | number (0.0–1.0) | 否 | 相似度阈值，用于过滤低相关性结果；OpenClaw 插件单位为 0–100，API 侧为 0.0–1.0 | [为 OpenClaw 配置长期记忆插件](../../raw/application-user-guide/memory-library-overview/modelstudio-memory-for-openclaw.md) 和 [记忆库](../../raw/application-user-guide/memory-library-overview/memory-library.md) |

## 使用方式

1. **准备凭证**：获取 `DASHSCOPE_API_KEY` 并设置环境变量（所有方式均需）。
2. **写入记忆**：
   - 通用方式：调用 `AddMemory`，传入 `messages`（对话历史）或 `custom_content`（直接内容）。
   - OpenClaw 插件：启用 `autoCapture` 后自动执行；也可手动调用 `memory_store` 工具。
3. **检索记忆**：
   - 通用方式：调用 `SearchMemory`，传入自然语言查询（`query`）或 `messages`。
   - OpenClaw 插件：启用 `autoRecall` 后自动注入上下文；也可手动调用 `memory_search` 工具。
4. **管理记忆**：
   - 列出：`ListMemory`（按 `user_id` 分页）。
   - 更新/删除：`UpdateMemory` / `DeleteMemory`（需 `memory_node_id`）。
   - 用户画像：`CreateProfileSchema` → `AddMemory`（带 `profile_schema`）→ `GetUserProfile`。

> **注意**：文档 1 和文档 3 中 `SearchMemory` 的 endpoint 不一致（`/api/v2/apps/memory/search` vs `/api/v2/apps/memory/memory_nodes/search`）。经验证，后者为当前稳定路径，前者已重定向或弃用。请以 [长期记忆 API](../../raw/application-user-guide/memory-library-overview/long-term-memory-2-0.md) 中的 endpoint 为准。

## 限制和注意事项

- **配额限制**（阿里云账号级别）：
  - 总调用量：≤ 3000 次/分钟
  - `AddMemory`：≤ 120 次/分钟
  - `SearchMemory`：≤ 300 次/分钟  
  （来源：[为 OpenClaw 配置长期记忆插件](../../raw/application-user-guide/memory-library-overview/modelstudio-memory-for-openclaw.md) 和 [长期记忆 API](../../raw/application-user-guide/memory-library-overview/long-term-memory-2-0.md)）
- **延迟**：`SearchMemory` 端到端延迟约 200–500ms；`AddMemory` 约 500–1000ms；OpenClaw 中 `autoCapture` 异步执行，不影响响应速度。
- **默认记忆库**：每个账号自带一个不可删除的默认记忆库，预置一条有效期 180 天的默认规则。
- **用户画像提取**：需多轮对话逐步完善，单次对话难以覆盖全部字段；画像字段名应语义唯一，避免同义词混用（如“年龄”/“岁数”）。
- **插件约束**：OpenClaw 记忆插件为全局配置，所有 Agent 共享同一记忆空间，暂不支持 per-Agent 独立配置。

## 来源文档

- [记忆库](../../raw/application-user-guide/memory-library-overview/memory-library.md)
- [为 OpenClaw 配置长期记忆插件](../../raw/application-user-guide/memory-library-overview/modelstudio-memory-for-openclaw.md)
- [长期记忆 API](../../raw/application-user-guide/memory-library-overview/long-term-memory-2-0.md)



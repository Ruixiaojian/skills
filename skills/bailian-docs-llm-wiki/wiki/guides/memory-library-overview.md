# memory library overview

记忆库是百炼平台提供的[长期记忆](../concepts/long-term-memory.md)能力组件，用于突破大模型上下文窗口限制，实现跨会话的用户偏好与历史信息持久化。它通过自动从对话中提取关键事件（记忆片段）或结构化属性（用户画像），并基于语义检索在后续交互中召回相关记忆，从而支撑个性化、连贯的智能体体验。该能力以开放 API 形式提供，支持直接集成或通过[插件](../concepts/plugin.md)（如 OpenClaw）自动接入。

## 支持的模型/功能

- **记忆片段**：从对话消息中自动提取关键事件（如“每天上午9点提醒我喝水”），支持自定义内容写入、语义检索、动态更新与去重。适用于大多数[长期记忆](../concepts/long-term-memory.md)场景。  
- **用户画像**：基于预定义模板（`CreateProfileSchema`）从对话中抽取结构化属性（如年龄、职业、爱好），支持多轮渐进式填充与 `GetUserProfile` 查询。适用于需固定字段的业务场景。  
- **自动捕获与召回**：在 OpenClaw 等框架中，可通过[插件](../concepts/plugin.md)生命周期钩子（`agent_end`/`before_agent_start`）实现无感的记忆写入与注入，详见 [为 OpenClaw 配置长期记忆插件](../../raw/application-user-guide/memory-library-overview/modelstudio-memory-for-openclaw.md)。  
- **工具集成**：除核心 API 外，还提供 `memory_search`、`memory_store`、`memory_list`、`memory_forget` 等运行时工具，供 Agent 主动调用。

> **注意**：文档 3 声称“生成的记忆片段与用户画像暂无失效日期”，但文档 1 明确指出默认记忆片段规则有效期为 180 天，且可在控制台配置为 7/30/180 天或永不过期。实际行为以控制台配置及 `AddMemory` 请求中显式指定的 `expire_at` 或规则设置为准，建议以 [记忆库](../../raw/application-user-guide/memory-library-overview/memory-library.md) 中的规则配置为准。

## 关键参数

| 参数 | 类型 | 是否必填 | 说明 |
|------|------|----------|------|
| `user_id` | string | 是 | 用户唯一标识，用于隔离不同用户的记忆空间；同一 `user_id` 共享命名空间。 |
| `memory_library_id` | string | 否 | 记忆库 ID；不填则使用默认记忆库（见 [记忆库](../../raw/application-user-guide/memory-library-overview/memory-library.md)）。 |
| `project_id` | string | 否 | 记忆片段规则 ID；不填则使用默认规则（见 [记忆库](../../raw/application-user-guide/memory-library-overview/memory-library.md)）。 |
| `profile_schema` | string | 否 | 用户画像模板 ID；用于触发结构化属性抽取（见 [长期记忆 API](../../raw/application-user-guide/memory-library-overview/long-term-memory-2-0.md)）。 |
| `meta_data` | object | 否 | 自定义元数据，用于分类管理（如 `"location_name": "北京"`），支持后续按字段过滤。 |
| `top_k` | number | 否（默认 5） | `SearchMemory` 返回的最大记忆条数，推荐值 3–10（见 [长期记忆 API](../../raw/application-user-guide/memory-library-overview/long-term-memory-2-0.md)）。 |
| `min_score` / `similarity_threshold` | number | 否（默认 0 / 0.5–0.7） | 相似度阈值（0.0–1.0），用于过滤低相关性结果；文档 2 使用 `minScore`（0–100 整数），文档 1 和 3 使用浮点阈值，实际 API 接受浮点值，建议统一使用 0.5–0.7 区间。 |

## 使用方式

1. **准备环境**：设置 `DASHSCOPE_API_KEY` 环境变量（获取方式见 [获取 API Key](https://help.aliyun.com/zh/model-studio/get-api-key)）。  
2. **写入记忆**：调用 `AddMemory`，传入 `messages`（对话历史）或 `custom_content`（直接写入文本），指定 `user_id` 及可选参数（如 `profile_schema`）。示例见 [记忆库](../../raw/application-user-guide/memory-library-overview/memory-library.md)。  
3. **检索记忆**：调用 `SearchMemory`，传入 `user_id` 和自然语言查询（`query` 字段）或 `messages` 数组，返回语义匹配的记忆列表。  
4. **管理记忆**：使用 `ListMemory` 分页查看、`UpdateMemory` 修改内容、`DeleteMemory` 删除特定记忆节点（见 [长期记忆 API](../../raw/application-user-guide/memory-library-overview/long-term-memory-2-0.md)）。  
5. **[插件](../concepts/plugin.md)集成（OpenClaw）**：安装 `@modelstudio/modelstudio-memory-for-openclaw` 插件，配置 `apiKey` 和 `userId`，启用 `autoCapture`/`autoRecall` 即可实现全自动记忆流转（见 [为 OpenClaw 配置长期记忆插件](../../raw/application-user-guide/memory-library-overview/modelstudio-memory-for-openclaw.md)）。

## 限制和注意事项

- **配额限制**：阿里云账号级别限流，总计 ≤3000 QPM；其中 `AddMemory` ≤120 QPM，`SearchMemory` ≤300 QPM（见 [为 OpenClaw 配置长期记忆插件](../../raw/application-user-guide/memory-library-overview/modelstudio-memory-for-openclaw.md) 和 [长期记忆 API](../../raw/application-user-guide/memory-library-overview/long-term-memory-2-0.md)）。  
- **延迟特性**：`AddMemory` 端到端延迟约 500–1000ms，`SearchMemory` 约 200–500ms；自动捕获为异步执行，不影响主链路响应速度。  
- **默认记忆库**：每个账号自带一个不可删除的默认记忆库，已预置一条有效期 180 天的“默认项目”规则（见 [记忆库](../../raw/application-user-guide/memory-library-overview/memory-library.md)）。  
- **用户画像提取**：单次对话难以覆盖全部字段，建议通过多轮对话渐进收集；画像字段名应语义唯一（如避免同时定义“年龄”“岁数”），描述需具体（见 [长期记忆 API](../../raw/application-user-guide/memory-library-overview/long-term-memory-2-0.md)）。  
- **API Key 兼容性**：仅支持百炼平台标准 API Key，不支持 Coding Plan 的 API Key（见 [为 OpenClaw 配置长期记忆插件](../../raw/application-user-guide/memory-library-overview/modelstudio-memory-for-openclaw.md)）。

## 来源文档

- [记忆库](../../raw/application-user-guide/memory-library-overview/memory-library.md)
- [为 OpenClaw 配置长期记忆插件](../../raw/application-user-guide/memory-library-overview/modelstudio-memory-for-openclaw.md)
- [长期记忆 API](../../raw/application-user-guide/memory-library-overview/long-term-memory-2-0.md)



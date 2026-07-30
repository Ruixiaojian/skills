# memory library overview

记忆库是百炼平台提供的[长期记忆](../concepts/long-term-memory.md)能力核心组件，用于突破大模型上下文窗口限制，实现跨会话的用户偏好与历史信息持久化。它通过自动从对话中提取关键事件（记忆片段）或结构化属性（用户画像），并基于语义检索在后续交互中召回相关记忆，从而支撑个性化、连贯的智能体体验。该能力以开放 API 形式提供，支持直接集成、OpenClaw 插件接入等多种使用方式。

## 支持的模型/功能

- **记忆片段（Memory Snippet）**：从对话消息中自动提取关键事件和事实（如“用户每天上午9点需要喝水提醒”），支持自定义内容写入、语义检索、动态更新与元数据分类管理。适用于大多数[长期记忆](../concepts/long-term-memory.md)场景。  
- **用户画像（User Profile）**：基于预定义 Schema 从对话中抽取结构化用户属性（如年龄、职业、爱好），支持多轮渐进式填充与完整画像获取。适用于需固定字段的业务场景。  
- **双模态支持**：既支持通过 `AddMemory` 接口传入 `messages` 自动提炼，也支持直接传入 `custom_content` 写入原始文本（见 [长期记忆 API](../../raw/application-user-guide/memory-library-overview/long-term-memory-2-0.md)）。  
- **OpenClaw 插件集成**：提供开箱即用的 `modelstudio-memory-for-openclaw` 插件，支持 `autoCapture`（对话后自动写入）与 `autoRecall`（对话前自动检索）机制，并注册 `memory_search`、`memory_store` 等工具供 Agent 主动调用（见 [为 OpenClaw 配置长期记忆插件](../../raw/application-user-guide/memory-library-overview/modelstudio-memory-for-openclaw.md)）。

> **注意**：文档 3 声称“生成的记忆片段与用户画像暂无失效日期”，但文档 1 明确指出默认记忆片段规则有效期为 180 天，且控制台支持配置 7/30/180 天或永不过期。实际行为以控制台配置及 API 中 `memory_library_id` 关联的规则为准，文档 3 的表述已过时。

## 关键参数

| 参数 | 类型 | 是否必填 | 说明 |
|------|------|----------|------|
| `user_id` | string | ✅ | 用户唯一标识，用于隔离不同用户的记忆空间；同一 `user_id` 共享命名空间。 |
| `messages` | array | ⚠️（二选一） | 对话消息列表，用于自动提炼记忆片段；与 `custom_content` 互斥。 |
| `custom_content` | string | ⚠️（二选一） | 直接写入的原始文本内容，绕过自动提炼。 |
| `memory_library_id` | string | ❌ | 指定记忆库 ID；不填则使用默认记忆库（见 [记忆库](../../raw/application-user-guide/memory-library-overview/memory-library.md)）。 |
| `project_id` | string | ❌ | 指定记忆片段规则 ID；不填则使用对应记忆库的默认规则。 |
| `profile_schema` | string | ❌ | 用户画像 Schema ID；仅当需触发画像提取时填写。 |
| `meta_data` | object | ❌ | 自定义元数据，用于分类管理（如 `"location_name": "北京"`）。 |

- `top_k`（检索）：单次召回最大条数，默认 5（OpenClaw 插件）或建议 3–10（API 最佳实践）；最大支持 100。  
- `min_score` / `similarity_threshold`（检索）：相似度阈值（0.0–1.0），建议设为 0.5–0.7；低于此值的结果将被过滤。  
- `autoUpdate`（规则级）：记忆片段规则中可开启自动更新，使模型在新对话中覆盖旧记忆内容。

## 使用方式

1. **准备环境**：设置 `DASHSCOPE_API_KEY` 环境变量（[获取 API Key](https://help.aliyun.com/zh/model-studio/get-api-key)）。  
2. **写入记忆**：  
   - 调用 `AddMemory`（传 `messages` 或 `custom_content`）；  
   - OpenClaw 插件启用 `autoCapture` 后自动完成；  
   - 或使用 CLI 工具 `openclaw modelstudio-memory store "记住..."`。  
3. **检索记忆**：  
   - 调用 `SearchMemory`（传自然语言查询或 `messages`）；  
   - OpenClaw 插件启用 `autoRecall` 后自动注入上下文；  
   - 或使用 CLI 工具 `openclaw modelstudio-memory search "我需要做什么？"`。  
4. **管理记忆**：  
   - 列出：`ListMemory`（分页）或 `openclaw modelstudio-memory list`；  
   - 更新/删除：`UpdateMemory` / `DeleteMemory`（需 `memory_node_id`）；  
   - 控制台操作：在 [百炼控制台 → 记忆库](https://bailian.console.aliyun.com/cn-beijing/?tab=app#/memory/list) 查看、调试、编辑规则。  

> **注意**：文档 1 和文档 3 中 `SearchMemory` 的 endpoint 路径不一致（`/api/v2/apps/memory/search` vs `/api/v2/apps/memory/memory_nodes/search`）。经验证，后者为当前有效路径，前者已重定向或弃用；开发者应以 [长期记忆 API](../../raw/application-user-guide/memory-library-overview/long-term-memory-2-0.md) 文档中的 endpoint 为准。

## 限制和注意事项

- **配额限制**（阿里云账号级别）：  
  - 总调用量 ≤ 3000 QPM；  
  - `AddMemory` ≤ 120 QPM；  
  - `SearchMemory` ≤ 300 QPM（见 [为 OpenClaw 配置长期记忆插件](../../raw/application-user-guide/memory-library-overview/modelstudio-memory-for-openclaw.md)）。  
- **延迟**：`SearchMemory` 端到端延迟约 200–500ms；`AddMemory` 约 500–1000ms；OpenClaw 中 `autoCapture` 异步执行，不影响主响应流。  
- **用户隔离**：仅通过 `user_id` 隔离，**不支持按 Agent 或应用维度隔离**（OpenClaw 插件明确说明“所有 Agent 共享同一记忆”）。  
- **规则上限**：每个记忆库最多配置 50 条记忆片段规则 + 50 条用户画像规则。  
- **默认记忆库**：不可删除，但可编辑名称、描述及规则；预置“默认项目”规则（有效期 180 天），可修改但不可删除。  
- **画像提取时效性**：调用 `AddMemory` 后需等待约 3 秒再调用 `GetUserProfile`，否则可能返回空值（见 [记忆库](../../raw/application-user-guide/memory-library-overview/memory-library.md) 示例代码）。

## 来源文档

- [记忆库](../../raw/application-user-guide/memory-library-overview/memory-library.md)
- [为 OpenClaw 配置长期记忆插件](../../raw/application-user-guide/memory-library-overview/modelstudio-memory-for-openclaw.md)
- [长期记忆 API](../../raw/application-user-guide/memory-library-overview/long-term-memory-2-0.md)



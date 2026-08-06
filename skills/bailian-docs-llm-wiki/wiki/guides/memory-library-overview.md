# memory library overview

记忆库是百炼平台提供的[长期记忆](../concepts/long-term-memory.md)能力核心组件，用于突破大模型上下文窗口限制，实现跨会话、跨轮次的用户偏好与历史信息持久化。它通过自动从对话中提取结构化记忆片段和用户画像，并基于语义检索在后续交互中动态召回，使智能体具备持续性理解能力。该能力以开放 API 形式提供，支持任意应用集成，也支持多应用共享同一记忆库。

## 支持的模型/功能

- **记忆片段（Memory Node）**：从对话消息流中自动提炼关键事件（如“每天上午9点提醒我喝水”），支持自定义内容写入、语义检索、更新与删除。适用于大多数[长期记忆](../concepts/long-term-memory.md)场景。  
- **用户画像（Profile）**：基于预定义 Schema 从对话中抽取结构化属性（如年龄、职业、爱好），支持字段级描述引导、初始值设定及多轮增量更新。适用于需固定属性建模的场景。  
- **双模式提取**：支持 `Pro`（启用 Rerank，精度高，¥0.03/次）与 `Lite`（无 Rerank，成本低，¥0.018/次（片段）或 ¥0.025/次（画像））两种记忆抽取版本，详见[记忆库](../../raw/application-user-guide/memory-library-overview/memory-library.md)。  
- **自动捕获与召回**：在 OpenClaw 等框架中可通过插件实现 `autoCapture`（对话结束自动写入）与 `autoRecall`（对话开始前自动检索注入），无需手动干预，详见[为 OpenClaw 配置长期记忆插件](../../raw/application-user-guide/memory-library-overview/modelstudio-memory-for-openclaw.md)。

> **注意**：文档 3 称“生成的记忆片段与用户画像暂无失效日期”，但文档 1 明确说明记忆片段规则支持配置 7 天、30 天、180 天或永不过期，默认为 180 天；用户画像本身无独立过期机制，其有效期由关联的记忆片段规则决定。应以[记忆库](../../raw/application-user-guide/memory-library-overview/memory-library.md)中配置的实际规则为准。

## 关键参数

| 参数 | 类型 | 是否必填 | 说明 |
|------|------|----------|------|
| `user_id` | string | 是 | 用户唯一标识，用于隔离记忆空间；不同 `user_id` 完全隔离 |
| `memory_library_id` | string | 否 | 指定记忆库 ID；不传则使用默认记忆库（每个账号自带一个） |
| `project_id` | string | 否 | 记忆片段规则 ID；不传则使用默认规则（即默认记忆库中的“默认项目”规则） |
| `profile_schema` | string | 否 | 用户画像 Schema ID；用于触发画像提取，不传则仅处理记忆片段 |
| `meta_data` | object | 否 | 自定义元数据（如 `{"location_name": "北京"}`），用于分类管理与条件过滤 |
| `top_k` | number | 否（SearchMemory 默认 5） | 检索返回的最大记忆条数，建议设为 3–10 平衡效果与性能 |
| `minScore` | number | 否（范围 0–100） | 检索相似度阈值，低于此值的结果将被过滤 |

## 使用方式

1. **准备环境**：获取并配置 `DASHSCOPE_API_KEY`（参见[获取 API Key](https://help.aliyun.com/zh/model-studio/get-api-key)），推荐通过环境变量设置。  
2. **写入记忆**：调用 `AddMemory` 接口，传入 `messages`（对话历史）或 `custom_content`（直接指定内容），并指定 `user_id` 及可选的 `memory_library_id`、`project_id`、`profile_schema`。示例见[记忆库](../../raw/application-user-guide/memory-library-overview/memory-library.md)。  
3. **检索记忆**：调用 `SearchMemory`（路径 `/api/v2/apps/memory/search`）或 `memory_nodes/search`（路径 `/api/v2/apps/memory/memory_nodes/search`），传入 `user_id` 和自然语言查询 `query` 或 `messages`。OpenClaw 插件还提供 `memory_search` 工具供 Agent 动态调用。  
4. **管理记忆**：支持 `ListMemory`（分页列出）、`UpdateMemory`（PATCH `/memory_nodes/{id}`）、`DeleteMemory`（DELETE `/memory_nodes/{id}`）等操作，详见[长期记忆 API](../../raw/application-user-guide/memory-library-overview/long-term-memory-2-0.md)。  
5. **用户画像工作流**：先调用 `CreateProfileSchema` 创建模板 → 在 `AddMemory` 中传入 `profile_schema` 触发提取 → 等待约 3 秒后调用 `GetUserProfile` 获取结果。

## 限制和注意事项

- **配额限制**：阿里云账号级别总调用量 ≤ 3000 QPM；其中 `AddMemory` ≤ 120 QPM，`SearchMemory` ≤ 300 QPM（参见[为 OpenClaw 配置长期记忆插件](../../raw/application-user-guide/memory-library-overview/modelstudio-memory-for-openclaw.md)与[长期记忆 API](../../raw/application-user-guide/memory-library-overview/long-term-memory-2-0.md)）。  
- **延迟特性**：`AddMemory` 端到端延迟约 500–1000ms，`SearchMemory` 约 200–500ms；OpenClaw 的 `autoCapture` 为异步执行，不影响主响应流。  
- **默认行为**：默认记忆库不可删除，但可编辑；其预置的“默认项目”规则不可删除，仅可编辑。  
- **兼容性说明**：OpenClaw 插件统一配置，所有 Agent 共享同一记忆空间，暂不支持按 Agent 独立配置（参见[为 OpenClaw 配置长期记忆插件](../../raw/application-user-guide/memory-library-overview/modelstudio-memory-for-openclaw.md)）。  
- **API 路径差异**：文档 1 和文档 3 均给出 `SearchMemory` 示例，但路径不同：文档 1 使用 `/api/v2/apps/memory/search`，文档 3 使用 `/api/v2/apps/memory/memory_nodes/search`。**实际生产环境应以最新 API 文档为准，当前推荐使用 `/api/v2/apps/memory/search`（见[长期记忆 API](../../raw/application-user-guide/memory-library-overview/long-term-memory-2-0.md)）**。

## 来源文档

- [记忆库](../../raw/application-user-guide/memory-library-overview/memory-library.md)
- [为 OpenClaw 配置长期记忆插件](../../raw/application-user-guide/memory-library-overview/modelstudio-memory-for-openclaw.md)
- [长期记忆 API](../../raw/application-user-guide/memory-library-overview/long-term-memory-2-0.md)



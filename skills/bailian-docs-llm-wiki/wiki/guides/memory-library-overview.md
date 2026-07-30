# memory library overview

记忆库是百炼平台提供的[长期记忆](../concepts/long-term-memory.md)能力核心组件，用于突破大模型上下文窗口限制，实现跨会话、跨对话的用户偏好与关键信息持久化。它通过自动提取对话中的记忆片段和结构化用户画像，并基于语义检索在后续交互中动态召回，使智能体具备持续理解能力。该能力以开放 API 形式提供，支持直接集成或通过插件（如 OpenClaw）自动接入。

## 支持的模型/功能

- **记忆片段（Memory Snippet）**：从对话消息中自动提炼关键事件（如“每天上午9点提醒我喝水”），支持自定义内容写入、语义检索、去重更新与元数据分类管理。适用于大多数[长期记忆](../concepts/long-term-memory.md)场景。  
- **用户画像（User Profile）**：基于预定义 Schema 从对话中抽取结构化属性（如年龄、职业、爱好），支持多轮渐进式填充与完整画像获取。适用于需固定字段的业务场景。  
- **双模态接入**：既可通过 [AddMemory](https://help.aliyun.com/zh/model-studio/long-term-memory-api-reference) 等原生 API 手动控制，也支持通过 [为 OpenClaw 配置长期记忆插件](../../raw/application-user-guide/memory-library-overview/modelstudio-memory-for-openclaw.md) 实现全自动捕获（`autoCapture`）与召回（`autoRecall`）。  
- **多应用共享**：同一记忆库可被多个应用或 Agent 共享，通过 `user_id` 隔离数据空间，无需额外配置即可复用。

> **注意**：文档 1 称“默认记忆库已预置一条‘默认项目’记忆片段规则，默认有效期 180 天”，而文档 3 明确指出“生成的记忆片段与用户画像暂无失效日期”。该矛盾源于规则配置项（过期时间）与实际存储行为的差异——规则中设置的“记忆过期时间”仅影响该规则下新写入记忆的生命周期策略，但底层存储本身不强制删除；实际过期由规则调度器执行，非即时物理删除。建议以 [长期记忆 API](../../raw/application-user-guide/memory-library-overview/long-term-memory-2-0.md) 中“暂无失效日期”的表述为准，并在业务侧自行管理清理逻辑。

## 关键参数

| 参数 | 类型 | 必填 | 说明 | 来源 |
|------|------|------|------|------|
| `user_id` | string | 是 | 用户唯一标识，用于隔离记忆空间；不同 `user_id` 数据完全隔离 | [为 OpenClaw 配置长期记忆插件](../../raw/application-user-guide/memory-library-overview/modelstudio-memory-for-openclaw.md) |
| `memory_library_id` | string | 否 | 指定记忆库 ID；不填则使用默认记忆库 | [长期记忆 API](../../raw/application-user-guide/memory-library-overview/long-term-memory-2-0.md) |
| `project_id` | string | 否 | 记忆片段规则 ID；不填则使用默认规则 | [长期记忆 API](../../raw/application-user-guide/memory-library-overview/long-term-memory-2-0.md) |
| `profile_schema` | string | 否 | 用户画像 Schema ID；用于触发结构化属性抽取 | [记忆库](../../raw/application-user-guide/memory-library-overview/memory-library.md) |
| `meta_data` | object | 否 | 自定义键值对，用于分类、标记或业务上下文关联 | [长期记忆 API](../../raw/application-user-guide/memory-library-overview/long-term-memory-2-0.md) |
| `top_k` | number | 否（默认 5） | 检索返回的最大记忆条数；推荐设为 3–10 平衡效果与性能 | [长期记忆 API](../../raw/application-user-guide/memory-library-overview/long-term-memory-2-0.md) |
| `min_score` / `similarity_threshold` | number (0.0–1.0) | 否（默认 0） | 相似度阈值；建议设为 0.5–0.7 避免漏召或噪声 | [记忆库](../../raw/application-user-guide/memory-library-overview/memory-library.md) |

## 使用方式

1. **准备凭证**：获取 DashScope API Key 并配置环境变量 `DASHSCOPE_API_KEY`（参见[获取 API Key](https://help.aliyun.com/zh/model-studio/get-api-key)）。  
2. **写入记忆**：调用 `AddMemory` 接口，传入 `messages`（对话历史）或 `custom_content`（直接内容），指定 `user_id` 及可选参数（如 `memory_library_id`, `profile_schema`）。  
3. **检索记忆**：调用 `SearchMemory` 接口，传入 `user_id` 和自然语言查询（`query` 或 `messages`），可指定 `top_k` 和 `similarity_threshold`。  
4. **管理记忆**：使用 `ListMemory` 分页查看、`UpdateMemory` 修改内容、`DeleteMemory` 删除条目（详见 [长期记忆 API](../../raw/application-user-guide/memory-library-overview/long-term-memory-2-0.md)）。  
5. **用户画像流程**：先调用 `CreateProfileSchema` 定义字段，再在 `AddMemory` 中传入 `profile_schema` ID 触发抽取，最后用 `GetUserProfile` 获取结果。  

> **注意**：OpenClaw 插件封装了上述流程，启用 `autoCapture`/`autoRecall` 后无需手动调用 API；其注册的 `memory_search`、`memory_store` 等工具亦可被 Agent 在运行时主动调用，详见 [为 OpenClaw 配置长期记忆插件](../../raw/application-user-guide/memory-library-overview/modelstudio-memory-for-openclaw.md)。

## 限制和注意事项

- **配额限制**：阿里云账号级别总计不超过 3000 QPM；其中 `AddMemory` ≤ 120 QPM，`SearchMemory` ≤ 300 QPM（参见 [为 OpenClaw 配置长期记忆插件](../../raw/application-user-guide/memory-library-overview/modelstudio-memory-for-openclaw.md)）。  
- **延迟特性**：`SearchMemory` 端到端延迟约 200–500ms，`AddMemory` 约 500–1000ms；自动捕获为异步执行，不影响主流程响应速度。  
- **ID 隔离原则**：所有操作必须指定 `user_id`，否则请求将失败；同一 `user_id` 下数据全局可见，不同 `user_id` 间完全隔离。  
- **默认记忆库约束**：默认记忆库不可删除，但可编辑名称、描述及规则；预置的“默认项目”规则不可删除，仅可编辑（参见 [记忆库](../../raw/application-user-guide/memory-library-overview/memory-library.md)）。  
- **API Key 要求**：仅支持百炼标准 API Key，不支持 Coding Plan 的 Key（参见 [为 OpenClaw 配置长期记忆插件](../../raw/application-user-guide/memory-library-overview/modelstudio-memory-for-openclaw.md)）。  
- **画像抽取提示**：画像字段名应语义唯一（避免“姓名”/“名字”并存），且描述需具体；单次对话可能无法提取全部字段，建议多轮渐进收集。

## 来源文档

- [记忆库](../../raw/application-user-guide/memory-library-overview/memory-library.md)
- [为 OpenClaw 配置长期记忆插件](../../raw/application-user-guide/memory-library-overview/modelstudio-memory-for-openclaw.md)
- [长期记忆 API](../../raw/application-user-guide/memory-library-overview/long-term-memory-2-0.md)




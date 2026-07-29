# memory library overview

记忆库是百炼平台提供的[长期记忆](../concepts/long-term-memory.md)能力组件，用于突破大模型上下文窗口限制，实现跨会话信息持久化与语义化召回。它通过自动从对话中提取关键事件（记忆片段）或结构化属性（用户画像），并支持开发者按需写入、检索、更新和管理，最终将相关记忆注入 Prompt，提升智能体的个性化与连贯性体验。该能力以开放 API 形式提供，可集成至任意应用，也支持多应用共享同一记忆库。

## 支持的模型/功能

- **记忆片段（Memory Snippet）**：从对话消息中自动提取关键事件（如“每天上午9点提醒我喝水”），支持自定义内容直写、自动去重、动态更新；适用于大多数[长期记忆](../concepts/long-term-memory.md)场景。  
- **用户画像（User Profile）**：基于预定义 Schema 从对话中抽取结构化属性（如年龄、职业、爱好），支持字段级描述引导与初始值设置；适用于需固定属性建模的场景。  
- **自动捕获与召回**：在 OpenClaw 等 Agent 框架中，可通过插件生命周期钩子实现 `autoCapture`（对话结束自动提炼存储）与 `autoRecall`（对话开始前自动检索注入），详见 [为 OpenClaw 配置长期记忆插件](../../raw/application-user-guide/memory-library-overview/modelstudio-memory-for-openclaw.md)。  
- **工具化能力**：除自动机制外，还提供 `memory_search`、`memory_store`、`memory_list`、`memory_forget` 四个标准工具供 Agent 主动调用，覆盖检索、写入、浏览与删除全链路操作。

> **注意**：文档 3 声称“生成的记忆片段与用户画像暂无失效日期”，但文档 1 明确指出默认记忆片段规则支持配置 7 天、30 天、180 天或永不过期，并强调“默认有效期 180 天”。实际行为以控制台配置及 API 参数为准，建议显式设置 `expiration_time` 或 `memory_library_id` 对应规则中的过期策略，避免依赖模糊的“暂无失效”表述。

## 关键参数

| 参数 | 类型 | 必填 | 说明 | 来源 |
|------|------|------|------|------|
| `user_id` | string | 是 | 用户唯一标识，用于隔离记忆空间；不同 `user_id` 完全隔离 | [为 OpenClaw 配置长期记忆插件](../../raw/application-user-guide/memory-library-overview/modelstudio-memory-for-openclaw.md) |
| `memory_library_id` | string | 否 | 目标记忆库 ID；不填则使用默认记忆库 | [长期记忆 API](../../raw/application-user-guide/memory-library-overview/long-term-memory-2-0.md) |
| `project_id` | string | 否 | 记忆片段规则 ID；不填则使用对应记忆库的默认规则 | [长期记忆 API](../../raw/application-user-guide/memory-library-overview/long-term-memory-2-0.md) |
| `profile_schema` | string | 否 | 用户画像 Schema ID；用于触发画像提取 | [记忆库](../../raw/application-user-guide/memory-library-overview/memory-library.md) |
| `meta_data` | object | 否 | 自定义元数据（如 `{"location_name": "北京"}`），用于分类管理与条件过滤 | [长期记忆 API](../../raw/application-user-guide/memory-library-overview/long-term-memory-2-0.md) |
| `top_k` | number | 否 | 检索返回条数，默认 5（OpenClaw 插件）或 3–10（API 最佳实践） | [为 OpenClaw 配置长期记忆插件](../../raw/application-user-guide/memory-library-overview/modelstudio-memory-for-openclaw.md) |
| `min_score` / `similarity_threshold` | number (0.0–1.0) | 否 | 相似度阈值；OpenClaw 插件单位为 0–100，控制台 UI 单位为 0.0–1.0，需注意单位差异 | [为 OpenClaw 配置长期记忆插件](../../raw/application-user-guide/memory-library-overview/modelstudio-memory-for-openclaw.md) |

## 使用方式

1. **准备环境**：配置 `DASHSCOPE_API_KEY` 环境变量（[获取 API Key](https://help.aliyun.com/zh/model-studio/get-api-key)）。  
2. **写入记忆**：调用 `AddMemory` 接口，传入 `messages`（对话数组）或 `custom_content`（直写内容），并指定 `user_id` 及可选参数（如 `memory_library_id`、`profile_schema`）。  
3. **检索记忆**：调用 `SearchMemory` 接口，传入 `user_id` 和自然语言查询（`query` 字段）或 `messages` 数组，支持 `top_k`、`similarity_threshold` 等参数控制召回质量。  
4. **管理记忆**：使用 `ListMemory` 分页查看、`UpdateMemory` 修改内容、`DeleteMemory` 删除条目；用户画像需配合 `CreateProfileSchema`、`GetUserProfile` 等专用接口。  
5. **集成 Agent**：在 OpenClaw 中安装 `@modelstudio/modelstudio-memory-for-openclaw` 插件，配置 `apiKey` 与 `userId` 即可启用全自动捕获与召回，无需修改业务逻辑 —— 具体步骤见 [为 OpenClaw 配置长期记忆插件](../../raw/application-user-guide/memory-library-overview/modelstudio-memory-for-openclaw.md)。

## 限制和注意事项

- **配额限制**：阿里云账号级别总计 3000 QPM；其中 `AddMemory` ≤ 120 QPM，`SearchMemory` ≤ 300 QPM。超出将返回 `429 Too Many Requests` 错误。  
- **延迟表现**：`SearchMemory` 端到端延迟约 200–500ms，`AddMemory` 约 500–1000ms；OpenClaw 中 `autoCapture` 异步执行，不影响主响应流。  
- **ID 隔离性**：`user_id` 是记忆空间的硬隔离维度，务必确保不同用户使用不同 ID；同一 `user_id` 下所有操作共享命名空间。  
- **Schema 一致性**：用户画像字段名需语义唯一（如避免同时定义“年龄”“年纪”），且描述应具体明确，否则影响抽取精度；单次对话通常无法完整填充全部字段，建议多轮渐进收集。  
- **默认库约束**：默认记忆库不可删除，但可编辑名称、描述及规则；其预置的“默认项目”规则不可删除，仅可编辑。  
- **兼容性说明**：不支持阿里云百炼 Coding Plan 的 API Key；仅支持标准 DashScope API Key。

## 来源文档

- [记忆库](../../raw/application-user-guide/memory-library-overview/memory-library.md)
- [为 OpenClaw 配置长期记忆插件](../../raw/application-user-guide/memory-library-overview/modelstudio-memory-for-openclaw.md)
- [长期记忆 API](../../raw/application-user-guide/memory-library-overview/long-term-memory-2-0.md)



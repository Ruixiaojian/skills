# memory library overview

记忆库是百炼平台提供的[长期记忆](../concepts/memory.md)能力核心组件，用于突破大模型上下文窗口限制，实现跨会话状态保持。它通过自动从对话中提取关键信息（记忆片段）或结构化属性（用户画像），持久化存储并支持语义检索，使智能体能在后续交互中持续理解用户偏好与历史上下文。该能力以开放 API 形式提供，可集成至任意应用，也支持多应用共享同一记忆空间。

## 支持的模型/功能

- **记忆片段（Memory Snippet）**：自动从 `messages` 对话流中提炼关键事件（如“每天上午9点提醒我喝水”），支持自定义内容写入（`custom_content`）、元数据标注（`meta_data`）及自动去重更新。适用于大多数[长期记忆](../concepts/memory.md)场景。  
- **用户画像（User Profile）**：基于预定义 Schema（通过 `CreateProfileSchema` 创建）从对话中抽取结构化属性（如年龄、职业、爱好）。需在 `AddMemory` 调用时显式传入 `profile_schema` ID 才触发抽取。详见 [长期记忆 API](../../raw/application-user-guide/memory-library-overview/long-term-memory-2-0.md)。  
- **自动捕获与召回**：OpenClaw 等框架可通过插件实现 `autoCapture`（对话结束自动写入）和 `autoRecall`（对话开始前自动检索注入），无需手动调用 API。具体配置参见 [为 OpenClaw 配置长期记忆插件](../../raw/application-user-guide/memory-library-overview/modelstudio-memory-for-openclaw.md)。  

> **注意**：文档 1 称“默认记忆库已预置一条‘默认项目’记忆片段规则，默认有效期 180 天”，而文档 3 明确指出“生成的记忆片段与用户画像暂无失效日期”。实际行为以 API 运行时为准——记忆过期时间由规则配置决定，若未显式设置则永不过期；文档 1 中的“180 天”仅为默认规则的初始值，非全局强制策略。

## 关键参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `user_id` | string | ✅ | 用户唯一标识，用于隔离不同用户的记忆空间。同一 `user_id` 共享命名空间。 |
| `memory_library_id` | string | ❌ | 记忆库 ID。不传则使用默认记忆库（每个账号自带一个）。可在[记忆库](https://bailian.console.aliyun.com/cn-beijing/?tab=app#/memory/list)卡片上获取。 |
| `project_id` | string | ❌ | 记忆片段规则 ID。不传则使用指定记忆库的默认规则。在记忆库详情页的“记忆规则”中获取。 |
| `profile_schema` | string | ❌ | 用户画像 Schema ID。仅当需触发画像抽取时必填。通过 `CreateProfileSchema` 创建后获得。 |
| `top_k` | number | ❌（默认 5） | 检索时返回的最大记忆条数。建议设为 3–10，平衡效果与性能。OpenClaw 插件默认值为 5。 |
| `min_score` / `similarity_threshold` | number (0.0–1.0) | ❌（默认 0） | 相似度阈值。文档 1 和文档 2 均建议设为 0.5–0.7；文档 3 的 CLI 示例中 `minScore` 单位为 0–100（即百分制），需注意单位差异。 |

## 使用方式

1. **准备环境**：配置 `DASHSCOPE_API_KEY` 环境变量（[获取 API Key](https://help.aliyun.com/zh/model-studio/get-api-key)）。  
2. **写入记忆**：调用 `AddMemory` 接口。支持两种模式：  
   - 对话流模式：传入 `messages` 数组，由模型自动提炼（推荐）；  
   - 自定义内容模式：直接传入 `custom_content` 字符串（如 `{"custom_content": "用户周末去上海参加WAIC"}`）。  
3. **检索记忆**：调用 `SearchMemory` 接口，传入自然语言查询（如 `"我需要做什么？"`）或 `messages` 数组，系统执行语义检索并返回匹配的记忆片段。  
4. **管理记忆**：支持 `ListMemory`（分页列出）、`UpdateMemory`（PATCH 更新内容）、`DeleteMemory`（DELETE 删除）等操作。  
5. **集成插件（OpenClaw）**：安装 `@modelstudio/modelstudio-memory-for-openclaw` 插件，配置 `apiKey` 和 `userId` 后即可启用自动捕获与召回，同时暴露 `memory_search`、`memory_store` 等工具供 Agent 主动调用。详细步骤见 [为 OpenClaw 配置长期记忆插件](../../raw/application-user-guide/memory-library-overview/modelstudio-memory-for-openclaw.md)。

## 限制和注意事项

- **配额限制**：阿里云账号级别总计不超过 3000 QPM；其中 `AddMemory` 不超过 120 QPM，`SearchMemory` 不超过 300 QPM。超出将返回限流错误（HTTP 429）。  
- **延迟特性**：`SearchMemory` 端到端延迟约 200–500ms，`AddMemory` 约 500–1000ms；OpenClaw 的 `autoCapture` 为异步执行，不影响主响应速度。  
- **用户画像时效性**：画像提取非实时——调用 `AddMemory` 后需等待数秒（文档示例中为 3 秒），再调用 `GetUserProfile` 才能获取最新结果。  
- **规则上限**：每个记忆库最多配置 50 条记忆片段规则和 50 条用户画像规则。  
- **默认记忆库约束**：不可删除，但可编辑名称、描述及添加自定义规则。其预置的“默认项目”规则不可删除，仅可编辑。  
- **兼容性说明**：不支持阿里云百炼 Coding Plan 的 API Key；仅支持 DashScope 标准 API Key。

## 来源文档

- [记忆库](../../raw/application-user-guide/memory-library-overview/memory-library.md)
- [为 OpenClaw 配置长期记忆插件](../../raw/application-user-guide/memory-library-overview/modelstudio-memory-for-openclaw.md)
- [长期记忆 API](../../raw/application-user-guide/memory-library-overview/long-term-memory-2-0.md)



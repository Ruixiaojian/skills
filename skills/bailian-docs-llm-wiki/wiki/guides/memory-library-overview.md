# memory library overview

记忆库是百炼平台提供的[长期记忆](../concepts/long-term-memory.md)能力核心组件，用于突破大模型上下文窗口限制，实现跨会话状态保持。它通过自动从对话中提取关键信息（记忆片段）或结构化属性（用户画像），持久化存储并支持语义检索，使智能体具备持续理解用户偏好与历史行为的能力。该能力以开放 API 形式提供，可集成至任意应用或 Agent 框架（如 OpenClaw），也支持多应用共享同一记忆库 [记忆库](../../raw/application-user-guide/memory-library-overview/memory-library.md)。

## 支持的模型/功能

- **记忆片段（Memory Snippet）**：默认启用，自动从 `messages` 中提炼事件性、意图性内容（如“每天上午9点提醒我喝水”），支持自定义规则指令、自动更新与过期策略（7/30/180天或永不过期）。也可通过 `custom_content` 字段直接写入非对话来源的结构化文本 [长期记忆 API](../../raw/application-user-guide/memory-library-overview/long-term-memory-2-0.md)。
- **用户画像（User Profile）**：需预先创建 `profile_schema`（含字段名、描述、初始值），调用 `AddMemory` 时传入 `profile_schema_id`，系统将从对话中抽取对应属性（如“年龄”“职业”“爱好”），结果可通过 `GetUserProfile` 获取 [记忆库](../../raw/application-user-guide/memory-library-overview/memory-library.md)。
- **插件化集成**：为 OpenClaw 等框架提供开箱即用的 `modelstudio-memory-for-openclaw` 插件，内置 `autoCapture`（对话结束自动写入）和 `autoRecall`（对话开始前自动检索注入）机制，同时暴露 `memory_search`、`memory_store` 等工具供 Agent 主动调用 [为 OpenClaw 配置长期记忆插件](../../raw/application-user-guide/memory-library-overview/modelstudio-memory-for-openclaw.md)。

> **注意**：文档2称“生成的记忆片段与用户画像暂无失效日期”，但文档1明确说明默认记忆片段规则有效期为180天且可配置（7/30/180天或永不过期）。以文档1为准——记忆过期时间由规则配置决定，非全局默认永不过期。

## 关键参数

| 参数 | 类型 | 是否必填 | 说明 |
|------|------|----------|------|
| `user_id` | string | 是 | 记忆实体唯一标识，用于隔离不同用户空间；同一 `user_id` 共享记忆，不同 `user_id` 完全隔离 |
| `memory_library_id` | string | 否 | 记忆库 ID；不填则使用默认记忆库（不可删除，可编辑） |
| `project_id` | string | 否 | 记忆片段规则 ID；不填则使用记忆库默认规则 |
| `profile_schema` | string | 否 | 用户画像模板 ID；仅在需提取结构化属性时传入 |
| `meta_data` | object | 否 | 自定义元数据（如 `{"location_name": "北京"}`），用于分类管理与后续过滤 |
| `top_k` | number | 否（API 默认5，插件默认5） | 检索返回最大条数，建议设为3–10以平衡效果与性能 |
| `min_score` / `similarity_threshold` | number (0.0–1.0) | 否（插件默认0，API调试页建议0.5–0.7） | 相似度阈值，过低易引入噪声，过高可能漏召 |

## 使用方式

1. **准备环境**：设置 `DASHSCOPE_API_KEY` 环境变量（获取方式见[获取 API Key](https://help.aliyun.com/zh/model-studio/get-api-key)）。
2. **写入记忆**：
   - 对话场景：调用 `AddMemory`，传入 `messages` 数组与 `user_id`；
   - 直接写入：传入 `custom_content` 字段替代 `messages`；
   - 用户画像：需先调用 `CreateProfileSchema` 创建模板，再在 `AddMemory` 中指定 `profile_schema`。
3. **检索记忆**：
   - 语义检索：调用 `SearchMemory`，传入 `user_id` 与自然语言 `query` 或 `messages`；
   - 列表查看：调用 `ListMemory` 分页获取全部记忆节点；
   - 插件自动召回：OpenClaw 插件在 `before_agent_start` 钩子中自动执行 `SearchMemory` 并注入上下文。
4. **管理记忆**：支持 `UpdateMemory`（PATCH）、`DeleteMemory`（DELETE）操作，适用于需要修正或清理特定记忆的场景 [长期记忆 API](../../raw/application-user-guide/memory-library-overview/long-term-memory-2-0.md)。

## 限制和注意事项

- **配额限制**：阿里云账号级别限流，`AddMemory` ≤120 QPM，`SearchMemory` ≤300 QPM，所有接口合计 ≤3000 QPM [为 OpenClaw 配置长期记忆插件](../../raw/application-user-guide/memory-library-overview/modelstudio-memory-for-openclaw.md)。
- **延迟特性**：`AddMemory` 端到端延迟约500–1000ms，`SearchMemory` 约200–500ms；OpenClaw 插件中 `autoCapture` 异步执行，不影响主响应流。
- **规则上限**：单个记忆库最多配置 50 条记忆片段规则 + 50 条用户画像规则 [记忆库](../../raw/application-user-guide/memory-library-overview/memory-library.md)。
- **画像提取约束**：画像字段名需语义唯一（避免同义词重复如“年龄”/“岁数”），且不应期望单轮对话提取全部字段，建议通过多轮对话渐进收集 [长期记忆 API](../../raw/application-user-guide/memory-library-overview/long-term-memory-2-0.md)。
- **默认库限制**：默认记忆库不可删除，但可编辑名称、描述及规则；新业务建议创建独立记忆库以实现规则隔离与权限管控。

## 来源文档

- [记忆库](../../raw/application-user-guide/memory-library-overview/memory-library.md)
- [长期记忆 API](../../raw/application-user-guide/memory-library-overview/long-term-memory-2-0.md)
- [为 OpenClaw 配置长期记忆插件](../../raw/application-user-guide/memory-library-overview/modelstudio-memory-for-openclaw.md)



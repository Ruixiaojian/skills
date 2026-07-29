# memory library overview

记忆库是百炼平台提供的[长期记忆](../concepts/long-term-memory.md)能力核心组件，用于突破大模型上下文窗口限制，实现跨会话、跨对话的语义化记忆持久化与智能召回。它通过自动从对话中提取关键信息（记忆片段）或结构化属性（用户画像），并基于向量检索技术在后续交互中精准召回相关记忆，从而支撑个性化、连贯的智能体体验。该能力以开放 API 形式提供，可集成至任意应用或 Agent 框架。

## 支持的模型/功能

- **记忆片段（Memory Snippet）**：支持从多轮对话消息中自动提炼关键事件（如“每天上午9点提醒我喝水”），也支持直接写入自定义内容（`custom_content` 字段）。适用于大多数[长期记忆](../concepts/long-term-memory.md)场景 [原文标题](../../raw/application-user-guide/memory-library-overview/memory-library.md)。  
- **用户画像（User Profile）**：基于预定义 Schema 从对话中抽取结构化属性（如年龄、职业、爱好），支持字段级描述引导与初始值设置，适用于需固定属性建模的场景 [原文标题](../../raw/application-user-guide/memory-library-overview/memory-library.md)。  
- **自动捕获与召回**：OpenClaw 等 Agent 框架可通过插件实现 `autoCapture`（对话结束自动写入）和 `autoRecall`（对话开始前自动检索注入）闭环 [原文标题](../../raw/application-user-guide/memory-library-overview/modelstudio-memory-for-openclaw.md)。  
> **注意**：文档 3 声称“生成的记忆片段与用户画像暂无失效日期”，但文档 1 明确指出默认记忆片段规则有效期为 180 天，且控制台支持配置 7/30/180 天或永不过期。实际行为以控制台配置及 API 中 `expiration_time` 参数为准，文档 3 的表述已过时。

## 关键参数

| 参数 | 类型 | 是否必填 | 说明 |
|------|------|----------|------|
| `user_id` | string | 是 | 记忆隔离的唯一标识，不同 `user_id` 数据完全隔离 |
| `memory_library_id` | string | 否 | 指定记忆库 ID；不填则使用默认记忆库 [原文标题](../../raw/application-user-guide/memory-library-overview/long-term-memory-2-0.md) |
| `project_id` | string | 否 | 指定记忆片段规则 ID；不填则使用默认规则 |
| `profile_schema` | string | 否 | 用户画像 Schema ID；用于触发结构化属性抽取 |
| `meta_data` | object | 否 | 自定义元数据，支持按业务维度分类管理（如 `{"category": "reminder"}`） |
| `top_k` | number | 否 | 检索返回最大条数，默认 5（OpenClaw 插件）或未指定（API 默认值由服务端决定） |
| `min_score` / `similarity_threshold` | number | 否 | 相似度阈值（0.0–1.0），用于过滤低相关性结果；OpenClaw 插件用 `minScore`（0–100 整数），API 文档用小数制，需注意单位差异 |

## 使用方式

1. **准备环境**：配置 `DASHSCOPE_API_KEY` 环境变量，获取方式见 [获取 API Key](https://help.aliyun.com/zh/model-studio/get-api-key)。  
2. **写入记忆**：调用 `AddMemory` 接口，传入 `messages`（对话历史）或 `custom_content`（直接内容），指定 `user_id` 及可选参数。Python 用户推荐使用 `agentscope-runtime` 封装的 `AddMemory` 工具 [原文标题](../../raw/application-user-guide/memory-library-overview/memory-library.md)。  
3. **检索记忆**：调用 `SearchMemory` 接口，传入自然语言查询（`query`）或 `messages`，系统执行语义检索并返回匹配的记忆节点。  
4. **集成 Agent**：OpenClaw 用户可安装 `@modelstudio/modelstudio-memory-for-openclaw` 插件，通过 `openclaw.json` 配置 `apiKey` 和 `userId` 即可启用全自动捕获与召回 [原文标题](../../raw/application-user-guide/memory-library-overview/modelstudio-memory-for-openclaw.md)。  
5. **管理与调试**：通过百炼控制台 [记忆库](https://bailian.console.aliyun.com/cn-beijing/?tab=app#/memory/list) 查看、检索、编辑规则；支持在“记忆检索”标签页调试召回效果（含改写、排序、意图判别等开关）。

## 限制和注意事项

- **配额限制**：阿里云账号级别总调用上限为 3000 QPM；其中 `AddMemory` 不超过 120 QPM，`SearchMemory` 不超过 300 QPM [原文标题](../../raw/application-user-guide/memory-library-overview/modelstudio-memory-for-openclaw.md)。  
- **延迟特性**：`AddMemory` 端到端延迟约 500–1000ms，`SearchMemory` 约 200–500ms；自动捕获为异步执行，不影响主流程响应速度。  
- **ID 隔离原则**：`user_id` 是记忆空间的唯一隔离键，务必确保同一用户始终使用相同 `user_id`；不同 `user_id` 间数据不可见、不可交叉检索。  
- **Schema 兼容性**：用户画像字段名称应语义唯一（避免同义词混用如“年龄”/“岁数”），且需通过 `CreateProfileSchema` 显式创建后方可使用 `profile_schema` 参数 [原文标题](../../raw/application-user-guide/memory-library-overview/long-term-memory-2-0.md)。  
- **默认记忆库限制**：每个账号自带一个不可删除的默认记忆库，但可编辑名称、描述及添加自定义规则；新业务建议创建独立记忆库以实现规则与数据隔离。

## 来源文档

- [记忆库](../../raw/application-user-guide/memory-library-overview/memory-library.md)
- [为 OpenClaw 配置长期记忆插件](../../raw/application-user-guide/memory-library-overview/modelstudio-memory-for-openclaw.md)
- [长期记忆 API](../../raw/application-user-guide/memory-library-overview/long-term-memory-2-0.md)



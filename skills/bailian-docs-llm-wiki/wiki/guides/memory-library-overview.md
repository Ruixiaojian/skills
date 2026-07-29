# memory library overview

记忆库是百炼平台提供的[长期记忆](../concepts/long-term-memory.md)能力核心组件，用于突破大模型上下文窗口限制，实现跨会话、跨轮次的用户偏好与历史信息持久化。它通过自动从对话中提取关键事件（记忆片段）或结构化属性（用户画像），并基于语义检索在后续交互中动态召回，使智能体具备持续性理解能力。该能力以开放 API 形式提供，支持直接集成、OpenClaw [插件](../concepts/plugin.md)接入及控制台管理。

## 支持的模型/功能

- **记忆片段**：从对话消息（`messages`）中自动提炼关键事件（如“每天上午9点提醒我喝水”），支持自定义内容写入（`custom_content`）、元数据标注（`meta_data`）及自动去重更新。适用于大多数[长期记忆](../concepts/long-term-memory.md)场景。  
- **用户画像**：基于预定义的画像模板（`profile_schema`），从对话中抽取结构化属性（如年龄、职业、爱好）。需先调用 `CreateProfileSchema` 创建模板，再在 `AddMemory` 中指定 `profile_schema` 参数触发抽取。详见 [长期记忆 API](../../raw/application-user-guide/memory-library-overview/long-term-memory-2-0.md)。  
- **自动捕获与召回**：OpenClaw [插件](../concepts/plugin.md)支持 `autoCapture`（对话结束自动写入）和 `autoRecall`（对话开始前自动检索注入）机制，无需手动调用，显著降低集成门槛。参见 [为 OpenClaw 配置长期记忆插件](../../raw/application-user-guide/memory-library-overview/modelstudio-memory-for-openclaw.md)。  

> **注意**：文档 1 称记忆片段默认有效期为 180 天，而文档 3 明确说明“生成的记忆片段与用户画像暂无失效日期”。该矛盾以文档 3 为准——**当前版本记忆无强制过期机制，过期时间由记忆规则配置决定，未配置时即永不过期**。

## 关键参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `user_id` | string | 是 | 用户唯一标识，用于隔离不同用户的记忆空间；同一 `user_id` 下所有记忆共享命名空间。 |
| `memory_library_id` | string | 否 | 指定目标记忆库 ID；不填则使用默认记忆库（每个账号自带一个，不可删除）。 |
| `project_id` | string | 否 | 记忆片段规则 ID；不填则使用所选记忆库的默认规则。 |
| `profile_schema` | string | 否 | 用户画像模板 ID；仅当需触发画像抽取时必填。 |
| `top_k` | number | 否（默认 5） | `SearchMemory` 返回的最大记忆条数；推荐值 3–10，平衡效果与性能。 |
| `min_score` / `similarity_threshold` | number | 否（默认 0 / 0.5） | 检索相似度阈值（0.0–1.0），低于此值的结果被过滤；文档 1 建议设为 0.5–0.7，文档 2 默认值为 0（即不限制），实际应按业务精度要求调整。 |

## 使用方式

1. **准备环境**：设置 `DASHSCOPE_API_KEY` 环境变量（获取方式见 [获取 API Key](https://help.aliyun.com/zh/model-studio/get-api-key)）。  
2. **写入记忆**：调用 `AddMemory` 接口。支持两种模式：  
   - 对话提炼：传入 `messages` 数组，由服务端自动提取（推荐）；  
   - 直接写入：传入 `custom_content` 字符串，绕过提取逻辑（适用于明确已知需存储的内容）。  
   示例见 [记忆库](../../raw/application-user-guide/memory-library-overview/memory-library.md)。  
3. **检索记忆**：调用 `SearchMemory`（或 `memory_nodes/search`），传入自然语言查询（`query` 或 `messages`）及 `user_id`。OpenClaw [插件](../concepts/plugin.md)还提供 `memory_search` 工具供 Agent 动态调用。  
4. **管理记忆**：支持 `ListMemory`（分页查看）、`UpdateMemory`（PATCH 更新内容）、`DeleteMemory`（DELETE 删除）等操作，详见 [长期记忆 API](../../raw/application-user-guide/memory-library-overview/long-term-memory-2-0.md)。  
5. **用户画像工作流**：创建模板（`CreateProfileSchema`）→ 写入带模板 ID 的对话（`AddMemory`）→ 异步获取结果（`GetUserProfile`），完整流程见 [记忆库](../../raw/application-user-guide/memory-library-overview/memory-library.md)。

## 限制和注意事项

- **配额限制**：阿里云账号级别总调用量 ≤ 3000 QPM；其中 `AddMemory` ≤ 120 QPM，`SearchMemory` ≤ 300 QPM。超出将返回限流错误（HTTP 429）。  
- **延迟特性**：`AddMemory` 端到端延迟约 500–1000ms，`SearchMemory` 约 200–500ms；OpenClaw 的 `autoCapture` 为异步执行，不影响主响应流。  
- **插件约束**：OpenClaw 记忆插件为全局配置，所有 Agent 共享同一记忆空间，**暂不支持按 Agent 实例独立隔离记忆**（见 [为 OpenClaw 配置长期记忆插件](../../raw/application-user-guide/memory-library-overview/modelstudio-memory-for-openclaw.md)）。  
- **字段命名规范**：用户画像中，同一模板内属性名称（`name`）应语义唯一（如避免同时存在“年龄”“年纪”），否则影响抽取准确率（见 [长期记忆 API](../../raw/application-user-guide/memory-library-overview/long-term-memory-2-0.md)）。  
- **调试建议**：控制台“记忆检索”标签页支持开启“改写”“排序”“意图判别召回”等功能优化效果；生产环境建议开启“排序”并设置 `similarity_threshold` 在 0.5–0.7 区间。

## 来源文档

- [记忆库](../../raw/application-user-guide/memory-library-overview/memory-library.md)
- [为 OpenClaw 配置长期记忆插件](../../raw/application-user-guide/memory-library-overview/modelstudio-memory-for-openclaw.md)
- [长期记忆 API](../../raw/application-user-guide/memory-library-overview/long-term-memory-2-0.md)



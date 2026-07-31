# memory library overview

记忆库是百炼平台提供的[长期记忆](../concepts/long-term-memory.md)能力核心组件，用于突破大模型上下文窗口限制，实现跨会话、跨对话的用户偏好与历史信息持久化。它通过自动从对话中提取结构化记忆片段和用户画像，并基于语义检索在后续交互中动态召回，使智能体具备持续性理解能力。该能力以开放 API 形式提供，支持直接集成、OpenClaw 插件接入等多种使用方式。

## 支持的模型/功能

- **记忆片段（Memory Snippet）**：自动从 `messages` 对话流中提炼关键事件（如“每天上午9点提醒我喝水”），也支持通过 `custom_content` 直接写入自定义文本。适用于大多数[长期记忆](../concepts/long-term-memory.md)场景。  
- **用户画像（User Profile）**：基于预定义的 `profile_schema`（含字段名、描述、初始值）从对话中抽取结构化属性（如年龄、职业、爱好）。需先调用 `CreateProfileSchema` 创建模板，再在 `AddMemory` 中指定 `profile_schema` ID 才能触发抽取。  
- **自动捕获与召回**：OpenClaw 插件支持 `autoCapture`（对话结束自动写入）和 `autoRecall`（对话开始前自动检索注入）机制，无需手动干预 [为 OpenClaw 配置长期记忆插件](../../raw/application-user-guide/memory-library-overview/modelstudio-memory-for-openclaw.md)。  
- **管理能力**：支持 `ListMemory`、`UpdateMemory`、`DeleteMemory` 等全生命周期操作，可结合 `meta_data` 进行分类管理 [长期记忆 API](../../raw/application-user-guide/memory-library-overview/long-term-memory-2-0.md)。

> **注意**：文档 3 声称“生成的记忆片段与用户画像暂无失效日期”，但文档 1 明确说明默认记忆片段规则有效期为 180 天，且可在控制台配置为 7/30/180 天或永不过期。实际行为以控制台配置及 API 参数 `expiration_days` 为准，建议显式设置避免歧义。

## 关键参数

| 参数 | 类型 | 必填 | 说明 | 来源 |
|------|------|------|------|------|
| `user_id` | string | 是 | 用户唯一标识，用于隔离记忆空间；同一 `user_id` 共享命名空间 [为 OpenClaw 配置长期记忆插件](../../raw/application-user-guide/memory-library-overview/modelstudio-memory-for-openclaw.md) | — |
| `memory_library_id` | string | 否 | 指定记忆库 ID；未提供时使用默认记忆库 [长期记忆 API](../../raw/application-user-guide/memory-library-overview/long-term-memory-2-0.md) | — |
| `project_id` | string | 否 | 记忆片段规则 ID；未提供时使用默认规则 [记憶庫](../../raw/application-user-guide/memory-library-overview/memory-library.md) | — |
| `profile_schema` | string | 否 | 用户画像模板 ID；仅当需触发画像抽取时必填 [记憶庫](../../raw/application-user-guide/memory-library-overview/memory-library.md) | — |
| `top_k` | number | 否 | 检索返回最大条数，默认 5（OpenClaw 插件）或未指定（API）；推荐设为 3–10 [长期记忆 API](../../raw/application-user-guide/memory-library-overview/long-term-memory-2-0.md) | — |
| `min_score` / `similarity_threshold` | number (0.0–1.0) | 否 | 相似度阈值，控制召回精度；OpenClaw 插件用 `minScore`（0–100），API 用 `similarity_threshold`（0.0–1.0） | — |
| `meta_data` | object | 否 | 自定义键值对，用于记忆分类、标签等元数据管理 [长期记忆 API](../../raw/application-user-guide/memory-library-overview/long-term-memory-2-0.md) | — |

## 使用方式

1. **准备环境**：设置 `DASHSCOPE_API_KEY` 环境变量，或在代码中显式传入 [获取 API Key](https://help.aliyun.com/zh/model-studio/get-api-key)。  
2. **写入记忆**：  
   - 对话流写入：调用 `AddMemory`，传入 `messages` 数组和 `user_id`；  
   - 自定义内容写入：使用 `custom_content` 字段直接存入文本；  
   - 用户画像写入：在 `AddMemory` 请求中携带 `profile_schema` ID。  
3. **检索记忆**：调用 `SearchMemory`，传入 `user_id` 和自然语言查询（如 `"我需要做什么？"`），结果可直接注入 Prompt。  
4. **查看与调试**：通过百炼控制台 [记忆库](https://bailian.console.aliyun.com/cn-beijing/?tab=app#/memory/list) 查看、检索、编辑记忆，或使用 `ListMemory` API 分页获取 [记憶庫](../../raw/application-user-guide/memory-library-overview/memory-library.md)。  
5. **OpenClaw 集成**：安装 `@modelstudio/modelstudio-memory-for-openclaw` 插件，配置 `apiKey` 和 `userId` 后，自动启用 `autoCapture`/`autoRecall`；同时注册 `memory_search`、`memory_store` 等工具供 Agent 主动调用 [为 OpenClaw 配置长期记忆插件](../../raw/application-user-guide/memory-library-overview/modelstudio-memory-for-openclaw.md)。

## 限制和注意事项

- **配额限制**：阿里云账号级别总计 ≤ 3000 QPM；其中 `AddMemory` ≤ 120 QPM，`SearchMemory` ≤ 300 QPM [为 OpenClaw 配置长期记忆插件](../../raw/application-user-guide/memory-library-overview/modelstudio-memory-for-openclaw.md)。  
- **延迟表现**：`SearchMemory` 端到端延迟 200–500ms，`AddMemory` 延迟 500–1000ms；OpenClaw 中 `autoCapture` 异步执行，不影响主响应流。  
- **默认记忆库**：每个账号自带一个不可删除的默认记忆库，已预置一条“默认项目”记忆片段规则（有效期 180 天），可编辑但不可删 [记憶庫](../../raw/application-user-guide/memory-library-overview/memory-library.md)。  
- **用户画像时效性**：画像提取非实时——`AddMemory` 触发抽取后需短暂延迟（文档示例建议 `await asyncio.sleep(3)`），再调用 `GetUserProfile` 获取结果。  
- **字段命名规范**：用户画像中避免语义近义字段并存（如同时定义“年龄”“岁数”），否则影响抽取准确率 [长期记忆 API](../../raw/application-user-guide/memory-library-overview/long-term-memory-2-0.md)。

## 来源文档

- [记忆库](../../raw/application-user-guide/memory-library-overview/memory-library.md)
- [为 OpenClaw 配置长期记忆插件](../../raw/application-user-guide/memory-library-overview/modelstudio-memory-for-openclaw.md)
- [长期记忆 API](../../raw/application-user-guide/memory-library-overview/long-term-memory-2-0.md)



# memory library overview

百炼平台的 Memory Library 是一套面向大模型应用的[长期记忆](../concepts/long-term-memory.md)能力基础设施，通过自动提取、结构化存储与语义检索机制，突破上下文窗口限制，实现跨会话的上下文感知与个性化交互。它既可通过 OpenClaw 插件开箱即用，也支持直接调用 API 集成到任意应用中。所有核心能力均基于阿里云百炼[长期记忆](../concepts/long-term-memory.md)服务（v2.0）提供。

## 支持的模型/功能

Memory Library 不依赖特定大模型，而是作为独立服务层运行，适配所有接入百炼平台的模型（如 Qwen 系列、通义千问等）。其核心功能分为两类：

- **记忆片段（Memory Snippets）**：从对话消息中自动提炼关键事件与事实（如“用户使用 FastAPI 框架”），支持语义检索、动态更新与智能去重。适用于通用[长期记忆](../concepts/long-term-memory.md)场景。  
- **用户画像（Profile Schema）**：基于预定义结构化模板（如年龄、职业、偏好字段）从对话中抽取属性，并持久化为可查询的用户画像。适用于需固定属性建模的业务场景。  

> **注意**：文档 3 称“生成的记忆片段与用户画像暂无失效日期”，但[记忆库](../../raw/application-user-guide/memory-library-overview/memory-library.md)明确说明默认记忆片段规则有效期为 180 天，且控制台支持配置 7/30/180 天或永不过期。实际过期行为以控制台配置为准，API 调用时若未显式指定 `memory_library_id` 和 `project_id`，将继承默认规则的有效期策略。

## 关键参数

| 参数名 | 类型 | 必填 | 说明 | 来源 |
|--------|------|------|------|------|
| `apiKey` | string | 是 | DashScope API Key（以 `sk-xxx` 开头），用于身份认证和配额计量 | [为 OpenClaw 配置长期记忆插件](../../raw/application-user-guide/memory-library-overview/modelstudio-memory-for-openclaw.md) |
| `userId` | string | 是 | 用户唯一标识符，用于隔离不同用户的记忆空间；同一 `userId` 下记忆共享，不同 `userId` 完全隔离 | [为 OpenClaw 配置长期记忆插件](../../raw/application-user-guide/memory-library-overview/modelstudio-memory-for-openclaw.md) |
| `memoryLibraryId` | string | 否 | 记忆库 ID，用于指定写入/检索的目标记忆库；不传则使用默认记忆库 | [记忆库](../../raw/application-user-guide/memory-library-overview/memory-library.md) |
| `projectId` | string | 否 | 记忆片段规则 ID，决定如何提取与存储内容；不传则使用该记忆库下的默认规则 | [记忆库](../../raw/application-user-guide/memory-library-overview/memory-library.md) |
| `profileSchema` | string | 否 | 用户画像模板 ID，用于启用结构化画像提取；需先通过 `CreateProfileSchema` 创建 | [长期记忆 API](../../raw/application-user-guide/memory-library-overview/long-term-memory-2-0.md) |
| `topK` | number | 否 | 默认 `5`（插件）或 `3–10`（API 最佳实践），控制每次 `SearchMemory` 返回的最大记忆条数 | [为 OpenClaw 配置长期记忆插件](../../raw/application-user-guide/memory-library-overview/modelstudio-memory-for-openclaw.md) |
| `minScore` / `similarity_threshold` | number | 否 | 相似度阈值（0–100 或 0.0–1.0），用于过滤低相关性结果；推荐设为 `0.5–0.7` | [记忆库](../../raw/application-user-guide/memory-library-overview/memory-library.md) |

## 使用方式

### 1. OpenClaw 插件集成（推荐快速上手）
- 安装插件：`openclaw plugins install @modelstudio/modelstudio-memory-for-openclaw`  
- 配置 `~/.openclaw/openclaw.json`，设置 `apiKey`、`userId` 及可选参数（如 `memoryLibraryId`）  
- 插件自动启用 `autoCapture`（对话后写入）与 `autoRecall`（对话前检索），无需修改 Agent 逻辑  
- 同时暴露四个工具供 Agent 主动调用：`memory_search`、`memory_store`、`memory_list`、`memory_forget`  

### 2. 直接 API 集成（灵活定制）
- **写入记忆**：调用 `AddMemory`，传入 `messages`（对话历史）或 `custom_content`（自定义文本），并指定 `userId`、`memoryLibraryId` 等元数据  
- **检索记忆**：调用 `SearchMemory`，传入自然语言查询或 `messages`，支持 `top_k`、`similarity_threshold` 等参数控制召回质量  
- **管理记忆**：使用 `ListMemory`、`UpdateMemory`、`DeleteMemory` 进行分页查看、内容更新与删除  
- **用户画像**：先调用 `CreateProfileSchema` 定义字段，再在 `AddMemory` 中传入 `profile_schema`，最后用 `GetUserProfile` 获取完整画像  

所有 API 均需通过 `Authorization: Bearer $DASHSCOPE_API_KEY` 认证，环境变量 `DASHSCOPE_API_KEY` 为必需配置。

## 限制和注意事项

- **配额限制**：阿里云账号级别总计不超过 3000 QPM；其中 `AddMemory` ≤ 120 QPM，`SearchMemory` ≤ 300 QPM。超出将返回 `429 Too Many Requests` 错误。  
- **延迟表现**：`SearchMemory` 端到端延迟约 200–500ms，`AddMemory` 约 500–1000ms；OpenClaw 插件的 `autoCapture` 为异步执行，不影响用户响应速度。  
- **插件约束**：OpenClaw 记忆插件为全局统一配置，所有 Agent 共享同一记忆空间，**暂不支持按 Agent 独立配置记忆库或规则**。  
- **兼容性**：仅支持 DashScope API Key，**不支持 Coding Plan 的 API Key**（见[为 OpenClaw 配置长期记忆插件](../../raw/application-user-guide/memory-library-overview/modelstudio-memory-for-openclaw.md)常见问题第3条）。  
- **数据一致性**：用户画像提取存在延迟（通常需 3 秒），调用 `GetUserProfile` 前建议 `await asyncio.sleep(3)` 或轮询确认。  
- **元数据支持**：API 层支持 `meta_data` 字段（如 `"location_name": "北京"`）用于分类管理，但 OpenClaw 插件当前配置项中未暴露该参数。

## 来源文档

- [为 OpenClaw 配置长期记忆插件](../../raw/application-user-guide/memory-library-overview/modelstudio-memory-for-openclaw.md)
- [记忆库](../../raw/application-user-guide/memory-library-overview/memory-library.md)
- [长期记忆 API](../../raw/application-user-guide/memory-library-overview/long-term-memory-2-0.md)



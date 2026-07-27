# memory library overview

记忆库是百炼平台提供的[长期记忆](../concepts/long-term-memory.md)能力组件，用于突破大模型上下文窗口限制，实现跨会话、跨对话的用户偏好与历史信息持久化。它通过自动从对话中提取结构化记忆片段和用户画像，并支持语义检索与注入，使智能体具备持续理解能力。该能力以 API 形式开放，可集成至任意应用或 Agent 框架（如 OpenClaw），也支持多应用共享同一记忆空间。

## 支持的模型/功能

- **记忆片段（Memory Snippet）**：从对话消息中自动提取关键事件（如“每天上午9点提醒我喝水”），支持自定义内容写入、语义检索、去重更新与元数据分类管理。适用于大多数[长期记忆](../concepts/long-term-memory.md)场景。  
- **用户画像（User Profile）**：基于预定义 Schema 从对话中抽取结构化属性（如年龄、职业、爱好），支持字段级描述引导、初始值设定与多轮增量更新。适用于需固定属性建模的场景。  
- **自动捕获与召回**：在 OpenClaw 等框架中，可通过插件生命周期钩子（`agent_end` / `before_agent_start`）实现全自动记忆写入与检索，无需手动调用 [为 OpenClaw 配置长期记忆插件](../../raw/application-user-guide/memory-library-overview/modelstudio-memory-for-openclaw.md)。  
- **多粒度控制**：支持按 `memory_library_id`（记忆库）、`project_id`（记忆片段规则）、`profile_schema`（画像模板）进行隔离与路由，满足多业务场景需求。

> **注意**：文档 3 称“生成的记忆片段与用户画像暂无失效日期”，但文档 1 明确指出默认记忆片段规则有效期为 180 天，且控制台界面支持配置 7/30/180 天或永不过期。实际行为以控制台配置及 API 参数为准，建议显式设置 `expiration_days` 或 `never_expire` 字段，避免依赖默认值。

## 关键参数

| 参数名 | 类型 | 必填 | 说明 | 来源 |
|--------|------|------|------|------|
| `user_id` | string | ✅ | 用户唯一标识，用于隔离记忆空间；不同 `user_id` 完全隔离 | [为 OpenClaw 配置长期记忆插件](../../raw/application-user-guide/memory-library-overview/modelstudio-memory-for-openclaw.md) |
| `memory_library_id` | string | ❌ | 目标记忆库 ID；不传则使用默认记忆库 | [长期记忆 API](../../raw/application-user-guide/memory-library-overview/long-term-memory-2-0.md) |
| `project_id` | string | ❌ | 记忆片段规则 ID；不传则使用该记忆库的默认规则 | [长期记忆 API](../../raw/application-user-guide/memory-library-overview/long-term-memory-2-0.md) |
| `profile_schema` | string | ❌ | 用户画像模板 ID；用于触发结构化属性抽取 | [记忆库](../../raw/application-user-guide/memory-library-overview/memory-library.md) |
| `meta_data` | object | ❌ | 自定义键值对，用于分类、过滤与管理（如 `"location_name": "北京"`） | [长期记忆 API](../../raw/application-user-guide/memory-library-overview/long-term-memory-2-0.md) |
| `top_k` | number | ❌（默认 5） | 检索返回的最大记忆条数；推荐设为 3–10 平衡效果与性能 | [长期记忆 API](../../raw/application-user-guide/memory-library-overview/long-term-memory-2-0.md) |
| `min_score` / `similarity_threshold` | number (0.0–1.0) | ❌（默认 0） | 相似度阈值，过滤低相关性结果；建议设为 0.5–0.7 | [记忆库](../../raw/application-user-guide/memory-library-overview/memory-library.md) |

## 使用方式

### 1. 基础 API 调用（通用）
- **写入记忆**：调用 `AddMemory`，传入 `messages`（对话数组）或 `custom_content`（纯文本），指定 `user_id` 及可选规则 ID。  
- **检索记忆**：调用 `SearchMemory`，传入自然语言查询（`query`）或 `messages`，返回语义匹配的记忆列表。  
- **管理记忆**：支持 `ListMemory`（分页查询）、`UpdateMemory`（PATCH）、`DeleteMemory`（DELETE）等操作。  
- **用户画像**：先调用 `CreateProfileSchema` 定义字段，再在 `AddMemory` 中传入 `profile_schema`，最后用 `GetUserProfile` 获取完整画像。

### 2. OpenClaw 插件集成（开箱即用）
安装 `@modelstudio/modelstudio-memory-for-openclaw` 插件后，在 `openclaw.json` 中配置 `apiKey` 和 `userId` 即可启用全自动捕获（`autoCapture`）与召回（`autoRecall`）。插件还暴露 `memory_search`、`memory_store` 等工具供 Agent 主动调用，详见 [为 OpenClaw 配置长期记忆插件](../../raw/application-user-guide/memory-library-overview/modelstudio-memory-for-openclaw.md)。

### 3. 控制台辅助
- 在 [百炼控制台 → 记忆库](https://bailian.console.aliyun.com/cn-beijing/?tab=app#/memory/list) 创建/编辑记忆库、配置规则、调试检索效果。  
- “记忆详情”页按 `user_id` 查看已存记忆；“记忆检索”页可实时测试查询改写、排序与阈值效果。

## 限制和注意事项

- **配额限制**：阿里云账号级别总计 ≤ 3000 QPM；其中 `AddMemory` ≤ 120 QPM，`SearchMemory` ≤ 300 QPM。超出将返回 `429 Too Many Requests` [长期记忆 API](../../raw/application-user-guide/memory-library-overview/long-term-memory-2-0.md)。  
- **延迟特性**：`AddMemory` 端到端延迟约 500–1000ms，`SearchMemory` 约 200–500ms；自动捕获为异步执行，不影响主流程响应速度。  
- **兼容性**：OpenClaw 插件统一配置，所有 Agent 共享同一记忆空间，暂不支持 per-Agent 独立配置 [为 OpenClaw 配置长期记忆插件](../../raw/application-user-guide/memory-library-overview/modelstudio-memory-for-openclaw.md)。  
- **API Key 要求**：仅支持百炼平台标准 API Key，**不支持 Coding Plan 的 API Key** [为 OpenClaw 配置长期记忆插件](../../raw/application-user-guide/memory-library-overview/modelstudio-memory-for-openclaw.md)。  
- **数据一致性**：用户画像提取存在约 3 秒延迟，调用 `GetUserProfile` 前需等待（如 Python 示例中的 `asyncio.sleep(3)`），否则可能返回空值。

## 来源文档

- [记忆库](../../raw/application-user-guide/memory-library-overview/memory-library.md)
- [为 OpenClaw 配置长期记忆插件](../../raw/application-user-guide/memory-library-overview/modelstudio-memory-for-openclaw.md)
- [长期记忆 API](../../raw/application-user-guide/memory-library-overview/long-term-memory-2-0.md)



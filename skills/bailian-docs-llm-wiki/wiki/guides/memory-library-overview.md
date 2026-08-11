# memory library overview

记忆库是百炼平台提供的[长期记忆](../concepts/long-term-memory.md)能力组件，用于突破大模型上下文窗口限制，实现跨会话的用户偏好、关键事件和结构化属性的持久化存储与语义化召回。它通过自动提取对话中的记忆片段与用户画像，并提供标准化 API 接口，使智能体具备持续性理解能力。该能力已全面集成于百炼控制台、Agentscope Runtime 及 OpenClaw 等主流框架。

## 支持的模型/功能

- **记忆片段（Memory Snippet）**：从对话中自动提取关键事件（如“每天上午9点提醒我喝水”），支持自定义内容写入、语义检索、动态更新与智能去重。适用于大多数[长期记忆](../concepts/long-term-memory.md)场景。  
- **用户画像（User Profile）**：基于预定义 Schema 从对话中抽取结构化属性（如年龄、职业、爱好），支持多轮渐进式填充与完整画像获取。适用于需固定字段的业务场景。  
- **双模式提取引擎**：支持 `Lite`（¥0.018/次，无 Rerank）与 `Pro`（¥0.03/次，含 Rerank）两种记忆抽取版本，详见 [记忆库](../../raw/application-user-guide/memory-library-overview/memory-library.md)。  
- **自动捕获与自动召回**：在 OpenClaw 等 Agent 框架中，可通过[插件](../concepts/plugin.md)生命周期钩子（`agent_end` / `before_agent_start`）实现零侵入式记忆写入与注入，详见 [为 OpenClaw 配置长期记忆插件](../../raw/application-user-guide/memory-library-overview/modelstudio-memory-for-openclaw.md)。

> **注意**：文档 3 声称“生成的记忆片段与用户画像暂无失效日期”，但文档 1 明确说明默认记忆片段规则有效期为 180 天，且可在控制台配置为 7/30/180 天或永不过期。实际行为以控制台配置及 API 中 `expiration_time` 参数为准，文档 3 的表述已过时。

## 关键参数

| 参数 | 类型 | 是否必填 | 说明 |
|------|------|----------|------|
| `user_id` | string | 是 | 用户唯一标识，用于隔离记忆空间；不同 `user_id` 完全隔离 |
| `memory_library_id` | string | 否 | 记忆库 ID；不传则使用默认记忆库（见 [记忆库](../../raw/application-user-guide/memory-library-overview/memory-library.md)） |
| `project_id` | string | 否 | 记忆片段规则 ID；不传则使用默认规则（见 [记忆库](../../raw/application-user-guide/memory-library-overview/memory-library.md)） |
| `profile_schema` | string | 否 | 用户画像 Schema ID；用于触发画像提取（见 [长期记忆 API](../../raw/application-user-guide/memory-library-overview/long-term-memory-2-0.md)） |
| `meta_data` | object | 否 | 自定义元数据（如 `{"location_name": "北京"}`），用于分类管理与条件检索 |
| `top_k` | number | 否（默认 5） | `SearchMemory` 返回的最大记忆条数，建议设为 3–10（见 [长期记忆 API](../../raw/application-user-guide/memory-library-overview/long-term-memory-2-0.md)） |
| `min_score` | number | 否（默认 0） | 相似度阈值（0–100），低于此值的记忆不返回 |

## 使用方式

### 1. 基础 API 调用（通用）
- **写入记忆**：调用 `AddMemory`，传入 `messages`（对话历史）或 `custom_content`（直接内容）。支持指定 `memory_library_id`、`project_id`、`profile_schema` 和 `meta_data`。  
- **检索记忆**：调用 `SearchMemory`，传入自然语言查询（`query` 字段）或 `messages`（推荐），返回语义匹配的记忆节点列表。  
- **管理记忆**：支持 `ListMemory`（分页查询）、`UpdateMemory`（PATCH）、`DeleteMemory`（DELETE）等完整 CRUD 操作。  

### 2. SDK 集成（Python）
需安装 `agentscope-runtime`：
```bash
pip install agentscope-runtime
```
示例见 [记忆库](../../raw/application-user-guide/memory-library-overview/memory-library.md) 中的 `AddMemory`、`SearchMemory`、`CreateProfileSchema` 等工具调用。

### 3. OpenClaw [插件](../concepts/plugin.md)集成
通过 `@modelstudio/modelstudio-memory-for-openclaw` [插件](../concepts/plugin.md)实现自动捕获与召回：
- 配置 `~/.openclaw/openclaw.json`，设置 `apiKey` 和 `userId`；
- 插件自动注册 `memory_search`、`memory_store` 等工具供 Agent 主动调用；
- CLI 命令支持 `openclaw modelstudio-memory search` 等调试操作（见 [为 OpenClaw 配置长期记忆插件](../../raw/application-user-guide/memory-library-overview/modelstudio-memory-for-openclaw.md)）。

## 限制和注意事项

- **速率限制（阿里云账号级别）**：  
  - `AddMemory`：≤ 120 次/分钟  
  - `SearchMemory`：≤ 300 次/分钟  
  - 所有记忆 API 总计 ≤ 3000 次/分钟（见 [为 OpenClaw 配置长期记忆插件](../../raw/application-user-guide/memory-library-overview/modelstudio-memory-for-openclaw.md) 和 [长期记忆 API](../../raw/application-user-guide/memory-library-overview/long-term-memory-2-0.md)）  
- **延迟指标**：  
  - `SearchMemory` 端到端延迟：200–500ms  
  - `AddMemory` 延迟：500–1000ms；自动捕获为异步执行，不影响主响应流  
- **记忆库配额**：每个记忆库最多配置 50 条记忆片段规则 + 50 条用户画像规则（见 [记忆库](../../raw/application-user-guide/memory-library-overview/memory-library.md)）  
- **API Key 要求**：仅支持百炼平台标准 API Key，**不支持 Coding Plan 的 API Key**（见 [为 OpenClaw 配置长期记忆插件](../../raw/application-user-guide/memory-library-overview/modelstudio-memory-for-openclaw.md)）  
- **用户画像提取时效性**：调用 `AddMemory` 写入含画像信息的对话后，需等待约 3 秒再调用 `GetUserProfile` 获取结果（见 [长期记忆 API](../../raw/application-user-guide/memory-library-overview/long-term-memory-2-0.md)）

## 来源文档

- [记忆库](../../raw/application-user-guide/memory-library-overview/memory-library.md)
- [为 OpenClaw 配置长期记忆插件](../../raw/application-user-guide/memory-library-overview/modelstudio-memory-for-openclaw.md)
- [长期记忆 API](../../raw/application-user-guide/memory-library-overview/long-term-memory-2-0.md)



# memory library overview

记忆库是百炼平台提供的[长期记忆](../concepts/long-term-memory.md)能力核心组件，用于突破大模型上下文窗口限制，实现跨会话、跨对话的语义化记忆持久化与智能召回。它通过自动提取对话中的关键事件（记忆片段）和结构化用户属性（用户画像），支持开发者在应用中按需写入、检索、更新和管理记忆，并将相关记忆注入 Prompt，从而构建具备持续理解能力的智能体。

## 支持的模型/功能

记忆库本身不绑定特定大模型，而是作为独立服务通过 API 与任意 LLM 应用集成。其核心功能包括：

- **记忆片段（Memory Snippet）**：从对话消息中自动提炼关键事实（如“每天上午9点提醒我喝水”），支持自定义规则控制提取逻辑；也支持直接写入 `custom_content` 字段的非对话内容 [长期记忆 API](../../raw/application-user-guide/memory-library-overview/long-term-memory-2-0.md)。
- **用户画像（User Profile）**：基于预定义 Schema（字段名+描述）从对话中抽取结构化属性（如年龄、职业、偏好），适用于需固定属性建模的场景 [记忆库](../../raw/application-user-guide/memory-library-overview/memory-library.md)。
- **自动捕获与召回**：在 OpenClaw 等框架中，可通过插件生命周期钩子实现对话结束自动写入、对话开始前自动检索并注入上下文 [为 OpenClaw 配置长期记忆插件](../../raw/application-user-guide/memory-library-overview/modelstudio-memory-for-openclaw.md)。

> **注意**：文档 3 称“生成的记忆片段与用户画像暂无失效日期”，但文档 1 明确说明默认记忆片段规则有效期为 180 天，且可在控制台配置 7/30/180 天或永不过期。实际行为以控制台配置及 API 参数 `expire_after_days` 为准，文档 3 的表述已过时。

## 关键参数

| 参数 | 类型 | 是否必填 | 说明 | 来源 |
|------|------|----------|------|------|
| `user_id` | string | 是 | 用户唯一标识，用于隔离不同用户的记忆空间；同一 `user_id` 下所有记忆共享命名空间 | [为 OpenClaw 配置长期记忆插件](../../raw/application-user-guide/memory-library-overview/modelstudio-memory-for-openclaw.md) |
| `memory_library_id` | string | 否 | 指定目标记忆库 ID；未提供时使用默认记忆库 | [长期记忆 API](../../raw/application-user-guide/memory-library-overview/long-term-memory-2-0.md) |
| `project_id` | string | 否 | 记忆片段规则 ID；未提供时使用该记忆库的默认规则 | [记忆库](../../raw/application-user-guide/memory-library-overview/memory-library.md) |
| `profile_schema` | string | 否 | 用户画像 Schema ID；用于触发画像提取流程 | [记忆库](../../raw/application-user-guide/memory-library-overview/memory-library.md) |
| `meta_data` | object | 否 | 自定义元数据（如 `{"location_name": "北京"}`），用于分类、过滤和管理记忆 | [长期记忆 API](../../raw/application-user-guide/memory-library-overview/long-term-memory-2-0.md) |
| `top_k` | number | 否（默认 5） | `SearchMemory` 返回的最大记忆条数；建议设为 3–10 平衡效果与性能 | [为 OpenClaw 配置长期记忆插件](../../raw/application-user-guide/memory-library-overview/modelstudio-memory-for-openclaw.md) |
| `min_score` / `similarity_threshold` | number (0.0–1.0) | 否（默认 0） | 相似度阈值，用于过滤低相关性结果；文档 2 使用 `minScore`（0–100 整数），文档 3 和控制台使用 `similarity_threshold`（0.0–1.0 浮点） | [为 OpenClaw 配置长期记忆插件](../../raw/application-user-guide/memory-library-overview/modelstudio-memory-for-openclaw.md)、[记忆库](../../raw/application-user-guide/memory-library-overview/memory-library.md) |

> **注意**：`minScore`（文档 2）与 `similarity_threshold`（文档 1/3）语义相同但数值范围不一致（整数 0–100 vs 浮点 0.0–1.0），调用方需根据所用 SDK 或接口规范转换，避免误配。

## 使用方式

### 基础 API 调用（通用）
1. **写入记忆**：调用 `AddMemory`，传入 `messages`（对话历史）或 `custom_content`（直接内容），指定 `user_id` 及可选参数。
2. **检索记忆**：调用 `SearchMemory`，传入 `user_id` 和自然语言查询（`query` 字段）或 `messages`（推荐），设置 `top_k`。
3. **管理记忆**：使用 `ListMemory`（分页查询）、`UpdateMemory`（PATCH）、`DeleteMemory`（DELETE）进行 CRUD 操作 [长期记忆 API](../../raw/application-user-guide/memory-library-overview/long-term-memory-2-0.md)。

### OpenClaw 插件集成（开箱即用）
- 安装 `@modelstudio/modelstudio-memory-for-openclaw` 插件，配置 `apiKey` 和 `userId` 即可启用自动捕获（`autoCapture`）与自动召回（`autoRecall`）。
- 插件额外暴露 `memory_search`、`memory_store`、`memory_list`、`memory_forget` 四个工具供 Agent 主动调用 [为 OpenClaw 配置长期记忆插件](../../raw/application-user-guide/memory-library-overview/modelstudio-memory-for-openclaw.md)。

### 控制台操作
- 在 [百炼控制台 > 记忆库](https://bailian.console.aliyun.com/cn-beijing/?tab=app#/memory/list) 创建/编辑记忆库，配置记忆片段规则（含有效期、自动更新）和用户画像规则（含字段描述、初始值） [记忆库](../../raw/application-user-guide/memory-library-overview/memory-library.md)。

## 限制和注意事项

- **配额限制**：阿里云账号级别总计 ≤ 3000 QPM；其中 `AddMemory` ≤ 120 QPM，`SearchMemory` ≤ 300 QPM [为 OpenClaw 配置长期记忆插件](../../raw/application-user-guide/memory-library-overview/modelstudio-memory-for-openclaw.md)、[长期记忆 API](../../raw/application-user-guide/memory-library-overview/long-term-memory-2-0.md)。
- **延迟指标**：`SearchMemory` 端到端延迟 200–500ms，`AddMemory` 500–1000ms；自动捕获为异步执行，不影响主链路响应速度 [为 OpenClaw 配置长期记忆插件](../../raw/application-user-guide/memory-library-overview/modelstudio-memory-for-openclaw.md)。
- **默认记忆库**：每个账号自带一个不可删除的默认记忆库，已预置一条有效期 180 天的“默认项目”规则，可编辑但不可删 [记忆库](../../raw/application-user-guide/memory-library-overview/memory-library.md)。
- **用户画像提取**：需多轮对话逐步完善，单次对话难以覆盖全部字段；字段名应语义唯一（避免“姓名”“名字”“名称”并存），描述需具体清晰 [长期记忆 API](../../raw/application-user-guide/memory-library-overview/long-term-memory-2-0.md)。
- **API Key 兼容性**：仅支持百炼标准 API Key，不支持 Coding Plan 的 API Key [为 OpenClaw 配置长期记忆插件](../../raw/application-user-guide/memory-library-overview/modelstudio-memory-for-openclaw.md)。

## 来源文档

- [记忆库](../../raw/application-user-guide/memory-library-overview/memory-library.md)
- [为 OpenClaw 配置长期记忆插件](../../raw/application-user-guide/memory-library-overview/modelstudio-memory-for-openclaw.md)
- [长期记忆 API](../../raw/application-user-guide/memory-library-overview/long-term-memory-2-0.md)



# memory library overview

百炼平台的 Memory Library 是一套面向大模型应用的[长期记忆](../concepts/long-term-memory.md)管理能力，通过自动提取、结构化存储与语义检索机制，突破上下文窗口限制，实现跨会话的用户偏好与历史信息持续感知。其核心由服务端[长期记忆](../concepts/long-term-memory.md) API 与客户端[插件](../concepts/plugin.md)（如 OpenClaw [插件](../concepts/plugin.md)）协同构成，支持记忆片段与用户画像两类内容，适用于个性化对话、状态延续、多轮任务等场景。开发者可通过 API 直接集成，或借助官方[插件](../concepts/plugin.md)快速启用自动捕获与召回能力。

## 支持的模型/功能

- **记忆类型**：支持两类结构化记忆内容  
  - **记忆片段**：从对话中自动提炼关键事件（如“每天上午9点提醒喝水”），适用于通用[长期记忆](../concepts/long-term-memory.md)场景；  
  - **用户画像**：基于自定义 Schema 提取结构化属性（如年龄、职业、爱好），需显式配置 `profile_schema` 参数，详见 [记忆库](../../raw/application-user-guide/memory-library-overview/memory-library.md)。  
- **核心能力**：自动记忆捕获（autoCapture）、自动记忆召回（autoRecall）、语义检索（SearchMemory）、直接写入（AddMemory）、分页管理（ListMemory）、精准删除（DeleteMemory）及画像全生命周期管理（CreateProfileSchema / GetUserProfile）。  
- **适用范围**：所有接入百炼长期记忆 API 的应用均支持，包括 OpenClaw Agent、自研 Agent 框架及任意 HTTP 客户端。> **注意**：文档 3 称“生成的记忆片段与用户画像暂无失效日期”，但 [记忆库](../../raw/application-user-guide/memory-library-overview/memory-library.md) 明确说明记忆片段规则支持设置 7 天/30 天/180 天/永不过期，实际有效期由规则配置决定，以控制台配置为准。

## 关键参数

| 参数名 | 类型 | 必填 | 默认值 | 说明 |
|--------|------|------|--------|------|
| `apiKey` | string | 是 | — | DashScope API Key（以 `sk-xxx` 开头），用于身份认证。不支持 Coding Plan 的 API Key，见 [为 OpenClaw 配置长期记忆插件](../../raw/application-user-guide/memory-library-overview/modelstudio-memory-for-openclaw.md)。 |
| `userId` | string | 是 | — | 用户唯一标识符，用于隔离记忆空间；同一 `userId` 共享命名空间，不同 `userId` 完全隔离。 |
| `memoryLibraryId` | string | 否 | 默认记忆库 | 记忆库 ID，可在[记忆库](../../raw/application-user-guide/memory-library-overview/memory-library.md)控制台卡片上获取；未传时使用默认记忆库。 |
| `projectId` | string | 否 | 默认项目规则 | 记忆片段规则 ID，用于指定提取策略；在记忆库详情页的“记忆规则”中获取。 |
| `profileSchema` | string | 否 | — | 用户画像 Schema ID，用于触发结构化属性抽取；需先调用 `CreateProfileSchema` 创建，见 [长期记忆 API](../../raw/application-user-guide/memory-library-overview/long-term-memory-2-0.md)。 |
| `topK` | number | 否 | `5` | 每次 `SearchMemory` 返回的最大记忆条数（范围 1–100）。 |
| `minScore` | number | 否 | `0` | 相似度阈值（0–100），低于此值的结果被过滤。 |
| `autoCapture` / `autoRecall` | boolean | 否 | `true` | 控制是否启用自动写入/自动读取，默认开启。 |

## 使用方式

### 1. 插件方式（OpenClaw）
- 安装插件：`openclaw plugins install @modelstudio/modelstudio-memory-for-openclaw`  
- 配置 `~/.openclaw/openclaw.json`，在 `plugins.entries.modelstudio-memory-for-openclaw.config` 中填入 `apiKey` 和 `userId` 等参数；`slots.memory` 必须设为 `"modelstudio-memory-for-openclaw"` 以禁用内置内存模块。  
- 重启 Gateway：`openclaw gateway restart`，验证状态：`openclaw plugins info modelstudio-memory-for-openclaw`。  
- 插件自动注册工具：`memory_search`、`memory_store`、`memory_list`、`memory_forget`，Agent 可在运行时动态调用。

### 2. 直接 API 调用
- 所有接口均通过 HTTPS 访问 `https://dashscope.aliyuncs.com/api/v2/apps/memory/...`，需在请求头携带 `Authorization: Bearer $DASHSCOPE_API_KEY`。  
- 写入记忆：`POST /add`，支持传入 `messages`（自动提取）或 `custom_content`（直接写入），可选 `meta_data` 分类管理。  
- 检索记忆：`POST /memory_nodes/search`，传入自然语言查询或 `messages`，返回语义匹配的记忆节点列表。  
- 管理记忆：`GET /memory_nodes`（分页列表）、`PATCH /memory_nodes/{id}`（更新）、`DELETE /memory_nodes/{id}`（删除）。  
- 用户画像：`POST /profile_schemas`（创建模板）、`GET /profile_schemas/{id}/user_profile`（获取画像）。

## 限制和注意事项

- **配额限制**（阿里云账号级别）：  
  - 总调用量 ≤ 3000 QPM；  
  - `AddMemory` ≤ 120 QPM；  
  - `SearchMemory` ≤ 300 QPM。  
  具体限流策略见 [长期记忆 API](../../raw/application-user-guide/memory-library-overview/long-term-memory-2-0.md)。  
- **性能指标**：`SearchMemory` 端到端延迟 200–500ms；`AddMemory` 延迟 500–1000ms；自动捕获为异步执行，不影响主响应流。  
- **兼容性**：  
  - 不支持阿里云百炼 Coding Plan 的 API Key；  
  - 插件仅支持统一配置，所有 Agent 共享同一记忆空间，暂不支持按 Agent 独立配置；  
  - `projectId` 和 `profileSchema` 为非必填项，但若需定制提取逻辑或画像能力，必须正确传入对应 ID。  
- **计费提示**：记忆库将于 **2026 年 8 月 20 日 10:00（北京时间）** 正式开始商业化计费，Pro/Lite 版本按次计费，详见 [记忆库](../../raw/application-user-guide/memory-library-overview/memory-library.md)。

## 来源文档

- [为 OpenClaw 配置长期记忆插件](../../raw/application-user-guide/memory-library-overview/modelstudio-memory-for-openclaw.md)
- [记忆库](../../raw/application-user-guide/memory-library-overview/memory-library.md)
- [长期记忆 API](../../raw/application-user-guide/memory-library-overview/long-term-memory-2-0.md)



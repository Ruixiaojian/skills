# memory library overview

百炼平台的 Memory Library 是一套面向大模型应用的[长期记忆](../concepts/long-term-memory.md)能力基础设施，通过自动提取、向量化存储与语义检索机制，突破上下文窗口限制，实现跨会话的用户偏好与历史信息持续感知。它既支持开箱即用的插件集成（如 OpenClaw），也提供标准化 API 供任意应用自主接入，底层由阿里云百炼[长期记忆](../concepts/long-term-memory.md)服务统一支撑。

## 支持的模型/功能

- **核心能力**：支持两类记忆内容  
  - **记忆片段（Memory Fragments）**：从对话中自动提炼关键事件（如“每天上午9点提醒喝水”），适用于通用[长期记忆](../concepts/long-term-memory.md)场景；  
  - **用户画像（Profile Schema）**：基于结构化模板抽取固定属性（如年龄、职业、爱好），需预先在控制台或通过 `CreateProfileSchema` API 创建规则 [记忆库](../../raw/application-user-guide/memory-library-overview/memory-library.md)。  
- **适用范围**：所有接入百炼 API 的大模型应用均可使用，支持多应用共享同一记忆库；不依赖特定模型，与底层 LLM 解耦。  
- **自动能力**：默认启用自动捕获（`autoCapture`）和自动召回（`autoRecall`），无需 Agent 主动调用即可完成记忆写入与注入 [为 OpenClaw 配置长期记忆插件](../../raw/application-user-guide/memory-library-overview/modelstudio-memory-for-openclaw.md)。  

> **注意**：文档 3 声称“生成的记忆片段与用户画像暂无失效日期”，但文档 2 明确指出记忆片段规则支持配置过期时间（7天/30天/180天/永不过期），且默认规则有效期为 180 天。实际行为以控制台配置及 API 参数为准，建议显式设置 `expire_time` 或 `memory_library_id` 以确保预期生命周期。

## 关键参数

| 参数名 | 类型 | 必填 | 默认值 | 说明 |
|--------|------|------|--------|------|
| `apiKey` | string | 是 | — | DashScope API Key（以 `sk-xxx` 开头），用于认证百炼服务调用 |
| `userId` | string | 是 | — | 用户唯一标识，用于隔离记忆空间；不同 `userId` 完全隔离 |
| `memoryLibraryId` | string | 否 | 默认记忆库 | 记忆库存储位置，可在[记忆库](../../raw/application-user-guide/memory-library-overview/memory-library.md)控制台获取 |
| `profileSchema` | string | 否 | — | 用户画像模板 ID，用于结构化属性抽取；需先创建画像规则 |
| `projectId` | string | 否 | 默认项目 | 记忆片段规则 ID，决定提取策略（如默认规则或自定义指令） |
| `topK` | number | 否 | `5` | 每次 `SearchMemory` 召回的最大记忆条数（1–100） |
| `minScore` | number | 否 | `0` | 相似度阈值（0–100），低于此值的结果被过滤 |
| `autoCapture` / `autoRecall` | boolean | 否 | `true` | 控制是否启用自动写入/自动注入，可关闭后由 Agent 显式调用工具 |

## 使用方式

### 1. 插件方式（OpenClaw）
适用于 OpenClaw Agent 场景：  
- 安装插件：`openclaw plugins install @modelstudio/modelstudio-memory-for-openclaw`  
- 配置 `~/.openclaw/openclaw.json`，启用并填入 `apiKey` 和 `userId`  
- 插件自动注册 `memory_search`、`memory_store` 等工具，Agent 可在推理中动态调用 [为 OpenClaw 配置长期记忆插件](../../raw/application-user-guide/memory-library-overview/modelstudio-memory-for-openclaw.md)  

### 2. 直接 API 调用
适用于任意自研应用：  
- **写入记忆**：调用 `AddMemory`，传入 `messages`（对话历史）或 `custom_content`（直接内容）  
- **检索记忆**：调用 `SearchMemory`，传入自然语言查询或 `messages` 上下文  
- **管理记忆**：支持 `ListMemory`、`UpdateMemory`、`DeleteMemory` 等完整 CRUD 操作  
- **用户画像**：通过 `CreateProfileSchema` → `AddMemory`（带 `profile_schema`）→ `GetUserProfile` 流程构建 [长期记忆 API](../../raw/application-user-guide/memory-library-overview/long-term-memory-2-0.md)  

### 3. 控制台操作
- 在百炼控制台 [记忆库](https://bailian.console.aliyun.com/cn-beijing?tab=app#/memory/list) 页面创建/编辑记忆库、配置规则、调试检索效果  
- 支持可视化查看记忆详情、分页列表、语义检索测试  

## 限制和注意事项

- **配额限制**（阿里云账号级别）：  
  - 所有 API 总调用量 ≤ 3000 QPM  
  - `AddMemory` ≤ 120 QPM  
  - `SearchMemory` ≤ 300 QPM  
  （详见 [长期记忆 API](../../raw/application-user-guide/memory-library-overview/long-term-memory-2-0.md)）  
- **延迟表现**：  
  - `SearchMemory` 端到端延迟：200–500ms  
  - `AddMemory` 延迟：500–1000ms；自动捕获为异步执行，不影响主响应流  
- **关键约束**：  
  - 不支持 Coding Plan 的 API Key，仅限百炼标准 API Key  
  - `memoryLibraryId` 和 `projectId` 未指定时，系统自动选择默认值，但生产环境建议显式传入以避免不确定性  
  - 用户画像字段名称应语义唯一（如避免同时定义“年龄”“岁数”），否则影响抽取准确率  
- **商业化提示**：记忆库将于 2026 年 8 月 20 日起正式计费，Pro/Lite 版本按调用次数收费（详见 [记忆库](../../raw/application-user-guide/memory-library-overview/memory-library.md)）

## 来源文档

- [为 OpenClaw 配置长期记忆插件](../../raw/application-user-guide/memory-library-overview/modelstudio-memory-for-openclaw.md)
- [记忆库](../../raw/application-user-guide/memory-library-overview/memory-library.md)
- [长期记忆 API](../../raw/application-user-guide/memory-library-overview/long-term-memory-2-0.md)



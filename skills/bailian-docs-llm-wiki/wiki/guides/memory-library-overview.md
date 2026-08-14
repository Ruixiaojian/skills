# memory library overview

记忆库是百炼平台提供的[长期记忆](../concepts/long-term-memory.md)能力组件，用于突破大模型上下文窗口限制，实现跨会话的信息持久化与语义化召回。它通过自动从对话中提取关键事件（记忆片段）或结构化属性（用户画像），并支持开发者在应用中按需写入、检索、更新和管理，最终将相关记忆注入 Prompt，提升智能体的个性化与连贯性体验。该能力以开放 API 形式提供，可集成至任意应用或 Agent 框架。

## 支持的模型/功能

- **记忆片段（Memory Nodes）**：从对话消息中自动提取关键事件（如“每天上午9点提醒我喝水”），支持自定义内容直接写入、语义检索、动态更新与元数据分类管理。适用于大多数[长期记忆](../concepts/long-term-memory.md)场景。  
- **用户画像（Profile Schema）**：基于预定义模板从对话中抽取结构化用户属性（如年龄、职业、爱好），支持字段级描述引导、初始值设置与多轮渐进式填充。适用于需固定属性建模的场景。  
- **双模式支持**：同时支持 `autoCapture`（对话结束自动提取）与 `autoRecall`（对话开始前自动检索）的[插件](../concepts/plugin.md)化集成（如 OpenClaw），也支持纯 API 主动调用。  
- **多应用共享**：同一记忆库可被多个应用或 Agent 共享，通过 `user_id` 实现逻辑隔离 [为 OpenClaw 配置长期记忆插件](../../raw/application-user-guide/memory-library-overview/modelstudio-memory-for-openclaw.md)。

> **注意**：文档 1 称“生成的记忆片段与用户画像暂无失效日期”，而文档 1 的“配置记忆片段规则”章节明确支持设置 7/30/180 天或永不过期；文档 2 未提过期机制。实际行为以控制台或 API 中配置的 `expired_in_days` 为准，**默认规则有效期为 180 天**，非“永不过期”。该矛盾以文档 1 的配置说明为准。

## 关键参数

| 参数 | 类型 | 是否必填 | 说明 | 来源 |
|------|------|----------|------|------|
| `user_id` | string | 是 | 用户唯一标识，用于隔离记忆空间；不同 `user_id` 数据完全隔离 | [记忆库](../../raw/application-user-guide/memory-library-overview/memory-library.md) |
| `memory_library_id` | string | 否 | 记忆库 ID；不传则使用默认记忆库 | [长期记忆 API](../../raw/application-user-guide/memory-library-overview/long-term-memory-2-0.md) |
| `project_id` | string | 否 | 记忆片段规则 ID；不传则使用默认规则 | [长期记忆 API](../../raw/application-user-guide/memory-library-overview/long-term-memory-2-0.md) |
| `profile_schema` | string | 否 | 用户画像模板 ID；仅当需提取画像时传入 | [记忆库](../../raw/application-user-guide/memory-library-overview/memory-library.md) |
| `meta_data` | object | 否 | 自定义键值对，用于分类管理（如 `"location_name": "北京"`） | [长期记忆 API](../../raw/application-user-guide/memory-library-overview/long-term-memory-2-0.md) |
| `plan_version` | string | 否 | 检索策略版本，取值 `"pro"`（启用 Rerank，¥0.001/次）或 `"lite"`（关闭 Rerank，¥0.00002/次）；Search 接口独立生效，优先级高于 `enable_rerank` | [长期记忆 API](../../raw/application-user-guide/memory-library-overview/long-term-memory-2-0.md) |

## 使用方式

### 1. 基础流程（API 主动调用）
- **写入**：调用 `AddMemory`，传入 `messages`（对话历史）或 `custom_content`（自定义文本）及 `user_id`。  
- **检索**：调用 `SearchMemory`，传入 `user_id` 和自然语言查询（如 `"我需要做什么？"`），推荐 `top_k=3~10`。  
- **管理**：支持 `ListMemory`（分页查询）、`UpdateMemory`（PATCH 更新内容）、`DeleteMemory`（DELETE 删除）等操作。  
- **画像专用**：需先 `CreateProfileSchema` 定义字段，再 `AddMemory` 时传 `profile_schema`，最后 `GetUserProfile` 获取结果。

### 2. [插件](../concepts/plugin.md)化集成（如 OpenClaw）
- 安装 `@modelstudio/modelstudio-memory-for-openclaw` [插件](../concepts/plugin.md)，配置 `apiKey` 和 `userId` 即可启用 `autoCapture`/`autoRecall`。  
- 插件额外暴露工具：`memory_search`（语义检索）、`memory_store`（直写）、`memory_list`（分页列出）、`memory_forget`（按 ID 删除）[为 OpenClaw 配置长期记忆插件](../../raw/application-user-guide/memory-library-overview/modelstudio-memory-for-openclaw.md)。

### 3. 控制台辅助
- 在 [百炼控制台 → 记忆库](https://bailian.console.aliyun.com/cn-beijing/?tab=app#/memory/list) 查看/编辑规则、调试检索效果、查看记忆详情。  
- 默认记忆库不可删除，但可编辑名称、描述及规则；新记忆库最多支持 50 条片段规则 + 50 条画像规则 [记忆库](../../raw/application-user-guide/memory-library-overview/memory-library.md)。

## 限制和注意事项

- **速率限制**：API 级别限流（阿里云账号维度）—— `AddMemory` ≤ 120 QPM，`SearchMemory` ≤ 300 QPM，所有接口合计 ≤ 3000 QPM。  
- **延迟预期**：`SearchMemory` 端到端延迟 200–500ms，`AddMemory` 500–1000ms；插件模式下 `autoCapture` 异步执行，不影响主响应流。  
- **计费生效时间**：记忆库将于 **2026 年 8 月 20 日 10:00（北京时间）** 正式商业化计费 [记忆库](../../raw/application-user-guide/memory-library-overview/memory-library.md)。  
- **策略版本兼容性**：`plan_version` 大小写不敏感（`"PRO"` ≡ `"pro"`），非法值将报错；修改 MemoryProject 的 `plan_version` 仅影响后续新增记忆，存量记忆不受影响。  
- **画像字段设计**：避免语义重叠字段（如同时定义 `"姓名"`/`"名字"`），单次对话可能无法提取全部字段，建议多轮渐进收集 [长期记忆 API](../../raw/application-user-guide/memory-library-overview/long-term-memory-2-0.md)。  
- **OpenClaw 限制**：记忆插件为全局统一配置，**暂不支持按 Agent 独立配置记忆库或规则** [为 OpenClaw 配置长期记忆插件](../../raw/application-user-guide/memory-library-overview/modelstudio-memory-for-openclaw.md)。

## 来源文档

- [记忆库](../../raw/application-user-guide/memory-library-overview/memory-library.md)
- [长期记忆 API](../../raw/application-user-guide/memory-library-overview/long-term-memory-2-0.md)
- [为 OpenClaw 配置长期记忆插件](../../raw/application-user-guide/memory-library-overview/modelstudio-memory-for-openclaw.md)



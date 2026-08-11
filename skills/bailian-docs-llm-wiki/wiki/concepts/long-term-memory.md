# 长期记忆

长期记忆是百炼平台提供的结构化、语义化用户状态持久化能力，用于突破大模型上下文窗口限制，实现跨会话的用户偏好、关键事件与结构化属性的自动提取、存储与智能召回。它不依赖传统向量检索，而是由平台专用记忆模型驱动，强调意图理解与上下文建模。

## 在百炼平台的不同场景中，这个概念如何使用

- **智能体（Agent）应用**：通过 `AddMemory` / `SearchMemory` 工具自动捕获对话中的待办事项、偏好声明（如“我不吃香菜”）、身份信息等；在 `before_agent_start` 钩子中注入相关记忆，提升多轮决策一致性。
- **工作流（Workflow）应用**：在大模型节点前调用 `SearchMemory` API，将召回的记忆片段作为系统提示或上下文变量注入，增强生成结果的个性化与连贯性。
- **高代码应用（Python SDK）**：集成 `agentscope-runtime` 中的 `AddMemory`、`SearchMemory` 等工具类，实现细粒度控制（如按 `meta_data` 分类写入、指定 `profile_schema` 提取画像）。
- **OpenClaw 框架**：通过 `@modelstudio/modelstudio-memory-for-openclaw` [插件](plugin.md)实现零侵入式记忆管理——自动在 `agent_end` 写入、在 `before_agent_start` 召回，无需修改业务逻辑。
- **记忆库统一管控**：所有记忆操作均归属至逻辑隔离的「记忆库」（`memory_library_id`），支持多租户、多业务线独立配置（如不同产品线使用不同默认库与过期策略）。

## 关键参数和配置

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `user_id` | string | 是 | 用户唯一标识（≤64 字符），所有操作以此为数据隔离边界 |
| `messages` 或 `custom_content` | array / string | 条件必填 | 二选一：传入对话历史（最多 50 条消息）或直接文本（≤512 字符） |
| `memory_library_id` | string | 否 | 指定记忆库 ID（≤32 字符）；不传则使用默认库 |
| `profile_schema` | string | 否 | 指定用户画像 Schema ID，触发结构化字段抽取（如 `age`, `job_title`） |
| `meta_data` | object | 否 | 自定义元数据（如 `{"channel": "wechat", "region": "shanghai"}`），支持后续条件检索 |
| `top_k` | integer | 否（默认 10） | `SearchMemory` 返回的最大条数（1–100） |
| `min_score` | double | 否（默认 0.3） | 相似度阈值 [0,1]，低于此值不返回（注意：部分文档以 0–100 表示，实际 API 接受 0–1 小数） |
| `expiration_time` | string | 否 | 记忆有效期，格式为 ISO8601（如 `"P180D"` 表示 180 天），或 `"P0D"`（永不过期）；控制台可配置默认值 |

> ⚠️ 注意：  
> - 所有 API 调用强制使用平台预置专用记忆模型，**不支持自定义 LLM 替换**；  
> - `AddMemory` 与 `SearchMemory` 均需携带 `Authorization: Bearer $DASHSCOPE_API_KEY`；  
> - 默认无 TTL，但实际控制台可配置 7/30/180 天或永不过期，`expiration_time` 参数优先级高于控制台默认值。

## 面向开发者，简洁实用

- ✅ **快速上手**：只需 `user_id` + `messages` 即可完成记忆写入；搜索时传入自然语言查询（如 `"我上次说的旅行计划"`）即可召回语义相关片段。  
- ✅ **结构化优先**：用 `profile_schema` 定义画像字段，让模型自动从多轮对话中渐进填充（如首次说“我30岁”，后续说“我是设计师”，最终 `GetUserProfile` 返回 `{age: 30, job_title: "设计师"}`）。  
- ✅ **生产就绪**：支持 `enable_rerank`（Pro 模式）提升召回精度；`meta_data` + `top_k` + `min_score` 组合可精准控制召回范围与质量。  
- ✅ **成本可控**：Lite 模式 ¥0.018/次（无重排），Pro 模式 ¥0.03/次（含语义重排），按调用次数计费，无存储费用。  
- 🚫 **避坑提示**：  
  - `messages` 中每条必须含 `role`（`user`/`assistant`）和 `content`；  
  - `SearchMemory` 不接受纯 `query` 字段（旧版接口已弃用），**必须传 `messages` 或 `custom_content`**；  
  - `ListMemory` 分页需配合 `page_num`/`page_size`，默认不返回全部数据。  

如需调试，推荐使用 OpenClaw CLI：  
```bash
openclaw modelstudio-memory search --user-id user_001 --query "我的生日"
```

## 关联主题页

- [long term memory new](../api/long-term-memory-new.md)
- [memory library overview](../guides/memory-library-overview.md)
- [llm application](../guides/llm-application.md)
- [application call](../api/application-call.md)
- [managed agents](../guides/managed-agents.md)



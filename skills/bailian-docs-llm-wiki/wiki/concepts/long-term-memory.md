# 长期记忆

长期记忆是百炼平台提供的结构化、跨会话、可检索的用户状态持久化能力，用于突破大模型上下文窗口限制，将对话中提取的关键事实、意图与用户属性转化为语义化、带生命周期管理的记忆片段，并支持基于 `user_id` 隔离的增删改查与高精度语义召回。

## 在百炼平台的不同场景中，这个概念如何使用

- **智能体（Agent）应用**：作为核心状态增强模块，长期记忆可自动捕获用户偏好（如“会议提醒时间”）、行为习惯（如“常用导出格式”）或任务上下文（如“上一轮分析的指标口径”），并在后续会话中通过 `SearchMemory` 动态注入 Prompt，显著提升多轮交互的一致性与个性化水平。OpenClaw 插件支持 `autoCapture`（对话结束自动写入）和 `autoRecall`（对话开始前自动检索），实现零侵入集成。

- **工作流（Workflow）与高代码应用**：通过标准 REST API 或 `agentscope-runtime` SDK 主动调用 `AddMemory` / `SearchMemory`，在关键节点（如订单确认后、用户反馈收集后）写入结构化记忆；也可结合 `meta_data` 字段按业务标签（如 `"order_stage": "paid"`）分类管理，支撑精细化运营策略。

- **用户画像构建**：配合预定义的 `profile_schema`（字段名、类型、描述），从自然语言对话中自动抽取结构化属性（如 `age: 28`, `preferred_language: "zh"`），形成动态演化的用户画像，供推荐、风控、客服等下游系统调用。

- **记忆库管理**：所有记忆均归属至逻辑隔离的「记忆库」（Memory Library），支持控制台可视化管理、分页浏览（`ListMemory`）、按规则批量清理（如按 `project_id` 或过期时间），并可配置默认有效期（7/30/180 天或永不过期）。

> ⚠️ 注意：长期记忆与 LLM 应用中提到的「0–30 轮短期记忆」完全独立——前者持久化存储于服务端向量数据库，后者仅为当前会话内临时缓存的 token 级上下文，不跨请求、不跨会话。

## 关键参数和配置

| 参数 | 类型 | 必填 | 说明 | 推荐值 |
|------|------|------|------|--------|
| `user_id` | string | 是 | 用户唯一标识，最大 64 字符；所有操作以此为数据域边界，**必须严格保证租户隔离** | `u_123456`（建议业务主键） |
| `messages` / `custom_content` | array / string | 互斥必填 | `messages`: 对话数组（最多 50 条，一问一答计 2 条）；`custom_content`: 纯文本（≤512 字符），优先级更高 | 优先用 `messages` 让平台自动提取语义；纯文本场景用 `custom_content` |
| `memory_library_id` | string | 否 | 指定记忆库存储位置；不传则使用默认库（控制台可见） | 生产环境建议显式指定，便于灰度与迁移 |
| `project_id` | string | 否 | 记忆片段规则 ID，用于区分不同业务场景（如 `"meeting_rules"`, `"support_rules"`）；支持 `SearchMemory` 多规则联合检索 | 按业务域划分，避免混用 |
| `profile_schema` | string | 否 | 用户画像模板 ID；仅当需触发结构化属性抽取时传入 | 创建后复用，避免重复定义 |
| `top_k` | integer | 否 | `SearchMemory` 最大召回数 | **3–10**（平衡精度与 token 开销） |
| `min_score` | double | 否 | 相似度阈值（0.0–1.0），低于此值的结果被过滤 | **0.4–0.6**（默认 0.3 偏宽松，易召回噪声） |
| `enable_rerank` / `enable_rewrite` | boolean | 否 | 是否启用重排序（提升相关性）与 query 重写（优化检索表达） | 高精度场景设为 `true`，但增加延迟 |
| `expiration_days` | integer | 否 | 记忆有效期（天），支持 `7`/`30`/`180` 或 `-1`（永不过期） | **显式设置**，避免依赖默认值导致意外过期 |

> ✅ 提示：`meta_data`（object 类型）可用于自定义分类，例如 `{ "source": "app_chat", "priority": "high" }`，后续可通过 `ListMemory` 的 `filter` 参数（JSONPath 表达式）筛选。

## 面向开发者，简洁实用

- **快速起步三步走**：
  1. 控制台创建记忆库 → 获取 `memory_library_id`；
  2. 调用 `AddMemory` 写入首条记忆（带 `user_id` 和 `messages`）；
  3. 调用 `SearchMemory` 检索（传 `user_id` + 当前问题 `messages`），结果直接拼入 Prompt。

- **SDK 优先**：推荐使用 `agentscope-runtime>=1.1.5`，封装了异步调用、错误重试与鉴权透传，比裸 API 更稳定：
  ```python
  from agentscope_runtime.tools.modelstudio_memory import AddMemory, SearchMemory
  # 写入
  await AddMemory().arun({"user_id": "u1", "messages": [{"role":"user","content":"明天9点开会"}]})
  # 检索（自动注入 context）
  res = await SearchMemory().arun({"user_id": "u1", "messages": [{"role":"user","content":"我明天有什么安排？"}], "top_k": 3})
  context = "\n".join([node.content for node in res.memory_nodes])
  ```

- **调试技巧**：
  - 所有记忆可在控制台 [记忆库页面](https://bailian.console.aliyun.com/cn-beijing/?tab=app#/memory/list) 实时查看、编辑、删除；
  - 使用 `ListMemory` 分页拉取全量数据，验证写入逻辑；
  - 检索不准时，先检查 `min_score` 是否过低，再开启 `enable_rewrite=True` 观察 query 优化效果。

- **生产注意事项**：
  - **限流**：`AddMemory` 单独限流 120 QPM，`SearchMemory` 单独限流 3000 QPM（账号级），请做好客户端降级（如本地缓存最近 3 条）；
  - **安全**：`user_id` 是唯一隔离维度，严禁用会话 ID、设备 ID 等非用户主键替代；
  - **成本**：记忆写入与检索本身不额外计费，但检索结果注入 Prompt 后会增加模型输入 token，计入 LLM 调用费用。

## 关联主题页

- [long term memory new](../api/long-term-memory-new.md)
- [memory library overview](../guides/memory-library-overview.md)
- [managed agents](../guides/managed-agents.md)
- [llm application](../guides/llm-application.md)



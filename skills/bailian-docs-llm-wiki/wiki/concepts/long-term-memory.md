# 长期记忆

长期记忆是百炼平台提供的结构化、跨会话的用户信息持久化能力，通过语义提取、隔离存储与向量检索，突破大模型上下文窗口限制，实现用户偏好、历史事件、结构化画像等关键信息的自动沉淀与智能召回。

## 在百炼平台的不同场景中，这个概念如何使用

- **智能体（Agent）应用**：作为状态延续的核心基础设施，长期记忆支持 Agent 在多轮对话中持续感知用户习惯（如“每天9点提醒喝水”）、任务进度（如“待办事项未完成”）和个性化偏好（如“喜欢简洁回复”）。Managed Agents 运行时可结合 `autoCapture`/`autoRecall` [插件](plugin.md)自动触发记忆写入与检索，无需修改 Agent 内部逻辑。  
- **工作流（Workflow）与高代码应用**：开发者可通过调用 `AddMemory` 和 `SearchMemory` API 主动管理记忆，例如在订单流程节点后写入用户收货偏好，在客服问答节点前检索历史投诉记录，实现业务逻辑驱动的记忆闭环。  
- **OpenClaw 等[插件](plugin.md)生态**：通过官方 `modelstudio-memory-for-openclaw` [插件](plugin.md)，开箱启用自动捕获（基于 `messages` 提取）与自动召回（在每次 LLM 调用前注入相关记忆），降低集成门槛；插件暴露 `memory_search`/`memory_store` 等标准工具供 Agent 动态调用。  
- **RAG 增强场景**：长期记忆与知识库（Knowledge Base）协同使用——知识库承载静态业务文档，长期记忆承载动态用户侧数据（如“张三上月退订了VIP服务”），二者在推理时联合注入上下文，提升回答准确性与个性化程度。  
- **用户画像构建**：配合 `ProfileSchema` 模板（如定义 `age`, `job`, `interests` 字段），从对话中结构化抽取并更新用户画像，支持精准推荐、分群运营等下游场景；`GetUserProfile` 接口可实时获取最新结构化视图。

## 关键参数和配置

| 参数 | 类型 | 必填 | 默认值 | 说明 |
|------|------|------|--------|------|
| `user_id` | string | 是 | — | 用户唯一标识，用于租户级隔离；建议使用业务系统 ID（如 `uid_12345`），禁止含 `/`, `?`, `#` 等 URL 不安全字符。 |
| `messages` / `custom_content` | array / string | 互斥 | — | `messages`: 对话数组（最多 50 条），至少含 1 条 `role: "user"` 消息，用于自动提取事件/意图；`custom_content`: ≤512 字符纯文本，用于直接写入确定性内容（如“用户已同意隐私协议”）。 |
| `memory_library_id` | string | 否 | 默认记忆库 | 记忆库 ID，控制台可查；不同库可配置独立权限与生命周期策略。 |
| `project_id` | string | 否 | 默认规则 | 记忆片段提取规则 ID，决定自动提取的字段与强度（如“宽松提取”或“仅提取明确承诺”）。 |
| `profile_schema` | string | 否 | — | 用户画像模板 ID，需预先创建；指定后 `AddMemory` 将按 Schema 结构化存储字段。 |
| `top_k` | integer | 否 | `5`（插件默认）/`10`（API 默认） | `SearchMemory` 返回的最大结果数，范围 `1–100`。 |
| `min_score` | double | 否 | `0.3`（API）/`0`（插件） | 相似度阈值（[0,1]），低于此值的结果被过滤；建议生产环境设为 `0.4` 以上以保障召回质量。 |
| `autoCapture` / `autoRecall` | boolean | 否 | `true` | 插件模式下控制是否启用自动写入/自动读取；设为 `false` 时需手动调用 API。 |

> ⚠️ 注意：  
> - `AddMemory` 的 `messages` 中若无 `user` 消息，将导致提取失败（返回空或报错）；  
> - 所有记忆默认**永不过期**，但可通过控制台为 `project_id` 绑定的规则设置 7/30/180 天有效期；  
> - `UpdateMemory` 当前**无 Python SDK 封装**，需手动构造 PATCH 请求；  
> - 全接口限流为阿里云账号级：总 QPM ≤ 3000，其中 `add` ≤ 120 QPM，`search` ≤ 300 QPM。

## 面向开发者，简洁实用

- **快速起步**：  
  ```python
  from agentscope.runtime import AddMemory, SearchMemory
  
  # 写入记忆（自动提取）
  AddMemory(
      user_id="uid_123",
      messages=[{"role": "user", "content": "帮我订明天上午10点的会议室"}]
  )
  
  # 检索记忆（自然语言查询）
  results = SearchMemory(
      user_id="uid_123",
      query="我最近订过哪些会议室？",
      top_k=3,
      min_score=0.5
  )
  print([r["content"] for r in results])
  ```

- **认证方式**：所有 HTTP 请求需携带 `Authorization: Bearer $DASHSCOPE_API_KEY`，Base URL 为 `https://dashscope.aliyuncs.com/api/v2/apps/memory/`。  
- **调试建议**：  
  - 使用 `ListMemory(user_id="xxx")` 查看已存记忆，验证提取效果；  
  - 对 `SearchMemory` 结果添加 `debug=True` 参数（SDK 支持），返回相似度分数与匹配片段位置；  
  - 生产环境务必设置 `min_score`，避免低质召回干扰 LLM 推理。  
- **最佳实践**：  
  - 用户首次交互后立即调用 `AddMemory` 写入基础画像（如 `{"name": "李四", "language": "zh"}`）；  
  - 敏感操作（如支付、授权）后同步写入 `custom_content` 标记，避免依赖自动提取；  
  - 定期调用 `DeleteMemory` 清理过期或错误记忆，维持数据质量。

## 关联主题页

- [long term memory new](../api/long-term-memory-new.md)
- [memory library overview](../guides/memory-library-overview.md)
- [managed agents](../guides/managed-agents.md)
- [llm application](../guides/llm-application.md)
- [application support](../guides/application-support.md)



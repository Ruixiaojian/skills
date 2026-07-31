# 长期记忆

长期记忆是百炼平台提供的结构化、可检索的用户状态持久化能力，用于突破大模型上下文窗口限制，实现跨会话、跨对话的语义化信息存储与智能召回。它通过自动提取对话关键事实或接收自定义内容，生成向量化记忆片段，并支持基于语义相似度的高效检索，为智能体提供连贯、个性化的上下文感知能力。

## 在百炼平台的不同场景中如何使用

- **智能体（Agent）应用**：在 `Agent 2.0` 中，长期记忆可通过 OpenClaw 插件自动启用 `autoCapture`（对话结束时自动提取并写入）和 `autoRecall`（新对话开始前自动检索并注入上下文），无需手动调用 API；也可在 [Prompt 工程](prompt-engineering.md)中显式拼接 `SearchMemory` 返回结果，增强推理依据。
- **工作流（Workflow）应用**：作为独立节点接入，通过 `SearchMemory` 节点在流程中动态检索用户历史偏好、待办事项等，驱动分支决策（如“是否已预约？”→ 调用记忆检索 → 分支跳转）。
- **高代码应用（Serverless/K8s）**：直接集成 `agentscope-runtime` SDK（≥1.1.5），调用 `AddMemory` / `SearchMemory` 等工具完成记忆生命周期管理；结合 `GetUserProfile` 可构建带结构化画像的个性化服务。
- **知识增强场景**：与 RAG 协同使用——长期记忆聚焦用户私有状态（如“我过敏花生”），知识库承载通用文档，二者通过不同 `project_id` 或 `memory_library_id` 隔离，避免语义混淆。
- **多应用共享**：多个 LLM Application 可复用同一 `memory_library_id`，实现跨应用的用户状态统一（例如客服机器人与日程助手共享同一用户的提醒设置）。

## 关键参数和配置

| 参数名 | 类型 | 必填 | 说明 | 默认值 |
|--------|------|------|------|--------|
| `user_id` | string | ✓ | 用户唯一标识（≤64 字符），用于严格隔离记忆空间；不同 `user_id` 的数据完全不可见 | — |
| `messages` / `custom_content` | array / string | 互斥必填 | `messages`：最多 50 条对话消息（一问一答计为 2 条），由平台自动提取关键事实；`custom_content`：纯文本（≤512 字符），直接存为记忆片段；二者同时提供时，`custom_content` 优先且 `messages` 被忽略 | — |
| `memory_library_id` | string | ✗ | 显式指定记忆库 ID；未传则使用默认库（可在控制台 [记忆库列表](https://bailian.console.aliyun.com/cn-beijing/?tab=app#/memory/list) 查看） | 默认库 |
| `project_id` | string | ✗ | 指定记忆片段规则 ID；未传则使用对应记忆库的默认规则（支持按业务场景配置不同提取策略，如“会议类” vs “健康类”） | 默认规则 |
| `top_k` | integer | ✗ | `SearchMemory` 返回的最大条数（范围 1–100） | `10` |
| `min_score` | double | ✗ | 相似度阈值（范围 `[0.0, 1.0]`），低于此值的结果被过滤；建议设为 `0.4–0.6` 平衡召回率与精度 | `0.3` |
| `meta_data` | object | ✗ | 自定义键值对（如 `{"source": "mobile_app", "priority": "high"}`），支持在 `UpdateMemory` 中增量更新，用于业务分类、标签或审计追踪 | `{}` |
| `expiration_days` | integer | ✗ | 记忆片段有效期（单位：天），支持 `7`/`30`/`180` 或 `-1`（永不过期）；**注意：该参数需在控制台规则配置中设定，API 不直接传入** | 控制台配置值 |

> ⚠️ 重要说明：  
> - 所有记忆片段与用户画像**无自动过期机制**，实际生命周期由 `expiration_days`（控制台规则配置）决定，而非硬编码逻辑；  
> - `AddMemory` 与 `SearchMemory` 均需传 `user_id`，否则请求失败；  
> - `SearchMemory` 的查询输入推荐使用自然语言问题（如 `"我明天有什么安排？"`）或单条 `messages`，不建议传长对话历史。

## 面向开发者：简洁实用指南

- **快速上手**：安装 `agentscope-runtime>=1.1.5`，用 3 行代码完成写入与检索：
  ```python
  from agentscope_runtime.tools.modelstudio_memory import AddMemory, SearchMemory
  await AddMemory().arun({"user_id": "u123", "messages": [{"role":"user","content":"每周三健身"}]})
  res = await SearchMemory().arun({"user_id": "u123", "messages": [{"role":"user","content":"我的运动计划"}], "top_k": 3})
  ```
- **性能优化**：  
  - `top_k` 建议设为 `3–5`，避免冗余信息干扰模型；  
  - `min_score` 低于 `0.3` 易引入噪声，高于 `0.7` 可能漏召，上线前务必用真实 query 测试调优；  
  - 高频写入场景下，合并多条消息为单次 `AddMemory` 调用（而非逐条），降低 QPM 消耗。
- **调试技巧**：  
  - 使用 `ListMemory` 分页查看已存记忆，验证提取效果；  
  - 在应用监控中筛选 `RETRIEVER` 类型 Span，查看 `SearchMemory` 的实际召回结果、相似度分数及耗时；  
  - 为 `meta_data` 添加 `debug: true` 标签，便于在监控中快速过滤测试数据。
- **生产注意事项**：  
  - `user_id` 必须全局唯一且稳定（推荐用业务系统用户 ID，而非临时 session ID）；  
  - 敏感信息（如身份证号）请勿直接写入 `custom_content`，应先脱敏或走合规加密通道；  
  - 配额限制：`AddMemory` ≤ 120 QPM，`SearchMemory` ≤ 300 QPM（按阿里云账号汇总），超限将返回 `429`。

## 关联主题页

- [long term memory new](../api/long-term-memory-new.md)
- [memory library overview](../guides/memory-library-overview.md)
- [managed agents](../guides/managed-agents.md)
- [llm application](../guides/llm-application.md)
- [application monitoring](../guides/application-monitoring.md)



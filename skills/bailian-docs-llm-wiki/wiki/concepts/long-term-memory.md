# 长期记忆

长期记忆是百炼平台提供的结构化、持久化、语义可检索的记忆管理能力，用于突破大模型上下文窗口限制，实现跨会话、跨请求的用户状态与行为信息持续沉淀与复用。它不是简单的缓存或日志存储，而是通过语义提炼、规则驱动和画像建模，将对话内容或自定义数据转化为高价值记忆片段，并支持低延迟、高召回的向量检索与结构化查询。

## 在百炼平台的不同场景中，这个概念如何使用

- **智能体（Agent）应用**：作为 Agent 的“经验库”，在每轮对话开始前自动检索（`autoRecall`）相关记忆注入上下文，或在对话结束后自动提炼关键意图/事件（如待办、偏好、承诺）写入（`autoCapture`）。支持与 MCP 工具、[知识库](knowledge-base.md)协同完成复杂任务规划（例如：“查我上周预约的医生”需结合记忆中的历史预约记录与[知识库](knowledge-base.md)中的医院信息）。

- **工作流（Workflow）应用**：通过 `memory_search` 工具节点主动调用 `SearchMemory`，在特定流程节点（如“用户身份确认”“个性化推荐”）注入记忆上下文；也可用 `memory_store` 节点在流程末尾持久化关键结果（如订单摘要、服务反馈），供后续流程复用。

- **Managed Agents（托管智能体）**：在沙箱环境中，Agent 可通过 SDK 或 API 主动调用 `AddMemory` / `SearchMemory` 实现记忆闭环——例如执行完文件分析后，将结论写入长期记忆；或在多步任务中，基于历史操作记忆避免重复决策。

- **高代码应用与自定义集成**：通过 RESTful API 或 `agentscope-runtime` SDK 直接集成，适用于需要精细控制记忆生命周期的场景（如金融风控中按用户 ID 隔离敏感行为记忆，或客服系统中按会话 ID 关联工单处理记录）。

- **用户画像构建**：配合 `profile_schema` 定义结构化字段（如 `age`, `preferred_language`, `subscription_tier`），系统从多轮对话中渐进抽取并更新画像，最终通过 `GetUserProfile` 获取统一视图，支撑个性化响应与精准运营。

## 关键参数和配置

| 参数名 | 类型 | 必填 | 说明 | 常用值/建议 |
|--------|------|------|------|-------------|
| `user_id` | string | 是 | 记忆归属实体唯一标识，用于租户级隔离；同一 `user_id` 下所有记忆可互通 | 最大 64 字符，建议使用业务侧用户主键（如 `uid_12345`） |
| `memory_library_id` | string | 否 | 目标记忆库 ID；不传则使用默认库（控制台可查看/编辑） | 默认库不可删除；多应用共享时建议显式指定以避免冲突 |
| `project_id` | string | 否 | 记忆片段提取规则 ID；不传则使用记忆库默认规则 | 规则决定“如何提炼”（如提取待办 vs 提取偏好），单库最多 50 条 |
| `profile_schema_id` | string | 否 | 用户画像模板 ID；仅当需结构化抽取时必填 | 必须先调用 `CreateProfileSchema` 创建，ID 从 `ListProfileSchemas` 返回中获取 |
| `messages` / `custom_content` | array / string | 互斥必填（`AddMemory`） | `messages`: 对话数组（最多 50 条，含 role/content）；`custom_content`: 纯文本（≤512 字符） | 推荐优先用 `messages`，语义更丰富；`custom_content` 适用于非对话源（如 CRM 同步数据） |
| `top_k` | integer | 否（`SearchMemory`） | 检索返回最大条数 | 默认 10；Agent 场景建议 3–5，平衡精度与 token 开销；Workflow 可设为 1–3 |
| `min_score` | double | 否（`SearchMemory`） | 相似度阈值（0.0–1.0） | 默认 0.3；调试建议 0.5–0.7，避免噪声；生产环境可动态调整 |
| `enable_rerank` / `enable_judge` / `enable_rewrite` | boolean | 否（`SearchMemory`） | 语义增强开关：重排序、意图判别、Query 重写 | 高质量场景建议开启；`enable_rerank` 显著提升 Top-K 准确率 |

> ⚠️ 注意：  
> - 所有接口均需 `Authorization: Bearer $DASHSCOPE_API_KEY` 认证；  
> - 记忆过期策略由 `project_id` 对应的规则配置决定（7/30/180 天或永不过期），**非全局默认永不过期**；  
> - `user_id` 是隔离边界，不同 `user_id` 间记忆完全不可见；  
> - OpenClaw 等插件中 `top_k` 和 `min_score` 默认值可能与 API 不同，需显式覆盖。

## 面向开发者，简洁实用

- **快速上手**：  
  ```python
  # 安装依赖
  pip install agentscope-runtime>=1.1.5
  
  # 写入 & 检索（一行代码封装）
  from agentscope_runtime.tools.modelstudio_memory import AddMemory, SearchMemory
  
  await AddMemory().arun({"user_id": "u123", "messages": [{"role":"user","content":"明天9点提醒我吃药"}]})
  result = await SearchMemory().arun({"user_id": "u123", "messages": [{"role":"user","content":"我的提醒有哪些？"}], "top_k": 3})
  ```

- **性能提示**：  
  - `AddMemory` 端到端延迟约 500–1000ms，建议异步调用（如 OpenClaw 的 `autoCapture`）；  
  - `SearchMemory` 延迟约 200–500ms，高频调用请复用 `user_id` + 合理 `top_k`；  
  - 配额限制：`AddMemory` ≤120 QPM，`SearchMemory` ≤300 QPM（账号级）。

- **避坑指南**：  
  - ❌ 不要硬编码 `profile_schema_id` —— 务必通过 `ListProfileSchemas` 动态获取；  
  - ❌ 不要混用 `messages` 和 `custom_content` —— 二者互斥；  
  - ✅ 为 `meta_data` 添加业务标签（如 `{"source": "app_chat", "channel": "wechat"}`），便于后续过滤与审计；  
  - ✅ 在 `SearchMemory` 中传入完整对话消息（含 system/user/assistant），比单 query 效果更优。

长期记忆不是“开箱即用”的黑盒，而是可配置、可观测、可演进的状态中枢。善用规则、画像与语义增强，才能让 Agent 真正记住用户、理解上下文、交付连续体验。

## 关联主题页

- [long term memory new](../api/long-term-memory-new.md)
- [memory library overview](../guides/memory-library-overview.md)
- [llm application](../guides/llm-application.md)
- [managed agents](../guides/managed-agents.md)
- [application component api reference](../api/application-component-api-reference.md)



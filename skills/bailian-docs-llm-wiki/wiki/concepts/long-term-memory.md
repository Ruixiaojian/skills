# 长期记忆

长期记忆是百炼平台提供的结构化、语义驱动的用户信息持久化能力，用于突破大模型上下文窗口限制，实现跨会话、跨轮次的用户偏好、关键事件与画像属性的自动提取、存储与智能召回。它不依赖传统向量库，而是由百炼专属记忆模型驱动，强调上下文感知与语义理解，支持完整生命周期管理（增删改查+画像建模）。

## 在百炼平台的不同场景中，这个概念如何使用

- **智能体（Agent）应用**：作为核心记忆基础设施，支撑 Agent 的持续性理解。可通过 OpenClaw 插件启用 `autoCapture`（对话结束自动提取记忆）与 `autoRecall`（对话开始前自动检索注入），无需手动调用 API；也可在 Agent 工具链中显式调用 `memory_search` 工具进行动态检索。
- **记忆库（Memory Library）**：是长期记忆的载体和管理单元。每个记忆库可配置独立的提取规则（如过期时间、Pro/Lite 模式）、默认项目（`project_id`）及用户画像 Schema。支持多应用共享同一记忆库，实现用户数据统一视图。
- **API 集成场景**：通过 RESTful 接口（如 `AddMemory`、`SearchMemory`）或 `agentscope-runtime` SDK 直接集成到自研系统中，适用于需要精细控制记忆写入时机、内容结构或检索策略的业务逻辑（如客服工单系统、个性化推荐引擎）。
- **Managed Agents 与 LLM 应用**：当前版本中，Managed Agents 和标准 LLM 应用（如工作流、高代码应用）**不原生集成长期记忆能力**；若需使用，必须通过外部 API 调用方式主动接入记忆库服务，无法通过平台内置配置项启用。

> ⚠️ 注意：长期记忆 ≠ 短期记忆（上下文轮数）。LLM 应用中配置的“0–30 轮短期记忆”仅影响单次请求的 [prompt](../guides/prompt.md) 构建，不涉及持久化存储；长期记忆则独立于会话生命周期，数据永久（或按规则过期）保留在服务端。

## 关键参数和配置

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `user_id` | string | 是 | 用户唯一标识（≤64 字符），所有接口必需，用于严格隔离不同用户的数据空间 |
| `memory_library_id` | string | 否 | 记忆库 ID（≤32 字符）；不传则使用账号默认记忆库（不可删除，可编辑） |
| `project_id` | string | 否 | 记忆片段规则 ID；不传则使用对应记忆库的默认项目规则（默认过期时间为 180 天） |
| `profile_schema` | string | 否 | 用户画像 Schema ID；传入后触发结构化属性抽取（如年龄、职业），否则仅处理通用记忆片段 |
| `messages` 或 `custom_content` | array / string | 二选一（仅 `AddMemory`） | `messages`: 最多 50 条对话消息（role/content）；`custom_content`: 纯文本（≤512 字符） |
| `top_k`（SearchMemory） | integer | 否 | 检索返回最大条数，范围 1–100，默认 10（OpenClaw 插件默认为 5） |
| `min_score`（SearchMemory） | double | 否 | 相似度阈值 [0.0, 1.0]，低于此值的结果被过滤，默认 0.3（文档中亦见 `minScore` 形式，单位为 0–100，等价于 `min_score * 100`） |
| `page_num` / `page_size`（ListMemory） | integer | 否 | 分页参数，默认 `page_num=1`, `page_size=10` |
| `meta_data` | object | 否 | 自定义 JSON 元数据（如 `{"category": "health", "source": "chat"}`），可用于后续条件过滤或业务分类 |

- **过期配置**：在记忆库控制台中可为 `project_id` 对应的规则设置过期时间（7/30/180 天或永不过期），**该设置决定记忆片段生命周期，用户画像有效期由其关联的记忆片段决定**。
- **模式选择**：`Pro` 模式启用 Rerank，精度更高（¥0.03/次）；`Lite` 模式无 Rerank，成本更低（¥0.018/次片段 或 ¥0.025/次画像）。

## 面向开发者，简洁实用

- ✅ **推荐起步方式**：安装 `agentscope-runtime>=1.1.5`，用封装类快速调用：
  ```python
  from agentscope.runtime import AddMemory, SearchMemory
  
  # 写入记忆
  AddMemory(user_id="u123", messages=[{"role": "user", "content": "我想每天9点喝水"}]).run()
  
  # 语义检索
  results = SearchMemory(user_id="u123", query="提醒我喝水的时间").run()
  print([r["content"] for r in results])
  ```
- ✅ **HTTP 调用要点**：Header 带 `Authorization: Bearer $DASHSCOPE_API_KEY`，Base URL 为 `https://dashscope.aliyuncs.com/api/v2/apps/memory/`，Content-Type 必须为 `application/json`。
- ⚠️ **避坑提示**：
  - `UpdateMemory` 当前仅 SDK 支持 `AddMemory`/`SearchMemory`，更新操作需直接调用 PATCH 接口；
  - `custom_content` 严格限长 512 字符，超长请先摘要；
  - `user_id` 和 `memory_library_id` 一旦写入不可修改，设计时需确保唯一性和稳定性；
  - 所有接口受阿里云账号级限流约束（总 QPM ≤ 3000，`AddMemory` ≤ 120，`SearchMemory` ≤ 300）；
  - 记忆提取为异步过程，`AddMemory` 返回成功仅表示已接收请求，实际提取完成需约 500–1000ms，画像结果需额外等待约 3 秒后调用 `GetUserProfile` 获取。

## 关联主题页

- [long term memory new](../api/long-term-memory-new.md)
- [memory library overview](../guides/memory-library-overview.md)
- [managed agents](../guides/managed-agents.md)
- [llm application](../guides/llm-application.md)



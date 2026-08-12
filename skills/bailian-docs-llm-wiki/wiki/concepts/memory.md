# 长期记忆

长期记忆是百炼平台提供的结构化、持久化用户上下文管理能力，用于突破大模型单次会话的上下文窗口限制，实现跨会话的用户偏好、习惯、意图与关键事件的自动捕获、语义检索与生命周期管理。

## 在百炼平台的不同场景中，这个概念如何使用

- **智能体（Agent）应用**：在新版 Agent 2.0 中，长期记忆作为可编程工具（`memory_search` / `memory_store` 等）被显式调用，支持在规划阶段动态注入历史上下文；也可通过 OpenClaw [插件](plugin.md)在 `before_agent_start` 和 `agent_end` 钩子中全自动写入与召回，无需修改业务逻辑。  
- **工作流（Workflow）应用**：可在任意节点（如「大模型」或「意图分类」节点）启用「自定义缓存」并配置记忆检索逻辑，将 `SearchMemory` 结果拼接至 Prompt 的 system 或 user 部分，实现个性化上下文增强。  
- **高代码应用**：通过 `agentscope-runtime>=1.1.5` SDK 或直接 HTTP 调用 `/api/v2/apps/memory/` 接口，在 Python 服务中自主控制记忆的增删改查、画像聚合（`GetUserProfile`）及规则切换。  
- **Managed Agents 托管运行时**：虽不内置自动记忆集成，但开发者可在 Session 事件处理逻辑中主动调用长期记忆 API —— 例如在收到 `tool_output` 后提取结果摘要写入记忆，或在新用户消息到达前检索相关历史片段注入系统提示词。

> ✅ 关键共识：长期记忆是**平台级独立服务**，与模型选型、应用类型、运行时环境解耦；所有场景均通过统一 API（或封装 SDK）交互，语义理解与检索由后端专用模型完成，不依赖所用大模型能力。

## 关键参数和配置

| 参数名 | 类型 | 必填 | 说明 | 建议值 |
|--------|------|------|------|--------|
| `user_id` | string | 是 | 用户唯一标识（≤64 字符），用于隔离数据空间；同一用户所有操作共享该 ID | 使用业务侧稳定 ID（如 `uid_12345`），避免会话级随机 ID |
| `memory_library_id` | string | 否 | 记忆库 ID（≤32 字符）；不传则使用账号默认库 | 生产环境建议显式指定，便于权限隔离与监控 |
| `project_id` | string | 否（但强烈建议显式传入） | 记忆片段提取规则 ID；未传时可能因默认规则变更导致行为漂移 | 在控制台「记忆库 → 规则管理」中创建并固定使用，避免隐式依赖 |
| `messages` / `custom_content` | array / string | 互斥必填 | `messages`：最多 50 条对话记录（role + content）；`custom_content`：纯文本（≤512 字符），优先级更高 | 对话后写入用 `messages`；事件摘要/外部系统同步用 `custom_content` |
| `top_k`, `min_score` | integer, double | 否（仅 `SearchMemory`） | 搜索召回控制：`top_k ∈ [1,100]`（默认 10），`min_score ∈ [0,1]`（默认 0.3） | 初期设 `top_k=5`, `min_score=0.4` 平衡精度与噪声；高敏感场景可升至 `0.6` |
| `meta_data` | object | 否 | 自定义元数据（扁平 JSON，如 `{"source": "chat", "priority": "high"}`），支持按字段过滤与高级检索 | 用于业务分类（如 `"channel": "app"`）、时效标记（如 `"valid_until": "2025-12-31"`） |

> ⚠️ 注意：  
> - 记忆片段**默认永不过期**，但可通过 `project_id` 关联的规则配置过期时间（7/30/180 天或永不过期），务必在控制台确认规则有效期；  
> - `UpdateMemory` 当前无 Python SDK 封装，需直接调用 HTTP PATCH 接口；  
> - `profile_schema` 仅在需触发用户画像提取时传入（配合 `CreateProfileSchema` 定义的模板 ID）。

## 面向开发者，简洁实用

- **快速上手**：安装 `pip install agentscope-runtime>=1.1.5`，初始化后一行调用：  
  ```python
  from agentscope.runtime import MemoryClient
  client = MemoryClient(api_key="YOUR_API_KEY")
  # 写入
  client.add_memory(user_id="u123", custom_content="喜欢咖啡，不加糖")
  # 检索
  results = client.search_memory(user_id="u123", query="饮品偏好", top_k=3)
  ```
- **生产就绪**：  
  - 显式传入 `project_id` 和 `memory_library_id`，禁用默认隐式行为；  
  - 对 `AddMemory` 和 `SearchMemory` 分别设置熔断与重试（推荐指数退避）；  
  - 将 `memory_node_id` 存入业务数据库，便于后续精准更新/删除；  
  - 定期调用 `ListMemory` + `DeleteMemory` 清理过期或低质量记忆（如 `meta_data.status == "archived"`）。  
- **调试技巧**：在控制台「记忆库 → 记忆列表」页直接查看、编辑、测试搜索，验证提取效果与语义相关性。

## 关联主题页

- [long term memory new](../api/long-term-memory-new.md)
- [memory library overview](../guides/memory-library-overview.md)
- [llm application](../guides/llm-application.md)
- [managed agents](../guides/managed-agents.md)



# 长期记忆

长期记忆是百炼平台提供的结构化、语义化的用户状态持久化能力，用于突破大模型上下文窗口限制，实现跨会话、跨任务的用户偏好、历史行为与关键事实的持续感知与智能复用。它不是简单的键值存储，而是通过自动语义提炼、向量化索引与多维规则管理，为 Agent 和 LLM 应用提供可检索、可更新、可画像的“记忆中枢”。

## 在百炼平台的不同场景中，这个概念如何使用

- **Agent 场景（Managed Agents / 智能体应用）**：作为核心状态层，支持 `autoCapture`（对话结束自动提炼为记忆片段）和 `autoRecall`（会话启动前自动语义检索并注入系统提示）。开发者可通过 SDK 工具 `memory_search`/`memory_store` 在运行时按需调用，也可在 Agent 系统提示词中引用 `{{user_profile}}` 或 `{{recent_memories}}` 变量（需平台模板支持）。

- **工作流（Workflow）场景**：虽不原生集成自动记忆[插件](plugin.md)，但可通过「大模型节点」调用 `SearchMemory` API 或 `agentscope-runtime` SDK，在流程中显式检索用户画像或历史事件（如“查询该用户最近三次订单偏好”），实现状态驱动的分支决策。

- **高代码应用（Rich Code Application）**：直接调用 RESTful API 或 `agentscope-runtime` SDK 进行细粒度控制，适用于需定制生命周期、混合多源记忆（如合并 CRM 数据与对话记忆）、或构建企业级用户档案的场景。

- **OpenClaw 等第三方框架集成**：通过官方[插件](plugin.md) `@modelstudio/modelstudio-memory-for-openclaw` 一键接入，自动挂载 `memory_search`/`memory_store` 等标准工具，并在 Gateway 层统一处理 `onSessionStart`/`onSessionEnd` 钩子，实现零侵入记忆闭环。

- **记忆库（Memory Library）基础设施层**：以 `memory_library_id` + `project_id` 为维度组织记忆规则，支持多租户隔离、规则版本管理与控制台可视化调试（如调整提取模板、设置过期策略），是所有上层能力的统一底座。

## 关键参数和配置

| 参数名 | 位置 | 类型 | 必填 | 默认值 | 说明 |
|--------|------|------|------|--------|------|
| `user_id` | 请求 body | string | ✅ | — | 用户唯一标识（≤64 字符），所有操作以此为归属边界，**不可为空或占位符（如 `"default"`）** |
| `memory_library_id` | 请求 body | string | ❌ | 默认库 | 控制台创建的记忆库 ID；未指定则写入/检索默认记忆库 |
| `project_id` | 请求 body | string | ❌ | 默认项目 | 决定内容提取规则（如“提取待办事项” vs “提取饮食偏好”），影响 `AddMemory` 的语义提炼结果 |
| `profile_schema` | 请求 body | string | ❌ | — | 用户画像模板 ID，用于结构化字段抽取（如 `age`, `job`, `allergy`），需预先创建 |
| `top_k` | `SearchMemory` body | integer | ❌ | `10`（API） / `5`（[插件](plugin.md)） | 召回最大条数，建议生产环境设为 `3–7` 平衡精度与性能 |
| `min_score` / `similarity_threshold` | `SearchMemory` body | double | ❌ | `0.3`（API） / `0`（插件） | 相似度阈值（0.0–1.0），低于此值的结果被过滤；**生产环境强烈建议设为 `0.5–0.7`** |
| `expiration_time` | `AddMemory` body | integer (seconds) | ❌ | `15552000`（180 天） | 记忆片段自动过期时间（秒），支持 `604800`（7天）、`2592000`（30天）、`0`（永不过期） |

> ⚠️ 注意：`UpdateMemory` 的 `meta_data` 是**增量更新**（PATCH 语义），而 `custom_content` 会**完全覆盖**原文本；`DeleteMemory` 和 `UpdateMemory` 的 `memory_node_id` 必须严格校验合法性，避免越权操作。

## 面向开发者，简洁实用

- **快速开始（推荐）**：安装 `pip install agentscope-runtime>=1.1.5`，使用封装好的异步工具：
  ```python
  from agentscope_runtime.tools.modelstudio_memory import AddMemory, SearchMemory
  
  # 写入记忆（自动提炼对话）
  add_tool = AddMemory(user_id="u123", project_id="proj_abc")
  result = await add_tool.arun(messages=[{"role": "user", "content": "明天上午9点提醒我开会"}])
  
  # 检索记忆（基于当前query语义匹配）
  search_tool = SearchMemory(user_id="u123", top_k=3, min_score=0.6)
  memories = await search_tool.arun(query="会议提醒")
  ```

- **直接调用 API（灵活可控）**：
  - Base URL：`https://dashscope.aliyuncs.com/api/v2/apps/memory/`
  - 认证：Header `Authorization: Bearer $DASHSCOPE_API_KEY`
  - 写入：`POST /add`（支持 `messages` 数组或 `custom_content` 字符串）
  - 检索：`POST /memory_nodes/search`
  - 列表：`GET /memory_nodes?user_id=u123&page_num=1&page_size=10`
  - 更新/删除：`PATCH /memory_nodes/{id}` / `DELETE /memory_nodes/{id}`

- **必做事项**：
  - 显式设置 `expiration_time`，避免记忆无限堆积；
  - 生产环境 `SearchMemory` 务必设置 `min_score ≥ 0.5`，防止低质召回干扰推理；
  - `user_id` 必须业务真实、全局唯一，禁止使用 session_id 或临时 token；
  - `UpdateMemory` 暂无 Python SDK 封装，需手动调用 PATCH 接口（参考 [API 参考文档](../../raw/application-api-reference/long-term-memory-new/long-term-memory-api-reference.md)）。

- **避坑提示**：
  - 所有接口限流为账号级：总计 ≤3000 QPM，`/add` ≤120 QPM，`/memory_nodes/search` ≤300 QPM；
  - 记忆内容（提取后）严格限制 ≤512 字符，超长文本请预处理摘要；
  - `autoRecall` 注入的记忆默认不带 `score` 字段，如需排序请改用 `SearchMemory` 显式调用。

## 关联主题页

- [long term memory new](../api/long-term-memory-new.md)
- [memory library overview](../guides/memory-library-overview.md)
- [managed agents](../guides/managed-agents.md)
- [managed agents api](../api/managed-agents-api.md)
- [llm application](../guides/llm-application.md)



# 长期记忆

长期记忆是百炼平台提供的结构化、持久化、可检索的用户上下文存储能力，用于解决大模型跨会话上下文丢失问题。它将对话历史自动提炼为语义化记忆片段，并支持基于 Schema 的用户画像建模，为智能体、工作流及高代码应用提供统一的长期状态管理基础设施。

## 在百炼平台的不同场景中，这个概念如何使用

- **智能体（Agent 2.0）**：作为短期记忆（会话内 0–30 轮）的补充，长期记忆用于跨会话召回关键信息（如用户偏好、待办事项、历史承诺）。开发者可通过 `SearchMemory` 工具在 Agent 规划阶段主动检索，或通过 OpenClaw 插件启用 `autoRecall` 实现无感注入。
  
- **工作流（Workflow）**：在大模型节点中，通过显式调用 `memory_search` 工具（或直接集成 `SearchMemory` API）将长期记忆注入 `input` 上下文，增强决策依据；配合 `memory_store` 可在流程关键节点（如用户确认后）持久化新信息。

- **高代码应用**：在 Python 服务中直接调用 `AddMemory` / `SearchMemory` SDK 或 RESTful API，实现与业务逻辑深度耦合的记忆写入与召回（例如：订单创建后存为记忆，客服会话中自动检索用户历史投诉）。

- **Managed Agents**：虽自身具备沙箱级会话状态，但长期记忆用于补充其“有状态”之外的全局用户画像（如职业、设备习惯），可在系统提示词中注入 `GetUserProfile` 结果，或在工具调用链中触发记忆检索以支持长周期任务（如“按用户过往饮食记录生成本周菜谱”）。

> ⚠️ 注意：长期记忆与智能体/工作流的**短期记忆（in-session cache）完全独立**——前者持久化、跨会话、需显式调用；后者临时、单次会话有效、由平台自动维护。

## 关键参数和配置

| 参数 | 类型 | 必填 | 说明 | 场景建议 |
|------|------|------|------|----------|
| `user_id` | string | ✅ | 用户唯一标识（≤64 字符），所有操作以此隔离空间。不同用户间记忆完全不可见。 | 生产环境必须绑定真实用户体系 ID（如 `uid_12345`），避免使用测试 ID。 |
| `memory_library_id` | string | ❌ | 记忆库 ID（≤32 字符）。不传则使用默认库；多租户或多业务隔离时建议显式指定。 | 多应用共享同一记忆库时，通过 `user_id` 隔离；多业务线建议为每个业务分配独立 `memory_library_id`。 |
| `project_id` / `project_ids` | string / list | ❌ | 记忆片段规则 ID（单个或列表）。决定内容提取逻辑（如“提取待办” vs “提取偏好”）。不传则用默认规则。 | 推荐为不同业务意图预置专用规则（如 `reminder_rule`, `profile_rule`），提升提取准确率。 |
| `top_k` | integer | ❌（默认 5–10） | `SearchMemory` 最大召回数。范围 1–100。 | 平衡效果与性能：多数场景设为 `3–5`；RAG 增强可设 `10`，但需注意 [Token](token.md) 消耗。 |
| `min_score` | double | ❌（默认 0.3–0.4） | 相似度阈值（[0,1]）。低于此值的结果被过滤。 | 初期建议 `0.3`；对精度要求高时（如医疗咨询）可升至 `0.5–0.6`，避免噪声干扰。 |
| `enable_rerank` | boolean | ❌（默认 `false`） | 启用重排模型优化排序质量。开启后延迟略增（+100–200ms），显著提升相关性。 | 对召回质量敏感的场景（如客服、个人助理）强烈建议开启。 |
| `enable_rewrite` | boolean | ❌（默认 `false`） | 启用查询改写（Query Rewriting），将自然语言问题转为更利于检索的表述。 | 适用于用户输入模糊的场景（如“我上次说的那个事？”），推荐与 `enable_rerank` 联用。 |
| `expiration` | integer（秒） | ❌ | 记忆片段有效期（秒）。不传则永不过期；传入后覆盖规则级默认过期策略（如 180 天）。 | 敏感信息（如验证码、临时授权）务必显式设置短时效（如 `3600` = 1 小时）。 |

- **写入方式二选一**（仅 `AddMemory`）：
  - `messages`: 数组，最多 50 条对话（含 `role: "user"/"assistant"`），平台自动提炼事件；
  - `custom_content`: 字符串（≤512 字符），绕过自动提炼，直接存为原始文本记忆。

- **元数据支持**：所有写入接口支持 `meta_data` 字段（object），可用于分类（`{"category": "reminder"}`）、来源标记（`{"source": "workflow_order"}`）或业务标签，后续可结合 `SearchMemory` 的过滤能力使用。

## 面向开发者，简洁实用

- ✅ **快速起步**：  
  ```bash
  # 添加一条记忆（自动提炼）
  curl -X POST https://dashscope.aliyuncs.com/api/v2/apps/memory/add \
    -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
    -H "Content-Type: application/json" \
    -d '{"user_id":"u123","messages":[{"role":"user","content":"帮我订明早9点的会议室"}]}'

  # 检索（带重排+阈值）
  curl -X POST https://dashscope.aliyuncs.com/api/v2/apps/memory/memory_nodes/search \
    -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
    -H "Content-Type: application/json" \
    -d '{"user_id":"u123","messages":[{"role":"user","content":"我有哪些预约？"}],"top_k":3,"min_score":0.4,"enable_rerank":true}'
  ```

- ✅ **Python SDK（推荐）**：  
  安装 `agentscope-runtime>=1.1.5`，使用封装好的异步工具：
  ```python
  from agentscope_runtime.tools.modelstudio_memory import AddMemory, SearchMemory

  # 写入
  add_tool = AddMemory()
  await add_tool(user_id="u123", messages=[{"role":"user","content":"每天提醒喝水"}])

  # 检索（返回 List[dict]，含 `id`, `content`, `score`, `meta_data`）
  search_tool = SearchMemory()
  results = await search_tool(
      user_id="u123",
      messages=[{"role":"user","content":"我的健康习惯"}],
      top_k=3,
      min_score=0.4,
      enable_rerank=True
  )
  ```

- ✅ **避坑指南**：
  - `UpdateMemory` 当前 **Python SDK 未封装**，请直接用 `requests` 调用 REST API；
  - `SearchMemory` 的 `query` 字段（纯字符串）与 `messages` 字段（对话数组）**互斥**，优先用 `messages` 以获得更优语义理解；
  - 所有 API 均受速率限制（`SearchMemory` ≤ 300 QPM），高频调用需加本地缓存或批量聚合；
  - 记忆内容计入模型输入 [Token](token.md) —— 检索结果若用于 LLM 提示，需评估总 [Token](token.md) 消耗，避免超限。

## 关联主题页

- [long term memory new](../api/long-term-memory-new.md)
- [memory library overview](../guides/memory-library-overview.md)
- [llm application](../guides/llm-application.md)
- [managed agents](../guides/managed-agents.md)



# 长期记忆

长期记忆是百炼平台提供的结构化、持久化用户上下文管理能力，用于突破大模型单次对话的上下文窗口限制，实现跨会话、跨对话的关键信息沉淀与语义化召回。它不依赖特定大模型，而是通过专用记忆库、向量引擎与规则引擎协同工作，自动提取事实、构建画像，并支持完整的 CRUD 与语义搜索操作。

## 在百炼平台的不同场景中如何使用

- **智能体（Agent）应用**：在 Agent 2.0 中，长期记忆作为可规划工具接入，支持对话结束自动写入（`AddMemory`）、对话开始前按需检索并注入 Prompt（`SearchMemory`），显著增强智能体的持续理解与个性化响应能力；可通过 `meta_data` 标记来源（如 `{"source": "meeting_summary"}`）实现精准过滤。
  
- **工作流（Workflow）应用**：在可视化编排中，可将 `AddMemory`、`SearchMemory` 等作为独立节点插入流程，例如在“日程确认”节点后调用 `AddMemory` 记录用户偏好，在“任务提醒”节点前调用 `SearchMemory` 获取历史安排，实现状态驱动的自动化决策。

- **高代码应用**：开发者可直接集成 `agentscope-runtime>=1.1.5` 提供的 SDK 工具类（`AddMemory`、`SearchMemory`、`ListMemory`），或调用 REST API 实现细粒度控制；适用于需自定义生命周期管理（如定时清理过期记忆）、多租户隔离（按 `user_id` + `memory_library_id` 分库）或与业务数据库联动的复杂场景。

> ⚠️ 注意：长期记忆与短期记忆（即对话历史轮数）完全正交——前者持久化存储于服务端记忆库，后者仅保留在当前会话 [Token](token.md) 上下文中，二者应协同使用而非替代。

## 关键参数和配置

| 参数名 | 类型 | 必填 | 说明 | 常用值 |
|--------|------|------|------|--------|
| `user_id` | string | 是 | 用户唯一标识（≤64 字符），用于数据空间隔离；建议与业务系统用户 ID 对齐 | `"u_123456"` |
| `messages` / `custom_content` | array / string | 互斥必填 | `messages`：最多 50 条对话记录，触发自动事件提取；`custom_content`：≤512 字符纯文本，绕过提取逻辑，直存为记忆片段 | `{"role":"user","content":"我过敏源是花生"}` 或 `"过敏源：花生"` |
| `memory_library_id` | string | 否 | 目标记忆库 ID（≤32 字符）；不传则使用默认库；多租户/多业务线建议显式指定 | `"lib_prod_user_prefs"` |
| `project_id` | string | 否 | 记忆片段提取规则 ID；不传则使用该库默认规则；可在控制台配置规则（如提取时效、字段白名单） | `"rule_v2_daily_habits"` |
| `profile_schema` | string | 否 | 用户画像 Schema ID；配合 `CreateProfileSchema` 定义后，可触发结构化属性抽取（如年龄、饮食禁忌） | `"schema_health_profile"` |
| `top_k` | integer | 否（Search/List） | 搜索/列表返回最大条数；平衡效果与性能，推荐 3–10 | `5`（默认） |
| `min_score` / `similarity_threshold` | double | 否（Search） | 相似度阈值（0.0–1.0）；低于此值的结果被过滤；注意：SDK 使用 `min_score`，部分旧接口文档称 `similarity_threshold`，语义相同 | `0.4`（推荐起点） |
| `meta_data` | object | 否 | 自定义 JSON 键值对，随记忆持久化；可用于分类、权限控制或后续业务逻辑路由 | `{"category": "health", "priority": 1}` |
| `expire_after_days` | integer | 否 | 记忆有效期（天）；不传则按规则默认值（控制台可设 7/30/180 天或 -1 表示永不过期） | `-1`（永不过期） |

> ✅ 最佳实践：  
> - 写入时优先用 `messages` 触发语义提取，确保信息结构化；  
> - 检索时传 `messages`（而非 `query`）更稳定，因平台会自动构造高质量查询向量；  
> - 所有 `user_id` 应做标准化（如小写、去空格），避免同一用户产生多个记忆空间。

## 面向开发者的快速上手

```python
# Python SDK（需 agentscope-runtime>=1.1.5）
from agentscope_runtime.tools.modelstudio_memory import AddMemory, SearchMemory, ListMemory

# 添加记忆（自动提取）
await AddMemory().arun({
    "user_id": "u1",
    "messages": [{"role":"user","content":"我每天早上7点喝咖啡"}],
    "meta_data": {"category": "habit"}
})

# 语义搜索（基于当前对话意图）
await SearchMemory().arun({
    "user_id": "u1",
    "messages": [{"role":"user","content":"我早上一般做什么？"}],
    "top_k": 3,
    "min_score": 0.35
})

# 分页查看（调试/审计用）
await ListMemory().arun({
    "user_id": "u1",
    "page_num": 1,
    "page_size": 20
})
```

- **认证**：所有 API 请求需携带 `Authorization: Bearer $DASHSCOPE_API_KEY`  
- **限流**：`AddMemory` ≤120 QPM，`SearchMemory` ≤300 QPM（阿里云账号级）  
- **生命周期管理**：记忆无自动过期，需业务侧主动调用 `DeleteMemory` 或按 `expire_after_days` 规则清理  

完整接口定义、错误码及更多语言 SDK 示例，请参考 [长期记忆（新）API 参考](../../raw/application-api-reference/long-term-memory-new/long-term-memory-api-reference.md)。

## 关联主题页

- [long term memory new](../api/long-term-memory-new.md)
- [memory library overview](../guides/memory-library-overview.md)
- [llm application](../guides/llm-application.md)



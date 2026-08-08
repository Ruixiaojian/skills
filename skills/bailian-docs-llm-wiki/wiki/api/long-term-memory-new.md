# long term memory new

[长期记忆](../concepts/long-term-memory.md)（新）是百炼平台提供的结构化记忆存储与检索能力，支持将对话自动提炼为语义化记忆片段，并基于画像模板构建用户画像。该能力通过 RESTful API 和 Python SDK 提供，适用于需要持久化、可检索、可更新用户上下文的智能体应用。所有接口均需使用 DashScope API Key 进行认证，详见 [长期记忆（新）API 参考](../../raw/application-api-reference/long-term-memory-new/long-term-memory-api-reference.md)。

## 支持的模型/功能

- **记忆片段管理**：支持添加（`AddMemory`）、搜索（`SearchMemory`）、列出（`ListMemory`）、删除（`DeleteMemory`）和更新（`UpdateMemory`）记忆片段；
- **用户画像建模**：支持创建、查询、更新、删除画像模板（`ProfileSchema`），并基于模板生成/获取用户画像（`GetUserProfile`）；
- **语义检索增强**：`SearchMemory` 支持 `top_k`、`min_score`、`enable_rerank`、`enable_rewrite` 等参数控制召回质量；
- **多规则混合检索**：可通过 `project_ids` 参数指定多个记忆片段规则 ID，实现跨规则联合检索。

> **注意**：原始文档中 `UpdateMemory` 的 Python SDK 封装状态存在不一致——文档明确说明“Python SDK 暂未提供此接口的封装”，但其他接口（如 `AddMemory`）均给出 `agentscope-runtime` 调用示例。开发者应以 [长期记忆（新）API 参考](../../raw/application-api-reference/long-term-memory-new/long-term-memory-api-reference.md) 中的代码示例为准，对 `UpdateMemory` 建议直接使用 `requests` 调用。

## 关键参数

| 参数名 | 类型 | 必填 | 说明 | 来源 |
|--------|------|------|------|------|
| `user_id` | string | 是 | 记忆实体唯一标识，≤64 字符；所有接口均需传入 | [长期记忆（新）API 参考](../../raw/application-api-reference/long-term-memory-new/long-term-memory-api-reference.md) |
| `messages` / `custom_content` | array / string | 互斥必填 | `AddMemory` 中二选一：`messages` 支持最多 50 条对话（含 user/assistant 角色），`custom_content` 为纯文本（≤512 字符） | [长期记忆（新）API 参考](../../raw/application-api-reference/long-term-memory-new/long-term-memory-api-reference.md) |
| `memory_library_id` | string | 否 | 记忆库 ID（≤32 字符）；不传则使用默认记忆库 | [长期记忆（新）API 参考](../../raw/application-api-reference/long-term-memory-new/long-term-memory-api-reference.md) |
| `top_k` | integer | 否 | `SearchMemory` 最大召回数，默认 10，范围 1–100 | |
| `min_score` | double | 否 | `SearchMemory` 相似度阈值，默认 0.3，范围 [0,1] | |
| `project_id` / `project_ids` | string / list | 否 | 单规则 ID 或多规则 ID 列表；不传则使用默认规则 | |

## 使用方式

### 1. 基础配置
- Base URL：`https://dashscope.aliyuncs.com/api/v2/apps/memory/`
- 认证：Header 中携带 `Authorization: Bearer $DASHSCOPE_API_KEY`
- Content-Type：`application/json`

### 2. 接口调用示例（关键场景）

- **添加记忆**（推荐 `messages` 方式）：
  ```bash
  curl -X POST https://dashscope.aliyuncs.com/api/v2/apps/memory/add \
    -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
    -H "Content-Type: application/json" \
    -d '{
      "user_id": "user_001",
      "messages": [{"role":"user","content":"明天10点提醒我整理会议纪要"}],
      "meta_data": {"source": "chat"}
    }'
  ```

- **语义搜索**（带过滤与重排）：
  ```bash
  curl -X POST https://dashscope.aliyuncs.com/api/v2/apps/memory/memory_nodes/search \
    -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
    -H "Content-Type: application/json" \
    -d '{
      "user_id": "user_001",
      "messages": [{"role":"user","content":"我有什么待办？"}],
      "top_k": 5,
      "min_score": 0.4,
      "enable_rerank": true
    }'
  ```

- **Python SDK（需 `agentscope-runtime>=1.1.5`）**：
  ```python
  from agentscope_runtime.tools.modelstudio_memory import AddMemory, SearchMemory
  # AddMemory 和 SearchMemory 均支持异步调用，使用后需显式 close()
  ```

## 限制和注意事项

- **限流策略（阿里云账号级别）**：
  - 所有接口总计 ≤ 3000 QPM；
  - `AddMemory` ≤ 120 QPM；
  - `SearchMemory` ≤ 300 QPM；
- **数据时效性**：当前生成的记忆片段与用户画像**无自动过期机制**，需业务侧自行管理生命周期；
- **内容长度**：
  - `custom_content` ≤ 512 字符；
  - `messages` 最多 50 条（一问一答计为 2 条）；
- **ID 约束**：`user_id` ≤ 64 字符，`memory_library_id` ≤ 32 字符；
- **SDK 兼容性**：`UpdateMemory` 和 `DeleteMemory` 的 Python SDK 封装尚未同步至 `agentscope-runtime` 主干，建议优先使用 REST API 调用，或参考 [长期记忆（新）API 参考](../../raw/application-api-reference/long-term-memory-new/long-term-memory-api-reference.md) 中的 `requests` 示例实现。

## 来源文档

- [长期记忆（新）API 参考](../../raw/application-api-reference/long-term-memory-new/long-term-memory-api-reference.md)



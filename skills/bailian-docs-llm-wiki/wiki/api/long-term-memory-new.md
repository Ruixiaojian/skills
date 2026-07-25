# long term memory new

[长期记忆](../concepts/long-term-memory.md)（新）是百炼平台提供的结构化用户记忆管理能力，支持自动从对话中提取关键信息、构建用户画像，并提供语义搜索、增删改查等完整生命周期操作。该功能基于专用记忆库和规则引擎实现，适用于需要持久化用户偏好、习惯、意图等上下文的智能体应用。详细接口定义与行为规范请参见 [长期记忆（新）API 参考](../../raw/application-api-reference/long-term-memory-new/long-term-memory-api-reference.md)。

## 支持的模型/功能

- **核心能力**：记忆片段自动提取（基于对话 `messages` 或自定义文本 `custom_content`）、多维度语义搜索、分页列表、单条更新/删除、用户画像模板（Profile Schema）管理及画像获取。
- **模型无关性**：底层不依赖特定大模型，所有语义理解、提取与检索逻辑由平台统一服务封装，开发者无需自行调用 LLM。
- **画像支持**：通过 `CreateProfileSchema` 等接口定义结构化画像模板，并关联至记忆库；后续可通过 `GetUserProfile` 获取聚合后的用户画像快照。该机制在 [长期记忆（新）API 参考](../../raw/application-api-reference/long-term-memory-new/long-term-memory-api-reference.md) 中有完整说明。

## 关键参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `user_id` | string | 是 | 记忆归属实体 ID（≤64 字符），用于隔离不同用户数据。所有接口均需传入。 |
| `messages` / `custom_content` | array / string | 互斥必填 | `AddMemory` 和 `SearchMemory` 中，`messages` 为对话数组（最多 50 条，一问一答计 2 条），`custom_content` 为纯文本（≤512 字符），二者不可共存。 |
| `memory_library_id` | string | 否 | 记忆库 ID（≤32 字符）。未传时使用默认记忆库，详见 [长期记忆（新）API 参考](../../raw/application-api-reference/long-term-memory-new/long-term-memory-api-reference.md)。 |
| `top_k`, `min_score` | integer, double | 否 | `SearchMemory` 专属：控制召回数量（1–100，默认 10）和最小相似度阈值（[0,1]，默认 0.3）。 |
| `page_num`, `page_size` | integer | 否 | `ListMemory` 分页参数（默认 page_num=1, page_size=10）。 |

> **注意**：`project_id`（记忆片段规则 ID）在文档中描述为“如不传则自动选择默认规则”，但实际调用中若记忆库未配置任何规则，将返回 400 错误。建议显式传入或确保记忆库已启用默认规则。

## 使用方式

- **HTTP 直接调用**：Base URL 为 `https://dashscope.aliyuncs.com/api/v2/apps/memory/`，所有请求需携带 `Authorization: Bearer $DASHSCOPE_API_KEY` 和 `Content-Type: application/json`。各接口路径见下表：

  | 接口 | 方法 | 路径 | 用途 |
  |------|------|------|------|
  | AddMemory | POST | `/add` | 添加记忆片段（自动提取） |
  | SearchMemory | POST | `/memory_nodes/search` | 语义搜索记忆片段 |
  | ListMemory | GET | `/memory_nodes` | 分页列出记忆片段 |
  | DeleteMemory | DELETE | `/memory_nodes/{memory_node_id}` | 删除指定记忆片段 |
  | UpdateMemory | PATCH | `/memory_nodes/{memory_node_id}` | 更新记忆片段内容 |

- **Python SDK 封装**：推荐使用 `agentscope-runtime>=1.1.5` 提供的工具类（如 `AddMemory`, `SearchMemory`, `ListMemory`, `DeleteMemory`），简化异步调用与错误处理。`UpdateMemory` 当前未封装，需自行用 `requests.patch` 调用（示例见原始文档）。

## 限制和注意事项

- **限流策略**（阿里云账号级别）：
  - 全部接口总计 ≤ 3000 QPM；
  - `AddMemory` ≤ 120 QPM；
  - `SearchMemory` ≤ 300 QPM。
- **数据时效性**：生成的记忆片段与用户画像**无自动过期机制**，需业务侧自行管理生命周期。
- **内容长度**：`custom_content` 严格限制为 ≤512 字符；`messages` 中单条 `content` 长度未明确定义，但整体 `messages` 数组上限为 50 条。
- **元数据（meta_data）**：仅 `AddMemory` 和 `UpdateMemory` 支持写入，`ListMemory` 返回时包含完整 `meta_data` 对象，其他接口不透出。
- **ID 唯一性**：`user_id` 由业务方保证全局唯一；`memory_node_id` 由平台生成，不可自定义。

## 来源文档

- [长期记忆（新）API 参考](../../raw/application-api-reference/long-term-memory-new/long-term-memory-api-reference.md)



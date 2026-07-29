# long term memory new

[长期记忆](../concepts/long-term-memory.md)（新）是百炼平台提供的结构化用户状态持久化能力，支持自动从对话中提取关键信息、构建用户画像，并提供语义搜索、增删改查等完整生命周期管理。该能力基于专用记忆模型实现，无需开发者自行训练或部署 Embedding 模型。所有 API 均通过 `https://dashscope.aliyuncs.com/api/v2/apps/memory/` 统一入口访问，认证方式为 Bearer [Token](../concepts/token.md) [原文标题](../../raw/application-api-reference/long-term-memory-new/long-term-memory-api-reference.md)。

## 支持的模型与功能

- **底层模型**：由百炼平台统一托管的记忆专用模型（非公开型号），不开放模型选择，所有接口均自动路由至最优模型。
- **核心功能**：
  - `AddMemory`：自动解析对话（最多 50 条消息）或接收自定义文本，生成结构化记忆片段，并可关联画像模板；
  - `SearchMemory`：基于语义相似度检索，支持 `top_k`、`min_score`、`enable_rerank` 等精细控制；
  - `ListMemory` / `DeleteMemory` / `UpdateMemory`：标准 CRUD 操作；
  - `ProfileSchema` 系列接口：管理用户画像模板（创建、更新、删除、获取），用于约束记忆提取的字段结构；
  - `GetUserProfile`：按模板拉取聚合后的用户画像快照。

> **注意**：文档中提及的 `agentscope-runtime>=1.1.5` SDK 封装了 `AddMemory`、`SearchMemory`、`ListMemory`、`DeleteMemory` 四个工具，但明确说明 `UpdateMemory` “Python SDK 暂未提供此接口的封装” [原文标题](../../raw/application-api-reference/long-term-memory-new/long-term-memory-api-reference.md)，需直接调用 REST API 实现。

## 关键参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `user_id` | string | 是 | 记忆归属标识，最大 64 字符；所有接口均需传入，用于隔离不同用户数据 |
| `memory_library_id` | string | 否 | 记忆库 ID（32 字符），不传则使用默认库；可在[控制台记忆库列表页](https://bailian.console.aliyun.com/cn-beijing/?tab=app#/memory/list)获取 [原文标题](../../raw/application-api-reference/long-term-memory-new/long-term-memory-api-reference.md) |
| `messages` 或 `custom_content` | array / string | 互斥必填 | `AddMemory` 中二选一：`messages` 为 role/content 对话数组（一问一答计 2 条），`custom_content` 为纯文本（≤512 字符） |
| `top_k` | integer | 否（SearchMemory） | 召回数量，默认 10，范围 1–100 |
| `min_score` | double | 否（SearchMemory） | 相似度阈值，默认 0.3，范围 [0,1] |
| `profile_schema` | string | 否（AddMemory） | 画像模板 ID，影响记忆提取字段；在记忆库详情页获取 [原文标题](../../raw/application-api-reference/long-term-memory-new/long-term-memory-api-reference.md) |

## 使用方式

1. **认证**：所有请求 Header 需携带 `Authorization: Bearer $DASHSCOPE_API_KEY`，API Key 获取方式见[官方指南](https://help.aliyun.com/zh/model-studio/get-api-key)。
2. **SDK 调用（推荐）**：
   - 安装：`pip install agentscope-runtime>=1.1.5`
   - 示例（AddMemory）：
     ```python
     from agentscope_runtime.tools.modelstudio_memory import AddMemory, Message, AddMemoryInput
     result = await AddMemory().arun(AddMemoryInput(
         user_id="user_001",
         messages=[Message(role="user", content="每天9点提醒我喝水")]
     ))
     ```
3. **REST 直连（如 UpdateMemory）**：
   - PATCH `/api/v2/apps/memory/memory_nodes/{memory_node_id}`
   - Body 包含 `user_id`、`custom_content` 等必需字段。

## 限制和注意事项

- **限流**：全接口总计 ≤3000 QPM（阿里云账号级）；其中 `AddMemory` ≤120 QPM，`SearchMemory` ≤300 QPM。
- **数据时效**：当前生成的记忆片段与用户画像**无自动失效机制**，需业务层自行管理生命周期 [原文标题](../../raw/application-api-reference/long-term-memory-new/long-term-memory-api-reference.md)。
- **内容长度**：`custom_content` 最大 512 字符；`messages` 最多 50 条记录。
- **字段覆盖**：`UpdateMemory` 的 `meta_data` 为**增量更新**（非全量替换），仅合并新键值对。
- **时间戳**：`UpdateMemory` 的 `timestamp` 字段为秒级 Unix 时间戳（可选），若不传则使用请求时刻。

## 来源文档

- [长期记忆（新）API 参考](../../raw/application-api-reference/long-term-memory-new/long-term-memory-api-reference.md)



# long term memory new

[长期记忆](../concepts/long-term-memory.md)（新）是百炼平台提供的结构化用户状态持久化能力，支持自动从对话中提取关键信息生成记忆片段，并提供语义搜索、增删改查等完整生命周期管理。该功能基于专用记忆库和画像模板机制，适用于需要跨会话维持用户上下文的智能体应用。所有接口均需通过 `Authorization: Bearer $DASHSCOPE_API_KEY` 认证，Base URL 为 `https://dashscope.aliyuncs.com/api/v2/apps/memory/`。

## 支持的模型/功能

- **核心能力**：自动从多轮对话（`messages`）中提取结构化记忆片段；也支持直接提交自定义文本（`custom_content`）。
- **画像建模**：通过 `CreateProfileSchema` 等接口定义用户画像模板，并关联至记忆库，实现结构化元数据管理。
- **语义检索**：`SearchMemory` 基于向量相似度召回，支持 `top_k`、`min_score`、重排序（`enable_rerank`）及 query 重写（`enable_rewrite`）等控制参数。
- **全量 CRUD**：除基础记忆操作外，还提供 `ListMemory` 分页查询、`UpdateMemory` 内容与元数据增量更新、`DeleteMemory` 物理删除。
- **SDK 封装**：Python 客户端已通过 `agentscope-runtime>=1.1.5` 提供 `AddMemory`、`SearchMemory`、`ListMemory`、`DeleteMemory` 四个封装工具类；`UpdateMemory` 暂未封装，需直接调用 HTTP API [原文标题](../../raw/application-api-reference/long-term-memory-new/long-term-memory-api-reference.md)。

## 关键参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `user_id` | string | 是 | 记忆归属实体 ID（≤64 字符），用于隔离不同用户的数据空间 |
| `messages` / `custom_content` | array / string | 互斥 | `messages` 最多 50 条（一问一答计 2 条）；`custom_content` ≤512 字符 |
| `memory_library_id` | string | 否 | 显式指定记忆库 ID（≤32 字符），不传则使用默认库 [原文标题](../../raw/application-api-reference/long-term-memory-new/long-term-memory-api-reference.md) |
| `profile_schema` | string | 否 | 画像模板 ID，需提前通过 `CreateProfileSchema` 创建并获取 |
| `top_k` | integer | 否 | `SearchMemory` 最大召回数（1–100，默认 10） |
| `min_score` | double | 否 | `SearchMemory` 相似度阈值 [0,1]（默认 0.3） |
| `meta_data` | object | 否 | 用户自定义键值对，支持在 `AddMemory`、`UpdateMemory` 中传入，`ListMemory` 返回时包含该字段 |

> **注意**：`AddMemory` 接口文档中明确说明 `messages` 与 `custom_content` 互斥，且填 `custom_content` 后会忽略 `messages`；但部分旧版示例代码曾同时携带二者，实际以 [原文标题](../../raw/application-api-reference/long-term-memory-new/long-term-memory-api-reference.md) 为准。

## 使用方式

1. **初始化认证**：在请求 Header 中设置 `Authorization: Bearer $DASHSCOPE_API_KEY` 和 `Content-Type: application/json`。
2. **添加记忆**：
   - 推荐使用 `AddMemory` 工具类（Python SDK），传入 `user_id` + `messages` 或 `custom_content`；
   - 若需强控制，可直接调用 `/add` 接口，参考 cURL 示例 [原文标题](../../raw/application-api-reference/long-term-memory-new/long-term-memory-api-reference.md)。
3. **检索记忆**：调用 `SearchMemory`，传入当前对话上下文（`messages`）触发语义匹配；建议设置 `min_score ≥ 0.4` 避免低质召回。
4. **管理记忆**：
   - 列表分页：`ListMemory` 支持 `page_num`/`page_size`；
   - 更新内容：`UpdateMemory` 仅接受 `PATCH` 请求，路径含 `memory_node_id`，Body 必须含 `custom_content`；
   - 删除操作：`DeleteMemory` 为 `DELETE` 请求，路径含 `memory_node_id`。

## 限制和注意事项

- **限流策略**（阿里云账号级别）：
  - 所有接口总 QPM ≤ 3000；
  - `AddMemory` 单独限流 120 QPM；
  - `SearchMemory` 单独限流 300 QPM。
- **数据时效性**：生成的记忆片段与用户画像暂无自动过期机制，需业务侧自行维护生命周期。
- **ID 约束**：`user_id`、`memory_library_id`、`memory_node_id` 均为字符串，长度分别 ≤64、≤32、长度未明确定义但实践中为 UUID 格式。
- **SDK 兼容性**：`agentscope-runtime>=1.1.5` 是最低要求；`UpdateMemory` 尚未封装，需手动构造 PATCH 请求。
- **错误处理**：所有接口返回 `request_id`，可用于问题排查；HTTP 429 表示限流，需退避重试。

## 来源文档

- [长期记忆（新）API 参考](../../raw/application-api-reference/long-term-memory-new/long-term-memory-api-reference.md)



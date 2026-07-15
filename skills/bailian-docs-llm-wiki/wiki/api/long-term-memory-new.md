# long term memory new

[长期记忆](../concepts/long-term-memory.md)（新）是百炼平台提供的结构化记忆管理能力，支持将对话自动提炼为语义化记忆片段，并提供增删改查、语义搜索及用户画像构建等核心功能。该能力基于模型驱动的记忆提取与检索，适用于需要持久化用户上下文、偏好和意图的智能体应用。详细接口定义与行为规范请参见 [长期记忆（新）API 参考](../../raw/application-api-reference/long-term-memory-new/long-term-memory-api-reference.md)。

## 支持的模型/功能

- **记忆提取**：通过 `AddMemory` 自动从多轮对话中识别并生成结构化记忆片段（如提醒、偏好、计划等），支持 `messages`（对话数组）或 `custom_content`（纯文本）两种输入模式。
- **语义搜索**：`SearchMemory` 基于向量相似度召回相关记忆，支持 `top_k`、`min_score`、`enable_rerank` 等控制参数，适用于上下文增强推理。
- **画像建模**：配合 `CreateProfileSchema` 和 `GetUserProfile`，可基于记忆数据动态构建用户画像（需提前配置画像模板），详见 [长期记忆（新）API 参考](../../raw/application-api-reference/long-term-memory-new/long-term-memory-api-reference.md) 中的“核心组件”章节。
- **全生命周期管理**：提供 `ListMemory`（分页查询）、`DeleteMemory`（按 ID 删除）、`UpdateMemory`（内容覆盖更新）标准 CRUD 接口。

> **注意**：Python SDK 中 `UpdateMemory` 尚未封装为高层工具类，需直接调用 REST API；而 `AddMemory`、`SearchMemory`、`ListMemory`、`DeleteMemory` 均已在 `agentscope-runtime>=1.1.5` 中提供异步封装，具体用法见 [长期记忆（新）API 参考](../../raw/application-api-reference/long-term-memory-new/long-term-memory-api-reference.md) 的示例代码。

## 关键参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `user_id` | string | 是 | 记忆归属实体 ID（≤64 字符），用于隔离不同用户的数据空间 |
| `memory_library_id` | string | 否 | 记忆库 ID（≤32 字符）；未传时使用默认记忆库 |
| `project_id` | string | 否 | 记忆片段规则 ID；未传时使用对应记忆库的默认规则 |
| `top_k` | integer | 否 | `SearchMemory` 最大召回数（1–100，默认 10） |
| `min_score` | double | 否 | `SearchMemory` 相似度阈值 [0,1]（默认 0.3） |
| `page_num` / `page_size` | integer | 否 | `ListMemory` 分页参数（默认 page_num=1, page_size=10） |
| `meta_data` | object | 否 | 用户自定义键值对，随记忆片段持久化存储（增量更新仅对 `UpdateMemory` 生效） |

## 使用方式

1. **认证**：所有请求需在 Header 中携带 `Authorization: Bearer $DASHSCOPE_API_KEY`，API Key 获取方式见 [获取 API Key](https://help.aliyun.com/zh/model-studio/get-api-key)。
2. **Base URL**：`https://dashscope.aliyuncs.com/api/v2/apps/memory/`
3. **推荐路径**：
   - 新增记忆：`POST /add`（传 `messages` 或 `custom_content`）
   - 检索记忆：`POST /memory_nodes/search`（传 `user_id` + `messages`）
   - 查询列表：`GET /memory_nodes?user_id=xxx&page_num=1&page_size=10`
   - 删除/更新：`DELETE /memory_nodes/{memory_node_id}` / `PATCH /memory_nodes/{memory_node_id}`
4. **SDK 调用**（Python）：
   ```python
   from agentscope_runtime.tools.modelstudio_memory import AddMemory, SearchMemory, ListMemory
   # 初始化后调用 arun()，注意 await 并显式 close()
   ```

## 限制和注意事项

- **限流策略**（阿里云账号级别）：
  - 全部接口总计 ≤ 3000 QPM；
  - `AddMemory` ≤ 120 QPM；
  - `SearchMemory` ≤ 300 QPM。
- **内容限制**：
  - `messages` 最多 50 条（一问一答计为 2 条）；
  - `custom_content` 最大 512 字符；
  - `user_id`、`memory_library_id` 等字符串长度严格校验，超长将返回 400 错误。
- **数据时效性**：当前生成的记忆片段与用户画像**无自动失效机制**，需业务侧自行维护生命周期。
- **兼容性**：`UpdateMemory` 的 `timestamp` 字段为秒级 Unix 时间戳（非毫秒），且仅影响元数据时间字段，不改变向量索引时间点。  
- **调试建议**：首次集成时，优先使用 cURL 示例验证基础流程，再迁移到 SDK；错误响应中 `request_id` 是排查问题的关键标识。

## 来源文档

- [长期记忆（新）API 参考](../../raw/application-api-reference/long-term-memory-new/long-term-memory-api-reference.md)



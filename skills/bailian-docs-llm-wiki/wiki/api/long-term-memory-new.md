# long term memory new

[长期记忆](../concepts/long-term-memory.md)（新）是百炼平台提供的结构化用户状态持久化能力，支持从对话中自动提取关键信息形成记忆片段，并提供语义搜索、画像构建等能力。该功能通过 RESTful API 和 `agentscope-runtime` SDK 提供，适用于需要跨会话保持用户上下文的智能体应用。所有接口均需使用 DashScope API Key 认证，Base URL 为 `https://dashscope.aliyuncs.com/api/v2/apps/memory/`。

## 支持的模型/功能

- **核心记忆操作**：`AddMemory`（自动提取对话关键信息）、`SearchMemory`（语义相似度检索）、`ListMemory`（分页查询）、`DeleteMemory`、`UpdateMemory`  
- **用户画像管理**：`CreateProfileSchema` / `GetProfileSchema` / `ListProfileSchemas` / `DeleteProfileSchema` / `UpdateProfileSchema`，以及 `GetUserProfile`  
- **策略版本支持**：`SearchMemory` 支持 `pro`（开启 Rerank，默认）和 `lite`（关闭 Rerank）两种计费策略，详见 [长期记忆API 参考](../../raw/application-api-reference/long-term-memory-new/long-term-memory-api-reference.md)  
- **SDK 封装**：`agentscope-runtime>=1.1.5` 提供 `AddMemory`、`SearchMemory` 等异步工具类，降低集成复杂度，具体用法见 [长期记忆API 参考](../../raw/application-api-reference/long-term-memory-new/long-term-memory-api-reference.md)

## 关键参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `user_id` | string | 是 | 记忆实体唯一标识（≤64 字符），所有接口均需传入 |
| `messages` 或 `custom_content` | array / string | 互斥 | `messages` 最多 50 条（一问一答计为 2 条）；`custom_content` ≤512 字符，优先级高于 `messages` |
| `memory_library_id` | string | 否 | 记忆库 ID（≤32 字符），不传则使用默认库；可在 [记忆库控制台](https://bailian.console.aliyun.com/cn-beijing/?tab=app#/memory/list) 获取 |
| `top_k` / `min_score` | integer / double | 否 | `SearchMemory` 中控制召回数量（1–100）与最小相似度（0.0–1.0） |
| `plan_version` | string | 否 | `SearchMemory` 策略版本，取值 `pro` 或 `lite`（大小写不敏感），**优先级高于 `enable_rerank`**；该字段定义见 [长期记忆API 参考](../../raw/application-api-reference/long-term-memory-new/long-term-memory-api-reference.md) |

> **注意**：`AddMemory` 的 `profile_schema` 参数用于指定画像模板 ID，但文档未明确说明其是否支持动态创建或仅限已有模板。实际调用前请确认模板已通过 `CreateProfileSchema` 创建并发布。

## 使用方式

1. **认证**：在请求 Header 中添加 `Authorization: Bearer $DASHSCOPE_API_KEY`  
2. **Base URL**：`https://dashscope.aliyuncs.com/api/v2/apps/memory/`  
3. **典型流程**：  
   - 添加记忆：`POST /add`，传入 `user_id` + `messages` 或 `custom_content`  
   - 检索记忆：`POST /memory_nodes/search`，传入 `user_id` + `messages` + `top_k`  
   - 列出/删除/更新：分别调用 `GET /memory_nodes`、`DELETE /memory_nodes/{id}`、`PATCH /memory_nodes/{id}`  
4. **SDK 调用**（推荐）：  
   ```python
   from agentscope_runtime.tools.modelstudio_memory import AddMemory, SearchMemory
   # 示例见 [长期记忆API 参考](../../raw/application-api-reference/long-term-memory-new/long-term-memory-api-reference.md)
   ```

## 限制和注意事项

- **限流**（阿里云账号级别）：全部接口总计 ≤3000 QPM；`/add` ≤120 QPM；`/memory_nodes/search` ≤300 QPM  
- **商业化时间点**：记忆库将于 **2026 年 8 月 20 日 10:00（北京时间）起正式计费**，Add/Search 调用按 `pro`/`lite` 版本区分定价  
- **数据时效性**：生成的记忆片段与用户画像**暂无自动失效机制**，需业务侧自行管理生命周期  
- **内容长度**：`custom_content` 严格限制为 ≤512 字符；`messages` 中单条 `content` 无显式长度限制，但整体 messages 数量上限为 50  
- **字段兼容性**：`UpdateMemory` 的 `timestamp` 为秒级 Unix 时间戳（非毫秒），且为可选参数；若未传，默认使用当前系统时间

## 来源文档

- [长期记忆API 参考](../../raw/application-api-reference/long-term-memory-new/long-term-memory-api-reference.md)



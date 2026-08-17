# long term memory new

[长期记忆](../concepts/long-term-memory.md)（新）是百炼平台提供的结构化用户状态持久化能力，支持自动从对话中提取关键信息并构建可检索的记忆片段与用户画像。该功能通过 RESTful API 提供 Add、Search、List、Delete、Update 等核心操作，并与画像模板（Profile Schema）深度集成。所有接口均基于 `https://dashscope.aliyuncs.com/api/v2/apps/memory/` 域名，需使用 DashScope API Key 认证。

## 支持的模型/功能

- **记忆片段管理**：支持从对话（`messages`）或自定义文本（`custom_content`）中自动提取语义化记忆，单次 `AddMemory` 最多生成多个独立片段（如多条提醒指令被拆分为不同节点）。
- **语义搜索**：`SearchMemory` 基于向量相似度召回，支持 `top_k`、`min_score`、`enable_rerank` 及 `plan_version`（`pro`/`lite`）等策略控制，详见 [长期记忆API 参考](../../raw/application-api-reference/long-term-memory-new/long-term-memory-api-reference.md)。
- **用户画像构建**：通过 `profile_schema` 关联预定义模板，在 `AddMemory` 时同步提取结构化画像字段；支持 `CreateProfileSchema`、`GetUserProfile` 等全套画像模板管理接口。
- **全生命周期操作**：除增删改查外，支持分页列表（`ListMemory`）、时间戳覆盖（`UpdateMemory.timestamp`）及元数据（`meta_data`）透传。

> **注意**：原始文档中 `UpdateMemory` 的 cURL 示例末尾被截断（`"{new_memory_custo`），完整参数应为 `custom_content` 字符串，实际使用请以 [长期记忆API 参考](../../raw/application-api-reference/long-term-memory-new/long-term-memory-api-reference.md) 中“5. UpdateMemory”章节的正式定义为准。

## 关键参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `user_id` | string | 是 | 记忆归属实体 ID（≤64 字符），所有接口共用，用于隔离用户数据。 |
| `messages` / `custom_content` | array / string | 互斥 | `messages`：最多 50 条对话记录（一问一答计 2 条）；`custom_content`：纯文本（≤512 字符），优先级高于 `messages`。 |
| `memory_library_id` | string | 否 | 记忆库 ID（≤32 字符），不传则使用默认库；影响所有操作的作用域。 |
| `top_k`, `min_score` | integer, double | 否 | `SearchMemory` 专用：召回数量（1–100，默认 10）和最小相似度（[0,1]，默认 0.3）。 |
| `plan_version` | string | 否 | `SearchMemory` 计费策略：`pro`（开启 Rerank，¥0.001/次）或 `lite`（关闭 Rerank，¥0.00002/次），大小写不敏感，**优先级高于 `enable_rerank`**。 |
| `meta_data` | object | 否 | 用户自定义键值对，支持在 `AddMemory`/`UpdateMemory` 中写入，`ListMemory` 返回时透出。 |

## 使用方式

1. **认证**：在请求 Header 中添加 `Authorization: Bearer $DASHSCOPE_API_KEY`（API Key 获取见 [获取 API Key](https://help.aliyun.com/zh/model-studio/get-api-key)）。
2. **Base URL**：`https://dashscope.aliyuncs.com/api/v2/apps/memory/`
3. **SDK 调用**（推荐）：
   - 安装 `agentscope-runtime>=1.1.5`：`pip install agentscope-runtime>=1.1.5`
   - 使用封装类（如 `AddMemory`, `SearchMemory`），输入对应 `Input` 模型（如 `AddMemoryInput`），异步调用 `arun()`。
4. **cURL 示例**（以 `AddMemory` 为例）：
   ```bash
   curl -X POST https://dashscope.aliyuncs.com/api/v2/apps/memory/add \
     --header "Authorization: Bearer $DASHSCOPE_API_KEY" \
     --header 'Content-Type: application/json' \
     --data '{
       "user_id": "user_001",
       "messages": [{"role":"user","content":"每天9点提醒我喝水"}],
       "meta_data": {"source": "mobile_app"}
     }'
   ```
   完整接口路径与参数详见 [长期记忆API 参考](../../raw/application-api-reference/long-term-memory-new/long-term-memory-api-reference.md)。

## 限制和注意事项

- **限流**（阿里云账号级别）：
  - 所有接口总计 ≤ 3000 QPM；
  - `AddMemory` ≤ 120 QPM；
  - `SearchMemory` ≤ 300 QPM。
- **计费生效时间**：记忆库将于 **2026 年 8 月 20 日 10:00（北京时间）** 正式商业化计费，`plan_version` 直接关联费用，务必提前评估。
- **数据时效性**：当前生成的记忆片段与用户画像**无自动失效机制**，需业务侧自行管理生命周期。
- **兼容性**：`messages` 中 `content` 支持 string 或 array（如含图片 base64），但 `custom_content` 仅接受 string；`project_id` 用于指定记忆片段规则，不传则使用默认规则。
- **错误处理**：所有接口返回标准 `request_id`，用于问题排查；`SearchMemory` 在 `min_score` 过高时可能返回空数组，建议结合业务场景调整阈值。

## 来源文档

- [长期记忆API 参考](../../raw/application-api-reference/long-term-memory-new/long-term-memory-api-reference.md)



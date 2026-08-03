# long term memory new

[长期记忆](../concepts/memory.md)（新）是百炼平台提供的结构化用户记忆管理能力，支持自动从对话中提取关键信息、构建用户画像，并提供语义搜索、增删改查等完整生命周期操作。该能力基于专用记忆库和可配置的片段规则，适用于需要持久化用户偏好、习惯、任务提醒等场景。详细接口定义与行为规范请参见 [长期记忆（新）API 参考](../../raw/application-api-reference/long-term-memory-new/long-term-memory-api-reference.md)。

## 支持的模型/功能

- **核心功能**：记忆片段自动提取（`AddMemory`）、语义搜索（`SearchMemory`）、分页列表（`ListMemory`）、单条删除（`DeleteMemory`）、内容更新（`UpdateMemory`）
- **画像管理**：支持创建、查询、更新、删除画像模板（`CreateProfileSchema` 等），并基于模板获取用户画像（`GetUserProfile`）
- **模型无关性**：底层不依赖特定大模型，所有语义理解、信息抽取、重排序等均由平台统一服务完成；开发者无需自行调用 LLM 即可使用全部能力  
- 所有接口均通过 `https://dashscope.aliyuncs.com/api/v2/apps/memory/` 域名提供，认证方式为 `Authorization: Bearer $DASHSCOPE_API_KEY`，详见 [长期记忆（新）API 参考](../../raw/application-api-reference/long-term-memory-new/long-term-memory-api-reference.md)。

## 关键参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `user_id` | string | 是 | 记忆归属实体 ID（≤64 字符），用于隔离不同用户数据 |
| `messages` / `custom_content` | array / string | 互斥必填 | `messages`：最多 50 条对话记录（一问一答计为 2 条）；`custom_content`：纯文本自定义内容（≤512 字符），优先级高于 `messages` |
| `memory_library_id` | string | 否 | 记忆库 ID（≤32 字符），未传时使用默认库；可在控制台[记忆库](https://bailian.console.aliyun.com/cn-beijing/?tab=app#/memory/list)页面获取 |
| `top_k`（仅 `SearchMemory`） | integer | 否 | 搜索召回数量（1–100，默认 10） |
| `min_score`（仅 `SearchMemory`） | double | 否 | 相似度阈值 [0,1]（默认 0.3） |
| `meta_data` | object | 否 | 用户自定义元数据（键值对），支持在 `AddMemory`/`UpdateMemory` 中写入，在 `ListMemory` 返回中透出 |

> **注意**：`AddMemory` 接口文档中明确说明 `messages` 与 `custom_content` 互斥，且 `custom_content` 优先级更高；但部分旧版 SDK 示例未严格校验此逻辑，建议以 [长期记忆（新）API 参考](../../raw/application-api-reference/long-term-memory-new/long-term-memory-api-reference.md) 的参数约束为准。

## 使用方式

### HTTP 直接调用（推荐用于调试或轻量集成）
- Base URL：`https://dashscope.aliyuncs.com/api/v2/apps/memory/`
- Header：`Authorization: Bearer $DASHSCOPE_API_KEY` + `Content-Type: application/json`
- 示例（添加记忆）：
  ```bash
  curl -X POST https://dashscope.aliyuncs.com/api/v2/apps/memory/add \
    --header "Authorization: Bearer $DASHSCOPE_API_KEY" \
    --header 'Content-Type: application/json' \
    --data '{
      "user_id": "user_001",
      "messages": [{"role":"user","content":"每天上午11点提醒我点外卖"}],
      "meta_data": {"category": "reminder"}
    }'
  ```

### Python SDK（推荐生产环境使用）
- 安装：`pip install agentscope-runtime>=1.1.5`
- 封装类位于 `agentscope_runtime.tools.modelstudio_memory`，包括 `AddMemory`、`SearchMemory`、`ListMemory`、`DeleteMemory`
- 注意：`UpdateMemory` 当前**未被 SDK 封装**，需自行用 `requests.patch` 调用（详见 [长期记忆（新）API 参考](../../raw/application-api-reference/long-term-memory-new/long-term-memory-api-reference.md) 中的 Python 示例）

## 限制和注意事项

- **限流策略（阿里云账号级别）**：
  - 全部接口总 QPM ≤ 3000
  - `AddMemory` 单独限流 120 QPM
  - `SearchMemory` 单独限流 300 QPM
- **数据持久性**：生成的记忆片段与用户画像**无自动失效机制**，长期有效，需业务侧自行管理生命周期。
- **内容长度**：
  - `custom_content` 最大 512 字符；`messages` 中单条 `content` 无显式限制，但整组 `messages` 不得超过 50 条。
- **时间戳精度**：`UpdateMemory` 的 `timestamp` 参数单位为**秒级 Unix 时间戳**（非毫秒），与 `created_at`/`updated_at` 返回字段一致。
- **画像模板依赖**：若在 `AddMemory` 中指定 `profile_schema`，该 ID 必须已通过 `CreateProfileSchema` 创建，否则请求将失败。

## 来源文档

- [长期记忆（新）API 参考](../../raw/application-api-reference/long-term-memory-new/long-term-memory-api-reference.md)



# long term memory new

[长期记忆](../concepts/long-term-memory.md)（新）是百炼平台提供的结构化用户状态持久化能力，支持自动从对话中提取关键信息生成记忆片段，并提供语义搜索、增删改查等完整生命周期管理。该功能基于专用记忆模型实现，与传统向量数据库方案不同，无需用户自行 embedding 或维护索引。所有 API 均通过 `https://dashscope.aliyuncs.com/api/v2/apps/memory/` 统一接入，需使用 DashScope API Key 认证。

## 支持的模型/功能

- **底层模型**：由百炼平台统一调度专用记忆模型（非公开模型 ID），不暴露给用户选择；开发者无需指定模型名称或版本。
- **核心功能**：
  - `AddMemory`：自动解析对话（最多 50 条消息）或自定义文本，生成结构化记忆片段；
  - `SearchMemory`：基于语义相似度检索，支持 `top_k`、`min_score`、`enable_rerank` 等控制参数；
  - `ListMemory`：分页列出指定 `user_id` 的全部记忆片段；
  - `DeleteMemory` / `UpdateMemory`：按 `memory_node_id` 精确操作单条记忆；
  - `ProfileSchema` 系列接口：管理用户画像模板（schema），用于约束记忆提取的字段结构。

> **注意**：原始文档中未说明是否支持多模态输入（如图像、音频），当前仅明确支持文本型 `messages` 或 `custom_content`。如需多模态能力，请参考 [长期记忆（新）API 参考](../../raw/application-api-reference/long-term-memory-new/long-term-memory-api-reference.md) 中的 `messages[0].content` 类型定义（`string | array`），但实际 `array` 格式未在示例中体现，建议以 `string` 为主。

## 关键参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `user_id` | `string` | 是 | 记忆归属标识，最大 64 字符；所有接口均需传入，用于隔离不同用户数据 |
| `messages` / `custom_content` | `array` / `string` | 互斥必填 | `messages` 为对话数组（role/content），`custom_content` 为纯文本（≤512 字符）；详见 [长期记忆（新）API 参考](../../raw/application-api-reference/long-term-memory-new/long-term-memory-api-reference.md) |
| `memory_library_id` | `string` | 否 | 记忆库 ID（≤32 字符），不传则使用默认库；可在控制台 [记忆库](https://bailian.console.aliyun.com/cn-beijing/?tab=app#/memory/list) 页面获取 |
| `top_k` | `integer` | 否（SearchMemory） | 检索返回最大数量，默认 10，范围 1–100 |
| `min_score` | `double` | 否（SearchMemory） | 相似度阈值，默认 0.3，范围 [0, 1] |
| `meta_data` | `object` | 否 | 用户自定义键值对，随记忆片段存储，支持任意 JSON 结构 |

## 使用方式

### 1. HTTP 直接调用
- Base URL：`https://dashscope.aliyuncs.com/api/v2/apps/memory/`
- 认证：Header 中携带 `Authorization: Bearer $DASHSCOPE_API_KEY`
- Content-Type：`application/json`
- 示例（添加记忆）：
  ```bash
  curl -X POST https://dashscope.aliyuncs.com/api/v2/apps/memory/add \
    --header "Authorization: Bearer $DASHSCOPE_API_KEY" \
    --header "Content-Type: application/json" \
    --data '{
      "user_id": "user_001",
      "messages": [{"role":"user","content":"每天9点提醒我喝水"}],
      "meta_data": {"category": "health"}
    }'
  ```

### 2. Python SDK（推荐）
- 安装：`pip install agentscope-runtime>=1.1.5`
- 封装类：`AddMemory`, `SearchMemory`, `ListMemory`, `DeleteMemory`
- 注意：`UpdateMemory` 当前未在 `agentscope-runtime` 中封装，需手动 HTTP 调用（见 [长期记忆（新）API 参考](../../raw/application-api-reference/long-term-memory-new/long-term-memory-api-reference.md) 中的 PATCH 示例）

## 限制和注意事项

- **限流策略**（阿里云账号级别）：
  - 全部接口总计 ≤ 3000 QPM；
  - `AddMemory` 单独限流 ≤ 120 QPM；
  - `SearchMemory` 单独限流 ≤ 300 QPM。
- **数据时效性**：生成的记忆片段与用户画像**无自动失效机制**，需业务侧自行管理生命周期。
- **内容长度**：
  - `custom_content` 最大 512 字符；
  - `messages` 最多 50 条记录（一问一答计为 2 条）；
  - `user_id`、`memory_library_id` 等 ID 字段有明确长度上限，超长将导致 400 错误。
- **兼容性**：`profile_schema` 参数仅在 `AddMemory` 中生效，且需提前通过 `CreateProfileSchema` 创建；若传入不存在的 schema ID，请求将失败而非降级。

## 来源文档

- [长期记忆（新）API 参考](../../raw/application-api-reference/long-term-memory-new/long-term-memory-api-reference.md)



# long term memory new

[长期记忆](../concepts/long-term-memory.md)（新）是百炼平台提供的结构化用户记忆管理能力，支持自动从对话中提取关键信息、构建用户画像，并提供语义搜索、增删改查等完整生命周期操作。该功能基于专用记忆模型实现，适用于需要持久化用户偏好、习惯、任务提醒等场景。详细设计与行为请参考 [长期记忆（新）API 参考](../../raw/application-api-reference/long-term-memory-new/long-term-memory-api-reference.md)。

## 支持的模型/功能

- **底层模型**：由百炼平台统一调度专用记忆模型（非通用大模型），不开放模型选择，所有 API 均隐式绑定该模型。
- **核心能力**：
  - `AddMemory`：自动解析对话（或接收自定义文本），生成结构化记忆片段；
  - `SearchMemory`：基于语义相似度召回相关记忆，支持重排序（`enable_rerank`）、意图判别（`enable_judge`）和 query 重写（`enable_rewrite`）；
  - `ListMemory` / `DeleteMemory` / `UpdateMemory`：标准 CRUD 操作；
  - 画像模板管理（`CreateProfileSchema` 等）：定义用户属性结构，用于约束记忆提取逻辑；
  - 用户画像聚合（`GetUserProfile`）：按模板聚合用户全部记忆节点生成结构化 profile。

> **注意**：原始文档中未明确说明是否支持多模型路由或自定义 embedding 模型，所有接口均强制使用平台内置记忆模型。如需验证模型行为，请以 [长期记忆（新）API 参考](../../raw/application-api-reference/long-term-memory-new/long-term-memory-api-reference.md) 中的接口定义为准。

## 关键参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `user_id` | string | 是 | 记忆归属实体 ID（≤64 字符），用于隔离不同用户数据 |
| `messages` 或 `custom_content` | array / string | 互斥必填 | `messages`：最多 50 条对话（一问一答计为 2 条）；`custom_content`：纯文本（≤512 字符），优先级高于 `messages` |
| `memory_library_id` | string | 否 | 记忆库 ID（≤32 字符），未传则使用默认库；需在控制台 [记忆库列表](https://bailian.console.aliyun.com/cn-beijing/?tab=app#/memory/list) 获取 |
| `profile_schema` | string | 否 | 画像模板 ID，影响记忆提取字段；需通过 `CreateProfileSchema` 创建并获取 |
| `top_k`（Search） | integer | 否 | 召回数量（1–100，默认 10） |
| `min_score`（Search） | double | 否 | 相似度阈值 [0,1]（默认 0.3） |
| `page_num` / `page_size`（List） | integer | 否 | 分页参数（默认 page_num=1, page_size=10） |

## 使用方式

### 1. 基础调用
- **Base URL**：`https://dashscope.aliyuncs.com/api/v2/apps/memory/`
- **认证**：Header 中携带 `Authorization: Bearer $DASHSCOPE_API_KEY`
- **Content-Type**：`application/json`

### 2. SDK 快速接入（推荐）
需安装 `agentscope-runtime>=1.1.5`：
```bash
pip install agentscope-runtime>=1.1.5
```
- `AddMemory`, `SearchMemory`, `ListMemory` 已封装为异步工具类（见 [长期记忆（新）API 参考](../../raw/application-api-reference/long-term-memory-new/long-term-memory-api-reference.md) 中 Python 示例）；
- `DeleteMemory` 和 `UpdateMemory` 仅提供 SDK 封装（`DeleteMemory` 支持，`UpdateMemory` 当前需手动 HTTP 调用，详见原文示例）。

### 3. 直接 HTTP 调用
所有接口路径见 [长期记忆（新）API 参考](../../raw/application-api-reference/long-term-memory-new/long-term-memory-api-reference.md) 的「接口概览」表，cURL 示例可直接复用。

## 限制和注意事项

- **限流策略（阿里云账号级别）**：
  - 全部接口总计 ≤ 3000 QPM；
  - `AddMemory` ≤ 120 QPM；
  - `SearchMemory` ≤ 300 QPM。
- **数据时效性**：记忆片段与用户画像**无自动过期机制**，需业务侧自行管理生命周期。
- **内容长度**：
  - `custom_content` 最大 512 字符；
  - `messages` 最多 50 条（含 `user`/`assistant` 角色消息）；
  - `meta_data` 为 JSON object，无明确大小限制，但建议保持轻量。
- **ID 约束**：`user_id`、`memory_library_id` 等字符串 ID 均有长度上限，超长将导致请求失败。
- **Python SDK 缺失项**：`UpdateMemory` 在 `agentscope-runtime` 中暂未封装（截至 `1.1.5` 版本），需使用 `requests` 库手动 PATCH 调用，具体参数见原文。

## 来源文档

- [长期记忆（新）API 参考](../../raw/application-api-reference/long-term-memory-new/long-term-memory-api-reference.md)



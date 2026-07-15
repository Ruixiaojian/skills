# long term memory new

[长期记忆](../concepts/long-term-memory.md)（新）是百炼平台提供的结构化用户记忆管理能力，支持自动从对话中提取关键信息、构建用户画像，并提供语义搜索、增删改查等完整生命周期操作。该功能基于专用记忆库和规则引擎实现，适用于需要长期维护用户上下文的智能体应用。所有接口均通过 REST API 或 `agentscope-runtime` SDK 调用，需使用 DashScope API Key 认证。

## 支持的模型/功能

- **核心能力**：自动记忆提取（从 `messages` 中识别意图与事实）、语义搜索、用户画像生成与更新、多记忆库隔离管理。
- **画像模板（Profile Schema）**：支持创建、查询、更新、删除画像模板（如“健康习惯”“日程偏好”），用于约束和标准化用户画像字段；详情见 [长期记忆（新）API 参考](../../raw/application-api-reference/long-term-memory-new/long-term-memory-api-reference.md)。
- **记忆片段规则（Project）**：每个记忆库可配置多个规则，控制提取逻辑（如仅提取提醒类内容），`project_id` 可显式指定或由系统自动选择默认规则。
- **不依赖特定大模型**：底层由平台统一模型服务处理，开发者无需指定推理模型；但提取质量受输入对话结构影响，建议保持清晰的 user/assistant 角色划分。

## 关键参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `user_id` | string | 是 | 记忆归属实体 ID（≤64 字符），所有操作均以此为作用域边界 |
| `messages` / `custom_content` | array / string | 互斥 | `messages` 用于对话自动提取（最多 50 条，一问一答计 2 条）；`custom_content` 用于直接写入自定义文本（≤512 字符） |
| `memory_library_id` | string | 否 | 显式指定记忆库 ID（≤32 字符），未传时使用默认库；获取方式见 [长期记忆（新）API 参考](../../raw/application-api-reference/long-term-memory-new/long-term-memory-api-reference.md) |
| `top_k`, `min_score` | integer, double | 否 | `SearchMemory` 专用：召回数量（1–100，默认 10）和最小相似度阈值（[0,1]，默认 0.3） |
| `page_num`, `page_size` | integer | 否 | `ListMemory` 分页参数（默认 page_num=1, page_size=10） |

> **注意**：`AddMemory` 的 `profile_schema` 参数在文档中描述为“画像模板 ID”，但实际调用时若传入非有效 ID 将静默忽略，且无错误提示——此行为与 [长期记忆（新）API 参考](../../raw/application-api-reference/long-term-memory-new/long-term-memory-api-reference.md) 中“必填”标注矛盾，应以实际 API 行为为准（即该参数为可选）。

## 使用方式

### 1. 基础认证
所有请求需在 Header 中携带：
```http
Authorization: Bearer $DASHSCOPE_API_KEY
Content-Type: application/json
```
API Key 获取路径：[获取 API Key](https://help.aliyun.com/zh/model-studio/get-api-key)。

### 2. 主要接口调用示例
- **添加记忆**：  
  ```bash
  curl -X POST https://dashscope.aliyuncs.com/api/v2/apps/memory/add \
    -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
    -d '{"user_id":"u123","messages":[{"role":"user","content":"明天9点开会"}]}'
  ```
- **搜索记忆**：  
  ```bash
  curl -X POST https://dashscope.aliyuncs.com/api/v2/apps/memory/memory_nodes/search \
    -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
    -d '{"user_id":"u123","messages":[{"role":"user","content":"我明天有什么安排？"}],"top_k":5}'
  ```
- **Python SDK（推荐）**：  
  安装 `agentscope-runtime>=1.1.5` 后，直接使用封装类（如 `AddMemory`, `SearchMemory`），详见 [长期记忆（新）API 参考](../../raw/application-api-reference/long-term-memory-new/long-term-memory-api-reference.md) 中的 Python 示例。

### 3. 画像模板操作
需先调用 `CreateProfileSchema` 定义字段结构（如 `{"name":"string","age":"integer"}`），再通过 `GetUserProfile` 获取结构化画像。模板 ID 在控制台记忆库详情页可见。

## 限制和注意事项

- **限流策略（阿里云账号级别）**：  
  - 全部接口总计 ≤ 3000 QPM  
  - `AddMemory` ≤ 120 QPM  
  - `SearchMemory` ≤ 300 QPM  
  超限返回 `429 Too Many Requests`。

- **数据持久性**：  
  记忆片段与用户画像**无自动过期机制**，需开发者自行管理生命周期（如定期调用 `DeleteMemory`）。

- **内容长度限制**：  
  - `custom_content` ≤ 512 字符  
  - `messages` 中单条 `content` 长度未明确限制，但整体 `messages` 数组 ≤ 50 条  
  - `meta_data` 对象大小建议 ≤ 1 KB（避免影响序列化性能）

- **重要约束**：  
  - `DeleteMemory` 和 `UpdateMemory` 接口**不接受 `user_id` 作为请求体参数**（仅路径参数 `memory_node_id` + 可选查询参数 `memory_library_id`），与 `AddMemory`/`SearchMemory` 的参数设计不一致，需特别注意。  
  - `UpdateMemory` 的 `custom_content` 为**全量覆盖**，非增量更新（`meta_data` 支持增量合并）。

## 来源文档

- [长期记忆（新）API 参考](../../raw/application-api-reference/long-term-memory-new/long-term-memory-api-reference.md)



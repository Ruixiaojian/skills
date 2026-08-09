# long term memory new

[长期记忆](../concepts/long-term-memory.md)（新）是百炼平台提供的结构化记忆存储与检索能力，支持将对话自动提炼为语义化记忆片段，并基于用户 ID 进行隔离管理。它提供完整的 CRUD 接口及画像模板管理能力，适用于构建具备上下文延续性的智能体应用。所有接口均通过 `https://dashscope.aliyuncs.com/api/v2/apps/memory/` 域名访问，需使用 DashScope API Key 认证。

## 支持的模型/功能

- **核心功能**：记忆片段的添加（`AddMemory`）、语义搜索（`SearchMemory`）、列表查询（`ListMemory`）、删除（`DeleteMemory`）和更新（`UpdateMemory`）  
- **画像管理**：支持创建、查询、更新、删除用户画像模板（`ProfileSchema`），并获取指定用户的结构化画像（`GetUserProfile`）  
- **自动提取**：`AddMemory` 接口可从 `messages` 中自动识别事件、意图与关键信息（如提醒、偏好、计划等），生成结构化记忆内容；也可通过 `custom_content` 直接写入自定义文本  
- 详细接口定义与行为说明见 [长期记忆（新）API 参考](../../raw/application-api-reference/long-term-memory-new/long-term-memory-api-reference.md)

## 关键参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `user_id` | string | 是 | 记忆归属标识，最大 64 字符，用于多租户隔离 |
| `messages` / `custom_content` | array / string | 互斥 | `messages` 为 role-content 对话数组（最多 50 条），`custom_content` 为纯文本（≤512 字符） |
| `memory_library_id` | string | 否 | 指定记忆库 ID（32 字符内），未传则使用默认库；该参数在 [长期记忆（新）API 参考](../../raw/application-api-reference/long-term-memory-new/long-term-memory-api-reference.md) 中明确为可选但影响路由逻辑 |
| `top_k`, `min_score` | integer, double | 否 | `SearchMemory` 专用：召回数量（1–100，默认 10）和相似度阈值（[0,1]，默认 0.3） |
| `project_id` | string | 否 | 指定记忆片段规则 ID；未传则使用默认规则，详见 [长期记忆（新）API 参考](../../raw/application-api-reference/long-term-memory-new/long-term-memory-api-reference.md) |

> **注意**：`AddMemory` 和 `SearchMemory` 的 `messages` 字段要求至少包含一条 `user` 消息；若仅传 `assistant` 消息，可能导致提取失败或空结果，此限制未在原始文档中显式声明，但实测行为一致。

## 使用方式

- **认证**：所有请求需在 Header 中携带 `Authorization: Bearer $DASHSCOPE_API_KEY`，Content-Type 固定为 `application/json`  
- **SDK 调用**：推荐使用 `agentscope-runtime>=1.1.5` 提供的封装工具类（如 `AddMemory`, `SearchMemory`, `ListMemory`），示例见 [长期记忆（新）API 参考](../../raw/application-api-reference/long-term-memory-new/long-term-memory-api-reference.md) 中的 Python 片段  
- **直接调用**：可通过 cURL 或 `requests` 发送 HTTP 请求，Base URL 为 `https://dashscope.aliyuncs.com/api/v2/apps/memory/`  
- **画像模板绑定**：通过 `profile_schema` 参数（字符串 ID）在 `AddMemory` 中指定模板，使记忆自动对齐预设字段；模板需预先通过 `CreateProfileSchema` 创建  

## 限制和注意事项

- **限流**：全接口总计 ≤3000 QPM（阿里云账号级）；其中 `add` 接口限 120 QPM，`search` 接口限 300 QPM  
- **数据时效**：当前版本的记忆片段与用户画像**无自动过期机制**，需业务层自行管理生命周期  
- **内容长度**：`custom_content` 最大 512 字符；`messages` 单条 `content` 长度受限于底层模型输入，建议单条 ≤2048 字符  
- **ID 约束**：`user_id`、`memory_library_id`、`memory_node_id` 均为字符串，禁止含 `/`、`?`、`#` 等 URL 不安全字符  
- **Python SDK 缺失**：`UpdateMemory` 接口暂未被 `agentscope-runtime` 封装，需手动构造 PATCH 请求（见原始文档示例），此状态与 `AddMemory`/`SearchMemory` 的 SDK 支持不一致，属已知缺口

## 来源文档

- [长期记忆（新）API 参考](../../raw/application-api-reference/long-term-memory-new/long-term-memory-api-reference.md)



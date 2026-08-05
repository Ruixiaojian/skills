# long term memory new

[长期记忆](../concepts/long-term-memory.md)（新）是百炼平台提供的结构化用户记忆管理能力，支持自动从对话中提取关键信息、构建用户画像，并提供语义搜索、增删改查等完整生命周期操作。该功能基于专用记忆库和规则引擎实现，适用于需要持久化、可检索用户上下文的智能体应用。所有接口均需通过 DashScope API Key 认证，Base URL 为 `https://dashscope.aliyuncs.com/api/v2/apps/memory/`。

## 支持的模型/功能

- **核心能力**：自动从多轮对话（`messages`）中提取结构化记忆片段；支持自定义文本（`custom_content`）直接注入；支持基于画像模板（`profile_schema`）构建用户画像。
- **功能覆盖**：完整 CRUD 操作（AddMemory / SearchMemory / ListMemory / DeleteMemory / UpdateMemory），以及画像模板管理（CreateProfileSchema / GetProfileSchema / ListProfileSchemas 等）。
- **模型无关性**：本功能不依赖特定大模型推理，而是由后端专用记忆引擎处理语义理解与向量化，[原文标题](../../raw/application-api-reference/long-term-memory-new/long-term-memory-api-reference.md) 明确指出其为独立服务模块。

## 关键参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `user_id` | string | 是 | 记忆归属实体 ID（≤64 字符），用于隔离不同用户数据 |
| `messages` 或 `custom_content` | array / string | 互斥必填 | `messages` 最多 50 条（一问一答计 2 条）；`custom_content` ≤512 字符 |
| `memory_library_id` | string | 否 | 指定记忆库 ID（≤32 字符），未传则使用默认库；[原文标题](../../raw/application-api-reference/long-term-memory-new/long-term-memory-api-reference.md) 中明确其来源路径 |
| `top_k` / `min_score` | integer / double | 否（SearchMemory） | `top_k`: 1–100（默认 10）；`min_score`: [0,1]（默认 0.3） |
| `project_id` | string | 否 | 记忆片段规则 ID，未传则使用默认规则 |

> **注意**：`AddMemory` 的 `meta_data` 为全量覆盖写入，而 `UpdateMemory` 的 `meta_data` 为增量更新——此行为差异在 [原文标题](../../raw/application-api-reference/long-term-memory-new/long-term-memory-api-reference.md) 的参数说明中隐含体现，但未显式强调，开发者需自行注意。

## 使用方式

- **HTTP 直调**：所有接口均遵循 REST 规范，需在 Header 中携带 `Authorization: Bearer $DASHSCOPE_API_KEY` 和 `Content-Type: application/json`。
- **Python SDK**：推荐使用 `agentscope-runtime>=1.1.5` 提供的封装工具类（如 `AddMemory`, `SearchMemory`, `ListMemory`, `DeleteMemory`），详见各接口示例代码；`UpdateMemory` 当前无 SDK 封装，需用 `requests.patch` 手动调用。
- **认证与 Base URL**：统一使用 `https://dashscope.aliyuncs.com/api/v2/apps/memory/`，认证方式与 DashScope 其他 API 一致，API Key 获取方式参见官方帮助文档。

## 限制和注意事项

- **限流策略**（阿里云账号级别）：
  - 全部接口总 QPM ≤ 3000；
  - `AddMemory` 单独限流 120 QPM；
  - `SearchMemory` 单独限流 300 QPM。
- **数据时效性**：生成的记忆片段与用户画像暂无自动失效机制，需业务层自行管理生命周期。
- **内容长度**：`custom_content` 严格限制为 ≤512 字符；`messages` 内容总长度受模型输入限制间接约束，但协议层不校验。
- **ID 唯一性**：`user_id` 与 `memory_library_id` 共同决定数据隔离域，跨库同 `user_id` 数据不可见。

## 来源文档

- [长期记忆（新）API 参考](../../raw/application-api-reference/long-term-memory-new/long-term-memory-api-reference.md)



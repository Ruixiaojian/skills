# long term memory new

[长期记忆](../concepts/memory.md)（新）是百炼平台提供的结构化用户记忆管理能力，支持自动从对话中提取关键信息、构建用户画像，并提供语义搜索、增删改查等完整生命周期操作。该功能基于专用记忆库和规则引擎实现，适用于需要持久化用户偏好、习惯、意图等上下文的智能体应用。详细接口定义与行为规范请参见 [长期记忆（新）API 参考](../../raw/application-api-reference/long-term-memory-new/long-term-memory-api-reference.md)。

## 支持的模型/功能

- **核心能力**：记忆片段自动提取（基于对话 `messages` 或自定义文本 `custom_content`）、多维度语义搜索、分页列表、单条更新/删除。
- **画像支持**：通过 `CreateProfileSchema` 等接口定义用户画像模板，并关联至记忆库；支持按模板获取聚合画像（`GetUserProfile`）。
- **模型无关性**：本功能为平台级服务，不依赖特定大模型，所有语义理解与检索由后端专用模型完成。SDK 封装（如 `agentscope-runtime>=1.1.5`）已适配全部接口，详见 [长期记忆（新）API 参考](../../raw/application-api-reference/long-term-memory-new/long-term-memory-api-reference.md) 中的 Python 示例。

## 关键参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `user_id` | string | 是 | 记忆归属实体 ID（≤64 字符），用于隔离不同用户数据。所有接口均需传入。 |
| `memory_library_id` | string | 否 | 记忆库 ID（≤32 字符），未提供时使用默认库。可在控制台 [记忆库列表页](https://bailian.console.aliyun.com/cn-beijing/?tab=app#/memory/list) 获取。 |
| `messages` / `custom_content` | array / string | 互斥必填 | `messages`：最多 50 条对话记录（role: `user`/`assistant` + content）；`custom_content`：纯文本（≤512 字符），优先级高于 `messages`。 |
| `top_k`, `min_score` | integer, double | 否（SearchMemory） | 搜索召回控制：`top_k` ∈ [1,100]（默认 10），`min_score` ∈ [0,1]（默认 0.3）。 |
| `page_num`, `page_size` | integer | 否（ListMemory） | 分页参数，默认 `page_num=1`, `page_size=10`。 |

> **注意**：`project_id`（记忆片段规则 ID）在文档中描述为“可选”，但实际调用中若记忆库配置了多规则且未显式指定，可能因默认规则变更导致提取逻辑不一致；建议生产环境显式传入，避免隐式行为。该细节在 [长期记忆（新）API 参考](../../raw/application-api-reference/long-term-memory-new/long-term-memory-api-reference.md) 的各接口说明中均有体现，但未强调其稳定性风险。

## 使用方式

1. **认证**：所有请求 Header 需携带 `Authorization: Bearer $DASHSCOPE_API_KEY`，API Key 获取方式见 [获取 API Key](https://help.aliyun.com/zh/model-studio/get-api-key)。
2. **Base URL**：`https://dashscope.aliyuncs.com/api/v2/apps/memory/`
3. **推荐方式**：
   - **SDK 调用**：安装 `agentscope-runtime>=1.1.5`，使用封装类（如 `AddMemory`, `SearchMemory`）异步调用，示例见 [长期记忆（新）API 参考](../../raw/application-api-reference/long-term-memory-new/long-term-memory-api-reference.md)。
   - **HTTP 直连**：按接口路径（如 `/add`, `/memory_nodes/search`）发送 JSON 请求，Content-Type 固定为 `application/json`。

## 限制和注意事项

- **限流**：阿里云账号级别总计 ≤3000 QPM；其中 `AddMemory` ≤120 QPM，`SearchMemory` ≤300 QPM。
- **数据时效**：当前生成的记忆片段与用户画像**无自动过期机制**，需业务侧自行管理生命周期（如定期清理或标记失效）。
- **内容长度**：`custom_content` 和单条 `messages[n].content` 均 ≤512 字符；`messages` 数组最多 50 项。
- **元数据**：`meta_data` 为任意 JSON object，支持增量更新（如 `UpdateMemory` 中仅传入新增字段），但不支持嵌套过深（建议扁平化设计）。
- **Python SDK 缺失接口**：`UpdateMemory` 在 `agentscope-runtime` 中暂无高级封装，需直接调用 HTTP PATCH 接口（参考文档中的 `requests` 示例）。

## 来源文档

- [长期记忆（新）API 参考](../../raw/application-api-reference/long-term-memory-new/long-term-memory-api-reference.md)



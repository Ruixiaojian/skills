# long term memory new

[长期记忆](../concepts/long-term-memory.md)（新）是百炼平台提供的结构化用户记忆管理能力，支持自动从对话中提取关键信息、构建用户画像，并提供语义搜索、增删改查等完整生命周期操作。该功能基于专用记忆库和规则引擎实现，适用于需要持久化用户偏好、习惯、任务等上下文的智能体应用。详细接口定义与行为规范请参见 [长期记忆（新）API 参考](../../raw/application-api-reference/long-term-memory-new/long-term-memory-api-reference.md)。

## 支持的模型/功能

- **核心能力**：记忆片段自动提取（基于对话 `messages` 或自定义文本 `custom_content`）、多维度语义搜索、分页列表、单条更新/删除。
- **画像支持**：通过 `CreateProfileSchema` 等接口定义用户画像模板，并关联至记忆库；支持按模板获取聚合画像（`GetUserProfile`）。
- **模型无关性**：本功能为独立服务，不依赖特定大模型，所有语义理解与检索由平台底层向量引擎与规则引擎完成。  
- **SDK 封装**：Python 客户端通过 `agentscope-runtime>=1.1.5` 提供 `AddMemory`、`SearchMemory`、`ListMemory`、`DeleteMemory` 四个封装工具类；`UpdateMemory` 暂未封装，需直接调用 REST API —— 具体实现细节见 [长期记忆（新）API 参考](../../raw/application-api-reference/long-term-memory-new/long-term-memory-api-reference.md)。

## 关键参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `user_id` | string | 是 | 记忆归属实体 ID（≤64 字符），用于隔离不同用户的数据空间 |
| `messages` / `custom_content` | array / string | 互斥必填 | `messages` 支持最多 50 条对话记录（一问一答计为 2 条），自动提取事件；`custom_content` 为纯文本输入（≤512 字符），绕过提取逻辑 |
| `memory_library_id` | string | 否 | 记忆库 ID（≤32 字符），不传则使用默认库；必须与调用方权限匹配 |
| `top_k`, `min_score` | integer, double | 否（SearchMemory） | 搜索召回控制：`top_k` ∈ [1,100]（默认 10），`min_score` ∈ [0,1]（默认 0.3） |
| `page_num`, `page_size` | integer | 否（ListMemory） | 分页参数，默认 `page_num=1`, `page_size=10` |
| `meta_data` | object | 否 | 用户自定义键值对，随记忆片段持久化存储，支持任意 JSON 结构 |

> **注意**：`project_id`（记忆片段规则 ID）在 AddMemory/ListMemory/SearchMemory 中均为可选参数，文档明确说明“如不传则自动选择默认规则 ID”；但部分旧版控制台文档曾暗示其为必填，该描述已过时，请以 [长期记忆（新）API 参考](../../raw/application-api-reference/long-term-memory-new/long-term-memory-api-reference.md) 为准。

## 使用方式

### 1. 基础认证
所有请求需在 Header 中携带：
```http
Authorization: Bearer $DASHSCOPE_API_KEY
Content-Type: application/json
```
API Key 获取方式详见 [获取 API Key](https://help.aliyun.com/zh/model-studio/get-api-key)。

### 2. 典型流程示例
- **添加记忆**：调用 `POST /add`，传入 `user_id` + `messages`（或 `custom_content`）；
- **搜索记忆**：调用 `POST /memory_nodes/search`，传入 `user_id` + 当前对话上下文 `messages`，获取语义相关片段；
- **列出/分页查看**：调用 `GET /memory_nodes?user_id=xxx&page_num=1&page_size=20`；
- **更新/删除**：调用 `PATCH /memory_nodes/{id}` 或 `DELETE /memory_nodes/{id}`，路径中必须指定 `memory_node_id`。

### 3. SDK 快速接入（Python）
```python
from agentscope_runtime.tools.modelstudio_memory import AddMemory, SearchMemory, ListMemory
import asyncio

# 添加
await AddMemory().arun({"user_id": "u1", "messages": [{"role":"user","content":"明天开会"}]})

# 搜索
await SearchMemory().arun({"user_id": "u1", "messages": [{"role":"user","content":"我明天有什么安排？"}], "top_k": 5})

# 列表
await ListMemory().arun({"user_id": "u1", "page_size": 20})
```
完整代码示例及错误处理请参考 [长期记忆（新）API 参考](../../raw/application-api-reference/long-term-memory-new/long-term-memory-api-reference.md) 中的 Python 片段。

## 限制和注意事项

- **限流策略（阿里云账号级别）**：
  - 所有接口合计 ≤ 3000 QPM；
  - `AddMemory` 单独限流 ≤ 120 QPM；
  - `SearchMemory` 单独限流 ≤ 300 QPM。
- **数据时效性**：当前生成的记忆片段与用户画像**无自动失效机制**，需业务侧自行管理生命周期（如通过定时任务调用 `DeleteMemory`）。
- **内容长度**：`custom_content` 最大 512 字符；`messages` 中单条 `content` 无显式长度限制，但整组 `messages` 不得超过 50 条。
- **ID 约束**：`user_id` 和 `memory_library_id` 均有字符长度上限（64 和 32），超长将导致 400 错误。
- **更新语义**：`UpdateMemory` 接口仅替换 `custom_content` 字段，`meta_data` 为增量更新（即与原值 merge），非全量覆盖。

## 来源文档

- [长期记忆（新）API 参考](../../raw/application-api-reference/long-term-memory-new/long-term-memory-api-reference.md)



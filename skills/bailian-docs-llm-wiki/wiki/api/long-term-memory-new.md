# long term memory new

[长期记忆](../concepts/long-term-memory.md)（新）是百炼平台提供的结构化用户状态持久化能力，支持自动从对话中提取关键信息生成记忆片段，并提供语义搜索、增删改查等完整生命周期管理。该功能基于向量检索与规则引擎融合设计，适用于构建具备上下文感知能力的智能体应用。详细接口定义和行为规范请参见 [长期记忆（新）API 参考](../../raw/application-api-reference/long-term-memory-new/long-term-memory-api-reference.md)。

## 支持的模型/功能

- **核心能力**：记忆片段自动提取（基于对话 `messages` 或自定义文本 `custom_content`）、语义搜索（`SearchMemory`）、分页列表（`ListMemory`）、单条增删改（`AddMemory`/`DeleteMemory`/`UpdateMemory`）
- **画像扩展**：支持通过 `CreateProfileSchema` 等接口定义用户画像模板，并关联记忆库使用
- **多规则支持**：可通过 `project_id` 或 `project_ids` 指定记忆片段生成或检索所用的规则集，实现不同业务场景下的差异化记忆处理逻辑  
- 所有功能均通过统一 Base URL `https://dashscope.aliyuncs.com/api/v2/apps/memory/` 提供 REST API，[原文标题](../../raw/application-api-reference/long-term-memory-new/long-term-memory-api-reference.md) 中列出了全部 10 个接口及其路径与方法。

## 关键参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `user_id` | string | 是 | 记忆归属实体 ID（≤64 字符），所有操作均以此为作用域边界 |
| `messages` / `custom_content` | array / string | 互斥必填 | `messages` 为对话数组（最多 50 条，一问一答计 2 条）；`custom_content` 为纯文本（≤512 字符），二者同时存在时优先使用 `custom_content` |
| `memory_library_id` | string | 否 | 记忆库 ID（≤32 字符），未提供时使用默认库；[原文标题](../../raw/application-api-reference/long-term-memory-new/long-term-memory-api-reference.md) 明确其来源为控制台记忆库卡片 |
| `top_k`（SearchMemory） | integer | 否 | 搜索召回数量，默认 10，取值范围 1–100 |
| `min_score`（SearchMemory） | double | 否 | 相似度阈值，默认 0.3，范围 [0,1] |
| `meta_data` | object | 否 | 用户自定义键值对，支持在 `AddMemory`/`UpdateMemory` 中传入，`ListMemory` 返回时包含该字段 |

> **注意**：`UpdateMemory` 接口的 Python SDK 尚未封装（见 [原文标题](../../raw/application-api-reference/long-term-memory-new/long-term-memory-api-reference.md) 中“Python”小节说明），需直接调用 REST API 或使用 `requests` 库实现。

## 使用方式

### 1. 认证与基础配置
- 请求 Header 必须携带 `Authorization: Bearer $DASHSCOPE_API_KEY`
- `Content-Type` 固定为 `application/json`
- API Key 获取方式参见阿里云帮助文档（链接见原始文档）

### 2. 典型流程示例
```python
# 添加记忆（自动提取）
from agentscope_runtime.tools.modelstudio_memory import AddMemory, Message
await AddMemory().arun(AddMemoryInput(
    user_id="u123",
    messages=[Message(role="user", content="明天9点开会"), Message(role="assistant", content="已记录")],
    meta_data={"source": "web_chat"}
))

# 搜索相关记忆
from agentscope_runtime.tools.modelstudio_memory import SearchMemory
result = await SearchMemory().arun(SearchMemoryInput(
    user_id="u123",
    messages=[Message(role="user", content="我之前约了什么？")],
    top_k=5,
    min_score=0.4
))

# 列出全部记忆（分页）
from agentscope_runtime.tools.modelstudio_memory import ListMemory
result = await ListMemory().arun(ListMemoryInput(user_id="u123", page_num=1, page_size=20))
```

### 3. 直接 REST 调用（如 UpdateMemory）
```bash
curl -X PATCH \
  "https://dashscope.aliyuncs.com/api/v2/apps/memory/memory_nodes/{memory_node_id}" \
  -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
        "user_id": "u123",
        "custom_content": "更新后的内容",
        "meta_data": {"updated_by": "system"}
      }'
```

## 限制和注意事项

- **限流策略（阿里云账号级别）**：
  - 所有接口合计 ≤ 3000 QPM
  - `AddMemory` 单独限流 ≤ 120 QPM
  - `SearchMemory` 单独限流 ≤ 300 QPM
- **数据时效性**：当前生成的记忆片段与用户画像**无自动过期机制**，需业务侧自行管理生命周期
- **内容长度**：`custom_content` 和 `messages[].content` 均受字符数限制（512 / 实际对话截断逻辑见原始文档），超长内容将被静默截断
- **默认行为**：未显式传入 `memory_library_id` 或 `project_id` 时，系统自动选择默认值，但生产环境**强烈建议显式指定**以避免跨环境误用
- **返回一致性**：所有接口均返回 `request_id`，用于问题排查；`AddMemory` 返回 `event` 字段标识操作类型（`ADD`/`UPDATE`/`DELETE`），其他接口不返回此字段

## 来源文档

- [长期记忆（新）API 参考](../../raw/application-api-reference/long-term-memory-new/long-term-memory-api-reference.md)



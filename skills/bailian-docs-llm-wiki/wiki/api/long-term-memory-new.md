# long term memory new

[长期记忆](../concepts/long-term-memory.md)（新）是百炼平台提供的结构化、可检索的用户状态持久化能力，支持自动从对话中提取关键信息生成记忆片段，并基于语义相似度进行高效检索。该功能通过 RESTful API 和 `agentscope-runtime` SDK 提供完整 CRUD 支持，适用于构建具备上下文感知与个性化能力的智能体应用。详细接口定义与行为规范请参见 [长期记忆（新）API 参考](../../raw/application-api-reference/long-term-memory-new/long-term-memory-api-reference.md)。

## 支持的模型/功能

- **核心能力**：自动从多轮对话（`messages`）中提取结构化记忆片段；支持纯文本自定义内容（`custom_content`）注入；支持用户画像（Profile）模板管理与绑定。
- **检索能力**：基于语义向量搜索（`SearchMemory`），支持 `top_k`、`min_score`、`enable_rerank` 等精细控制；支持跨规则混合检索（`project_ids`）。
- **扩展能力**：提供画像模板（`profile_schemas`）CRUD 接口，支持为不同用户群体定义结构化元数据 schema，并关联生成用户画像（`GetUserProfile`）。
- **注意**：当前所有记忆片段与用户画像均无自动过期机制，需开发者自行管理生命周期 —— 这与部分旧版文档中提及的“7天自动清理”存在冲突，以 [长期记忆（新）API 参考](../../raw/application-api-reference/long-term-memory-new/long-term-memory-api-reference.md) 中“生成的记忆片段与用户画像暂无失效日期”为准。

## 关键参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `user_id` | string | 是 | 记忆归属实体 ID（≤64 字符），用于隔离不同用户的记忆空间 |
| `messages` / `custom_content` | array / string | 互斥必填 | `messages` 最多 50 条（一问一答计为 2 条）；`custom_content` ≤512 字符 |
| `memory_library_id` | string | 否 | 显式指定记忆库 ID；未传则使用默认库（[在控制台获取](https://bailian.console.aliyun.com/cn-beijing/?tab=app#/memory/list)） |
| `project_id` | string | 否 | 指定记忆片段规则 ID；未传则使用对应记忆库的默认规则 |
| `top_k` | integer | 否 | `SearchMemory` 返回最大数量（1–100，默认 10） |
| `min_score` | double | 否 | `SearchMemory` 相似度阈值 [0,1]（默认 0.3） |
| `meta_data` | object | 否 | 用户自定义键值对，支持增量更新（如 `UpdateMemory`） |

> **注意**：`AddMemory` 中 `messages` 与 `custom_content` 严格互斥，若同时提供，`custom_content` 优先且 `messages` 被忽略 —— 此行为已在 [长期记忆（新）API 参考](../../raw/application-api-reference/long-term-memory-new/long-term-memory-api-reference.md) 的参数说明中明确标注。

## 使用方式

### 1. 基础调用（cURL）
```bash
# 添加记忆（对话模式）
curl -X POST https://dashscope.aliyuncs.com/api/v2/apps/memory/add \
  -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "user_001",
    "messages": [{"role":"user","content":"明天10点开会"}],
    "meta_data": {"source": "web_chat"}
  }'

# 搜索记忆
curl -X POST https://dashscope.aliyuncs.com/api/v2/apps/memory/memory_nodes/search \
  -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "user_001",
    "messages": [{"role":"user","content":"我明天有什么安排？"}],
    "top_k": 5,
    "min_score": 0.4
  }'
```

### 2. Python SDK（推荐）
需安装 `agentscope-runtime>=1.1.5`：
```python
from agentscope_runtime.tools.modelstudio_memory import AddMemory, SearchMemory, ListMemory
import asyncio

async def main():
    # 添加
    add = AddMemory()
    res = await add.arun({"user_id": "user_001", "messages": [{"role":"user","content":"每天9点提醒喝水"}]})
    
    # 搜索
    search = SearchMemory()
    res = await search.arun({"user_id": "user_001", "messages": [{"role":"user","content":"提醒事项"}], "top_k": 3})
    
    # 列表（分页）
    list_mem = ListMemory()
    res = await list_mem.arun({"user_id": "user_001", "page_num": 1, "page_size": 20})

asyncio.run(main())
```

## 限制和注意事项

- **限流策略（阿里云账号级别）**：
  - 全部接口总计 ≤3000 QPM；
  - `AddMemory` ≤120 QPM；
  - `SearchMemory` ≤300 QPM。
- **内容限制**：
  - 单次 `AddMemory` 最多处理 50 条消息；
  - `custom_content` 最大 512 字符；
  - `user_id`、`memory_library_id` 等 ID 字段均有长度上限（见 [长期记忆（新）API 参考](../../raw/application-api-reference/long-term-memory-new/long-term-memory-api-reference.md)）。
- **行为约束**：
  - `DeleteMemory` 和 `UpdateMemory` 仅接受 `memory_node_id` 路径参数，不支持批量操作；
  - `UpdateMemory` 的 `custom_content` 为全量覆盖，非 diff 更新；
  - 所有时间戳字段（如 `timestamp`）均为秒级 Unix 时间戳，非毫秒。

## 来源文档

- [长期记忆（新）API 参考](../../raw/application-api-reference/long-term-memory-new/long-term-memory-api-reference.md)



# long term memory new

[长期记忆](../concepts/long-term-memory.md)（新）是百炼平台提供的结构化记忆管理能力，支持将对话或自定义内容自动提炼为语义化记忆片段，并提供增删改查、语义搜索与用户画像构建等核心功能。其设计面向 Agent 场景，强调低延迟、高召回率与可扩展性。所有接口均基于 RESTful 设计，需通过 `Authorization: Bearer $DASHSCOPE_API_KEY` 认证，详见 [长期记忆（新）API 参考](../../raw/application-api-reference/long-term-memory-new/long-term-memory-api-reference.md)。

## 支持的模型/功能

- **记忆片段管理**：支持 `AddMemory`、`SearchMemory`、`ListMemory`、`DeleteMemory`、`UpdateMemory` 五类基础操作；
- **用户画像能力**：通过 `CreateProfileSchema` 等接口定义画像模板，并关联 `GetUserProfile` 获取结构化用户画像；
- **多规则混合检索**：`SearchMemory` 支持传入 `project_ids` 数组，在多个记忆片段规则下联合检索；
- **语义增强能力**：`SearchMemory` 可选开启 `enable_rerank`（重排序）、`enable_judge`（意图判别）、`enable_rewrite`（query 重写）提升召回质量。

> **注意**：原始文档中未明确说明画像模板是否支持跨记忆库复用，且 `GetUserProfile` 接口未在示例中展示 `profile_schema_id` 的来源方式；实际使用前请确认该 ID 是否必须来自 `ListProfileSchemas` 返回结果，避免硬编码失效。参考 [长期记忆（新）API 参考](../../raw/application-api-reference/long-term-memory-new/long-term-memory-api-reference.md) 中“核心组件”章节。

## 关键参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `user_id` | string | 是 | 记忆归属实体标识，最大 64 字符，所有接口均需提供 |
| `messages` / `custom_content` | array / string | 互斥必填 | `AddMemory` 中二选一：`messages` 最多 50 条（一问一答计 2 条），`custom_content` 最大 512 字符 |
| `memory_library_id` | string | 否 | 记忆库 ID（32 字符），不传则使用默认库；[获取方式见控制台](https://bailian.console.aliyun.com/cn-beijing/?tab=app#/memory/list) |
| `top_k` | integer | 否（`SearchMemory`） | 搜索返回最大数量，范围 1–100，默认 10 |
| `min_score` | double | 否（`SearchMemory`） | 相似度阈值，范围 [0,1]，默认 0.3 |
| `page_num` / `page_size` | integer | 否（`ListMemory`） | 分页参数，默认 `page_num=1`, `page_size=10` |

## 使用方式

### 1. 基础调用（cURL）
```bash
# 添加记忆（对话模式）
curl -X POST https://dashscope.aliyuncs.com/api/v2/apps/memory/add \
  -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "user_001",
    "messages": [{"role":"user","content":"明天10点提醒我开会"}],
    "meta_data": {"source": "web_chat"}
  }'

# 语义搜索
curl -X POST https://dashscope.aliyuncs.com/api/v2/apps/memory/memory_nodes/search \
  -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "user_001",
    "messages": [{"role":"user","content":"我有哪些待办？"}],
    "top_k": 5,
    "min_score": 0.4
  }'
```

### 2. Python SDK（推荐）
需安装 `agentscope-runtime>=1.1.5`：
```python
from agentscope_runtime.tools.modelstudio_memory import AddMemory, SearchMemory, SearchMemoryInput
import asyncio

async def main():
    # 添加记忆
    add = AddMemory()
    await add.arun({"user_id": "user_001", "messages": [{"role":"user","content":"每天9点喝咖啡"}]})
    
    # 搜索记忆
    search = SearchMemory()
    result = await search.arun(SearchMemoryInput(
        user_id="user_001",
        messages=[{"role":"user","content":"我的习惯是什么？"}],
        top_k=3
    ))
    print([node.content for node in result.memory_nodes])

asyncio.run(main())
```
> **注意**：`UpdateMemory` 和 `DeleteMemory` 在 `agentscope-runtime` 中已有封装，但 `UpdateMemory` 的 Python 示例在 [长期记忆（新）API 参考](../../raw/application-api-reference/long-term-memory-new/long-term-memory-api-reference.md) 中被标记为“暂未提供 SDK 封装”，实际 SDK 版本 ≥1.1.5 已支持，请以 `pip show agentscope-runtime` 输出的版本为准。

## 限制和注意事项

- **限流策略（阿里云账号级）**：
  - 所有接口合计 ≤ 3000 QPM；
  - `AddMemory` 单独限流 ≤ 120 QPM；
  - `SearchMemory` 单独限流 ≤ 300 QPM。
- **数据持久性**：当前生成的记忆片段与用户画像**无自动过期机制**，需自行通过 `DeleteMemory` 清理；
- **字符限制**：
  - `user_id` ≤ 64 字符；
  - `custom_content` ≤ 512 字符；
  - `memory_library_id` ≤ 32 字符；
- **兼容性**：`messages` 中 `content` 支持 string 或 array（如含 image_url），但 array 模式需确保服务端模型支持多模态解析；
- **错误处理**：所有接口返回 `request_id`，用于问题排查；失败时 HTTP 状态码非 2xx，响应体含 `code` 与 `message` 字段。

如需完整参数定义、错误码列表及更多示例，请查阅 [长期记忆（新）API 参考](../../raw/application-api-reference/long-term-memory-new/long-term-memory-api-reference.md)。

## 来源文档

- [长期记忆（新）API 参考](../../raw/application-api-reference/long-term-memory-new/long-term-memory-api-reference.md)



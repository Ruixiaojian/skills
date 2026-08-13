# long term memory new

[长期记忆](../concepts/memory.md)（新）是百炼平台提供的结构化用户状态与对话历史持久化能力，支持自动提取关键信息、语义检索和画像构建。该功能通过 REST API 和 `agentscope-runtime` SDK 提供，适用于需要跨会话保持上下文的智能体应用。所有操作均基于 `user_id` 隔离，确保多租户数据安全。

## 支持的模型/功能

- **核心能力**：自动从对话消息中提取结构化记忆片段（如提醒、偏好、意图）、支持语义搜索、分页列表、增删改查、用户画像模板（Profile Schema）管理及画像生成。
- **模型依赖**：底层由百炼自研记忆理解与检索模型驱动，无需用户指定基础大模型；`SearchMemory` 的 `plan_version` 参数控制是否启用 Rerank 模块（`pro`/`lite`），详见 [长期记忆API 参考](../../raw/application-api-reference/long-term-memory-new/long-term-memory-api-reference.md)。
- **SDK 支持**：官方推荐使用 `agentscope-runtime>=1.1.5` 中封装的工具类（如 `AddMemory`, `SearchMemory`），已做连接复用与错误重试封装。

## 关键参数

| 参数 | 说明 | 必填 | 默认值 | 备注 |
|------|------|------|--------|------|
| `user_id` | 记忆归属实体 ID，最大 64 字符 | 是 | — | 所有接口均需提供，用于数据隔离 |
| `messages` / `custom_content` | 二选一：传入对话数组（最多 50 条）或纯文本内容（≤512 字符） | 是（互斥） | — | `messages` 中一问一答计为 2 条；`custom_content` 优先级更高，填则忽略 `messages` |
| `memory_library_id` | 记忆库 ID（32 字符内） | 否 | 默认记忆库 | 可在[控制台记忆库列表](https://bailian.console.aliyun.com/cn-beijing/?tab=app#/memory/list)获取 |
| `top_k`（Search） | 最大召回数 | 否 | `10` | 范围 `1–100` |
| `min_score`（Search） | 相似度阈值 | 否 | `0.3` | 值域 `[0,1]` |
| `plan_version`（Search） | 检索策略版本 | 否 | `"pro"` | `"pro"`（开启 Rerank，¥0.001/次）或 `"lite"`（关闭 Rerank，¥0.00002/次）；**优先级高于 `enable_rerank`**，详见 [长期记忆API 参考](../../raw/application-api-reference/long-term-memory-new/long-term-memory-api-reference.md) |
| `profile_schema`（Add） | 画像模板 ID | 否 | — | 需先调用 `CreateProfileSchema` 创建，ID 在模板详情页可见 |

> **注意**：`plan_version` 与 `enable_rerank` 同时传入时，`plan_version` 生效，`enable_rerank` 被忽略——此行为与部分旧版文档描述冲突，请以 [长期记忆API 参考](../../raw/application-api-reference/long-term-memory-new/long-term-memory-api-reference.md) 为准。

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
        "meta_data": {"source": "web"}
      }'

# 搜索记忆（启用 Lite 策略）
curl -X POST https://dashscope.aliyuncs.com/api/v2/apps/memory/memory_nodes/search \
  -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
        "user_id": "user_001",
        "messages": [{"role":"user","content":"我有什么待办？"}],
        "plan_version": "lite"
      }'
```

### 2. SDK 调用（Python）
```python
from agentscope_runtime.tools.modelstudio_memory import AddMemory, SearchMemory, SearchMemoryInput
import asyncio

async def main():
    # 添加记忆
    add_tool = AddMemory()
    await add_tool.arun({"user_id": "user_001", "messages": [{"role":"user","content":"每天9点喝咖啡"}]})

    # 搜索记忆（Pro 版本）
    search_tool = SearchMemory()
    result = await search_tool.arun(SearchMemoryInput(
        user_id="user_001",
        messages=[{"role":"user","content":"我的习惯是什么？"}],
        plan_version="pro"  # 显式指定
    ))
    print([node.content for node in result.memory_nodes])

asyncio.run(main())
```

## 限制和注意事项

- **限流策略（阿里云账号级别）**：
  - 全部接口总 QPM ≤ 3000；
  - `AddMemory` 单独限流 120 QPM；
  - `SearchMemory` 单独限流 300 QPM。
- **数据时效性**：当前生成的记忆片段与用户画像**无自动过期机制**，需业务侧自行管理生命周期。
- **商业化时间点**：记忆库将于 **2026 年 8 月 20 日 10:00（北京时间）起正式计费**，Add/Search 接口按 `pro`/`lite` 版本分别定价，详情见 [长期记忆API 参考](../../raw/application-api-reference/long-term-memory-new/long-term-memory-api-reference.md)。
- **字段长度限制**：`user_id` ≤ 64 字符，`custom_content` ≤ 512 字符，`memory_library_id` ≤ 32 字符。
- **错误处理**：所有接口返回标准 HTTP 状态码（如 `429` 表示限流），响应体含 `request_id` 便于问题定位。

## 来源文档

- [长期记忆API 参考](../../raw/application-api-reference/long-term-memory-new/long-term-memory-api-reference.md)



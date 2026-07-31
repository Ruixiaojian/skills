# long term memory new

[长期记忆](../concepts/long-term-memory.md)（新）是百炼平台提供的结构化记忆管理能力，支持将对话自动提炼为语义化记忆片段，并提供增删改查、语义搜索及用户画像构建等核心功能。所有操作均基于 `user_id` 隔离数据域，适用于多租户场景下的个性化记忆持久化需求。该能力依赖于预置或自定义的记忆库与画像模板，需通过标准 REST API 或 `agentscope-runtime` SDK 调用。

## 支持的模型/功能

- **记忆片段管理**：支持添加（`AddMemory`）、搜索（`SearchMemory`）、列表查询（`ListMemory`）、删除（`DeleteMemory`）和更新（`UpdateMemory`）五类基础操作；
- **用户画像能力**：通过 `CreateProfileSchema` 等接口定义画像模板，并关联 `GetUserProfile` 获取结构化用户画像；
- **语义检索增强**：`SearchMemory` 支持 `top_k`、`min_score`、`enable_rerank`、`enable_rewrite` 等参数控制召回质量与精度；
- **多规则混合检索**：`SearchMemory` 支持传入 `project_ids` 数组，在多个记忆片段规则下联合检索；
- **自动信息提取**：`AddMemory` 接收原始对话（`messages`）或自定义文本（`custom_content`），自动提取关键意图与事实，生成结构化记忆内容。

> **注意**：当前文档中未明确说明所依赖的底层大模型（如 Qwen 系列版本），但 [长期记忆（新）API 参考](../../raw/application-api-reference/long-term-memory-new/long-term-memory-api-reference.md) 明确指出其能力由平台统一调度，开发者无需指定模型 ID；若其他文档声称需显式传入 `model` 参数，则以本 [原文标题](../../raw/application-api-reference/long-term-memory-new/long-term-memory-api-reference.md) 为准。

## 关键参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `user_id` | string | 是 | 记忆归属实体标识，最大 64 字符，用于数据隔离 |
| `messages` / `custom_content` | array / string | 互斥必填 | `messages` 为对话数组（最多 50 条，一问一答计 2 条）；`custom_content` 为纯文本（≤512 字符），优先级高于 `messages` |
| `memory_library_id` | string | 否 | 记忆库 ID（32 字符内），不传则使用默认库；可在[记忆库](https://bailian.console.aliyun.com/cn-beijing/?tab=app#/memory/list)页面获取 |
| `profile_schema` | string | 否 | 画像模板 ID，用于指导记忆提取逻辑；详情见 [原文标题](../../raw/application-api-reference/long-term-memory-new/long-term-memory-api-reference.md) 中“创建画像模板”部分 |
| `top_k` | integer | 否 | `SearchMemory` 最大召回数，默认 10，范围 1–100 |
| `min_score` | double | 否 | `SearchMemory` 相似度阈值，默认 0.3，范围 [0,1] |
| `enable_rerank` / `enable_rewrite` | boolean | 否 | 控制是否启用重排序与 query 重写，默认均为 `false` |

## 使用方式

### 1. 基础配置
- Base URL：`https://dashscope.aliyuncs.com/api/v2/apps/memory/`
- 认证：Header 中携带 `Authorization: Bearer $DASHSCOPE_API_KEY`（API Key 获取方式见 [原文标题](../../raw/application-api-reference/long-term-memory-new/long-term-memory-api-reference.md)）
- Content-Type：`application/json`

### 2. 推荐调用路径
- **初始化**：先通过控制台创建记忆库，再调用 `CreateProfileSchema` 定义画像模板（可选但推荐）；
- **存入记忆**：调用 `AddMemory`，传入 `user_id` 和 `messages` 或 `custom_content`；
- **检索记忆**：调用 `SearchMemory`，传入当前对话上下文（`messages`）及 `user_id`，获取语义相关记忆；
- **维护记忆**：使用 `ListMemory` 分页浏览，`UpdateMemory` 或 `DeleteMemory` 按需修正或清理。

### 3. SDK 示例（Python）
需安装 `agentscope-runtime>=1.1.5`：
```python
from agentscope_runtime.tools.modelstudio_memory import AddMemory, SearchMemory, Message
import asyncio

async def main():
    # 添加记忆
    add = AddMemory()
    await add.arun({"user_id": "u1", "messages": [Message("user", "明天9点开会")]})

    # 搜索记忆
    search = SearchMemory()
    res = await search.arun({
        "user_id": "u1",
        "messages": [Message("user", "我明天有什么安排？")],
        "top_k": 3
    })
    print([n.content for n in res.memory_nodes])
```

## 限制和注意事项

- **限流策略（阿里云账号级别）**：
  - 所有接口总 QPM ≤ 3000；
  - `AddMemory` 单独限流 120 QPM；
  - `SearchMemory` 单独限流 300 QPM；
- **数据时效性**：生成的记忆片段与用户画像**暂无自动失效机制**，需业务侧自行管理生命周期；
- **内容长度**：`custom_content` 最大 512 字符；`messages` 单次最多 50 条记录；
- **字段兼容性**：`UpdateMemory` 的 `timestamp` 为秒级 Unix 时间戳（非毫秒），默认使用当前时间；
- **SDK 覆盖度**：`UpdateMemory` 当前未被 `agentscope-runtime` 封装，需直接调用 REST API（参见 [原文标题](../../raw/application-api-reference/long-term-memory-new/long-term-memory-api-reference.md) 中的 cURL 示例）；
- **错误处理**：所有接口返回 `request_id`，可用于问题排查与服务端日志关联。

## 来源文档

- [长期记忆（新）API 参考](../../raw/application-api-reference/long-term-memory-new/long-term-memory-api-reference.md)



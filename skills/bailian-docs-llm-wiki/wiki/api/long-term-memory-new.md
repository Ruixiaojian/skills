# long term memory new

[长期记忆](../concepts/long-term-memory.md)（新）是百炼平台提供的结构化用户记忆管理能力，支持将对话自动提炼为可检索、可更新的记忆片段，并关联用户画像。该功能基于语义理解构建，适用于个性化推荐、上下文延续、用户习惯建模等场景。所有 API 均需通过 `Authorization: Bearer $DASHSCOPE_API_KEY` 认证，Base URL 为 `https://dashscope.aliyuncs.com/api/v2/apps/memory/`。详细接口定义与行为请参见 [长期记忆（新）API 参考](../../raw/application-api-reference/long-term-memory-new/long-term-memory-api-reference.md)。

## 支持的模型/功能

- **记忆片段管理**：支持添加（`AddMemory`）、搜索（`SearchMemory`）、列出（`ListMemory`）、删除（`DeleteMemory`）和更新（`UpdateMemory`）记忆节点。
- **用户画像建模**：支持创建、查询、更新、删除画像模板（`ProfileSchema`），并基于模板生成/获取用户画像（`GetUserProfile`）。
- **多规则混合检索**：`SearchMemory` 支持传入 `project_ids` 数组，在多个记忆片段规则下联合召回。
- **语义增强能力**：`SearchMemory` 可选开启 query 重写（`enable_rewrite`）、意图判别（`enable_judge`）和结果重排序（`enable_rerank`）。

> **注意**：Python SDK 中 `UpdateMemory` 接口暂未封装进 `agentscope-runtime`（见 [长期记忆（新）API 参考](../../raw/application-api-reference/long-term-memory-new/long-term-memory-api-reference.md) 中 Python 示例说明），需直接调用 REST API 实现。

## 关键参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `user_id` | string | 是 | 记忆归属实体 ID（≤64 字符），用于隔离不同用户的记忆空间 |
| `messages` / `custom_content` | array / string | 互斥 | `messages` 为对话数组（最多 50 条，一问一答计 2 条）；`custom_content` 为纯文本（≤512 字符），二者填一则忽略另一方 |
| `memory_library_id` | string | 否 | 记忆库 ID（≤32 字符），不传则使用默认库 |
| `project_id` / `project_ids` | string / list | 否 | 单条操作指定规则 ID；搜索时支持传入数组实现跨规则混合检索 |
| `top_k` | integer | 否 | `SearchMemory` 最大召回数（1–100，默认 10） |
| `min_score` | double | 否 | `SearchMemory` 相似度阈值 [0,1]（默认 0.3） |
| `meta_data` | object | 否 | 用户自定义键值对，支持增量更新（如 `UpdateMemory` 中） |

## 使用方式

### 1. 添加记忆
```python
from agentscope_runtime.tools.modelstudio_memory import AddMemory, Message, AddMemoryInput
import asyncio

async def add():
    tool = AddMemory()
    result = await tool.arun(AddMemoryInput(
        user_id="user_001",
        messages=[
            Message(role="user", content="每天上午9点提醒我喝水"),
            Message(role="assistant", content="好的，已记录")
        ],
        meta_data={"category": "提醒"}
    ))
    print(f"新增 {len(result.memory_nodes)} 个记忆片段")
```

### 2. 搜索记忆
```python
from agentscope_runtime.tools.modelstudio_memory import SearchMemory, Message, SearchMemoryInput

async def search():
    tool = SearchMemory()
    result = await tool.arun(SearchMemoryInput(
        user_id="user_001",
        messages=[Message(role="user", content="明天有什么日程？")],
        top_k=5,
        min_score=0.5
    ))
    for node in result.memory_nodes:
        print(node.content)
```

### 3. 列出与分页
```python
from agentscope_runtime.tools.modelstudio_memory import ListMemory, ListMemoryInput

async def list_all():
    tool = ListMemory()
    result = await tool.arun(ListMemoryInput(
        user_id="user_001",
        page_num=1,
        page_size=20
    ))
    print(f"共 {result.total} 条，当前页 {len(result.memory_nodes)} 条")
```

完整接口路径与请求示例详见 [长期记忆（新）API 参考](../../raw/application-api-reference/long-term-memory-new/long-term-memory-api-reference.md)。

## 限制和注意事项

- **限流策略（阿里云账号级）**：
  - 所有接口合计 ≤ 3000 QPM；
  - `AddMemory` ≤ 120 QPM；
  - `SearchMemory` ≤ 300 QPM。
- **内容长度限制**：
  - `custom_content` 和 `messages` 提取后的 `content` 字段均 ≤ 512 字符；
  - `messages` 数组最多 50 条（含 `user`/`assistant` 交替）。
- **时效性**：当前版本的记忆片段与用户画像**无自动过期机制**，需业务侧自行管理生命周期。
- **ID 约束**：`user_id`、`memory_library_id`、`profile_schema_id` 等 ID 字段均区分大小写，且不可含空格或特殊字符（仅支持字母、数字、下划线、短横线）。
- **认证要求**：所有请求必须携带 `Authorization: Bearer $DASHSCOPE_API_KEY` Header，API Key 获取方式见 [获取 API Key](https://help.aliyun.com/zh/model-studio/get-api-key)，该说明亦在 [长期记忆（新）API 参考](../../raw/application-api-reference/long-term-memory-new/long-term-memory-api-reference.md) 的“公共请求信息”章节中明确。

## 来源文档

- [长期记忆（新）API 参考](../../raw/application-api-reference/long-term-memory-new/long-term-memory-api-reference.md)



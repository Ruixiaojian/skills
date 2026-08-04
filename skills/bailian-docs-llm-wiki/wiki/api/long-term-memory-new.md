# long term memory new

[长期记忆](../concepts/long-term-memory.md)（新）是百炼平台提供的结构化用户状态管理能力，支持将对话自动提炼为可检索、可更新的记忆片段，并支持基于画像模板的用户建模。该能力通过 REST API 和 `agentscope-runtime` SDK 提供，适用于构建具备上下文感知与长期状态保持的智能体应用。详细设计与语义处理逻辑参见 [长期记忆（新）API 参考](../../raw/application-api-reference/long-term-memory-new/long-term-memory-api-reference.md)。

## 支持的模型/功能

- **记忆片段管理**：支持 `AddMemory`（自动提取对话关键信息）、`SearchMemory`（语义相似度检索）、`ListMemory`（分页查询）、`DeleteMemory`、`UpdateMemory`。
- **用户画像建模**：通过 `CreateProfileSchema` 等接口定义并管理画像模板，支持关联记忆片段生成结构化用户画像（`GetUserProfile`）。
- **多规则混合检索**：`SearchMemory` 支持传入 `project_ids` 数组，在多个记忆片段规则下联合召回，提升覆盖广度。
- 所有接口均基于 DashScope 统一认证体系，无需额外模型部署或向量库运维。具体接口路径与行为定义详见 [长期记忆（新）API 参考](../../raw/application-api-reference/long-term-memory-new/long-term-memory-api-reference.md)。

## 关键参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `user_id` | string | 是 | 记忆归属实体 ID（≤64 字符），用于隔离不同用户的记忆空间 |
| `messages` / `custom_content` | array / string | 互斥必填 | `messages` 为对话数组（最多 50 条，一问一答计 2 条）；`custom_content` 为纯文本输入（≤512 字符），二者同时存在时优先使用 `custom_content` |
| `memory_library_id` | string | 否 | 记忆库 ID（≤32 字符），未提供时使用默认记忆库；可在控制台 [记忆库列表](https://bailian.console.aliyun.com/cn-beijing/?tab=app#/memory/list) 获取 |
| `top_k`（SearchMemory） | integer | 否 | 最大召回数，默认 10，取值范围 1–100 |
| `min_score`（SearchMemory） | double | 否 | 相似度阈值，默认 0.3，取值范围 [0, 1] |
| `project_id` / `project_ids` | string / list | 否 | 指定记忆片段规则 ID；`SearchMemory` 中支持多 ID 混合检索 |
| `meta_data` | object | 否 | 用户自定义键值对，随记忆片段持久化存储，支持增量更新（仅 `UpdateMemory`） |

> **注意**：`AddMemory` 的 `messages` 字段中 `content` 支持 string 或 array 类型（如含图像 URL 的多模态消息），但当前版本仅对 text 内容进行语义提取；该限制在 [长期记忆（新）API 参考](../../raw/application-api-reference/long-term-memory-new/long-term-memory-api-reference.md) 的示例中未明确标注，需以实际 API 响应为准。

## 使用方式

### 1. 基础调用（REST）
- Base URL：`https://dashscope.aliyuncs.com/api/v2/apps/memory/`
- 认证：Header `Authorization: Bearer $DASHSCOPE_API_KEY`
- Content-Type：`application/json`

示例（添加记忆）：
```bash
curl -X POST https://dashscope.aliyuncs.com/api/v2/apps/memory/add \
  -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "user_001",
    "messages": [{"role":"user","content":"明天10点提醒我开会"}],
    "meta_data": {"source": "web_chat"}
  }'
```

### 2. Python SDK（推荐）
需安装 `agentscope-runtime>=1.1.5`：
```python
from agentscope_runtime.tools.modelstudio_memory import AddMemory, AddMemoryInput
import asyncio

async def main():
    adder = AddMemory()
    result = await adder.arun(AddMemoryInput(
        user_id="user_001",
        messages=[{"role": "user", "content": "每天9点提醒我吃药"}],
        meta_data={"category": "health"}
    ))
    print(f"新增 {len(result.memory_nodes)} 条记忆")
    await adder.close()
```

> **注意**：`UpdateMemory` 当前未被 `agentscope-runtime` 封装，必须使用 `requests` 直接调用 PATCH 接口，详见 [长期记忆（新）API 参考](../../raw/application-api-reference/long-term-memory-new/long-term-memory-api-reference.md) 中的 Python 示例。

## 限制和注意事项

- **限流**：全接口总 QPM ≤ 3000（阿里云账号级别）；其中 `AddMemory` ≤ 120 QPM，`SearchMemory` ≤ 300 QPM。
- **内容长度**：`custom_content` ≤ 512 字符；`messages` 中单条 `content` 长度无显式限制，但过长文本可能影响提取质量。
- **时效性**：记忆片段与用户画像**无自动过期机制**，需业务侧自行管理生命周期。
- **ID 约束**：`user_id`、`memory_library_id`、`memory_node_id` 均为字符串，禁止包含 `/`、`?`、`#` 等 URL 不安全字符。
- **空值处理**：`ListMemory` 返回的 `meta_data` 字段可能为 `null`，调用方需做空判断；`SearchMemory` 的 `min_score=0` 仍可能因语义匹配失败返回空数组。

## 来源文档

- [长期记忆（新）API 参考](../../raw/application-api-reference/long-term-memory-new/long-term-memory-api-reference.md)



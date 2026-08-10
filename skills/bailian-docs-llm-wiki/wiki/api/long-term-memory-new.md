# long term memory new

[长期记忆](../concepts/long-term-memory.md)（新）是百炼平台提供的结构化用户记忆管理能力，支持自动从对话中提取关键信息、构建用户画像，并提供语义搜索、增删改查等完整生命周期操作。该功能基于专用记忆模型实现，所有 API 均通过统一的 `https://dashscope.aliyuncs.com/api/v2/apps/memory/` 接口域提供服务。详细接口定义与行为规范请参见 [长期记忆（新）API 参考](../../raw/application-api-reference/long-term-memory-new/long-term-memory-api-reference.md)。

## 支持的模型与功能

- **底层模型**：由百炼平台统一调度专用记忆理解与检索模型，开发者无需指定具体模型名称。
- **核心功能**：
  - `AddMemory`：自动解析对话或自定义文本，生成结构化记忆片段；
  - `SearchMemory`：基于语义相似度召回相关记忆，支持 `top_k`、`min_score`、重排序与 query 重写；
  - `ListMemory`：分页列出指定用户的全部记忆片段；
  - `DeleteMemory` / `UpdateMemory`：按 `memory_node_id` 精确管理单条记忆；
  - 画像模板管理（`CreateProfileSchema` 等）：定义用户属性结构，支撑画像生成；
  - 用户画像获取（`GetUserProfile`）：返回结构化用户特征摘要。

> **注意**：文档中未明确说明是否支持[多模态](../concepts/multi-modal.md)输入（如图像、音频），当前所有接口仅接受文本型 `messages.content` 或 `custom_content`，实际能力以 [长期记忆（新）API 参考](../../raw/application-api-reference/long-term-memory-new/long-term-memory-api-reference.md) 中的参数类型定义为准。

## 关键参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `user_id` | string | 是 | 记忆归属实体 ID（≤64 字符），用于隔离不同用户数据 |
| `messages` | array | 否（与 `custom_content` 互斥） | 对话消息列表，每条含 `role`（`user`/`assistant`）和 `content`；最多 50 条（一问一答计为 2 条） |
| `custom_content` | string | 否（与 `messages` 互斥） | 纯文本内容（≤512 字符），绕过对话解析直接存入 |
| `memory_library_id` | string | 否 | 指定记忆库 ID（≤32 字符）；不传则使用默认库 |
| `profile_schema` | string | 否 | 画像模板 ID，影响记忆提取字段与画像生成逻辑 |
| `top_k` | integer | 否（SearchMemory） | 搜索召回最大数量（1–100，默认 10） |
| `min_score` | double | 否（SearchMemory） | 相似度阈值 [0,1]（默认 0.3） |

所有请求需在 Header 中携带 `Authorization: Bearer $DASHSCOPE_API_KEY` 和 `Content-Type: application/json`，详见 [长期记忆（新）API 参考](../../raw/application-api-reference/long-term-memory-new/long-term-memory-api-reference.md)。

## 使用方式

### 1. HTTP 直调
Base URL：`https://dashscope.aliyuncs.com/api/v2/apps/memory/`  
示例（添加记忆）：
```bash
curl -X POST https://dashscope.aliyuncs.com/api/v2/apps/memory/add \
  -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "user_001",
    "messages": [{"role":"user","content":"每天9点提醒我喝水"}],
    "meta_data": {"source": "app_v2"}
  }'
```

### 2. Python SDK（推荐）
需安装 `agentscope-runtime>=1.1.5`：
```python
from agentscope_runtime.tools.modelstudio_memory import AddMemory, AddMemoryInput
import asyncio

async def main():
    tool = AddMemory()
    result = await tool.arun(AddMemoryInput(
        user_id="user_001",
        messages=[{"role": "user", "content": "明天开会"}],
        meta_data={"project": "Q3"}
    ))
    print(f"生成 {len(result.memory_nodes)} 条记忆")
    await tool.close()

asyncio.run(main())
```
> **注意**：`UpdateMemory` 当前未被 `agentscope-runtime` 封装，需自行用 `requests.patch` 调用，具体见 [长期记忆（新）API 参考](../../raw/application-api-reference/long-term-memory-new/long-term-memory-api-reference.md) 中的示例。

## 限制和注意事项

- **限流策略（阿里云账号级别）**：
  - 所有接口总 QPM ≤ 3000；
  - `AddMemory` 单独限流 120 QPM；
  - `SearchMemory` 单独限流 300 QPM。
- **数据时效性**：记忆片段与用户画像无自动过期机制，需业务侧自行管理生命周期。
- **内容长度**：`custom_content` 和单条 `messages.content` 均 ≤ 512 字符；`messages` 数组最多 50 项。
- **互斥约束**：`messages` 与 `custom_content` 不可同时存在，后者优先级更高。
- **错误处理**：HTTP 状态码非 2xx 时，响应体含 `code` 与 `message` 字段，需解析判断具体失败原因（如 `INVALID_ARGUMENT`、`NOT_FOUND`）。

## 来源文档

- [长期记忆（新）API 参考](../../raw/application-api-reference/long-term-memory-new/long-term-memory-api-reference.md)



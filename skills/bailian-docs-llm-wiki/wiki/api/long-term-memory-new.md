# long term memory new

[长期记忆](../concepts/long-term-memory.md)（新）是百炼平台提供的结构化用户记忆管理能力，支持将对话自动提炼为可检索、可更新的记忆片段，并支持基于画像模板的用户画像构建。该功能通过 REST API 和 Python SDK 提供完整 CRUD 能力，适用于需要持久化用户偏好、习惯、意图等上下文信息的智能体应用。详细接口定义与行为规范见 [长期记忆（新）API 参考](../../raw/application-api-reference/long-term-memory-new/long-term-memory-api-reference.md)。

## 支持的模型/功能

- **记忆片段管理**：支持 `AddMemory`、`SearchMemory`、`ListMemory`、`DeleteMemory`、`UpdateMemory` 五类核心操作，覆盖记忆的创建、语义搜索、分页查询、删除与内容更新。
- **用户画像构建**：通过 `CreateProfileSchema` 等画像模板相关接口，定义结构化字段（如 `age`, `occupation`, `preference`），并关联至 `GetUserProfile` 获取聚合画像。
- **多规则混合检索**：`SearchMemory` 支持传入 `project_ids` 数组，在多个记忆片段规则下联合召回，提升跨场景记忆覆盖度。
- **端到端 SDK 封装**：`agentscope-runtime>=1.1.5` 提供 `AddMemory`、`SearchMemory`、`ListMemory`、`DeleteMemory` 的异步 Python 工具类封装；但 `UpdateMemory` 当前未被 SDK 封装，需直接调用 REST API —— 此限制已在 [长期记忆（新）API 参考](../../raw/application-api-reference/long-term-memory-new/long-term-memory-api-reference.md) 的 UpdateMemory 章节明确说明。

> **注意**：原始文档中 `UpdateMemory` 的 Python 示例使用 `requests.patch` 手动调用，而其他接口均提供 `agentscope-runtime` 封装。SDK 文档未声明对该接口的未来支持计划，开发者应避免依赖未封装接口的抽象层一致性。

## 关键参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `user_id` | `string` | 是 | 记忆归属实体 ID（≤64 字符），所有接口均需指定，用于隔离不同用户数据。 |
| `messages` / `custom_content` | `array` / `string` | 互斥必填 | `AddMemory` 中二选一：`messages` 支持最多 50 条对话（一问一答计为 2 条），自动提取；`custom_content` 为纯文本（≤512 字符），绕过自动解析。详见 [长期记忆（新）API 参考](../../raw/application-api-reference/long-term-memory-new/long-term-memory-api-reference.md)。 |
| `memory_library_id` | `string` | 否 | 显式指定记忆库 ID（≤32 字符）；不传则使用默认记忆库。可在控制台 [记忆库列表页](https://bailian.console.aliyun.com/cn-beijing/?tab=app#/memory/list) 获取。 |
| `top_k` | `integer` | 否（`SearchMemory`） | 搜索召回数量，默认 `10`，取值范围 `1–100`。 |
| `min_score` | `double` | 否（`SearchMemory`） | 相似度阈值，默认 `0.3`，范围 `[0,1]`；设为 `0` 可返回全部匹配项（受 `top_k` 限制）。 |
| `meta_data` | `object` | 否 | 用户自定义键值对，支持任意 JSON 对象，用于扩展元信息（如地理位置、设备类型等）。 |

## 使用方式

### 1. 基础认证
所有请求需在 Header 中携带：
```http
Authorization: Bearer $DASHSCOPE_API_KEY
Content-Type: application/json
```
API Key 获取方式见 [获取 API Key](https://help.aliyun.com/zh/model-studio/get-api-key)。

### 2. 接口调用示例（REST）
- **添加记忆**（自动解析对话）：
  ```bash
  curl -X POST https://dashscope.aliyuncs.com/api/v2/apps/memory/add \
    -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
    -H "Content-Type: application/json" \
    -d '{
      "user_id": "user_001",
      "messages": [{"role":"user","content":"明天10点提醒我开会"}]
    }'
  ```
- **语义搜索**（带过滤）：
  ```bash
  curl -X POST https://dashscope.aliyuncs.com/api/v2/apps/memory/memory_nodes/search \
    -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
    -H "Content-Type: application/json" \
    -d '{
      "user_id": "user_001",
      "messages": [{"role":"user","content":"我有什么待办？"}],
      "top_k": 5,
      "min_score": 0.5
    }'
  ```

### 3. Python SDK 调用（推荐）
安装依赖：
```bash
pip install agentscope-runtime>=1.1.5
```
使用封装工具（以 `AddMemory` 为例）：
```python
from agentscope_runtime.tools.modelstudio_memory import AddMemory, Message, AddMemoryInput
import asyncio

async def main():
    tool = AddMemory()
    try:
        res = await tool.arun(AddMemoryInput(
            user_id="user_001",
            messages=[Message(role="user", content="每天9点提醒我吃药")],
            meta_data={"source": "mobile_app"}
        ))
        print(f"生成 {len(res.memory_nodes)} 条记忆")
    finally:
        await tool.close()
```
> **注意**：`UpdateMemory` 无对应 SDK 封装，必须使用 `requests.patch` 手动调用，具体参数格式请严格参照 [长期记忆（新）API 参考](../../raw/application-api-reference/long-term-memory-new/long-term-memory-api-reference.md)。

## 限制和注意事项

- **限流策略**（阿里云账号级别）：
  - 全部接口总 QPM ≤ 3000；
  - `AddMemory` 单独限流 120 QPM；
  - `SearchMemory` 单独限流 300 QPM。
- **数据生命周期**：当前生成的记忆片段与用户画像**无自动失效机制**，需业务侧自行管理过期逻辑。
- **内容长度约束**：
  - `custom_content` 最大 512 字符；
  - `messages` 中单条 `content` 无明确长度限制，但整组 `messages` 不得超过 50 条。
- **默认行为**：`memory_library_id` 和 `project_id` 等参数若未显式传入，系统将自动选择默认值，但生产环境建议显式指定以避免配置漂移。
- **时间戳精度**：`UpdateMemory` 的 `timestamp` 字段为秒级 Unix 时间戳；若未提供，则使用请求发起时刻。

## 来源文档

- [长期记忆（新）API 参考](../../raw/application-api-reference/long-term-memory-new/long-term-memory-api-reference.md)



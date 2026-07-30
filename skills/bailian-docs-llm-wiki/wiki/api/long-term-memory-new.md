# long term memory new

[长期记忆](../concepts/long-term-memory.md)（新）是百炼平台提供的结构化用户记忆管理能力，支持自动从对话中提取关键信息、构建用户画像，并提供语义搜索、增删改查等完整生命周期管理接口。该功能基于专用记忆模型实现，所有记忆片段与用户画像默认永不过期。开发者可通过 REST API 或 `agentscope-runtime` SDK 快速集成。

## 支持的模型/功能

- **底层模型**：由百炼平台统一调度的专用记忆模型（非通用大模型），不对外暴露模型 ID，也不支持自定义模型替换。  
- **核心功能**：  
  - `AddMemory`：自动解析对话（最多 50 条消息）或接收自定义文本，生成结构化记忆片段；  
  - `SearchMemory`：基于语义相似度检索，支持 `top_k`、`min_score`、`enable_rerank` 等精细控制；  
  - `ListMemory` / `DeleteMemory` / `UpdateMemory`：标准 CRUD 操作；  
  - `ProfileSchema` 系列接口：定义并管理用户画像模板，用于约束记忆提取字段（如年龄、偏好、健康目标等）。  
- 所有功能均在 [长期记忆（新）API 参考](../../raw/application-api-reference/long-term-memory-new/long-term-memory-api-reference.md) 中完整定义，包括各接口的路径、参数和返回结构。

## 关键参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `user_id` | string | 是 | 记忆归属实体 ID（≤64 字符），用于隔离不同用户数据 |
| `messages` 或 `custom_content` | array / string | 互斥必填 | `messages` 为 role/content 对数组（一问一答计 2 条）；`custom_content` 为纯文本（≤512 字符），二者共存时优先使用 `custom_content` |
| `memory_library_id` | string | 否 | 记忆库 ID（≤32 字符），未传则使用默认库；可在控制台[记忆库](https://bailian.console.aliyun.com/cn-beijing/?tab=app#/memory/list)页面获取，详见 [长期记忆（新）API 参考](../../raw/application-api-reference/long-term-memory-new/long-term-memory-api-reference.md) |
| `profile_schema` | string | 否 | 画像模板 ID，用于指定记忆提取规则；需先通过 `CreateProfileSchema` 创建 |
| `top_k`（Search） | integer | 否 | 检索最大返回数（1–100，默认 10） |
| `min_score`（Search） | double | 否 | 相似度阈值 [0,1]（默认 0.3） |

> **注意**：`AddMemory` 接口文档中明确要求 `messages` 与 `custom_content` 互斥，但部分旧版 SDK 示例曾同时传入两者——请以 [长期记忆（新）API 参考](../../raw/application-api-reference/long-term-memory-new/long-term-memory-api-reference.md) 的权威定义为准，避免被忽略。

## 使用方式

### 1. 基础认证
所有请求需在 Header 中携带：
```http
Authorization: Bearer $DASHSCOPE_API_KEY
Content-Type: application/json
```
API Key 获取方式见 [获取 API Key](https://help.aliyun.com/zh/model-studio/get-api-key)。

### 2. 推荐 SDK 调用（Python）
安装依赖：
```bash
pip install agentscope-runtime>=1.1.5
```

示例（添加记忆）：
```python
from agentscope_runtime.tools.modelstudio_memory import AddMemory, Message, AddMemoryInput
import asyncio

async def add_example():
    tool = AddMemory()
    try:
        result = await tool.arun(AddMemoryInput(
            user_id="user_001",
            messages=[Message(role="user", content="每天9点提醒我吃药")],
            meta_data={"category": "health"}
        ))
        print(f"生成 {len(result.memory_nodes)} 个片段")
    finally:
        await tool.close()
```

### 3. REST API 直调（cURL）
```bash
curl -X POST https://dashscope.aliyuncs.com/api/v2/apps/memory/add \
  -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "user_001",
    "custom_content": "用户计划下周去杭州出差",
    "meta_data": {"trip_city": "hangzhou"}
  }'
```

完整接口路径与方法详见 [长期记忆（新）API 参考](../../raw/application-api-reference/long-term-memory-new/long-term-memory-api-reference.md) 的“接口概览”章节。

## 限制和注意事项

- **限流策略（阿里云账号级）**：  
  - 全部接口总 QPM ≤ 3000；  
  - `AddMemory` 单独限流 120 QPM；  
  - `SearchMemory` 单独限流 300 QPM。  
- **数据时效性**：所有记忆片段与用户画像**无自动过期机制**，需业务侧自行管理生命周期。  
- **内容长度**：`custom_content` 最大 512 字符；`messages` 最多 50 条（含 user/assistant 交替）。  
- **SDK 兼容性**：`UpdateMemory` 接口暂未封装进 `agentscope-runtime`，需用 `requests` 等 HTTP 库直接调用（参考原始文档示例）。  
- **错误处理**：所有接口返回 `request_id`，用于问题排查；建议在生产环境记录该 ID。

## 来源文档

- [长期记忆（新）API 参考](../../raw/application-api-reference/long-term-memory-new/long-term-memory-api-reference.md)



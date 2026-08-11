# long term memory new

[长期记忆](../concepts/long-term-memory.md)（新）是百炼平台提供的结构化用户记忆管理能力，支持自动从对话中提取关键信息、构建用户画像，并提供语义搜索、增删改查等完整生命周期操作。该能力基于专用记忆模型实现，与传统向量检索解耦，强调语义理解与意图建模。详细接口定义和行为约束请参见 [长期记忆（新）API 参考](../../raw/application-api-reference/long-term-memory-new/long-term-memory-api-reference.md)。

## 支持的模型/功能

- **底层模型**：由平台统一调度专用记忆模型（非用户可选 LLM），不暴露模型名称或版本，所有 API 调用均隐式绑定该能力。
- **核心功能**：
  - `AddMemory`：自动解析对话（`messages`）或接收自定义文本（`custom_content`），生成结构化记忆片段；
  - `SearchMemory`：基于语义相似度召回相关记忆，支持 `top_k`、`min_score`、`enable_rerank` 等控制参数；
  - `ListMemory` / `DeleteMemory` / `UpdateMemory`：标准 CRUD 操作；
  - `ProfileSchema` 系列接口：管理用户画像模板（schema），用于约束画像字段结构；
  - `GetUserProfile`：按 schema 获取聚合后的用户画像。

> **注意**：文档中未提及任何支持第三方模型接入或自定义记忆模型替换的能力，所有调用均强制使用平台预置模型。此设计与旧版[长期记忆](../concepts/long-term-memory.md)（已下线）存在本质差异，[长期记忆（新）API 参考](../../raw/application-api-reference/long-term-memory-new/long-term-memory-api-reference.md) 明确指出“生成的记忆片段与用户画像暂无失效日期”，而旧版文档曾描述过 TTL 机制——该信息已过时，以本页为准。

## 关键参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `user_id` | string | 是 | 记忆归属实体 ID（≤64 字符），用于隔离不同用户数据 |
| `messages` | array | 条件必填 | 对话消息列表，每条含 `role`（`user`/`assistant`）和 `content`；最多 50 条（一问一答计 2 条） |
| `custom_content` | string | 条件必填 | 自定义文本内容（≤512 字符），与 `messages` 互斥 |
| `memory_library_id` | string | 否 | 记忆库 ID（≤32 字符）；不传则使用默认库，详见 [长期记忆（新）API 参考](../../raw/application-api-reference/long-term-memory-new/long-term-memory-api-reference.md) |
| `profile_schema` | string | 否 | 画像模板 ID，用于指定记忆提取所依据的 schema |
| `top_k` | integer | 否 | `SearchMemory` 最大召回数（1–100，默认 10） |
| `min_score` | double | 否 | `SearchMemory` 相似度阈值 [0,1]（默认 0.3） |

## 使用方式

### 1. 基础认证
所有请求需在 Header 中携带：
```http
Authorization: Bearer $DASHSCOPE_API_KEY
Content-Type: application/json
```
API Key 获取方式见 [获取 API Key](https://help.aliyun.com/zh/model-studio/get-api-key)。

### 2. 接口调用示例（cURL）
```bash
# 添加记忆（对话模式）
curl -X POST https://dashscope.aliyuncs.com/api/v2/apps/memory/add \
  -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "user_001",
    "messages": [{"role":"user","content":"明天10点提醒我整理会议纪要"}],
    "meta_data": {"source": "web_chat"}
  }'

# 搜索记忆
curl -X POST https://dashscope.aliyuncs.com/api/v2/apps/memory/memory_nodes/search \
  -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "user_001",
    "messages": [{"role":"user","content":"我有什么待办？"}],
    "top_k": 5,
    "min_score": 0.4
  }'
```

### 3. Python SDK（推荐）
需安装 `agentscope-runtime>=1.1.5`：
```python
from agentscope_runtime.tools.modelstudio_memory import AddMemory, SearchMemory, SearchMemoryInput
import asyncio

async def main():
    add_tool = AddMemory()
    search_tool = SearchMemory()
    
    # 添加
    await add_tool.arun({"user_id": "user_001", "messages": [...]})
    
    # 搜索
    result = await search_tool.arun(SearchMemoryInput(
        user_id="user_001",
        messages=[{"role": "user", "content": "提醒事项"}],
        top_k=3
    ))
    print([node.content for node in result.memory_nodes])
```

## 限制和注意事项

- **限流策略（阿里云账号级别）**：
  - 所有接口总计 ≤ 3000 QPM；
  - `AddMemory` 单独限流 ≤ 120 QPM；
  - `SearchMemory` 单独限流 ≤ 300 QPM；
- **数据持久性**：记忆片段与用户画像**无自动过期机制**，需业务侧自行管理生命周期（如通过 `DeleteMemory` 清理）；
- **内容长度**：`custom_content` ≤ 512 字符；`messages` 总条数 ≤ 50；
- **ID 约束**：`user_id` 和 `memory_library_id` 长度分别 ≤ 64 和 32 字符，且仅支持 ASCII 字符；
- **Schema 依赖**：若使用 `profile_schema`，必须先通过 `CreateProfileSchema` 创建并获取 ID，否则添加/搜索可能降级为通用提取；
- **Python SDK 缺失接口**：`UpdateMemory` 当前未被 `agentscope-runtime` 封装，需直接调用 REST API（见原始文档示例）；
- **调试建议**：首次集成时，优先使用 `ListMemory` 验证数据写入是否成功，并检查 `request_id` 用于问题排查。

## 来源文档

- [长期记忆（新）API 参考](../../raw/application-api-reference/long-term-memory-new/long-term-memory-api-reference.md)



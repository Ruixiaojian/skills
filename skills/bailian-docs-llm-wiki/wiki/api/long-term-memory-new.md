# long term memory new

[长期记忆](../concepts/long-term-memory.md)（新）是百炼平台提供的结构化用户记忆管理能力，支持自动从对话中提取关键信息生成记忆片段，并提供语义搜索、增删改查等完整生命周期操作。该功能基于专用记忆模型实现，无需用户自行调用大模型进行摘要或向量化，所有语义理解与检索均由服务端统一处理。详细接口定义与行为规范请参见 [长期记忆（新）API 参考](../../raw/application-api-reference/long-term-memory-new/long-term-memory-api-reference.md)。

## 支持的模型/功能

- **底层模型**：由百炼平台统一托管的专用记忆模型（非公开型号），不对外暴露模型 ID，开发者无需指定或切换模型。
- **核心功能**：
  - `AddMemory`：自动解析对话（`messages`）或接收自定义文本（`custom_content`），生成结构化记忆片段；
  - `SearchMemory`：基于语义相似度检索相关记忆，支持 `top_k`、`min_score`、`enable_rerank` 等控制参数；
  - `ListMemory`：分页列出指定 `user_id` 的全部记忆片段；
  - `DeleteMemory` / `UpdateMemory`：按 `memory_node_id` 精确操作单个记忆片段；
  - `ProfileSchema` 系列接口：管理用户画像模板（schema），用于约束记忆提取的字段结构。

> **注意**：文档中提及的 `agentscope-runtime>=1.1.5` SDK 封装仅覆盖 `AddMemory`、`SearchMemory`、`ListMemory` 和 `DeleteMemory`，但 `UpdateMemory` 在 Python 中明确标注为“暂未提供封装”，需直接调用 REST API —— 此不一致已在 [长期记忆（新）API 参考](../../raw/application-api-reference/long-term-memory-new/long-term-memory-api-reference.md) 中如实说明，开发者应以该文档为准。

## 关键参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `user_id` | string | 是 | 记忆归属实体标识（≤64 字符），所有接口均需传入 |
| `messages` 或 `custom_content` | array / string | 互斥必填 | `messages` 最多 50 条（一问一答计 2 条）；`custom_content` ≤512 字符 |
| `memory_library_id` | string | 否 | 指定记忆库 ID（≤32 字符），不传则使用默认库 |
| `profile_schema` | string | 否 | 画像模板 ID，影响记忆提取的字段结构 |
| `top_k`（Search） | integer | 否 | 召回数量，默认 10，范围 1–100 |
| `min_score`（Search） | double | 否 | 相似度阈值，默认 0.3，范围 [0,1] |
| `page_num` / `page_size`（List） | integer | 否 | 分页参数，默认 `page_num=1`, `page_size=10` |

所有请求必须携带 `Authorization: Bearer $DASHSCOPE_API_KEY` 头，且 `Content-Type: application/json`。更多参数细节请参考 [长期记忆（新）API 参考](../../raw/application-api-reference/long-term-memory-new/long-term-memory-api-reference.md)。

## 使用方式

1. **基础调用**：直接通过 HTTP 请求访问 `https://dashscope.aliyuncs.com/api/v2/apps/memory/{path}`；
2. **Python SDK**（推荐）：
   - 安装：`pip install agentscope-runtime>=1.1.5`
   - 导入对应工具类（如 `AddMemory`, `SearchMemory`, `ListMemory`, `DeleteMemory`），传入 `Input` 对象并调用 `arun()`；
   - 注意：`UpdateMemory` 无 SDK 封装，需用 `requests.patch` 手动调用；
3. **cURL 示例**：文档中每个接口均提供可直接运行的 cURL 命令，含完整 header 与 data 结构。

示例（添加记忆）：
```python
from agentscope_runtime.tools.modelstudio_memory import AddMemory, Message, AddMemoryInput
import asyncio

async def main():
    tool = AddMemory()
    result = await tool.arun(AddMemoryInput(
        user_id="user_001",
        messages=[Message(role="user", content="明天9点开会"), Message(role="assistant", content="已记录")],
        meta_data={"source": "web_chat"}
    ))
    print(f"生成 {len(result.memory_nodes)} 个片段")
```

## 限制和注意事项

- **限流策略**（阿里云账号级别）：
  - 全部接口总计 ≤3000 QPM；
  - `AddMemory` ≤120 QPM；
  - `SearchMemory` ≤300 QPM；
- **数据时效性**：生成的记忆片段与用户画像**无自动过期机制**，需业务侧自行清理；
- **内容长度**：`custom_content` 严格限制为 ≤512 字符；`messages` 中单条 `content` 无显式长度限制，但整体 `messages` 不得超过 50 条；
- **ID 约束**：`user_id` 和 `memory_library_id` 长度分别不得超过 64 和 32 字符，超长将导致 400 错误；
- **元数据更新**：`UpdateMemory` 的 `meta_data` 为**增量更新**（非全量覆盖），已有字段保留，新增字段合并写入。

如需了解完整错误码、返回结构及各接口边界条件，请务必查阅原始文档 [长期记忆（新）API 参考](../../raw/application-api-reference/long-term-memory-new/long-term-memory-api-reference.md)。

## 来源文档

- [长期记忆（新）API 参考](../../raw/application-api-reference/long-term-memory-new/long-term-memory-api-reference.md)



# long term memory new

[长期记忆](../concepts/memory.md)（新）是百炼平台提供的结构化用户记忆管理能力，支持自动从对话中提取关键信息、构建用户画像，并提供语义搜索、增删改查等完整生命周期操作。该能力基于专用记忆库和规则引擎实现，适用于需要持久化用户偏好、习惯、任务提醒等场景。详细接口定义与行为规范请参见 [长期记忆（新）API 参考](../../raw/application-api-reference/long-term-memory-new/long-term-memory-api-reference.md)。

## 支持的模型/功能

- **核心功能**：记忆片段自动提取（基于对话 `messages` 或自定义 `custom_content`）、语义搜索（`SearchMemory`）、分页列表（`ListMemory`）、单条增删改（`AddMemory`/`DeleteMemory`/`UpdateMemory`）
- **画像管理**：支持创建、查询、更新、删除画像模板（`ProfileSchema`），并基于模板生成用户画像（`GetUserProfile`）
- **底层模型**：由平台统一调度，开发者无需指定模型；所有记忆处理（如摘要生成、事件识别、语义向量化）均通过百炼内部模型链完成，具体模型选型不对外暴露
- **集成方式**：提供 RESTful API 和 Python SDK（`agentscope-runtime>=1.1.5`）两种调用方式，[长期记忆（新）API 参考](../../raw/application-api-reference/long-term-memory-new/long-term-memory-api-reference.md) 中包含全部接口路径与参数说明

## 关键参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `user_id` | string | 是 | 记忆归属实体 ID（≤64 字符），用于隔离不同用户数据 |
| `messages` / `custom_content` | array / string | 互斥必填 | `messages`：最多 50 条对话记录（一问一答计为 2 条）；`custom_content`：纯文本（≤512 字符），优先级高于 `messages` |
| `memory_library_id` | string | 否 | 记忆库 ID（≤32 字符），未传时使用默认库；可在控制台 [记忆库](https://bailian.console.aliyun.com/cn-beijing/?tab=app#/memory/list) 页面获取 |
| `profile_schema` | string | 否 | 画像模板 ID，决定记忆提取的结构化字段；未传则使用默认模板 |
| `top_k`, `min_score` | integer, double | 否（`SearchMemory`） | 搜索召回数量（1–100，默认 10）与最小相似度阈值（[0,1]，默认 0.3） |
| `page_num`, `page_size` | integer | 否（`ListMemory`） | 分页参数（默认 `page_num=1`, `page_size=10`） |

> **注意**：`UpdateMemory` 接口在 [长期记忆（新）API 参考](../../raw/application-api-reference/long-term-memory-new/long-term-memory-api-reference.md) 中明确要求 `custom_content` 为必填，但其 Python SDK 尚未封装该接口，需自行通过 `requests` 调用 —— 此为当前 SDK 功能滞后，非文档矛盾。

## 使用方式

### 1. 基础调用（REST API）
- Base URL：`https://dashscope.aliyuncs.com/api/v2/apps/memory/`
- 认证：Header 中携带 `Authorization: Bearer $DASHSCOPE_API_KEY`
- Content-Type：`application/json`
- 示例（添加记忆）：
  ```bash
  curl -X POST https://dashscope.aliyuncs.com/api/v2/apps/memory/add \
    -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
    -H "Content-Type: application/json" \
    -d '{
      "user_id": "user_001",
      "messages": [{"role":"user","content":"每天9点提醒我喝水"}],
      "meta_data": {"source": "mobile_app"}
    }'
  ```

### 2. Python SDK（推荐）
- 安装：`pip install agentscope-runtime>=1.1.5`
- 使用示例（搜索）：
  ```python
  from agentscope_runtime.tools.modelstudio_memory import SearchMemory, Message, SearchMemoryInput
  import asyncio

  async def main():
      search = SearchMemory()
      try:
          res = await search.arun(SearchMemoryInput(
              user_id="user_001",
              messages=[Message(role="user", content="明天有什么安排？")],
              top_k=5
          ))
          for node in res.memory_nodes:
              print(node.content)
      finally:
          await search.close()
  asyncio.run(main())
  ```
- 所有 SDK 工具类及输入类型定义均以 [长期记忆（新）API 参考](../../raw/application-api-reference/long-term-memory-new/long-term-memory-api-reference.md) 为准。

## 限制和注意事项

- **限流策略**（阿里云账号级别）：
  - 全部接口总 QPM ≤ 3000
  - `AddMemory` 单独限流 120 QPM
  - `SearchMemory` 单独限流 300 QPM
- **数据时效性**：当前版本的记忆片段与用户画像**无自动过期机制**，需业务侧自行管理生命周期。
- **内容长度**：
  - `custom_content` 最大 512 字符；`messages` 中单条 `content` 长度受整体 50 条限制约束，超长内容将被截断或拒绝。
- **ID 约束**：`user_id`、`memory_library_id`、`memory_node_id` 均为字符串，禁止含 `/`、`?`、`#` 等 URL 不安全字符。
- **错误处理**：所有接口返回标准 HTTP 状态码（如 429 表示限流，400 表示参数错误），响应体中 `request_id` 用于问题排查。

## 来源文档

- [长期记忆（新）API 参考](../../raw/application-api-reference/long-term-memory-new/long-term-memory-api-reference.md)



# long term memory new

[长期记忆](../concepts/long-term-memory.md)（新）是百炼平台提供的结构化用户记忆管理能力，支持自动从对话中提取关键信息生成记忆片段，并提供语义搜索、画像构建等能力。该功能基于专用记忆库实现，所有 API 均通过 `https://dashscope.aliyuncs.com/api/v2/apps/memory/` 统一接入。详细接口定义与行为规范请参见 [长期记忆API 参考](../../raw/application-api-reference/long-term-memory-new/long-term-memory-api-reference.md)。

## 支持的模型/功能

- **记忆片段管理**：支持 `AddMemory`（自动提取或自定义写入）、`SearchMemory`（语义检索）、`ListMemory`（分页查询）、`DeleteMemory`（按 ID 删除）、`UpdateMemory`（内容更新）。
- **用户画像支持**：通过 `CreateProfileSchema` 等接口定义画像模板，并在 `AddMemory` 中传入 `profile_schema` 参数触发画像自动构建与更新；支持 `GetUserProfile` 获取结构化画像。
- **多策略检索**：`SearchMemory` 支持 `plan_version=pro`（开启 Rerank，精度更高）和 `plan_version=lite`（关闭 Rerank，成本更低），二者计费不同，详见 [长期记忆API 参考](../../raw/application-api-reference/long-term-memory-new/long-term-memory-api-reference.md)。
- **SDK 封装**：官方 Python SDK（`agentscope-runtime>=1.1.5`）已封装全部接口，推荐用于生产环境集成，使用方式见 [长期记忆API 参考](../../raw/application-api-reference/long-term-memory-new/long-term-memory-api-reference.md)。

## 关键参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `user_id` | string | 是 | 记忆归属实体标识（≤64 字符），所有接口均需提供，用于隔离不同用户数据。 |
| `messages` / `custom_content` | array / string | 互斥 | `AddMemory` 中二选一：`messages` 支持最多 50 条对话记录（一问一答计为 2 条），由系统自动提取；`custom_content` 为纯文本输入（≤512 字符），绕过提取逻辑。 |
| `memory_library_id` | string | 否 | 指定记忆库 ID（≤32 字符），不传则使用默认记忆库。可在控制台 [记忆库列表页](https://bailian.console.aliyun.com/cn-beijing/?tab=app#/memory/list) 获取。 |
| `top_k`, `min_score`, `enable_rerank`, `plan_version` | integer/double/boolean/string | 否（SearchMemory） | 控制搜索召回数量（1–100）、相似度阈值（[0,1]）、是否启用重排序；`plan_version` 优先级高于 `enable_rerank`，且决定计费类型（Pro/Lite）。 |
| `profile_schema` | string | 否（AddMemory） | 画像模板 ID，传入后将在添加记忆时同步更新对应用户画像。 |

> **注意**：`plan_version` 参数在 `SearchMemory` 中为大小写不敏感字符串（如 `"PRO"`、`"lite"` 均有效），但原始文档中示例仅展示小写形式；实际调用建议统一使用小写以避免歧义。

## 使用方式

1. **认证**：所有请求需在 Header 中携带 `Authorization: Bearer $DASHSCOPE_API_KEY`，API Key 请从 [获取 API Key](https://help.aliyun.com/zh/model-studio/get-api-key) 获取。
2. **Base URL**：`https://dashscope.aliyuncs.com/api/v2/apps/memory/`
3. **Content-Type**：固定为 `application/json`
4. **SDK 调用（推荐）**：
   - 安装：`pip install agentscope-runtime>=1.1.5`
   - 示例（AddMemory）：
     ```python
     from agentscope_runtime.tools.modelstudio_memory import AddMemory, Message, AddMemoryInput
     result = await AddMemory().arun(AddMemoryInput(
         user_id="user_001",
         messages=[Message(role="user", content="每天9点提醒我吃药")],
         meta_data={"category": "健康"}
     ))
     ```
5. **cURL 调用（调试用）**：参考 [长期记忆API 参考](../../raw/application-api-reference/long-term-memory-new/long-term-memory-api-reference.md) 中各接口的完整示例。

## 限制和注意事项

- **限流**（阿里云账号级别）：
  - 所有接口总 QPM ≤ 3000；
  - `AddMemory` 单独限流 120 QPM；
  - `SearchMemory` 单独限流 300 QPM。
- **数据时效性**：当前生成的记忆片段与用户画像**无自动失效机制**，需业务侧自行管理生命周期。
- **商业化时间点**：记忆库将于 **2026 年 8 月 20 日 10:00（北京时间）起正式计费**，Add 和 Search 调用按 Pro/Lite 版本区分定价，详情见 [记忆库计费标准](https://help.aliyun.com/zh/model-studio/memory-library#h3-pricing)。
- **字段长度限制**：`user_id` ≤ 64 字符，`memory_library_id` ≤ 32 字符，`custom_content` ≤ 512 字符。
- **消息格式要求**：`messages` 中每条 `content` 支持 string 或 array（如含图片 base64），但 array 形式未在原始文档中给出具体 schema 示例，生产环境建议优先使用 string。

## 来源文档

- [长期记忆API 参考](../../raw/application-api-reference/long-term-memory-new/long-term-memory-api-reference.md)



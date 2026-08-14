# long term memory new

[长期记忆](../concepts/long-term-memory.md)（新）是百炼平台提供的结构化用户状态持久化能力，支持将对话历史自动提炼为语义化记忆片段，并提供增删改查、语义搜索及用户画像构建等核心功能。其底层基于向量检索与大模型理解能力，适用于需要长期维护用户上下文的智能体应用。所有 API 均通过 `https://dashscope.aliyuncs.com/api/v2/apps/memory/` 统一接入，认证方式为 Bearer [Token](../concepts/token.md)。

## 支持的模型/功能

- **记忆片段管理**：支持 `AddMemory`（自动提取关键信息）、`SearchMemory`（语义相似度检索）、`ListMemory`（分页查询）、`DeleteMemory` 和 `UpdateMemory`。
- **用户画像能力**：通过 `CreateProfileSchema` 等接口定义画像模板，并在 `AddMemory` 中传入 `profile_schema` ID 实现自动画像生成与更新；支持 `GetUserProfile` 获取结构化画像。
- **策略版本区分**：`SearchMemory` 支持 `pro`（启用 Rerank，精度更高）和 `lite`（关闭 Rerank，成本更低）两种计费策略，详见 [长期记忆API 参考](../../raw/application-api-reference/long-term-memory-new/long-term-memory-api-reference.md)。
- **多规则混合检索**：`SearchMemory` 支持通过 `project_ids` 参数指定多个记忆片段规则 ID 进行联合召回。

> **注意**：原始文档中 `AddMemory` 的 `messages` 字段说明存在歧义——示例代码显示最多支持 5 条用户-助手交替消息（即 5 轮对话），但文档正文写为“最多支持50条对话记录”。实际限制以 [长期记忆API 参考](../../raw/application-api-reference/long-term-memory-new/long-term-memory-api-reference.md) 中的 cURL 示例和 Python SDK 行为为准：单次 `AddMemory` 最多处理 **5 轮完整对话（10 条 message）**，超出部分将被截断或报错。

## 关键参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `user_id` | string | 是 | 记忆归属实体标识（≤64 字符），所有接口均需提供 |
| `memory_library_id` | string | 否 | 记忆库 ID（≤32 字符），未提供时使用默认库；可在控制台 [记忆库](https://bailian.console.aliyun.com/cn-beijing/?tab=app#/memory/list) 页面获取 |
| `profile_schema` | string | 否（仅 `AddMemory`） | 画像模板 ID，传入后触发自动画像提取；详情见 [长期记忆API 参考](../../raw/application-api-reference/long-term-memory-new/long-term-memory-api-reference.md) |
| `top_k` / `min_score` | integer / double | 否（仅 `SearchMemory`） | 检索结果数量上限（1–100，默认 10）和最小相似度阈值（[0,1]，默认 0.3） |
| `plan_version` | string | 否（仅 `SearchMemory`） | 检索策略版本：`pro`（默认，启用 Rerank）或 `lite`（关闭 Rerank）；优先级高于 `enable_rerank` |

## 使用方式

- **HTTP 直接调用**：  
  Base URL：`https://dashscope.aliyuncs.com/api/v2/apps/memory/`  
  Header：`Authorization: Bearer $DASHSCOPE_API_KEY` + `Content-Type: application/json`  
  示例见 [长期记忆API 参考](../../raw/application-api-reference/long-term-memory-new/long-term-memory-api-reference.md) 中的 cURL 片段。

- **Python SDK（推荐）**：  
  安装：`pip install agentscope-runtime>=1.1.5`  
  导入对应工具类（如 `AddMemory`, `SearchMemory`），构造 `Input` 对象并调用 `arun()` 方法。SDK 自动处理鉴权、重试与错误解析。

- **典型流程**：  
  1. 创建记忆库与画像模板（可选）→  
  2. 调用 `AddMemory` 写入对话或自定义内容 →  
  3. 在后续请求中调用 `SearchMemory` 获取相关记忆 →  
  4. 必要时用 `ListMemory`/`UpdateMemory`/`DeleteMemory` 进行维护。

## 限制和注意事项

- **限流**：全接口账号级总 QPM ≤ 3000；其中 `AddMemory` ≤ 120 QPM，`SearchMemory` ≤ 300 QPM。
- **内容长度**：`custom_content` ≤ 512 字符；`messages` 中单条 `content` 长度受模型上下文限制，建议 ≤ 2048 字符。
- **时效性**：记忆片段与用户画像无自动过期机制，需业务侧自行清理。
- **计费生效时间**：记忆库将于 **2026 年 8 月 20 日 10:00（北京时间）** 正式商业化计费，此前为免费试用期。
- **字段互斥**：`AddMemory` 中 `messages` 与 `custom_content` 互斥，若同时提供，以 `custom_content` 为准且忽略 `messages`。

## 来源文档

- [长期记忆API 参考](../../raw/application-api-reference/long-term-memory-new/long-term-memory-api-reference.md)



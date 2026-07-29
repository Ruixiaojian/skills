# long term memory new

[长期记忆](../concepts/long-term-memory.md)（新）是百炼平台提供的结构化用户记忆管理能力，支持自动从对话中提取关键信息、构建用户画像，并提供语义搜索、增删改查等完整生命周期操作。该功能基于专用记忆库和规则引擎实现，所有 API 均通过统一的 `https://dashscope.aliyuncs.com/api/v2/apps/memory/` 接口基地址访问。详细接口定义与行为规范请参见 [长期记忆（新）API 参考](../../raw/application-api-reference/long-term-memory-new/long-term-memory-api-reference.md)。

## 支持的模型/功能

- **核心能力**：记忆片段自动提取（基于对话或自定义文本）、语义搜索、分页列表、单条增删改、用户画像模板（Profile Schema）管理及画像获取。
- **不依赖大模型推理**：记忆提取与检索由后端专用服务完成，无需调用 `qwen-*` 等基础模型；但提取质量受底层 NLP 模型影响，具体模型未公开披露。
- **画像模板支持**：可通过 `CreateProfileSchema` 等接口定义结构化画像字段（如 `age`, `preference`），并在 `AddMemory` 时通过 `profile_schema` 参数关联，详见 [长期记忆（新）API 参考](../../raw/application-api-reference/long-term-memory-new/long-term-memory-api-reference.md) 中“核心组件”章节。

## 关键参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `user_id` | string | 是 | 记忆归属实体 ID（≤64 字符），用于隔离不同用户数据，是所有接口的必需标识。 |
| `messages` / `custom_content` | array / string | 互斥必填 | `AddMemory` 中二选一：`messages` 支持最多 50 条对话记录（一问一答计为 2 条）；`custom_content` 为纯文本（≤512 字符），优先级高于 `messages`。 |
| `memory_library_id` | string | 否 | 记忆库 ID（≤32 字符），未传时使用默认记忆库。需在控制台 [记忆库](https://bailian.console.aliyun.com/cn-beijing/?tab=app#/memory/list) 页面获取，该链接亦见于 [长期记忆（新）API 参考](../../raw/application-api-reference/long-term-memory-new/long-term-memory-api-reference.md)。 |
| `top_k` / `min_score` | integer / double | 否（SearchMemory） | `SearchMemory` 中控制召回数量（1–100，默认 10）和相似度阈值（[0,1]，默认 0.3）。 |

> **注意**：`project_id`（记忆片段规则 ID）在 `AddMemory`、`SearchMemory`、`ListMemory` 中均为可选参数，文档明确说明“如不传，会自动选择默认规则 ID”。但部分旧版 SDK 示例可能误将其设为必填，实际调用时可省略。

## 使用方式

### 1. 基础认证
所有请求需在 Header 中携带：
```http
Authorization: Bearer $DASHSCOPE_API_KEY
Content-Type: application/json
```
API Key 获取方式见 [获取 API Key](https://help.aliyun.com/zh/model-studio/get-api-key)。

### 2. 主要接口调用示例
- **添加记忆**：推荐使用 `messages` 字段传入对话历史，系统自动提取事件（如提醒、偏好）；若需精确控制内容，用 `custom_content`。
- **搜索记忆**：传入当前对话上下文（如 `[{role:"user", content:"明天有什么安排？"}]`），返回语义最相关记忆片段。
- **列表/删除/更新**：均需 `user_id` + `memory_node_id`（后者通过 `AddMemory` 或 `ListMemory` 返回获得）。

### 3. SDK 支持
- Python：推荐使用 `agentscope-runtime>=1.1.5` 提供的封装类（`AddMemory`, `SearchMemory`, `ListMemory`, `DeleteMemory`），详见 [长期记忆（新）API 参考](../../raw/application-api-reference/long-term-memory-new/long-term-memory-api-reference.md) 中各接口的 Python 示例。
- `UpdateMemory` 当前无 SDK 封装，需直接调用 REST API（PATCH 方法）。

## 限制和注意事项

- **限流策略**（阿里云账号级别）：
  - 所有接口总计 ≤ 3000 QPM；
  - `AddMemory` 单独限流 ≤ 120 QPM；
  - `SearchMemory` 单独限流 ≤ 300 QPM。
- **数据持久性**：生成的记忆片段与用户画像**暂无失效日期**，长期保留，需自行通过 `DeleteMemory` 清理。
- **内容长度**：`custom_content` 和 `messages[].content` 均受后端处理能力约束，超长文本可能被截断或提取失败，建议单次 `custom_content` ≤ 512 字符。
- **时间戳精度**：`UpdateMemory` 的 `timestamp` 参数为秒级 Unix 时间戳，非毫秒；若未提供，则使用请求发起时刻。

## 来源文档

- [长期记忆（新）API 参考](../../raw/application-api-reference/long-term-memory-new/long-term-memory-api-reference.md)



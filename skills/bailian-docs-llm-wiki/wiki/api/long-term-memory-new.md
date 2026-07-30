# long term memory new

[长期记忆](../concepts/long-term-memory.md)（新）是百炼平台提供的结构化用户记忆管理能力，支持自动从对话中提取关键信息生成记忆片段，并提供语义搜索、增删改查等完整生命周期管理。该能力基于专用模型实现意图理解与信息抽取，适用于构建具备上下文感知能力的智能体应用。详细接口定义和行为规范请参见 [长期记忆（新）API 参考](../../raw/application-api-reference/long-term-memory-new/long-term-memory-api-reference.md)。

## 支持的模型/功能

- **核心能力**：自动从 `messages` 对话流中提取结构化记忆（如提醒、偏好、事件），或接受 `custom_content` 直接注入文本；
- **画像联动**：支持通过 `profile_schema_id` 关联画像模板，将记忆片段映射至用户画像字段；
- **[多模态](../concepts/multi-modal.md)适配**：`messages.content` 支持 string 或 array 类型（如含 image_url 的[多模态](../concepts/multi-modal.md)消息），但当前仅对文本内容进行语义解析；
- **检索增强**：`SearchMemory` 支持 `enable_rerank`、`enable_judge`、`enable_rewrite` 等高级搜索开关，需在请求中显式启用；
- 所有功能均依赖百炼平台统一认证体系，无需额外模型部署。具体能力边界详见 [长期记忆（新）API 参考](../../raw/application-api-reference/long-term-memory-new/long-term-memory-api-reference.md)。

## 关键参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `user_id` | string | 是 | 记忆归属实体 ID（≤64 字符），用于隔离不同用户数据 |
| `messages` / `custom_content` | array / string | 互斥必填 | `messages` 最多 50 条（一问一答计为 2 条）；`custom_content` ≤512 字符 |
| `memory_library_id` | string | 否 | 显式指定记忆库 ID（≤32 字符），不传则使用默认库；[获取方式见控制台](https://bailian.console.aliyun.com/cn-beijing/?tab=app#/memory/list) |
| `profile_schema_id` | string | 否 | 画像模板 ID，用于约束记忆片段结构化输出格式 |
| `top_k`（SearchMemory） | integer | 否 | 检索召回数（1–100，默认 10） |
| `min_score`（SearchMemory） | double | 否 | 相似度阈值 [0,1]（默认 0.3） |

> **注意**：`project_id` 参数在文档中描述为“记忆片段规则 ID”，但实际调用中若未传入，系统会自动选择默认规则；该行为与 [长期记忆（新）API 参考](../../raw/application-api-reference/long-term-memory-new/long-term-memory-api-reference.md) 中“说明”字段一致，无需手动指定。

## 使用方式

### 基础调用
- **Base URL**：`https://dashscope.aliyuncs.com/api/v2/apps/memory/`
- **认证**：Header 中携带 `Authorization: Bearer $DASHSCOPE_API_KEY`
- **Content-Type**：`application/json`

### SDK 快速接入
- Python 推荐使用 `agentscope-runtime>=1.1.5`：
  - `AddMemory`, `SearchMemory`, `ListMemory` 已封装为异步工具类；
  - `DeleteMemory` 和 `UpdateMemory` 也提供封装，但 `UpdateMemory` 的 Python 示例中明确提示“SDK 暂未提供封装”，需用 `requests` 直接调用 —— 此处存在文档内不一致，**以 [长期记忆（新）API 参考](../../raw/application-api-reference/long-term-memory-new/long-term-memory-api-reference.md) 中 Python 示例为准**。

### 典型流程示例
```python
# 添加记忆（自动抽取）
await AddMemory().arun(AddMemoryInput(
    user_id="user_001",
    messages=[Message(role="user", content="明天9点开会"), Message(role="assistant", content="已记录")],
    meta_data={"source": "chat"}
))

# 搜索相关记忆
await SearchMemory().arun(SearchMemoryInput(
    user_id="user_001",
    messages=[Message(role="user", content="我之前有什么待办？")],
    top_k=5,
    min_score=0.5
))
```

## 限制和注意事项

- **限流策略**（阿里云账号级别）：
  - 全部接口总计 ≤3000 QPM；
  - `AddMemory` 单独限流 ≤120 QPM；
  - `SearchMemory` 单独限流 ≤300 QPM；
- **数据持久性**：记忆片段与用户画像无自动过期机制，需业务侧自行管理生命周期；
- **内容长度**：`custom_content` 和单条 `messages.content` 均受 512 字符限制，超长内容将被截断；
- **时间戳精度**：`UpdateMemory` 的 `timestamp` 为秒级 Unix 时间戳，毫秒级输入会被向下取整；
- **错误处理**：所有接口返回 `request_id`，用于问题排查；失败时 HTTP 状态码非 2xx，响应体含 `code` 与 `message` 字段。

> **注意**：文档中 `DeleteMemory` 的 cURL 示例路径含 `{memory_node_id}` 占位符，但未说明需替换为真实 ID；实际调用时必须替换，否则返回 404。该细节在 [长期记忆（新）API 参考](../../raw/application-api-reference/long-term-memory-new/long-term-memory-api-reference.md) 的“路径参数”小节有明确定义，开发者需严格遵循。

## 来源文档

- [长期记忆（新）API 参考](../../raw/application-api-reference/long-term-memory-new/long-term-memory-api-reference.md)




# long term memory new

[长期记忆](../concepts/long-term-memory.md)（新）是百炼平台提供的结构化用户记忆管理能力，支持自动从对话中提取关键信息、构建用户画像，并提供语义搜索、增删改查等完整生命周期操作。该能力基于专用记忆模型实现，与传统向量库方案不同，强调语义理解与上下文感知。所有接口均通过统一的 REST API 提供，同时支持 `agentscope-runtime` SDK 封装调用。

## 支持的模型/功能

- **底层模型**：由百炼平台专属记忆模型驱动，非通用大模型或外部向量模型；不开放模型选择，无需指定 model 参数。
- **核心功能**：
  - `AddMemory`：自动解析对话（最多 50 条消息）或接收自定义文本，生成结构化记忆片段；
  - `SearchMemory`：基于语义相似度检索，支持 `top_k`、`min_score`、`enable_rerank` 等精细控制；
  - `ListMemory`：分页列出指定用户的全部记忆片段；
  - `DeleteMemory` / `UpdateMemory`：按 `memory_node_id` 精确操作单条记忆；
  - `ProfileSchema` 系列接口：管理用户画像模板（创建、查询、更新、删除），用于约束记忆提取逻辑；
  - `GetUserProfile`：获取某用户在指定画像模板下的聚合画像结果。

> **注意**：原始文档中未明确说明是否支持[多模态](../concepts/multimodal.md)输入（如图像、音频），当前所有接口仅接受文本型 `content` 字段（含 `messages[].content` 和 `custom_content`），详见 [长期记忆（新）API 参考](../../raw/application-api-reference/long-term-memory-new/long-term-memory-api-reference.md)。

## 关键参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `user_id` | string | 是 | 记忆归属实体 ID（≤64 字符），所有接口均需提供，用于隔离不同用户数据 |
| `messages` 或 `custom_content` | array / string | 二选一 | `AddMemory` 中互斥：前者传对话历史（role/content），后者传纯文本（≤512 字符） |
| `memory_library_id` | string | 否 | 指定记忆库 ID（≤32 字符）；不传则使用默认记忆库，见 [长期记忆（新）API 参考](../../raw/application-api-reference/long-term-memory-new/long-term-memory-api-reference.md) |
| `project_id` | string | 否 | 记忆片段规则 ID；不传则使用对应记忆库的默认规则 |
| `top_k`（SearchMemory） | integer | 否 | 最大召回数，范围 1–100，默认 10 |
| `min_score`（SearchMemory） | double | 否 | 相似度阈值 [0,1]，默认 0.3 |
| `page_num` / `page_size`（ListMemory） | integer | 否 | 分页参数，默认 page_num=1, page_size=10 |

## 使用方式

1. **认证**：所有请求需在 Header 中携带 `Authorization: Bearer $DASHSCOPE_API_KEY`，API Key 获取方式见 [获取 API Key](https://help.aliyun.com/zh/model-studio/get-api-key)。
2. **Base URL**：`https://dashscope.aliyuncs.com/api/v2/apps/memory/`
3. **SDK 调用（推荐）**：
   - 安装依赖：`pip install agentscope-runtime>=1.1.5`
   - 使用 `AddMemory`、`SearchMemory`、`ListMemory` 等封装类（示例见 [长期记忆（新）API 参考](../../raw/application-api-reference/long-term-memory-new/long-term-memory-api-reference.md)）。
4. **直接 HTTP 调用**：参考各接口的 cURL 示例，注意 `Content-Type: application/json`。

## 限制和注意事项

- **限流策略（阿里云账号级）**：
  - 所有接口总和 ≤ 3000 QPM；
  - `AddMemory` 单独限流 120 QPM；
  - `SearchMemory` 单独限流 300 QPM。
- **数据时效性**：生成的记忆片段与用户画像**暂无自动过期机制**，需业务侧自行管理生命周期。
- **内容长度**：
  - `custom_content` ≤ 512 字符；
  - `messages` 最多 50 条（一问一答计为 2 条）；
  - `meta_data` 为 JSON object，无明确大小限制，但建议保持轻量。
- **更新行为**：`UpdateMemory` 仅更新 `custom_content` 和 `meta_data`（增量合并），不支持修改 `messages` 或 `user_id`。
- > **注意**：`UpdateMemory` 的 Python SDK 尚未封装，需用 `requests` 直接调用 PATCH 接口，此与 `AddMemory`/`SearchMemory` 的 SDK 支持不一致，详见 [长期记忆（新）API 参考](../../raw/application-api-reference/long-term-memory-new/long-term-memory-api-reference.md)。

## 来源文档

- [长期记忆（新）API 参考](../../raw/application-api-reference/long-term-memory-new/long-term-memory-api-reference.md)



# toolkits and [frameworks](frameworks.md)

阿里云百炼提供多种 [OpenAI 兼容接口](../concepts/openai-compatible-interface.md)及配套工具链，支持开发者快速迁移现有应用或构建新场景。所有接口均基于统一的 `compatible-mode/v1` 协议层，通过调整 `base_url`、`api_key` 和 `model` 即可接入，无需重写业务逻辑。核心能力覆盖文本生成、多模态理解、向量嵌入、批量处理、对话状态管理及文件操作等全栈需求。

## 支持的模型/功能

百炼支持的 OpenAI 兼容能力按协议类型划分，各接口支持的模型存在明确边界：

- **Chat Completions 接口**（[OpenAI Chat接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-of-openai-with-dashscope.md)）：支持 Qwen 系列（`qwen-plus`, `qwen-flash`, `qwen3-*`）、Qwen-VL、Qwen-Coder、Qwen-Omni、Qwen-Math，以及第三方直供模型（DeepSeek、Kimi、GLM、MiniMax）。**注意**：Qwen-Audio 明确不支持该协议，仅支持 DashScope 原生协议。
- **Responses API**（[OpenAI Responses接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-with-openai-responses-api.md)）：专为智能体设计，支持 `qwen3-*` 全系列（如 `qwen3.7-plus`, `qwen3.7-flash`, `qwen3-coder-plus` 等），并内置联网搜索、网页抓取等工具能力；但**不支持 Qwen-VL 或 Qwen-OCR**。
- **Completions 接口**（[completions 接口](../../raw/model-api-reference/toolkits-and-frameworks/completions.md)）：当前**仅支持 `qwen-coder-turbo`**，用于代码补全与续写，不支持其他模型。
- **Vision 接口**（[OpenAI Vision接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/qwen-vl-compatible-with-openai.md)）：支持 `Qwen-VL`, `QVQ`, `Qwen-OCR`，其中 QVQ 仅支持[流式输出](../concepts/streaming-output.md)。
- **Embedding 接口**（[OpenAI Embedding接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/embedding-interfaces-compatible-with-openai.md)）：支持 `text-embedding-v1` 至 `v4` 全系列，**不支持多模态 Embedding 模型**（如 `qwen3-vl-embedding`）。
- **File 接口**（[OpenAI文件接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/openai-file-interface.md)）：支持 `purpose="file-extract"`（用于 Qwen-Long/Qwen-Doc-Turbo）、`"batch"`（用于批量推理）、`"fine-tune"`（用于调优任务）三类用途。
- **Batch 接口**：分为两种形态：
  - 文件批量（[OpenAI兼容-Batch（文件输入）](../../raw/model-api-reference/toolkits-and-frameworks/batch-interfaces-compatible-with-openai.md)）：支持文本、多模态、向量模型，单次请求上下文最大 256K tokens；
  - 同步 Batch Chat（[OpenAI兼容-Batch Chat](../../raw/model-api-reference/toolkits-and-frameworks/openai-compatible-batch-chat.md)）：仅支持单请求，需切换 `base_url` 至 `https://batch.dashscope.aliyuncs.com`。

> **注意**：文档 6 与文档 7 均提及 `qwen3.7-max` 等模型在 Batch 场景下支持 256K 上下文，但文档 6 明确列出其为“华北2（北京）”支持模型，而文档 7 未限定地域；实际使用时应以控制台可用模型列表为准，避免跨地域调用失败。

## 关键参数

所有 [OpenAI 兼容接口](../concepts/openai-compatible-interface.md)共用以下核心参数，行为一致：

- `base_url`：必须配置为业务空间专属域名（如 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`），旧域名（`dashscope.aliyuncs.com`）虽仍可用，但性能与稳定性较低，[官方强烈建议迁移](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-of-openai-with-dashscope.md)。
- `api_key`：需使用对应地域的 API Key（北京、新加坡、弗吉尼亚等 Key 不互通），推荐配置至环境变量 `DASHSCOPE_API_KEY`。
- `model`：必须为文档中明确列出的支持型号，拼写错误或使用非兼容型号将返回 404。
- `stream`：布尔值，控制是否[流式输出](../concepts/streaming-output.md)；`stream_options={"include_usage": true}` 可在流式末尾返回 token 统计。
- `temperature` / `top_p`：二者互斥，建议仅设置其一以控制输出多样性。
- `max_tokens`：仅作截断控制，不影响模型内部生成长度。

特定接口扩展参数：
- `completions`：使用 `prompt` 字符串，支持 `<tool_call>{prefix}<tool_call>{suffix}<tool_call>` 语法进行中段补全。
- `Responses API`：使用 `input`（字符串或消息数组）和 `previous_response_id`（自动管理上下文）。
- `Conversations API`（[OpenAI Conversations接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/openai-compatible-conversations.md)）：通过 `conversation_id` 和 `items` 实现会话持久化，支持跨设备上下文同步。
- `Embedding`：`dimensions` 参数仅对 `v3`/`v4` 有效；`encoding_format` 可选 `"float"` 或 `"base64"`。
- `Batch`：`completion_window`（如 `"24h"`）定义最长等待时间；`enable_thinking` 需作为顶层参数与 `model` 同级传入。

## 使用方式

### SDK 调用（推荐）
1. 安装最新版 `openai` SDK（`pip install -U openai`）；
2. 初始化客户端时指定 `base_url` 和 `api_key`；
3. 根据接口选择对应方法：
   - Chat：`client.chat.completions.create(...)`
   - Responses：`client.responses.create(...)`
   - Completions：`client.completions.create(...)`
   - Embeddings：`client.embeddings.create(...)`
   - Files：`client.files.create(...)` / `client.files.retrieve(...)`
   - Batches：`client.batches.create(...)`（文件批量）或切换 `base_url` 后调用 `chat.completions.create(...)`（同步 Batch Chat）
   - Conversations：`client.conversations.create(...)` / `client.conversations.retrieve(...)`

### LangChain 集成
- **`langchain_openai`**：仅支持 [OpenAI 兼容接口](../concepts/openai-compatible-interface.md)的模型（如 `qwen-plus`），需配置 `base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"`；
- **`langchain_community.chat_models.tongyi`**（Python）或 **`@langchain/community/chat_models/alibaba_tongyi`**（JS）：支持百炼全部模型（含非兼容型号），使用原生 DashScope 协议，需安装 `dashscope` 或 `@langchain/community`。

### HTTP 直连
- 所有 endpoint 均为 `POST https://{base_url}/{endpoint}`，如：
  - Chat：`/chat/completions`
  - Responses：`/responses`
  - Embeddings：`/embeddings`
  - Files：`/files`
- 请求头需包含 `Authorization: Bearer ${DASHSCOPE_API_KEY}` 和 `Content-Type: application/json`；
- 请求体结构严格遵循 OpenAI 官方 schema，详见各文档示例。

## 限制和注意事项

- **地域隔离**：API Key、`base_url`、支持模型均按地域隔离。北京地域 Key 无法用于新加坡 endpoint，反之亦然；跨地域调用将返回鉴权失败。
- **域名迁移强制性**：华北2（北京）和新加坡地域的旧域名（`dashscope.aliyuncs.com`/`dashscope-intl.aliyuncs.com`）已标记为“建议迁移”，[Responses API 文档](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-with-openai-responses-api.md) 更明确指出其旧路径 `/api/v2/apps/...` “即将停止维护”，务必更新。
- **Qwen-Audio 与多模态 Embedding 不兼容**：前者仅支持 DashScope 原生协议；后者（如 `qwen3-vl-embedding`）需使用专用多模态向量接口，不可混用 OpenAI Embedding endpoint。
- **Batch 超时控制**：同步 Batch Chat 默认超时 3600 秒，需在客户端显式设置（如 Python 的 `.with_options(timeout=1800.0)`）；文件批量任务无客户端超时，但 `completion_window` 必须 ≤ 24 小时。
- **Conversations API 无消息存储**：`Delete conversation` 仅删除会话元数据，`items`（消息历史）仍保留在服务端，需单独清理。
- **文件配额**：总文件数 ≤ 10000，总大小 ≤ 100 GB；单个 `file-extract` 文件 ≤ 150 MB，`batch` 文件 ≤ 500 MB，`fine-tune` 文件 ≤ 300 MB。

## 来源文档

- [OpenAI Chat接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-of-openai-with-dashscope.md)
- [OpenAI Responses接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-with-openai-responses-api.md)
- [completions 接口](../../raw/model-api-reference/toolkits-and-frameworks/completions.md)
- [OpenAI Vision接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/qwen-vl-compatible-with-openai.md)
- [OpenAI文件接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/openai-file-interface.md)
- [OpenAI兼容-Batch（文件输入）](../../raw/model-api-reference/toolkits-and-frameworks/batch-interfaces-compatible-with-openai.md)
- [OpenAI兼容-Batch Chat](../../raw/model-api-reference/toolkits-and-frameworks/openai-compatible-batch-chat.md)
- [OpenAI Conversations接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/openai-compatible-conversations.md)
- [OpenAI Embedding接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/embedding-interfaces-compatible-with-openai.md)
- [在LangChain中使用阿里云百炼](../../raw/model-api-reference/toolkits-and-frameworks/use-bailian-in-langchain.md)



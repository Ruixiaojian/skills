# toolkits and [frameworks](frameworks.md)

阿里云百炼提供多套 OpenAI 兼容的工具包与框架接口，覆盖文本生成、视觉理解、向量嵌入、批量推理、文件处理及会话管理等核心场景。开发者可复用现有 OpenAI SDK 代码，仅需调整 `base_url`、`api_key` 和模型名即可快速迁移。所有接口均支持主流编程语言（Python/Node.js/Java/Go/C#/HTTP），并提供业务空间专属域名以提升稳定性与性能。

## 支持的模型/功能

- **文本生成**：`qwen3.8-max`、`qwen3.7-plus`、`qwen-plus`、`qwen-flash` 等全系列 Qwen 模型，以及 DeepSeek（v4）、GLM（5.2）等第三方模型（[原文标题](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-with-openai-responses-api.md)）；  
- **视觉理解**：`qwen3-vl-plus`、`qwen3-vl-flash`、`qwen-vl-ocr`，支持图像+文本[多模态](../concepts/multi-modal.md)输入（[原文标题](../../raw/model-api-reference/toolkits-and-frameworks/qwen-vl-compatible-with-openai.md)）；  
- **向量嵌入**：`text-embedding-v4`（2048维）、`text-embedding-v3`、`text-embedding-v2`，支持100+语种及编程语言（[原文标题](../../raw/model-api-reference/toolkits-and-frameworks/embedding-interfaces-compatible-with-openai.md)）；  
- **代码补全**：`qwen-coder-turbo`（仅通过 `completions` 接口调用）；  
- **长文档与文件分析**：`qwen-long`、`qwen-doc-turbo`，依赖文件上传后通过 `file_id` 调用；  
- **批量处理**：支持单请求同步 Batch Chat（`/chat/completions`）与多请求异步 Batch File（`/files` + `/batches`），成本降低 50%；  
- **会话管理**：`conversations` API 提供跨设备上下文持久化能力，配合 `responses` API 实现自动历史注入。

> **注意**：文档 1 与文档 2 对 `qwen-coder-turbo` 的支持范围存在矛盾——文档 1 明确列出其为 Responses API 支持模型，但文档 3 明确指出该模型**仅支持 `completions` 接口**，且文档 2 的模型列表未包含 `qwen-coder-turbo`。实际应以文档 3 为准：`qwen-coder-turbo` 不支持 `chat/completions` 或 `responses`，仅限 `completions`。

## 关键参数

| 参数 | 类型 | 说明 | 备注 |
|------|------|------|------|
| `base_url` | string | 必填。地域专属端点，格式为 `https://{WorkspaceId}.{region}.maas.aliyuncs.com/compatible-mode/v1` | 华北2（北京）、新加坡必须使用业务空间专属域名；弗吉尼亚、东京、法兰克福、美国等地域部分仍沿用 `dashscope-us.aliyuncs.com`（见 [原文标题](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-of-openai-with-dashscope.md)） |
| `model` | string | 必填。模型名称需严格匹配文档所列支持列表 | `qwen-audio` 不支持任何 [OpenAI 兼容接口](../concepts/openai-compatible-api.md)（见 [原文标题](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-of-openai-with-dashscope.md)） |
| `previous_response_id` | string | Responses API 特有。用于多轮对话上下文关联 | 必须传入上一轮响应的顶层 `id`（UUID 格式），非 `output` 数组内消息的 `id`（见 [原文标题](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-with-openai-responses-api.md)） |
| `purpose` | string | 文件接口特有。取值 `file-extract`（文档分析）、`batch`（批量任务）、`fine-tune`（调优数据集） | `file-extract` 支持 TXT/DOCX/PDF 等 10+ 格式，单文件 ≤150 MB（见 [原文标题](../../raw/model-api-reference/toolkits-and-frameworks/openai-file-interface.md)） |
| `enable_thinking` | boolean | Batch 场景下控制思考模式开关 | `qwen3.5+` 系列默认开启，显式设为 `false` 可避免额外 reasoning token 成本（见 [原文标题](../../raw/model-api-reference/toolkits-and-frameworks/batch-interfaces-compatible-with-openai.md)） |

## 使用方式

1. **初始化客户端**：配置 `api_key`（推荐环境变量 `DASHSCOPE_API_KEY`）与 `base_url`；  
2. **选择接口路径**：
   - 文本对话 → `client.chat.completions.create()`（Chat Completions）或 `client.responses.create()`（Responses）；
   - 视觉理解 → `client.chat.completions.create()` + `messages.content` 含 `image_url`；
   - 向量嵌入 → `client.embeddings.create()`；
   - 批量同步 → `base_url` 指向 `https://batch.dashscope.aliyuncs.com/compatible-mode/v1`；
   - 批量异步 → 先 `client.files.create(purpose="batch")`，再 `client.batches.create()`；
   - 文件分析 → `client.files.create(purpose="file-extract")`，后续在 `messages` 中引用 `file_id`；
   - 会话管理 → `client.conversations.create()` 创建会话，`client.responses.create(previous_response_id=...)` 自动注入上下文；
3. **[流式输出](../concepts/streaming-output.md)**：设置 `stream=True` 并遍历 `chunk`，如需末尾 [Token](../concepts/token.md) 统计，添加 `stream_options={"include_usage": True}`；  
4. **LangChain 集成**：优先选用 `langchain_openai.ChatOpenAI`（兼容性好）或 `langchain_community.chat_models.tongyi.ChatTongyi`（支持全部百炼模型）（见 [原文标题](../../raw/model-api-reference/toolkits-and-frameworks/use-bailian-in-langchain.md)）。

## 限制和注意事项

- **地域限制**：DeepSeek v4、GLM 5.2 仅支持华北2（北京）与新加坡；Qwen-VL 系列在各地域支持模型不同，需查控制台确认；  
- **文件配额**：总文件数 ≤10,000 个，总大小 ≤100 GB，无自动过期机制；  
- **Batch 限制**：单次 Batch 请求最大上下文为 256K tokens（`qwen3.5+` 系列），`qwen3.5-omni-plus` 不支持语音输出；  
- **URL 迁移强制要求**：`/api/v2/apps/protocols/compatible-mode/v1/responses` 和 `/api/v2/apps/protocols/compatible-mode/v1/conversations` 已废弃，必须迁移到 `/compatible-mode/v1/{endpoint}`（见 [原文标题](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-with-openai-responses-api.md) 和 [原文标题](../../raw/model-api-reference/toolkits-and-frameworks/openai-compatible-conversations.md)）；  
- **超时设置**：Batch Chat 默认等待 3600 秒，需在 SDK 客户端显式配置 `timeout`（如 Python 的 `.with_options(timeout=1800.0)`），HTTP 调用需设置连接级超时；  
- **安全提示**：切勿硬编码 `api_key` 到源码，生产环境务必使用环境变量或密钥管理服务。

## 来源文档

- [OpenAI Responses接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-with-openai-responses-api.md)
- [OpenAI Chat接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-of-openai-with-dashscope.md)
- [completions 接口](../../raw/model-api-reference/toolkits-and-frameworks/completions.md)
- [OpenAI Vision接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/qwen-vl-compatible-with-openai.md)
- [OpenAI文件接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/openai-file-interface.md)
- [OpenAI兼容-Batch（文件输入）](../../raw/model-api-reference/toolkits-and-frameworks/batch-interfaces-compatible-with-openai.md)
- [OpenAI兼容-Batch Chat](../../raw/model-api-reference/toolkits-and-frameworks/openai-compatible-batch-chat.md)
- [OpenAI Embedding接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/embedding-interfaces-compatible-with-openai.md)
- [OpenAI Conversations接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/openai-compatible-conversations.md)
- [在LangChain中使用阿里云百炼](../../raw/model-api-reference/toolkits-and-frameworks/use-bailian-in-langchain.md)



# toolkits and [frameworks](frameworks.md)

阿里云百炼平台提供多种 [OpenAI 兼容接口](../concepts/openai-compatible-interface.md)及配套工具链，支持开发者快速迁移现有应用或构建新模型服务。核心能力覆盖文本生成、多模态理解、向量嵌入、批量推理、[文件处理](../concepts/file-processing.md)与对话状态管理等场景，所有接口均通过统一的 `compatible-mode/v1` 路径提供标准化访问。

## 支持的模型/功能

百炼支持的 OpenAI 兼容能力按协议类型划分，各接口支持的模型存在明确差异：

- **Chat Completions 接口**（[OpenAI Chat接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-of-openai-with-dashscope.md)）：支持 Qwen 系列（`qwen-plus`, `qwen-flash`, `qwen3-*`）、Qwen-VL、Qwen-Coder、Qwen-Omni、Qwen-Math，以及第三方直供模型（DeepSeek、Kimi、GLM、MiniMax），但 **Qwen-Audio 不支持该协议**。
  
- **Responses API**（[OpenAI Responses接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-with-openai-responses-api.md)）：专为智能体原生交互设计，支持 `qwen3.8-max`、`qwen3.7-plus`、`qwen3-coder-*`、`deepseek-v4-flash` 等最新模型，并内置联网搜索、网页抓取、代码解释器等工具能力。

- **Vision 接口**（[OpenAI Vision接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/qwen-vl-compatible-with-openai.md)）：仅支持视觉模型 `Qwen-VL`、`QVQ`、`Qwen-OCR`；其中 `QVQ` **仅支持[流式输出](../concepts/streaming-output.md)**。

- **Embedding 接口**（[OpenAI Embedding接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/embedding-interfaces-compatible-with-openai.md)）：支持 `text-embedding-v1` 至 `v4` 全系列，但 **多模态 Embedding 模型（如 `qwen3-vl-embedding`）不支持 [OpenAI 兼容接口](../concepts/openai-compatible-interface.md)**。

- **Batch 接口**（[OpenAI兼容-Batch（文件输入）](../../raw/model-api-reference/toolkits-and-frameworks/batch-interfaces-compatible-with-openai.md)）：支持文本生成、多模态理解及文本向量模型，但 `qwen3.5-omni-plus` **不支持语音输出**，且部分模型（如 `qwen3.8-max`）在 Batch 场景下单次上下文最大支持 256K tokens。

- **Conversations API**（[OpenAI Conversations接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/openai-compatible-conversations.md)）：用于跨设备/长时间会话的状态持久化，需配合 Responses API 使用，不直接参与模型推理。

> **注意**：文档 1 和文档 2 均强调应迁移到业务空间专属域名（如 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com`），但文档 6 的 Batch 接口示例仍使用旧域名 `https://dashscope.aliyuncs.com/compatible-mode/v1`，而文档 7 的 Batch Chat 明确要求使用 `https://batch.dashscope.aliyuncs.com/compatible-mode/v1` —— 这表明不同 Batch 子接口的 endpoint 并不统一，开发者需严格按接口类型选用对应 base_url。

## 关键参数

| 参数 | 类型 | 必选 | 说明 | 来源参考 |
|------|------|------|------|----------|
| `base_url` | string | 是 | 接口服务地址，地域与接口类型决定具体值（如 Chat 用 `.../compatible-mode/v1`，Batch Chat 用 `batch.dashscope.aliyuncs.com/...`） | [OpenAI Chat接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-of-openai-with-dashscope.md) |
| `model` | string | 是 | 模型名称，必须与所选接口支持的模型列表严格匹配（例如 `qwen-vl-plus` 仅可用于 Vision 接口） | [OpenAI Vision接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/qwen-vl-compatible-with-openai.md) |
| `stream` / `stream_options` | boolean / object | 否 | 控制[流式输出](../concepts/streaming-output.md)，`stream_options={"include_usage": true}` 可在末尾返回 token 统计 | [completions 接口](../../raw/model-api-reference/toolkits-and-frameworks/completions.md) |
| `previous_response_id` | string | 否（Responses API） | 用于多轮对话上下文关联，须传入上一轮响应的顶层 `id`（UUID 格式），非 `output` 中消息的 `id` | [OpenAI Responses接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-with-openai-responses-api.md) |
| `purpose` | string | 是（Files API） | 文件用途标识：`file-extract`（文档分析）、`batch`（批量任务）、`fine-tune`（调优数据集） | [OpenAI文件接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/openai-file-interface.md) |
| `enable_thinking` | boolean | 否（Batch 场景） | 控制思考模式开关，影响 token 成本；必须作为 JSONL 请求体顶层字段，不可置于 `extra_body` 内 | [OpenAI兼容-Batch（文件输入）](../../raw/model-api-reference/toolkits-and-frameworks/batch-interfaces-compatible-with-openai.md) |

## 使用方式

- **SDK 调用**：推荐使用 `openai` 官方 SDK（Python/Node.js/Java/Go/C#）或 LangChain 封装（`langchain_openai`, `langchain-community`）。LangChain 提供两种集成路径：`ChatOpenAI`（仅支持部分模型，见 [OpenAI Chat接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-of-openai-with-dashscope.md) 文档）和 `ChatTongyi`（支持全部百炼文本模型）。
  
- **HTTP 直连**：所有接口均提供标准 RESTful endpoint，需设置 `Authorization: Bearer $DASHSCOPE_API_KEY` 和 `Content-Type: application/json`。注意 Vision 接口需构造含 `image_url` 的结构化 `content` 数组，Files API 需使用 `multipart/form-data` 提交文件。

- **地域与 WorkspaceId**：北京、新加坡地域必须使用业务空间专属域名并填入真实 `{WorkspaceId}`；弗吉尼亚、东京、法兰克福等地域则使用固定域名（如 `dashscope-us.aliyuncs.com`），无需 WorkspaceId。

- **[文件处理](../concepts/file-processing.md)流程**：先调用 `/files` 上传（指定 `purpose`），获取 `file_id` 后，再用于 Qwen-Long/Qwen-Doc-Turbo 推理、Batch 任务或 Fine-tuning。

## 限制和注意事项

- **域名迁移强制性**：华北2（北京）和新加坡地域的旧域名（`dashscope.aliyuncs.com` / `dashscope-intl.aliyuncs.com`）虽仍可用，但官方明确建议迁移至业务空间专属域名以获得“卓越性能和更高稳定性”；Responses API 的旧路径 `/api/v2/apps/protocols/compatible-mode/v1/responses` 已标记为“即将停止维护”，必须迁移到 `/compatible-mode/v1/responses`。

- **模型能力边界**：
  - `Qwen-Audio` 不支持 OpenAI 兼容协议，仅支持 DashScope 原生协议；
  - `QVQ` 模型强制[流式输出](../concepts/streaming-output.md)，非流式调用将失败；
  - `completions` 接口仅支持前缀补全或前后缀中间补全，**暂不支持后缀补全前缀**；
  - `qwen3.5-omni-plus` 在 Batch 场景下不支持语音输出。

- **配额与容量**：Files API 总存储上限为 100 GB / 10,000 个文件；单个 `file-extract` 文件最大 150 MB，`batch` 文件最大 500 MB，`fine-tune` 文件最大 300 MB。

- **超时与重试**：Batch Chat 默认等待超时 3600 秒（1 小时），需在客户端显式配置 timeout（如 Python SDK 的 `with_options(timeout=...)`）；Batch File API 为异步任务，需轮询 `batches.retrieve()` 获取状态，避免短时高频查询。

- **安全实践**：强烈建议将 `DASHSCOPE_API_KEY` 配置为环境变量，而非硬编码于源码中；若必须代码内配置，需确保其不被提交至公开仓库。

## 来源文档

- [OpenAI Chat接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-of-openai-with-dashscope.md)
- [OpenAI Responses接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-with-openai-responses-api.md)
- [completions 接口](../../raw/model-api-reference/toolkits-and-frameworks/completions.md)
- [OpenAI Vision接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/qwen-vl-compatible-with-openai.md)
- [OpenAI文件接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/openai-file-interface.md)
- [OpenAI兼容-Batch（文件输入）](../../raw/model-api-reference/toolkits-and-frameworks/batch-interfaces-compatible-with-openai.md)
- [OpenAI兼容-Batch Chat](../../raw/model-api-reference/toolkits-and-frameworks/openai-compatible-batch-chat.md)
- [OpenAI Embedding接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/embedding-interfaces-compatible-with-openai.md)
- [OpenAI Conversations接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/openai-compatible-conversations.md)
- [在LangChain中使用阿里云百炼](../../raw/model-api-reference/toolkits-and-frameworks/use-bailian-in-langchain.md)



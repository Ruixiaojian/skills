# toolkits and [frameworks](frameworks.md)

阿里云百炼提供多套 OpenAI 兼容的 API 接口与框架集成方案，覆盖文本生成、视觉理解、嵌入向量、文件处理、批量推理及会话管理等核心场景。开发者可复用现有 OpenAI SDK 代码，仅需调整 `base_url`、`api_key` 和 `model` 参数即可快速迁移。所有接口均支持主流编程语言（Python/Node.js/Java/Go/C#/HTTP），并提供业务空间专属域名以提升性能与稳定性。

## 支持的模型/功能

百炼支持的 OpenAI 兼容能力按功能维度划分如下：

- **文本生成**：  
  - `responses` 接口（[OpenAI Responses接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-with-openai-responses-api.md)）支持 `qwen3.7-plus`、`qwen3.5-flash` 等数十个 Qwen 系列模型，并内置联网搜索、网页抓取、代码解释器等工具；  
  - `chat/completions` 接口（[OpenAI Chat接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-of-openai-with-dashscope.md)）支持 Qwen、DeepSeek、Kimi、GLM、MiniMax 等多方模型（含三方直供模型），但 Qwen-Audio 不支持该协议；  
  - `completions` 接口（[completions 接口](../../raw/model-api-reference/toolkits-and-frameworks/completions.md)）专用于代码补全，当前仅支持 `qwen-coder-turbo`。

- **多模态理解**：  
  `chat/completions`（[OpenAI Vision接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/qwen-vl-compatible-with-openai.md)）支持 `qwen3-vl-plus`、`QVQ`、`Qwen-OCR` 等视觉模型，其中 QVQ 仅支持[流式输出](../concepts/streaming-output.md)。

- **向量嵌入**：  
  `embeddings` 接口（[OpenAI Embedding接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/embedding-interfaces-compatible-with-openai.md)）支持 `text-embedding-v4` 等多版本文本嵌入模型，但多模态 Embedding（如 `qwen3-vl-embedding`）**不支持** [OpenAI 兼容接口](../concepts/openai-compatible-interface.md)。

- **文件与批量处理**：  
  `files` 接口（[OpenAI文件接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/openai-file-interface.md)）支持 `file-extract`（文档问答）、`batch`（批量任务）、`fine-tune`（调优数据集）三类用途；  
  `batch` 接口（[OpenAI兼容-Batch（文件输入）](../../raw/model-api-reference/toolkits-and-frameworks/batch-interfaces-compatible-with-openai.md)）支持 JSONL 格式批量提交，适用于非实时场景。

- **会话管理**：  
  `conversations` 接口（[OpenAI Conversations接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/openai-compatible-conversations.md)）提供会话生命周期管理（创建/查询/更新/删除），配合 `responses` API 实现跨设备上下文延续。

> **注意**：文档 1 中列出的 `qwen3.6-35b-a3b` 等部分模型未在文档 2 的通用 Chat 接口支持列表中出现，且文档 2 明确指出“三方直供模型仅在中国站的中国内地地域可用”，而文档 1 未限定地域。实际使用时请以控制台可用模型为准，并确认对应地域的 API Key 与服务端点。

## 关键参数

| 参数 | 类型 | 说明 | 备注 |
|------|------|------|------|
| `base_url` | string | 服务端点地址 | 必须使用业务空间专属域名（如 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`），旧域名 `dashscope.aliyuncs.com` 已逐步停用（见 [OpenAI Responses接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-with-openai-responses-api.md) 和 [OpenAI Conversations接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/openai-compatible-conversations.md)） |
| `model` | string | 模型名称 | 需严格匹配文档中列出的支持型号，例如 `qwen3.7-plus`（Responses）、`qwen3-vl-plus`（Vision）、`text-embedding-v4`（Embedding） |
| `previous_response_id` | string | 上一轮响应 ID | 仅 Responses API 支持，用于自动关联上下文，**必须传顶层 `id`（UUID 格式），而非 `output` 内消息的 `id`**（见 [OpenAI Responses接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-with-openai-responses-api.md)） |
| `enable_thinking` | boolean | 是否启用思考模式 | Batch 场景下 `qwen3.7`/`qwen3.6`/`qwen3.5` 系列模型默认开启，需显式设置为 `false` 关闭以控制成本（见 [OpenAI兼容-Batch Chat](../../raw/model-api-reference/toolkits-and-frameworks/openai-compatible-batch-chat.md) 和 [OpenAI兼容-Batch（文件输入）](../../raw/model-api-reference/toolkits-and-frameworks/batch-interfaces-compatible-with-openai.md)） |
| `purpose` | string | 文件用途标识 | `files.create()` 必填，取值为 `file-extract`、`batch` 或 `fine-tune`（见 [OpenAI文件接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/openai-file-interface.md)） |

## 使用方式

### 基础调用流程
1. **配置环境**：获取并配置 `DASHSCOPE_API_KEY` 到环境变量；  
2. **初始化客户端**：指定 `base_url`（务必使用业务空间专属域名）和 `api_key`；  
3. **发起请求**：根据接口类型调用对应方法（如 `client.responses.create()`、`client.chat.completions.create()`、`client.embeddings.create()`）；  
4. **处理响应**：解析返回的 `output_text`（Responses）、`choices[0].message.content`（Chat）、`data[0].embedding`（Embeddings）等字段。

### 框架集成
- **LangChain**：推荐使用 `langchain_openai`（仅支持部分模型）或 `langchain-community` + `dashscope`（支持全部模型）。示例：
  ```python
  # OpenAI 兼容方式（受限模型）
  from langchain_openai import ChatOpenAI
  llm = ChatOpenAI(base_url="https://dashscope.aliyuncs.com/compatible-mode/v1", model="qwen-plus")
  
  # DashScope 原生方式（全模型支持）
  from langchain_community.chat_models.tongyi import ChatTongyi
  llm = ChatTongyi(model="qwen-plus", dashscope_api_key=os.getenv("DASHSCOPE_API_KEY"))
  ```
  详见 [在LangChain中使用阿里云百炼](../../raw/model-api-reference/toolkits-and-frameworks/use-bailian-in-langchain.md)。

### 批量与异步
- **Batch Chat**：将 `base_url` 替换为 `https://batch.dashscope.aliyuncs.com/compatible-mode/v1`，其余参数与 Chat 接口一致；  
- **Batch File**：先调用 `client.files.create(purpose="batch")` 上传 JSONL 文件，再调用 `client.batches.create(input_file_id=..., endpoint="/v1/chat/completions")` 提交任务；  
- **超时控制**：Batch 接口默认等待 3600 秒，可通过 SDK 的 `timeout` 参数（Python/Java/Node.js）或 HTTP `timeout` header 自定义。

## 限制和注意事项

- **地域与域名约束**：  
  华北2（北京）和新加坡地域已启用业务空间专属域名（如 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com`），旧域名 `dashscope.aliyuncs.com` 将停止维护。美国（弗吉尼亚）、德国（法兰克福）、日本（东京）仍使用 `dashscope-us.aliyuncs.com` 等固定域名（见 [OpenAI Responses接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-with-openai-responses-api.md)）。

- **模型与协议兼容性**：  
  - Qwen-Audio **不支持** OpenAI 兼容协议，仅支持 DashScope 原生协议；  
  - 多模态 Embedding 模型（如 `qwen3-vl-embedding`）**不支持** OpenAI Embedding 接口；  
  - `completions` 接口当前**仅支持 `qwen-coder-turbo`**，不支持其他模型（见 [completions 接口](../../raw/model-api-reference/toolkits-and-frameworks/completions.md)）。

- **文件与配额限制**：  
  - `files` 接口总存储上限为 **100 GB**，最多 **10,000 个文件**；  
  - `file-extract` 单文件最大 **150 MB**，`batch` 单文件最大 **500 MB**，`fine-tune` 单文件最大 **300 MB**；  
  - `batch` 测试模型 `batch-test-model` 文件大小上限 **1 MB**，行数上限 **100 行**。

- **上下文与状态管理**：  
  - `previous_response_id` 在 Responses API 中有效期为 **7 天**；  
  - `conversations` API 创建的会话本身不存储消息内容，仅维护元数据，消息需通过 `items` 接口单独添加（见 [OpenAI Conversations接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/openai-compatible-conversations.md)）。

- **错误处理**：  
  所有接口均遵循 OpenAI 错误格式（`error.code`、`error.message`），常见错误码参考 [错误码文档](https://help.aliyun.com/zh/model-studio/error-code)。

## 来源文档

- [OpenAI Responses接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-with-openai-responses-api.md)
- [OpenAI Chat接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-of-openai-with-dashscope.md)
- [OpenAI Vision接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/qwen-vl-compatible-with-openai.md)
- [completions 接口](../../raw/model-api-reference/toolkits-and-frameworks/completions.md)
- [OpenAI文件接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/openai-file-interface.md)
- [OpenAI兼容-Batch Chat](../../raw/model-api-reference/toolkits-and-frameworks/openai-compatible-batch-chat.md)
- [OpenAI Embedding接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/embedding-interfaces-compatible-with-openai.md)
- [OpenAI兼容-Batch（文件输入）](../../raw/model-api-reference/toolkits-and-frameworks/batch-interfaces-compatible-with-openai.md)
- [OpenAI Conversations接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/openai-compatible-conversations.md)
- [在LangChain中使用阿里云百炼](../../raw/model-api-reference/toolkits-and-frameworks/use-bailian-in-langchain.md)



# toolkits and [frameworks](frameworks.md)

阿里云百炼提供多种 OpenAI 兼容的工具包与框架接口，支持开发者快速迁移现有应用。所有接口均基于标准 OpenAI REST API 协议设计，仅需调整 `base_url`、`api_key` 和模型名称即可接入，无需重写业务逻辑。核心能力覆盖文本生成、[多模态](../concepts/multi-modal.md)理解、向量嵌入、批量推理、对话状态管理及[文件处理](../concepts/file-processing.md)等场景。

## 支持的模型/功能

百炼支持的 [OpenAI 兼容接口](../concepts/openai-compatible-interface.md)按功能划分为以下几类：

- **Chat 接口**：支持 `qwen-plus`、`qwen-max`、`qwen-flash`、`qwen-long`、`qwen-vl-plus`、`qwen-ocr`、`deepseek-r1`、`kimi`、`glm`、`minimax` 等主流模型（含商业版与开源版），详见 [OpenAI Chat接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-of-openai-with-dashscope.md)；  
- **Vision 接口**：专为视觉理解优化，支持 `qwen-vl-plus`、`qvq`、`qwen-ocr`，其中 `qvq` 仅支持[流式输出](../concepts/streaming-output.md)；  
- **Embedding 接口**：支持 `text-embedding-v1` 至 `v4` 全系列文本向量模型，支持多语种及可选维度（`v3/v4` 支持 `dimensions` 参数）；  
- **Completions 接口**：面向代码补全等场景，当前仅支持 `qwen-coder-turbo`（见 [completions 接口](../../raw/model-api-reference/toolkits-and-frameworks/completions.md)）；  
- **Conversations 接口**：提供会话生命周期管理（创建、查询、更新、删除、追加消息），适用于跨设备长周期对话；  
- **Files 接口**：支持上传文件用于文档问答（`purpose=file-extract`）、批量任务（`purpose=batch`）或模型调优（`purpose=fine-tune`）；  
- **Batch 接口**：包含两种模式——  
  - **Batch Chat**（单请求同步等待）：通过 `https://batch.dashscope.aliyuncs.com/compatible-mode/v1` 调用，适用于低频高成本场景；  
  - **Batch File**（JSONL 文件异步提交）：支持千级并发，费用为实时调用的 50%，详见 [OpenAI兼容-Batch（文件输入）](../../raw/model-api-reference/toolkits-and-frameworks/batch-interfaces-compatible-with-openai.md)。

> **注意**：`Qwen-Audio` 明确不支持 OpenAI 兼容协议，仅支持 DashScope 原生协议；`qwen3.5-omni-plus` 在 Batch 场景下不支持语音输出，且 `qwen3.7`/`qwen3.6`/`qwen3.5` 系列模型默认开启思考模式，需显式设置 `enable_thinking=false` 关闭以避免额外 token 成本。

## 关键参数

所有 [OpenAI 兼容接口](../concepts/openai-compatible-interface.md)共用以下核心参数：

| 参数 | 类型 | 必选 | 说明 |
|------|------|------|------|
| `model` | string | 是 | 模型名称，如 `qwen-plus`、`text-embedding-v4`、`qwen-vl-plus` 等 |
| `base_url` | string | 是 | 服务端点，**必须使用业务空间专属域名**（如 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`），旧域名（`dashscope.aliyuncs.com`）已不推荐使用（见 [OpenAI Chat接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-of-openai-with-dashscope.md)） |
| `api_key` | string | 是 | 百炼 API Key，建议通过环境变量 `DASHSCOPE_API_KEY` 配置以降低泄露风险 |

通用可选参数：
- `temperature` / `top_p`：控制生成多样性，二者建议只设其一；
- `max_tokens`：限制输出长度，超限将截断（不影响模型内部生成过程）；
- `stream` + `stream_options={"include_usage": true}`：启用[流式输出](../concepts/streaming-output.md)并在末尾返回 token 统计；
- `stop`：指定终止字符串，可用于敏感词过滤；
- `seed`：设置随机种子以获得确定性输出（范围 `0–2^31−1`）；
- `presence_penalty`：抑制重复内容（范围 `[-2.0, 2.0]`）。

模型特有参数：
- Embedding：`dimensions`（仅 `v3/v4` 支持）、`encoding_format`（`float` 或 `base64`）；
- Conversations：`metadata`（结构化元数据，≤16 对键值对）；
- Batch File：`completion_window`（最长等待时间，如 `"24h"`）、`enable_thinking`（与 `model` 同级，不可置于 `extra_body` 内）。

## 使用方式

### SDK 调用（推荐）
- **Python**：安装 `openai>=1.0.0` 或 `langchain_openai`，初始化时传入 `base_url` 和 `api_key`：
  ```python
  from openai import OpenAI
  client = OpenAI(
      api_key=os.getenv("DASHSCOPE_API_KEY"),
      base_url="https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1"
  )
  # Chat
  client.chat.completions.create(model="qwen-plus", messages=[...])
  # Embedding
  client.embeddings.create(model="text-embedding-v4", input="hello")
  # Files
  client.files.create(file=Path("doc.pdf"), purpose="file-extract")
  # Conversations
  client.conversations.create(items=[{"role":"system","content":"..."}])
  ```
- **Node.js/Java/Go/C#**：同理配置 `baseURL` 或 `baseUrl`，调用对应方法（详见各文档示例）。

### HTTP 直连
- 所有接口均支持标准 REST 调用，`Authorization: Bearer ${DASHSCOPE_API_KEY}` + `Content-Type: application/json`；
- Endpoint 示例：
  - Chat：`POST https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1/chat/completions`
  - Embedding：`POST https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1/embeddings`
  - Conversations：`POST https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1/conversations`

### LangChain 集成
- **OpenAI 方式**：使用 `langchain_openai.ChatOpenAI`，仅支持部分模型（见 [在LangChain中使用阿里云百炼](../../raw/model-api-reference/toolkits-and-frameworks/use-bailian-in-langchain.md)）；
- **DashScope 原生方式**：使用 `langchain_community.chat_models.tongyi.ChatTongyi`，支持全部百炼文本模型，推荐用于生产环境。

## 限制和注意事项

- **地域与域名**：北京、新加坡、东京、弗吉尼亚四地均提供专属 `WorkspaceId` 域名，**强烈建议迁移**（旧域名 `dashscope.aliyuncs.com` 性能与稳定性较低）；  
- **三方模型可用性**：`DeepSeek`、`Kimi`、`GLM`、`MiniMax` 等仅在中国内地地域可用，调用前须在控制台开通对应服务；  
- **文件限制**：`files` 接口总存储上限 100 GB / 10000 个文件；`file-extract` 单文件 ≤150 MB，`batch` 单文件 ≤500 MB，`fine-tune` 单文件 ≤300 MB；  
- **Batch 超时**：Batch Chat 默认超时 3600 秒（1 小时），Batch File 任务最长等待 `completion_window`（如 `"24h"`）；  
- **Qwen-Audio 不兼容**：该模型明确不支持 OpenAI 协议，需改用 DashScope 原生 SDK；  
- **[函数调用](../concepts/function-calling.md)（Function Calling）**：仅 `chat.completions` 接口支持，`completions` 接口不支持（见 [completions 接口](../../raw/model-api-reference/toolkits-and-frameworks/completions.md)）；  
- **[多模态](../concepts/multi-modal.md)输入**：`qwen-vl-plus` 等模型支持 `image_url`（HTTP URL 或 `data:image/...` Base64），但 `completions` 接口不支持图像输入。

## 来源文档

- [OpenAI Chat接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-of-openai-with-dashscope.md)
- [completions 接口](../../raw/model-api-reference/toolkits-and-frameworks/completions.md)
- [OpenAI Vision接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/qwen-vl-compatible-with-openai.md)
- [OpenAI文件接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/openai-file-interface.md)
- [OpenAI兼容-Batch（文件输入）](../../raw/model-api-reference/toolkits-and-frameworks/batch-interfaces-compatible-with-openai.md)
- [OpenAI兼容-Batch Chat](../../raw/model-api-reference/toolkits-and-frameworks/openai-compatible-batch-chat.md)
- [OpenAI Embedding接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/embedding-interfaces-compatible-with-openai.md)
- [OpenAI Conversations接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/openai-compatible-conversations.md)
- [在LangChain中使用阿里云百炼](../../raw/model-api-reference/toolkits-and-frameworks/use-bailian-in-langchain.md)



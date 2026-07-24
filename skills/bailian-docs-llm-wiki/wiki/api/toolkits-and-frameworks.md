# toolkits and [frameworks](frameworks.md)

阿里云百炼提供多种 OpenAI 兼容的工具包与框架接口，支持开发者无缝迁移现有应用。核心能力覆盖文本生成（chat/completions）、多模态理解（vision）、向量嵌入（embedding）、文件管理（files）、批量处理（batch）、会话管理（conversations）等场景，并兼容主流 SDK（如 OpenAI SDK、LangChain）。

## 支持的模型/功能

百炼支持的 OpenAI 兼容功能按协议类型划分如下：

- **Chat 接口**：支持 `qwen-plus`、`qwen-max`、`qwen-flash`、`qwen-long`、`qwen-omni`、`qwen-math`、`qwen-coder` 等 Qwen 系列模型，以及第三方直供模型（如 `deepseek-r1`、`kimi-pro`、`glm-4`、`minimax-abab6.5`）。详见 [OpenAI Chat接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-of-openai-with-dashscope.md)。
- **Vision 接口**：支持 `qwen-vl-plus`、`qwen3-vl-plus`、`qwen-vl-ocr`、`qvq` 等视觉模型，支持 `image_url` 格式输入；注意 `QVQ` 模型仅支持[流式输出](../concepts/streaming-output.md) [OpenAI Vision接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/qwen-vl-compatible-with-openai.md)。
- **Embedding 接口**：支持 `text-embedding-v1` 至 `v4` 全系列文本向量模型，但**多模态 Embedding 模型（如 `qwen3-vl-embedding`）不支持 OpenAI 兼容协议**，需使用原生 DashScope 接口 [OpenAI Embedding接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/embedding-interfaces-compatible-with-openai.md)。
- **Completions 接口**：当前**仅支持 `qwen-coder-turbo`**，专用于代码补全场景（前缀/前后缀补全），不支持通用文本生成 [completions 接口](../../raw/model-api-reference/toolkits-and-frameworks/completions.md)。
- **Files 接口**：支持 `purpose=file-extract`（文档问答）、`purpose=batch`（批量任务输入）、`purpose=fine-tune`（调优数据集）三类用途，对应 `qwen-long`、`qwen-doc-turbo`、`batch` 和 `fine-tuning` 场景 [OpenAI文件接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/openai-file-interface.md)。
- **Batch 接口**：分为两种模式：
  - **文件批量（Batch File）**：通过 JSONL 文件提交数百至数千请求，适用于数据分析、评测等非实时场景；
  - **单请求批量（Batch Chat）**：单次请求保持连接等待结果，成本降低 50%，适用于对延迟不敏感但需同步返回的场景 [OpenAI兼容-Batch（文件输入）](../../raw/model-api-reference/toolkits-and-frameworks/batch-interfaces-compatible-with-openai.md) 和 [OpenAI兼容-Batch Chat](../../raw/model-api-reference/toolkits-and-frameworks/openai-compatible-batch-chat.md)。
- **Conversations 接口**：提供会话生命周期管理（create/retrieve/update/delete）及消息项增删（items），用于跨设备/长时间对话上下文持久化 [OpenAI Conversations接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/openai-compatible-conversations.md)。

> **注意**：文档 1 与文档 9 均提及 `qwen-audio` 不支持 OpenAI 兼容协议，但文档 1 明确指出“Qwen-Audio不支持OpenAI兼容协议，仅支持DashScope协议”，而其他文档未再提及该模型——该限制仍有效，且无例外。

## 关键参数

| 参数 | 类型 | 说明 | 备注 |
|------|------|------|------|
| `base_url` | string | 接口服务地址 | 必须使用业务空间专属域名（如 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`），旧域名（`dashscope.aliyuncs.com`）已不推荐；各地域 URL 不同，需严格匹配 [OpenAI Chat接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-of-openai-with-dashscope.md) |
| `model` | string | 模型名称 | 必须从各接口支持的模型列表中选择，例如 `completions` 接口仅接受 `qwen-coder-turbo`；`embedding` 接口仅接受 `text-embedding-*` 系列；`vision` 接口仅接受 `qwen-vl-*` 系列 |
| `stream` / `stream_options` | boolean / object | [流式输出](../concepts/streaming-output.md)控制 | `stream=true` 启用流式；`stream_options={"include_usage": true}` 可在最后一 chunk 返回 token 统计；`QVQ` 模型强制流式 [OpenAI Vision接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/qwen-vl-compatible-with-openai.md) |
| `enable_thinking` | boolean | 思考模式开关 | 仅对 `qwen3.5+` 系列模型生效，默认开启；若需关闭以降低成本，必须作为 `body` 顶层参数传入（不可放在 `extra_body` 中） [OpenAI兼容-Batch（文件输入）](../../raw/model-api-reference/toolkits-and-frameworks/batch-interfaces-compatible-with-openai.md) |
| `dimensions` | integer | 向量维度 | 仅 `text-embedding-v3` 和 `v4` 支持，取值需在模型支持范围内（如 `v4` 支持 64–2048） [OpenAI Embedding接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/embedding-interfaces-compatible-with-openai.md) |

## 使用方式

### SDK 调用（推荐）
- **OpenAI SDK**：安装 `openai>=1.0.0`，配置 `api_key`（建议环境变量）和 `base_url` 即可复用原有逻辑。所有接口均遵循 OpenAI Python/Node.js/Java/Go SDK 标准方法（如 `client.chat.completions.create`、`client.files.create`、`client.batches.create`）。
- **LangChain 集成**：
  - `langchain_openai.ChatOpenAI`：仅支持 OpenAI 兼容模型（如 `qwen-plus`），不支持 `qwen-long` 或 `qwen-doc-turbo`；
  - `langchain_community.chat_models.tongyi.ChatTongyi`（Python）或 `@langchain/community/chat_models/alibaba_tongyi`（JS）：支持百炼全部文本模型，包括部署后模型 [在LangChain中使用阿里云百炼](../../raw/model-api-reference/toolkits-and-frameworks/use-bailian-in-langchain.md)。

### HTTP 直调
- 所有接口均支持标准 RESTful 调用，`Authorization: Bearer ${DASHSCOPE_API_KEY}` + `Content-Type: application/json`；
- 注意 endpoint 差异：`chat/completions`、`completions`、`embeddings`、`files`、`batches`、`conversations` 等路径不可混用；
- `files` 接口需用 `multipart/form-data` 提交（`--form`），其余均为 JSON body。

### 地域与 WorkspaceId
- `{WorkspaceId}` 是必需占位符，需从百炼控制台「业务空间详情」获取；
- 北京、新加坡、东京、弗吉尼亚四地均有独立 `base_url`，API Key 与地域强绑定，**跨地域调用将失败**。

## 限制和注意事项

- **Qwen-Audio 不支持 OpenAI 兼容协议**：必须使用 DashScope 原生协议，此限制在多份文档中一致确认 [OpenAI Chat接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-of-openai-with-dashscope.md)。
- **Completions 接口功能受限**：仅支持 `qwen-coder-turbo`，且**不支持 `stop` 字符串截断、`logprobs` 输出、`n>1` 并行采样**，仅提供基础补全能力 [completions 接口](../../raw/model-api-reference/toolkits-and-frameworks/completions.md)。
- **Batch Chat 超时约束**：默认等待 3600 秒（1 小时），超时即断连返回错误；客户端需显式设置 `timeout`（Python/Node.js/Go/Java 均支持），C# 需设 `HttpClient.Timeout`。
- **文件配额硬性限制**：`files` 接口总容量 ≤100 GB、文件数 ≤10000 个；单文件大小上限依 `purpose` 而异：`file-extract` ≤150 MB，`batch` ≤500 MB，`fine-tune` ≤300 MB [OpenAI文件接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/openai-file-interface.md)。
- **Conversations 接口元数据限制**：`metadata` 最多 16 对 key-value，key ≤64 字符，value ≤512 字符；`items` 创建时最多 20 条初始消息 [OpenAI Conversations接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/openai-compatible-conversations.md)。
- **三方直供模型地域限制**：DeepSeek、Kimi、GLM 等仅在中国内地（北京）可用，调用前需在控制台开通对应服务，且**不支持国际地域**。

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



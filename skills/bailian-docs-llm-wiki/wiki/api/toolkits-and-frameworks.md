# toolkits and [frameworks](frameworks.md)

阿里云百炼提供多种 [OpenAI 兼容接口](../concepts/openai-compatible-api.md)及配套工具链，支持开发者快速迁移现有应用或构建新模型服务。核心能力覆盖文本生成、视觉理解、向量嵌入、批量推理、文件处理及对话状态管理等场景，所有接口均通过统一的 `compatible-mode/v1` 路径提供标准化调用方式，并支持多地域业务空间专属域名以提升稳定性与性能。

## 支持的模型/功能

百炼支持的 OpenAI 兼容能力按功能维度划分如下：

- **通用文本生成**：通过 `chat/completions` 接口支持 Qwen 系列（如 `qwen3.7-plus`、`qwen-plus`）、第三方直供模型（DeepSeek、Kimi、GLM 等）及代码专用模型（`qwen-coder-turbo`）。[OpenAI Chat接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-of-openai-with-dashscope.md) 文档明确列出各地域支持的完整模型列表。
  
- **视觉理解**：`qwen3-vl-plus`、`qwen-vl-ocr`、`QVQ` 等多模态模型支持 OpenAI Vision 协议，接受 `image_url` 类型输入并返回结构化描述。[OpenAI Vision接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/qwen-vl-compatible-with-openai.md) 文档说明其仅支持[流式输出](../concepts/streaming-output.md)（QVQ 模型强制流式）。

- **文本补全**：`completions` 接口专为代码补全设计，当前仅支持 `qwen-coder-turbo` 模型，且仅限华北2（北京）地域。[completions 接口](../../raw/model-api-reference/toolkits-and-frameworks/completions.md) 明确指出该接口不支持后缀生成前缀等高级补全模式。

- **长上下文与文档分析**：`Qwen-Long` 和 `Qwen-Doc-Turbo` 可通过文件 ID 进行问答与数据提取，依赖 [OpenAI文件接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/openai-file-interface.md) 上传 `.pdf`、`.docx`、图像等格式文件（单文件上限 150 MB）。

- **向量嵌入**：`text-embedding-v1` 至 `v4` 系列模型支持 OpenAI Embedding 接口，其中 `v3` 和 `v4` 支持 `dimensions` 参数自定义向量维度；多模态 Embedding（如 `qwen3-vl-embedding`）**不支持** OpenAI 兼容协议，需使用专用 API。[OpenAI Embedding接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/embedding-interfaces-compatible-with-openai.md) 明确标注此限制。

- **批量处理**：提供两种 Batch 方式：
  - **文件批量**（`/files` + `/batches`）：适用于数千请求的异步批处理，支持 `qwen3.7-max` 等大模型单次 256K token 上下文，费用为实时调用的 50%；
  - **同步 Batch Chat**（`/batch/chat/completions`）：单请求同步等待，适用于数据标注等非实时场景，端点为 `https://batch.dashscope.aliyuncs.com/compatible-mode/v1`。二者能力差异详见 [OpenAI兼容-Batch（文件输入）](../../raw/model-api-reference/toolkits-and-frameworks/batch-interfaces-compatible-with-openai.md) 与 [OpenAI兼容-Batch Chat](../../raw/model-api-reference/toolkits-and-frameworks/openai-compatible-batch-chat.md)。

- **对话状态管理**：`conversations` 接口用于创建、更新、删除会话元数据；`responses` 接口则通过 `previous_response_id` 自动注入历史上下文，无需手动维护消息数组。二者配合可实现跨设备对话延续。[OpenAI Conversations接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/openai-compatible-conversations.md) 与 [OpenAI Responses接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-with-openai-responses-api.md) 分别详述其设计目标与适用场景。

> **注意**：文档 1（Responses API）与文档 3（Chat API）均提及 `qwen3.7-plus` 等模型支持，但 Responses API 明确列出数十个带时间戳的变体（如 `qwen3.7-plus-2026-05-26`），而 Chat API 文档仅泛称“Qwen 大语言模型”，未列具体版本。实际调用时应以 Responses API 文档中的模型列表为准，避免因模型命名不一致导致 404 错误。

## 关键参数

| 参数 | 适用接口 | 说明 | 注意事项 |
|------|----------|------|----------|
| `base_url` | 所有兼容接口 | 必须配置为业务空间专属域名（如 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`）以获得最佳性能；旧域名（`dashscope.aliyuncs.com`）仍可用但即将停用。 | `{WorkspaceId}` 需从控制台获取，不同地域域名格式不同（见各文档“服务地址”章节）。 |
| `model` | `chat/completions`, `completions`, `embeddings`, `responses` | 模型名称必须严格匹配支持列表，大小写敏感。`qwen-coder-turbo` 仅在 `completions` 接口有效，不可用于 `chat/completions`。 | `qwen3-vl-plus` 在 Vision 接口有效，但在 Chat 接口可能返回 `model_not_found`。 |
| `enable_thinking` | Batch 场景（`qwen3.5/3.6/3.7` 系列） | 控制是否启用思考模式（产生 reasoning tokens）。默认开启，显式设为 `false` 可降低成本。 | 该参数必须作为 JSONL 请求体顶层字段传入，**不可**置于 `extra_body` 内（见文档 6 和 8 的“重要”提示）。 |
| `previous_response_id` | `responses` 接口 | 传入上一轮响应的顶层 `id`（UUID 格式），用于自动关联上下文。 | 必须是 `response.id`，而非 `output[].id`（见文档 1 示例注释）。 |
| `purpose` | `files/create` | 决定文件用途：`file-extract`（文档分析）、`batch`（批量任务）、`fine-tune`（调优数据集）。不同 purpose 对文件格式和大小限制不同（如 `batch` 要求 jsonl，最大 500 MB）。 | `file-extract` 支持图片，`batch` 不支持图片直接上传（需转为 base64 或 URL）。 |

## 使用方式

### 基础调用流程
1. **配置环境**：设置 `DASHSCOPE_API_KEY` 环境变量，安装对应 SDK（如 `pip install openai langchain_openai`）；
2. **初始化客户端**：指定 `base_url` 和 `api_key`；
3. **构造请求**：根据接口类型传入必要参数（`model`, `input`/`messages`/`prompt`/`input` 等）；
4. **处理响应**：解析 `output_text`（Responses）、`choices[0].message.content`（Chat）、`data[0].embedding`（Embedding）等字段。

### 框架集成
- **LangChain**：推荐使用 `langchain_openai.ChatOpenAI`（兼容部分模型）或 `langchain_community.chat_models.tongyi.ChatTongyi`（支持全部百炼模型）。[在LangChain中使用阿里云百炼](../../raw/model-api-reference/toolkits-and-frameworks/use-bailian-in-langchain.md) 提供 Python/JS/Java 完整示例，包括 streaming、tool calling 等高级用法。
- **批量任务**：优先使用文件批量（`/batches`），其吞吐量与成本优势显著；若只需单请求延迟容忍，选用同步 Batch Chat（`/batch/chat/completions`），注意调整 `timeout`（最长 3600 秒）。

### 地域与域名选择
- **北京/新加坡用户**：必须使用业务空间专属域名（`{WorkspaceId}.cn-beijing.maas.aliyuncs.com`），否则可能遭遇性能下降或未来不可用；
- **弗吉尼亚/东京/法兰克福用户**：仅弗吉尼亚提供公共域名（`dashscope-us.aliyuncs.com`），其余地域需配置 WorkspaceId（见文档 1、3、4）。

## 限制和注意事项

- **地域限制**：`completions` 接口**仅支持华北2（北京）地域**（文档 2 明确声明），其他地域调用将失败；`Qwen-Audio` 模型**完全不支持** OpenAI 兼容协议（文档 3 注明）。
  
- **文件配额**：文件存储总大小上限 100 GB，文件数上限 10,000 个；达到任一上限后新上传将失败（文档 5）。

- **Batch 文件格式**：JSONL 输入文件中每行必须是合法 JSON，且 `body` 字段需包含 `model` 和 `messages`（Chat）或 `input`（Embedding）等必需字段；多模态请求需将图片转为 `image_url` 或 base64（文档 6 示例）。

- **参数冲突**：`temperature` 与 `top_p` **不可同时设置**，否则请求将被拒绝（文档 2 “输入参数”说明）。

- **模型能力差异**：`qwen3.5-omni-plus` 在 Batch 场景下**不支持语音输出**（文档 6、8 的“重要”提示）；`qwen-vl-plus` 在 Vision 接口支持流式，在 Chat 接口则为非流式（需验证实际行为）。

- **过期路径**：`/api/v2/apps/protocols/compatible-mode/v1/responses`（文档 1）和 `/api/v2/apps/protocols/compatible-mode/v1/conversations`（文档 9）路径已废弃，必须迁移到 `/compatible-mode/v1/{endpoint}`。

## 来源文档

- [OpenAI Responses接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-with-openai-responses-api.md)
- [completions 接口](../../raw/model-api-reference/toolkits-and-frameworks/completions.md)
- [OpenAI Chat接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-of-openai-with-dashscope.md)
- [OpenAI Vision接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/qwen-vl-compatible-with-openai.md)
- [OpenAI文件接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/openai-file-interface.md)
- [OpenAI兼容-Batch（文件输入）](../../raw/model-api-reference/toolkits-and-frameworks/batch-interfaces-compatible-with-openai.md)
- [OpenAI兼容-Batch Chat](../../raw/model-api-reference/toolkits-and-frameworks/openai-compatible-batch-chat.md)
- [OpenAI Embedding接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/embedding-interfaces-compatible-with-openai.md)
- [OpenAI Conversations接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/openai-compatible-conversations.md)
- [在LangChain中使用阿里云百炼](../../raw/model-api-reference/toolkits-and-frameworks/use-bailian-in-langchain.md)



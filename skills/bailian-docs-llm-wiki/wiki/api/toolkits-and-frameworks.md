# toolkits and [frameworks](frameworks.md)

阿里云百炼提供多种 [OpenAI 兼容接口](../concepts/openai-compatible-interface.md)及配套工具链，支持开发者无缝迁移现有应用。核心能力覆盖文本生成（Chat/Completions/Responses）、多模态理解（Vision）、向量化（Embedding）、文件处理（Files）、批量推理（Batch）、会话管理（Conversations）等场景，并兼容主流框架如 LangChain。所有接口均基于统一的 `compatible-mode/v1` 协议层，通过调整 `base_url`、`api_key` 和 `model` 即可快速接入。

## 支持的模型/功能

百炼支持的 OpenAI 兼容能力按协议类型划分，各接口支持的模型存在差异，需严格匹配：

- **Chat Completions 接口**：支持 Qwen 系列（`qwen-plus`、`qwen-flash`、`qwen3-*`）、Qwen-VL、Qwen-Coder、Qwen-Omni、Qwen-Math、DeepSeek（三方直供）、Kimi、GLM、MiniMax 等；但明确不支持 `Qwen-Audio` [原文标题](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-of-openai-with-dashscope.md)。  
- **Responses API**：专为智能体设计，仅支持 `qwen3-*` 系列模型（如 `qwen3.7-plus`、`qwen3.5-flash` 等），并内置联网搜索、网页抓取等工具能力 [原文标题](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-with-openai-responses-api.md)。  
- **Completions 接口**：当前仅支持 `qwen-coder-turbo`，用于代码补全与中间内容生成 [原文标题](../../raw/model-api-reference/toolkits-and-frameworks/completions.md)。  
- **Vision 接口**：支持 `Qwen-VL`、`QVQ`、`Qwen-OCR`，其中 `QVQ` 仅支持[流式输出](../concepts/streaming-output.md) [原文标题](../../raw/model-api-reference/toolkits-and-frameworks/qwen-vl-compatible-with-openai.md)。  
- **Embedding 接口**：支持 `text-embedding-v1` 至 `v4`，但**多模态 Embedding 模型（如 `qwen3-vl-embedding`）不支持 [OpenAI 兼容接口](../concepts/openai-compatible-interface.md)**，需使用专用多模态向量 API [原文标题](../../raw/model-api-reference/toolkits-and-frameworks/embedding-interfaces-compatible-with-openai.md)。  
- **Files 接口**：支持 `purpose=file-extract`（文档分析）、`purpose=batch`（批量任务）、`purpose=fine-tune`（调优数据集），对应模型包括 `Qwen-Long`、`Qwen-Doc-Turbo` 及 Batch 支持的全部模型 [原文标题](../../raw/model-api-reference/toolkits-and-frameworks/openai-file-interface.md)。  
- **Batch 接口**：分两种模式——文件批量（`/files` + `/batches`）和单请求同步批量（`/batch/chat/completions`），前者支持 `qwen3-*`、`deepseek-*`、`qwen-vl-*` 等数十种模型，后者仅支持部分文本与多模态模型 [原文标题](../../raw/model-api-reference/toolkits-and-frameworks/batch-interfaces-compatible-with-openai.md)。  

> **注意**：文档 6（Batch 文件输入）与文档 7（Batch Chat）对同一模型（如 `qwen3.7-plus`）的适用性描述一致，但文档 7 明确要求“单次请求”，而文档 6 要求 JSONL 文件格式；二者本质是不同调用范式，无矛盾。  
> **注意**：文档 1 和文档 2 均强调北京/新加坡地域应迁移到业务空间专属域名（`{WorkspaceId}.cn-beijing.maas.aliyuncs.com`），但文档 3（Completions）仍使用旧域名 `https://dashscope.aliyuncs.com`，该接口**仅适用于华北2（北京）地域且未更新域名**，存在过时风险。

## 关键参数

所有 [OpenAI 兼容接口](../concepts/openai-compatible-interface.md)共用以下核心参数，行为与 OpenAI 官方一致，但部分参数有百炼特有约束：

- `base_url`：必须设置为对应地域的兼容端点，例如北京地域为 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`；弗吉尼亚、东京、法兰克福等地域无需 `{WorkspaceId}` [原文标题](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-of-openai-with-dashscope.md)。  
- `model`：必须为百炼实际支持的模型名，不可直接复用 OpenAI 的 `gpt-4` 等名称；模型列表需查阅各接口文档，例如 Responses API 不接受 `qwen-plus` [原文标题](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-with-openai-responses-api.md)。  
- `stream` 与 `stream_options`：流式响应时，`stream_options={"include_usage": true}` 可在最后一 chunk 返回 token 统计，该行为在 Chat、Vision、Responses 接口中均有效。  
- `temperature` / `top_p`：二者互斥，建议只设置其一；`temperature` 取值范围 `[0, 2.0)`，`top_p` 为 `(0, 1.0]`。  
- `max_tokens`：仅控制响应截断，**不影响模型实际生成长度**；若模型输出超限，返回内容将被截断。  
- `stop`：支持字符串或 token ID 数组，可用于敏感词拦截。  
- `seed`：设置后提升结果确定性，取值范围 `0` 至 `2^31-1`。  
- `presence_penalty`：控制重复度，范围 `[-2.0, 2.0]`，正值抑制重复。  
- `enable_thinking`：仅 Batch 场景下生效，`qwen3.*` 系列模型默认开启思考模式，显式设为 `false` 可避免额外 token 成本 [原文标题](../../raw/model-api-reference/toolkits-and-frameworks/batch-interfaces-compatible-with-openai.md)。  

## 使用方式

### 基础调用流程
1. **获取凭证**：在百炼控制台开通服务并获取对应地域的 API Key，**强烈建议配置到环境变量 `DASHSCOPE_API_KEY`**，避免硬编码泄露风险。  
2. **配置端点**：根据接口类型与地域选择 `base_url`，北京/新加坡务必使用 `{WorkspaceId}` 专属域名以获得最佳性能。  
3. **构造请求**：按接口规范传入 `model`、`messages`（Chat）、`input`（Responses）、`prompt`（Completions）等必选参数。  
4. **处理响应**：非流式返回完整 JSON；流式需按 chunk 解析，注意 `finish_reason` 和末尾含 `usage` 的 chunk。  

### 框架集成
- **LangChain**：推荐使用 `langchain_openai`（兼容部分模型）或 `langchain-community` + `dashscope`（支持全部模型）。`ChatOpenAI` 构造时需指定 `base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"`；`ChatTongyi` 则使用原生 DashScope SDK，支持更多模型与高级特性 [原文标题](../../raw/model-api-reference/toolkits-and-frameworks/use-bailian-in-langchain.md)。  
- **批量任务**：优先使用文件批量（`/files` + `/batches`），上传 JSONL 后轮询状态；若只需单请求延迟容忍，可用 `/batch/chat/completions` 并设置 `timeout`（最长 3600 秒）[原文标题](../../raw/model-api-reference/toolkits-and-frameworks/openai-compatible-batch-chat.md)。  
- **上下文管理**：  
  - Responses API：通过 `previous_response_id` 自动关联历史，无需维护消息数组；  
  - Conversations API：创建会话后调用 `/conversations/{id}/items` 追加消息，实现跨设备持久化 [原文标题](../../raw/model-api-reference/toolkits-and-frameworks/openai-compatible-conversations.md)。  

## 限制和注意事项

- **地域与域名绑定**：API Key 与 `base_url` 必须匹配同一地域（如北京 Key 配北京 URL），否则返回 `invalid_api_key` 错误；旧域名（`dashscope.aliyuncs.com`）虽仍可用，但文档 1、2、4、8 均明确建议迁移至 `{WorkspaceId}` 专属域名以提升稳定性。  
- **模型能力隔离**：同一模型在不同接口中能力不同，例如 `qwen-plus` 在 Chat 接口可用，但在 Responses 接口不可用；`Qwen-Audio` 完全不支持 OpenAI 协议 [原文标题](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-of-openai-with-dashscope.md)。  
- **文件服务配额**：`/files` 接口总存储上限 100 GB、最多 10,000 个文件；单文件大小限制依 `purpose` 而异：`file-extract` 最大 150 MB，`batch` 最大 500 MB，`fine-tune` 最大 300 MB [原文标题](../../raw/model-api-reference/toolkits-and-frameworks/openai-file-interface.md)。  
- **Batch 超时机制**：文件批量任务最长等待 24 小时；单请求同步批量（Batch Chat）默认超时 3600 秒，需在客户端显式设置 `timeout` 参数。  
- **三方模型可用性**：DeepSeek、Kimi 等三方直供模型**仅在中国站内地地域可用**，且需在控制台单独开通服务 [原文标题](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-of-openai-with-dashscope.md)。  
- **错误处理**：所有接口遵循 OpenAI 错误格式（`error.code` + `error.message`），常见错误码详见官方文档；调试时建议先用 `batch-test-model` 验证链路 [原文标题](../../raw/model-api-reference/toolkits-and-frameworks/batch-interfaces-compatible-with-openai.md)。

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



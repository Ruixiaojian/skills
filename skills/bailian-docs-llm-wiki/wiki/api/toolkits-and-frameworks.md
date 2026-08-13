# toolkits and [frameworks](frameworks.md)

阿里云百炼平台提供多种与主流开源框架兼容的工具包和接口规范，支持开发者快速集成大模型能力。核心包括 OpenAI 兼容系列（Chat、Completions、Embedding、Vision、Responses、Conversations、Batch）、原生文件管理接口，以及 LangChain 等主流框架的专用适配器。所有接口均需配置 API Key 与地域专属 base_url，并遵循统一的认证与错误处理机制。

## 支持的模型/功能

百炼支持的模型能力按接口类型划分：

- **文本生成**：`qwen-plus`、`qwen-flash`、`qwen3.8-max` 等全系千问文本模型，以及 DeepSeek、Kimi、GLM、MiniMax 等第三方直供模型（详见 [OpenAI Chat接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-of-openai-with-dashscope.md)）；
- **代码补全**：`qwen-coder-turbo` 专用于 Completions 接口，支持前缀补全与前后缀中间生成两种模式；
- **[多模态](../concepts/multimodal.md)理解**：`qwen-vl-plus`、`qwen3-vl-plus`、`QVQ`、`Qwen-OCR` 等视觉模型，兼容 OpenAI Vision 规范；
- **向量嵌入**：`text-embedding-v1` 至 `v4` 全系列文本向量模型，支持多语种与可变维度输出；
- **长文档与文件分析**：`qwen-long`、`qwen-doc-turbo` 依赖文件上传接口（purpose=`file-extract`）实现文档问答与数据提取；
- **批量推理**：`qwen3.8-max`、`qwen3.5-omni-plus` 等支持 256K 上下文的模型可用于 Batch Chat 或 Batch File 场景；
- **智能体增强**：`Responses API` 内置联网搜索、网页抓取等工具，`Conversations API` 提供跨设备上下文持久化能力。

> **注意**：`Qwen-Audio` 明确不支持 OpenAI 兼容协议，仅支持 DashScope 原生协议；而 `qwen3-vl-embedding` 等[多模态](../concepts/multimodal.md) Embedding 模型也不支持 OpenAI Embedding 接口，需使用专用[多模态](../concepts/multimodal.md)向量 API [原文标题](../../raw/model-api-reference/toolkits-and-frameworks/embedding-interfaces-compatible-with-openai.md)。

## 关键参数

各接口共用以下关键参数，但行为存在差异：

- **`base_url`**：必须使用业务空间专属域名（如 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`），旧域名（`dashscope.aliyuncs.com`）虽仍可用，但性能与稳定性较低，官方强烈建议迁移 [原文标题](../../raw/model-api-reference/toolkits-and-frameworks/qwen-vl-compatible-with-openai.md)；
- **`model`**：模型名需严格匹配文档列表，例如 `qwen-coder-turbo` 仅在 Completions 接口有效，不可用于 Chat 接口；
- **`stream` / `stream_options`**：[流式输出](../concepts/streaming-output.md)在 Chat、Vision、Responses 等接口中通用，`stream_options={"include_usage": true}` 可在末尾返回 token 统计；
- **`max_tokens`**：在 Completions 接口中仅作截断控制，不影响生成过程；而在 Chat/Responses 中影响实际输出长度；
- **`temperature` 与 `top_p`**：二者互斥，文档明确建议“只设置其中一个值”以避免行为不可控 [原文标题](../../raw/model-api-reference/toolkits-and-frameworks/completions.md)；
- **`enable_thinking`**：仅 Batch 场景下对 `qwen3.x` 系列模型生效，默认开启，显式设为 `false` 可关闭思考模式以降低成本；
- **`dimensions`**：仅 `text-embedding-v3` 和 `v4` 支持，用于指定向量维度（如 `1024`），`v1`/`v2` 不支持该参数。

## 使用方式

### 基础调用流程
1. **获取凭证**：在百炼控制台开通服务并获取 API Key，推荐配置至环境变量 `DASHSCOPE_API_KEY`；
2. **选择接口与模型**：根据任务类型选择对应接口（如代码补全用 `completions`，多轮对话用 `chat.completions`，批量处理用 `batch`）及兼容模型；
3. **配置 SDK 或 HTTP 客户端**：
   - OpenAI SDK：设置 `base_url` 为业务空间专属地址，`api_key` 为环境变量；
   - LangChain：`langchain_openai.ChatOpenAI` 适用于部分模型；`langchain_community.chat_models.tongyi.ChatTongyi` 支持全部百炼文本模型 [原文标题](../../raw/model-api-reference/toolkits-and-frameworks/use-bailian-in-langchain.md)；
4. **构造请求体**：按接口规范传入 `prompt`（Completions）、`messages`（Chat）、`input`（Responses）、`file`（Files）等字段；
5. **处理响应**：解析 `choices[0].message.content`（Chat）、`output_text`（Responses）、`data[0].embedding`（Embedding）等结构化字段。

### 典型场景示例
- **代码补全**：使用 `completions` 接口 + `qwen-coder-turbo`，通过 `<tool_call>{prefix}<tool_call>{suffix}<tool_call>` 模板实现函数体生成；
- **多模态理解**：`chat.completions.create` 中 `messages.content` 包含 `{"type":"image_url","image_url":{"url":"..."}}` 结构；
- **批量处理**：Batch Chat 使用 `base_url="https://batch.dashscope.aliyuncs.com/compatible-mode/v1"`；Batch File 则先调用 `files.create(purpose="batch")` 上传 JSONL 文件，再提交任务；
- **长文档问答**：先 `files.create(purpose="file-extract")` 上传 PDF/TXT，再将返回的 `file_id` 传入 `qwen-long` 的请求参数。

## 限制和注意事项

- **地域与模型绑定**：`DeepSeek-V4` 仅支持华北2（北京）与新加坡地域；`QVQ` 模型强制要求[流式输出](../concepts/streaming-output.md)；`qwen3.5-omni-plus` 在 Batch 场景下不支持语音输出；
- **文件限制**：`file-extract` 单文件上限 150 MB，`batch` 文件上限 500 MB，`fine-tune` 文件上限 300 MB；总存储配额为 100 GB / 10000 个文件；
- **超时与重试**：Batch Chat 默认等待 3600 秒，需在 SDK 客户端显式配置 `timeout` 参数（如 Python 的 `.with_options(timeout=1800.0)`）；
- **上下文管理**：`Responses API` 使用 `previous_response_id`（顶层 `id`）关联上下文，而非 `output` 数组内消息的 `id`；`Conversations API` 需手动创建会话并 `create_items` 添加消息；
- **参数冲突风险**：`temperature` 与 `top_p` 同时设置可能导致结果不稳定，应严格遵循文档建议“只设置其中一个”；
- **测试与验证**：批量任务推荐先用 `batch-test-model` 进行链路验证，该模型跳过真实推理，仅校验格式与权限。

## 来源文档

- [completions 接口](../../raw/model-api-reference/toolkits-and-frameworks/completions.md)
- [OpenAI Vision接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/qwen-vl-compatible-with-openai.md)
- [OpenAI Chat接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-of-openai-with-dashscope.md)
- [OpenAI Responses接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-with-openai-responses-api.md)
- [OpenAI兼容-Batch Chat](../../raw/model-api-reference/toolkits-and-frameworks/openai-compatible-batch-chat.md)
- [OpenAI兼容-Batch（文件输入）](../../raw/model-api-reference/toolkits-and-frameworks/batch-interfaces-compatible-with-openai.md)
- [OpenAI Embedding接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/embedding-interfaces-compatible-with-openai.md)
- [OpenAI文件接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/openai-file-interface.md)
- [OpenAI Conversations接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/openai-compatible-conversations.md)
- [在LangChain中使用阿里云百炼](../../raw/model-api-reference/toolkits-and-frameworks/use-bailian-in-langchain.md)



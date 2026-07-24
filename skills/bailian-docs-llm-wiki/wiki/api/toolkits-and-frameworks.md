# toolkits and [frameworks](frameworks.md)

百炼平台提供多套 [OpenAI 兼容接口](../concepts/openai-compatible-api.md)（Chat、Responses、Completions、Vision、Embedding、Files、Batch、Conversations），支持主流开发框架（如 OpenAI SDK、LangChain）无缝集成。开发者只需调整 `base_url`、`api_key` 和 `model` 参数，即可复用现有代码迁移至百炼服务，无需重写业务逻辑。

## 支持的模型/功能

百炼兼容接口覆盖全模态能力：
- **文本生成**：`qwen-plus`、`qwen-flash`、`qwen3.7-max` 等全系列 Qwen 模型，以及 DeepSeek、Kimi、GLM、MiniMax 等三方直供模型（仅限中国内地地域）[原文标题](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-of-openai-with-dashscope.md)；
- **视觉理解**：`qwen-vl-plus`、`qvq`、`qwen-ocr`，支持图像+文本[多模态](../concepts/multi-modal.md)输入 [原文标题](../../raw/model-api-reference/toolkits-and-frameworks/qwen-vl-compatible-with-openai.md)；
- **文本补全**：`qwen-coder-turbo`，专用于代码续写与中间内容生成 [原文标题](../../raw/model-api-reference/toolkits-and-frameworks/completions.md)；
- **向量嵌入**：`text-embedding-v1` 至 `v4`，支持多语种及可变维度输出，但[多模态](../concepts/multi-modal.md) Embedding（如 `qwen3-vl-embedding`）**不支持** [OpenAI 兼容接口](../concepts/openai-compatible-api.md) [原文标题](../../raw/model-api-reference/toolkits-and-frameworks/embedding-interfaces-compatible-with-openai.md)；
- **长文档处理**：`qwen-long`、`qwen-doc-turbo` 通过文件 ID 实现文档问答与数据提取；
- **批量推理**：支持单请求同步 Batch Chat（`/chat/completions`）与文件驱动 Batch（JSONL 输入），成本降低 50%；
- **会话管理**：`Conversations API` 自动维护跨设备上下文，配合 `Responses API` 实现免消息历史构建的智能体交互 [原文标题](../../raw/model-api-reference/toolkits-and-frameworks/openai-compatible-conversations.md)。

> **注意**：`Qwen-Audio` 明确不支持 OpenAI 兼容协议，仅支持 DashScope 原生协议；`Responses API` 的旧路径 `/api/v2/apps/protocols/compatible-mode/v1/responses` 已废弃，必须迁移到 `/compatible-mode/v1/responses`。

## 关键参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `base_url` | string | 是 | 地域专属端点，北京/新加坡需使用 `{WorkspaceId}.<region>.maas.aliyuncs.com/compatible-mode/v1`；弗吉尼亚/东京/法兰克福等区域使用固定域名或 `{WorkspaceId}` 占位符。所有接口均**强烈建议迁移至业务空间专属域名**以获得更高性能与稳定性 [原文标题](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-of-openai-with-dashscope.md)。 |
| `api_key` | string | 是 | 百炼 API Key，**按地域隔离**（北京、新加坡、弗吉尼亚等 Key 不互通），且必须配置为环境变量 `DASHSCOPE_API_KEY` 或显式传入。 |
| `model` | string | 是 | 模型名称，需严格匹配支持列表（如 `qwen3.7-plus`、`text-embedding-v4`），大小写敏感。 |
| `stream` | boolean | 否 | 控制[流式输出](../concepts/streaming-output.md)，默认 `false`；流式响应需配合 `stream_options={"include_usage": true}` 获取最终 token 统计。 |
| `enable_thinking` | boolean | 否 | 仅 Batch 场景下生效，控制是否启用思考模式（默认开启），影响 token 计费；必须作为 JSONL 请求体顶层字段，不可置于 `extra_body` 内。 |
| `dimensions` | integer | 否 | 仅 `text-embedding-v3/v4` 支持，指定向量维度（如 `1024`）。 |

## 使用方式

### 通用调用流程
1. **安装依赖**：`pip install -U openai`（Python）、`npm install openai`（Node.js）等；
2. **初始化客户端**：传入 `api_key` 和对应地域的 `base_url`；
3. **发起请求**：调用 `.chat.completions.create()`、`.embeddings.create()`、`.files.create()` 等方法；
4. **处理响应**：解析 `choices[0].message.content`（Chat）、`data[0].embedding`（Embedding）、`output_text`（Responses）等字段。

### 框架集成
- **LangChain**：推荐使用 `langchain_openai.ChatOpenAI`（兼容部分模型）或 `langchain_community.chat_models.tongyi.ChatTongyi`（支持全部百炼模型）[原文标题](../../raw/model-api-reference/toolkits-and-frameworks/use-bailian-in-langchain.md)；
- **Batch 文件提交**：需准备符合格式的 JSONL 文件（含 `custom_id`, `method`, `url`, `body`），上传后调用 `client.batches.create(input_file_id=..., endpoint="/v1/chat/completions")`；
- **Conversations 管理**：先 `client.conversations.create()` 创建会话，再 `client.conversations.{id}/items` 追加消息，后续请求自动注入历史。

## 限制和注意事项

- **地域与模型绑定**：`qwen3.7-plus` 在北京/新加坡/弗吉尼亚均可用，但 `qwen3.5-397b-a17b` 仅限北京与新加坡；`qwen3.7-plus` 在日本东京仅支持特定版本（如 `2026-05-26`）；
- **文件限制**：`file-extract` 用途最大 150 MB；`batch` 用途最大 500 MB；`fine-tune` 用途最大 300 MB；总存储上限 10,000 文件 / 100 GB；
- **QVQ 模型强制流式**：`qwen-vl-plus` 可选流/非流，但 `qvq` **仅支持[流式输出](../concepts/streaming-output.md)**，否则调用失败；
- **API 路径变更**：`Responses API`、`Conversations API` 的旧版路径（含 `/api/v2/apps/protocols/`）已弃用，新代码必须使用 `/compatible-mode/v1/{endpoint}`；
- **[Token](../concepts/token.md) 计费差异**：Batch 场景下 `qwen3.5-omni-plus` 不支持语音输出；思考模式开启时 `output_tokens_details.reasoning_tokens` 单独计费；
- **安全实践**：**严禁硬编码 `api_key`**，必须通过环境变量（`DASHSCOPE_API_KEY`）注入，避免泄露风险。

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



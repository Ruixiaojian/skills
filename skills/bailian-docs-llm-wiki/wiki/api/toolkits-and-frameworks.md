# toolkits and [frameworks](frameworks.md)

阿里云百炼平台提供多种 OpenAI 兼容的工具包与框架接口，支持开发者无缝迁移现有应用。核心能力覆盖文本生成、多模态理解、向量嵌入、批量推理、会话管理及专用补全等场景，所有接口均通过统一的 `compatible-mode/v1` 路径提供标准化访问。开发者只需调整 `base_url`、`api_key` 和 `model` 三个参数，即可复用 OpenAI SDK 生态。

## 支持的模型/功能

百炼支持的 [OpenAI 兼容接口](../concepts/openai-compatible-api.md)按功能划分为以下几类：

- **Chat Completions**：支持 Qwen 系列（`qwen-plus`、`qwen3.7-plus`、`qwen3-max` 等）、Qwen-VL、Qwen-Coder、Qwen-Omni、Qwen-Math，以及第三方直供模型（DeepSeek、Kimi、GLM、MiniMax）[原文标题](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-of-openai-with-dashscope.md)。  
- **Vision（多模态）**：仅限 `qwen-vl-plus`、`qven3-vl-plus`、`qwen3-vl-flash`、`qvq`、`qwen-vl-ocr` 等视觉模型，其中 QVQ 仅支持[流式输出](../concepts/streaming-output.md) [原文标题](../../raw/model-api-reference/toolkits-and-frameworks/qwen-vl-compatible-with-openai.md)。  
- **Responses API**：专为智能体设计，内置联网搜索、网页抓取等工具，支持 `qwen3-max`、`qwen3-plus`、`qwen3-flash` 及 `qwen3-coder` 全系列模型，显著简化上下文管理 [原文标题](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-with-openai-responses-api.md)。  
- **Completions（文本补全）**：当前仅支持 `qwen-coder-turbo`，适用于代码续写、函数体生成等场景，支持前缀+后缀双向约束补全 [原文标题](../../raw/model-api-reference/toolkits-and-frameworks/completions.md)。  
- **Embeddings**：支持 `text-embedding-v1` 至 `v4` 全系列，`v3`/`v4` 支持 `dimensions` 参数动态指定向量维度；多模态 Embedding（如 `qwen3-vl-embedding`）**不兼容** OpenAI 接口 [原文标题](../../raw/model-api-reference/toolkits-and-frameworks/embedding-interfaces-compatible-with-openai.md)。  
- **Batch（文件输入）**：支持文本、多模态（含图像 URL/Base64）、向量嵌入等任务，单文件最大 500 MB，需 `purpose="batch"` [原文标题](../../raw/model-api-reference/toolkits-and-frameworks/batch-interfaces-compatible-with-openai.md)。  
- **Conversations API**：用于跨设备/长时间会话状态管理，支持创建、查询、更新、删除会话及追加消息项，与 Responses API 协同实现无状态对话延续 [原文标题](../../raw/model-api-reference/toolkits-and-frameworks/openai-compatible-conversations.md)。

> **注意**：文档 1 与文档 2 均声明 Qwen-Audio 不支持 OpenAI 兼容协议，但文档 1 明确列出其在“支持的模型列表”中，而文档 2 未提及。实际以文档 1 的说明为准：**Qwen-Audio 仅支持 DashScope 协议，不可用于 [OpenAI 兼容接口](../concepts/openai-compatible-api.md)**。

## 关键参数

| 参数 | 类型 | 必选 | 说明 | 备注 |
|------|------|------|------|------|
| `base_url` | string | 是 | 接口服务地址，**必须使用业务空间专属域名**（如 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`） | 文档 1、2、3、5、7、10 均强调旧域名（`dashscope.aliyuncs.com`）已过时，应迁移至 `{WorkspaceId}` 格式；文档 9 的 Batch Chat 使用独立域名 `https://batch.dashscope.aliyuncs.com/compatible-mode/v1` |
| `api_key` | string | 是 | 百炼 API Key，**按地域隔离**（北京/新加坡/弗吉尼亚等需对应 Key） | 所有文档均要求配置环境变量 `DASHSCOPE_API_KEY` 以降低泄露风险 |
| `model` | string | 是 | 模型名称，严格区分大小写与版本后缀（如 `qwen3.7-plus` ≠ `qwen3-plus`） | 文档 3 列出超 30 个 Responses API 专用模型名；文档 4 仅支持 `qwen-coder-turbo`；文档 10 中 `text-embedding-v4` 支持 `dimensions` 参数（v1/v2 不支持） |
| `stream` | boolean | 否 | 是否启用流式响应，默认 `false` | 流式调用需配合 `stream_options={"include_usage": true}` 获取 token 统计（文档 1、2） |
| `enable_thinking` | boolean | 否 | Batch 场景下控制思考模式开关，影响 token 计费 | 文档 5 和 9 明确要求该参数必须置于 JSONL `body` 顶层，与 `model` 同级，不可嵌套于 `extra_body` |

## 使用方式

### SDK 调用（推荐）
- **OpenAI SDK**：安装 `openai>=1.0`，初始化 `OpenAI(api_key=..., base_url=...)`，调用 `client.chat.completions.create()` 或 `client.embeddings.create()` 等方法。  
- **LangChain 集成**：  
  - `langchain_openai.ChatOpenAI`：仅支持 OpenAI 兼容模型（如 `qwen-plus`），需配置 `base_url`；  
  - `langchain_community.chat_models.tongyi.ChatTongyi`：支持百炼全量模型（含非兼容接口模型），需安装 `dashscope` 包 [原文标题](../../raw/model-api-reference/toolkits-and-frameworks/use-bailian-in-langchain.md)。  

### HTTP 直连
- 构造 `POST` 请求，`Authorization: Bearer ${DASHSCOPE_API_KEY}`，`Content-Type: application/json`；  
- Endpoint 示例：`/compatible-mode/v1/chat/completions`（Chat）、`/compatible-mode/v1/responses`（Responses）、`/compatible-mode/v1/embeddings`（Embedding）；  
- Batch 文件上传使用 `/compatible-mode/v1/files`（`purpose=batch`），再通过 `/batches` 提交任务 [原文标题](../../raw/model-api-reference/toolkits-and-frameworks/openai-file-interface.md)。

### 特殊场景适配
- **多轮对话**：Responses API 使用 `previous_response_id`；Conversations API 使用 `conversation_id` + `items` 追加；  
- **文件处理**：Qwen-Long/Qwen-Doc-Turbo 需 `purpose=file-extract`；Batch 输入需 `purpose=batch`；微调数据集需 `purpose=fine-tune`；  
- **视觉输入**：`messages.content` 必须为数组，含 `{"type":"image_url","image_url":{"url":"..."}}` 和 `{"type":"text","text":"..."}` 结构（文档 2）。

## 限制和注意事项

- **地域与域名绑定**：北京/新加坡地域必须使用 `{WorkspaceId}` 专属域名；弗吉尼亚/法兰克福/东京等地域使用固定域名（如 `dashscope-us.aliyuncs.com`），且 API Key 不通用；  
- **模型能力差异**：  
  - Qwen-Audio **不支持** OpenAI 兼容协议（文档 1）；  
  - QVQ 模型 **仅支持[流式输出](../concepts/streaming-output.md)**（文档 2）；  
  - `qwen3.5-omni-plus` 在 Batch 场景下 **不支持语音输出**（文档 5、9）；  
- **Batch 限制**：  
  - 单次请求上下文最大 256K tokens（`qwen3.7-max` 等系列）；  
  - `enable_thinking` 参数若误置于 `extra_body` 将被忽略（文档 5、9）；  
- **安全实践**：API Key **严禁硬编码**，必须通过环境变量注入；生产环境应启用 `stream_options.include_usage` 监控 token 消耗；  
- **错误处理**：所有接口返回标准 OpenAI 错误结构（`{"error":{"message":...,"code":...}}`），需参考 [错误码文档](https://help.aliyun.com/zh/model-studio/error-code) 解析。

## 来源文档

- [OpenAI Chat接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-of-openai-with-dashscope.md)
- [OpenAI Vision接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/qwen-vl-compatible-with-openai.md)
- [OpenAI Responses接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-with-openai-responses-api.md)
- [completions 接口](../../raw/model-api-reference/toolkits-and-frameworks/completions.md)
- [OpenAI兼容-Batch（文件输入）](../../raw/model-api-reference/toolkits-and-frameworks/batch-interfaces-compatible-with-openai.md)
- [OpenAI文件接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/openai-file-interface.md)
- [OpenAI Conversations接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/openai-compatible-conversations.md)
- [在LangChain中使用阿里云百炼](../../raw/model-api-reference/toolkits-and-frameworks/use-bailian-in-langchain.md)
- [OpenAI兼容-Batch Chat](../../raw/model-api-reference/toolkits-and-frameworks/openai-compatible-batch-chat.md)
- [OpenAI Embedding接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/embedding-interfaces-compatible-with-openai.md)



# toolkits and [frameworks](frameworks.md)

阿里云百炼提供多种 OpenAI 兼容的工具包与框架接口，覆盖文本生成、[多模态](../concepts/multimodal.md)理解、向量嵌入、批量推理、对话管理及高级智能体能力等场景。开发者可复用现有 OpenAI SDK 代码，仅需调整 `base_url`、`api_key` 和 `model` 即可快速迁移，无需重写业务逻辑。

## 支持的模型/功能

百炼支持的 [OpenAI 兼容接口](../concepts/openai-compatible-api.md)按功能划分为以下几类：

- **Chat Completions**：通用对话接口，支持 Qwen 系列（如 `qwen-plus`, `qwen3.8-max`）、Qwen-VL、Qwen-Coder、Qwen-Omni、Qwen-Math 及第三方直供模型（DeepSeek、Kimi、GLM、MiniMax）[原文标题](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-of-openai-with-dashscope.md)。  
- **Vision（图像理解）**：兼容 OpenAI Vision 规范，支持 `qwen-vl-plus`、`qwen3-vl-plus`、`QVQ`、`Qwen-OCR` 等视觉模型，支持 `image_url` 格式输入 [原文标题](../../raw/model-api-reference/toolkits-and-frameworks/qwen-vl-compatible-with-openai.md)。  
- **Embedding**：支持 `text-embedding-v1` 至 `v4` 全系列文本向量模型，其中 `v3` 和 `v4` 支持 `dimensions` 参数指定向量维度 [原文标题](../../raw/model-api-reference/toolkits-and-frameworks/embedding-interfaces-compatible-with-openai.md)。  
- **Completions（文本补全）**：专用于代码/内容续写，当前仅支持 `qwen-coder-turbo` 模型，支持前缀补全与“前缀+后缀”中间生成两种模式 [原文标题](../../raw/model-api-reference/toolkits-and-frameworks/completions.md)。  
- **Files（文件管理）**：用于上传文档供 Qwen-Long/Qwen-Doc-Turbo 进行问答或作为 Batch/Fine-tune 的输入，支持 `file-extract`、`batch`、`fine-tune` 三种用途 [原文标题](../../raw/model-api-reference/toolkits-and-frameworks/openai-file-interface.md)。  
- **Batch（批量推理）**：含两种形态：  
  - *Batch File*：通过 JSONL 文件异步提交大批量请求，支持 `qwen3.8-max` 等 256K 上下文模型及[多模态](../concepts/multimodal.md)模型 [原文标题](../../raw/model-api-reference/toolkits-and-frameworks/batch-interfaces-compatible-with-openai.md)；  
  - *Batch Chat*：同步阻塞式单请求批量接口，适用于数据标注等非实时场景，端点为 `https://batch.dashscope.aliyuncs.com/compatible-mode/v1` [原文标题](../../raw/model-api-reference/toolkits-and-frameworks/openai-compatible-batch-chat.md)。  
- **Conversations & Responses（对话状态与智能体）**：  
  - `Conversations API` 提供会话生命周期管理（创建/查询/更新/删除），支持跨设备上下文持久化；  
  - `Responses API` 是 Chat Completions 的增强版，内置联网搜索、代码解释器等工具，支持 `previous_response_id` 自动续接上下文，且 `id` 有效期为 7 天 [原文标题](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-with-openai-responses-api.md)。

> **注意**：文档 2（completions.md）声明仅支持 `qwen-coder-turbo`，但文档 1（compatibility-of-openai-with-dashscope.md）中“支持的模型列表”未包含该模型，且明确指出 `Qwen-Audio` 不支持 OpenAI 兼容协议。此处以文档 2 的明确限定为准，`completions` 接口当前仅限 `qwen-coder-turbo`。

## 关键参数

所有 [OpenAI 兼容接口](../concepts/openai-compatible-api.md)共用以下核心参数：

- `base_url`：必须配置为地域专属域名（推荐），格式为 `https://{WorkspaceId}.{region}.maas.aliyuncs.com/compatible-mode/v1`。北京、新加坡、东京、弗吉尼亚、法兰克福等地域均支持，其中 `{WorkspaceId}` 需从控制台获取 [原文标题](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-of-openai-with-dashscope.md)。  
- `api_key`：须使用对应地域的 API Key，北京与新加坡 Key 不互通。  
- `model`：必须使用百炼支持的模型名（如 `qwen-plus`, `qwen-vl-plus`, `text-embedding-v4`），不可混用 OpenAI 原生模型名。  

其他常用参数：
- `stream` / `stream_options={"include_usage": true}`：启用[流式输出](../concepts/streaming-output.md)并在末尾返回 token 统计；  
- `temperature` / `top_p`：二选一设置，避免同时指定；  
- `max_tokens`：仅截断输出，不影响模型内部生成长度；  
- `seed`：设置后可提升结果确定性；  
- `presence_penalty`：控制重复度，范围 `[-2.0, 2.0]`；  
- `stop`：支持字符串或 token ID 列表，用于主动终止生成。

## 使用方式

### SDK 调用（推荐）
1. 安装对应 SDK：`pip install -U openai`（Python）、`npm install openai`（Node.js）等；  
2. 初始化客户端时传入 `api_key` 和 `base_url`；  
3. 调用对应方法（如 `client.chat.completions.create`、`client.embeddings.create`、`client.files.create`、`client.responses.create`）；  
4. 对于 LangChain 用户，可直接使用 `langchain_openai.ChatOpenAI` 或 `langchain_community.chat_models.tongyi.ChatTongyi`，后者支持全部百炼模型 [原文标题](../../raw/model-api-reference/toolkits-and-frameworks/use-bailian-in-langchain.md)。

### HTTP 调用
- 方法：`POST {base_url}/{endpoint}`（如 `/chat/completions`, `/embeddings`, `/files`, `/responses`）；  
- Header：`Authorization: Bearer ${DASHSCOPE_API_KEY}`, `Content-Type: application/json`；  
- Body：JSON 格式，字段与 SDK 参数一致（如 `model`, `input`, `messages`, `purpose` 等）。

### 地域与端点映射
| 功能 | 北京端点 | 新加坡端点 | 弗吉尼亚端点 | 批量 Chat 专用端点 |
|------|----------|------------|--------------|---------------------|
| Chat/Vision/Embedding | `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1` | `https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/compatible-mode/v1` | `https://dashscope-us.aliyuncs.com/compatible-mode/v1` | `https://batch.dashscope.aliyuncs.com/compatible-mode/v1` |

> **注意**：文档 5（batch-interfaces-compatible-with-openai.md）中“适用范围”表格列出新加坡仅支持 `qwen-max`/`qwen-plus`/`qwen-turbo`，但文档 10（compatibility-with-openai-responses-api.md）明确说明 DeepSeek 模型在新加坡可用，且文档 6（openai-compatible-batch-chat.md）未限制新加坡模型列表。实际支持模型应以控制台或最新 API 文档为准，开发时建议优先查阅控制台模型市场。

## 限制和注意事项

- **域名迁移强制要求**：旧域名 `https://dashscope.aliyuncs.com` 和 `https://dashscope-intl.aliyuncs.com` 已不推荐使用，新业务必须采用 `{WorkspaceId}` 专属域名以保障性能与稳定性 [原文标题](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-of-openai-with-dashscope.md)。  
- **三方模型地域限制**：DeepSeek、Kimi、GLM、MiniMax 等直供模型仅在中国内地地域（北京、杭州等）可用，调用前需在控制台开通对应服务。  
- **文件配额**：`files` 接口总容量上限 100 GB，文件数上限 10,000 个；单文件大小限制依 `purpose` 而异：`file-extract` ≤ 150 MB，`batch` ≤ 500 MB，`fine-tune` ≤ 300 MB。  
- **Batch 超时**：Batch File 最长等待时间为 24 小时；Batch Chat 默认超时 3600 秒（1 小时），可通过 SDK `timeout` 参数或 HTTP `timeout` header 自定义（60–3600 秒）。  
- **Responses API 上下文**：`previous_response_id` 必须传入上一轮响应的顶层 `id`（如 `resp_xxx`），而非 `output` 中消息的 `id`（如 `msg_xxx`），且该 `id` 7 天内有效。  
- **不兼容项**：`Qwen-Audio` 不支持 OpenAI 兼容协议；[多模态](../concepts/multimodal.md) Embedding 模型（如 `qwen3-vl-embedding`）不支持 OpenAI 接口；`completions` 接口暂不支持后缀生成前缀。

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
- [OpenAI Responses接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-with-openai-responses-api.md)



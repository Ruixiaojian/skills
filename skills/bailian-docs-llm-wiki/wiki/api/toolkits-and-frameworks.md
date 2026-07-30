# toolkits and [frameworks](frameworks.md)

阿里云百炼提供多套 OpenAI 兼容的工具包与框架接口，覆盖文本生成、视觉理解、向量嵌入、批量推理、会话管理等核心场景。开发者可复用现有 OpenAI SDK 和生态工具（如 LangChain），仅需调整 `base_url`、`api_key` 和模型名即可快速迁移。所有接口均支持[流式输出](../concepts/streaming-output.md)、[函数调用](../concepts/function-calling.md)、上下文管理等关键能力，并针对不同地域提供业务空间专属域名以提升稳定性。

## 支持的模型/功能

百炼支持的 [OpenAI 兼容接口](../concepts/openai-compatible-interface.md)按功能划分为以下几类：

- **Chat Completions**：通用对话接口，支持 Qwen 系列（`qwen-plus`、`qwen3.7-plus` 等）、Qwen-VL、Qwen-Coder、Qwen-Omni、Qwen-Math，以及第三方直供模型（DeepSeek、Kimi、GLM、MiniMax）[原文标题](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-of-openai-with-dashscope.md)。  
- **Responses API**：增强型智能体原生接口，内置联网搜索、网页抓取、代码解释器等工具，支持 `qwen3.7-max`、`qwen3.7-plus`、`qwen3-coder-plus` 等全系 Qwen3 模型及 `qwen-plus` [原文标题](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-with-openai-responses-api.md)。  
- **Vision API**：视觉理解专用接口，支持 `qwen3-vl-plus`、`QVQ`、`Qwen-OCR`，兼容 OpenAI [多模态](../concepts/multi-modal.md)消息格式（含 `image_url`）[原文标题](../../raw/model-api-reference/toolkits-and-frameworks/qwen-vl-compatible-with-openai.md)。  
- **Embedding API**：文本向量化接口，支持 `text-embedding-v4`（2048维）、`text-embedding-v3`、`text-embedding-v2`，但**[多模态](../concepts/multi-modal.md) Embedding 模型（如 `qwen3-vl-embedding`）不支持 OpenAI 兼容协议** [原文标题](../../raw/model-api-reference/toolkits-and-frameworks/embedding-interfaces-compatible-with-openai.md)。  
- **Conversations API**：会话状态管理接口，用于跨设备/长时间中断的上下文持久化，支持 `system`/`user`/`assistant`/`developer` 角色及元数据存储 [原文标题](../../raw/model-api-reference/toolkits-and-frameworks/openai-compatible-conversations.md)。  
- **Batch Chat / Batch File**：异步批量处理接口，适用于数据标注、评测等非实时场景，支持 `qwen3.7-max`、`qwen3.5-omni-plus` 等模型，单次请求上下文最大 256K tokens [原文标题](../../raw/model-api-reference/toolkits-and-frameworks/openai-compatible-batch-chat.md)。  
- **Files API**：文件上传与管理接口，用途包括文档分析（`purpose="file-extract"`）、批量任务输入（`purpose="batch"`）、模型调优（`purpose="fine-tune"`）[原文标题](../../raw/model-api-reference/toolkits-and-frameworks/openai-file-interface.md)。  
- **Completions API**：纯文本补全接口，当前仅支持 `qwen-coder-turbo`，适用于代码续写、函数体生成等场景 [原文标题](../../raw/model-api-reference/toolkits-and-frameworks/completions.md)。

> **注意**：`Qwen-Audio` 明确不支持 OpenAI 兼容协议，仅支持 DashScope 原生协议；而 `qwen3.5-omni-plus` 在 Batch 场景下不支持语音输出，与文档 5 和文档 9 的描述一致，无矛盾。

## 关键参数

所有 [OpenAI 兼容接口](../concepts/openai-compatible-interface.md)共用以下核心参数：

- `model`：必需，模型名称（如 `"qwen3.7-plus"`）。不同接口支持的模型列表差异较大，需严格对照各文档确认。  
- `base_url`：必需，服务端点。**强烈建议使用业务空间专属域名**（如 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`），而非旧版 `https://dashscope.aliyuncs.com`，以获得更高性能和稳定性 [原文标题](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-of-openai-with-dashscope.md)。  
- `api_key`：必需，需配置为环境变量 `DASHSCOPE_API_KEY` 或显式传入（不推荐硬编码）。  
- `stream`：布尔值，默认 `false`。设为 `true` 启用[流式输出](../concepts/streaming-output.md)，配合 `stream_options={"include_usage": true}` 可在末尾返回 token 统计。  
- `temperature` / `top_p`：二选一控制生成多样性，避免同时设置。  
- `max_tokens`：限制输出长度，超限将截断，不影响模型内部生成逻辑。  
- `stop`：字符串或数组，指定停止生成的触发词。  
- `seed`：整数，设置后可提升结果确定性。  

此外：
- **Responses API** 特有 `previous_response_id`（用于多轮上下文关联）和 `input`（支持纯字符串输入，无需 `messages` 数组）[原文标题](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-with-openai-responses-api.md)。  
- **Batch 接口** 特有 `enable_thinking`（控制是否启用思考模式，影响 token 成本）且必须作为 JSONL `body` 的顶层字段 [原文标题](../../raw/model-api-reference/toolkits-and-frameworks/openai-compatible-batch-chat.md)。  
- **Embedding API** 特有 `dimensions`（仅 `v3`/`v4` 支持）和 `encoding_format`（`"float"` 或 `"base64"`）。  
- **Files API** 特有 `purpose`（`"file-extract"`/`"batch"`/`"fine-tune"`），决定文件用途及格式约束。

## 使用方式

### SDK 调用（推荐）
1. 安装对应 SDK：`pip install -U openai`（基础）、`pip install langchain_openai`（LangChain 集成）或 `pip install dashscope langchain-community`（原生百炼集成）。  
2. 初始化客户端时指定 `base_url` 和 `api_key`：  
   ```python
   from openai import OpenAI
   client = OpenAI(
       api_key=os.getenv("DASHSCOPE_API_KEY"),
       base_url="https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1"
   )
   ```
3. 根据接口类型调用对应方法：  
   - Chat：`client.chat.completions.create(...)`  
   - Responses：`client.responses.create(...)`  
   - Embeddings：`client.embeddings.create(...)`  
   - Conversations：`client.conversations.create(...)`  
   - Files：`client.files.create(file=..., purpose="...")`  
   - Batches：`client.batches.create(input_file_id=..., endpoint="/v1/chat/completions", ...)`  

### HTTP 调用
直接构造 POST 请求，URL 为 `base_url + /{endpoint}`，例如：  
- Chat：`POST https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1/chat/completions`  
- Embeddings：`POST https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1/embeddings`  
- Files：`POST https://dashscope.aliyuncs.com/compatible-mode/v1/files`（注意 Files API 当前仍使用通用域名）  

### LangChain 集成
- 使用 `langchain_openai.ChatOpenAI` 适配 OpenAI 兼容模型（支持子集）；  
- 使用 `langchain_community.chat_models.tongyi.ChatTongyi` 适配全部百炼模型（需 `dashscope` SDK）[原文标题](../../raw/model-api-reference/toolkits-and-frameworks/use-bailian-in-langchain.md)。  

## 限制和注意事项

- **地域与域名**：北京、新加坡地域已推出业务空间专属域名（`{WorkspaceId}.cn-beijing.maas.aliyuncs.com`），**强烈建议迁移**；弗吉尼亚、东京、法兰克福等地域暂未提供专属域名，仍使用 `dashscope-us.aliyuncs.com` 等通用地址。旧域名（`dashscope.aliyuncs.com`）虽仍可用，但性能与稳定性较低。  
- **模型兼容性**：  
  - `Qwen-Audio` 不支持 OpenAI 协议，仅 DashScope 协议可用；  
  - `Qwen-VL` 等视觉模型需使用 `messages` 中 `image_url` 字段，且 `qwen3-vl-plus` 支持流式，`QVQ` 仅支持流式 [原文标题](../../raw/model-api-reference/toolkits-and-frameworks/qwen-vl-compatible-with-openai.md)；  
  - `completions` 接口当前仅支持 `qwen-coder-turbo`，不支持其他模型。  
- **Batch 限制**：  
  - 最长等待时间 3600 秒（1 小时），超时将断开连接；  
  - `qwen3.5-omni-plus` 在 Batch 场景下不支持语音输出；  
  - `enable_thinking` 参数必须置于 JSONL `body` 顶层，不可嵌套在 `extra_body` 中。  
- **Files API 限制**：  
  - `file-extract`：单文件 ≤ 150 MB，支持 TXT/DOCX/PDF 等；  
  - `batch`：单文件 ≤ 500 MB，必须为 JSONL 格式；  
  - `fine-tune`：单文件 ≤ 300 MB，必须为 JSONL 格式。  
- **安全实践**：API Key **必须通过环境变量配置**（如 `DASHSCOPE_API_KEY`），禁止硬编码在源码中；生产环境应启用密钥轮换与访问控制。  
- **错误处理**：所有接口均遵循 OpenAI 错误码规范（如 `invalid_api_key`、`rate_limit_exceeded`），具体含义参见[错误码文档](https://help.aliyun.com/zh/model-studio/error-code)。

## 来源文档

- [OpenAI Chat接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-of-openai-with-dashscope.md)
- [OpenAI Responses接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-with-openai-responses-api.md)
- [OpenAI Vision接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/qwen-vl-compatible-with-openai.md)
- [completions 接口](../../raw/model-api-reference/toolkits-and-frameworks/completions.md)
- [OpenAI兼容-Batch Chat](../../raw/model-api-reference/toolkits-and-frameworks/openai-compatible-batch-chat.md)
- [OpenAI文件接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/openai-file-interface.md)
- [OpenAI Embedding接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/embedding-interfaces-compatible-with-openai.md)
- [OpenAI Conversations接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/openai-compatible-conversations.md)
- [OpenAI兼容-Batch（文件输入）](../../raw/model-api-reference/toolkits-and-frameworks/batch-interfaces-compatible-with-openai.md)
- [在LangChain中使用阿里云百炼](../../raw/model-api-reference/toolkits-and-frameworks/use-bailian-in-langchain.md)



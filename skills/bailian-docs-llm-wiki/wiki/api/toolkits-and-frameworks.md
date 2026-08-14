# toolkits and [frameworks](frameworks.md)

阿里云百炼提供多种 OpenAI 兼容的工具包与框架接口，支持开发者无缝迁移现有应用。核心能力覆盖文本生成（Chat、Completions、Responses）、多模态理解（Vision）、[向量嵌入](../concepts/embedding.md)（Embedding）、文件管理（Files）、批量处理（Batch）、会话管理（Conversations）等场景，所有接口均通过统一的 `compatible-mode/v1` 路径暴露，并支持主流 SDK（OpenAI、LangChain 等）。

## 支持的模型/功能

百炼支持的 [OpenAI 兼容接口](../concepts/openai-compatible-api.md)按功能划分为以下几类：

- **Chat Completions**：兼容标准 `chat/completions` 接口，支持 Qwen 系列（如 `qwen-plus`、`qwen3.8-max`）、Qwen-VL、Qwen-Coder、Qwen-Omni、DeepSeek（阿里云直供/硅基流动直供）、Kimi、GLM、MiniMax 等模型；但需注意 **Qwen-Audio 不支持 OpenAI 兼容协议**，仅支持 DashScope 原生协议 [原文标题](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-of-openai-with-dashscope.md)。  
- **Completions**：专用于文本补全，当前仅支持 `qwen-coder-turbo` 模型，适用于代码生成、内容续写等场景 [原文标题](../../raw/model-api-reference/toolkits-and-frameworks/completions.md)。  
- **Responses API**：作为 Chat Completions 的演进版，内置联网搜索、网页抓取、代码解释器等智能体原生能力，支持更灵活的字符串输入与 `previous_response_id` 上下文自动关联，适用于复杂任务链路 [原文标题](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-with-openai-responses-api.md)。  
- **Vision**：支持 `qwen3-vl-plus`、`QVQ`、`Qwen-OCR` 等视觉模型，兼容 `image_url` 类型消息，其中 **QVQ 仅支持[流式输出](../concepts/streaming-output.md)** [原文标题](../../raw/model-api-reference/toolkits-and-frameworks/qwen-vl-compatible-with-openai.md)。  
- **Embedding**：支持 `text-embedding-v1` 至 `v4` 系列文本向量模型，但 **多模态 Embedding 模型（如 `qwen3-vl-embedding`）不支持 [OpenAI 兼容接口](../concepts/openai-compatible-api.md)**，需使用专用多模态向量 API [原文标题](../../raw/model-api-reference/toolkits-and-frameworks/embedding-interfaces-compatible-with-openai.md)。  
- **Files**：用于上传文档（`purpose=file-extract`）、批量任务输入（`purpose=batch`）或调优数据集（`purpose=fine-tune`），支持 TXT/DOCX/PDF/图片等格式，单文件上限 150 MB（文档分析）或 500 MB（Batch） [原文标题](../../raw/model-api-reference/toolkits-and-frameworks/openai-file-interface.md)。  
- **Batch**：分两类：  
  - *文件批量*（`/files` + `/batches`）：异步处理 JSONL 文件，支持千问 Max/Plus/Flash、Qwen-VL 等数十种模型，成本为实时调用的 50% [原文标题](../../raw/model-api-reference/toolkits-and-frameworks/batch-interfaces-compatible-with-openai.md)；  
  - *同步 Batch Chat*（`/chat/completions` with `batch.dashscope.aliyuncs.com`）：单请求同步等待，适用于数据标注等非实时场景，同样享 5 折优惠 [原文标题](../../raw/model-api-reference/toolkits-and-frameworks/openai-compatible-batch-chat.md)。  
- **Conversations**：管理长期对话状态，支持创建、查询、更新、删除会话及追加消息项，配合 Responses API 实现跨设备上下文延续 [原文标题](../../raw/model-api-reference/toolkits-and-frameworks/openai-compatible-conversations.md)。

> **注意**：文档 6 与文档 7 对 `qwen3.5-omni-plus` 的支持描述存在矛盾——文档 6 明确指出该模型“不支持语音输出”，而文档 7 未提及此限制；实际使用中应以文档 6 为准，避免在 Batch 场景下依赖其语音能力。

## 关键参数

各接口共性关键参数如下（部分为 OpenAI 标准参数，部分为百炼扩展）：

- **`base_url`**：必须配置为业务空间专属域名（推荐）或通用域名。  
  - 业务空间专属（性能/稳定性更优）：`https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`（北京）、`https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/compatible-mode/v1`（新加坡）等；  
  - 通用域名（兼容性兜底）：`https://dashscope.aliyuncs.com/compatible-mode/v1`（北京）、`https://dashscope-intl.aliyuncs.com/compatible-mode/v1`（新加坡）等。  
  `{WorkspaceId}` 需从控制台「业务空间详情」获取，旧域名（如 `dashscope.aliyuncs.com`）虽仍可用，但官方强烈建议迁移 [原文标题](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-of-openai-with-dashscope.md)。  

- **`model`**：严格区分大小写，须与百炼控制台模型市场名称一致（如 `qwen3-vl-plus`，非 `qwen-vl-plus`）。第三方模型（如 DeepSeek）需先在控制台开通对应服务。  

- **`stream` & `stream_options`**：  
  - `stream=true` 启用[流式输出](../concepts/streaming-output.md)；  
  - `stream_options={"include_usage": true}` 可在流式最后一 chunk 返回 token 统计。  

- **`enable_thinking`**（Batch 场景特有）：控制是否启用思考模式（产生额外 reasoning tokens）。`qwen3.5+` 系列默认开启，**必须作为 `body` 顶层参数传入，不可置于 `extra_body` 内**，否则无效 [原文标题](../../raw/model-api-reference/toolkits-and-frameworks/batch-interfaces-compatible-with-openai.md)。  

- **`dimensions`**（Embedding 特有）：仅 `text-embedding-v3` 和 `v4` 支持，用于指定向量维度（如 `1024`）。  

- **`previous_response_id`**（Responses API 特有）：传入上一轮响应的顶层 `id`（UUID 格式），而非 `output` 数组内消息的 `id`，用于自动上下文关联。  

- **`purpose`**（Files API 特有）：决定文件用途，值为 `file-extract`（文档分析）、`batch`（批量推理）、`fine-tune`（模型调优），不同 purpose 对文件格式与大小限制不同。

## 使用方式

### SDK 调用（推荐）

1. **安装依赖**：  
   - OpenAI SDK：`pip install -U openai`（Python）、`npm install openai`（Node.js）；  
   - LangChain：`pip install langchain_openai`（Python）或 `npm install @langchain/openai`（JS），亦可选用 `langchain-community` + `dashscope` 获取全模型支持 [原文标题](../../raw/model-api-reference/toolkits-and-frameworks/use-bailian-in-langchain.md)。  

2. **初始化客户端**：  
   ```python
   from openai import OpenAI
   client = OpenAI(
       api_key=os.getenv("DASHSCOPE_API_KEY"),  # 强烈建议配置环境变量
       base_url="https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1"
   )
   ```

3. **调用示例**：  
   - Chat：`client.chat.completions.create(model="qwen-plus", messages=[...])`；  
   - Completions：`client.completions.create(model="qwen-coder-turbo", prompt="<tool_call>...<tool_call>")`；  
   - Responses：`client.responses.create(model="qwen3.8-max", input="你好")`；  
   - Files：`client.files.create(file=Path("doc.pdf"), purpose="file-extract")`；  
   - Batch（文件）：`client.batches.create(input_file_id="file-batch-xxx", endpoint="/v1/chat/completions", completion_window="24h")`；  
   - Batch（同步）：将 `base_url` 改为 `"https://batch.dashscope.aliyuncs.com/compatible-mode/v1"` 后调用 `chat.completions.create`；  
   - Conversations：`client.conversations.create(items=[{"role":"system","content":"..."}])`。

### HTTP 直连

构造 `POST` 请求，Header 包含 `Authorization: Bearer $DASHSCOPE_API_KEY` 与 `Content-Type: application/json`，Body 为标准 OpenAI JSON 格式（如 `{"model":"qwen-plus","messages":[...]}`）。Endpoint 依据接口类型选择，例如：  
- Chat：`POST https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1/chat/completions`；  
- Embedding：`POST https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1/embeddings`；  
- Files：`POST https://dashscope.aliyuncs.com/compatible-mode/v1/files`（注意此处仍用通用域名）。

## 限制和注意事项

- **地域与模型绑定**：部分模型仅在特定地域可用（如 DeepSeek-V4 仅支持北京与新加坡），且三方直供模型（如 SiliconFlow DeepSeek）**仅在中国站内地地域可用**，调用前需在控制台开通 [原文标题](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-of-openai-with-dashscope.md)。  
- **文件配额**：百炼存储空间上限为 **10,000 个文件** 或 **总大小 100 GB**，超限后上传失败，需手动清理旧文件释放配额 [原文标题](../../raw/model-api-reference/toolkits-and-frameworks/openai-file-interface.md)。  
- **[Token](../concepts/token.md) 限制**：  
  - `qwen3.5+` 系列模型在 Batch 场景下单次请求上下文最大支持 **256K tokens**；  
  - `completions` 接口的 `max_tokens` 仅控制返回截断，**不影响模型实际生成长度**，若生成超限将被截断 [原文标题](../../raw/model-api-reference/toolkits-and-frameworks/completions.md)。  
- **API Key 隔离**：北京与新加坡地域的 API Key **不通用**，切换地域时必须更换对应 Key，否则鉴权失败。  
- **路径弃用预警**：`/api/v2/apps/protocols/compatible-mode/v1/responses` 和 `/api/v2/apps/protocols/compatible-mode/v1/conversations` 等旧路径 **即将停止维护**，必须迁移至 `/compatible-mode/v1/responses` 和 `/compatible-mode/v1/conversations` [原文标题](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-with-openai-responses-api.md)。  
- **LangChain 兼容性差异**：`langchain_openai` 仅支持百炼部分模型（如 `qwen-plus`），若需调用全部模型（如 `qwen-long`）或使用原生功能（如长上下文），应选用 `langchain-community` + `dashscope` 方案 [原文标题](../../raw/model-api-reference/toolkits-and-frameworks/use-bailian-in-langchain.md)。

## 来源文档

- [OpenAI Chat接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-of-openai-with-dashscope.md)
- [completions 接口](../../raw/model-api-reference/toolkits-and-frameworks/completions.md)
- [OpenAI Responses接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-with-openai-responses-api.md)
- [OpenAI文件接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/openai-file-interface.md)
- [OpenAI Vision接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/qwen-vl-compatible-with-openai.md)
- [OpenAI兼容-Batch（文件输入）](../../raw/model-api-reference/toolkits-and-frameworks/batch-interfaces-compatible-with-openai.md)
- [OpenAI兼容-Batch Chat](../../raw/model-api-reference/toolkits-and-frameworks/openai-compatible-batch-chat.md)
- [OpenAI Conversations接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/openai-compatible-conversations.md)
- [OpenAI Embedding接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/embedding-interfaces-compatible-with-openai.md)
- [在LangChain中使用阿里云百炼](../../raw/model-api-reference/toolkits-and-frameworks/use-bailian-in-langchain.md)



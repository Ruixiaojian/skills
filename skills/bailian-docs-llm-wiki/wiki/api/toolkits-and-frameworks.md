# toolkits and [frameworks](frameworks.md)

阿里云百炼提供多种 [OpenAI 兼容接口](../concepts/openai-compatible-interface.md)及专用工具链，支持开发者快速迁移现有应用或构建新场景。所有接口均基于统一的 `compatible-mode/v1` 协议层，通过调整 `base_url`、`api_key` 和 `model` 三要素即可接入，无需重写核心逻辑。各接口在功能定位、模型支持和使用约束上存在明确分工，需按场景选型。

## 支持的模型/功能

百炼支持的 OpenAI 兼容能力覆盖文本、视觉、向量、文件与对话管理等维度：

- **Chat Completions**：通用对话接口，支持 `qwen-plus`、`qwen3-*` 系列、`Qwen-VL`、`Qwen-Coder`、`DeepSeek`（三方直供）、`Kimi`、`GLM`、`MiniMax` 等模型，但 **Qwen-Audio 不支持该协议** [原文标题](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-of-openai-with-dashscope.md)。  
- **Responses API**：面向智能体的演进接口，内置联网搜索、网页抓取等工具，支持 `qwen3.7-plus`、`qwen3-coder-*` 等数十个 `qwen3-*` 模型，**不支持 `qwen-coder-turbo` 等旧版 coder 模型** [原文标题](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-with-openai-responses-api.md)。  
- **Completions**：专用于代码/文本补全，**当前仅支持 `qwen-coder-turbo`**，且仅限北京地域 [原文标题](../../raw/model-api-reference/toolkits-and-frameworks/completions.md)。  
- **Vision**：多模态理解接口，支持 `Qwen-VL`、`QVQ`、`Qwen-OCR`，其中 **QVQ 仅支持[流式输出](../concepts/streaming-output.md)** [原文标题](../../raw/model-api-reference/toolkits-and-frameworks/qwen-vl-compatible-with-openai.md)。  
- **Embedding**：文本向量化接口，支持 `text-embedding-v1` 至 `v4`，**多模态 Embedding 模型（如 `qwen3-vl-embedding`）不兼容 OpenAI 接口** [原文标题](../../raw/model-api-reference/toolkits-and-frameworks/embedding-interfaces-compatible-with-openai.md)。  
- **Files**：文件上传与管理，用途包括文档问答（`file-extract`）、批量推理（`batch`）和模型调优（`fine-tune`），单文件上限依用途而异（150 MB / 500 MB / 300 MB） [原文标题](../../raw/model-api-reference/toolkits-and-frameworks/openai-file-interface.md)。  
- **Batch**：异步批量处理，支持两种模式：  
  - 文件输入（JSONL 格式）：适用于大规模任务，费用为实时调用的 50%；  
  - Batch Chat（同步阻塞）：单请求模式，保持实时 API 调用习惯，同样享 5 折优惠 [原文标题](../../raw/model-api-reference/toolkits-and-frameworks/openai-compatible-batch-chat.md)。  
- **Conversations**：会话状态管理，配合 Responses API 实现跨设备上下文延续，支持创建、查询、更新、删除会话及添加消息项 [原文标题](../../raw/model-api-reference/toolkits-and-frameworks/openai-compatible-conversations.md)。

> **注意**：文档 6（Batch 文件输入）与文档 7（Batch Chat）对同一模型（如 `qwen-plus`）的适用性描述存在差异——前者明确列出 `qwen-plus` 在华北2（北京）可用，后者亦将其列入支持列表，但文档 7 的“适用范围”小节未注明地域限制，而文档 6 明确要求中国内地使用 `https://dashscope.aliyuncs.com`，国际使用 `https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com`。实际使用时，**Batch Chat 必须使用专用域名 `https://batch.dashscope.aliyuncs.com`**，与常规 Batch 文件接口的域名不同，此为关键区别。

## 关键参数

所有 [OpenAI 兼容接口](../concepts/openai-compatible-interface.md)共用以下核心参数，部分接口有扩展：

- `base_url`：必须配置，不同接口/地域有严格对应关系：  
  - Chat/Responses/Vision/Embedding/Conversations：`https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`（北京）、`https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/compatible-mode/v1`（新加坡）等；  
  - Files/Batch（文件输入）：`https://dashscope.aliyuncs.com/compatible-mode/v1`（中国内地）或 `https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/compatible-mode/v1`（国际）；  
  - Batch Chat：**必须使用 `https://batch.dashscope.aliyuncs.com/compatible-mode/v1`**，与其他接口域名隔离。  
- `model`：模型名称需严格匹配支持列表，例如 `qwen3.7-plus`（Responses）、`qwen-coder-turbo`（Completions）、`text-embedding-v4`（Embedding）。  
- `api_key`：需与 `base_url` 所属地域一致（如北京地域 API Key 不能用于新加坡 endpoint）。  
- `stream`：布尔值，控制是否流式返回，默认 `false`；Vision 接口的 `QVQ` 模型强制流式。  
- `stream_options`：当 `stream=true` 时，设 `{"include_usage": true}` 可在最后一 chunk 返回 token 统计。  
- `enable_thinking`：仅 Batch 场景下有效，控制思考模式开关（`true`/`false`），需作为 JSONL `body` 的顶层字段，**不可置于 `extra_body` 内**。  
- `previous_response_id`（Responses API）：用于多轮对话，传入上一轮响应的顶层 `id`（UUID 格式），非 `output` 中 `msg_*` ID。  
- `purpose`（Files API）：必需字段，取值 `file-extract`、`batch` 或 `fine-tune`，决定文件用途及格式校验规则。

## 使用方式

### 基础调用流程
1. **获取并配置凭证**：在百炼控制台获取对应地域的 API Key，并推荐配置至环境变量 `DASHSCOPE_API_KEY`。  
2. **初始化客户端**：使用 OpenAI SDK（Python/Node.js/Java/Go/C#）或 HTTP 客户端，设置 `base_url` 和 `api_key`。  
3. **构造请求**：按接口规范传入 `model`、输入内容（如 `messages`、`input`、`prompt`、`file`）及其他参数。  
4. **处理响应**：解析 JSON 结构，注意 `choices[0].message.content`（Chat）、`output_text`（Responses）、`data[0].embedding`（Embedding）等字段差异。

### 典型示例
- **Chat Completions（非流式）**：
  ```python
  from openai import OpenAI
  client = OpenAI(api_key=os.getenv("DASHSCOPE_API_KEY"), 
                  base_url="https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1")
  resp = client.chat.completions.create(model="qwen-plus", messages=[{"role":"user","content":"你好"}])
  print(resp.choices[0].message.content)
  ```
- **Responses API（多轮）**：
  ```python
  resp1 = client.responses.create(model="qwen3.7-plus", input="我的名字是张三")
  resp2 = client.responses.create(model="qwen3.7-plus", input="你还记得我的名字吗？", 
                                  previous_response_id=resp1.id)  # 注意传顶层 id
  ```
- **Files API（上传）**：
  ```python
  file_obj = client.files.create(file=Path("doc.pdf"), purpose="file-extract")  # 用于 Qwen-Long/Qwen-Doc-Turbo
  ```
- **Batch Chat（同步）**：
  ```python
  client = OpenAI(..., base_url="https://batch.dashscope.aliyuncs.com/compatible-mode/v1").with_options(timeout=1800.0)
  resp = client.chat.completions.create(model="qwen-plus", messages=[...])  # 阻塞等待完成
  ```

### LangChain 集成
- **OpenAI 方式**：使用 `langchain_openai.ChatOpenAI`，仅支持 OpenAI 兼容模型（如 `qwen-plus`），`base_url` 设为 `https://dashscope.aliyuncs.com/compatible-mode/v1`。  
- **DashScope 方式**：使用 `langchain_community.chat_models.tongyi.ChatTongyi`，支持全部百炼文本模型，需安装 `dashscope` 包，`dashscope_api_key` 为凭证字段 [原文标题](../../raw/model-api-reference/toolkits-and-frameworks/use-bailian-in-langchain.md)。

## 限制和注意事项

- **地域与域名绑定**：API Key、`base_url`、模型可用性三者强绑定。例如，北京地域 API Key 无法用于 `dashscope-us.aliyuncs.com`；`qwen3.7-plus` 在 Responses API 中可用，但在 Completions API 中不可用。  
- **业务空间专属域名迁移**：北京、新加坡地域已启用 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com` 等新域名，**旧域名 `https://dashscope.aliyuncs.com` 将逐步停用**，文档 1、2、4、8 均强调此迁移要求。  
- **模型能力差异**：  
  - `Qwen-Audio` 不支持 OpenAI 兼容协议；  
  - `QVQ` 模型强制流式，无非流式选项；  
  - `qwen3.7-*` 系列模型在 Batch 场景默认开启思考模式，需显式设置 `enable_thinking=false` 关闭以控本。  
- **文件服务配额**：Files API 总存储上限 100 GB、最多 10,000 个文件，超限后上传失败，需主动清理。  
- **Batch 超时机制**：Batch Chat 默认等待 3600 秒（1 小时），超时断连；Batch 文件任务最长等待 24 小时，需轮询状态。  
- **安全实践**：**严禁硬编码 API Key**，务必通过环境变量或密钥管理服务注入；SDK 调用时优先使用 `os.getenv("DASHSCOPE_API_KEY")`。

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



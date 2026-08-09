# toolkits and [frameworks](frameworks.md)

阿里云百炼平台提供多种 [OpenAI 兼容接口](../concepts/openai-compatible-interface.md)及配套工具链，支持开发者快速迁移现有应用或构建新模型服务。所有接口均基于统一的 `compatible-mode/v1` 协议层，覆盖文本生成、视觉理解、嵌入向量、批量推理、会话管理、文件处理等核心场景，并兼容主流 SDK（如 OpenAI SDK、LangChain）和编程语言。

## 支持的模型/功能

百炼支持的 OpenAI 兼容能力按功能维度划分如下：

- **Chat Completions**：支持 Qwen 系列（`qwen-plus`、`qwen3-max` 等）、DeepSeek（`deepseek-v4-flash`）、Kimi、GLM、MiniMax 等数十种模型，详见 [OpenAI Chat接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-of-openai-with-dashscope.md)；  
- **Vision（[多模态](../concepts/multimodal.md)）**：支持 `qwen-vl-plus`、`qwen3-vl-plus`、`QVQ`、`qwen-vl-ocr` 等视觉模型，支持 `image_url` 格式输入与流式响应；  
- **Embeddings**：支持 `text-embedding-v1` 至 `v4` 全系列文本向量模型，支持 `dimensions` 参数动态指定向量维度（仅 v3/v4），但[多模态 Embedding 模型不支持 OpenAI 兼容接口](../../raw/model-api-reference/toolkits-and-frameworks/embedding-interfaces-compatible-with-openai.md)；  
- **Responses API**：作为 Chat Completions 的演进版，内置联网搜索、网页抓取等智能体原生工具，支持 `previous_response_id` 自动上下文关联，适用于复杂任务编排；  
- **Conversations API**：用于跨设备/长时间对话状态管理，支持创建、查询、更新、删除会话及追加消息项，配合 Responses API 实现无状态上下文延续；  
- **Files API**：支持 `purpose=file-extract`（文档问答）、`purpose=batch`（批量任务输入）、`purpose=fine-tune`（调优数据集上传）三类用途，单文件上限分别为 150 MB / 500 MB / 300 MB；  
- **Batch Chat**：同步阻塞式批量推理接口，支持 `qwen-plus`、`qwen3.7-flash` 等主流模型，最大上下文达 256K tokens；  
- **Batch File（JSONL）**：异步批量提交接口，支持文本、[多模态](../concepts/multimodal.md)、Embedding 等全类型模型，费用为实时调用的 50%；  
- **Completions（补全）**：专用于代码补全等场景，当前仅支持 `qwen-coder-turbo` 模型，且[暂不支持后缀生成前缀](../../raw/model-api-reference/toolkits-and-frameworks/completions.md)。

> **注意**：文档 1 和文档 3 均声明 Qwen-VL 支持 OpenAI Vision 接口，但文档 1 明确指出 *“Qwen-Audio 不支持 OpenAI 兼容协议”*，而文档 3 未提及音频模型兼容性——该信息缺口需以文档 1 为准，即非文本/图像模态（如音频）不在 OpenAI 兼容范围内。

## 关键参数

| 参数 | 类型 | 说明 | 备注 |
|------|------|------|------|
| `base_url` | string | 服务端点地址 | 必须使用业务空间专属域名（如 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`），旧域名（`dashscope.aliyuncs.com`）虽仍可用但**不推荐**，详见 [OpenAI Chat接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-of-openai-with-dashscope.md)； |
| `model` | string | 模型名称 | 需严格匹配控制台开通的模型名（如 `qwen3-vl-plus`），三方直供模型（如 SiliconFlow DeepSeek）仅在中国内地地域可用； |
| `stream` | boolean | 是否启用[流式输出](../concepts/streaming-output.md) | 默认 `false`；流式响应中需设置 `stream_options={"include_usage": true}` 才能在末尾返回 token 统计； |
| `enable_thinking` | boolean | 控制混合思考模式开关 | 仅 Batch 场景下生效，`qwen3.5+` 系列默认开启，显式设为 `false` 可避免额外 token 成本； |
| `dimensions` | integer | 向量维度 | 仅 `text-embedding-v3`/`v4` 支持，`v1`/`v2` 不支持该参数； |
| `previous_response_id` | string | 上一轮 Responses API 的顶层 `id` | 用于多轮对话上下文自动注入，**不是 `output` 数组内消息的 `id`**，详见 [OpenAI Responses接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-with-openai-responses-api.md)； |

## 使用方式

### 1. SDK 初始化（通用）
```python
from openai import OpenAI
import os

client = OpenAI(
    api_key=os.getenv("DASHSCOPE_API_KEY"),  # 强烈建议配置环境变量
    base_url="https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1"  # 替换为实际 WorkspaceId
)
```

### 2. 接口调用示例
- **Chat**：`client.chat.completions.create(model="qwen-plus", messages=[...])`  
- **Vision**：`messages` 中 `content` 为数组，含 `{"type":"image_url","image_url":{"url":"..."}}` 对象；  
- **Embedding**：`client.embeddings.create(model="text-embedding-v4", input="...", dimensions=1024)`；  
- **Responses**：`client.responses.create(model="qwen3.8-max", input="...")` 或带 `previous_response_id`；  
- **Conversations**：先 `client.conversations.create(items=[...])` 获取 `conv_xxx`，再 `client.conversations.items.create(conversation_id, ...)` 追加消息；  
- **Files**：`client.files.create(file=Path("doc.pdf"), purpose="file-extract")`；  
- **Batch Chat**：`base_url` 切换为 `https://batch.dashscope.aliyuncs.com/compatible-mode/v1`；  
- **Batch File**：上传 JSONL 后调用 `client.batches.create(input_file_id="file-batch-xxx", endpoint="/v1/chat/completions")`。

### 3. LangChain 集成
- **OpenAI 方式**：使用 `langchain_openai.ChatOpenAI`，仅支持部分模型（如 `qwen-plus`），依赖 `base_url` 和 `model`；  
- **DashScope 原生方式**：使用 `langchain_community.chat_models.tongyi.ChatTongyi`，支持全部百炼模型，需 `dashscope_api_key` 参数；  
详情见 [在LangChain中使用阿里云百炼](../../raw/model-api-reference/toolkits-and-frameworks/use-bailian-in-langchain.md)。

## 限制和注意事项

- **地域与域名绑定**：北京/新加坡地域必须使用 `{WorkspaceId}.<region>.maas.aliyuncs.com` 域名；弗吉尼亚、东京、法兰克福等地域使用 `dashscope-us.aliyuncs.com` 等固定域名；旧域名（`dashscope.aliyuncs.com`）已逐步淘汰，[文档 4、7、9 均强调需迁移](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-with-openai-responses-api.md)；  
- **模型可用性差异**：`qwen3.8-max` 在 Batch Chat 中支持 256K 上下文，但在普通 Chat 中受默认 token 限制；`qwen3.5-omni-plus` 在 Batch 场景下不支持语音输出；  
- **文件配额**：`purpose=file-extract` 总存储上限为 100 GB / 10000 文件，超限后上传失败；  
- **超时控制**：Batch Chat 默认等待 3600 秒，需通过 SDK `timeout` 参数或 HTTP `timeout` 头显式设置；  
- **安全实践**：API Key **严禁硬编码**，必须通过环境变量（如 `DASHSCOPE_API_KEY`）注入；  
- **错误处理**：所有接口遵循 OpenAI 错误格式（`{"error":{"code":"invalid_api_key","message":"..."}}`），需统一解析 `error.code`；  
- **版本兼容性**：`/api/v2/apps/protocols/compatible-mode/v1/...` 等旧路径已标记为“即将停止维护”，必须迁移到 `/compatible-mode/v1/...` 新路径。

## 来源文档

- [OpenAI Chat接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-of-openai-with-dashscope.md)
- [completions 接口](../../raw/model-api-reference/toolkits-and-frameworks/completions.md)
- [OpenAI Vision接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/qwen-vl-compatible-with-openai.md)
- [OpenAI Responses接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-with-openai-responses-api.md)
- [OpenAI文件接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/openai-file-interface.md)
- [OpenAI兼容-Batch Chat](../../raw/model-api-reference/toolkits-and-frameworks/openai-compatible-batch-chat.md)
- [OpenAI兼容-Batch（文件输入）](../../raw/model-api-reference/toolkits-and-frameworks/batch-interfaces-compatible-with-openai.md)
- [OpenAI Embedding接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/embedding-interfaces-compatible-with-openai.md)
- [OpenAI Conversations接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/openai-compatible-conversations.md)
- [在LangChain中使用阿里云百炼](../../raw/model-api-reference/toolkits-and-frameworks/use-bailian-in-langchain.md)



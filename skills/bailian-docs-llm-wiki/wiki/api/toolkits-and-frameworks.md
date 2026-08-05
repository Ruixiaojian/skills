# toolkits and [frameworks](frameworks.md)

阿里云百炼提供多套 OpenAI 兼容的工具包与框架接口，覆盖文本生成、视觉理解、嵌入向量、批量处理、文件管理、会话状态管理等核心场景。开发者可复用现有 OpenAI 生态代码（如 SDK、LangChain 集成），仅需调整 `base_url`、`api_key` 和模型名即可快速迁移。所有接口均支持[流式输出](../concepts/streaming-output.md)、[Token](../concepts/token.md) 统计与标准错误码体系。

## 支持的模型/功能

百炼支持的 OpenAI 兼容能力按功能维度划分如下：

- **Chat Completions**：支持 Qwen 系列（`qwen-plus`、`qwen3.7-plus` 等）、Qwen-VL、Qwen-Coder、Qwen-Omni、Qwen-Math 及第三方直供模型（DeepSeek、Kimi、GLM、MiniMax）；但 [Qwen-Audio 不支持 OpenAI 兼容协议](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-of-openai-with-dashscope.md)，仅支持 DashScope 原生协议。
- **Responses API**：专为智能体设计，内置联网搜索、网页抓取、代码解释器等工具，支持更简洁的字符串输入与 `previous_response_id` 上下文自动关联；支持 `qwen3-max`、`qwen3-plus`、`qwen3-flash`、`qwen3-coder` 等全系 Qwen3 模型及 `qwen-plus`。
- **Vision（多模态）**：支持 `qwen-vl-plus`、`qvq`、`qwen-ocr`，兼容 OpenAI 的 `image_url` 结构化消息格式；其中 [QVQ 模型仅支持流式输出](../../raw/model-api-reference/toolkits-and-frameworks/qwen-vl-compatible-with-openai.md)。
- **Embedding**：支持 `text-embedding-v1` 至 `v4` 全系列文本向量模型，含多维度配置（如 `dimensions=1024`），但多模态 Embedding（如 `qwen3-vl-embedding`）**不支持** [OpenAI 兼容接口](../concepts/openai-compatible-interface.md)。
- **Batch 处理**：分为两种模式：
  - **文件批量（Batch File）**：通过 JSONL 文件提交数百至数千请求，适用于评测、标注等离线任务，支持 `qwen3.7-max` 等大上下文模型（单请求最大 256K tokens）；
  - **同步 Batch Chat**：单请求阻塞式调用，语义与实时 Chat API 完全一致，仅端点改为 `https://batch.dashscope.aliyuncs.com/compatible-mode/v1`。
- **Files API**：用于上传文档供 `qwen-long`（长文档问答）、`qwen-doc-turbo`（数据提取）或 Batch 任务使用，`purpose` 参数区分用途（`file-extract` / `batch` / `fine-tune`）。
- **Conversations API**：提供会话生命周期管理（创建、查询、更新、删除）及消息项追加，配合 Responses API 实现跨设备上下文延续。

> **注意**：文档 6 与文档 8 对 `qwen3.7-plus` 等模型在 Batch 场景下的上下文长度描述一致（256K），但文档 2 中 Responses API 的示例响应显示 `input_tokens=49`，未体现该能力上限；实际使用时请以 [OpenAI Responses接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-with-openai-responses-api.md) 文档中“支持的模型”列表为准，并确认模型是否启用长上下文能力。

## 关键参数

所有 [OpenAI 兼容接口](../concepts/openai-compatible-interface.md)共用以下核心参数，行为与 OpenAI 官方一致：

- `model`：必需，模型名称（如 `qwen3.7-plus`、`text-embedding-v4`），需与所选接口支持列表匹配。
- `base_url`：必需，地域专属端点，**必须使用业务空间域名**（如 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`），旧域名（`dashscope.aliyuncs.com`）已不推荐；WorkspaceId 需从控制台获取。
- `api_key`：必需，百炼 API Key，建议通过环境变量（`DASHSCOPE_API_KEY`）配置。
- `stream`：布尔值，控制是否[流式输出](../concepts/streaming-output.md)；流式响应末尾可通过 `stream_options={"include_usage": true}` 返回 [Token](../concepts/token.md) 统计。
- `temperature` / `top_p`：二选一控制生成多样性，避免同时设置。
- `max_tokens`：软限制，超限将截断输出，不影响模型内部生成逻辑。
- `stop`：字符串或数组，指定终止词。
- `seed`：整数，启用确定性输出（相同 seed + 相同输入 → 相同输出）。

此外，特定接口有扩展参数：
- **Responses API**：`input`（字符串或消息数组）、`previous_response_id`（关联上一轮响应 ID）；
- **Batch Chat**：需显式设置客户端超时（如 Python SDK 的 `.with_options(timeout=1800.0)`），默认 3600 秒；
- **Embedding**：`dimensions`（仅 v3/v4 支持）、`encoding_format="float"`；
- **Files API**：`purpose`（`file-extract`/`batch`/`fine-tune`）；
- **Conversations API**：`items`（初始消息）、`metadata`（结构化会话元数据）。

## 使用方式

### 基础调用（Python + OpenAI SDK）
```python
from openai import OpenAI
import os

client = OpenAI(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url="https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1"  # 替换为真实 WorkspaceId
)

# Chat Completions
resp = client.chat.completions.create(model="qwen-plus", messages=[{"role":"user","content":"你好"}])

# Responses API（智能体）
resp = client.responses.create(model="qwen3.7-plus", input="今天天气如何？")

# Embedding
resp = client.embeddings.create(model="text-embedding-v4", input="hello world", dimensions=1024)

# Files upload
file_obj = client.files.create(file=Path("doc.pdf"), purpose="file-extract")
```

### LangChain 集成
- **OpenAI 兼容层**（`langchain_openai`）：仅支持部分模型（如 `qwen-plus`），需配置 `base_url`；详见 [在LangChain中使用阿里云百炼](../../raw/model-api-reference/toolkits-and-frameworks/use-bailian-in-langchain.md)。
- **原生 DashScope 层**（`langchain-community` + `dashscope`）：支持全部百炼模型（含部署模型），推荐用于生产环境。

### HTTP 直调
所有接口均提供标准 RESTful 端点，例如：
- Chat：`POST https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1/chat/completions`
- Embedding：`POST https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1/embeddings`
- Batch File 创建：`POST https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1/batches`

## 限制和注意事项

- **地域与域名**：北京、新加坡地域**必须使用业务空间专属域名**（含 `{WorkspaceId}`），旧域名虽暂可用但性能与稳定性较低；弗吉尼亚、东京、法兰克福等地域暂无业务空间域名，直接使用 `dashscope-us.aliyuncs.com` 等全局域名。
- **模型可用性差异**：同一模型在不同接口中支持情况不同——例如 `qwen-vl-plus` 支持 Vision 接口但不支持 Completions 接口；`qwen-coder-turbo` 仅支持 Completions 接口（见 [completions 接口](../../raw/model-api-reference/toolkits-and-frameworks/completions.md)）；`qwen-audio` 完全不支持 OpenAI 协议。
- **三方模型限制**：DeepSeek、Kimi 等直供模型**仅在中国内地地域可用**，且需在控制台单独开通服务。
- **Batch 与思考模式**：`qwen3.7`/`qwen3.6`/`qwen3.5` 系列模型在 Batch 场景下默认开启思考模式，会产生额外 `reasoning_tokens` 成本；若无需思考，须显式传入 `enable_thinking=false`（作为 `body` 顶层参数，非 `extra_body`）。
- **文件配额**：Files API 总存储上限为 100 GB / 10,000 个文件，无有效期；超限时需手动清理。
- **Conversations 生命周期**：会话 ID（`conv_xxx`）有效期为 7 天，过期后 `previous_response_id` 将失效；会话删除仅移除元数据，不删除关联消息项。

## 来源文档

- [OpenAI Chat接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-of-openai-with-dashscope.md)
- [OpenAI Responses接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-with-openai-responses-api.md)
- [completions 接口](../../raw/model-api-reference/toolkits-and-frameworks/completions.md)
- [OpenAI Vision接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/qwen-vl-compatible-with-openai.md)
- [OpenAI文件接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/openai-file-interface.md)
- [OpenAI兼容-Batch（文件输入）](../../raw/model-api-reference/toolkits-and-frameworks/batch-interfaces-compatible-with-openai.md)
- [OpenAI Conversations接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/openai-compatible-conversations.md)
- [OpenAI兼容-Batch Chat](../../raw/model-api-reference/toolkits-and-frameworks/openai-compatible-batch-chat.md)
- [OpenAI Embedding接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/embedding-interfaces-compatible-with-openai.md)
- [在LangChain中使用阿里云百炼](../../raw/model-api-reference/toolkits-and-frameworks/use-bailian-in-langchain.md)



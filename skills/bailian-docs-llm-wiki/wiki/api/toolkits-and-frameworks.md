# toolkits and [frameworks](frameworks.md)

阿里云百炼提供多套 OpenAI 兼容的工具包与框架接口，覆盖文本生成、视觉理解、向量嵌入、批量推理、文件管理、会话状态管理等核心场景。开发者可复用现有 OpenAI SDK 代码，仅需调整 `base_url`、`api_key` 和模型名即可快速迁移。所有接口均支持主流编程语言（Python/Node.js/Java/Go/C#/HTTP），并可通过业务空间专属域名获得更高性能与稳定性。

## 支持的模型/功能

百炼兼容 OpenAI 的接口体系按功能划分为多个子集，各子集支持的模型存在差异：

- **Chat Completions**（[OpenAI Chat接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-of-openai-with-dashscope.md)）：支持 Qwen 系列（`qwen-plus`, `qwen-flash`, `qwen3-*`）、Qwen-VL、Qwen-Coder、Qwen-Omni、Qwen-Math、DeepSeek（阿里云直供及三方直供）、Kimi、GLM、MiniMax 等；**注意**：Qwen-Audio 明确不支持该协议。
- **Responses API**（[OpenAI Responses接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-with-openai-responses-api.md)）：聚焦智能体原生能力，支持 `qwen3.8-max`、`qwen3.7-plus`、`deepseek-v4-flash`、`glm-5.2` 等新一代模型，内置联网搜索、网页抓取等工具；**注意**：其旧版路径 `/api/v2/apps/protocols/compatible-mode/v1/responses` 已标记为“即将停止维护”，必须迁移到 `/compatible-mode/v1/responses`。
- **Vision**（[OpenAI Vision接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/qwen-vl-compatible-with-openai.md)）：专用于多模态理解，支持 `qwen3-vl-plus`、`QVQ`（仅流式）、`Qwen-OCR`；QVQ 模型强制要求[流式输出](../concepts/streaming-output.md)。
- **Embedding**（[OpenAI Embedding接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/embedding-interfaces-compatible-with-openai.md)）：支持 `text-embedding-v1` 至 `v4` 全系列，其中 `v3`/`v4` 支持 `dimensions` 参数；**注意**：多模态 Embedding 模型（如 `qwen3-vl-embedding`）**不支持** [OpenAI 兼容接口](../concepts/openai-compatible-api.md)，需使用专用多模态向量 API。
- **Completions**（[completions 接口](../../raw/model-api-reference/toolkits-and-frameworks/completions.md)）：面向代码补全等前缀/中缀生成任务，当前**仅支持 `qwen-coder-turbo`**，且仅限华北2（北京）地域。
- **Files**（[OpenAI文件接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/openai-file-interface.md)）：统一文件上传入口，`purpose` 决定用途：`file-extract`（文档分析）、`batch`（批量推理输入）、`fine-tune`（调优数据集）。
- **Batch**（[OpenAI兼容-Batch（文件输入）](../../raw/model-api-reference/toolkits-and-frameworks/batch-interfaces-compatible-with-openai.md) 与 [OpenAI兼容-Batch Chat](../../raw/model-api-reference/toolkits-and-frameworks/openai-compatible-batch-chat.md)）：前者通过 JSONL 文件异步处理大批量请求（成本降50%），后者为单请求同步等待模式（官网限时5折）；两者模型支持范围不同，例如 `qwen3.5-omni-plus` 在 Batch 文件模式下不支持语音输出。
- **Conversations**（[OpenAI Conversations接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/openai-compatible-conversations.md)）：用于跨设备/长时间对话的状态管理，配合 Responses API 实现上下文自动注入；其旧版路径 `/api/v2/apps/protocols/compatible-mode/v1/conversations` 同样已标记为“即将停止维护”。

## 关键参数

所有 [OpenAI 兼容接口](../concepts/openai-compatible-api.md)共用以下核心参数，行为与 OpenAI 官方一致：

- `model`：必需，模型名称（如 `"qwen3.8-max"`），需与所选接口支持列表匹配。
- `base_url`：必需，服务端点。**强烈建议使用业务空间专属域名**（如 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`），而非旧域名 `https://dashscope.aliyuncs.com`；`{WorkspaceId}` 需从控制台获取。
- `api_key`：必需，百炼 API Key，推荐配置为环境变量 `DASHSCOPE_API_KEY`。
- `stream`：布尔值，控制是否[流式输出](../concepts/streaming-output.md)（默认 `false`）；Vision 接口的 QVQ 模型强制 `true`。
- `stream_options`：对象，当 `stream=true` 时，设 `{"include_usage": true}` 可在流末尾返回 token 统计。
- `max_tokens`、`temperature`、`top_p`、`stop`、`seed`、`presence_penalty`：通用采样与截断参数，语义与 OpenAI 一致（详见 [completions 接口](../../raw/model-api-reference/toolkits-and-frameworks/completions.md) 文档）。

此外，特定接口有扩展参数：
- **Responses API**：`input`（字符串或消息数组）、`previous_response_id`（用于多轮上下文关联）。
- **Batch Chat**：需将 `base_url` 设为 `https://batch.dashscope.aliyuncs.com/compatible-mode/v1`，并设置客户端超时（最长 3600 秒）。
- **Embedding**：`dimensions`（仅 `v3`/`v4` 支持）、`encoding_format`（`"float"` 或 `"base64"`）。
- **Conversations**：`items`（初始消息）、`metadata`（结构化元数据）。

## 使用方式

### 基础调用（Python + OpenAI SDK）
```python
from openai import OpenAI
import os

client = OpenAI(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url="https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1",  # 替换为实际 WorkspaceId
)

# Chat Completions
response = client.chat.completions.create(
    model="qwen-plus",
    messages=[{"role": "user", "content": "你好"}]
)

# Responses API
response = client.responses.create(
    model="qwen3.8-max",
    input="你能做什么？"
)

# Embedding
response = client.embeddings.create(
    model="text-embedding-v4",
    input="测试文本"
)
```

### LangChain 集成
- **OpenAI 兼容层**（`langchain_openai`）：支持部分模型，配置简单，适用于快速验证：
  ```python
  from langchain_openai import ChatOpenAI
  llm = ChatOpenAI(
      api_key=os.getenv("DASHSCOPE_API_KEY"),
      base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
      model="qwen-plus"
  )
  ```
- **DashScope 原生层**（`langchain-community` + `dashscope`）：支持全部百炼模型及高级特性（如多模态、工具调用）：
  ```python
  from langchain_community.chat_models.tongyi import ChatTongyi
  llm = ChatTongyi(
      model="qwen-plus",
      dashscope_api_key=os.getenv("DASHSCOPE_API_KEY")
  )
  ```

### HTTP 调用（curl 示例）
```bash
# Chat Completions
curl -X POST https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1/chat/completions \
  -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"model":"qwen-plus","messages":[{"role":"user","content":"你好"}]}'

# Files upload
curl -X POST https://dashscope.aliyuncs.com/compatible-mode/v1/files \
  -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
  --form 'file=@"test.txt"' \
  --form 'purpose="file-extract"'
```

## 限制和注意事项

- **地域与模型绑定**：`deepseek-v4` 系列模型仅支持华北2（北京）与新加坡地域；`qwen3.5-omni-plus` 在 Batch 场景下不支持语音输出；`qwen-coder-turbo` 仅支持华北2（北京）地域。
- **域名迁移强制性**：[OpenAI 兼容接口](../concepts/openai-compatible-api.md)的旧版路径（如 `/api/v2/apps/protocols/...`）和旧域名（如 `https://dashscope.aliyuncs.com`）虽仍可用，但官方明确要求迁移至业务空间专属域名（`https://{WorkspaceId}.<region>.maas.aliyuncs.com`）以保障性能与稳定性。
- **功能缺失与例外**：
  - Qwen-Audio 不支持任何 OpenAI 兼容协议，仅支持 DashScope 原生协议。
  - 多模态 Embedding 模型（`qwen3-vl-embedding` 等）不兼容 OpenAI Embedding 接口。
  - QVQ 模型仅支持[流式输出](../concepts/streaming-output.md)，非流式调用将失败。
- **配额与容量**：文件服务总存储上限为 100 GB / 10,000 个文件；Batch 文件单个最大 500 MB；Embedding 单行最大 Token 数因模型而异（如 `text-embedding-v4` 为 8192）。
- **安全实践**：API Key **严禁硬编码**，必须通过环境变量（如 `DASHSCOPE_API_KEY`）注入；生产环境应启用业务空间专属域名以隔离租户流量。

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



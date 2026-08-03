# toolkits and [frameworks](frameworks.md)

阿里云百炼平台提供多种 OpenAI 兼容的工具包与框架接口，支持开发者无缝迁移现有应用。核心能力覆盖文本生成（Chat、Completions、Responses）、多模态理解（Vision）、向量嵌入（Embedding）、批量处理（Batch）、会话管理（Conversations）及文件操作（Files），并兼容主流开发框架如 LangChain。所有接口均基于统一的 `compatible-mode/v1` 协议层，通过调整 `base_url`、`api_key` 和 `model` 即可快速接入。

## 支持的模型/功能

百炼支持的 [OpenAI 兼容接口](../concepts/openai-compatible-interface.md)按功能划分为以下几类：

- **Chat Completions**：标准对话接口，支持 `qwen-plus`、`qwen-flash`、`qwen3-*` 系列、`Qwen-VL`、`Qwen-Coder`、`DeepSeek`（三方直供）、`Kimi`、`GLM`、`MiniMax` 等模型；但需注意 `Qwen-Audio` 明确不支持该协议 [OpenAI Chat接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-of-openai-with-dashscope.md)。  
- **Responses API**：增强型智能体原生接口，内置联网搜索、网页抓取、代码解释器等工具，支持 `qwen3.7-plus`、`qwen3.5-flash`、`qwen3-coder-plus` 等 30+ 个 `qwen3-*` 模型及 `qwen-plus`、`qwen-flash` [OpenAI Responses接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-with-openai-responses-api.md)。  
- **Vision（多模态）**：专用于图像理解，支持 `Qwen-VL`、`QVQ`、`Qwen-OCR`，其中 `QVQ` 仅支持[流式输出](../concepts/streaming-output.md) [OpenAI Vision接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/qwen-vl-compatible-with-openai.md)。  
- **Embedding**：文本向量化服务，支持 `text-embedding-v1` 至 `v4`，其中 `v3` 和 `v4` 支持 `dimensions` 参数；多模态 Embedding（如 `qwen3-vl-embedding`）**不支持** [OpenAI 兼容接口](../concepts/openai-compatible-interface.md) [OpenAI Embedding接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/embedding-interfaces-compatible-with-openai.md)。  
- **Completions**：面向代码补全场景，当前仅支持 `qwen-coder-turbo` 模型，且**仅限华北2（北京）地域** [completions 接口](../../raw/model-api-reference/toolkits-and-frameworks/completions.md)。  
- **Batch（文件输入）**：异步批量处理，支持 `qwen3.7-max`、`qwen3.7-plus`、`qwen-vl-plus` 等数十个模型，单次请求上下文最大支持 256K tokens [OpenAI兼容-Batch（文件输入）](../../raw/model-api-reference/toolkits-and-frameworks/batch-interfaces-compatible-with-openai.md)。  
- **Batch Chat**：同步式批量调用（单请求），与实时 Chat 接口参数一致，仅需切换 `base_url` 为 `https://batch.{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1` [OpenAI兼容-Batch Chat](../../raw/model-api-reference/toolkits-and-frameworks/openai-compatible-batch-chat.md)。  
- **Conversations**：会话状态管理，支持创建、查询、更新、删除会话及追加消息项，配合 Responses API 实现跨设备上下文延续 [OpenAI Conversations接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/openai-compatible-conversations.md)。  
- **Files**：文件上传与管理，`purpose=file-extract` 用于文档问答（Qwen-Long/Qwen-Doc-Turbo），`purpose=batch` 用于批量任务输入，`purpose=fine-tune` 用于调优数据集 [OpenAI文件接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/openai-file-interface.md)。

> **注意**：文档 1 与文档 2 均强调“建议迁移至业务空间专属域名”，但文档 1 中 `BASE_URL` 示例未包含 `/compatible-mode/v1` 后缀（如 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`），而文档 2 的 `service address` 部分明确写出完整路径。实际使用应以文档 2 的格式为准，即 `https://{WorkspaceId}.<region>.maas.aliyuncs.com/compatible-mode/v1`，否则将导致 404 错误。

## 关键参数

各接口共用以下基础参数，部分接口扩展特定字段：

- **`base_url`**：必须配置，格式为 `https://{WorkspaceId}.<region>.maas.aliyuncs.com/compatible-mode/v1`（北京/新加坡/东京/法兰克福）或 `https://dashscope-us.aliyuncs.com/compatible-mode/v1`（弗吉尼亚）。旧域名（如 `dashscope.aliyuncs.com`）已过时，强烈建议迁移 [OpenAI Chat接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-of-openai-with-dashscope.md)。  
- **`api_key`**：必须配置，需与 `base_url` 所在地域匹配（北京与新加坡 API Key 不互通）。推荐通过环境变量 `DASHSCOPE_API_KEY` 设置，避免硬编码。  
- **`model`**：必须指定，值需严格匹配支持列表中的模型名称（如 `qwen3.7-plus`，非 `qwen-plus-latest`）。  
- **通用可选参数**：`temperature`（[0, 2.0)）、`top_p`（(0,1.0]）、`max_tokens`、`stream`（布尔值）、`stop`（字符串或数组）、`seed`（整数）、`presence_penalty`（[-2.0, 2.0]）——详见 [completions 接口](../../raw/model-api-reference/toolkits-and-frameworks/completions.md) 的输入参数说明。  
- **Responses API 特有参数**：`input`（字符串或消息数组）、`previous_response_id`（用于多轮对话上下文关联）、`tool_choice`（`auto`/`none`/`required`）。  
- **Embedding API 特有参数**：`dimensions`（仅 `text-embedding-v3/v4` 支持）、`encoding_format`（`float` 或 `base64`）。  
- **Batch 相关参数**：`enable_thinking`（`true`/`false`，控制思考 token 计费，须与 `model` 同级传入，不可置于 `extra_body` 内）；`completion_window`（如 `"24h"`）。  
- **Conversations API 特有参数**：`items`（初始消息数组，最多 20 条）、`metadata`（键值对，最多 16 对，key≤64 字符，value≤512 字符）。

## 使用方式

### SDK 调用（Python 示例）
```python
from openai import OpenAI
import os

client = OpenAI(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url="https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1"  # 替换为实际 WorkspaceId
)

# Chat Completions
resp = client.chat.completions.create(model="qwen-plus", messages=[{"role":"user","content":"你好"}])

# Responses API（推荐用于智能体）
resp = client.responses.create(model="qwen3.7-plus", input="你能做什么？")

# Embedding
resp = client.embeddings.create(model="text-embedding-v4", input="测试文本", dimensions=1024)

# Batch Chat（同步等待）
client = client.with_options(timeout=1800.0)  # 设置最长等待时间（秒）
resp = client.chat.completions.create(model="qwen-plus", messages=[{"role":"user","content":"你好"}])
```

### HTTP 调用（curl 示例）
```bash
# Chat Completions
curl -X POST "https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1/chat/completions" \
  -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"model":"qwen-plus","messages":[{"role":"user","content":"你好"}]}'

# Responses API
curl -X POST "https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1/responses" \
  -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"model":"qwen3.7-plus","input":"你能做什么？"}'

# Embedding
curl -X POST "https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1/embeddings" \
  -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"model":"text-embedding-v4","input":"测试文本","dimensions":1024}'
```

### LangChain 集成
- **OpenAI 兼容方式**（支持部分模型）：安装 `langchain_openai`，使用 `ChatOpenAI`，`base_url` 设为 `https://dashscope.aliyuncs.com/compatible-mode/v1`。  
- **DashScope 原生方式**（支持全部模型）：安装 `langchain-community` 和 `dashscope`，使用 `ChatTongyi`，需传入 `dashscope_api_key` [在LangChain中使用阿里云百炼](../../raw/model-api-reference/toolkits-and-frameworks/use-bailian-in-langchain.md)。

## 限制和注意事项

- **地域与 API Key 绑定**：北京、新加坡、弗吉尼亚等地域的 API Key **不可混用**，且北京/新加坡的 `base_url` 必须包含 `WorkspaceId`，弗吉尼亚则固定为 `dashscope-us.aliyuncs.com`。  
- **模型可用性差异**：`Qwen-VL` 在北京/新加坡/东京/弗吉尼亚均支持，但 `QVQ` 仅支持[流式输出](../concepts/streaming-output.md)；`Qwen-Audio` 完全不支持 OpenAI 兼容协议 [OpenAI Chat接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-of-openai-with-dashscope.md)。  
- **Batch 场景特殊限制**：`qwen3.5-omni-plus` 不支持语音输出；`qwen3.7-max` 等长上下文模型在 Batch 中支持 256K tokens，但需显式设置 `enable_thinking` 控制成本 [OpenAI兼容-Batch（文件输入）](../../raw/model-api-reference/toolkits-and-frameworks/batch-interfaces-compatible-with-openai.md)。  
- **Conversations API 迁移要求**：旧路径 `/api/v2/apps/protocols/compatible-mode/v1/conversations` 已废弃，必须使用新版 `/compatible-mode/v1/conversations` [OpenAI Conversations接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/openai-compatible-conversations.md)。  
- **文件大小限制**：`purpose=file-extract` 最大 150 MB；`purpose=batch` 最大 500 MB；`purpose=fine-tune` 最大 300 MB [OpenAI文件接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/openai-file-interface.md)。  
- **超时机制**：Batch Chat 默认超时 3600 秒（1 小时），需通过 SDK `timeout` 参数或 HTTP `timeout` 头显式设置；Responses API 的 `previous_response_id` 有效期为 7 天。

## 来源文档

- [OpenAI Chat接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-of-openai-with-dashscope.md)
- [OpenAI Responses接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-with-openai-responses-api.md)
- [completions 接口](../../raw/model-api-reference/toolkits-and-frameworks/completions.md)
- [OpenAI Vision接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/qwen-vl-compatible-with-openai.md)
- [OpenAI兼容-Batch（文件输入）](../../raw/model-api-reference/toolkits-and-frameworks/batch-interfaces-compatible-with-openai.md)
- [OpenAI文件接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/openai-file-interface.md)
- [OpenAI兼容-Batch Chat](../../raw/model-api-reference/toolkits-and-frameworks/openai-compatible-batch-chat.md)
- [OpenAI Embedding接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/embedding-interfaces-compatible-with-openai.md)
- [OpenAI Conversations接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/openai-compatible-conversations.md)
- [在LangChain中使用阿里云百炼](../../raw/model-api-reference/toolkits-and-frameworks/use-bailian-in-langchain.md)



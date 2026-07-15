# toolkits and [frameworks](frameworks.md)

阿里云百炼平台提供多种 [OpenAI 兼容接口](../concepts/openai-compatible-api.md)及配套工具链，支持开发者快速迁移现有应用或构建新场景。所有接口均基于统一的 `compatible-mode/v1` 协议层，通过调整 `base_url`、`api_key` 和 `model` 三个参数即可接入，无需重写业务逻辑。核心能力覆盖文本生成、视觉理解、向量嵌入、批量处理、会话管理与低代码集成（如 LangChain），适配从单次调用到大规模异步任务的全栈需求。

## 支持的模型/功能

百炼支持的 [OpenAI 兼容接口](../concepts/openai-compatible-api.md)按功能划分为以下几类：

- **Chat Completions**：通用对话接口，支持 `qwen-plus`、`qwen3.7-plus`、`qwen-coder-turbo`、`deepseek-r1`、`kimi`、`glm` 等数十种文本与代码模型；也兼容多模态模型如 `qwen-vl-plus`、`qwen3-vl-plus` [原文标题](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-of-openai-with-dashscope.md)。  
- **Responses API**：面向智能体的增强型接口，内置联网搜索、网页抓取、代码解释器等工具，支持 `qwen3.7-max`、`qwen3.5-plus`、`qwen3-coder-next` 等新一代模型，显著简化复杂任务编排 [原文标题](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-with-openai-responses-api.md)。  
- **Completions**：专用于代码补全与内容续写，当前仅支持 `qwen-coder-turbo` 模型，支持前缀补全与“前缀+后缀”中间生成两种模式 [原文标题](../../raw/model-api-reference/toolkits-and-frameworks/completions.md)。  
- **Vision**：图像理解专用接口，支持 `qwen-vl-plus`、`qwen3-vl-plus`、`QVQ`、`qwen-vl-ocr`，兼容 OpenAI 的 `image_url` 输入格式 [原文标题](../../raw/model-api-reference/toolkits-and-frameworks/qwen-vl-compatible-with-openai.md)。  
- **Embedding**：文本向量化接口，支持 `text-embedding-v4`（2048维）、`v3`、`v2`、`v1` 四代模型，支持 `dimensions` 参数动态指定维度，适用于检索增强（RAG）等场景 [原文标题](../../raw/model-api-reference/toolkits-and-frameworks/embedding-interfaces-compatible-with-openai.md)。  
- **Batch（文件输入）**：异步批量处理接口，支持 `qwen3.7-max`、`qwen3.5-omni-plus`、`qwen-vl-ocr` 等模型，单请求上下文最大支持 256K tokens，费用为实时调用的 50% [原文标题](../../raw/model-api-reference/toolkits-and-frameworks/batch-interfaces-compatible-with-openai.md)。  
- **Conversations**：会话状态管理接口，支持跨设备/长时间中断的上下文持久化，配合 Responses API 实现自动历史注入，避免手动维护消息数组 [原文标题](../../raw/model-api-reference/toolkits-and-frameworks/openai-compatible-conversations.md)。  

> **注意**：文档 5（Batch 文件输入）与文档 7（Batch Chat）存在关键差异——前者为**异步文件提交模式**（需上传 JSONL 文件、轮询状态、下载结果），后者为**同步 HTTP 请求模式**（保持连接等待结果返回，单请求）。二者适用场景不同，不可混用；文档 7 明确声明“本接口仅支持提交单个请求”，而文档 5 支持千级并发请求批量处理。

## 关键参数

所有 [OpenAI 兼容接口](../concepts/openai-compatible-api.md)共享以下核心参数，行为与 OpenAI 官方一致：

| 参数 | 类型 | 说明 |
|------|------|------|
| `model` | string | 必填。模型名称，如 `"qwen3.7-plus"`、`"text-embedding-v4"`。注意：`qwen-audio` 不支持 OpenAI 协议，仅支持 DashScope 原生协议。 |
| `base_url` | string | 必填。服务端点，**必须使用业务空间专属域名**以获得最佳性能与稳定性：<br>• 北京：`https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`<br>• 新加坡：`https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/compatible-mode/v1`<br>• 弗吉尼亚：`https://dashscope-us.aliyuncs.com/compatible-mode/v1`<br>• 法兰克福：`https://{WorkspaceId}.eu-central-1.maas.aliyuncs.com/compatible-mode/v1`<br>• 东京：`https://{WorkspaceId}.ap-northeast-1.maas.aliyuncs.com/compatible-mode/v1` |
| `api_key` | string | 必填。阿里云百炼 API Key，**各地域 Key 不互通**，需按 `base_url` 所在地域分别获取并配置。 |
| `stream` | boolean | 可选。启用[流式输出](../concepts/streaming-output.md)（`true`），适用于长响应或前端实时渲染。 |
| `stream_options` | object | 可选。当 `stream=true` 时，设 `{"include_usage": true}` 可在最后一 chunk 返回 token 统计。 |
| `temperature` / `top_p` | float | 可选。互斥使用，控制生成多样性（`temperature ∈ [0, 2.0)`，`top_p ∈ (0, 1.0]`）。 |
| `max_tokens` | integer | 可选。限制响应最大 token 数，超限将截断（不影响模型内部生成过程）。 |

> **注意**：`enable_thinking` 是 Batch 场景特有参数（见文档 5 和 7），用于显式开关思考模式（影响 token 计费），**必须作为 JSONL `body` 的顶层字段传入，不可置于 `extra_body` 中**。该参数在 Chat Completions 或 Responses 同步接口中无效。

## 使用方式

### 1. SDK 调用（推荐）
安装对应 SDK 并初始化客户端：
```python
from openai import OpenAI
client = OpenAI(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url="https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1"
)
```
- **Chat**：`client.chat.completions.create(model=..., messages=[...])`  
- **Responses**：`client.responses.create(model=..., input="...")`  
- **Completions**：`client.completions.create(model=..., prompt="...")`  
- **Embedding**：`client.embeddings.create(model=..., input="...")`  
- **Batch（文件）**：先 `client.files.create(file=..., purpose="batch")`，再 `client.batches.create(input_file_id=..., endpoint="/v1/chat/completions")`  
- **Conversations**：`client.conversations.create(items=[...])` → 获取 `id` 后用于后续 `responses.create(previous_response_id=...)`  

### 2. LangChain 集成
- **OpenAI 兼容层**（`langchain_openai`）：仅支持部分模型（如 `qwen-plus`），依赖 `base_url` 指向百炼兼容端点 [原文标题](../../raw/model-api-reference/toolkits-and-frameworks/use-bailian-in-langchain.md)。  
- **DashScope 原生层**（`langchain-community` + `dashscope`）：支持全部百炼模型（含部署模型），使用 `ChatTongyi` 类，不依赖 OpenAI 协议。  

### 3. HTTP 直连
构造标准 OpenAI 格式请求：
```bash
curl -X POST https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1/chat/completions \
  -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
        "model": "qwen3.7-plus",
        "messages": [{"role":"user","content":"你好"}]
      }'
```

## 限制和注意事项

- **地域与 Key 绑定**：API Key 与 `base_url` 所属地域强绑定（如北京 Key 不能用于新加坡 `base_url`），且各接口对地域支持不完全一致（例如 `completions` 接口仅支持北京地域）。  
- **域名迁移强制要求**：旧域名 `https://dashscope.aliyuncs.com` 和 `https://dashscope-intl.aliyuncs.com` 已不推荐使用，**所有新项目必须采用 `{WorkspaceId}.xxx.maas.aliyuncs.com` 专属域名**，否则可能遭遇性能下降或未来停服风险。  
- **模型能力差异**：  
  - `Qwen-Audio` 不支持 OpenAI 兼容协议（见文档 1）；  
  - `qwen3.5-omni-plus` 在 Batch 场景下不支持语音输出（文档 5 和 7）；  
  - `QVQ` 模型仅支持[流式输出](../concepts/streaming-output.md)（文档 4）。  
- **Batch 与 Conversations 的协同**：`previous_response_id`（Responses API）与 `conversation_id`（Conversations API）是两个独立的状态管理机制，前者用于单次响应链路，后者用于长期会话存储，不可混用。  
- **文件上传配额**：`purpose=file-extract`（文档分析）单文件上限 150 MB；`purpose=batch`（批量任务）单文件上限 500 MB；`purpose=fine-tune`（调优）单文件上限 300 MB（见文档 6）。  
- **错误处理**：所有接口遵循 OpenAI 错误格式（`{"error": {"code": "...", "message": "..."}}`），具体码表参考[统一错误码文档](https://help.aliyun.com/zh/model-studio/error-code)。

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



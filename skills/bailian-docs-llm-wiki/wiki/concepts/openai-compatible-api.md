# OpenAI 兼容接口

OpenAI 兼容接口是百炼平台提供的一组标准化 API 协议层，严格遵循 OpenAI REST API 的路径、请求/响应结构、参数命名与语义规范（如 `/v1/chat/completions`），使开发者能直接复用 OpenAI SDK（如 `openai>=1.0.0`）或现有代码逻辑调用千问（Qwen）及第三方模型，实现零改造迁移。

## 在百炼平台的不同场景中，这个概念如何使用

OpenAI 兼容接口不是单一接口，而是一套按能力分层的协议集合，覆盖多种模型类型与任务场景：

- **通用对话生成**：通过 `Chat Completions` 接口（`POST /compatible-mode/v1/chat/completions`）调用 `qwen3.7-plus`、`deepseek-r1`、`kimi-k2.7-code` 等文本/代码模型，支持标准 `messages` 格式、流式响应（`stream=true`）和基础采样参数（`temperature`, `top_p`, `max_tokens`）。

- **智能体增强能力**：`Responses API`（同路径但启用特定模型如 `qwen3.7-max`）在兼容基础上内置联网搜索、网页提取、代码解释器等工具链，自动处理工具调用循环，无需客户端手动解析 `tool_calls` 并重发 `tool_result`。

- **多模态理解**：`Vision` 接口（`/v1/chat/completions`）支持 OpenAI 格式的 `image_url` 输入，兼容 `qwen-vl-plus`、`qwen3-vl-plus` 等视觉语言模型，可混合文本与图像消息。

- **向量化与排序**：`Embedding`（`/v1/embeddings`）和 `Rerank`（`/v1/rerank`）接口完全对齐 OpenAI Embedding/Rerank 规范，支持 `dimensions`、`input` 数组、`top_n` 等关键参数，无缝接入 RAG 流水线。

- **批量异步处理**：`Batch` 接口（`/v1/batch`）提供 OpenAI 风格的异步提交能力，适用于高吞吐文本处理，单次支持 256K tokens 上下文。

- **会话状态管理**：`Conversations` 接口（`/v1/conversations`）配合 Responses 使用，实现跨请求的上下文持久化，避免手动拼接 `messages`。

> ⚠️ 注意：并非所有百炼模型都支持 OpenAI 协议——例如 `qwen-audio`、`wan2.6-t2i`（文生图）仅提供 DashScope 原生接口；Qwen3 系列部分高级能力（如 `enable_thinking`）需通过原生 SDK 或 `extra_body` 显式传递，OpenAI 兼容接口默认不透传。

## 关键参数和配置

| 参数 | 类型 | 说明 | 必填 |
|------|------|------|------|
| `model` | string | 模型 ID，如 `qwen3.7-plus`、`text-embedding-v4`、`qwen3-rerank`。**必须与 Base URL 所在地域匹配**（如 `qwen3.7-plus-us` 仅限美国地域）。 | 是 |
| `base_url` | string | 服务端点，**必须使用业务空间专属域名**以保障性能与稳定性：<br>• 北京：`https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`<br>• 新加坡：`https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/compatible-mode/v1`<br>• 弗吉尼亚：`https://dashscope-us.aliyuncs.com/compatible-mode/v1`<br>• 法兰克福/东京：同北京格式，替换对应地域代码 | 是 |
| `api_key` | string | 百炼 API Key，**严格按地域与计费方案隔离**（Token Plan、Coding Plan、按量计费 Key 不互通）。需通过 [API Key 页面](https://bailian.console.aliyun.com/?tab=model#/api-key) 创建并匹配 `base_url` 地域。 | 是 |
| `messages` | array | 对话消息列表，格式为 `[{"role": "user", "content": "..."}]`。`Responses API` 可自动注入历史，但生产环境建议显式传入以确保可控性。 | Chat Completions / Responses / Vision 等需对话场景下必填 |
| `stream` | boolean | 启用流式响应（`true`）。返回 `data: {...}` SSE 格式，每 chunk 含 `delta.content`。 | 否 |
| `stream_options` | object | 当 `stream=true` 时，设 `{"include_usage": true}` 可在末尾 chunk 返回 token 统计（`usage` 字段）。 | 否 |
| `temperature` / `top_p` | float | 控制生成随机性，二者互斥。`temperature ∈ [0, 2.0)`，`top_p ∈ (0, 1.0]`。 | 否 |
| `max_tokens` | integer | 最大输出 token 数，影响响应长度与计费。不同模型有硬上限（如 `qwen3.7-plus` 支持 32K 上下文，实际可用受系统 [prompt](../guides/prompt.md) 占用）。 | 否 |

## 面向开发者，简洁实用

- ✅ **快速上手**：只需三步——获取 API Key → 构造 `base_url`（含 WorkspaceId）→ 用 OpenAI SDK 调用，无需修改业务代码。
- ✅ **灵活切换**：同一套 SDK 可无缝切换 Qwen、DeepSeek、Kimi 等模型，仅需改 `model` 参数。
- ✅ **生产就绪**：推荐使用业务空间专属 `base_url`（而非公共域名），获得更低延迟、更高并发与独立配额。
- ❌ **避坑提示**：
  - 不要混用地域 Key 与 URL（如北京 Key + 美国 URL → 401）；
  - `qwen-audio`、`wan2.6-t2i` 等模型**不支持** OpenAI 协议，请查文档确认模型兼容性；
  - 工具调用（`tools`）在 Chat Completions 中需客户端自行解析并重发，`Responses API` 才支持自动执行；
  - `enable_search`、`enable_thinking` 等 Qwen 特有参数**不在 OpenAI 协议内**，需通过 DashScope SDK 或 `extra_body` 传递。

示例（Python）：
```python
from openai import OpenAI

client = OpenAI(
    api_key="sk-xxx",  # 替换为你的百炼 API Key
    base_url="https://your-workspace-id.cn-beijing.maas.aliyuncs.com/compatible-mode/v1"
)

# 标准对话
resp = client.chat.completions.create(
    model="qwen3.7-plus",
    messages=[{"role": "user", "content": "用 Python 写一个快速排序"}]
)
print(resp.choices[0].message.content)

# 流式响应
for chunk in client.chat.completions.create(
    model="qwen3.7-plus",
    messages=[{"role": "user", "content": "讲个笑话"}],
    stream=True,
    stream_options={"include_usage": True}
):
    if chunk.choices[0].delta.content:
        print(chunk.choices[0].delta.content, end="")
```

## 关联主题页

- [qwen api reference](../api/qwen-api-reference.md)
- [get started with models](../guides/get-started-with-models.md)
- [toolkits and frameworks](../api/toolkits-and-frameworks.md)
- [use chat client or development tool](../guides/use-chat-client-or-development-tool.md)
- [vector and sort](../api/vector-and-sort.md)



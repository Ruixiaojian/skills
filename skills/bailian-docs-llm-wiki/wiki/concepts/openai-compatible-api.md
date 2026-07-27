# OpenAI 兼容接口

OpenAI 兼容接口是百炼平台提供的一套标准化 RESTful API 协议，严格遵循 OpenAI 官方 API 的路径、请求/响应结构、参数命名与语义规范（如 `/v1/chat/completions`），使开发者能复用 OpenAI SDK（如 `openai>=1.0`）、主流 AI 工具（Cursor、Dify、Qwen Code 等）及现有代码逻辑，零改造接入百炼的各类大模型能力。

## 在百炼平台的不同场景中，这个概念如何使用

- **通用文本生成**：通过 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1/chat/completions` 调用 `qwen3.7-plus`、`qwen-max`、`glm-5.2`、`deepseek-v4-pro` 等模型，支持标准 `messages` 输入、`stream` 流式响应和 `tools` [函数调用](function-calling.md)。
- **智能体快速构建**：使用 `Responses API`（同一兼容路径下）——无需显式配置 `tools`，即可自动触发联网搜索、代码解释器等内置工具，适用于 `qwen3-max`、`qwen3-coder` 等模型，大幅简化会话状态管理。
- **多模态理解**：对 `qwen-vl-plus`、`qwen3-vl-flash`、`qvq` 等视觉模型，通过 `messages` 中嵌入 `image_url` 或 Base64 图像，调用 `/v1/chat/completions` 实现图文理解；注意 Qwen-Audio 不支持该协议。
- **向量嵌入与排序**：`text-embedding-v4`、`qwen3-rerank` 等模型提供 `/v1/embeddings` 和 `/v1/rerank` 兼容端点，支持 `dimensions`、`top_n` 等 OpenAI 风格参数，但多模态 Embedding（如 `qwen3-vl-embedding`）**不兼容** OpenAI 接口。
- **批量推理与文件处理**：通过 `/v1/batch`（独立域名 `https://batch.dashscope.aliyuncs.com/compatible-mode/v1`）提交 JSONL 文件，支持文本、图像 URL 批量处理，需指定 `purpose="batch"`。
- **长期会话管理**：配合 `Conversations API`（`/v1/conversations`），创建/追加/查询会话，与 Responses API 协同实现跨设备、无状态对话延续。

> ⚠️ 注意：  
> - **域名必须使用业务空间专属格式**（如 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`），旧域名 `dashscope.aliyuncs.com` 已过时；  
> - **API Key 与 Base URL 必须地域一致且方案匹配**（如 [Token](token.md) Plan 个人版 Key 只能用于对应 [Token](token.md) Plan Base URL）；  
> - `qwen-deep-research`、`tongyi-intent-detect-v3` 等专用模型**仅支持 DashScope 原生接口，不兼容 OpenAI 协议**。

## 关键参数和配置

| 参数 | 类型 | 是否必填 | 说明 | 注意事项 |
|------|------|----------|------|----------|
| `base_url` | string | 是 | 业务空间专属 endpoint，格式为 `https://{WorkspaceId}.{region}.maas.aliyuncs.com/compatible-mode/v1` | 不可使用 `dashscope.aliyuncs.com`；Batch 场景需用独立域名 `https://batch.dashscope.aliyuncs.com/compatible-mode/v1` |
| `api_key` | string | 是 | 百炼 API Key（非 AccessKey），按地域和计费方案隔离 | 推荐设为环境变量 `DASHSCOPE_API_KEY`，避免硬编码 |
| `model` | string | 是 | 模型 ID，严格区分大小写与版本（如 `qwen3.7-plus` ≠ `qwen3-plus`） | `qwen3.8-max-preview` 等模型强制要求 `enable_thinking: true` |
| `messages` | array | 是 | 标准 OpenAI 消息数组，支持 `role: "user"/"assistant"/"system"` + `content`（含 `image_url`） | OCR、GUI 模型需在 `content` 中传图像；`system` 角色在部分模型（如 `tongyi-intent-detect-v3`）中承担关键指令作用 |
| `stream` | boolean | 否 | 是否启用流式响应，默认 `false` | 流式调用需解析 `choices[0].delta`；OCR、QVQ 等模型流式响应需额外传 `stream_options={"include_usage": true}` |
| `tools` / `tool_choice` | array / object | 否 | OpenAI 格式工具定义或调用策略（如 `"auto"`、`{"type": "function", "function": {"name": "xxx"}}`） | `functions` 参数已废弃；`response_format`（如 JSON Schema）**不支持**，将返回 `400` 错误 |
| `enable_thinking` | boolean | 否（部分模型必需） | 控制思考模式开关，影响推理路径与 token 计费 | `qwen3.8-max-preview` 等模型必须设为 `true`；该参数需置于请求 JSON 顶层，不可嵌套 |

## 面向开发者，简洁实用

- ✅ **开箱即用**：安装 `openai>=1.0`，初始化客户端即可调用：
  ```python
  from openai import OpenAI
  client = OpenAI(
      api_key="YOUR_API_KEY",
      base_url="https://your-workspace-id.cn-beijing.maas.aliyuncs.com/compatible-mode/v1"
  )
  response = client.chat.completions.create(
      model="qwen3.7-plus",
      messages=[{"role": "user", "content": "你好"}],
      stream=True
  )
  ```
- ✅ **调试建议**：  
  - 遇到 `400` 错误？检查是否误用了 `response_format` 或 `functions`；  
  - 流式响应无数据？确认 `stream=True` 且客户端正确处理 `delta` 字段；  
  - 认证失败（`401`）？核对 `api_key` 所属地域/方案是否与 `base_url` 匹配；  
  - 模型不识别？验证 `model` 名称是否精确（参考各文档中的“支持的模型列表”）。  
- ✅ **避坑清单**：  
  - 不要混用 OpenAI 与 Anthropic 协议（如 Hermes Agent 用 `/apps/anthropic`，Cursor 用 `/compatible-mode/v1`）；  
  - `qwen-deep-research`、`Qwen-Audio`、`tongyi-intent-detect-v3` 等模型**不支持** OpenAI 兼容接口；  
  - 多模态 Embedding（`qwen3-vl-embedding`）需用 DashScope 原生接口，不可走 `/v1/embeddings`。

## 关联主题页

- [qwen api reference](../api/qwen-api-reference.md)
- [toolkits and frameworks](../api/toolkits-and-frameworks.md)
- [use chat client or development tool](../guides/use-chat-client-or-development-tool.md)
- [more models](../api/more-models.md)
- [model deployment 1](../guides/model-deployment-1.md)
- [vector and sort](../api/vector-and-sort.md)



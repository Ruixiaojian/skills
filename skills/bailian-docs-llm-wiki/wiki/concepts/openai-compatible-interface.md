# OpenAI 兼容接口

OpenAI 兼容接口是百炼平台提供的一组遵循 OpenAI REST API 协议标准的模型调用入口，支持使用标准 OpenAI SDK（如 `openai` Python SDK v1.0+）或原生 HTTP 请求快速接入千问（Qwen）系列及第三方主流大模型，无需修改业务代码逻辑，仅需调整 `base_url` 和 `api_key` 即可完成迁移。

## 在百炼平台的不同场景中如何使用

- **快速迁移现有应用**：已有基于 OpenAI `chat/completions`、`/embeddings`、`/files`、`/batches` 等接口构建的应用，只需将 `base_url` 替换为百炼兼容域名（如 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`），并传入 `DASHSCOPE_API_KEY`，即可零改造调用 Qwen、DeepSeek、Kimi、GLM 等模型。
- **智能体（Agent）开发**：选用 `OpenAI 兼容-Responses` 接口（端点 `/v1/chat/completions` + `response_mode=responses`），自动集成联网搜索、代码解释器、网页内容提取等工具能力，并通过 `previous_response_id` 关联上下文，简化多轮工具调用与状态管理。
- **多模态与专业场景**：  
  - 视觉理解：在 `messages` 中传入含 `image_url` 的 content，调用 `qwen3-vl-plus` 等模型，兼容 OpenAI Vision 格式；  
  - 向量嵌入：使用 `/v1/embeddings` 端点调用 `text-embedding-v3/v4`，支持 `dimensions` 参数；  
  - 文档处理：通过 `/v1/files`（`purpose=file-extract`）和 `/v1/batches`（同步 Batch Chat）实现批量 PDF/Word 解析与结构化输出。
- **生产环境部署服务**：已部署的模型（PTU/MU 模式）同样暴露 OpenAI 兼容 endpoint，调用方式与预置模型一致，便于统一 SDK 封装与监控体系。

> ⚠️ 注意：并非所有模型均支持 OpenAI 兼容协议。例如 `Qwen-Audio`、`Qwen-Deep-Research`、`qwen3-vl-embedding`（多模态向量）仅支持 DashScope 原生接口；`Completions`（文本补全）和部分 `Files/Batch` 接口仍使用旧域名 `https://dashscope.aliyuncs.com/compatible-mode/v1`，不适用业务空间专属域名。

## 关键参数和配置

| 参数 | 类型 | 必填 | 说明 | 示例 |
|------|------|------|------|------|
| `base_url` | string | ✅ | 接口根地址，**必须匹配 API Key 所属地域与计费方案**：<br>• 业务空间专属（推荐）：`https://{WorkspaceId}.{region}.maas.aliyuncs.com/compatible-mode/v1`<br>• 兼容旧域名（北京）：`https://dashscope.aliyuncs.com/compatible-mode/v1`<br>• Batch Chat 固定：`https://batch.dashscope.aliyuncs.com/compatible-mode/v1` | `https://ws-abc123.cn-beijing.maas.aliyuncs.com/compatible-mode/v1` |
| `model` | string | ✅ | 模型 ID，需与所选接口类型匹配：<br>• Chat：`qwen3.8-max`, `deepseek-v4-flash`<br>• Responses：仅 `qwen3-*` 系列（如 `qwen3-max`）<br>• Embedding：仅 `text-embedding-v3`, `text-embedding-v4`<br>• Vision：仅 `qwen3-vl-plus`, `qwen3.5-ocr` | `"qwen3.7-plus"` |
| `messages` | array | ✅ | 对话消息数组，格式为 `[{"role": "user/system/assistant", "content": "..."}]`；Vision 模型支持 `content` 包含 `image_url` 字段 | `[{"role":"user","content":"你好"}]` |
| `stream` | boolean | ❌ | 是否启用流式响应，默认 `false`；设为 `true` 时返回 SSE 流，需按 `delta.content` 解析 | `true` |
| `stream_options` | object | ❌ | 流式增强选项，设 `{"include_usage": true}` 可在流结束事件中获取 token 统计 | `{"include_usage": true}` |
| `max_tokens` | integer | ❌ | 限制生成 token 数（不含输入）；**注意**：在 Responses 接口中该值包含系统提示与工具调用开销，建议生产环境改用 DashScope 接口的 `max_output_tokens` 实现精确控制 | `1024` |

- **认证方式**：所有请求需在 `Authorization` Header 中携带 `Bearer <your_dashscope_api_key>`（非 `DASHSCOPE_API_KEY` 的原始值，而是控制台生成的 DashScope API Key）。
- **地域隔离**：API Key、`base_url`、模型列表三者必须严格同地域（如北京 Key 不可用于新加坡 endpoint），否则返回 `401` 或 `404`。

## 面向开发者：简洁实用提示

- ✅ **首选 SDK 调用**：使用 `openai==1.40.0+`，初始化时指定 `base_url` 和 `api_key`，直接复用 `client.chat.completions.create(...)`，无需适配字段名。
- ✅ **生产环境必用业务空间域名**：提升稳定性、支持 WebSocket/AOQ、超时达 3600 秒，且可绑定独立配额与监控。
- ✅ **流式响应解析要点**：OpenAI 兼容接口返回 `delta.content`（非 `output.text`），最终 `usage` 在 `data: [DONE]` 前的 `delta` 事件中（当 `stream_options.include_usage=true`）。
- ⚠️ **避坑提醒**：
  - `max_tokens` 在 Responses 接口行为不透明 → 改用 DashScope 原生接口做 token 精确控制；
  - 工具调用（tool use）在 Responses 中自动管理，在 Chat Completions 中需手动拼接 `tool_calls` → 明确选择接口类型；
  - `qwen3-vl-embedding` 等多模态向量模型**不支持** OpenAI `/embeddings` → 请查文档切换至原生多模态向量 API。

如需调试，推荐使用 `curl` 快速验证：
```bash
curl -X POST "https://ws-xxx.cn-beijing.maas.aliyuncs.com/compatible-mode/v1/chat/completions" \
  -H "Authorization: Bearer YOUR_DASHSCOPE_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "qwen3.7-plus",
    "messages": [{"role": "user", "content": "你是谁？"}]
  }'
```

## 关联主题页

- [qwen api reference](../api/qwen-api-reference.md)
- [toolkits and frameworks](../api/toolkits-and-frameworks.md)
- [get started with models](../guides/get-started-with-models.md)
- [more models](../api/more-models.md)
- [model deployment 1](../guides/model-deployment-1.md)



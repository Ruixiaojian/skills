# 流式输出

流式输出（Streaming Output）是指模型响应以增量方式分块返回，而非等待全部生成完成后再一次性返回完整结果。该机制显著降低端到端延迟，提升用户感知流畅度，并支持实时渲染、语音合成驱动、渐进式思考展示等交互场景。

## 在百炼平台的不同场景中，这个概念如何使用

流式输出是百炼平台全栈 API 的通用能力，但具体实现方式和语义因协议与场景而异：

- **标准文本生成（Chat Completions / DashScope 原生接口）**：启用 `stream=true` 后，服务端按 token 或语义片段（如标点、短句）逐块推送 `data: {...}` SSE 消息；每个 chunk 包含 `delta.content`（本次新增文本）、`index`（消息序号）及可选的 `finish_reason`（如 `"stop"` 或 `"length"`）。适用于聊天界面实时打字效果、长文本生成监控等。

- **[OpenAI 兼容接口](openai-compatible-interface.md)（含 Toolkits & Frameworks）**：完全兼容 OpenAI 的流式格式，同时扩展支持 `stream_options={"include_usage": true}` —— 此时在流结束前的最后一个 chunk 中，将额外返回 `usage` 字段（含 `prompt_tokens`、`completion_tokens`、`total_tokens`），便于客户端精准统计与计费对账。

- **Realtime / Omni-Realtime API（WebSocket/AOQ/WebRTC）**：采用事件驱动流式模型，响应以结构化事件形式推送（如 `response.text.delta`、`response.audio.delta`、`conversation.item.input_audio_transcription`）。`delta` 事件天然具备增量性，无需客户端做去重处理；配合 `semantic_vad` 或 `server_vad` 可实现“边说边听、边听边答”的低延迟闭环。

- **Application Support（应用层）**：除基础 `stream=True` 外，支持 `incremental_output=True`（仅当 `stream=True` 时生效），确保每次 chunk 仅包含**本次新增 token**，而非从开头累计重传（避免前端重复渲染或语音合成卡顿），是构建高性能对话 UI 的关键配置。

- **批量处理（Batch）与文件处理（Files API）**：**不支持流式输出**。所有 Batch 请求均为同步阻塞式响应，需等待全部任务完成才返回结果数组；Files API 的文档解析、向量化等操作亦为异步任务，通过 `status` 轮询获取最终结果。

## 关键参数和配置

| 参数 | 类型 | 说明 | 是否必需 | 默认值 |
|------|------|------|----------|--------|
| `stream` | `boolean` | 启用流式响应的核心开关 | 否 | `false` |
| `stream_options` | `object` | 流式增强选项（仅 [OpenAI 兼容接口](openai-compatible-interface.md)支持） | 否 | — |
| `stream_options.include_usage` | `boolean` | 是否在流末尾 chunk 中返回 token 使用统计 | 否 | `false` |
| `incremental_output` | `boolean` | 是否启用真正增量式流（避免内容重复） | 否 | `false`（仅 `stream=true` 时生效） |

> ⚠️ 注意事项：
> - Anthropic 兼容接口（`/v1/messages`）必须显式设置 `stream: true`，且需正确解析 `event: message_start` / `content_block_delta` / `message_stop` 等 SSE 事件类型；
> - Omni-Realtime API 不使用 `stream` 参数，其流式行为由协议（WebSocket/AOQ）和事件模型天然决定；
> - `incremental_output=True` 是百炼特有优化，OpenAI 官方 SDK 默认行为为全量重传（`delta.content` 为当前完整文本），务必显式启用以获得最佳体验。

## 面向开发者，简洁实用

- ✅ **推荐做法**：所有实时交互类应用（Web 聊天、语音助手、代码补全）均应默认开启 `stream=True`；若需精确计费或调试，追加 `stream_options={"include_usage": true}`（OpenAI 兼容）或监听 `response.usage` 事件（Omni-Realtime）。
- ✅ **性能提示**：启用 `incremental_output=True` 可减少网络传输量与前端字符串拼接开销，尤其在高吞吐场景下效果显著。
- ❌ **避坑指南**：不要在 Batch、Files 或非流式 Endpoint（如 `/v1/embeddings`）上设置 `stream=true` —— 将返回错误（HTTP 400）；Omni-Realtime 接口忽略 `stream` 参数，勿误配。
- 🛠️ **调试建议**：使用 `curl -N` 或 SDK 的 `stream=True` 模式捕获原始流，观察 chunk 结构；生产环境建议监听 `finish_reason` 判断生成是否正常终止，避免因超时或截断导致内容不全。

## 关联主题页

- [qwen api reference](../api/qwen-api-reference.md)
- [toolkits and frameworks](../api/toolkits-and-frameworks.md)
- [omni realtime api](../api/omni-realtime-api.md)
- [realtime api user guide](../api/realtime-api-user-guide.md)
- [application support](../guides/application-support.md)



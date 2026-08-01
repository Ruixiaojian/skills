# 流式输出

流式输出（Streaming Output）是指模型服务在生成响应过程中，将结果以增量方式分块、实时推送至客户端，而非等待全部内容生成完毕后一次性返回。这种方式显著降低用户感知延迟，提升交互流畅度，是构建实时对话、语音合成、长文本生成等场景的关键能力。

## 在百炼平台的不同场景中如何使用

- **模型 API 调用（Qwen 系列）**：通过 DashScope 原生接口或 [OpenAI 兼容接口](openai-compatible-interface.md)（`/chat/completions`）设置 `stream=true`，即可启用逐 token 流式响应；Anthropic 兼容接口也支持流式，但事件格式（如 `content_block_delta`）与前两者不兼容，需单独适配。
- **应用调用（Application Call）**：仅 OpenAI 兼容的 Responses API 支持 `stream=true`；DashScope 原生应用接口暂不支持流式。注意：工作流类应用必须在控制台「结束节点」手动开启“流式输出”开关并重新发布，否则即使请求中设置 `stream=true` 也不会生效。
- **实时多模态 API（Omni Realtime / Realtime API）**：原生基于 WebSocket 或 AOQ 的事件驱动架构天然支持流式。文本输出以 `response.text.delta` 事件形式推送；音频输出以 `response.audio.delta` 分片推送（PCM 格式），无需额外参数，流式为默认行为。
- **RAG 与智能体应用**：在应用配置中启用流式后，模型生成、插件调用返回、知识库检索结果均可按阶段流式透出；配合 `incremental_output=true` 可确保每次只返回新增内容，避免重复渲染。

## 关键参数和配置

| 参数 | 类型 | 说明 | 默认值 | 生效范围 |
|------|------|------|--------|----------|
| `stream` | boolean | 启用基础流式模式（逐 token 或逐事件推送） | `false` | 所有支持流式的 API（Qwen 模型、Application Responses、Omni Realtime 等） |
| `incremental_output` | boolean | 在 `stream=true` 基础上启用增量模式：每次仅返回本次新增内容，不重复发送历史片段 | `false` | DashScope 原生接口、Application SDK（推荐搭配 `stream=true` 使用） |
| `modalities` | array | 实时 API 中控制输出模态，如 `["text", "audio"]` 表示同时流式返回文本与音频分片 | `["text","audio"]` | Omni Realtime / Realtime API |

> ⚠️ 注意事项：
> - `stream=true` 与异步模式（如 `background=true`）互斥，不可同时启用；
> - Anthropic Messages 接口的流式响应结构与 OpenAI/DashScope 不同，需按其规范解析 `delta.text` 字段；
> - 工作流应用未开启节点级流式开关时，`stream=true` 请求将退化为同步响应；
> - 流式响应的 HTTP 状态码仍为 `200 OK`，但 Content-Type 为 `text/event-stream`，需使用 EventSource 或自定义流解析器处理。

## 面向开发者：简洁实用建议

- ✅ **首选 SDK**：使用 `dashscope` SDK（v1.20.0+）调用模型或应用，内置流式迭代器（如 `for chunk in response: ...`），自动处理 SSE 解析与重连；
- ✅ **错误处理**：流式请求可能中途断连，建议监听 `error` 事件并实现指数退避重试（SDK 已内置）；
- ✅ **前端渲染**：对文本流，推荐累积 `chunk.output.text` 并防抖更新 UI；对音频流，可直接将 `response.audio.delta` Base64 数据喂入 Web Audio API；
- ❌ **避免陷阱**：不要在流式响应中依赖 `response.usage`（该字段仅在最终 `done` 事件中出现）；不要在 `stream=true` 时尝试读取 `response.output.text` 全量字段（为空或不完整）。

## 关联主题页

- [qwen api reference](../api/qwen-api-reference.md)
- [application call](../api/application-call.md)
- [omni realtime api](../api/omni-realtime-api.md)
- [realtime api user guide](../api/realtime-api-user-guide.md)
- [application support](../guides/application-support.md)



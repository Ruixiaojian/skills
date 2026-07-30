# 流式输出

流式输出（Streaming Output）是指模型服务将生成结果分块、实时、逐段返回给客户端的通信模式，而非等待完整响应生成完毕后一次性返回。它通过 HTTP Server-Sent Events（SSE）、WebSocket 或 chunked transfer encoding 等协议实现低延迟、高感知的实时交互体验，是构建对话式应用、语音助手、实时翻译等场景的核心能力。

## 在百炼平台的不同场景中，这个概念如何使用

- **知识问答（Knowledge Chat）**：`/api/v2/apps/knowledge/chat` 接口采用 SSE 协议返回结构化流式事件，包含 `event: planning`（推理规划）、`event: tool_call`（工具调用）、`event: message`（最终回答）三类事件，支持前端逐步渲染思考过程与答案。
- **Qwen 文本生成（OpenAI 兼容 / DashScope 原生）**：所有 `chat/completions`、`messages` 及 DashScope 原生 `/generation` 接口均支持 `stream=true`。[OpenAI 兼容接口](openai-compatible-interface.md)返回 `delta` 字段增量内容；DashScope 原生接口返回 `output.text` 分段，语义更清晰、调试字段（如 `usage`）更完整。
- **OpenAI 兼容工具包（Toolkits & Frameworks）**：`stream` 是通用布尔参数，启用后可配合 `stream_options={"include_usage": true}` 在流末尾获取 token 统计，适用于 LangChain 等框架集成。
- **Omni 实时 API（WebSocket）**：基于事件驱动模型，服务端通过 `response.text.delta` 和 `response.audio.delta` 事件持续推送文本片段或音频 PCM 数据帧，实现毫秒级端到端流式响应。
- **Realtime API（AOQ/WebRTC）**：底层协议天然支持流式媒体与文本混合传输；`qwen3.5-omni-realtime` 等模型在 `session.update` 后即开始推送 `response.text.delta`，无需额外开启开关，流式行为由协议与会话状态自动触发。

## 关键参数和配置

| 参数 | 类型 | 说明 | 适用接口 |
|------|------|------|----------|
| `stream` | `boolean` | 必需显式设为 `true` 才启用流式输出 | OpenAI 兼容、DashScope 原生、Knowledge Chat、Responses API |
| `stream_options` | `object` | 控制流式附加行为：<br>• `{"include_usage": true}`：在流结束事件（`[DONE]` 或 `event: done`）中返回 `usage` 字段 | OpenAI 兼容、Responses API（DashScope 原生默认始终返回 `usage`） |
| SSE `event` 类型 | `string` | 知识问答流中必须解析的事件名：<br>• `planning`：模型规划步骤<br>• `tool_call`：工具调用请求<br>• `message`：最终生成内容 | Knowledge Chat（`/api/v2/apps/knowledge/chat`） |
| WebSocket `delta` 事件 | `string` | Omni Realtime 中关键事件名：<br>• `response.text.delta`：文本增量<br>• `response.audio.delta`：音频 PCM 增量 | Omni Realtime API |
| 连接保活要求 | — | 客户端必须保持长连接（HTTP Keep-Alive 或 WebSocket 持久连接），超时断连将中断流式响应 | 所有流式接口 |

> ⚠️ 注意：  
> - 不同协议流式格式不兼容：OpenAI 的 `delta` ≠ DashScope 的 `output.text` ≠ Knowledge 的 `event:message`；请按对应文档解析；  
> - Knowledge Chat 的 SSE 响应需设置 `Accept: text/event-stream` 请求头，并正确处理 `data:` 行与换行符；  
> - Omni Realtime 和 AOQ 场景下，流式输出与 VAD（语音活动检测）强耦合，`semantic_vad` 可提升文本流与语音流的语义对齐精度。

## 面向开发者，简洁实用

- ✅ **首选 DashScope 原生接口**：流式字段语义统一（`output.text`）、含完整 `usage`、支持增量调试，适合生产环境；
- ✅ **前端解析建议**：使用 `EventSource`（SSE）或 `WebSocket` 原生 API，避免依赖未适配百炼格式的第三方 SDK；
- ✅ **错误处理必做**：监听连接中断、`429` 限流、`503` 服务不可用，实现自动重连 + 断点续传（Knowledge Chat 支持 `last_event_id`）；
- ❌ **避免混用域名**：`dashscope.aliyuncs.com`（OpenAPI）与 `{workspaceId}.maas.aliyuncs.com`（应用网关）流式行为不一致，严禁跨体系调用；
- 🚀 **性能提示**：启用流式后，首 token 延迟（Time to First [Token](token.md), TTFT）显著降低，但总生成时间（E2E Latency）不变；优化重点应放在 [prompt](../guides/prompt.md) 工程与模型选型上。

## 关联主题页

- [knowledge](../api/knowledge.md)
- [qwen api reference](../api/qwen-api-reference.md)
- [toolkits and frameworks](../api/toolkits-and-frameworks.md)
- [omni realtime api](../api/omni-realtime-api.md)
- [realtime api user guide](../api/realtime-api-user-guide.md)



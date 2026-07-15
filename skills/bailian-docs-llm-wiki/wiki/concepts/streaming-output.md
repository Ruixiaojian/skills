# 流式输出

流式输出（Streaming Output）是百炼平台提供的一种实时响应机制，允许模型在生成结果的过程中，将输出内容分块、逐步推送至客户端，而非等待全部内容生成完毕后一次性返回。该机制显著降低端到端延迟，提升用户交互体验，尤其适用于对话类、语音合成、长文本生成等对实时性敏感的场景。

## 在百炼平台的不同场景中，这个概念如何使用

流式输出在百炼平台中并非统一协议，而是根据接口类型和底层能力采用不同传输机制，开发者需按场景适配解析方式：

- **HTTP SSE（Server-Sent Events）流式**  
  主要用于 `knowledge/chat`（知识问答）和 `application-call/responses`（OpenAI 兼容 Responses API）等 REST 接口。服务端以 `text/event-stream` MIME 类型响应，每条消息格式为：  
  ```
  event: chunk
  data: {"output":{"text":"你好"}}
  
  event: chunk
  data: {"output":{"text":"，很高兴为您服务。"}}
  
  event: done
  data: {"output":{"text":"，很高兴为您服务。"},"usage":{...}}
  ```  
  客户端需监听 `chunk` 事件持续拼接文本，并在收到 `done` 事件后处理最终结果与统计信息。

- **WebSocket 实时流式**  
  专用于 `Qwen-Omni-Realtime` 系列 API。通过双向 WebSocket 连接，服务端主动推送结构化事件（如 `response.text.delta`、`response.audio.delta`），支持文本、音频、工具调用状态等多模态增量输出，适用于语音助手、实时字幕等低延迟场景。

- **DashScope 原生 HTTP 流式**  
  在 `Generation.call` 等原生接口中，通过 `stream=true` 启用，返回标准 SSE 格式；若需更细粒度控制（如仅增量返回新 token），可配合 `incremental_output=true` 参数，此时 `output.text` 字段为本次增量内容，而非累计全文。

- **非流式回退兼容**  
  所有支持流式的接口均提供 `stream=false` 选项（默认值因接口而异），此时返回单次完整 JSON 响应，结构与流式末尾 `event: done` 的 `data` 字段一致，便于快速调试或轻量集成。

> ⚠️ 注意：流式能力依赖服务端配置。例如工作流应用需在「结束节点」显式开启“流式输出”开关并重新发布；Omni Realtime 模型需在 `session.update` 中设置 `modalities: ["text", "audio"]` 才能触发音频流。

## 关键参数和配置

| 参数 | 类型 | 说明 | 所属接口/场景 |
|------|------|------|----------------|
| `stream` | `boolean` | 全局开关，启用流式传输（SSE 或 WebSocket）。设为 `true` 时，响应头含 `Content-Type: text/event-stream`（HTTP）或建立 WebSocket 连接（Realtime）。 | 所有支持流式的接口（`knowledge/chat`, `responses`, `Generation`, `Application.call` 等） |
| `incremental_output` | `boolean` | **仅 DashScope 原生接口有效**。当 `stream=true` 时，若设为 `true`，则 `output.text` 返回本次增量内容；若为 `false`（默认），则返回当前累计全文。 | `dashscope.Generation` / 原生 `/generation` 接口 |
| `modalities` | `string[]` | **仅 Omni Realtime API 有效**。指定输出模态组合，如 `["text"]` 或 `["text","audio"]`，决定是否触发对应流式事件。 | `qwen3.5-omni-realtime` 等 WebSocket 接口 |
| `session_id`（流式上下文） | `string` | 在支持会话的流式调用中（如 `Application.call`），`session_id` 用于关联多轮流式响应，确保上下文连续性。注意：`Responses API` 异步模式（`background=true`）不支持流式。 | `Application.call`, `responses` 同步流式 |

## 面向开发者，简洁实用

- ✅ **首选 SDK 调用**：Python 使用 `dashscope` SDK 的 `stream=True` 参数（如 `Generation.call(..., stream=True)`），SDK 自动处理 SSE 解析与事件分发，避免手动解析 `event:` 行。
- ✅ **HTTP 调试建议**：用 `curl -N` 或浏览器 DevTools 的 Network → EventStream 查看原始流数据；生产环境务必设置超时（如 `timeout=120s`），防止连接挂起。
- ✅ **错误处理要点**：流式请求失败时，可能已部分接收数据。请检查 HTTP 状态码（如 `401`, `429`）及首个 `event: error` 消息，不要仅依赖 `event: done`。
- ❌ **避坑提示**：
  - 工作流应用未在结束节点开启“流式输出” → 即使传 `stream=true` 也返回非流式响应；
  - Omni Realtime 使用 `qwen-omni-turbo-realtime` 模型 → 不支持 `temperature`/`max_tokens` 等参数，但流式功能正常；
  - `knowledge/chat` 接口 `stream=false` 时，响应结构与流式 `done` 事件 payload 完全一致，可复用同一解析逻辑。

流式输出是构建高性能 AI 应用的关键能力。正确启用并解析它，能让您的产品获得接近本地响应的流畅体验。

## 关联主题页

- [knowledge](../api/knowledge.md)
- [application call](../api/application-call.md)
- [omni realtime api](../api/omni-realtime-api.md)
- [qwen api reference](../api/qwen-api-reference.md)
- [bailian application calling](../guides/bailian-application-calling.md)



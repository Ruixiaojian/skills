# 流式输出

流式输出（Streaming Output）是百炼平台提供的一种渐进式响应机制，允许模型在推理过程中将结果分块（如逐 token、逐句或逐段）实时返回，而非等待全部生成完成后再一次性返回。该机制显著降低端到端延迟，提升用户体验，尤其适用于对话交互、实时语音合成、前端渐进渲染等对响应速度和交互感要求高的场景。

## 在百炼平台的不同场景中如何使用

流式输出在百炼平台中并非单一能力，而是贯穿多个核心服务的通用交互模式，具体应用方式如下：

- **Application Call（智能体/工作流调用）**  
  通过 `stream=true` 参数启用流式响应（默认 `false`）。需注意：  
  - 工作流应用必须在结束节点显式开启「流式输出」开关，否则即使请求中设置 `stream=true` 也无效；  
  - 异步调用（`background=true`）与流式互斥，不可同时启用；  
  - 返回格式为 Server-Sent Events（SSE），每帧包含 `delta`（增量文本）、`finish_reason` 和可选的 `usage` 字段。

- **Realtime API（全模态实时交互）**  
  流式是其默认且唯一输出模式。基于 WebSocket 或 AOQ 协议，模型以毫秒级粒度持续推送 `text.delta` 和 `audio.chunk`（PCM 音频帧），支持自然打断、VAD 触发、语音+文本同步渲染。无需额外参数，只要建立连接即进入流式通信。

- **Omni Realtime API（Qwen-Omni 系列）**  
  原生支持低延迟流式，输出模态由 `session.update` 中的 `modalities` 决定（如 `["text", "audio"]`）。音频流与文本流严格时间对齐，支持 `smooth_output`（仅 Flash 版）优化音频拼接平滑度。

- **标准模型调用（OpenAI 兼容 / DashScope 原生）**  
  对 `qwen3.7-plus` 等文本模型，直接在 `chat.completions.create()` 中传入 `stream=True` 即可启用。SDK 自动解析 SSE 流，开发者可逐 chunk 处理（如实时写入 DOM 或转发至前端 WebSocket）。

- **Application Support（应用增强能力）**  
  支持两种语义层级的流式：  
  - `stream=True`：标准 token 级流式，返回原始增量文本；  
  - `incremental_output=True`：应用层增量流式，返回经后处理（如 Markdown 渲染、工具调用结果组装）后的结构化增量内容，更适合前端直接消费。

## 关键参数和配置

| 参数 | 类型 | 作用 | 注意事项 |
|------|------|------|----------|
| `stream` | `boolean` | 启用基础流式输出（token 级） | 所有支持流式的接口通用；设为 `true` 后响应头为 `Content-Type: text/event-stream` |
| `incremental_output` | `boolean` | 启用应用层增量流式（结构化内容级） | 仅 Application Call 和部分智能体场景支持；与 `stream=true` 可叠加使用，但优先级高于 `stream` |
| `modalities` | `string[]` | 指定流式输出模态（如 `["text"]`, `["text","audio"]`） | Omni Realtime 必填；`["audio"]` 单独不支持，至少含 `"text"` |
| `smooth_output` | `boolean` | 启用音频流平滑拼接（仅 `qwen3.5-omni-flash-realtime`） | 减少音频卡顿，但略微增加首包延迟；默认 `false` |

> ⚠️ 重要限制：  
> - 异步模式（`background=true`）下禁止启用流式；  
> - 流式响应不支持重试（retry）机制，需前端自行处理连接中断；  
> - 实时音频流要求客户端具备 PCM 解码与播放能力（24 kHz 输出，16-bit signed integer）。

## 面向开发者：简洁实用建议

- **首选 SDK 封装**：Python 使用 `dashscope.Application.call(..., stream=True)` 或 OpenAI SDK 的 `response = client.chat.completions.create(..., stream=True)`；JavaScript 推荐 `fetch()` + `ReadableStream` 或官方 Realtime SDK，避免手动解析 SSE。
- **前端渲染**：对 `stream=True`，累加 `delta.content` 并实时更新 UI；对 `incremental_output=True`，直接按 `output_type`（如 `"text"`, `"image_url"`）渲染对应组件。
- **错误处理**：监听 `event: error` 和 HTTP 状态码（如 400/429/503），结合 `retry-after` 头实现指数退避重连。
- **性能优化**：流式场景下，禁用 `max_tokens` 过大值（易导致长尾延迟）；对语音合成，预加载音色资源并复用 `session` 连接。
- **调试技巧**：使用 `curl -N` 或 Postman 的 SSE 插件直接观察原始流；生产环境务必启用 `RequestId` 日志追踪。

## 关联主题页

- [application call](../api/application-call.md)
- [realtime api user guide](../api/realtime-api-user-guide.md)
- [omni realtime api](../api/omni-realtime-api.md)
- [application support](../guides/application-support.md)
- [get started with models](../guides/get-started-with-models.md)
- [more about models](../api/more-about-models.md)



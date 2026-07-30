# 流式输出

流式输出（Streaming Output）是指模型服务在生成响应过程中，将结果以增量方式分块（chunk）实时返回给客户端，而非等待全部内容生成完毕后一次性返回。这种方式显著降低端到端延迟，提升用户感知的响应速度与交互流畅性，是构建低延迟对话、实时语音合成、长文本生成等场景的关键能力。

## 在百炼平台的不同场景中如何使用

- **Qwen 系列模型 API（OpenAI 兼容 / DashScope 原生）**：  
  默认启用流式输出（`stream: true`），适用于 `qwen-max`、`qwen-plus`、`qwen-turbo` 等文本生成模型。[OpenAI 兼容接口](openai-compatible-interface.md)返回符合 SSE 标准的 `text/event-stream` 响应；DashScope 原生接口支持更细粒度控制（如 `incremental_output` 参数）。注意：OpenAI 兼容-Responses 模式下，流式 chunk 中 `delta.tool_calls` 字段可能不完整，建议非流式模式验证工具调用逻辑。

- **应用调用（Application Call）**：  
  仅**同步调用**支持流式输出（通过 `stream=true` 启用），适用于新版智能体、旧版智能体及工作流；**异步调用（`background=true`）不支持流式输出**，必须轮询或订阅事件获取最终结果。

- **Omni Realtime API 与 Realtime API**：  
  原生基于 WebSocket 的事件驱动架构，天然支持流式输出。文本以 `response.text.delta` 事件逐 token 推送；音频以 `response.audio.delta` 事件按 PCM 帧（通常 20ms/帧）持续下发。`modalities: ["text", "audio"]` 配置下，两类流可并行、低延迟同步输出。

- **异步任务类模型（图像/视频生成等）**：  
  **不支持流式输出**。此类任务需通过 `task_id` 轮询或事件总线接收完成通知，结果为一次性结构化响应（如 OSS URL 或 base64 图片）。

## 关键参数和配置

| 参数 | 类型 | 说明 | 适用场景 |
|------|------|------|----------|
| `stream` | `boolean` | 控制是否启用流式响应。设为 `true` 时，HTTP 响应头为 `Content-Type: text/event-stream`，响应体为 SSE 格式 chunk。默认值为 `false`（同步阻塞模式）。 | Qwen API、Application Call（同步） |
| `incremental_output` | `boolean` | DashScope 原生接口特有参数，启用后返回增量 token（等效于 `stream=true`），但响应格式为 JSON 数组而非 SSE。适用于无法处理 SSE 的客户端。 | DashScope 文本生成原生接口 |
| `modalities` | `array` | 指定输出模态组合，如 `["text"]` 或 `["text","audio"]`。决定流式事件类型（`response.text.delta` / `response.audio.delta`）。 | Omni Realtime API、Realtime API |
| `enable_search` / `tools` | `boolean` / `array` | 影响流式内容结构：启用后，流式响应中会包含 `response.tool_use.delta` 或 `response.search_result.delta` 等事件，需客户端按事件类型解析。 | Omni Realtime（`qwen3.5-omni-realtime` 系列）、Qwen DashScope 接口 |

> ⚠️ 注意事项：
> - 流式响应需客户端正确处理 SSE 解析（如 `EventSource` 或 `aiohttp.ClientSession` 的 `content.iter_any()`）；
> - 所有流式接口均要求连接保持活跃，超时断连将中断输出；
> - 异步调用、文件上传、[多模态](multi-modal.md)预处理等前置步骤**本身不支持流式**，仅最终模型推理阶段可流式。

## 面向开发者：简洁实用建议

- ✅ **首选流式**：对延迟敏感场景（如客服对话、语音助手），务必设置 `stream=true` 并监听增量事件；
- ✅ **验证兼容性**：OpenAI SDK 默认支持 SSE，但需确认版本 ≥1.0；自定义 HTTP 客户端请严格遵循 [SSE 协议规范](https://html.spec.whatwg.org/multipage/server-sent-events.html)；
- ✅ **错误处理**：流式请求失败时，部分 chunk 可能已接收，需检查 `event: error` 或 `data:` 中的 `error` 字段，并重试完整请求；
- ❌ **避免混用**：不要在 `background=true` 的异步请求中设置 `stream=true`（会被忽略）；
- 🛠️ **调试技巧**：使用 `curl -N` 或 Postman 的 SSE 插件直接观察原始流式响应，快速定位解析问题。

## 关联主题页

- [qwen api reference](../api/qwen-api-reference.md)
- [application call](../api/application-call.md)
- [omni realtime api](../api/omni-realtime-api.md)
- [realtime api user guide](../api/realtime-api-user-guide.md)
- [more about models](../api/more-about-models.md)



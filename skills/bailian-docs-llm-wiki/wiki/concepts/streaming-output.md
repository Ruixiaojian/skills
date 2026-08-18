# 流式输出

流式输出（Streaming Output）是指模型服务在生成响应过程中，将结果以连续、分块的方式实时返回给客户端，而非等待整个响应生成完毕后一次性返回。这种方式显著降低端到端延迟，提升用户感知的响应速度与交互自然度，是构建实时对话、语音助手、长文本生成等体验的关键能力。

## 在百炼平台的不同场景中，这个概念如何使用

- **Qwen 系列模型 API（OpenAI 兼容 / DashScope 原生）**：  
  通过设置 `stream=true`（[OpenAI 兼容接口](openai-compatible-api.md)）或 `incremental_output=true`（DashScope 原生接口），启用流式响应。[OpenAI 兼容接口](openai-compatible-api.md)返回符合 OpenAI SSE 格式的 `data: {"delta": {"content": "..."}}` 事件；DashScope 接口则返回 `output.text` 字段的增量片段，语义更贴近原始 token 输出，适合对分块粒度有明确控制需求的场景（如前端逐字高亮、token 统计）。

- **Qwen-Omni Realtime API（WebSocket）**：  
  流式是默认且强制的行为模式。服务端通过 `response.text.delta`、`response.audio.delta` 等结构化事件持续推送文本和音频数据，无需显式开启开关。开发者需监听对应事件类型，并按需拼接、渲染或合成。该设计天然适配语音交互的“边说边听”范式，支持毫秒级延迟反馈。

- **应用调用（Application Call）**：  
  仅 OpenAI 兼容协议（`/api/v2/apps/agent/{APP_ID}/compatible-mode/v1/responses`）支持 `stream=true` 参数。但需注意：**流式能力依赖后端应用配置**——工作流类应用必须在结束节点显式启用“流式输出”开关，否则即使请求带 `stream=true`，仍将降级为同步响应。智能体类应用默认支持流式，但若内部调用非流式插件或工具，可能中断流式链路。

- **Realtime API 多协议（AOQ/WebRTC/WebSocket）**：  
  所有协议均原生支持流式，但实现机制不同：  
  - WebSocket：基于文本事件（如 `response.text.delta`）；  
  - AOQ/WebRTC：基于二进制媒体帧（PCM 音频 chunk、文本元数据包），由 SDK 自动解包并触发回调，开发者无需处理底层分块逻辑。

## 关键参数和配置

| 接口类型 | 参数名 | 类型 | 是否必需 | 说明 |
|----------|--------|------|----------|------|
| OpenAI 兼容（Qwen / Application） | `stream` | boolean | 否（默认 `false`） | 设为 `true` 启用 SSE 流式响应；必须配合 `Content-Type: text/event-stream` 处理。 |
| DashScope 原生（Qwen） | `incremental_output` | boolean | 否（默认 `false`） | 替代 `stream` 的百炼原生流式开关；返回 `output.text` 增量，更精确反映模型 token 生成顺序。 |
| Omni Realtime（WebSocket） | — | — | — | **无显式参数**；流式为默认行为，由协议层保障。 |
| Application Call（OpenAI 兼容） | `stream` | boolean | 否（默认 `false`） | 同上；但要求目标工作流应用已开启“流式输出”配置。 |
| Omni Realtime（AOQ/WebRTC） | — | — | — | **无显式参数**；流式由连接建立即生效，SDK 自动管理分块与缓冲。 |

> ⚠️ 注意：`stream=true` 与异步调用（`background=true`）互斥，不可同时设置；流式响应不支持 `response_format: json_object`（JSON Schema 强约束会阻断增量输出）。

## 面向开发者，简洁实用

- **调试建议**：首次接入时，优先使用 `curl -N` 或 Postman 的 SSE 模式验证 OpenAI 兼容流式；DashScope 原生流式推荐用官方 Python SDK 的 `Generation.call(..., stream=True)` 方法，自动处理 event parsing。
- **错误处理**：流式请求失败时，服务端可能返回部分有效 chunk 后中断连接。客户端应监听 `event: error` 或连接关闭事件，并实现重试逻辑（建议带 `last_event_id` 或 `session_id` 续传）。
- **性能优化**：  
  - 文本流：避免高频 DOM 操作，可累积 2–3 个 chunk 后批量渲染；  
  - 音频流（Omni）：启用 `smooth_output=true`（`qwen3.5-omni-flash-realtime`）可减少语音卡顿，提升口语连贯性；  
  - 长上下文：流式下 `messages` 总长度限制不变（如 [OpenAI 兼容接口](openai-compatible-api.md)仍为 24,576 tokens），请提前截断或摘要历史。
- **兼容性提示**：OpenAI 兼容接口的 `delta.content` 可能为空字符串（表示换行/标点等控制符），需忽略空内容；DashScope 的 `incremental_output` 返回的 `text` 字段始终为非空增量片段，更适合 token 级精度控制。

## 关联主题页

- [qwen api reference](../api/qwen-api-reference.md)
- [omni realtime api](../api/omni-realtime-api.md)
- [realtime api user guide](../api/realtime-api-user-guide.md)
- [application call](../api/application-call.md)



# 流式输出

流式输出（Streaming Output）是指模型响应以增量方式、分块逐次返回，而非等待完整结果生成后一次性返回。它通过持续推送 token 或事件片段，显著降低端到端延迟，提升用户感知的实时性与交互自然度，是语音对话、长文本生成、实时翻译等低延迟场景的核心能力。

## 在百炼平台的不同场景中，这个概念如何使用

流式输出在百炼平台中并非统一机制，而是根据接入协议和应用类型差异化实现，开发者需按场景选择并正确配置：

- **Realtime API（WebSocket/WebRTC/AOQ）**：  
  所有实时[多模态](multi-modal.md)模型（如 `qwen3.5-omni-plus-realtime`）**默认启用流式输出**，无需显式开关。客户端通过监听 `response.text.delta`（文本增量）、`response.audio.chunk`（音频 PCM 块）、`response.tool_calls.delta`（工具调用片段）等事件，实时消费数据。这是真正的双向流式——输入音频流式上传，输出文本/音频流式下发，端到端延迟可控制在 300ms 内。

- **Application Call（应用调用）**：  
  仅支持**同步调用**启用流式（`stream=true`），且**仅对工作流应用生效**（智能体应用暂不支持）。需在应用发布时提前开启“流式输出”开关，否则即使请求携带 `stream=true` 也会降级为非流式响应。异步调用（`background=true`）**完全不支持流式**。

- **Qwen 系列基础模型 API（DashScope / OpenAI 兼容）**：  
  通过 `stream=true` 参数启用。[OpenAI 兼容接口](openai-compatible-api.md)返回 `delta.content` 字段；DashScope 原生接口返回 `output.text` 字段（含增量内容）。注意：`OpenAI 兼容-Responses` 模式下，流式响应会包含工具调用中间状态（如 `delta.tool_calls`），便于前端动态渲染思考过程。

- **Application Support（应用增强能力）**：  
  当同时启用 `stream=true` 和 `incremental_output=true` 时，实现**真正增量式流式**：每个 chunk 仅包含本次新增内容（非全量重发），避免前端重复渲染。该参数对 SDK 版本敏感，建议使用 DashScope SDK ≥ v1.2.0 并显式设置。

> ⚠️ 注意：流式能力受模型限制。例如 `qwen-omni-turbo-realtime` 禁止修改 `temperature`/`top_p` 等参数，但流式本身不受影响；而 `qwen-turbo` 的流式调用不享受免费额度。

## 关键参数和配置

| 参数 | 类型 | 说明 | 是否必需 | 备注 |
|------|------|------|----------|------|
| `stream` | `boolean` | 启用流式响应模式 | 是（流式场景下） | 所有支持流式的 API 均需显式设为 `true`；默认为 `false` |
| `incremental_output` | `boolean` | 启用增量式流式（仅返回新增内容） | 否（推荐启用） | 仅 Application Call 和部分 DashScope 接口支持；旧版 SDK 可能失效 |
| `modalities` | `array<string>` | 指定输出模态（如 `["text"]` 或 `["text","audio"]`） | 是（Realtime API） | Realtime API 中决定是否流式输出音频块；`["text"]` 时仅流式文本 |
| `voice` / `output_audio_format` | `string` | 音色与音频格式 | Realtime API 必需 | 影响音频流式 chunk 的编码（当前仅支持 `pcm`） |

- **Realtime API 特有事件驱动字段**（非请求参数，但需客户端处理）：
  - `response.text.delta`: 文本增量（UTF-8 字符串）
  - `response.audio.chunk`: 音频二进制 chunk（`Uint8Array`，PCM 格式）
  - `response.progress`: 生成进度百分比（部分模型支持）
  - `response.done`: 表示该响应单元结束（非整个会话）

## 面向开发者，简洁实用

- ✅ **必做**：流式调用前，务必确认目标模型/应用明确支持流式（参考各文档“支持的模型/功能”章节），并检查地域与 Workspace ID 是否符合要求。
- ✅ **推荐**：Realtime API 客户端使用 DashScope SDK 的 `onEvent` 回调；Qwen/OpenAI 接口使用 `SSE` 解析器（如 `eventsource-parser`），避免手动解析 raw stream。
- ✅ **避坑**：
  - 不要对 `stream=true` 的请求设置过短的 HTTP 超时（建议 ≥ 60s）；
  - Realtime API 中 `modalities` 缺失或非法值会导致连接立即关闭；
  - Application Call 的 `stream=true` 对智能体无效，误用将返回 400 错误；
  - `incremental_output=true` 在未更新 SDK 时可能导致前端重复追加文本，建议先验证行为。
- ✅ **调试技巧**：使用控制台「API 调试」页或 `curl -N` 命令直接观察原始 SSE 流，确认 `data:` 字段结构与预期一致。

## 关联主题页

- [omni realtime api](../api/omni-realtime-api.md)
- [realtime api user guide](../api/realtime-api-user-guide.md)
- [application call](../api/application-call.md)
- [qwen api reference](../api/qwen-api-reference.md)
- [application support](../guides/application-support.md)



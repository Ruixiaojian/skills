# 流式输出

流式输出（Streaming Output）是指模型服务在生成响应过程中，将结果以增量、分块的方式持续返回给客户端，而非等待全部内容生成完毕后一次性返回。这种方式显著降低端到端延迟，提升用户体验，尤其适用于长文本生成、实时语音合成、[多模态](multi-modal.md)交互等对响应速度敏感的场景。

## 在百炼平台的不同场景中如何使用

流式输出在百炼平台中广泛支持，但具体实现方式和适用范围因接口协议与模型类型而异：

- **Qwen 文本生成 API（DashScope / OpenAI 兼容）**：所有同步文本生成接口均支持 `stream=true`。DashScope 接口通过 `output.text` 字段逐块返回文本；[OpenAI 兼容接口](openai-compatible-interface.md)则遵循 OpenAI 标准，返回 `choices[0].delta.content` 字段，需按 chunk 拼接。注意：`qwen-max` 在 DashScope 接口中默认启用思考模式，流式输出会包含中间推理步骤（如 `<think>...</think>`），而 [OpenAI 兼容接口](openai-compatible-interface.md)不暴露该结构。

- **Omni Realtime API（WebSocket）**：作为原生实时协议，流式是默认行为。文本输出以 `text` 事件形式实时推送；若启用 `output_modalities: ["TEXT", "AUDIO"]`，音频流通过 `audio` 事件以 PCM 分片形式持续下发，支持低延迟 TTS 播放。

- **Realtime API（WebSocket/WebRTC/AOQ）**：所有协议均天然支持流式。WebSocket 使用 HTTP chunked encoding 或 WebSocket message 分帧；WebRTC 和 AOQ 则基于 DataChannel 或 QUIC stream 实时传输文本/音频片段，开发者需监听对应事件（如 `onTextChunk`, `onAudioFrame`）。

- **Application Call（智能体/工作流调用）**：仅 OpenAI 兼容的 Responses API 支持 `stream=true` 参数；DashScope 原生应用调用接口暂不支持流式。**关键前提**：工作流应用必须在结束节点显式开启“流式输出”开关并重新发布，否则即使客户端传 `stream=true` 也降级为非流式响应。

- **[多模态](multi-modal.md)模型（如 Qwen-VL、Tripo、Fun-Music）**：目前**不支持流式输出**。图像、3D、视频、音乐等生成任务均为同步完成，返回完整二进制或 URL 结果。

## 关键参数和配置

| 参数 | 类型 | 说明 | 适用接口 | 注意事项 |
|------|------|------|----------|----------|
| `stream` | boolean | 启用流式响应开关 | Qwen API（DashScope & OpenAI 兼容）、Application Call（Responses API） | 必须设为 `true`；HTTP 请求头需保持 `Connection: keep-alive`，响应 Content-Type 为 `text/event-stream`（SSE）或 `application/octet-stream`（WebSocket） |
| `output_modalities` | array | 指定输出模态组合 | Omni Realtime API、Realtime API | 如 `["TEXT"]` 或 `["TEXT", "AUDIO"]`；影响流式事件类型与频率 |
| `turn_detection.type` | string | VAD 类型，影响语音输入与文本输出节奏 | Omni Realtime API | `"semantic_vad"` 可触发更自然的语义级流式中断，仅 `qwen3.5-omni-realtime` 支持 |
| `smooth_output` | boolean | 控制 TTS 输出是否口语化分段（避免生硬停顿） | `qwen3-omni-flash-realtime` | 仅该模型支持；设为 `true` 时，文本流更贴近自然说话节奏 |

> ⚠️ 注意：  
> - 流式响应下，错误不会延迟抛出——若请求中途失败（如鉴权失败、token 耗尽），服务端会立即发送 `error` 事件并关闭连接；  
> - 客户端必须正确处理 partial chunk（如 [OpenAI 兼容接口](openai-compatible-interface.md)中 `delta.content` 可能为空字符串，表示换行或格式标记）；  
> - 所有流式接口均**不支持重试幂等性**，重复发送相同 `stream=true` 请求会产生独立流，需由客户端自行管理会话状态。

## 面向开发者：简洁实用建议

- ✅ **首选 SDK**：使用 `dashscope` Python SDK（v1.20.0+）或官方 Realtime SDK，内置流式解析器与自动重连逻辑，避免手动解析 SSE 或 WebSocket 事件。
- ✅ **文本流拼接**：OpenAI 兼容接口中，始终检查 `delta.content` 是否为 `None` 或空字符串，仅追加非空内容；DashScope 接口关注 `output.text` 字段，忽略 `output.choices[0].finish_reason` 为 `null` 的中间响应。
- ✅ **音频流播放**：Omni Realtime 的 PCM 音频流采样率固定为 24kHz，位深 16bit，单声道；建议使用 Web Audio API 或 Android AudioTrack 进行 buffer 管理，避免卡顿。
- ❌ **避免滥用**：非实时场景（如批量摘要、离线报告生成）请使用非流式接口，减少连接开销与资源占用。
- 🔍 **调试技巧**：启用 `debug=true`（部分接口支持）可查看 token 级别生成过程；结合 `X-DashScope-Trace-ID` 头定位流式异常链路。

## 关联主题页

- [qwen api reference](../api/qwen-api-reference.md)
- [omni realtime api](../api/omni-realtime-api.md)
- [realtime api user guide](../api/realtime-api-user-guide.md)
- [model experience](../guides/model-experience.md)
- [application call](../api/application-call.md)



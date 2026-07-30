# 流式输出

流式输出（Streaming Output）是指模型服务在生成响应过程中，将结果分块（chunk）实时、渐进地返回给客户端，而非等待全部内容生成完毕后一次性返回。这种机制显著降低端到端延迟，提升交互自然感，是实时语音对话、长文本生成、智能助手等场景的核心能力支撑。

## 在百炼平台的不同场景中如何使用

流式输出在百炼平台覆盖三大类调用路径，适用性与启用方式各不相同：

- **Realtime API（AOQ/WebRTC/WebSocket）**：原生支持流式输出，无需额外参数。服务端通过事件流（如 `response.text.delta`、`response.audio.delta`）持续推送增量内容，客户端按需拼接、渲染或播放。适用于低延迟多模态交互（如语音问答、实时翻译），音频/文本均以毫秒级粒度流式下发。

- **Qwen 系列标准模型（DashScope 原生 / OpenAI 兼容 / Anthropic 兼容）**：通过 `stream=true` 参数启用。[OpenAI 兼容接口](openai-compatible-interface.md)返回符合 SSE（Server-Sent Events）规范的流式响应；DashScope 原生接口返回 JSON Lines 格式（每行一个 `{"output": {"text": "..."}}` 对象）。适用于文本生成、代码补全、多轮对话等通用场景。

- **应用调用（Application Call）**：仅同步调用（`background=false`）支持流式输出，需显式设置 `stream=true`。工作流应用还需在控制台“结束节点”手动开启「流式输出」开关；新版/旧版智能体默认支持。异步调用（`background=true`）**不支持流式输出**，必须轮询获取最终结果。

> ⚠️ 注意：流式输出要求客户端具备流式解析能力（如处理 SSE、逐行读取 JSON Lines、监听 WebSocket 事件），且需自行处理 chunk 拼接、中断恢复、超时重连等逻辑。

## 关键参数和配置

| 参数 | 所属场景 | 类型 | 说明 | 是否必需 |
|------|----------|------|------|-----------|
| `stream` | Qwen API、Application Call | `boolean` | 启用流式响应模式 | 否（默认 `false`） |
| `modalities: ["text", "audio"]` | Realtime API、Omni Realtime API | `array` | 指定输出模态，决定是否流式返回音频 | 是（影响流式内容类型） |
| `turn_detection.type` | Omni Realtime API | `string` | `semantic_vad` 或 `server_vad`，影响语音输入切分与响应触发时机，间接影响流式节奏 | 否（默认 `server_vad`） |
| `smooth_output` | Omni Realtime API（`qwen3.5-omni-plus/flash-realtime`） | `boolean` | 启用音频平滑合成，减少流式音频断点，提升听感连续性 | 否（默认 `false`） |
| `idle_timeout_ms` | Omni Realtime API（`qwen3.5-omni-plus/flash-realtime` + `server_vad`） | `integer` | 静默超时后主动引导，确保流式会话不中断 | 否 |

- **无全局开关**：流式能力由协议层和模型能力共同决定，不可跨协议强制启用（例如 AOQ 协议不支持 OpenAI 兼容流式格式）。
- **音频流式约束**：Realtime/Omni API 的音频流固定为 PCM 格式、24 kHz 采样率，客户端需按帧接收并实时播放，不可跳过或缓存整段再播。
- **错误处理**：流式过程中若发生中断（如网络闪断、服务端异常），需监听 `error` 事件或检查 HTTP 状态码，主动重建连接或会话。

## 面向开发者：简洁实用建议

- ✅ **首选 WebSocket Realtime API**：若需音视频+文本全流式，直接使用 Omni Realtime API（WebSocket 协议），事件语义清晰，SDK 封装完善。
- ✅ **文本生成用 OpenAI 兼容流式**：已有 OpenAI 生态的项目，复用 `openai>=1.0` SDK 的 `stream=True` 即可，兼容性好、调试方便。
- ✅ **应用集成加 `stream=true`**：调用已发布智能体或工作流时，同步请求中添加 `stream=true`，配合 DashScope SDK 的 `Application.call(..., stream=True)` 最简接入。
- ❌ **勿在异步调用中设 `stream=true`**：该组合无效，API 将忽略该参数并返回完整结果。
- ⚙️ **流式必配超时与重试**：所有流式请求应设置 `timeout=60s+`（Realtime 建议 120s），并实现基于 `session_id` 或 `task_id` 的断点续传逻辑。
- 📈 **监控关键指标**：关注首字节延迟（TTFB）、chunk 间隔抖动、丢包率（音频流）、`response.text.done` / `response.audio.done` 事件到达完整性，用于优化 VAD 配置与网络策略。

## 关联主题页

- [realtime api user guide](../api/realtime-api-user-guide.md)
- [omni realtime api](../api/omni-realtime-api.md)
- [qwen api reference](../api/qwen-api-reference.md)
- [application call](../api/application-call.md)
- [more about models](../api/more-about-models.md)



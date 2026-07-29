# realtime api user guide

Realtime API 是一套面向低延迟、弱网对抗和多模态实时交互场景的协议化接入方案，支持 WebSocket、WebRTC 和 AOQ 三种传输协议，开发者可根据终端类型、部署环境与业务需求选择最适配的接入方式。所有协议均基于统一的事件驱动模型，通过 `session.update` 配置会话、`input_audio_buffer.append` 等事件流式输入数据，并接收 `response.text.delta`、`response.audio.delta` 等增量响应。

## 支持的模型/功能

Realtime API 当前支持以下核心模型与应用类型，不同协议的支持能力存在差异：

| 模型/应用类型 | AOQ | WebRTC | WebSocket |
|---------------|-----|--------|-----------|
| 实时全模态（qwen3.5-omni-plus-realtime、qwen3.5-omni-flash-realtime） | ✅ | ✅ | ✅ |
| 实时语音翻译（qwen3.5-livetranslate-flash-realtime） | ✅ | ✅ | ✅ |
| 多模态开发套件（multimodal-dialog） | ❌ | ✅ | ✅ |
| 实时语音识别（Fun-ASR系列） | ❌ | ❌ | ✅ |
| 实时语音合成（CosyVoice系列） | ❌ | ❌ | ✅ |
| 实时语音对话（qwen-audio-3.0-realtime-plus/flash） | ❌ | ❌ | ✅ |

> **注意**：文档 [通过WebRTC使用多模态交互套件实现实时通话](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-best-practices/best-practice-webrtc-multimodal-dialog.md) 明确指出 `multimodal-dialog` 仅支持 WebRTC 和 WebSocket；而 [Realtime API简介](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-overview.md) 的表格中亦标注 AOQ 不支持该套件。二者一致，无矛盾。

AOQ 与 WebRTC 均内置回声消除（AEC）和降噪能力，WebSocket 方案需客户端自行处理；AOQ 和 WebRTC 支持音视频+文本混合传输，WebSocket 仅支持文本/音频/图像分通道传输，不支持原生多模态融合。

## 关键参数

### 协议级通用参数
- `Authorization: Bearer <API_KEY>`：建连阶段必需的鉴权头，**严禁硬编码于客户端**，生产环境应由业务 AppServer 代理请求或使用 [Token](../concepts/token.md) 机制（AOQ 必须）。
- `model`：URL 查询参数，指定目标模型或应用，如 `qwen3.5-omni-plus-realtime` 或 `multimodal-dialog`。
- `workspace_id`：百炼工作空间唯一标识，用于路由至对应服务实例，格式为 `llm-xxxxxxxxxx`。

### 会话配置参数（`session.update` 事件）
- `modalities`: `["text", "audio"]` 等数组，声明期望输出模态。
- `voice`: 输出音频音色名（如 `"Ethan"`），仅当 `audio` 在 `modalities` 中时生效。
- `input_audio_format` / `output_audio_format`: 当前仅支持 `"pcm"`。
- `turn_detection`: VAD 配置对象，`type` 可选 `"server_vad"` 或 `"semantic_vad"`（推荐用于 qwen3.5-omni 系列）；`silence_duration_ms` 控制静音阈值，默认 800ms。
- `instructions`: 系统角色提示词，影响模型行为。

### 协议特有参数
- **WebRTC**: SDP 交换需 `Content-Type: application/sdp`；服务端 endpoint 格式为 `{workspace_id}.{region}.maas.aliyuncs.com`。
- **AOQ**: 必须使用 `x-dashscope-rtc-transport: moq` 请求头；建连凭证含 `aoqTokenForClient`、`sid`、`clientRelayEndpoints` 等字段，详见 [Token鉴权](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-quick-start-guide/realtime-token-authentication.md)。
- **WebSocket**: 连接 URL 为 `wss://dashscope.aliyuncs.com/...`，握手阶段携带 `Authorization` 头。

## 使用方式

### 协议选择指南
- **WebSocket**: 适用于服务端集成、快速原型验证、浏览器外环境（如 Node.js CLI 工具）。接入成本最低，但弱网对抗与 AI 场景适配性较弱。
- **WebRTC**: 适用于浏览器端实时互动（如网页版智能客服），依赖原生浏览器能力，需处理 CORS 限制（SDP 交换需后端代理）。
- **AOQ**: 适用于 Android/iOS/HarmonyOS 原生 App，对延迟、弱网、多模态有极致要求，需集成 [AOQ SDK](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-quick-start-guide/realtime-sdk-download.md) 并管理 [Token](../concepts/token.md)。

### 核心流程（以 AOQ 为例）
1. **初始化引擎**：调用 `createEngine`，设置 `AoqEngineDelegate` 回调。
2. **启动采集**：`startAudioCapture()` + `startVideoCapture()`（可选），支持内部/外部采集模式。
3. **获取凭证**：业务 AppServer 向百炼网关请求 [Token](../concepts/token.md)（见 [Token鉴权](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-quick-start-guide/realtime-token-authentication.md)）。
4. **建连控制**：调用 `connect(config)` 前，务必 `enableSendMediaStream(.audio, false)` 暂停发送；收到 `session.updated` 事件后，再 `enableSendMediaStream(.audio, true)` 开启（见 [媒体流发送管理](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-function/aoq-media-stream-control.md)）。
5. **事件交互**：通过 `send()` 发送 `session.update`、`input_audio_buffer.append` 等事件；通过 `onDataMsg` 处理 `response.text.delta`、`response.audio.delta` 等响应。

### WebRTC 注意事项
- 浏览器端无法直连百炼网关（CORS 限制），SDP 交换必须由业务后端代理，**禁止在前端代码中暴露 API Key**。
- `RTCPeerConnection` 应配置 `iceServers: []`（服务端 ICE-lite 模式），无需 STUN/TURN 服务器。
- 视频发送需通过 Canvas 降帧（如 2fps）并 `replaceTrack(null)` 实现门控，确保 `session.created` 后才推送媒体流（见 [通过WebRTC使用qwen3.5-omni-plus-realtime实现实时通话](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-best-practices/best-practice-webrtc-omni-realtime.md)）。

## 限制和注意事项

- **并发与限流**：所有协议共享百炼平台的并发限流策略，具体配额请参考 [限流文档](https://help.aliyun.com/zh/model-studio/rate-limit)，未明确说明的默认值以控制台为准。
- **浏览器兼容性**：WebRTC 仅支持现代浏览器（Chrome/Edge/Firefox/Safari），AOQ 不支持浏览器环境。
- **媒体流同步**：AOQ 协议下，`enableSendMediaStream` 是强制控制点——模型未返回 `session.updated` 前发送媒体流将被丢弃或导致连接异常；WebSocket/WebRTC 无此严格约束，但强烈建议遵循相同模式以保证稳定性。
- **SDK 版本**：AOQ Client SDK v1.0.1 起支持 Opus 编解码插件（需单独下载 [libPluginOpus](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-quick-start-guide/realtime-sdk-download.md)），未加载插件时仅支持 PCM。
- **音频设备管理**：AOQ SDK 的 `isVoipMode` 参数影响硬件 AEC 行为，且扬声器切换（`enableSpeakerphone`）仅在 VoIP 模式下有效；非 VoIP 模式下调用将触发 `AoqECAudioDeviceEarpieceRequiresVoipMode` 错误（见 [音频常用功能介绍](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-function/aoq-audio-features.md)）。
- **自定义采集/播放**：若需外部音频/视频源（如 TTS 输出、屏幕录制），必须先调用 `startAudioCapture({isExternal:true})` 或 `startVideoCapture({isExternal:true})`，再通过 `pushAudioExternalStreamData` / `pushExternalVideoCapturedFrame` 推送数据，否则 SDK 不消费帧（见 [自定义音频采集](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-function/aoq-custom-audio-capture.md) 和 [自定义视频输入](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-function/aoq-custom-video-input.md)）。

## 来源文档

- [Realtime API简介](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-overview.md)
- [通过WebRTC使用多模态交互套件实现实时通话](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-best-practices/best-practice-webrtc-multimodal-dialog.md)
- [通过WebRTC使用qwen3.5-omni-plus-realtime实现实时通话](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-best-practices/best-practice-webrtc-omni-realtime.md)
- [通过AOQ使用qwen3.5-omni-plus-realtime实现实时通话](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-best-practices/best-practice-aoq-omni-realtime.md)
- [SDK下载](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-quick-start-guide/realtime-sdk-download.md)
- [Token鉴权](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-quick-start-guide/realtime-token-authentication.md)
- [实现接通模型/应用](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-quick-start-guide/realtime-connect-model.md)
- [AOQ SDK简介](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-desc.md)
- [连接状态管理](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-function/aoq-connection-management.md)
- [音频常用功能介绍](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-function/aoq-audio-features.md)
- [媒体流发送管理](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-function/aoq-media-stream-control.md)
- [自定义音频采集](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-function/aoq-custom-audio-capture.md)
- [自定义音频播放](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-function/aoq-custom-audio-playback.md)
- [自定义视频输入](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-function/aoq-custom-video-input.md)
- [视频常用功能介绍](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-function/aoq-video-features.md)



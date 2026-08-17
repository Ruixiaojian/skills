# realtime api user guide

Realtime API 是百炼平台面向低延迟、高可靠性实时交互场景提供的核心能力，支持 AOQ、WebRTC 和 WebSocket 三种传输协议，覆盖语音识别（ASR）、语音合成（TTS）、多模态对话、实时翻译等全栈 AI 实时服务。开发者可根据终端类型、网络环境、功能需求和接入成本选择最适配的协议方案，并通过统一的事件驱动模型与模型/应用交互。

## 支持的模型/功能

Realtime API 当前支持以下模型与应用类型，但**不同协议的支持范围存在显著差异**：

- **实时全模态**（`qwen3.5-omni-plus-realtime`, `qwen3.5-omni-flash-realtime`）：全部协议（AOQ/WebRTC/WebSocket）均支持。
- **实时语音翻译**（`qwen3.5-livetranslate-flash-realtime`）：全部协议均支持。
- **多模态开发套件**（`multimodal-dialog`）：全部协议均支持。
- **实时语音识别**（`Qwen-Audio-3.0-ASR-Flash-Streaming`, `Fun-ASR-Realtime` 系列）：**仅 AOQ 和 WebSocket 支持，WebRTC 不支持** [Realtime API 概述](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-overview.md)。
- **实时语音合成**（`CosyVoice` 系列、`qwen-audio-3.0-tts-flash`、`qwen-audio-3.0-tts-plus`）：**仅 AOQ 和 WebSocket 支持，WebRTC 不支持** [Realtime API 概述](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-overview.md)。
- **实时语音对话**（`qwen-audio-3.0-realtime-plus`, `qwen-audio-3.0-realtime-flash`）：全部协议均支持。

> **注意**：文档 1 明确指出 WebRTC 不支持 ASR/TTS 类模型，但文档 4 的 WebRTC 接入示例中未体现此限制，且未提供替代方案。实际接入时请以文档 1 的模型支持矩阵为准，避免在 WebRTC 场景下误用 ASR/TTS 模型。

## 关键参数

### 协议选择参数
- `x-dashscope-rtc-transport`：HTTP 请求头字段，用于显式指定协议。取值为 `moq`（AOQ）、`webrtc`（WebRTC）或 `websocket`（WebSocket）。该参数必须在建连请求中携带，否则默认行为未定义。

### 鉴权参数
- `Authorization: Bearer <API_KEY>`：所有协议建连时必需的 HTTP 头，用于身份认证。**AOQ 协议要求 API Key 仅在服务端（AppServer）使用**，客户端通过网关返回的 `aoqTokenForClient` 建连，严禁将 API Key 暴露在客户端代码中 [Token鉴权](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-quick-start-guide/realtime-token-authentication.md)。

### 会话配置参数（`session.update` 事件）
- `modalities`: 指定输出模态，如 `["text"]` 或 `["text","audio"]`。
- `voice`: 输出音频音色（TTS 相关）。
- `input_audio_format` / `output_audio_format`: 当前仅支持 `pcm`。
- `turn_detection`: 语音活动检测（VAD）配置，`type` 可选 `server_vad` 或 `semantic_vad`（推荐后者）。

## 使用方式

### 协议选型指南
- **AOQ**：适用于对延迟、弱网对抗、多模态混合传输有极致要求的移动端原生应用（Android/iOS/HarmonyOS/Linux），内置回声消除与降噪，需集成 [AOQ SDK](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-quick-start-guide/realtime-sdk-download.md)。
- **WebRTC**：适用于浏览器端实时互动或已有 WebRTC 基础设施的场景，依赖浏览器原生能力，无专用 SDK。
- **WebSocket**：适用于服务端集成、快速原型验证或跨平台轻量接入，可通过 DashScope SDK 快速实现。

### AOQ 标准接入流程
1. **服务端鉴权**：业务 AppServer 调用百炼网关 allocate 接口，传入 `model` 和 `clientIp`，获取 `aoqTokenForClient`、`sid`、`clientRelayEndpoints` 等凭证。
2. **客户端连接**：使用 AOQ SDK 的 `connect()` 方法，传入上述凭证配置 `AoqConnectConfig`。
3. **媒体流控制**：建连后默认发送媒体流，但**必须等待收到服务端 `session.updated` 事件后，再调用 `enableSendMediaStream(.audio, true)` 开启音频发送**，否则服务端可能拒绝接收数据 [媒体流发送管理](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-function/aoq-media-stream-control.md)。
4. **自定义采集/播放（可选）**：如需接管音频/视频源，需在 `startAudioCapture()` 或 `startVideoCapture()` 中设置 `isExternal=true`，并通过 `pushAudioExternalStreamData()` 或 `pushExternalVideoCapturedFrame()` 推送数据 [自定义音频采集](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-function/aoq-custom-audio-capture.md)、[自定义视频输入](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-function/aoq-custom-video-input.md)。

### WebRTC 与 WebSocket
- WebRTC：通过标准 SDP 交换建立连接，详见 [接入模型与应用](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-quick-start-guide/realtime-connect-model.md)。
- WebSocket：使用 DashScope SDK 的 `RealtimeClient` 类，传入 `model` 和 `api_key` 即可初始化，无需处理底层握手。

## 限制和注意事项

- **AOQ 连接状态管理**：SDK 提供明确的状态机（`Connecting` → `Connected`/`Failed` → `Disconnected`）。`Failed` 是瞬态，SDK 会自动迁移到 `Disconnected`，业务层无需在 `onConnectionStatusChange(Failed)` 后手动调用 `disconnect()` [连接状态管理](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-function/aoq-connection-management.md)。
- **Opus 编解码依赖**：AOQ SDK 使用插件方式加载 Opus，集成时**必须下载并加载 `libPluginOpus`（Android/iOS/HarmonyOS）或 `PluginOpus.framework`（iOS）**，否则 ASR/TTS 功能不可用 [SDK下载](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-quick-start-guide/realtime-sdk-download.md)。
- **外部音频流推送**：实时采集建议每 10ms 推送一帧；若 `pushAudioExternalStreamData()` 返回错误码 `110`（缓冲区满），应短暂 `sleep(30ms)` 后重试，**切勿丢弃数据** [自定义音频采集](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-function/aoq-custom-audio-capture.md)。
- **安全红线**：API Key 绝对禁止硬编码到客户端、提交至代码仓库或通过前端接口直接下发。必须通过服务端代理鉴权或环境变量安全管理。

## 来源文档

- [Realtime API 概述](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-overview.md)
- [SDK下载](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-quick-start-guide/realtime-sdk-download.md)
- [Token鉴权](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-quick-start-guide/realtime-token-authentication.md)
- [接入模型与应用](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-quick-start-guide/realtime-connect-model.md)
- [AOQ SDK简介](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-desc.md)
- [连接状态管理](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-function/aoq-connection-management.md)
- [媒体流发送管理](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-function/aoq-media-stream-control.md)
- [音频常用功能介绍](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-function/aoq-audio-features.md)
- [自定义音频采集](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-function/aoq-custom-audio-capture.md)
- [视频常用功能介绍](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-function/aoq-video-features.md)
- [自定义视频输入](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-function/aoq-custom-video-input.md)
- [自定义音频播放](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-function/aoq-custom-audio-playback.md)



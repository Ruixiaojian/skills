# realtime api user guide

Realtime API 是百炼平台提供的低延迟、高可靠实时 AI 交互能力，支持 AOQ、WebRTC 和 WebSocket 三种传输协议，面向[多模态](../concepts/multi-modal.md)实时对话、语音识别/合成、实时翻译等场景。开发者可根据终端类型、网络环境、功能需求和接入成本选择最适配的协议方案，并通过统一的模型接口与服务交互。

## 支持的模型/功能

Realtime API 当前支持以下模型与应用类型，但**协议支持存在差异**：

- **实时全模态**（`qwen3.5-omni-plus-realtime`, `qwen3.5-omni-flash-realtime`）：全部三种协议均支持 [Realtime API 概述](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-overview.md)  
- **实时语音翻译**（`qwen3.5-livetranslate-flash-realtime`）：全部三种协议均支持  
- **[多模态](../concepts/multi-modal.md)开发套件**（`multimodal-dialog`）：全部三种协议均支持  
- **实时语音识别**（`Qwen-Audio-3.0-ASR-Flash-Streaming`, `Fun-ASR-Realtime` 系列）：**仅 AOQ 和 WebSocket 支持**，WebRTC 不支持  
- **实时语音合成**（`CosyVoice` 系列）：**仅 AOQ 和 WebSocket 支持**，WebRTC 不支持  
- **实时语音对话**（`qwen-audio-3.0-realtime-plus`, `qwen-audio-3.0-realtime-flash`）：全部三种协议均支持  

> **注意**：文档 1 明确指出 WebRTC 不支持 ASR 和 TTS 类模型，但文档 4 的 WebRTC 接入示例中未强调此限制，且未提供替代方案。实际集成时请以文档 1 的模型支持矩阵为准，避免在 WebRTC 场景下误用 ASR/TTS 模型。

## 关键参数

| 参数 | 协议适用性 | 说明 |
|------|------------|------|
| `model` | 全部 | 必填，指定目标模型名称，如 `qwen3.5-omni-plus-realtime`；需与所选协议支持范围匹配 |
| `Authorization: Bearer <API_KEY>` | 全部 | 建连阶段 HTTP Header 鉴权凭证；**AOQ 协议中 API Key 仅用于服务端网关请求，客户端使用 `aoqTokenForClient`** [Token鉴权](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-quick-start-guide/realtime-token-authentication.md) |
| `x-dashscope-rtc-transport: moq` | AOQ | 请求头标识，显式指定使用 AOQ 协议 |
| `clientIp` | AOQ（选填） | 客户端真实公网 IP，用于 Relay 节点最优路由；不填则默认使用网关请求 IP |
| `sid`, `aoqTokenForClient`, `clientRelayEndpoints` | AOQ | AOQ 连接必需凭证，由服务端 allocate 接口返回，客户端 SDK 直接使用 [Token鉴权](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-quick-start-guide/realtime-token-authentication.md) |
| `Content-Type: application/sdp` | WebRTC | SDP 交换阶段必需，非 JSON 格式 |
| `input_audio_format` / `output_audio_format` | AOQ/WebRTC | 当前仅支持 `pcm`；输入采样率通常为 16 kHz，输出为 24 kHz（详见 [接入模型与应用](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-quick-start-guide/realtime-connect-model.md)） |
| `turn_detection.type` | AOQ/WebRTC | VAD 类型，`semantic_vad` 推荐用于 `qwen3.5-omni-realtime` 系列；WebRTC 仅支持服务端 VAD，不支持手动模式 |

## 使用方式

### 协议选择与接入路径
- **AOQ**：适用于 Android/iOS/HarmonyOS 原生 App，需集成 [AOQ SDK](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-quick-start-guide/realtime-sdk-download.md)，流程为：服务端申请凭证 → 客户端 SDK 连接 → `session.update` → 启用媒体流。关键控制点包括 `enableSendMediaStream` 精确管理发送时机 [媒体流发送管理](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-function/aoq-media-stream-control.md)。
- **WebRTC**：适用于浏览器端，无需专用 SDK，直接使用原生 WebRTC API；建连依赖 SDP 交换，需白名单开通 Endpoint；媒体流通过 RTP 自动传输，无需手动推送 buffer 事件 [接入模型与应用](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-quick-start-guide/realtime-connect-model.md)。
- **WebSocket**：适用于服务端或快速原型验证，接入门槛最低；通过 `wss://dashscope.aliyuncs.com/api-ws/v1/realtime?model=...` 直连，鉴权简单，但无内置弱网对抗与音视频处理能力。

### 核心操作示例（AOQ）
1. **连接前禁用媒体流**：调用 `engine.enableSendMediaStream(.audio, enable: false)` 避免模型未就绪时数据丢失。
2. **收到 `session.updated` 后启用**：在 `onDataMsg` 回调中解析事件，再调用 `enableSendMediaStream(.audio, enable: true)`。
3. **自定义音频采集/播放**：通过 `startAudioCapture(isExternal: true)` + `pushAudioExternalStreamData()` 或 `startAudioPlayer(isExternal: true)` + `onPlaybackAudioFrame` 实现深度控制 [自定义音频采集](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-function/aoq-custom-audio-capture.md)、[自定义音频播放](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-function/aoq-custom-audio-playback.md)。
4. **自定义视频输入**：支持原始帧（I420/NV12/BGRA）或编码帧（JPEG）两种模式，分别调用 `pushExternalVideoCapturedFrame()` 或 `pushExternalVideoEncodedFrame()` [自定义视频输入](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-function/aoq-custom-video-input.md)。

## 限制和注意事项

- **协议兼容性限制**：WebRTC 不支持 ASR 和 TTS 模型，若业务需语音识别或合成，请选用 AOQ 或 WebSocket 协议。
- **AOQ 连接状态管理**：SDK 状态机为 `Connecting` → `Connected`/`Failed` → `Disconnected`；`Failed` 为瞬态，SDK 自动迁移至 `Disconnected`，业务层无需在 `onConnectionStatusChange(.failed)` 中调用 `disconnect` [连接状态管理](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-function/aoq-connection-management.md)。
- **媒体流控制强制要求**：AOQ 协议下，**必须在收到服务端 `session.updated` 事件后才调用 `enableSendMediaStream(true)`**；提前发送会导致服务端丢弃数据或连接异常。
- **Opus 编解码依赖**：AOQ SDK 需额外下载并加载 Opus 插件（`libPluginOpus.zip` 或 `PluginOpus.framework.zip`），否则音频功能不可用 [SDK下载](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-quick-start-guide/realtime-sdk-download.md)。
- **安全规范**：API Key **严禁硬编码于客户端代码或提交至代码仓库**，应通过后端服务下发临时 [Token](../concepts/token.md) 或使用服务端代理模式（AOQ 推荐） [Token鉴权](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-quick-start-guide/realtime-token-authentication.md)。

## 来源文档

- [Realtime API 概述](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-overview.md)
- [SDK下载](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-quick-start-guide/realtime-sdk-download.md)
- [Token鉴权](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-quick-start-guide/realtime-token-authentication.md)
- [接入模型与应用](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-quick-start-guide/realtime-connect-model.md)
- [连接状态管理](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-function/aoq-connection-management.md)
- [媒体流发送管理](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-function/aoq-media-stream-control.md)
- [自定义音频播放](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-function/aoq-custom-audio-playback.md)
- [自定义音频采集](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-function/aoq-custom-audio-capture.md)
- [自定义视频输入](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-function/aoq-custom-video-input.md)
- [音频常用功能介绍](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-function/aoq-audio-features.md)
- [视频常用功能介绍](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-function/aoq-video-features.md)



# realtime api user guide

Realtime API 是百炼平台面向低延迟、高可靠性实时交互场景提供的统一接入层，支持 AOQ（AI over QUIC）、WebRTC 和 WebSocket 三种传输协议，覆盖语音识别、语音合成、多模态对话、实时翻译等全栈 AI 实时能力。开发者可根据终端类型、网络环境、功能需求和工程成熟度选择最适配的协议方案。

## 支持的模型/功能

Realtime API 当前支持以下模型与应用类型，但**协议支持存在差异**：

- **实时全模态**（`qwen3.5-omni-plus-realtime`, `qwen3.5-omni-flash-realtime`）：全部协议（AOQ/WebRTC/WebSocket）均支持 [Realtime API 概述](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-overview.md)  
- **实时语音翻译**（`qwen3.5-livetranslate-flash-realtime`）：全部协议支持  
- **多模态开发套件**（`multimodal-dialog`）：全部协议支持  
- **实时语音识别**（`Qwen-Audio-3.0-ASR-Flash-Streaming`, `Fun-ASR-Realtime` 系列）：仅 AOQ 和 WebSocket 支持；**WebRTC 不支持**  
- **实时语音合成**（`CosyVoice` 系列、`qwen-audio-3.0-tts-flash`/`plus`）：仅 AOQ 和 WebSocket 支持；**WebRTC 不支持**  
- **实时语音对话**（`qwen-audio-3.0-realtime-plus`, `qwen-audio-3.0-realtime-flash`）：全部协议支持  

> **注意**：文档 1 明确列出 WebRTC 对 ASR/TTS 模型“不支持”，但文档 5 的“WebRTC 接入”章节未强调此限制，且未提供替代方案示例。实际集成时请以文档 1 的模型支持矩阵为准，避免在 WebRTC 场景中误用 ASR/TTS 模型。

## 关键参数

| 参数 | 协议适用性 | 说明 |
|------|------------|------|
| `Authorization: Bearer <API_KEY>` | 全协议 | 建连阶段 HTTP Header 鉴权，**API Key 必须由服务端持有并用于请求网关**；客户端仅使用网关返回的临时 `aoqTokenForClient`（AOQ）或直接携带（WebSocket/WebRTC）[Token鉴权](../../raw/model-api-reference/realtime-api-user-guide/realtime-token-authentication.md) |
| `x-dashscope-rtc-transport: moq` | AOQ 专用 | 标识使用 AOQ 协议，必须在建连请求中显式声明 |
| `clientIp`（请求体） | AOQ 专用 | 客户端真实公网 IP，用于 Relay 接入点智能调度；不填则默认使用网关出口 IP |
| `sid`, `aoqTokenForClient`, `clientRelayCertFingerprint`, `clientRelayEndpoints` | AOQ 专用 | 由服务端调用 `/api/v1/webrtc/realtime` 分配返回，客户端 SDK 连接必需 |
| `session.update` 事件中的 `modalities`, `voice`, `input_audio_format`, `output_audio_format`, `instructions`, `turn_detection` | 全协议（语义一致） | 会话初始化配置，决定输出模态（文本/音频）、音色、音频格式（PCM）、系统指令及 VAD 行为；其中 `turn_detection.type` 推荐对 `qwen3.5-omni-realtime` 系列设为 `semantic_vad` |

## 使用方式

### 协议选型与接入路径
- **AOQ**：适用于移动端原生 App（Android/iOS/HarmonyOS/Linux），需集成 [AOQ SDK](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-desc.md)，流程为：服务端分配凭证 → 客户端 `createEngine` → `connect` → 收到 `session.updated` 后调用 `enableSendMediaStream(true)` 开启媒体流。
- **WebRTC**：适用于浏览器端或已有 WebRTC 基础设施的场景，**无官方 SDK**，需基于标准 WebRTC API（如 `RTCPeerConnection`）实现 SDP 交换与 DataChannel 通信。
- **WebSocket**：适用于服务端集成或快速原型验证，接入门槛最低，可直接通过 DashScope SDK 或原生 WebSocket 库连接。

### 核心控制逻辑（AOQ）
- **连接状态管理**：SDK 提供明确的状态机（`Connecting` → `Connected`/`Failed` → `Disconnected`），业务需监听 `onConnectionStatusChange` 回调处理状态迁移 [连接状态管理](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-function/aoq-connection-management.md)。
- **媒体流发送时机**：必须在收到服务端 `session.updated` 事件后，再调用 `enableSendMediaStream(.audio, true)` 和 `enableSendMediaStream(.video, true)`，否则服务端可能拒绝接收数据 [媒体流发送管理](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-function/aoq-media-stream-control.md)。
- **自定义音视频处理**：支持外部采集/播放模式，通过 `isExternal=true` 关闭 SDK 内置模块，并使用 `pushAudioExternalStreamData` 或 `onPlaybackAudioFrame` 等接口接管 PCM 数据流，适用于 TTS 输出、ASR 输入、音效处理等高级场景。

## 限制和注意事项

- **API Key 安全**：严禁将 API Key 硬编码至客户端代码或提交至代码仓库；AOQ 协议强制要求服务端代理鉴权，客户端仅使用临时 [Token](../concepts/token.md)，此设计显著提升安全性。
- **模型兼容性**：部分模型（如 ASR/TTS）不支持 WebRTC 协议，强行接入将导致建连失败或功能异常；务必依据 [Realtime API 概述](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-overview.md) 中的模型支持矩阵选择协议。
- **音频/视频格式约束**：
  - 输入音频：当前仅支持 `pcm` 格式，采样率需匹配模型要求（如 Omni 系列要求 16 kHz）。
  - 输出音频：当前仅支持 `pcm` 格式，采样率为 24 kHz。
  - 视频编码：原始帧模式支持 I420/NV12/NV21/BGRA/RGBA；编码帧模式当前**仅支持 JPEG**。
- **资源管理**：调用 `pushAudioExternalStreamData` 或 `pushExternalVideoCapturedFrame` 时，若返回错误码 `110`（缓冲区满），需短暂休眠（如 30ms）后重试，不可丢弃数据；引擎销毁前必须停止所有推送循环并移除外部流。
- **平台差异**：iOS 的 `CVPixelBuffer`、Android 的 `TextureOES` 等零拷贝格式需按平台规范正确管理内存引用；OHOS 平台需使用 `XComponent` 作为渲染容器。

## 来源文档

- [Realtime API 概述](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-overview.md)
- [SDK下载](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-quick-start-guide/realtime-sdk-download.md)
- [AOQ SDK简介](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-desc.md)
- [Token鉴权](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-quick-start-guide/realtime-token-authentication.md)
- [接入模型与应用](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-quick-start-guide/realtime-connect-model.md)
- [连接状态管理](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-function/aoq-connection-management.md)
- [媒体流发送管理](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-function/aoq-media-stream-control.md)
- [音频常用功能介绍](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-function/aoq-audio-features.md)
- [自定义音频播放](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-function/aoq-custom-audio-playback.md)
- [自定义音频采集](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-function/aoq-custom-audio-capture.md)
- [视频常用功能介绍](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-function/aoq-video-features.md)
- [自定义视频输入](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-function/aoq-custom-video-input.md)



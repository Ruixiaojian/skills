# realtime api user guide

Realtime API 是百炼平台面向实时多模态交互场景提供的低延迟、高可靠通信能力，支持 AOQ、WebRTC 和 WebSocket 三种传输协议，覆盖移动端原生应用、浏览器端互动及服务端快速集成等不同需求。开发者可根据业务对延迟、弱网对抗、平台兼容性及接入复杂度的要求，选择最适配的协议方案。

## 支持的模型/功能

Realtime API 当前支持以下核心模型与应用类型，但**协议支持存在显著差异**：

- **实时全模态模型**（如 `qwen3.5-omni-plus-realtime`、`qwen3.5-omni-flash-realtime`）：  
  ✅ 全协议支持（AOQ / WebRTC / WebSocket）  
  > **注意**：文档 1 中明确指出 AOQ 和 WebRTC 均支持该类模型，而 WebSocket 仅支持文本/音频/图像，不支持视频流；但文档 4 的 AOQ 接入示例中配置了 `["text","audio"]` 模态，未启用视频，实际使用需以[模型/应用支持力度](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-overview.md)为准。

- **多模态开发套件**（`multimodal-dialog`）：  
  ✅ WebRTC / WebSocket 支持，❌ AOQ 不支持  

- **实时语音识别**（Fun-ASR 系列）、**实时语音合成**（CosyVoice 系列）、**实时语音对话**（`qwen-audio-3.0-realtime-plus` 等）：  
  ✅ 仅 WebSocket 支持，❌ AOQ 与 WebRTC 均不支持  

所有模型的最新名称、上下文长度、定价及快照版本，请务必通过 [阿里云百炼控制台](https://bailian.console.aliyun.com/cn-beijing#/home) 查阅；并发限流策略详见 [限流](https://help.aliyun.com/zh/model-studio/rate-limit)。

## 关键参数

### 鉴权参数
- **`Authorization: Bearer <API_KEY>`**：所有协议建连阶段必需，通过 HTTP Header 传递。  
  - API Key 必须在服务端安全管理，**严禁硬编码于客户端**（参见 [Token鉴权](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-quick-start-guide/realtime-token-authentication.md)）。  
  - AOQ 协议采用服务端代理鉴权：AppServer 使用 API Key 向网关申请 `aoqTokenForClient`，客户端仅携带该临时 [Token](../concepts/token.md) 连接，避免密钥暴露。

### 协议标识参数
- **`x-dashscope-rtc-transport: moq`**：AOQ 协议专用请求头，用于显式声明使用 AOQ（QUIC）传输。  
- **`Content-Type: application/sdp`**：WebRTC SDP 交换必需，区别于 AOQ/WebSocket 的 `application/json`。  
- **`clientIp`**（选填）：AOQ 建连请求体中指定客户端真实公网 IP，用于 Relay 接入点智能调度；不填则默认使用 AppServer 请求 IP。

### 会话配置参数（`session.update`）
- **`modalities`**：指定输出模态，如 `["text"]` 或 `["text","audio"]`；当前不支持视频输出。  
- **`voice`**：TTS 音色标识（如 `"Ethan"`），仅当 `modalities` 包含 `"audio"` 时生效。  
- **`input_audio_format` / `output_audio_format`**：固定为 `"pcm"`，采样率分别为 16kHz（输入）和 24kHz（输出）。  
- **`turn_detection`**：语音活动检测（VAD）配置，推荐 `qwen3.5-omni-realtime` 系列模型使用 `semantic_vad` 类型（参见 [接入模型与应用](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-quick-start-guide/realtime-connect-model.md)）。

## 使用方式

### 协议选型与接入路径
| 协议 | 适用场景 | SDK/依赖 | 关键步骤 |
|------|----------|-----------|-----------|
| **AOQ** | 移动端原生 App（Android/iOS/HarmonyOS），要求极致弱网对抗与低延迟 | [AOQ SDK](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-quick-start-guide/realtime-sdk-download.md) + Opus 插件 | 1. AppServer 调用 allocate 接口获取 `aoqTokenForClient`<br>2. 客户端调用 `connect()` 并传入凭证<br>3. **必须等待 `session.updated` 后再调用 `enableSendMediaStream()`**（参见 [媒体流发送管理](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-function/aoq-media-stream-control.md)） |
| **WebRTC** | 浏览器端或已有 WebRTC 基础设施的场景，需原生音视频支持 | 浏览器原生 API 或标准 WebRTC 库 | 1. 客户端生成 Offer SDP<br>2. POST 到 `/api/v1/webrtc/realtime?model=xxx` 并携带 `Authorization`<br>3. 解析服务端返回的 Answer SDP 并建立连接<br>⚠️ 功能目前白名单开放，需联系商务获取 Endpoint（参见 [Token鉴权](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-quick-start-guide/realtime-token-authentication.md)） |
| **WebSocket** | 服务端集成、原型验证、轻量级文本/语音交互 | DashScope SDK 或通用 WebSocket 客户端 | 1. 直接 WebSocket 握手，Header 携带 `Authorization`<br>2. 发送 `session.update` 初始化会话<br>3. 通过 `input_audio_buffer.append` 等事件推送数据（AOQ/WebRTC 无需此步） |

### 核心 SDK 控制逻辑（AOQ）
- **连接状态管理**：遵循明确的状态机（`Connecting` → `Connected` → `Failed` → `Disconnected`），`onConnectionStatusChange` 回调通知状态变更（参见 [连接状态管理](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-function/aoq-connection-management.md)）。  
- **媒体流控制**：`enableSendMediaStream(.audio, false)` 在 `connect()` 前禁用发送，收到 `session.updated` 后设为 `true`，否则服务端可能拒绝数据（参见 [媒体流发送管理](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-function/aoq-media-stream-control.md)）。  
- **自定义音视频**：支持外部采集/播放（`isExternal=true`），通过 `pushAudioExternalStreamData()` 或 `pushExternalVideoCapturedFrame()` 注入 PCM/视频帧，适用于 TTS 输出、文件混音、AI 生成画面等场景（参见 [自定义音频采集](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-function/aoq-custom-audio-capture.md) 和 [自定义视频输入](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-function/aoq-custom-video-input.md)）。

## 限制和注意事项

- **协议能力边界**：  
  - AOQ 与 WebRTC 内置回声消除（AEC）和降噪，WebSocket **无内置 AEC/降噪**，需客户端自行处理（参见 [Realtime API 概述](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-overview.md)）。  
  - WebSocket 不支持视频流传输，仅支持文本、音频（PCM）、图像（Base64）；AOQ/WebRTC 支持音视频混合传输。  

- **SDK 使用约束**：  
  - AOQ SDK 的 `enableSendMediaStream()` 必须在 `createEngine()` 之后调用，且默认行为是 `connect()` 成功后立即发送媒体流——若模型要求 `session.updated` 后才接收数据，**必须显式禁用再启用**（参见 [媒体流发送管理](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-function/aoq-media-stream-control.md)）。  
  - 外部音频流推送时，错误码 `110`（缓冲区满）需主动重试（Sleep 30ms 后重推），不可丢弃数据（参见 [自定义音频采集](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-function/aoq-custom-audio-capture.md)）。  

- **安全与合规**：  
  - API Key 为高危凭证，必须通过环境变量或后端下发，禁止出现在客户端代码、配置文件或 Git 历史中（参见 [Token鉴权](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-quick-start-guide/realtime-token-authentication.md)）。  
  - 自定义音频播放时，`onPlaybackAudioFrame` 回调中的 `frame.dataPtr` 仅在回调内有效，异步使用需深拷贝（参见 [自定义音频播放](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-function/aoq-custom-audio-playback.md)）。

## 来源文档

- [Realtime API 概述](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-overview.md)
- [SDK下载](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-quick-start-guide/realtime-sdk-download.md)
- [Token鉴权](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-quick-start-guide/realtime-token-authentication.md)
- [接入模型与应用](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-quick-start-guide/realtime-connect-model.md)
- [AOQ SDK简介](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-desc.md)
- [连接状态管理](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-function/aoq-connection-management.md)
- [媒体流发送管理](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-function/aoq-media-stream-control.md)
- [音频常用功能介绍](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-function/aoq-audio-features.md)
- [自定义音频播放](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-function/aoq-custom-audio-playback.md)
- [自定义音频采集](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-function/aoq-custom-audio-capture.md)
- [视频常用功能介绍](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-function/aoq-video-features.md)
- [自定义视频输入](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-function/aoq-custom-video-input.md)



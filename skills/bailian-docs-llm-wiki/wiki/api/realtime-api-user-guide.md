# realtime api user guide

Realtime API 是百炼平台面向实时多模态交互场景提供的低延迟、高可靠通信能力，支持 AOQ、WebRTC 和 WebSocket 三种传输协议，适配不同终端、网络环境与业务需求。开发者可根据场景特性（如弱网对抗、浏览器兼容性、接入成本）选择协议，并通过统一的模型/应用接口调用 AI 能力。所有协议均基于 Token 鉴权，连接建立后通过结构化事件（如 `session.update`、`input_audio_buffer.append`）驱动交互流程。

## 支持的模型/功能

Realtime API 当前支持以下核心模型与应用类型，各协议支持情况需严格对照 [Realtime API 概述](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-overview.md) 中的兼容性表格：

- **实时全模态模型**：`qwen3.5-omni-plus-realtime`、`qwen3.5-omni-flash-realtime`、`qwen3.5-livetranslate-flash-realtime` —— 全协议支持（AOQ/WebRTC/WebSocket）。
- **实时语音识别（ASR）**：`Qwen-Audio-3.0-ASR-Flash-Streaming`、`Fun-ASR-Realtime` 系列 —— **仅 AOQ 和 WebSocket 支持**，WebRTC 明确不支持（见 [Realtime API 概述](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-overview.md)）。
- **实时语音合成（TTS）**：`CosyVoice` 系列 —— **仅 AOQ 和 WebSocket 支持**，WebRTC 不支持。
- **实时语音对话模型**：`qwen-audio-3.0-realtime-plus`、`qwen-audio-3.0-realtime-flash` —— 全协议支持。
- **多模态开发套件**：`multimodal-dialog` —— 全协议支持。

> **注意**：文档 5 中 WebRTC 接入示例代码存在截断（末尾为 `audioSender?.replaceTrack(audioTrack); videoSender?.replaceT`），且未提供完整 `sendUpdate` 实现；实际开发请以 [接入模型与应用](../../raw/model-api-reference/realtime-api-user-guide/realtime-connect-model.md) 官方完整版为准，避免因代码不完整导致连接失败。

## 关键参数

### 协议选择与建连参数
- `x-dashscope-rtc-transport`：HTTP Header 中指定协议，`moq` 表示 AOQ，`webrtc` 表示 WebRTC（WebSocket 无需此头）。
- `clientIp`（AOQ 专用）：选填，用于 Relay 接入点优化，建议由 AppServer 获取客户端真实公网 IP 后传入。
- `model`：URL Query 参数，必须指定支持的模型名，如 `?model=qwen3.5-omni-plus-realtime`。

### 会话配置（`session.update` 事件）
- `modalities`：输出模态数组，支持 `["text"]` 或 `["text","audio"]`，决定是否返回音频流。
- `voice`：TTS 音色标识符（如 `"Ethan"`），仅当 `modalities` 包含 `"audio"` 时生效。
- `input_audio_format` / `output_audio_format`：当前**仅支持 `"pcm"`**，采样率分别为 16kHz（输入）和 24kHz（输出）。
- `turn_detection`：语音活动检测（VAD）配置，推荐 `type: "semantic_vad"`（语义级 VAD），`silence_duration_ms` 建议设为 `800`。

### SDK 配置参数（AOQ）
- `publishTracks` / `subscribeTracks`：声明需发布/订阅的媒体轨道（`.audio`, `.video`, `.data`），必须在 `connect()` 前设置。
- `enableSendMediaStream(trackType, enable)`：精确控制媒体流发送时机，**必须在收到 `session.updated` 后调用 `enable: true`**（见 [媒体流发送管理](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-function/aoq-media-stream-control.md)）。

## 使用方式

### 协议接入路径
- **AOQ**：适用于移动端原生应用（Android/iOS/HarmonyOS）。需下载 [AOQ SDK](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-quick-start-guide/realtime-sdk-download.md)，通过 AppServer 代理鉴权获取 `aoqTokenForClient` 后调用 `engine.connect(config)`。媒体流需显式控制启停。
- **WebRTC**：适用于浏览器端或已有 WebRTC 基础设施的场景。无专用 SDK，直接使用浏览器原生 API 或第三方 WebRTC 库。需通过 SDP 交换完成建连，**当前为白名单开放**，Endpoint 需联系商务获取（见 [Token鉴权](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-quick-start-guide/realtime-token-authentication.md)）。
- **WebSocket**：适用于服务端集成或快速原型验证。可直接使用 DashScope SDK，接入门槛最低，但弱网对抗能力弱，且不内置回声消除/降噪（需客户端自行处理）。

### 标准交互流程（AOQ 示例）
1. AppServer 调用百炼 Allocate 接口，携带 `Authorization: Bearer <API_KEY>` 获取 `aoqTokenForClient`、`sid`、`relayEndpoints` 等凭证。
2. 客户端创建 `AoqClientEngine`，设置 `onConnectionStatusChange` 回调。
3. 调用 `connect(config)` 前，先执行 `enableSendMediaStream(.audio, false)` 暂停发送。
4. 连接成功（`status == .connected`）后，发送 `session.update` 事件。
5. 收到服务端 `session.updated` 事件后，调用 `enableSendMediaStream(.audio, true)` 开启媒体流。
6. 音频/视频数据通过已注册的轨道自动传输，无需手动发送缓冲区事件。

## 限制和注意事项

- **API Key 安全**：API Key **严禁硬编码于客户端**或提交至代码仓库。AOQ 协议强制要求服务端代理鉴权，客户端仅使用临时 `aoqTokenForClient`；WebRTC/WebSocket 若由客户端直连，必须通过后端服务下发 Token（见 [Token鉴权](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-quick-start-guide/realtime-token-authentication.md)）。
- **媒体流控制**：AOQ 下，**未收到 `session.updated` 前发送媒体流将被服务端拒绝**。务必遵循“先禁用、后开启”模式（见 [媒体流发送管理](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-function/aoq-media-stream-control.md)）。
- **Opus 编解码依赖**：AOQ SDK 使用独立 Opus 插件，Android/iOS/HarmonyOS 均需额外下载并集成 `libPluginOpus`（见 [SDK下载](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-quick-start-guide/realtime-sdk-download.md)）。
- **自定义采集/播放**：外部音频流（`addAudioExternalStream`）和自定义视频输入（`pushExternalVideoCapturedFrame`）需在 `onConnectionStatusChange(.connected)` 后初始化，推送数据前须确保 `streamId`/`trackType` 有效，且需主动处理缓冲区满（错误码 110）等异常（见 [自定义音频采集](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-function/aoq-custom-audio-capture.md) 和 [自定义视频输入](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-function/aoq-custom-video-input.md)）。
- **并发与限流**：具体并发数、QPS 限制及计费规则，请查阅官方 [限流文档](https://help.aliyun.com/zh/model-studio/rate-limit)，不在本指南范围内。

## 来源文档

- [Realtime API 概述](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-overview.md)
- [AOQ SDK简介](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-desc.md)
- [SDK下载](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-quick-start-guide/realtime-sdk-download.md)
- [Token鉴权](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-quick-start-guide/realtime-token-authentication.md)
- [接入模型与应用](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-quick-start-guide/realtime-connect-model.md)
- [连接状态管理](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-function/aoq-connection-management.md)
- [媒体流发送管理](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-function/aoq-media-stream-control.md)
- [音频常用功能介绍](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-function/aoq-audio-features.md)
- [自定义音频播放](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-function/aoq-custom-audio-playback.md)
- [视频常用功能介绍](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-function/aoq-video-features.md)
- [自定义音频采集](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-function/aoq-custom-audio-capture.md)
- [自定义视频输入](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-function/aoq-custom-video-input.md)



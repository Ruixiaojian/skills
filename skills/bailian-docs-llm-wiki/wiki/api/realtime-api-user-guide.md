# realtime api user guide

Realtime API 是一套面向低延迟、抗弱网、多模态实时交互场景的协议化接入方案，支持 WebSocket、WebRTC 和 AOQ（AI over QUIC）三种传输协议，开发者可根据终端类型、网络环境和业务需求灵活选型。本文档系统梳理其模型支持、核心参数、接入方式及关键限制，为开发者提供可直接落地的实践指南。

## 支持的模型/功能

Realtime API 支持三类核心能力：**实时全模态对话**（如 `qwen3.5-omni-plus-realtime`）、**多模态开发套件**（`multimodal-dialog`）以及**基础语音能力**（ASR/TTS/对话）。不同协议对模型的支持存在明确差异：

- **AOQ 与 WebRTC** 均完整支持 `qwen3.5-omni-plus-realtime`、`qwen3.5-omni-flash-realtime` 及 `qwen3.5-livetranslate-flash-realtime` 等实时全模态模型；  
- **WebSocket** 是唯一支持 `Fun-ASR`、`CosyVoice` 和 `qwen-audio-3.0-realtime-plus` 等纯语音模型的协议；  
- **多模态开发套件 `multimodal-dialog`** 仅支持 WebRTC 和 WebSocket，**不支持 AOQ** —— 这一限制在 [Realtime API简介](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-overview.md) 中有明确说明，但需注意文档 6 中“通过WebRTC使用多模态交互套件”的示例未提及此限制，实际接入时应以概述文档为准。  
> **注意**：文档 1 明确指出 AOQ 不支持 `multimodal-dialog`，而文档 6 的标题与正文均未强调该限制，易引发误用。开发者务必以 [Realtime API简介](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-overview.md) 的表格为准。

## 关键参数

所有协议均依赖统一的身份认证机制，但建连流程中的关键参数各不相同：

- **通用鉴权**：必须通过 `Authorization: Bearer <API_KEY>` HTTP Header 完成，API Key 需在百炼控制台创建并严格保密，**禁止硬编码于客户端**（参见 [Token鉴权](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-quick-start-guide/realtime-token-authentication.md)）。  
- **AOQ 特有参数**：服务端调用网关时需携带 `x-dashscope-rtc-transport: moq` 头，并传入 `clientIp`（选填）用于优化 Relay 接入点；客户端连接时需使用网关返回的 `aoqTokenForClient`、`sid`、`clientRelayCertFingerprint` 及 `clientRelayEndpoints`（参见 [Token鉴权](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-quick-start-guide/realtime-token-authentication.md)）。  
- **WebSocket/WebRTC 共同参数**：模型名称通过 URL Query 参数 `?model=<model_name>` 指定，如 `qwen3.5-omni-plus-realtime`；SDP 交换或握手请求中需设置 `Content-Type`（WebRTC 为 `application/sdp`，WebSocket 为 `application/json`）。  
- **会话配置参数**：连接成功后，客户端需发送 `session.update` 事件，其中 `modalities`（输出模态）、`voice`（音色）、`input_audio_format`（输入格式，仅 PCM）、`output_audio_format`（输出格式，仅 PCM）及 `turn_detection`（VAD 类型与阈值）均为必需字段，详见 [实现接通模型/应用](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-quick-start-guide/realtime-connect-model.md)。

## 使用方式

接入流程遵循“鉴权 → 建连 → 配置 → 通信”四步范式，协议差异主要体现在前两步：

- **AOQ**：需业务 AppServer 代理调用百炼网关获取临时 [Token](../concepts/token.md)（`aoqTokenForClient`），客户端 SDK 使用该 [Token](../concepts/token.md) 连接；SDK 提供跨平台封装（Android/iOS/HarmonyOS），需集成 `AoqClientSdk` 及 Opus 插件（参见 [SDK下载](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-quick-start-guide/realtime-sdk-download.md)）。建连后必须等待 `session.updated` 事件再启用媒体流（`enableSendMediaStream`），否则模型可能未就绪（参见 [媒体流发送管理](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-function/aoq-media-stream-control.md)）。  
- **WebRTC**：无官方 SDK，Web 端直接使用浏览器原生 `RTCPeerConnection`，需由业务 AppServer 代理完成 SDP 交换（避免前端暴露 API Key）；关键操作包括：创建连接、添加音频/视频轨道、创建 `oai-events` DataChannel、生成 Offer、发送 Offer 获取 Answer、设置远端描述。媒体轨道需在收到 `session.created` 后手动启用（等效于 AOQ 的 `enableSendMediaStream(true)`）。  
- **WebSocket**：适用于服务端集成或快速验证，通过 DashScope SDK 或标准 WebSocket 客户端连接，消息体为 JSON 格式，需自行处理音频编解码与 VAD。  

## 限制和注意事项

- **协议兼容性**：AOQ 仅支持 Android/iOS/HarmonyOS 原生应用，**不支持浏览器**；WebRTC 和 WebSocket 均支持浏览器，但 WebRTC 在浏览器中受 CORS 限制，必须由后端代理 SDP 交换（参见 [通过WebRTC使用qwen3.5-omni-plus-realtime实现实时通话](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-best-practices/best-practice-webrtc-omni-realtime.md)）。  
- **媒体流控制**：AOQ SDK 默认建连后即发送媒体流，**必须显式调用 `enableSendMediaStream(false)` 禁用，待 `session.updated` 后再启用**，否则会导致数据丢失或连接异常（参见 [媒体流发送管理](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-function/aoq-media-stream-control.md)）。  
- **自定义采集/播放**：AOQ 支持外部音频/视频流注入（如 TTS 输出、屏幕录制），但需严格遵循生命周期——必须在 `onConnectionStatusChange(Connected)` 后添加流，并在销毁前移除；推送 PCM 数据时需处理缓冲区满错误（错误码 110）（参见 [自定义音频采集](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-function/aoq-custom-audio-capture.md)）。  
- **安全红线**：API Key 绝不可出现在客户端代码或公开仓库中；AOQ 的 `aoqTokenForClient` 为短期有效凭证，客户端无需且不应解析其内容。

## 来源文档

- [Realtime API简介](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-overview.md)
- [SDK下载](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-quick-start-guide/realtime-sdk-download.md)
- [Token鉴权](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-quick-start-guide/realtime-token-authentication.md)
- [实现接通模型/应用](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-quick-start-guide/realtime-connect-model.md)
- [通过WebRTC使用qwen3.5-omni-plus-realtime实现实时通话](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-best-practices/best-practice-webrtc-omni-realtime.md)
- [通过WebRTC使用多模态交互套件实现实时通话](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-best-practices/best-practice-webrtc-multimodal-dialog.md)
- [通过AOQ使用qwen3.5-omni-plus-realtime实现实时通话](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-best-practices/best-practice-aoq-omni-realtime.md)
- [AOQ SDK简介](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-desc.md)
- [连接状态管理](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-function/aoq-connection-management.md)
- [媒体流发送管理](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-function/aoq-media-stream-control.md)
- [音频常用功能介绍](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-function/aoq-audio-features.md)
- [自定义音频采集](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-function/aoq-custom-audio-capture.md)
- [自定义音频播放](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-function/aoq-custom-audio-playback.md)
- [自定义视频输入](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-function/aoq-custom-video-input.md)
- [视频常用功能介绍](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-function/aoq-video-features.md)



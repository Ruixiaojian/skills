# realtime api user guide

Realtime API 是百炼平台提供的低延迟、高可靠实时[多模态](../concepts/multi-modal.md)交互能力，支持 WebSocket、WebRTC 和 AOQ 三种传输协议，面向服务端集成、浏览器互动和移动端原生应用等不同场景。开发者可根据业务对延迟、弱网对抗、平台兼容性及接入复杂度的要求，选择最适配的协议方案。所有协议均通过统一的模型/应用接口提供服务，但底层实现与能力边界存在显著差异。

## 支持的模型/功能

Realtime API 当前支持以下核心模型与应用类型，不同协议的支持情况需严格对照：

- **实时全模态模型**：`qwen3.5-omni-plus-realtime`、`qwen3.5-omni-flash-realtime`、`qwen3.5-livetranslate-flash-realtime` —— 全协议（AOQ/WebRTC/WebSocket）均支持 [Realtime API简介](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-overview.md)。
- **[多模态](../concepts/multi-modal.md)开发套件**：`multimodal-dialog` —— 仅 WebRTC 和 WebSocket 支持，**AOQ 不支持** [Realtime API简介](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-overview.md)。
- **实时语音识别**：`Fun-ASR系列模型` —— 仅 WebSocket 支持。
- **实时语音合成**：`CosyVoice系列模型` —— 仅 WebSocket 支持。
- **实时语音对话**：`qwen-audio-3.0-realtime-plus`、`qwen-audio-3.0-realtime-flash` —— 仅 WebSocket 支持。

> **注意**：文档 3 中称 `multimodal-dialog` 在 WebRTC 下可用，而文档 1 明确列出其 AOQ 支持为“不支持”，二者一致；但文档 3 的示例代码中使用了 `model=multimodal-dialog` 的 WebRTC 端点，与文档 1 的表格完全吻合，无矛盾。需注意 `multimodal-dialog` 本质是应用而非基础模型，其 WebRTC 接入方式已在 [通过WebRTC使用多模态交互套件实现实时通话](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-best-practices/best-practice-webrtc-multimodal-dialog.md) 中详细说明。

## 关键参数

### 协议通用参数
- `Authorization`: Bearer `<API_KEY>`，建连阶段必须携带，**严禁硬编码于客户端** [Token鉴权](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-quick-start-guide/realtime-token-authentication.md)。
- `model`: 指定目标模型或应用名称（如 `qwen3.5-omni-plus-realtime`），必需。

### 协议特有参数
- **WebSocket**: 无额外 HTTP 头，直接在 WebSocket 握手请求头中传递 `Authorization`。
- **WebRTC**: SDP 交换请求需设置 `Content-Type: application/sdp`；生产环境必须由 AppServer 代理，避免前端暴露 API Key。
- **AOQ**: 
  - 建连请求需包含 `x-dashscope-rtc-transport: moq` 头 [Token鉴权](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-quick-start-guide/realtime-token-authentication.md)；
  - 客户端连接时使用 `aoqTokenForClient`（非 API Key），该 [Token](../concepts/token.md) 由 AppServer 向百炼网关申请后下发；
  - 必须传入 `sid`、`certFingerprint`、`relayEndpoints` 及 `workspaceIdHash` 等凭证字段。

### 会话配置参数（`session.update` 事件）
- `modalities`: 输出模态数组，如 `["text", "audio"]`；
- `voice`: 输出音色名称（如 `"Ethan"`）；
- `input_audio_format` / `output_audio_format`: 当前仅支持 `"pcm"`；
- `turn_detection`: VAD 配置对象，`type` 可选 `"server_vad"` 或 `"semantic_vad"`（推荐后者），`silence_duration_ms` 控制响应触发静默时长。

## 使用方式

### 协议选择指南
| 场景 | 推荐协议 | 关键依据 |
|------|----------|----------|
| 服务端集成、快速原型验证 | WebSocket | 接入难度极低，SDK 封装完善 |
| 浏览器端音视频互动、已有 WebRTC 基础设施 | WebRTC | 原生浏览器支持，内置回声消除/降噪 |
| 移动端原生应用、弱网/高实时性要求 | AOQ | 极致弱网对抗、建连快、混合数据传输 |

### 各协议典型流程
- **WebSocket**: 通过 DashScope SDK 直接建立连接，发送 `input_audio_buffer.append` 等事件流式输入音频，接收 `response.text.delta` 等事件[流式输出](../concepts/streaming-output.md)。无需 SDP 交换或媒体轨道管理。
- **WebRTC**: 
  1. 创建 `RTCPeerConnection` 并禁用媒体轨道发送（`track.enabled = false`）；
  2. 获取本地媒体流并添加至连接；
  3. 创建 `oai-events` DataChannel；
  4. 生成 Offer SDP 并通过 AppServer 代理 POST 至百炼 WebRTC 端点；
  5. 设置服务端返回的 Answer SDP，连接建立后收到 `session.created` 再启用媒体发送 [通过WebRTC使用qwen3.5-omni-plus-realtime实现实时通话](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-best-practices/best-practice-webrtc-omni-realtime.md)。
- **AOQ**: 
  1. AppServer 向百炼网关申请 `aoqTokenForClient` 等凭证；
  2. 客户端调用 `createEngine` 并设置回调；
  3. 调用 `startAudioCapture`/`startVideoCapture` 启动采集；
  4. 调用 `connect` 传入凭证，**连接前必须调用 `enableSendMediaStream(.audio, false)` 暂停发送**；
  5. 收到 `session.updated` 事件后，再调用 `enableSendMediaStream(.audio, true)` 开启媒体流 [媒体流发送管理](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-function/aoq-media-stream-control.md)。

## 限制和注意事项

- **安全限制**：API Key 绝不可出现在客户端代码或前端请求中。WebSocket 和 WebRTC 的鉴权需通过服务端代理完成；AOQ 必须使用 [Token](../concepts/token.md) 鉴权机制 [Token鉴权](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-quick-start-guide/realtime-token-authentication.md)。
- **媒体流控制**：AOQ 和 WebRTC 均要求在收到 `session.updated`（AOQ）或 `session.created`（WebRTC）事件后才开启媒体发送，否则 AI 侧可能未就绪导致数据丢失 [媒体流发送管理](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-function/aoq-media-stream-control.md)。
- **平台兼容性**：AOQ 仅支持 Android/iOS/HarmonyOS，不支持浏览器；WebRTC 依赖浏览器原生支持；WebSocket 兼容任意支持该协议的环境。
- **自定义采集**：AOQ 提供完整的自定义音频/视频采集能力，但需严格遵循生命周期——必须在 `onConnectionStatusChange(connected)` 后再调用 `addAudioExternalStream` 或 `pushExternalVideoCapturedFrame`，且需自行管理缓冲区满（错误码 110）等异常 [自定义音频采集](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-function/aoq-custom-audio-capture.md)。
- **限流与并发**：具体并发数、QPS 限制请参考[限流文档](https://help.aliyun.com/zh/model-studio/rate-limit)，模型价格与快照版本信息以[百炼控制台](https://bailian.console.aliyun.com/cn-beijing#/home)为准。

## 来源文档

- [Realtime API简介](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-overview.md)
- [通过WebRTC使用qwen3.5-omni-plus-realtime实现实时通话](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-best-practices/best-practice-webrtc-omni-realtime.md)
- [通过WebRTC使用多模态交互套件实现实时通话](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-best-practices/best-practice-webrtc-multimodal-dialog.md)
- [通过AOQ使用qwen3.5-omni-plus-realtime实现实时通话](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-best-practices/best-practice-aoq-omni-realtime.md)
- [AOQ SDK简介](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-desc.md)
- [SDK下载](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-quick-start-guide/realtime-sdk-download.md)
- [Token鉴权](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-quick-start-guide/realtime-token-authentication.md)
- [实现接通模型/应用](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-quick-start-guide/realtime-connect-model.md)
- [连接状态管理](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-function/aoq-connection-management.md)
- [媒体流发送管理](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-function/aoq-media-stream-control.md)
- [自定义音频采集](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-function/aoq-custom-audio-capture.md)
- [音频常用功能介绍](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-function/aoq-audio-features.md)
- [自定义音频播放](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-function/aoq-custom-audio-playback.md)
- [自定义视频输入](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-function/aoq-custom-video-input.md)
- [视频常用功能介绍](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-function/aoq-video-features.md)



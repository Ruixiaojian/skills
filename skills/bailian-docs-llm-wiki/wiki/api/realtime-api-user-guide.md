# realtime api user guide

Realtime API 是一套面向低延迟、多模态、弱网环境优化的实时交互协议栈，提供 WebSocket、WebRTC 和 AOQ（AI over QUIC）三种传输协议，支持语音识别、语音合成、多模态对话等 AI 场景。开发者可根据终端类型、网络条件和业务需求选择最适配的接入方式。

## 支持的模型/功能

Realtime API 当前支持以下核心模型与应用类型，但**协议支持存在显著差异**：

- **全模态实时模型**（如 `qwen3.5-omni-plus-realtime`、`qwen3.5-omni-flash-realtime`、`qwen3.5-livetranslate-flash-realtime`）：  
  - **AOQ** 和 **WebRTC** 均完全支持；  
  - **WebSocket** 也支持，但仅适用于服务端集成或原型验证，不推荐用于浏览器端音视频交互 [Realtime API简介](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-overview.md)。

- **多模态开发套件**（`multimodal-dialog`）：  
  - **WebRTC** 和 **WebSocket** 支持；  
  - **AOQ 不支持**（见文档 1 表格）[Realtime API简介](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-overview.md)。

- **语音识别/合成/对话专用模型**（如 `Fun-ASR` 系列、`CosyVoice` 系列、`qwen-audio-3.0-realtime-plus`）：  
  - **仅 WebSocket 支持**；  
  - WebRTC 与 AOQ 均不支持该类模型 [Realtime API简介](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-overview.md)。

> **注意**：文档 2（WebRTC + multimodal-dialog）与文档 1 明确声明 `multimodal-dialog` 在 WebRTC 下受支持，但文档 8 的“AOQ 接入”章节未提及该应用类型，且文档 1 明确标注 AOQ 对 `multimodal-dialog` 为“不支持”。因此，`multimodal-dialog` **不可通过 AOQ 接入**，此为确定性限制，非过时信息。

## 关键参数

不同协议的关键参数与配置逻辑差异较大，需严格区分：

- **通用鉴权参数**：所有协议均在建连阶段通过 `Authorization: Bearer <API_KEY>` 完成身份认证，但**AOQ 要求服务端代理鉴权**，客户端使用临时 [Token](../concepts/token.md) 连接，避免 API Key 暴露 [Token鉴权](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-quick-start-guide/realtime-token-authentication.md)。

- **会话配置参数**（`session.update` 事件）：  
  - `modalities`: 指定输出模态，如 `["text", "audio"]`；  
  - `voice`: 输出音色名称（如 `"Ethan"`）；  
  - `input_audio_format` / `output_audio_format`: 当前仅支持 `"pcm"`；  
  - `turn_detection`: VAD 配置对象，`type` 可选 `"server_vad"` 或 `"semantic_vad"`（后者推荐用于 `qwen3.5-omni-realtime` 模型），含 `threshold` 和 `silence_duration_ms` [实现接通模型/应用](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-quick-start-guide/realtime-connect-model.md)。

- **AOQ 特有连接参数**：  
  - `aoqTokenForClient`、`sid`、`certFingerprint`、`relayEndpoints`：均由业务 AppServer 向百炼网关请求后返回，客户端 SDK `connect()` 时传入 [Token鉴权](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-quick-start-guide/realtime-token-authentication.md)。

- **WebRTC 特有信令参数**：  
  - SDP 交换 URL 中必须携带 `model` 查询参数（如 `?model=qwen3.5-omni-plus-realtime`）；  
  - 请求头需包含 `Content-Type: application/sdp` [通过WebRTC使用qwen3.5-omni-plus-realtime实现实时通话](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-best-practices/best-practice-webrtc-omni-realtime.md)。

## 使用方式

### 协议选型原则
- **服务端集成 / 快速验证** → WebSocket（SDK 封装完善，接入最快）；  
- **浏览器端音视频交互** → WebRTC（原生支持，内置 AEC/NS）；  
- **移动端原生 App（Android/iOS/HarmonyOS）** → AOQ（极致弱网对抗、建连快、混合数据传输）。

### 典型接入流程
1. **准备凭证**：在百炼控制台创建 API Key，并按协议要求管理（WebSocket/WebRTC 直接使用；AOQ 需 AppServer 代为申请 [Token](../concepts/token.md)）。  
2. **初始化客户端**：  
   - WebSocket：使用 DashScope SDK 初始化；  
   - WebRTC：创建 `RTCPeerConnection`，添加媒体轨道与 `oai-events` DataChannel；  
   - AOQ：调用 `createEngine`，设置 `AoqEngineDelegate` 回调 [AOQ SDK简介](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-desc.md)。  
3. **建立连接**：  
   - WebSocket：直接 `connect()`；  
   - WebRTC：生成 Offer SDP → HTTP POST 至信令端点 → 设置 Answer SDP；  
   - AOQ：AppServer 获取 [Token](../concepts/token.md) 后，调用 `engine.connect(config)` [连接状态管理](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-function/aoq-connection-management.md)。  
4. **控制媒体流**：  
   - **AOQ**：必须在收到 `session.updated` 后，显式调用 `enableSendMediaStream(.audio, true)` 才开启发送，否则模型可能未就绪 [媒体流发送管理](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-function/aoq-media-stream-control.md)；  
   - **WebRTC**：需在 `ontrack` 回调中绑定远端音频流播放，并通过 `gateMedia(false)` 等机制控制本地媒体发送时机 [通过WebRTC使用qwen3.5-omni-plus-realtime实现实时通话](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-best-practices/best-practice-webrtc-omni-realtime.md)。  
5. **断开与销毁**：调用 `disconnect()` 并在必要时 `destroy()` 引擎。

## 限制和注意事项

- **浏览器兼容性**：WebRTC 和 WebSocket 均被现代浏览器原生支持；AOQ **不支持浏览器环境**，仅限 Android/iOS/HarmonyOS 原生应用 [Realtime API简介](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-overview.md)。  
- **CORS 限制**：WebRTC Demo 中浏览器无法直连百炼信令端点（因 CORS），必须由业务后端代理 SDP 交换请求 [通过WebRTC使用多模态交互套件实现实时通话](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-best-practices/best-practice-webrtc-multimodal-dialog.md)。  
- **媒体流控制强制性**：AOQ 协议下，若未在 `session.updated` 后调用 `enableSendMediaStream`，SDK 默认会立即发送媒体流，可能导致模型侧接收异常数据。务必遵循“先禁用、后开启”模式 [媒体流发送管理](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-function/aoq-media-stream-control.md)。  
- **自定义采集/播放**：AOQ 提供完整的外部音频/视频流接口（`addAudioExternalStream`、`pushExternalVideoCapturedFrame` 等），适用于 TTS 推流、文件混音、AI 画面生成等高级场景，详见 [自定义音频采集](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-function/aoq-custom-audio-capture.md) 与 [自定义视频输入](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-function/aoq-custom-video-input.md)。  
- **安全红线**：API Key **严禁硬编码于前端代码或提交至代码仓库**，应通过环境变量或后端服务下发 [Token鉴权](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-quick-start-guide/realtime-token-authentication.md)。

## 来源文档

- [Realtime API简介](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-overview.md)
- [通过WebRTC使用多模态交互套件实现实时通话](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-best-practices/best-practice-webrtc-multimodal-dialog.md)
- [通过WebRTC使用qwen3.5-omni-plus-realtime实现实时通话](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-best-practices/best-practice-webrtc-omni-realtime.md)
- [通过AOQ使用qwen3.5-omni-plus-realtime实现实时通话](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-best-practices/best-practice-aoq-omni-realtime.md)
- [AOQ SDK简介](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-desc.md)
- [SDK下载](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-quick-start-guide/realtime-sdk-download.md)
- [Token鉴权](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-quick-start-guide/realtime-token-authentication.md)
- [实现接通模型/应用](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-quick-start-guide/realtime-connect-model.md)
- [连接状态管理](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-function/aoq-connection-management.md)
- [媒体流发送管理](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-function/aoq-media-stream-control.md)
- [自定义音频播放](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-function/aoq-custom-audio-playback.md)
- [音频常用功能介绍](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-function/aoq-audio-features.md)
- [自定义音频采集](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-function/aoq-custom-audio-capture.md)
- [视频常用功能介绍](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-function/aoq-video-features.md)
- [自定义视频输入](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-function/aoq-custom-video-input.md)



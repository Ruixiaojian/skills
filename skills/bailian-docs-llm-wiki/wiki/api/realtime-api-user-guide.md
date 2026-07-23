# realtime api user guide

Realtime API 是一套面向低延迟、[多模态](../concepts/multi-modal.md) AI 交互场景的实时通信协议栈，支持 WebSocket、WebRTC 和 AOQ（AI over QUIC）三种传输协议，分别适配服务端集成、浏览器端互动和移动端原生应用等不同技术栈与网络环境。开发者需根据目标平台、延迟要求、弱网适应性及数据类型选择合适协议，并配合对应 SDK 或标准 Web API 实现接入。

## 支持的模型/功能

Realtime API 当前支持以下核心模型与应用类型，但协议支持存在明确差异：

- **实时全模态模型**（如 `qwen3.5-omni-plus-realtime`、`qwen3.5-omni-flash-realtime`、`qwen3.5-livetranslate-flash-realtime`）：三协议均支持，是唯一在 WebSocket、WebRTC 和 AOQ 上完全可用的模型类别。
- **[多模态](../concepts/multi-modal.md)开发套件**（`multimodal-dialog`）：仅支持 WebRTC 和 WebSocket，[不支持 AOQ](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-overview.md)。
- **实时语音识别**（Fun-ASR 系列）、**实时语音合成**（CosyVoice 系列）、**实时语音对话**（`qwen-audio-3.0-realtime-plus` 等）：**仅支持 WebSocket 协议**，[WebRTC 和 AOQ 均不支持](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-overview.md)。

> **注意**：文档 4 与文档 5 均以 WebRTC 接入 `multimodal-dialog` 和 `qwen3.5-omni-plus-realtime` 为示例，但文档 1 明确指出 `multimodal-dialog` 不支持 AOQ；而文档 7 的 AOQ 示例仅覆盖 `qwen3.5-omni-plus-realtime`，未提及 `multimodal-dialog`。因此，`multimodal-dialog` 的 AOQ 支持状态以文档 1 的表格为准，属明确不支持项，非过时信息。

## 关键参数

### 鉴权参数
- `Authorization: Bearer <API_KEY>`：所有协议建连阶段必需的 HTTP Header。AOQ 协议中该 Key 仅用于服务端向百炼网关发起 `allocate` 请求，客户端使用返回的 `aoqTokenForClient` 连接，避免密钥暴露 [Token鉴权](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-quick-start-guide/realtime-token-authentication.md)。

### 协议特有参数
- **AOQ**：`x-dashscope-rtc-transport: moq`（必须）、`clientIp`（选填，用于 Relay 节点优化）。
- **WebRTC**：SDP 交换请求中 `Content-Type: application/sdp`，且 `model` 参数需显式指定（如 `?model=qwen3.5-omni-plus-realtime`）。
- **WebSocket**：无特殊 Header，依赖标准 WebSocket 握手，模型通过 URL query 参数或初始消息体指定。

### 会话配置参数（通过 `session.update` 事件发送）
- `modalities`: 指定输出模态，如 `["text", "audio"]`。
- `voice`: 输出音色 ID（如 `"Ethan"`）。
- `input_audio_format` / `output_audio_format`: 当前仅支持 `"pcm"`。
- `turn_detection`: VAD 配置对象，`type` 可选 `"server_vad"` 或 `"semantic_vad"`（推荐后者），含 `threshold` 和 `silence_duration_ms`。

## 使用方式

### 协议选择与接入路径
- **WebSocket**：适用于服务端或快速原型验证，使用 DashScope SDK（参见[安装SDK](https://help.aliyun.com/zh/model-studio/install-sdk)），接入成本最低，但弱网对抗能力差。
- **WebRTC**：适用于浏览器端，需自行管理 `RTCPeerConnection`、媒体流与 DataChannel，内置回声消除与降噪，[通过WebRTC使用多模态交互套件实现实时通话](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-best-practices/best-practice-webrtc-multimodal-dialog.md) 提供完整 JS 示例。
- **AOQ**：适用于 Android/iOS/HarmonyOS 原生应用，需集成 [AOQ SDK](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-quick-start-guide/realtime-sdk-download.md)，具备极致弱网对抗与混合数据传输能力，[通过AOQ使用qwen3.5-omni-plus-realtime实现实时通话](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-best-practices/best-practice-aoq-omni-realtime.md) 包含各平台集成指南。

### 核心流程共性
1. **获取凭证**：WebSocket 直接使用 API Key；WebRTC 通过 SDP 交换携带 Key；AOQ 由 AppServer 调用百炼 `allocate` 接口获取 `sid` 与 `aoqTokenForClient`。
2. **建立连接**：WebSocket 直连；WebRTC 完成 Offer/Answer 协商；AOQ 调用 `engine.connect(config)`。
3. **会话初始化**：连接成功后，发送 `session.update` 事件配置模态、音色、VAD 等。
4. **媒体流控制**：AOQ 必须在收到 `session.updated` 后调用 `enableSendMediaStream(.audio, true)` 开启发送；WebRTC 需在收到 `session.created` 后解除媒体门控；WebSocket 通常由 SDK 自动处理。

### 媒体流高级控制（AOQ 专属）
- **自定义音频采集/播放**：通过 `isExternal=true` 关闭内部设备，使用 `addAudioExternalStream` + `pushAudioExternalStreamData` 或 `setAudioFrameObserver` 实现 TTS 注入或 ASR 处理 [自定义音频采集](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-function/aoq-custom-audio-capture.md)。
- **自定义视频输入**：支持原始帧（I420/NV12/BGRA）或编码帧（JPEG）推送，需先 `startVideoCapture(isExternal=true)` [自定义视频输入](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-function/aoq-custom-video-input.md)。

## 限制和注意事项

- **浏览器兼容性**：WebRTC 原生支持所有现代浏览器；AOQ 不支持浏览器，仅限原生平台；WebSocket 兼容性最广。
- **建连与媒体发送时机**：AOQ 和 WebRTC 均要求严格遵循“先建连 → 收到服务端确认（`session.updated` 或 `session.created`）→ 再开启媒体发送”流程，否则模型可能无法接收数据。此逻辑在 [媒体流发送管理](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-function/aoq-media-stream-control.md) 中有明确强调。
- **CORS 限制**：WebRTC 的 SDP 交换在浏览器端直连百炼服务受 CORS 限制，[文档 4 和 5 均明确指出 Demo 需通过 curl 或业务后端代理完成](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-best-practices/best-practice-webrtc-multimodal-dialog.md)，生产环境必须由 AppServer 代理。
- **Opus 编解码**：AOQ SDK 使用插件化 Opus，下载 SDK 时必须同步获取并集成 `libPluginOpus`（Android/iOS/HarmonyOS 各平台均有对应包）。
- **连接状态管理**：AOQ SDK 提供明确的状态机（Connecting → Connected → Failed → Disconnected），业务需监听 `onConnectionStatusChange` 回调处理状态迁移，`Failed` 为瞬态，SDK 会自动进入 `Disconnected`，无需手动 `disconnect` [连接状态管理](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-function/aoq-connection-management.md)。

## 来源文档

- [Realtime API简介](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-overview.md)
- [SDK下载](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-quick-start-guide/realtime-sdk-download.md)
- [Token鉴权](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-quick-start-guide/realtime-token-authentication.md)
- [通过WebRTC使用多模态交互套件实现实时通话](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-best-practices/best-practice-webrtc-multimodal-dialog.md)
- [通过WebRTC使用qwen3.5-omni-plus-realtime实现实时通话](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-best-practices/best-practice-webrtc-omni-realtime.md)
- [实现接通模型/应用](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-quick-start-guide/realtime-connect-model.md)
- [通过AOQ使用qwen3.5-omni-plus-realtime实现实时通话](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-best-practices/best-practice-aoq-omni-realtime.md)
- [AOQ SDK简介](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-desc.md)
- [连接状态管理](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-function/aoq-connection-management.md)
- [音频常用功能介绍](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-function/aoq-audio-features.md)
- [媒体流发送管理](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-function/aoq-media-stream-control.md)
- [自定义音频播放](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-function/aoq-custom-audio-playback.md)
- [自定义音频采集](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-function/aoq-custom-audio-capture.md)
- [视频常用功能介绍](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-function/aoq-video-features.md)
- [自定义视频输入](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-function/aoq-custom-video-input.md)



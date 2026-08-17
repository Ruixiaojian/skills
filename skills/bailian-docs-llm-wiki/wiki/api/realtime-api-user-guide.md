# realtime api user guide

Realtime API 是面向低延迟、高可靠 AI 实时交互场景的协议级接口，支持 AOQ、WebRTC 和 WebSocket 三种传输协议，覆盖语音识别、语音合成、[多模态](../concepts/multi-modal.md)对话等核心能力。开发者可根据终端类型、网络环境和业务需求选择最适配的协议，并通过统一的鉴权与事件模型快速集成。

## 支持的模型/功能

Realtime API 当前支持以下模型与应用类型，但**协议支持存在差异**：

- **实时全模态**（`qwen3.5-omni-plus-realtime`, `qwen3.5-omni-flash-realtime`）：AOQ、WebRTC、WebSocket 均支持  
- **实时语音翻译**（`qwen3.5-livetranslate-flash-realtime`）：AOQ、WebRTC、WebSocket 均支持  
- **[多模态](../concepts/multi-modal.md)开发套件**（`multimodal-dialog`）：AOQ、WebRTC、WebSocket 均支持  
- **实时语音识别**（`Qwen-Audio-3.0-ASR-Flash-Streaming`, `Fun-ASR-Realtime` 系列）：**仅 AOQ 和 WebSocket 支持**，WebRTC 不支持（见 [Realtime API 概述](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-overview.md)）  
- **实时语音合成**（`CosyVoice` 系列、`qwen-audio-3.0-tts-flash`、`qwen-audio-3.0-tts-plus`）：**仅 AOQ 和 WebSocket 支持**，WebRTC 不支持  
- **实时语音对话**（`qwen-audio-3.0-realtime-plus`, `qwen-audio-3.0-realtime-flash`）：AOQ、WebRTC、WebSocket 均支持  

> **注意**：文档 1 明确指出 WebRTC 不支持 ASR 和 TTS 类模型，但文档 4 的“WebRTC 接入”章节示例中未体现该限制，且未说明替代方案。实际接入时请以文档 1 的协议支持矩阵为准，避免在 WebRTC 中尝试调用不支持的模型。

## 关键参数

| 参数 | 说明 | 示例值 | 来源 |
|------|------|--------|------|
| `model` | 模型标识符，必须与协议支持矩阵匹配 | `qwen3.5-omni-plus-realtime` | [Realtime API 概述](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-overview.md) |
| `x-dashscope-rtc-transport` | 协议标识头，AOQ 必须设为 `moq` | `moq` | [Token鉴权](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-quick-start-guide/realtime-token-authentication.md) |
| `clientIp` | 客户端真实公网 IP（选填），用于 Relay 节点最优调度 | `203.208.60.1` | [Token鉴权](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-quick-start-guide/realtime-token-authentication.md) |
| `session.update` 事件中的 `modalities` | 输出模态控制，决定服务端返回内容类型 | `["text", "audio"]` | [接入模型与应用](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-quick-start-guide/realtime-connect-model.md) |
| `session.update` 事件中的 `turn_detection.type` | VAD 类型，`semantic_vad` 为 `qwen3.5-omni-realtime` 系列推荐值 | `semantic_vad` | [接入模型与应用](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-quick-start-guide/realtime-connect-model.md) |

## 使用方式

### 1. 鉴权与建连
所有协议均使用 `Authorization: Bearer <API_KEY>` 进行建连阶段鉴权：
- **AOQ**：由 AppServer 向百炼网关发起 HTTP POST 请求获取 `aoqTokenForClient` 和 Relay 地址，客户端 SDK 使用该 [Token](../concepts/token.md) 连接（非 API Key 直连）  
- **WebRTC**：客户端或服务端在 SDP 交换请求中携带 API Key  
- **WebSocket**：客户端在 WebSocket 握手请求头中直接携带 API Key  

> **注意**：API Key **严禁硬编码于客户端**，应通过后端服务下发临时凭证（如 AOQ 的 `aoqTokenForClient`）。详见 [Token鉴权](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-quick-start-guide/realtime-token-authentication.md)。

### 2. SDK 集成
- **AOQ**：必须下载对应平台的 [AOQ SDK](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-quick-start-guide/realtime-sdk-download.md)，并加载 Opus 插件；连接流程需严格遵循“先禁用媒体发送 → 收到 `session.updated` → 再开启发送”的时序（见 [媒体流发送管理](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-function/aoq-media-stream-control.md)）  
- **WebRTC**：无专用 SDK，Web 端使用原生 `RTCPeerConnection`，其他端依赖标准 WebRTC 库；需确保 Offer SDP 包含 `m=audio` 且创建名为 `"oai-events"` 的 DataChannel  
- **WebSocket**：可复用通用 WebSocket SDK，参考 DashScope SDK 快速验证  

### 3. 媒体与数据流控制
- **音频采集/播放**：支持内部设备管理与外部流注入（如 TTS 输出、文件混音），外部流需通过 `addAudioExternalStream` 注册后推送 PCM 数据（见 [自定义音频采集](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-function/aoq-custom-audio-capture.md) 和 [自定义音频播放](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-function/aoq-custom-audio-playback.md)）  
- **视频输入**：支持内部摄像头采集与外部帧注入（原始 I420/NV12/BGRA 或已编码 JPEG），外部模式需设置 `isExternal=true` 并调用 `pushExternalVideoCapturedFrame`（见 [自定义视频输入](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-function/aoq-custom-video-input.md)）  

## 限制和注意事项

- **协议兼容性**：WebRTC 不支持 ASR/TTS 模型，若需在浏览器中实现语音识别，必须改用 WebSocket 协议或服务端转译  
- **连接状态管理**：AOQ SDK 状态机为 `Connecting → Connected/Failed → Disconnected`，`Failed` 为瞬态，SDK 自动迁移至 `Disconnected`，业务层无需在 `onConnectionStatusChange(Failed)` 中调用 `disconnect`（见 [连接状态管理](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-function/aoq-connection-management.md)）  
- **媒体流时序**：AOQ 下必须收到服务端 `session.updated` 事件后才调用 `enableSendMediaStream(true)`，否则服务端可能丢弃数据或连接异常  
- **资源释放**：自定义音频/视频流推送需维护 `running` 标记，在引擎销毁或流移除前主动停止推送循环，避免内存访问越界  
- **Opus 插件**：AOQ SDK 依赖独立 Opus 插件包，未加载将导致音频编解码失败（见 [SDK下载](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-quick-start-guide/realtime-sdk-download.md)）

## 来源文档

- [Realtime API 概述](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-overview.md)
- [Token鉴权](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-quick-start-guide/realtime-token-authentication.md)
- [SDK下载](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-quick-start-guide/realtime-sdk-download.md)
- [接入模型与应用](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-quick-start-guide/realtime-connect-model.md)
- [AOQ SDK简介](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-desc.md)
- [连接状态管理](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-function/aoq-connection-management.md)
- [媒体流发送管理](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-function/aoq-media-stream-control.md)
- [自定义音频播放](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-function/aoq-custom-audio-playback.md)
- [自定义音频采集](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-function/aoq-custom-audio-capture.md)
- [视频常用功能介绍](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-function/aoq-video-features.md)
- [自定义视频输入](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-function/aoq-custom-video-input.md)
- [音频常用功能介绍](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-function/aoq-audio-features.md)



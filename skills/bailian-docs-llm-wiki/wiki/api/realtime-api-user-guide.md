# realtime api user guide

Realtime API 是百炼平台面向实时[多模态](../concepts/multi-modal.md)交互场景提供的低延迟、高可靠通信能力，支持 AOQ（AI over QUIC）、WebRTC 和 WebSocket 三种传输协议，适配不同终端、网络环境与业务需求。开发者可根据场景特性（如弱网对抗、浏览器兼容性、接入成本）选择最合适的协议，并通过统一的模型接口调用实时语音识别、合成、翻译、全模态对话等能力。

## 支持的模型/功能

Realtime API 当前支持以下模型与应用类型，但**协议支持存在差异**：

- **实时全模态**：`qwen3.5-omni-plus-realtime`、`qwen3.5-omni-flash-realtime` —— 全协议（AOQ/WebRTC/WebSocket）支持  
- **实时语音翻译**：`qwen3.5-livetranslate-flash-realtime` —— 全协议支持  
- **[多模态](../concepts/multi-modal.md)开发套件**：`multimodal-dialog` —— 全协议支持  
- **实时语音识别（ASR）**：`Qwen-Audio-3.0-ASR-Flash-Streaming`、`Fun-ASR-Realtime` 系列 —— **仅 AOQ 和 WebSocket 支持**，WebRTC 不支持（见 [Realtime API 概述](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-overview.md)）  
- **实时语音合成（TTS）**：`CosyVoice` 系列、`qwen-audio-3.0-tts-flash`、`qwen-audio-3.0-tts-plus` —— **仅 AOQ 和 WebSocket 支持**，WebRTC 不支持（见 [Realtime API 概述](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-overview.md)）  
- **实时语音对话**：`qwen-audio-3.0-realtime-plus`、`qwen-audio-3.0-realtime-flash` —— 全协议支持  

> **注意**：文档 1 明确指出 WebRTC 不支持 ASR/TTS 模型，但文档 5 的“WebRTC 接入”章节未对此限制作任何说明，也未提供替代方案。实际接入时请以文档 1 的模型支持矩阵为准，避免在 WebRTC 场景中误用 ASR/TTS 模型。

## 关键参数

### 协议选择与建连参数
- `x-dashscope-rtc-transport`：HTTP 请求头字段，指定协议。值为 `moq`（AOQ）、`webrtc`（WebRTC）或省略（默认 WebSocket）  
- `clientIp`（AOQ 专用）：客户端真实公网 IP，用于 Relay 节点智能调度；若不传则使用网关请求 IP（见 [Token鉴权](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-quick-start-guide/realtime-token-authentication.md)）  
- `model`：URL 查询参数，必需，指定目标模型名（如 `qwen3.5-omni-plus-realtime`）  

### 会话配置（`session.update`）
- `modalities`：输出模态数组，如 `["text", "audio"]` 或 `["text"]`  
- `voice`：TTS 音色标识符（如 `"Ethan"`）  
- `input_audio_format` / `output_audio_format`：当前仅支持 `"pcm"`  
- `turn_detection`：语音活动检测（VAD）配置，推荐 `semantic_vad` 类型（适用于 `qwen3.5-omni-realtime` 系列），需设置 `threshold` 和 `silence_duration_ms`  

### 媒体控制参数（AOQ SDK）
- `enableSendMediaStream(trackType, enable)`：精确控制音频/视频流发送时机，**必须在收到 `session.updated` 后启用**（见 [媒体流发送管理](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-function/aoq-media-stream-control.md)）  
- `isExternal`（采集/播放配置）：设为 `true` 可禁用 SDK 内部设备管理，启用自定义采集或播放（见 [自定义音频采集](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-function/aoq-custom-audio-capture.md) 和 [自定义音频播放](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-function/aoq-custom-audio-playback.md)）

## 使用方式

### 1. 鉴权与建连
所有协议均通过 `Authorization: Bearer <API_KEY>` 完成**建连阶段**鉴权（非数据传输阶段）。  
- **AOQ**：AppServer 调用百炼网关获取 `aoqTokenForClient`、`sid`、`relayEndpoints` 等凭证，客户端 SDK 使用该凭证连接（见 [Token鉴权](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-quick-start-guide/realtime-token-authentication.md)）  
- **WebRTC**：客户端直接携带 API Key 发起 SDP 交换请求（POST `/api/v1/webrtc/realtime?model=xxx`，`Content-Type: application/sdp`）  
- **WebSocket**：客户端在 WebSocket 握手请求头中携带 API Key  

### 2. AOQ SDK 核心流程（移动端原生）
1. `createEngine` → 设置 `AoqEngineDelegate` 回调  
2. `startAudioCapture` / `startVideoCapture`（可选）→ 启动本地采集  
3. `connect(config)` → 传入网关返回的凭证（`token`, `sid`, `relayEndpoints` 等）  
4. 在 `onConnectionStatusChange(.connected)` 中发送 `session.update`  
5. 在 `onDataMsg` 中监听 `session.updated`，**随后调用 `enableSendMediaStream(.audio, true)`**（见 [媒体流发送管理](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-function/aoq-media-stream-control.md)）  
6. `disconnect()` 主动断开；`destroy()` 销毁引擎  

### 3. 自定义媒体处理（高级场景）
- **自定义音频采集**：设置 `isExternal=true` + `addAudioExternalStream()` + 循环 `pushAudioExternalStreamData()`（见 [自定义音频采集](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-function/aoq-custom-audio-capture.md)）  
- **自定义视频输入**：分原始帧模式（`startVideoCapture(isExternal=true)` + `pushExternalVideoCapturedFrame()`）和编码帧模式（`setVideoEncoderConfig(isExternal=true)` + `pushExternalVideoEncodedFrame()`）（见 [自定义视频输入](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-function/aoq-custom-video-input.md)）  

## 限制和注意事项

- **API Key 安全**：严禁硬编码于客户端。AOQ 协议强制要求服务端代理鉴权，避免密钥暴露；WebSocket/WebRTC 若由客户端直连，必须通过后端服务下发临时 [Token](../concepts/token.md)（见 [Token鉴权](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-quick-start-guide/realtime-token-authentication.md)）  
- **媒体流发送时机**：AOQ 协议下，**必须等待 `session.updated` 事件后再启用媒体发送**，否则服务端可能拒绝接收数据（见 [媒体流发送管理](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-function/aoq-media-stream-control.md)）  
- **SDK 版本与[插件](../concepts/plugin.md)**：AOQ SDK v1.1.0 起支持 Linux 平台及 ASR/TTS 模型，但需额外下载并集成 `libPluginOpus.zip`（见 [SDK下载](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-quick-start-guide/realtime-sdk-download.md)）  
- **状态机行为**：AOQ 连接失败（`Failed`）为瞬态，SDK 会自动迁移至 `Disconnected`，业务层无需在 `onConnectionStatusChange(.failed)` 中调用 `disconnect()`（见 [连接状态管理](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-function/aoq-connection-management.md)）  
- **缓冲区管理**：推送外部音频/视频帧时，若返回错误码 `110`（缓冲区满），需短暂休眠（如 30ms）后重试，**不可丢弃数据**（见 [自定义音频采集](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-function/aoq-custom-audio-capture.md) 和 [自定义视频输入](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-function/aoq-custom-video-input.md)）

## 来源文档

- [Realtime API 概述](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-overview.md)
- [AOQ SDK简介](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-desc.md)
- [Token鉴权](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-quick-start-guide/realtime-token-authentication.md)
- [SDK下载](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-quick-start-guide/realtime-sdk-download.md)
- [接入模型与应用](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-quick-start-guide/realtime-connect-model.md)
- [连接状态管理](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-function/aoq-connection-management.md)
- [媒体流发送管理](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-function/aoq-media-stream-control.md)
- [音频常用功能介绍](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-function/aoq-audio-features.md)
- [自定义音频播放](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-function/aoq-custom-audio-playback.md)
- [自定义音频采集](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-function/aoq-custom-audio-capture.md)
- [自定义视频输入](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-function/aoq-custom-video-input.md)
- [视频常用功能介绍](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-function/aoq-video-features.md)



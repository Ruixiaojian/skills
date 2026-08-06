# realtime api user guide

Realtime API 是百炼平台提供的低延迟、高可靠实时交互接口，支持[多模态](../concepts/multimodal.md)（音视频+文本）端到端传输，面向 AI 原生实时场景深度优化。开发者可根据业务需求在 AOQ、WebRTC 和 WebSocket 三种协议间灵活选型，并通过统一的事件驱动模型与服务端交互。所有协议均基于 [Token](../concepts/token.md) 鉴权，建连后数据流无需重复认证。

## 支持的模型/功能

Realtime API 当前支持以下模型与应用类型，各协议兼容性如下表所示（依据 [Realtime API 概述](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-overview.md)）：

| 模型/应用类型 | 模型示例 | AOQ | WebRTC | WebSocket |
|---------------|----------|-----|--------|-----------|
| 实时全模态 | `qwen3.5-omni-plus-realtime` | ✅ | ✅ | ✅ |
| 实时语音翻译 | `qwen3.5-livetranslate-flash-realtime` | ✅ | ✅ | ✅ |
| [多模态](../concepts/multimodal.md)开发套件 | `multimodal-dialog` | ✅ | ✅ | ✅ |
| 实时语音识别 | `Qwen-Audio-3.0-ASR-Flash-Streaming` | ✅ | ❌ | ✅ |
| 实时语音合成 | `CosyVoice` 系列 | ✅ | ❌ | ✅ |
| 实时语音对话 | `qwen-audio-3.0-realtime-plus` | ✅ | ✅ | ✅ |

> **注意**：文档中明确标注 WebRTC **不支持** ASR 和 TTS 类模型（如 `Qwen-Audio-3.0-ASR-Flash-Streaming`、`CosyVoice` 系列），而 AOQ 和 WebSocket 均支持。该限制在 [Realtime API 概述](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-overview.md) 中已统一说明，无矛盾。

协议选型建议：
- **AOQ**：适用于移动端原生应用（Android/iOS/HarmonyOS/Linux），对弱网、低延迟、[多模态](../concepts/multimodal.md)混合传输有极致要求，且需内置回声消除与降噪能力；
- **WebRTC**：适用于浏览器端或已有 WebRTC 基础设施的场景，依赖原生浏览器支持，适合音视频通话类交互；
- **WebSocket**：适用于服务端集成、快速原型验证或轻量级文本/音频场景，接入门槛最低，但弱网对抗能力弱，且无内置音频处理能力。

## 关键参数

### 连接凭证参数（AOQ 专用）
AOQ 协议需通过服务端 `allocate` 接口获取临时连接凭证，客户端 SDK 使用以下字段建连（参见 [Token鉴权](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-quick-start-guide/realtime-token-authentication.md)）：
- `token`：客户端连接令牌（`aoqTokenForClient`），非 API Key；
- `sid`：会话唯一标识；
- `certFingerprint`：Relay TLS 证书指纹（`clientRelayCertFingerprint`）；
- `relayEndpoints`：Relay 接入点数组（含 `endpoint` 和 `port`）；
- `workspaceIdHash`：工作区 ID 哈希（来自 `extraInfo.workspaceIdHash`）；
- `publishTracks` / `subscribeTracks`：必须至少包含 `.audio` 和 `.data` 轨道。

### 会话配置参数（通用）
所有协议均通过 `session.update` 事件配置 AI 会话行为，关键字段包括：
- `modalities`: 指定输出模态，如 `["text", "audio"]` 或 `["text"]`；
- `voice`: 输出音色名称（如 `"Ethan"`）；
- `input_audio_format` / `output_audio_format`: 当前仅支持 `"pcm"`；
- `instructions`: 系统角色提示词；
- `turn_detection`: 语音活动检测配置，推荐 `semantic_vad` 类型（尤其用于 `qwen3.5-omni-realtime` 系列）；
- `silence_duration_ms`: VAD 静音触发阈值（毫秒），默认 `800`。

> **注意**：文档 [接入模型与应用](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-quick-start-guide/realtime-connect-model.md) 中示例代码将 `input_audio_format` 和 `output_audio_format` 明确限定为 `"pcm"`，且注明输入采样率 16 kHz、输出采样率 24 kHz；该约束在其他文档中未被推翻，属强制要求。

## 使用方式

### 协议接入流程
- **AOQ**：  
  1. 下载对应平台 SDK（[SDK下载](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-quick-start-guide/realtime-sdk-download.md)）；  
  2. 业务服务端调用 `allocate` 接口获取凭证；  
  3. 客户端创建引擎 → 设置回调 → 启动采集/播放 → 调用 `connect(config)`；  
  4. **必须**在收到 `session.updated` 后调用 `enableSendMediaStream(.audio, true)` 开启媒体发送（见 [媒体流发送管理](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-function/aoq-media-stream-control.md)）。

- **WebRTC**：  
  1. 使用浏览器原生 `RTCPeerConnection` 或标准 WebRTC 库；  
  2. 创建 Offer 并通过 HTTP POST 发送至 `https://{endpoint}/api/v1/webrtc/realtime?model={model_name}`，携带 `Authorization: Bearer <API_KEY>`；  
  3. 解析 Answer SDP 并 `setRemoteDescription`；  
  4. 监听 DataChannel（名称须为 `"oai-events"`）接收服务端事件。

- **WebSocket**：  
  1. 直接建立 WebSocket 连接，URL 格式为 `wss://{endpoint}/api/v1/ws/realtime?model={model_name}`；  
  2. 握手时通过 `Authorization: Bearer <API_KEY>` 完成鉴权；  
  3. 后续通过 JSON 消息收发 `session.update`、`input_audio_buffer.append` 等事件（详见 DashScope SDK 文档）。

### 音视频控制（AOQ 专用）
- **采集/播放控制**：使用 `startAudioCapture()` / `startAudioPlayer()` 及对应停止/静音 API（见 [音频常用功能介绍](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-function/aoq-audio-features.md)）；  
- **自定义采集/播放**：通过 `isExternal=true` 关闭内部设备，配合 `pushAudioExternalStreamData()` 或 `onPlaybackAudioFrame()` 回调实现（见 [自定义音频采集](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-function/aoq-custom-audio-capture.md) 和 [自定义音频播放](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-function/aoq-custom-audio-playback.md)）；  
- **视频输入**：支持内部采集、外部原始帧（I420/NV12/BGRA 等）或外部编码帧（JPEG）三种模式（见 [视频常用功能介绍](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-function/aoq-video-features.md) 和 [自定义视频输入](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-function/aoq-custom-video-input.md)）。

## 限制和注意事项

- **鉴权安全**：API Key **严禁硬编码于客户端**，AOQ 必须采用服务端代理鉴权模式，客户端仅使用临时 `aoqTokenForClient`（见 [Token鉴权](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-quick-start-guide/realtime-token-authentication.md)）；  
- **媒体流时序**：AOQ 协议下，**必须等待 `session.updated` 事件后再启用媒体发送**，否则服务端可能拒绝接收数据（该规则在 [接入模型与应用](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-quick-start-guide/realtime-connect-model.md) 和 [媒体流发送管理](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-function/aoq-media-stream-control.md) 中均被强调）；  
- **平台兼容性**：AOQ 不支持浏览器环境；WebRTC 在非浏览器端需依赖第三方 WebRTC 实现；WebSocket 兼容性最广，但无内置音频处理能力，客户端需自行实现回声消除、降噪等；  
- **SDK 版本**：AOQ SDK v1.1.0 起新增 Linux 平台支持，并强化 ASR/TTS/多模态套件兼容性（见 [SDK下载](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-quick-start-guide/realtime-sdk-download.md)）；  
- **错误处理**：AOQ SDK 对物理限制（网络中断、设备故障）和外部因素（[Token](../concepts/token.md) 无效）区分处理，前者自动恢复，后者通过 `onConnectionStatusChange(.failed)` 通知（见 [AOQ SDK简介](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-desc.md)）。

## 来源文档

- [Realtime API 概述](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-overview.md)
- [SDK下载](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-quick-start-guide/realtime-sdk-download.md)
- [接入模型与应用](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-quick-start-guide/realtime-connect-model.md)
- [Token鉴权](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-quick-start-guide/realtime-token-authentication.md)
- [AOQ SDK简介](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-desc.md)
- [连接状态管理](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-function/aoq-connection-management.md)
- [媒体流发送管理](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-function/aoq-media-stream-control.md)
- [音频常用功能介绍](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-function/aoq-audio-features.md)
- [自定义音频播放](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-function/aoq-custom-audio-playback.md)
- [自定义音频采集](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-function/aoq-custom-audio-capture.md)
- [视频常用功能介绍](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-function/aoq-video-features.md)
- [自定义视频输入](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-function/aoq-custom-video-input.md)



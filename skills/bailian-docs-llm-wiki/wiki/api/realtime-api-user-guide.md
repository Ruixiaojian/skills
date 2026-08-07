# realtime api user guide

Realtime API 是面向 AI 多模态实时交互场景的低延迟、高鲁棒性通信协议栈，支持 AOQ（AI over QUIC）、WebRTC 和 WebSocket 三种传输协议，覆盖移动端原生应用、浏览器端互动及服务端快速集成等全场景。开发者可根据业务对延迟、弱网对抗、平台兼容性及接入成本的要求，选择最适配的协议方案。

## 支持的模型/功能

Realtime API 支持以下模型与应用类型，但**协议支持存在差异**：

- **实时全模态**（`qwen3.5-omni-plus-realtime`, `qwen3.5-omni-flash-realtime`）：AOQ、WebRTC、WebSocket 均支持  
- **实时语音翻译**（`qwen3.5-livetranslate-flash-realtime`）：AOQ、WebRTC、WebSocket 均支持  
- **多模态开发套件**（`multimodal-dialog`）：AOQ、WebRTC、WebSocket 均支持  
- **实时语音识别**（`Qwen-Audio-3.0-ASR-Flash-Streaming`, `Fun-ASR-Realtime` 系列）：**仅 AOQ 和 WebSocket 支持**，WebRTC 不支持 [原文标题](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-overview.md)  
- **实时语音合成**（`CosyVoice` 系列）：**仅 AOQ 和 WebSocket 支持**，WebRTC 不支持 [原文标题](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-overview.md)  
- **实时语音对话**（`qwen-audio-3.0-realtime-plus`, `qwen-audio-3.0-realtime-flash`）：AOQ、WebRTC、WebSocket 均支持  

> **注意**：文档 1 中明确列出 WebRTC 对 ASR/TTS 模型“不支持”，但文档 4 的 WebRTC 接入示例中未提及此限制，且未说明替代方案。实际接入时请以控制台模型能力矩阵或最新 SDK 文档为准，避免因协议不兼容导致建连失败。

## 关键参数

### 协议选择与建连参数
| 参数 | 说明 | 协议适用性 |
|------|------|------------|
| `x-dashscope-rtc-transport` | HTTP Header，指定协议类型：`moq`（AOQ）、`webrtc`（WebRTC）、`websocket`（WebSocket） | 仅 AOQ 和 WebRTC 需显式设置；WebSocket 使用标准 ws/wss 协议，无需该头 |
| `clientIp` | 客户端真实公网 IP，用于 Relay 接入点智能调度 | **AOQ 专用**，WebSocket/WebRTC 不支持 [原文标题](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-quick-start-guide/realtime-token-authentication.md) |
| `Authorization: Bearer <API_KEY>` | 所有协议均在建连阶段通过此 Header 鉴权 | 全协议通用 |

### 会话配置（`session.update`）
- `modalities`: 输出模态数组，如 `["text", "audio"]`（必填）  
- `voice`: TTS 音色标识（如 `"Ethan"`），仅当 `modalities` 包含 `"audio"` 时生效  
- `input_audio_format` / `output_audio_format`: 当前仅支持 `"pcm"`  
- `turn_detection`: VAD 配置对象，`type` 推荐 `"semantic_vad"`（适用于 `qwen3.5-omni-realtime` 系列）  

## 使用方式

### 协议接入路径
- **AOQ**：需集成 [AOQ SDK](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-quick-start-guide/realtime-sdk-download.md)，适用于 Android/iOS/HarmonyOS/Linux 原生应用。流程为：AppServer 调用 allocate 接口获取 `aoqTokenForClient` → 客户端 SDK 调用 `connect()` → 收到 `session.updated` 后调用 `enableSendMediaStream(.audio, true)` 开启媒体流。  
- **WebRTC**：无专用 SDK，依赖浏览器原生 API 或第三方 WebRTC 库。需通过 SDP 交换建连，鉴权在 POST 请求中完成。**当前为白名单开放**，需联系商务获取 Endpoint [原文标题](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-quick-start-guide/realtime-token-authentication.md)。  
- **WebSocket**：最简接入方式，适合服务端集成或原型验证。可直接使用 DashScope SDK，无需处理音视频编解码细节。

### 媒体流控制（AOQ 必须）
必须遵循“先禁用、后开启”原则：  
1. `connect()` 前调用 `enableSendMediaStream(.audio, false)`  
2. 在 `onDataMsg` 回调中监听 `session.updated` 事件  
3. 收到后调用 `enableSendMediaStream(.audio, true)` [原文标题](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-function/aoq-media-stream-control.md)  

### 自定义音视频输入（高级场景）
- **自定义音频采集**：设置 `isExternal=true` 后，通过 `addAudioExternalStream()` + `pushAudioExternalStreamData()` 推送 PCM 数据（如 TTS 输出）[原文标题](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-function/aoq-custom-audio-capture.md)  
- **自定义视频输入**：支持原始帧（I420/NV12/BGRA）或已编码帧（JPEG）两种模式，需配置 `isExternal=true` 并调用对应 `pushExternalVideo*Frame()` 接口 [原文标题](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-function/aoq-custom-video-input.md)  

## 限制和注意事项

- **API Key 安全**：严禁硬编码于客户端。AOQ 协议强制要求服务端代理鉴权（客户端仅使用临时 `aoqTokenForClient`），而 WebRTC/WebSocket 允许客户端直连，务必通过后端下发 [Token](../concepts/token.md) [原文标题](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-quick-start-guide/realtime-token-authentication.md)  
- **Opus 编解码依赖**：AOQ SDK 需单独下载并加载 Opus 插件（`libPluginOpus.zip` 或 `PluginOpus.framework.zip`），否则 ASR/TTS 功能不可用 [原文标题](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-quick-start-guide/realtime-sdk-download.md)  
- **连接状态管理**：AOQ SDK 状态机为 `Connecting` → `Connected`/`Failed` → `Disconnected`。`Failed` 为瞬态，SDK 自动迁移至 `Disconnected`，业务层无需在 `onConnectionStatusChange(.failed)` 中调用 `disconnect()` [原文标题](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-function/aoq-connection-management.md)  
- **模型就绪时机**：所有媒体流（音频/视频）必须在收到 `session.updated` 后再启用，否则服务端可能丢弃数据或返回错误。此规则对 AOQ 强制，WebSocket/WebRTC 未明确要求但建议统一遵循。  
- **地域与 Endpoint**：接入域名需根据实际地域选择，详见[地域及接入域名](https://help.aliyun.com/zh/model-studio/regions/)，不同模型的 Endpoint 可能不同。

## 来源文档

- [Realtime API 概述](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-overview.md)
- [SDK下载](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-quick-start-guide/realtime-sdk-download.md)
- [Token鉴权](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-quick-start-guide/realtime-token-authentication.md)
- [接入模型与应用](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-quick-start-guide/realtime-connect-model.md)
- [AOQ SDK简介](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-desc.md)
- [媒体流发送管理](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-function/aoq-media-stream-control.md)
- [连接状态管理](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-function/aoq-connection-management.md)
- [音频常用功能介绍](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-function/aoq-audio-features.md)
- [自定义音频播放](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-function/aoq-custom-audio-playback.md)
- [自定义音频采集](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-function/aoq-custom-audio-capture.md)
- [自定义视频输入](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-function/aoq-custom-video-input.md)
- [视频常用功能介绍](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-function/aoq-video-features.md)



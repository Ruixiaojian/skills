# realtime api user guide

Realtime API 是面向 AI 多模态实时交互场景设计的低延迟、高鲁棒性通信协议栈，支持 AOQ（AI over QUIC）、WebRTC 和 WebSocket 三种传输协议，适配不同终端、网络环境与开发复杂度需求。开发者可根据业务对弱网对抗、端侧平台支持、浏览器兼容性及接入成本的要求，选择最合适的协议方案。

## 支持的模型/功能

Realtime API 当前支持以下核心模型与应用类型，各协议的支持情况一致（详见 [Realtime API 概述](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-overview.md)）：

- **实时全模态**：`qwen3.5-omni-plus-realtime`、`qwen3.5-omni-flash-realtime`  
- **实时语音翻译**：`qwen3.5-livetranslate-flash-realtime`  
- **多模态开发套件**：`multimodal-dialog`  
- **实时语音识别（ASR）**：`Qwen-Audio-3.0-ASR-Flash-Streaming`、`Fun-ASR-Realtime` 系列  
- **实时语音合成（TTS）**：`CosyVoice` 系列  
- **实时语音对话**：`qwen-audio-3.0-realtime-plus`、`qwen-audio-3.0-realtime-flash`  

> **注意**：文档 1 明确指出 ASR 和 TTS 模型在 WebRTC 协议下“不支持”，但文档 3 的“模型/应用支持力度”表格中却标注为“支持”。该矛盾以文档 1 的原始说明为准——**WebRTC 协议当前不支持 ASR 和 TTS 模型**，仅 AOQ 和 WebSocket 支持。

所有模型的最新名称、上下文长度、定价及快照版本，请以 [阿里云百炼控制台](https://bailian.console.aliyun.com/cn-beijing#/home) 实时信息为准。

## 关键参数

### 连接凭证参数（AOQ）
由业务 AppServer 调用百炼 Allocate 接口获取，用于 SDK `connect()`：
- `token`：客户端连接令牌（`aoqTokenForClient`），非 API Key  
- `sid`：会话唯一标识  
- `certFingerprint`：Relay TLS 证书指纹（`clientRelayCertFingerprint`）  
- `relayEndpoints`：Relay 接入点数组（含 `endpoint` 和 `port`）  
- `workspaceIdHash`：工作区 ID 哈希（`extraInfo.workspaceIdHash`）  
- `publishTracks` / `subscribeTracks`：需显式声明媒体轨道（如 `.audio`, `.data`）  

### 会话配置参数（`session.update` 事件）
通过 `AoqDataMsg` 发送 JSON，关键字段包括：
- `modalities`: 输出模态列表，如 `["text", "audio"]`  
- `voice`: TTS 音色名（如 `"Ethan"`）  
- `input_audio_format` / `output_audio_format`: 当前仅支持 `"pcm"`  
- `instructions`: 系统角色指令（纯文本）  
- `turn_detection`: VAD 配置对象，推荐 `semantic_vad` 类型（适用于 `qwen3.5-omni-realtime` 系列）

### 媒体流控制参数
- `enableSendMediaStream(trackType, enable)`: 必须在收到 `session.updated` 后调用 `enable: true` 才可发送音视频（见 [媒体流发送管理](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-function/aoq-media-stream-control.md)）  
- `isExternal` 标志：在 `AoqAudioCaptureConfig` / `AoqVideoCaptureConfig` 中设为 `true`，启用自定义采集/播放（见 [自定义音频采集](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-function/aoq-custom-audio-capture.md) 和 [自定义音频播放](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-function/aoq-custom-audio-playback.md)）

## 使用方式

### 协议选型与接入路径
| 协议 | 适用场景 | 客户端要求 | 典型接入方式 |
|--------|-----------|-------------|----------------|
| **AOQ** | 移动端原生 App、极致弱网对抗、多模态混合传输 | Android/iOS/HarmonyOS/Linux SDK | 调用 `AoqClientEngine.createEngine()` → `connect(config)` → 监听 `onConnectionStatusChange` → 收到 `session.updated` 后调用 `enableSendMediaStream()` |
| **WebRTC** | 浏览器端互动、已有 WebRTC 基础设施 | 浏览器原生 API 或 `aiortc` 等库 | 构建 `RTCPeerConnection` → 添加 `AudioStreamTrack` → 创建 Offer → HTTP POST 至 `/api/v1/webrtc/realtime?model=...` 完成 SDP 交换 |
| **WebSocket** | 服务端集成、快速原型验证、低门槛接入 | 任意支持 WebSocket 的环境 | 使用 DashScope SDK 或标准 WebSocket 客户端，握手时携带 `Authorization: Bearer <API_KEY>` |

### AOQ SDK 核心流程（以 iOS 为例）
1. **初始化引擎**：`AoqClientEngine.createEngine(config, delegate: self)`  
2. **启动采集/播放**：`startAudioCapture()` / `startAudioPlayer()`（可设 `isExternal=true`）  
3. **获取并解析 [Token](../concepts/token.md)**：AppServer 请求 Allocate 接口，客户端解析响应（见 [Token鉴权](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-quick-start-guide/realtime-token-authentication.md)）  
4. **建连**：构造 `AoqConnectConfig` 并调用 `engine.connect(config)`  
5. **会话配置**：在 `onConnectionStatusChange(.connected)` 中发送 `session.update`  
6. **开启媒体流**：在 `onDataMsg` 中监听 `session.updated`，随后调用 `enableSendMediaStream(.audio, true)`  
7. **断连销毁**：`engine.disconnect()` → `AoqClientEngine.destroy()`  

### 自定义媒体处理（关键扩展能力）
- **自定义音频采集**：设 `config.isExternal = true` → `addAudioExternalStream()` → 循环 `pushAudioExternalStreamData()`（需处理错误码 `110` 缓冲区满）  
- **自定义音频播放**：设 `config.isExternal = true` → `setAudioFrameObserver()` → `enableAudioFrameObserver()` → 在 `onPlaybackAudioFrame()` 中用 `AudioTrack` 等渲染 PCM  
- **自定义视频输入**：分两种模式：  
  - *原始帧*：`config.isExternal = true` → `pushExternalVideoCapturedFrame()`（支持 I420/NV12/BGRA/CVPixelBuffer）  
  - *编码帧*：`config.isExternal = true` + `codecType = JPEG` → `pushExternalVideoEncodedFrame()`  

## 限制和注意事项

- **协议限制**：WebRTC 当前为白名单开放，需联系商务经理获取 Endpoint；AOQ 不支持浏览器，仅限原生平台（Android/iOS/HarmonyOS/Linux）；WebSocket 不提供内置回声消除/降噪，需客户端自行实现。  
- **建连安全**：API Key **严禁硬编码于客户端**，必须通过服务端代理鉴权（AOQ）或后端下发（WebRTC/WebSocket）。  
- **媒体流时序**：AOQ 下必须严格遵循“先禁用、后开启”原则——`connect()` 前调用 `enableSendMediaStream(false)`，仅在收到 `session.updated` 后才调用 `enableSendMediaStream(true)`，否则服务端可能拒绝接收数据。  
- **SDK 版本兼容性**：AOQ SDK v1.1.0 新增 Linux 平台支持，并明确要求 Opus 编解码器需单独下载 `libPluginOpus` 插件（见 [SDK下载](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-quick-start-guide/realtime-sdk-download.md)）；v1.0.1 不支持 Linux。  
- **状态管理**：`Failed` 是瞬态，SDK 会自动迁移到 `Disconnected`，业务层无需在 `onConnectionStatusChange(.failed)` 中调用 `disconnect()`。  
- **资源释放**：使用自定义采集/播放时，务必在引擎销毁前停止推送循环、移除流、释放 `AudioTrack` 等资源，避免崩溃或内存泄漏。

## 来源文档

- [Realtime API 概述](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-overview.md)
- [SDK下载](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-quick-start-guide/realtime-sdk-download.md)
- [接入模型与应用](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-quick-start-guide/realtime-connect-model.md)
- [AOQ SDK简介](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-desc.md)
- [Token鉴权](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-quick-start-guide/realtime-token-authentication.md)
- [连接状态管理](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-function/aoq-connection-management.md)
- [媒体流发送管理](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-function/aoq-media-stream-control.md)
- [自定义音频播放](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-function/aoq-custom-audio-playback.md)
- [音频常用功能介绍](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-function/aoq-audio-features.md)
- [自定义音频采集](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-function/aoq-custom-audio-capture.md)
- [视频常用功能介绍](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-function/aoq-video-features.md)
- [自定义视频输入](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-function/aoq-custom-video-input.md)



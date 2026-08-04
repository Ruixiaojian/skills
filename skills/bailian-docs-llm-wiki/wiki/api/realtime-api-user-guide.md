# realtime api user guide

Realtime API 是百炼平台提供的低延迟、高可靠实时交互能力接口，支持 AOQ、WebRTC 和 WebSocket 三种传输协议，面向多模态 AI 场景深度优化。开发者可根据终端类型、网络条件、功能需求和接入成本选择最适配的协议方案，并通过统一鉴权与事件模型快速集成语音识别、语音合成、实时对话、多模态交互等能力。

## 支持的模型/功能

Realtime API 当前支持以下模型与应用类型，各协议兼容性如下表所示（依据 [Realtime API 概述](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-overview.md)）：

| 模型/应用类型 | 模型名称 | AOQ | WebRTC | WebSocket |
|---------------|----------|-----|--------|-----------|
| 实时全模态 | `qwen3.5-omni-plus-realtime`, `qwen3.5-omni-flash-realtime` | ✅ | ✅ | ✅ |
| 实时语音翻译 | `qwen3.5-livetranslate-flash-realtime` | ✅ | ✅ | ✅ |
| 多模态开发套件 | `multimodal-dialog` | ✅ | ✅ | ✅ |
| 实时语音识别 | `Qwen-Audio-3.0-ASR-Flash-Streaming`, `Fun-ASR-Realtime` 系列 | ✅ | ❌ | ✅ |
| 实时语音合成 | `CosyVoice` 系列 | ✅ | ❌ | ✅ |
| 实时语音对话 | `qwen-audio-3.0-realtime-plus`, `qwen-audio-3.0-realtime-flash` | ✅ | ✅ | ✅ |

> **注意**：文档中明确标注 WebRTC 不支持 ASR/TTS 类模型，但 [接入模型与应用](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-quick-start-guide/realtime-connect-model.md) 的流程图及代码示例未体现此限制，实际接入时请以 [Realtime API 概述](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-overview.md) 的兼容性表格为准。

## 关键参数

### 鉴权参数
- `Authorization: Bearer <API_KEY>`：所有协议建连阶段必需，通过 HTTP Header 传递。API Key 须在[百炼控制台](https://bailian.console.aliyun.com/cn-beijing#/home)创建并安全保管，**严禁硬编码于客户端**。
- `x-dashscope-rtc-transport: moq`：AOQ 协议专用 Header，标识使用 AOQ（QUIC）传输。

### 连接凭证（AOQ）
服务端调用 allocate 接口后返回 JSON 响应，关键字段包括：
- `aoqTokenForClient`：客户端 SDK 初始化必需的临时连接令牌；
- `sid`：会话唯一标识；
- `clientRelayEndpoints`：Relay 接入点列表（含 `endpoint` 和 `port`）；
- `clientRelayCertFingerprint`：TLS 证书指纹，用于证书校验；
- `extraInfo.workspaceIdHash`：工作区哈希，需传入 SDK 配置。

### 会话配置（`session.update`）
客户端建连成功后需发送 `session.update` 事件，核心字段包括：
- `modalities`: 如 `["text", "audio"]`，指定输出模态；
- `voice`: 音色 ID（如 `"Ethan"`）；
- `input_audio_format` / `output_audio_format`: 当前仅支持 `"pcm"`；
- `turn_detection`: VAD 配置对象，推荐 `type: "semantic_vad"`（适用于 `qwen3.5-omni-realtime` 系列）；
- `instructions`: 系统角色提示词。

详见 [接入模型与应用](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-quick-start-guide/realtime-connect-model.md) 中的完整 JSON 示例。

## 使用方式

### 协议选型与接入路径
- **AOQ**：适用于移动端原生应用（Android/iOS/HarmonyOS/Linux），需集成 [AOQ SDK](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-quick-start-guide/realtime-sdk-download.md)，具备极致弱网对抗与内置 AEC/降噪能力。
- **WebRTC**：适用于浏览器端或已有 WebRTC 基础设施的场景，无需专用 SDK，直接使用原生 `RTCPeerConnection` API；当前为白名单开放，需联系商务获取 Endpoint。
- **WebSocket**：适用于服务端集成或快速原型验证，接入门槛最低，可通过 DashScope SDK 快速启动。

### AOQ 核心流程（以 iOS/Android 为例）
1. **初始化引擎**：调用 `AoqClientEngine.createEngine()`，设置 `AoqEngineDelegate` 回调；
2. **启动采集**：`startAudioCapture()` / `startVideoCapture()`（可选）；
3. **获取凭证**：业务 AppServer 调用 allocate 接口，获取 `aoqTokenForClient` 等参数；
4. **连接建连**：构造 `AoqConnectConfig` 并调用 `engine.connect(config)`；
5. **控制媒体流**：连接成功后默认发送媒体流，**必须等待收到 `session.updated` 事件后再调用 `enableSendMediaStream(.audio, true)` 启用发送**（见 [媒体流发送管理](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-function/aoq-media-stream-control.md)）；
6. **自定义扩展**：支持[自定义音频采集](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-function/aoq-custom-audio-capture.md)、[自定义视频输入](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-function/aoq-custom-video-input.md)、[自定义音频播放](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-function/aoq-custom-audio-playback.md)等高级能力。

### WebRTC 基础流程（Web 端）
1. 创建 `RTCPeerConnection`，添加 `AudioStreamTrack`（必需）及 `DataChannel`（命名需为 `"txt"` 以接收服务端事件）；
2. 生成 Offer SDP，通过 POST 请求至 `https://{endpoint}/api/v1/webrtc/realtime?model={model_name}`，携带 `Authorization` Header；
3. 解析服务端返回的 Answer SDP，调用 `setRemoteDescription()` 完成 ICE 协商；
4. 监听 DataChannel 消息，处理 `session.created` 后发送 `session.update`。

## 限制和注意事项

- **协议限制**：WebRTC 明确不支持 ASR/TTS 类模型（如 `Qwen-Audio-3.0-ASR-Flash-Streaming`），仅 AOQ 和 WebSocket 支持；WebSocket 不支持视频传输。
- **SDK 兼容性**：AOQ SDK v1.1.0 新增 Linux 平台支持，并强化 ASR/TTS/多模态套件能力；v1.0.1 版本已不推荐用于新项目（见 [SDK下载](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-quick-start-guide/realtime-sdk-download.md)）。
- **媒体流控制**：AOQ 协议下，`enableSendMediaStream()` 必须在 `session.updated` 后调用，否则服务端可能丢弃数据；默认行为是连接成功即发送，易导致数据错失。
- **Opus 编解码依赖**：AOQ SDK 使用外部 Opus 插件，集成时需同步下载并加载 `libPluginOpus.zip`（Android/HarmonyOS）或 `PluginOpus.framework.zip`（iOS）。
- **状态管理**：AOQ 连接状态机为 `Connecting → Connected/Failed → Disconnected`，`Failed` 为瞬态，SDK 自动迁移至 `Disconnected`，业务层无需在 `onConnectionStatusChange(Failed)` 中手动调用 `disconnect()`（见 [连接状态管理](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-function/aoq-connection-management.md)）。

## 来源文档

- [Realtime API 概述](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-overview.md)
- [SDK下载](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-quick-start-guide/realtime-sdk-download.md)
- [Token鉴权](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-quick-start-guide/realtime-token-authentication.md)
- [接入模型与应用](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-quick-start-guide/realtime-connect-model.md)
- [AOQ SDK简介](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-desc.md)
- [连接状态管理](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-function/aoq-connection-management.md)
- [媒体流发送管理](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-function/aoq-media-stream-control.md)
- [音频常用功能介绍](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-function/aoq-audio-features.md)
- [自定义音频采集](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-function/aoq-custom-audio-capture.md)
- [视频常用功能介绍](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-function/aoq-video-features.md)
- [自定义视频输入](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-function/aoq-custom-video-input.md)
- [自定义音频播放](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-function/aoq-custom-audio-playback.md)



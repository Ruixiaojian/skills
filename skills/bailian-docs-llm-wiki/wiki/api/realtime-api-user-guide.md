# realtime api user guide

Realtime API 是阿里云百炼平台提供的低延迟、高可靠实时交互能力接口，支持 AOQ（AI over QUIC）、WebRTC 和 WebSocket 三种传输协议，面向多模态 AI 场景深度优化。开发者可根据终端类型、网络环境、功能需求和接入成本灵活选型，快速构建语音对话、实时翻译、全模态交互等应用。

## 支持的模型/功能

Realtime API 当前支持以下核心模型与应用类型，但**不同协议的支持范围存在差异**：

- **实时全模态**：`qwen3.5-omni-plus-realtime`、`qwen3.5-omni-flash-realtime` —— 全协议（AOQ/WebRTC/WebSocket）均支持  
- **实时语音翻译**：`qwen3.5-livetranslate-flash-realtime` —— 全协议均支持  
- **多模态开发套件**：`multimodal-dialog` —— 全协议均支持  
- **实时语音识别（ASR）**：`Qwen-Audio-3.0-ASR-Flash-Streaming`、`Fun-ASR-Realtime` 系列 —— **仅 AOQ 和 WebSocket 支持，WebRTC 不支持**  
- **实时语音合成（TTS）**：`CosyVoice` 系列 —— **仅 AOQ 和 WebSocket 支持，WebRTC 不支持**  
- **实时语音对话**：`qwen-audio-3.0-realtime-plus`、`qwen-audio-3.0-realtime-flash` —— 全协议均支持  

> **注意**：文档 1 中表格明确列出 WebRTC 对 ASR/TTS 模型“不支持”，而部分旧版 SDK 示例或社区文档可能未强调此限制。实际接入时请以 [Realtime API 概述](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-overview.md) 的兼容性矩阵为准。

## 关键参数

### 协议通用参数
- `Authorization: Bearer <API_KEY>`：建连阶段必需的 HTTP Header，用于身份认证；**API Key 必须通过服务端下发，严禁硬编码至客户端**（见 [Token鉴权](../../raw/model-api-reference/realtime-api-user-guide/realtime-token-authentication.md)）。
- `model`：URL 查询参数，指定目标模型（如 `qwen3.5-omni-plus-realtime`），不同模型对应不同接入地址。

### AOQ 协议特有参数（由服务端 allocate 接口返回）
- `aoqTokenForClient`：客户端连接令牌，传入 `AoqConnectConfig.token`
- `sid`：会话唯一标识
- `certFingerprint`：Relay TLS 证书指纹
- `relayEndpoints`：Relay 接入点数组（含 `endpoint` 和 `port`）
- `workspaceIdHash`：工作区 ID 哈希，用于路由

### 会话配置参数（`session.update` 事件体）
- `modalities`: `["text"]` 或 `["text","audio"]`，控制输出模态  
- `voice`: 输出音色（如 `"Ethan"`）  
- `input_audio_format` / `output_audio_format`: 当前仅支持 `"pcm"`  
- `turn_detection`: 语音活动检测配置，推荐 `semantic_vad` 类型（见 [接入模型与应用](../../raw/model-api-reference/realtime-api-user-guide/realtime-connect-model.md)）

## 使用方式

### 协议选型建议
- **移动端原生应用（Android/iOS/HarmonyOS/Linux）**：优先选用 **AOQ**，具备极致弱网对抗、内置回声消除/降噪、低建连延迟及多模态混合传输能力。需集成 [AOQ SDK简介](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-desc.md) 提供的客户端 SDK。  
- **浏览器端应用**：选用 **WebRTC**，利用原生支持，适合已有 WebRTC 基础设施的场景；注意其 ASR/TTS 模型不支持。  
- **服务端集成或快速原型验证**：选用 **WebSocket**，接入门槛最低，通过 DashScope SDK 即可调用。

### AOQ 标准接入流程（关键步骤）
1. **获取凭证**：业务 AppServer 调用百炼 allocate 接口，携带 `Authorization` 头和 `x-dashscope-rtc-transport: moq`，获取 `aoqTokenForClient` 等参数。  
2. **初始化引擎**：调用 `AoqClientEngine.createEngine(config, delegate)`，实现 `AoqEngineDelegate` 监听状态与数据。  
3. **预配置媒体**：调用 `startAudioCapture()`、`startVideoCapture()`（可选）等开启采集，**但默认禁用发送**（见下文）。  
4. **建连与会话协商**：  
   - 调用 `engine.connect(config)` 发起连接；  
   - 在 `onConnectionStatusChange(.connected)` 后发送 `session.update` 事件；  
   - **必须等待收到 `session.updated` 服务端响应后**，再调用 `enableSendMediaStream(.audio, true)` 开启媒体流（见 [媒体流发送管理](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-function/aoq-media-stream-control.md)）。  
5. **断开连接**：调用 `engine.disconnect()`，引擎可复用重连。

### 自定义媒体处理（高级场景）
- **自定义音频采集**：设置 `isExternal=true` 后，通过 `addAudioExternalStream()` 注册流，并循环调用 `pushAudioExternalStreamData()` 推送 PCM 数据（如 TTS 输出、文件音频）。  
- **自定义音频播放**：设置 `isExternal=true` 后，通过 `setAudioFrameObserver()` 和 `enableAudioFrameObserver()` 获取解码后的 PCM 帧，交由应用层渲染（如 AudioTrack、ASR 引擎）。  
- **自定义视频输入**：支持原始帧（I420/NV12/BGRA 等）或已编码帧（JPEG）两种模式，通过 `pushExternalVideoCapturedFrame()` 或 `pushExternalVideoEncodedFrame()` 推送（见 [自定义视频输入](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-function/aoq-custom-video-input.md)）。

## 限制和注意事项

- **建连鉴权仅一次**：[Token](../concepts/token.md) 鉴权发生在建连握手阶段，连接建立后数据传输无需重复认证（见 [Token鉴权](../../raw/model-api-reference/realtime-api-user-guide/realtime-token-authentication.md)）。  
- **AOQ 媒体流发送时机**：若在 `session.updated` 前开启媒体发送，服务端可能因未就绪而丢弃数据或触发异常；务必遵循“先禁用、后开启”流程。  
- **SDK 版本与插件依赖**：AOQ SDK 依赖 Opus 编解码插件（`libPluginOpus`），集成时必须下载并加载对应平台插件（见 [SDK下载](../../raw/model-api-reference/realtime-api-user-guide/realtime-sdk-download.md)）。  
- **WebRTC 白名单限制**：WebRTC 功能当前为白名单开放，需联系商务经理获取 Endpoint，非白名单用户无法使用（见 [Token鉴权](../../raw/model-api-reference/realtime-api-user-guide/realtime-token-authentication.md)）。  
- **状态机行为**：AOQ 连接状态中 `Failed` 为瞬态，SDK 会自动迁移到 `Disconnected`，业务层无需在 `onConnectionStatusChange(.failed)` 中调用 `disconnect()`（见 [连接状态管理](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/aoq-connection-management.md)）。

## 来源文档

- [Realtime API 概述](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-overview.md)
- [AOQ SDK简介](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-desc.md)
- [SDK下载](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-quick-start-guide/realtime-sdk-download.md)
- [接入模型与应用](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-quick-start-guide/realtime-connect-model.md)
- [Token鉴权](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-quick-start-guide/realtime-token-authentication.md)
- [连接状态管理](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-function/aoq-connection-management.md)
- [媒体流发送管理](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-function/aoq-media-stream-control.md)
- [音频常用功能介绍](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-function/aoq-audio-features.md)
- [自定义音频播放](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-function/aoq-custom-audio-playback.md)
- [自定义音频采集](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-function/aoq-custom-audio-capture.md)
- [自定义视频输入](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-function/aoq-custom-video-input.md)
- [视频常用功能介绍](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-function/aoq-video-features.md)



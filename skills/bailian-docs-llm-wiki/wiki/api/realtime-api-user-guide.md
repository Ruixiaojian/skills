# realtime api user guide

Realtime API 是百炼平台提供的低延迟、高可靠实时多模态交互能力，支持 WebSocket、WebRTC 和 AOQ 三种传输协议，面向服务端集成、浏览器互动和移动端原生应用等不同场景。开发者可根据业务对延迟、弱网对抗、平台兼容性及数据类型的需求，选择最适配的协议与模型组合。

## 支持的模型/功能

Realtime API 当前支持以下核心模型与应用类型，协议支持情况如下表所示（依据 [Realtime API简介](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-overview.md)）：

| 模型/应用类型 | AOQ | WebRTC | WebSocket |
|---------------|-----|--------|-----------|
| 实时全模态（`qwen3.5-omni-plus-realtime`, `qwen3.5-omni-flash-realtime`, `qwen3.5-livetranslate-flash-realtime`） | ✅ | ✅ | ✅ |
| 多模态开发套件（`multimodal-dialog`） | ❌ | ✅ | ✅ |
| 实时语音识别（Fun-ASR 系列） | ❌ | ❌ | ✅ |
| 实时语音合成（CosyVoice 系列） | ❌ | ❌ | ✅ |
| 实时语音对话（`qwen-audio-3.0-realtime-plus`, `qwen-audio-3.0-realtime-flash`） | ❌ | ❌ | ✅ |

> **注意**：文档 1 明确指出 `multimodal-dialog` 不支持 AOQ，但文档 6 的标题与正文均未提及该套件在 AOQ 下的可用性，且未提供对应接入示例；而文档 5 明确限定其为 WebRTC 场景。因此，AOQ 协议下不可用于 `multimodal-dialog`，此为权威结论。

所有模型均需通过百炼控制台获取最新名称、上下文长度、价格及快照版本信息，并遵守并发限流策略（参见[限流](https://help.aliyun.com/zh/model-studio/rate-limit)）。

## 关键参数

### 鉴权参数
- **`Authorization: Bearer <API_KEY>`**：所有协议建连阶段必需，通过 HTTP Header 传递。API Key 需在百炼控制台「API Key 管理」中创建并安全保管。
- **AOQ 特有参数**：服务端调用网关时需额外携带 `x-dashscope-rtc-transport: moq` 头以声明 AOQ 协议（见 [Token鉴权](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-quick-start-guide/realtime-token-authentication.md)）。

### 会话配置参数（`session.update`）
- `modalities`: 指定输出模态，如 `["text"]` 或 `["text","audio"]`。
- `voice`: 输出音色标识（如 `"Ethan"`）。
- `input_audio_format` / `output_audio_format`: 当前仅支持 `"pcm"`。
- `instructions`: 系统角色指令。
- `turn_detection`: VAD 配置对象，含 `type`（`server_vad` 或 `semantic_vad`）、`threshold` 和 `silence_duration_ms`。

### AOQ 连接凭证字段（服务端响应）
- `aoqTokenForClient`: 客户端 SDK 初始化所需 token。
- `sid`: 会话唯一标识。
- `clientRelayEndpoints`: Relay 接入点数组（`endpoint` + `port`）。
- `clientRelayCertFingerprint`: TLS 证书指纹。
- `extraInfo.workspaceIdHash`: 工作区 ID 哈希，用于客户端路由。

## 使用方式

### 协议选型与接入路径
- **WebSocket**: 适用于服务端集成或快速原型验证，接入门槛最低，使用 DashScope SDK 即可实现。不支持浏览器原生音视频处理（如回声消除），需客户端自行实现。
- **WebRTC**: 适用于浏览器端低延迟音视频交互，内置回声消除与降噪，需通过 `RTCPeerConnection` 手动管理 SDP 交换与媒体轨道。因 CORS 限制，SDP 交换必须由业务后端代理（见 [通过WebRTC使用多模态交互套件实现实时通话](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-best-practices/best-practice-webrtc-multimodal-dialog.md)）。
- **AOQ**: 适用于移动端原生应用（Android/iOS/HarmonyOS），专为 AI 多模态实时交互优化，具备极致弱网对抗与建连速度，需集成 AOQ Client SDK 并加载 Opus 插件（见 [SDK下载](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-quick-start-guide/realtime-sdk-download.md)）。

### 核心流程（AOQ 示例）
1. **初始化引擎**：调用 `createEngine` 并设置 `AoqEngineDelegate` 回调。
2. **启动采集与播放**：分别调用 `startAudioCapture`、`startAudioPlayer`、`startVideoCapture`（可选）。
3. **获取连接凭证**：业务 AppServer 向百炼网关发起带 `x-dashscope-rtc-transport: moq` 的 POST 请求，获取 `aoqTokenForClient` 等字段。
4. **建立连接**：构造 `AoqConnectConfig`，调用 `connect()`；连接成功后收到 `onConnectionStatusChange(.connected)`。
5. **控制媒体流**：**必须**在收到服务端 `session.updated` 事件后，再调用 `enableSendMediaStream(.audio, true)` 开启发送（见 [媒体流发送管理](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-function/aoq-media-stream-control.md)）。
6. **断开连接**：调用 `disconnect()`。

### 自定义能力（AOQ）
- **自定义音频采集/播放**：通过 `isExternal=true` 关闭内部采集/播放模块，使用 `addAudioExternalStream` + `pushAudioExternalStreamData` 或 `setAudioFrameObserver` + `enableAudioFrameObserver` 实现完全可控的数据流（见 [自定义音频采集](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-function/aoq-custom-audio-capture.md) 与 [自定义音频播放](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-function/aoq-custom-audio-playback.md)）。
- **自定义视频输入**：支持原始帧（I420/NV12/BGRA 等）或已编码帧（JPEG）两种模式，通过 `pushExternalVideoCapturedFrame` 或 `pushExternalVideoEncodedFrame` 推送（见 [自定义视频输入](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-function/aoq-custom-video-input.md)）。

## 限制和注意事项

- **API Key 安全**：严禁硬编码于客户端代码或提交至代码仓库。AOQ 协议强制要求服务端代理鉴权，客户端仅使用临时 `aoqTokenForClient`；WebSocket/WebRTC 客户端若直接使用 API Key，必须通过后端代理请求。
- **媒体流发送时机**：所有协议均要求在收到服务端 `session.created` 或 `session.updated` 事件确认会话就绪后，方可开启媒体流发送。AOQ SDK 提供 `enableSendMediaStream` 显式控制（见 [媒体流发送管理](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-function/aoq-media-stream-control.md)），WebRTC 需通过 `track.enabled = false` 或 `replaceTrack(null)` 实现等效门控（见 [通过WebRTC使用qwen3.5-omni-plus-realtime实现实时通话](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-best-practices/best-practice-webrtc-omni-realtime.md)）。
- **平台与权限**：
  - Android/iOS/HarmonyOS 需在清单文件中声明 `INTERNET`、`RECORD_AUDIO`、`CAMERA` 权限，并在运行时申请。
  - iOS 需在 `Info.plist` 中添加 `NSMicrophoneUsageDescription` 和 `NSCameraUsageDescription`。
- **浏览器限制**：WebRTC 在浏览器中受 CORS 约束，SDP 交换无法由前端直连百炼服务端，必须由业务后端代理完成。
- **SDK 初始化依赖**：`enableSendMediaStream`、`setAudioFrameObserver` 等 API 必须在 `createEngine` 之后、`connect` 之前调用，否则无效。

## 来源文档

- [Realtime API简介](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-overview.md)
- [SDK下载](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-quick-start-guide/realtime-sdk-download.md)
- [Token鉴权](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-quick-start-guide/realtime-token-authentication.md)
- [实现接通模型/应用](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-quick-start-guide/realtime-connect-model.md)
- [通过WebRTC使用多模态交互套件实现实时通话](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-best-practices/best-practice-webrtc-multimodal-dialog.md)
- [通过AOQ使用qwen3.5-omni-plus-realtime实现实时通话](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-best-practices/best-practice-aoq-omni-realtime.md)
- [AOQ SDK简介](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-desc.md)
- [通过WebRTC使用qwen3.5-omni-plus-realtime实现实时通话](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-best-practices/best-practice-webrtc-omni-realtime.md)
- [连接状态管理](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-function/aoq-connection-management.md)
- [媒体流发送管理](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-function/aoq-media-stream-control.md)
- [音频常用功能介绍](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-function/aoq-audio-features.md)
- [自定义音频播放](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-function/aoq-custom-audio-playback.md)
- [自定义音频采集](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-function/aoq-custom-audio-capture.md)
- [视频常用功能介绍](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-function/aoq-video-features.md)
- [自定义视频输入](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-function/aoq-custom-video-input.md)



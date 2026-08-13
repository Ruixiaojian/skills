# realtime api user guide

Realtime API 是百炼平台提供的低延迟、高可靠实时交互能力接口，支持 AOQ、WebRTC 和 WebSocket 三种传输协议，面向[多模态](../concepts/multimodal.md) AI 场景深度优化。开发者可根据终端类型、网络环境、功能需求和接入成本灵活选型，快速构建语音对话、实时翻译、全模态交互等应用。本文档系统梳理核心能力、参数配置、接入流程及关键约束，供开发者直接参考实施。

## 支持的模型/功能

Realtime API 当前支持以下模型与应用类型，但**不同协议的支持范围存在差异**：

- **实时全模态**：`qwen3.5-omni-plus-realtime`、`qwen3.5-omni-flash-realtime` —— 全协议（AOQ/WebRTC/WebSocket）均支持  
- **实时语音翻译**：`qwen3.5-livetranslate-flash-realtime` —— 全协议均支持  
- **[多模态](../concepts/multimodal.md)开发套件**：`multimodal-dialog` —— 全协议均支持  
- **实时语音识别（ASR）**：`Qwen-Audio-3.0-ASR-Flash-Streaming`、`Fun-ASR-Realtime` 系列 —— **仅 AOQ 和 WebSocket 支持，WebRTC 不支持**  
- **实时语音合成（TTS）**：`CosyVoice` 系列、`qwen-audio-3.0-tts-flash`、`qwen-audio-3.0-tts-plus` —— **仅 AOQ 和 WebSocket 支持，WebRTC 不支持**  
- **实时语音对话**：`qwen-audio-3.0-realtime-plus`、`qwen-audio-3.0-realtime-flash` —— 全协议均支持  

> **注意**：文档 [Realtime API 概述](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-overview.md) 明确列出 WebRTC 对 ASR/TTS 模型“不支持”，而部分旧版 SDK 示例或未更新的代码片段可能隐含错误假设。请以该文档为准，避免在 WebRTC 场景中尝试调用 ASR/TTS 模型。

模型最新名称、上下文长度、定价及快照版本，请始终以[阿里云百炼控制台](https://bailian.console.aliyun.com/cn-beijing#/home)为准；并发限流策略详见[限流文档](https://help.aliyun.com/zh/model-studio/rate-limit)。

## 关键参数

### 协议级通用参数
- `Authorization`: Bearer `<API_KEY>` —— 建连阶段必需，**不可暴露于客户端**（AOQ 推荐服务端代理鉴权）  
- `workspaceIdHash`: 工作区哈希值，由网关分配（如 `allocate` 接口响应中的 `extraInfo.workspaceIdHash`），AOQ 必填  
- `sid`: 会话唯一标识，由网关分配，AOQ 必填  
- `token`: 客户端连接令牌（如 `aoqTokenForClient`），AOQ 必填；WebSocket/WebRTC 中直接使用 API Key  
- `relayEndpoints` & `certFingerprint`: AOQ Relay 接入点及 TLS 证书指纹，用于 QUIC 连接建立  

### 会话配置参数（`session.update` 事件）
- `modalities`: 输出模态数组，如 `["text"]` 或 `["text","audio"]`  
- `voice`: TTS 音色名（如 `"Ethan"`），仅当 `modalities` 包含 `"audio"` 时生效  
- `input_audio_format` / `output_audio_format`: 当前仅支持 `"pcm"`  
- `instructions`: 系统角色指令（UTF-8 字符串）  
- `turn_detection`: 语音活动检测（VAD）配置对象  
  - `type`: `"server_vad"` 或 `"semantic_vad"`（推荐后者用于 Omni 系列）  
  - `threshold`: VAD 检测阈值（0.0–1.0）  
  - `silence_duration_ms`: 静音触发响应时长（毫秒）  

### AOQ SDK 特有参数
- `enableSendMediaStream(.audio, false)`：建连后默认禁用媒体发送，**必须在收到 `session.updated` 后显式启用**，否则服务端可能丢弃数据 [媒体流发送管理](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-function/aoq-media-stream-control.md)  
- `isExternal = true`：在 `startAudioCapture`/`startVideoCapture` 中启用外部采集模式，用于自定义音频/视频源注入 [自定义音频采集](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-function/aoq-custom-audio-capture.md)、[自定义视频输入](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-function/aoq-custom-video-input.md)  

## 使用方式

### 协议选型与接入路径
| 协议 | 适用场景 | 客户端依赖 | 关键步骤 |
|--------|-----------|-------------|------------|
| **AOQ** | 移动端原生 App、极致弱网对抗、[多模态](../concepts/multimodal.md)混合传输 | AOQ SDK（Android/iOS/HarmonyOS/Linux） | 1. 服务端调用 `allocate` 获取 `sid`/`token`/`relayEndpoints`<br>2. 客户端 `createEngine` → `connect(config)`<br>3. 监听 `onConnectionStatusChange(.connected)` → 发送 `session.update`<br>4. 监听 `onDataMsg("session.updated")` → 调用 `enableSendMediaStream(.audio, true)` |
| **WebRTC** | 浏览器端、已有 WebRTC 基础设施 | 浏览器原生 API 或 `aiortc` 等库 | 1. 客户端生成 Offer SDP<br>2. POST 到 `https://{endpoint}/api/v1/webrtc/realtime?model=...`（带 `Authorization`）<br>3. 解析 Answer SDP 并 `setRemoteDescription`<br>4. 通过 DataChannel（如 `"oai-events"`）收发 JSON 事件 |
| **WebSocket** | 服务端集成、快速原型验证、跨平台兼容 | DashScope SDK 或标准 WebSocket Client | 1. 直接 WebSocket 握手（`wss://...`），Header 带 `Authorization`<br>2. 发送 `session.update` 初始化会话<br>3. 通过文本帧或二进制帧传输音频/图像数据 |

### AOQ SDK 核心流程（必读）
1. **初始化与连接**：调用 `AoqClientEngine.createEngine()` 创建引擎，实现 `AoqEngineDelegate` 回调；`connect(config)` 触发状态迁移（`Connecting` → `Connected` 或 `Failed` → `Disconnected`）[连接状态管理](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-function/aoq-connection-management.md)  
2. **媒体流控制**：建连前调用 `enableSendMediaStream(.audio, false)`，收到 `session.updated` 后再启用，确保服务端已就绪  
3. **自定义扩展**：  
   - 音频：通过 `addAudioExternalStream()` + `pushAudioExternalStreamData()` 注入 TTS 或文件音频  
   - 视频：通过 `startVideoCapture(isExternal: true)` + `pushExternalVideoCapturedFrame()` 推送原始帧，或 `setVideoEncoderConfig(isExternal: true)` + `pushExternalVideoEncodedFrame()` 推送 JPEG 编码帧  

## 限制和注意事项

- **API Key 安全**：严禁硬编码于客户端。AOQ 必须采用服务端代理鉴权（AppServer 调用 `allocate` 获取临时 token）；WebSocket/WebRTC 若由客户端直连，需通过后端代理或短期 [Token](../concepts/token.md) 机制规避泄露风险 [Token鉴权](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-quick-start-guide/realtime-token-authentication.md)  
- **媒体流时序**：AOQ 下，**未收到 `session.updated` 前发送媒体流将导致服务端静默丢弃**。务必遵循“先禁用、后开启”流程，不可依赖默认行为  
- **编解码约束**：  
  - 输入音频：仅支持 16 kHz PCM（`input_audio_format: "pcm"`）  
  - 输出音频：仅支持 24 kHz PCM（`output_audio_format: "pcm"`）  
  - 视频编码：H.264 为主，JPEG 仅支持外部编码帧模式  
- **平台兼容性**：  
  - AOQ SDK 不支持浏览器环境，仅适用于原生客户端（Android/iOS/HarmonyOS/Linux）  
  - WebRTC 在浏览器中原生支持，移动端需依赖第三方 WebRTC 库（非阿里云提供）  
- **资源释放**：调用 `disconnect()` 后引擎仍存活，可重连；`destroy()` 才彻底释放资源。自定义音频/视频流推送线程必须在 `removeAudioExternalStream()`/`stopVideoCapture()` 前停止，避免访问已释放内存  
- **Opus 依赖**：AOQ SDK 使用插件方式加载 Opus 编解码器，集成时**必须下载并加载 `libPluginOpus`（Android/iOS/HarmonyOS）或 `PluginOpus.framework`（iOS）**，否则 Opus 编码失败 [SDK下载](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-quick-start-guide/realtime-sdk-download.md)

## 来源文档

- [Realtime API 概述](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-overview.md)
- [SDK下载](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-quick-start-guide/realtime-sdk-download.md)
- [接入模型与应用](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-quick-start-guide/realtime-connect-model.md)
- [Token鉴权](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-quick-start-guide/realtime-token-authentication.md)
- [AOQ SDK简介](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-desc.md)
- [连接状态管理](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-function/aoq-connection-management.md)
- [媒体流发送管理](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-function/aoq-media-stream-control.md)
- [自定义音频播放](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-function/aoq-custom-audio-playback.md)
- [自定义音频采集](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-function/aoq-custom-audio-capture.md)
- [视频常用功能介绍](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-function/aoq-video-features.md)
- [自定义视频输入](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-function/aoq-custom-video-input.md)
- [音频常用功能介绍](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-function/aoq-audio-features.md)



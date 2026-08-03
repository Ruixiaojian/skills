# realtime api user guide

Realtime API 是百炼平台提供的低延迟、高可靠实时交互能力，支持 AOQ、WebRTC 和 WebSocket 三种传输协议，面向多模态 AI 场景深度优化。开发者可根据终端类型、网络环境、功能需求和接入成本灵活选型，快速构建语音对话、实时翻译、音视频智能客服等应用。本文档聚焦核心开发路径，涵盖协议能力、关键参数、接入方式及限制说明。

## 支持的模型/功能

Realtime API 当前支持以下模型与应用类型，不同协议的支持情况存在差异：

- **实时全模态**：`qwen3.5-omni-plus-realtime`、`qwen3.5-omni-flash-realtime` —— 全协议支持（AOQ/WebRTC/WebSocket）  
- **实时语音翻译**：`qwen3.5-livetranslate-flash-realtime` —— 全协议支持  
- **多模态开发套件**：`multimodal-dialog` —— 全协议支持  
- **实时语音识别（ASR）**：`Qwen-Audio-3.0-ASR-Flash-Streaming`、`Fun-ASR-Realtime` 系列 —— **AOQ 和 WebSocket 支持，WebRTC 不支持**  
- **实时语音合成（TTS）**：`CosyVoice` 系列 —— **AOQ 和 WebSocket 支持，WebRTC 不支持**  
- **实时语音对话**：`qwen-audio-3.0-realtime-plus`、`qwen-audio-3.0-realtime-flash` —— 全协议支持  

> **注意**：文档 [接入模型与应用](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-quick-start-guide/realtime-connect-model.md) 中 WebRTC 接入示例代码存在截断（末尾为 `audioSender?.replaceTrack(audioTrack); videoSender?.replaceT`），实际使用时需补全完整逻辑；该问题已在 [Realtime API 概述](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-overview.md) 的“最佳实践”链接中提供完整参考实现。

模型最新名称、上下文长度、定价及快照版本请以[阿里云百炼控制台](https://bailian.console.aliyun.com/cn-beijing#/home)为准；并发限流策略详见官方限流文档。

## 关键参数

### 协议选择参数
- `x-dashscope-rtc-transport`：HTTP 请求头中指定协议，取值为 `moq`（AOQ）、`webrtc` 或留空（WebSocket 默认）  
- `clientIp`（AOQ 专属）：建连请求体中可选字段，用于指定客户端真实公网 IP，影响 Relay 接入点分配；不填则默认使用网关请求 IP  

### 会话配置参数（`session.update` 事件）
- `modalities`：输出模态数组，如 `["text"]` 或 `["text","audio"]`  
- `voice`：TTS 音色标识（如 `"Ethan"`）  
- `input_audio_format` / `output_audio_format`：当前仅支持 `"pcm"`  
- `turn_detection`：语音活动检测配置，推荐 `semantic_vad` 类型（适用于 `qwen3.5-omni-realtime` 系列）  
- `instructions`：系统角色指令，影响模型行为  

### SDK 配置参数（AOQ）
- `AoqConnectConfig`：包含 `token`、`sid`、`certFingerprint`、`relayEndpoints`、`workspaceIdHash` 等必填字段  
- `AoqAudioCodecConfig`：需显式设置 `codecType`（`AudioPCM` 或 `AudioOpus`）、`sampleRate`（ASR/TTS 常用 16kHz，Omni 输出常用 24kHz）  
- `enableSendMediaStream`：连接后需显式调用 `false` 禁用，待收到 `session.updated` 后再设为 `true`，否则服务端可能拒绝接收媒体流 [媒体流发送管理](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-function/aoq-media-stream-control.md)

## 使用方式

### 1. 协议选型与接入路径
- **AOQ**：适用于移动端原生 App（Android/iOS/HarmonyOS/Linux），需集成 [AOQ SDK](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-quick-start-guide/realtime-sdk-download.md)，具备极致弱网对抗与内置 AEC/降噪能力  
- **WebRTC**：适用于浏览器端或已有 WebRTC 基础设施的场景，无需专用 SDK，直接使用标准 WebRTC API；但需白名单开通，Endpoint 需联系商务获取  
- **WebSocket**：适用于服务端集成或快速原型验证，接入门槛最低，通过 DashScope SDK 即可调用  

### 2. 鉴权流程（统一要求）
所有协议均在**建连阶段**通过 HTTP Header `Authorization: Bearer <API_KEY>` 完成鉴权：
- **AOQ**：API Key 由业务 AppServer 持有并请求网关，客户端使用网关返回的 `aoqTokenForClient` 连接  
- **WebRTC**：API Key 在 SDP 交换 HTTP 请求中携带  
- **WebSocket**：API Key 在 WebSocket 握手请求中携带  
> **注意**：API Key 绝不可硬编码于客户端，必须通过后端服务安全下发 [Token鉴权](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-quick-start-guide/realtime-token-authentication.md)

### 3. AOQ 典型接入步骤
1. 业务 AppServer 调用网关 allocate 接口获取 `aoqTokenForClient`、`sid`、`relayEndpoints` 等凭证  
2. 客户端创建 `AoqClientEngine`，设置 `onConnectionStatusChange` 回调  
3. 调用 `startAudioCapture()` / `startVideoCapture()` 启动采集（可选 `isExternal=true` 切换至自定义采集）  
4. 构造 `AoqConnectConfig` 并调用 `connect()`，**连接前务必调用 `enableSendMediaStream(.audio, false)`**  
5. 在 `onDataMsg` 中监听 `session.updated`，收到后调用 `enableSendMediaStream(.audio, true)` 开启媒体发送  
6. 通过 `pushAudioExternalStreamData` 或 `pushExternalVideoCapturedFrame` 实现自定义音视频输入（如 TTS 输出、屏幕共享）  

### 4. 自定义音视频能力
- **音频**：支持外部采集（`isExternal=true`）、外部播放（`isExternal=true` + `setAudioFrameObserver`）、文件混音、TTS 流注入 [自定义音频采集](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-function/aoq-custom-audio-capture.md)、[自定义音频播放](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-function/aoq-custom-audio-playback.md)  
- **视频**：支持原始帧（I420/NV12/BGRA）或已编码帧（JPEG）两种自定义输入模式，需正确配置 `isExternal` 标志位 [自定义视频输入](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-function/aoq-custom-video-input.md)  

## 限制和注意事项

- **协议兼容性限制**：WebRTC 不支持 ASR/TTS 模型，仅支持全模态与对话类模型；WebSocket 无内置 AEC/降噪，需客户端自行处理回声与噪声  
- **AOQ SDK 依赖**：必须配套下载 Opus 编解码插件（`libPluginOpus.zip` 或 `PluginOpus.framework.zip`），否则无法启用 Opus 编码 [SDK下载](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-quick-start-guide/realtime-sdk-download.md)  
- **连接状态管理**：AOQ SDK 状态机为 `Connecting → Connected/Failed → Disconnected`，`Failed` 为瞬态，SDK 自动迁移至 `Disconnected`，业务层无需在 `onConnectionStatusChange(Failed)` 中调用 `disconnect` [连接状态管理](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-function/aoq-connection-management.md)  
- **媒体流控制强制要求**：AOQ 接入时，**必须在 `connect()` 前禁用媒体发送，并在收到 `session.updated` 后开启**；否则模型可能因未就绪而丢弃数据或报错  
- **性能与资源**：外部音频流推送需严格遵循 `10ms/帧`（实时采集）或 `40ms/帧+30ms sleep`（文件解析）节奏，缓冲区满（错误码 110）时需重试而非丢弃 [音频常用功能介绍](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-function/aoq-audio-features.md)  
- **地域与域名**：Endpoint 需根据实际部署地域选择，具体列表参见[地域及接入域名](https://help.aliyun.com/zh/model-studio/regions/)

## 来源文档

- [Realtime API 概述](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-overview.md)
- [SDK下载](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-quick-start-guide/realtime-sdk-download.md)
- [Token鉴权](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-quick-start-guide/realtime-token-authentication.md)
- [接入模型与应用](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-quick-start-guide/realtime-connect-model.md)
- [AOQ SDK简介](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-desc.md)
- [连接状态管理](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-function/aoq-connection-management.md)
- [音频常用功能介绍](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-function/aoq-audio-features.md)
- [自定义音频播放](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-function/aoq-custom-audio-playback.md)
- [自定义音频采集](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-function/aoq-custom-audio-capture.md)
- [自定义视频输入](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-function/aoq-custom-video-input.md)
- [视频常用功能介绍](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-function/aoq-video-features.md)
- [媒体流发送管理](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-function/aoq-media-stream-control.md)



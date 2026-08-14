# realtime api user guide

Realtime API 是百炼平台提供的低延迟、高可靠实时交互能力，支持多模态（音视频+文本）端到端实时处理。它通过 AOQ、WebRTC 和 WebSocket 三种传输协议，适配不同终端、网络环境与业务需求，开发者可根据场景选择最优接入路径。所有协议均基于统一的模型服务层，共享模型能力与鉴权体系。

## 支持的模型/功能

Realtime API 支持以下核心模型与应用类型，但**协议支持存在差异**：

- **实时全模态**（`qwen3.5-omni-plus-realtime`, `qwen3.5-omni-flash-realtime`）：AOQ、WebRTC、WebSocket 均支持  
- **实时语音翻译**（`qwen3.5-livetranslate-flash-realtime`）：AOQ、WebRTC、WebSocket 均支持  
- **多模态开发套件**（`multimodal-dialog`）：AOQ、WebRTC、WebSocket 均支持  
- **实时语音识别**（`Qwen-Audio-3.0-ASR-Flash-Streaming`, `Fun-ASR-Realtime` 系列）：**仅 AOQ 和 WebSocket 支持**，WebRTC 不支持 [原文标题](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-overview.md)  
- **实时语音合成**（`CosyVoice` 系列、`qwen-audio-3.0-tts-flash`、`qwen-audio-3.0-tts-plus`）：**仅 AOQ 和 WebSocket 支持**，WebRTC 不支持 [原文标题](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-overview.md)  
- **实时语音对话**（`qwen-audio-3.0-realtime-plus`, `qwen-audio-3.0-realtime-flash`）：AOQ、WebRTC、WebSocket 均支持  

> **注意**：文档 1 明确指出 WebRTC 不支持 ASR/TTS 模型，但文档 3 的 WebRTC 接入示例中未体现该限制，且未提供替代方案。实际接入时请以文档 1 的模型支持矩阵为准，避免在 WebRTC 场景下误用 ASR/TTS 模型。

## 关键参数

### 协议通用参数
- `Authorization: Bearer <API_KEY>`：建连阶段 HTTP Header 鉴权，**客户端不得硬编码 API Key**，应由业务 AppServer 代理请求并下发临时凭证 [原文标题](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-quick-start-guide/realtime-token-authentication.md)  
- `model`：URL 查询参数，指定目标模型名称（如 `qwen3.5-omni-plus-realtime`）  
- `workspaceIdHash`：工作区哈希值，用于路由和计费，由网关分配  

### AOQ 特有参数（`AoqConnectConfig`）
- `token`：客户端连接令牌（`aoqTokenForClient`），非 API Key  
- `sid`：会话唯一标识  
- `certFingerprint`：Relay TLS 证书指纹（`clientRelayCertFingerprint`）  
- `relayEndpoints`：Relay 接入点数组（含 `endpoint` 和 `port`）  
- `publishTracks` / `subscribeTracks`：媒体轨道配置（必须包含 `.audio` 和 `.data` 轨道）  

### session.update 事件参数（关键会话配置）
- `modalities`: `["text"]` 或 `["text","audio"]`，控制输出模态  
- `voice`: 输出音色（如 `"Ethan"`）  
- `input_audio_format`: 固定为 `"pcm"`（16kHz 采样率）  
- `output_audio_format`: 固定为 `"pcm"`（24kHz 采样率）  
- `instructions`: 系统角色提示词  
- `turn_detection`: 语音活动检测配置，`type` 推荐 `"semantic_vad"`（配合 Omni 系列模型）  

## 使用方式

### 协议选型建议
- **AOQ**：移动端原生应用首选，尤其需弱网对抗、多模态混合传输或内置 AEC/降噪能力的场景  
- **WebRTC**：浏览器端互动或已有 WebRTC 基础设施的场景，依赖浏览器原生支持  
- **WebSocket**：服务端集成、快速原型验证或跨平台轻量接入，接入门槛最低  

### AOQ 接入核心流程
1. **AppServer 代理鉴权**：调用百炼 `/api/v1/webrtc/realtime`（带 `x-dashscope-rtc-transport: moq`）获取 `sid`、`aoqTokenForClient` 等凭证  
2. **创建引擎并注册回调**：实现 `AoqEngineDelegate` 监听 `onConnectionStatusChange`、`onDataMsg`  
3. **预配置媒体流**：调用 `enableSendMediaStream(.audio, false)` 禁用发送，避免过早推流  
4. **建连**：传入 `AoqConnectConfig` 调用 `connect()`  
5. **等待会话就绪**：收到 `session.updated` 服务端事件后，调用 `enableSendMediaStream(.audio, true)` 开启媒体发送  
6. **销毁资源**：断开连接后调用 `disconnect()` 和 `destroy()`  

### WebRTC 接入要点
- 无需专用 SDK，直接使用浏览器原生 `RTCPeerConnection`  
- 必须添加 `AudioStreamTrack` 以确保 Offer SDP 包含 `m=audio`（服务端必需）  
- 必须创建名为 `"oai-events"` 的 `DataChannel`（服务端通过此通道推送事件）  
- SDP 交换阶段完成鉴权（HTTP POST 请求携带 `Authorization`）  

### WebSocket 接入
- 参见 [安装SDK](https://help.aliyun.com/zh/model-studio/install-sdk) 获取通用 DashScope SDK  
- 通过 SDK 的 `RealtimeClient` 类发起连接，自动处理握手与消息序列化  

## 限制和注意事项

- **建连鉴权仅一次**：`Authorization` 头仅在建连 HTTP 请求中生效，后续数据帧无需重复鉴权  
- **媒体流发送时机**：AOQ 下必须在收到 `session.updated` 后再开启媒体发送，否则服务端可能丢弃数据 [原文标题](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-function/aoq-media-stream-control.md)  
- **Opus 编解码依赖**：AOQ SDK 需额外下载并加载 Opus [插件](../concepts/plugin.md)（`libPluginOpus.zip` 或 `PluginOpus.framework.zip`），否则无法启用 Opus 编码 [原文标题](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-quick-start-guide/realtime-sdk-download.md)  
- **自定义采集/播放**：  
  - 外部音频流需在 `Connected` 状态后调用 `addAudioExternalStream()`，并严格管理 `pushAudioExternalStreamData()` 的推送循环与缓冲区满（错误码 110）重试逻辑  
  - 自定义视频输入分“原始帧”与“编码帧”两种模式，二者不可混用；原始帧模式需先调用 `startVideoCapture(isExternal=true)`，编码帧模式则跳过采集启动步骤  
- **平台兼容性**：AOQ 仅支持 Android/iOS/HarmonyOS/Linux；WebRTC 原生支持浏览器；WebSocket 兼容任意支持标准 WebSocket 的环境

## 来源文档

- [Realtime API 概述](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-overview.md)
- [SDK下载](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-quick-start-guide/realtime-sdk-download.md)
- [接入模型与应用](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-quick-start-guide/realtime-connect-model.md)
- [AOQ SDK简介](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-desc.md)
- [Token鉴权](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-quick-start-guide/realtime-token-authentication.md)
- [连接状态管理](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-function/aoq-connection-management.md)
- [媒体流发送管理](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-function/aoq-media-stream-control.md)
- [音频常用功能介绍](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-function/aoq-audio-features.md)
- [自定义音频播放](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-function/aoq-custom-audio-playback.md)
- [自定义音频采集](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-function/aoq-custom-audio-capture.md)
- [视频常用功能介绍](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-function/aoq-video-features.md)
- [自定义视频输入](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-function/aoq-custom-video-input.md)



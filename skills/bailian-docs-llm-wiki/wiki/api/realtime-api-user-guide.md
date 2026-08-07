# realtime api user guide

Realtime API 是阿里云百炼平台提供的低延迟、高可靠实时交互能力，支持 AOQ、WebRTC 和 WebSocket 三种传输协议，面向[多模态](../concepts/multi-modal.md) AI 场景深度优化。开发者可根据业务需求（如弱网对抗、浏览器兼容性、接入成本）选择合适协议，并通过统一的 [Token](../concepts/token.md) 鉴权机制安全接入。所有协议均基于 DashScope SDK 或标准 Web API 实现，无需自建信令或媒体服务器。

## 支持的模型/功能

Realtime API 当前支持以下核心模型与应用类型，各协议支持情况一致（详见 [Realtime API 概述](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-overview.md)）：

- **实时全模态**：`qwen3.5-omni-plus-realtime`、`qwen3.5-omni-flash-realtime`  
- **实时语音翻译**：`qwen3.5-livetranslate-flash-realtime`  
- **[多模态](../concepts/multi-modal.md)开发套件**：`multimodal-dialog`  
- **实时语音识别（ASR）**：`Qwen-Audio-3.0-ASR-Flash-Streaming`、`Fun-ASR-Realtime` 系列  
- **实时语音合成（TTS）**：`CosyVoice` 系列  
- **实时语音对话**：`qwen-audio-3.0-realtime-plus`、`qwen-audio-3.0-realtime-flash`  

> **注意**：文档 1 明确指出 ASR 和 TTS 模型 **不支持 WebRTC 协议**，但文档 4 的“WebRTC 接入”章节示例中未体现该限制，且未说明替代方案。实际集成时请以 [Realtime API 概述](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-overview.md) 中的协议支持矩阵为准。

## 关键参数

### 鉴权参数
- `Authorization: Bearer <API_KEY>`：仅用于建连阶段 HTTP 请求头，**不可暴露于客户端**（AOQ 协议需服务端代理获取临时 token）。
- `x-dashscope-rtc-transport`：协议标识，AOQ 固定为 `moq`；WebRTC 和 WebSocket 不需此 header。

### 连接凭证（AOQ 专用）
- `aoqTokenForClient`：客户端 SDK 初始化必需字段，由服务端 allocate 接口返回。
- `sid`：会话唯一 ID，必须传入 SDK。
- `clientRelayEndpoints`：Relay 接入点列表，含 `endpoint` 和 `port`。
- `clientRelayCertFingerprint`：TLS 证书指纹，用于校验 Relay 安全性。
- `workspaceIdHash`：工作区标识哈希，影响模型上下文隔离。

### 会话配置（`session.update` 事件）
- `modalities`：输出模态数组，如 `["text", "audio"]`。
- `voice`：TTS 音色名（如 `"Ethan"`）。
- `input_audio_format` / `output_audio_format`：当前仅支持 `"pcm"`。
- `turn_detection`：VAD 配置对象，推荐 `type: "semantic_vad"`（适用于 Omni 系列模型）。

## 使用方式

### 协议选型与接入路径
| 协议 | 适用场景 | 客户端依赖 | 典型接入路径 |
|------|----------|------------|--------------|
| **AOQ** | 移动端原生 App、极致弱网/低延迟需求 | [AOQ SDK](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-quick-start-guide/realtime-sdk-download.md)（Android/iOS/Harmony/Linux） | 服务端调用 allocate → 获取 `aoqTokenForClient` → 客户端 SDK `connect()` → 收到 `session.updated` 后启用媒体流 |
| **WebRTC** | 浏览器端实时互动、已有 WebRTC 基础设施 | 浏览器原生 API 或 `aiortc`（服务端） | 客户端生成 Offer → POST 到 `/api/v1/webrtc/realtime?model=xxx` → 服务端返回 Answer → ICE 自动建连 |
| **WebSocket** | 服务端集成、快速原型验证、跨平台兼容 | DashScope SDK 或标准 WebSocket Client | 直接 WebSocket 握手（带 `Authorization` header）→ 发送 `session.update` → 开始流式收发 |

### AOQ 核心流程（关键实践）
1. **连接前禁用媒体发送**：调用 `enableSendMediaStream(.audio, false)` 和 `enableSendMediaStream(.video, false)`，避免模型未就绪时数据丢失。
2. **收到 `session.updated` 后启用**：在 `onDataMsg` 回调中解析事件，确认后调用 `enableSendMediaStream(true)`。
3. **媒体控制独立**：音频与视频可分别启停，例如仅推送音频时无需启动视频采集（见 [媒体流发送管理](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-function/aoq-media-stream-control.md)）。

### 自定义音视频处理
- **自定义音频采集**：设置 `isExternal=true` 后，通过 `addAudioExternalStream()` 注册流，再循环调用 `pushAudioExternalStreamData()` 推送 PCM 数据（[自定义音频采集](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-function/aoq-custom-audio-capture.md)）。
- **自定义音频播放**：设置 `isExternal=true` 后，注册 `setAudioFrameObserver()` 监听 `onPlaybackAudioFrame`，自行渲染 PCM 数据（[自定义音频播放](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-function/aoq-custom-audio-playback.md)）。
- **自定义视频输入**：分原始帧（`pushExternalVideoCapturedFrame`）和编码帧（`pushExternalVideoEncodedFrame`）两种模式，需显式配置 `isExternal=true` 并匹配像素格式（[自定义视频输入](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-function/aoq-custom-video-input.md)）。

## 限制和注意事项

- **API Key 安全**：严禁硬编码于客户端或提交至代码仓库。AOQ 协议强制要求服务端代理鉴权，客户端仅使用临时 `aoqTokenForClient`。
- **建连超时**：AOQ `sid` 默认有效期为 7200 秒（2 小时），过期需重新 allocate；WebSocket 连接超时由客户端实现决定。
- **媒体流时机**：未收到 `session.updated` 前发送媒体数据将被服务端丢弃，务必遵循“先禁用、后开启”流程（[媒体流发送管理](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-function/aoq-media-stream-control.md)）。
- **Opus 编解码依赖**：AOQ SDK 需额外下载并加载 Opus 插件（如 `libPluginOpus.zip`），否则 ASR/TTS 功能不可用（见 [SDK下载](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-quick-start-guide/realtime-sdk-download.md)）。
- **WebRTC 白名单**：WebRTC Endpoint 为白名单开放，需联系商务经理获取接入权限（文档 3 明确提示）。

## 来源文档

- [Realtime API 概述](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-overview.md)
- [SDK下载](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-quick-start-guide/realtime-sdk-download.md)
- [Token鉴权](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-quick-start-guide/realtime-token-authentication.md)
- [接入模型与应用](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-quick-start-guide/realtime-connect-model.md)
- [AOQ SDK简介](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-desc.md)
- [连接状态管理](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-function/aoq-connection-management.md)
- [媒体流发送管理](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-function/aoq-media-stream-control.md)
- [音频常用功能介绍](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-function/aoq-audio-features.md)
- [自定义音频播放](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-function/aoq-custom-audio-playback.md)
- [自定义音频采集](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-function/aoq-custom-audio-capture.md)
- [视频常用功能介绍](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-function/aoq-video-features.md)
- [自定义视频输入](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-function/aoq-custom-video-input.md)



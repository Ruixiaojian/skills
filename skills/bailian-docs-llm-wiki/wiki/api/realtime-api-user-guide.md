# realtime api user guide

Realtime API 是面向 AI [多模态](../concepts/multimodal.md)实时交互场景的低延迟、高鲁棒性通信协议栈，支持 AOQ（AI over QUIC）、WebRTC 和 WebSocket 三种传输协议，适配不同终端、网络环境与开发复杂度需求。开发者可根据业务对延迟、弱网对抗、浏览器兼容性及接入成本的要求，选择最合适的协议方案。

## 支持的模型/功能

Realtime API 支持以下模型与应用类型，但**协议支持存在差异**：

- **实时全模态**（`qwen3.5-omni-plus-realtime`, `qwen3.5-omni-flash-realtime`）：AOQ、WebRTC、WebSocket 均支持  
- **实时语音翻译**（`qwen3.5-livetranslate-flash-realtime`）：AOQ、WebRTC、WebSocket 均支持  
- **[多模态](../concepts/multimodal.md)开发套件**（`multimodal-dialog`）：AOQ、WebRTC、WebSocket 均支持  
- **实时语音识别**（`Qwen-Audio-3.0-ASR-Flash-Streaming`, `Fun-ASR-Realtime` 系列）：**仅 AOQ 和 WebSocket 支持**，WebRTC 不支持 [原文标题](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-overview.md)  
- **实时语音合成**（`CosyVoice` 系列）：**仅 AOQ 和 WebSocket 支持**，WebRTC 不支持 [原文标题](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-overview.md)  
- **实时语音对话**（`qwen-audio-3.0-realtime-plus`, `qwen-audio-3.0-realtime-flash`）：AOQ、WebRTC、WebSocket 均支持  

> **注意**：文档 1 中明确列出 WebRTC 对 ASR/TTS 模型“不支持”，但文档 4 的 WebRTC 接入示例中未体现该限制，且未提供替代方案。实际集成时请以文档 1 的模型支持矩阵为准，避免在 WebRTC 场景下误用 ASR/TTS 模型。

## 关键参数

| 参数 | 协议适用性 | 说明 |
|------|------------|------|
| `Authorization: Bearer <API_KEY>` | 所有协议 | **建连阶段唯一鉴权方式**，通过 HTTP Header 传递；连接建立后无需重复鉴权。API Key 必须由服务端管理，严禁硬编码至客户端 [原文标题](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-quick-start-guide/realtime-token-authentication.md) |
| `x-dashscope-rtc-transport: moq` | AOQ | 请求头中指定 AOQ 协议，用于服务端路由 |
| `clientIp`（选填） | AOQ | 客户端真实公网 IP，用于 Relay 接入点最优分配；若不填，则使用请求网关的 IP |
| `sid` / `aoqTokenForClient` / `clientRelayCertFingerprint` | AOQ | AOQ 连接必需凭证，由服务端 allocate 接口返回，客户端 SDK 直接使用 |
| SDP Offer/Answer | WebRTC | 通过 `application/sdp` Content-Type 的 HTTP POST 交换，鉴权同步完成 |
| `model` 查询参数 | 所有协议 | URL 中必需，如 `?model=qwen3.5-omni-plus-realtime`，决定后端模型路由 |

## 使用方式

### 协议选型建议
- **AOQ**：移动端原生应用首选，尤其适用于弱网、[多模态](../concepts/multimodal.md)（音视频+文本）、需内置回声消除/降噪的场景；需集成 [AOQ SDK](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-quick-start-guide/realtime-sdk-download.md)  
- **WebRTC**：浏览器端或已有 WebRTC 基础设施的场景；无专用 SDK，依赖浏览器原生 API 或标准 WebRTC 库  
- **WebSocket**：服务端集成、快速原型验证、低门槛接入；推荐通过 DashScope SDK 封装使用  

### AOQ 核心流程（必须遵循）
1. **服务端申请凭证**：AppServer 调用百炼 allocate 接口，传入 `API_KEY` 和 `model`，获取 `sid`、`aoqTokenForClient` 等字段  
2. **客户端初始化引擎**：调用 `AoqClientEngine.createEngine()`，设置 `AoqEngineDelegate` 回调  
3. **连接前禁用媒体发送**：`engine.enableSendMediaStream(.audio, enable: false)`（关键！）  
4. **发起连接**：传入 `aoqTokenForClient`、`sid`、`relayEndpoints` 等配置调用 `connect()`  
5. **等待 `session.updated` 后开启发送**：收到服务端事件后，再调用 `enableSendMediaStream(.audio, enable: true)`，否则服务端可能拒绝接收数据 [原文标题](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-function/aoq-media-stream-control.md)  

### 自定义媒体流（高级场景）
- **音频**：通过 `addAudioExternalStream()` + `pushAudioExternalStreamData()` 注入 TTS 或文件音频；启用 `enable3A` 可对输入 PCM 进行回声消除等处理  
- **视频**：支持两种模式：  
  - *原始帧模式*：`startVideoCapture(isExternal: true)` 后调用 `pushExternalVideoCapturedFrame()`（支持 I420/NV12/BGRA 等格式）  
  - *编码帧模式*：`setVideoEncoderConfig(isExternal: true)` 后调用 `pushExternalVideoEncodedFrame()`（当前仅 JPEG）  

## 限制和注意事项

- **AOQ [Token](../concepts/token.md) 有效期**：`sidExpiresInSecs` 字段返回会话过期时间（默认 7200 秒），超时需重新 allocate  
- **媒体流控制时机**：`enableSendMediaStream()` 必须在 `createEngine()` 之后、`connect()` 之前调用；未调用则 connect 成功后立即发送，易导致服务端丢弃数据  
- **SDK 状态机**：AOQ 连接状态为 `Connecting` → `Connected`/`Failed` → `Disconnected`；`Failed` 为瞬态，SDK 自动迁移至 `Disconnected`，业务层无需主动 `disconnect` [原文标题](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-function/aoq-connection-management.md)  
- **Opus 编解码依赖**：AOQ SDK 需额外下载并加载 Opus [插件](../concepts/plugin.md)（如 `libPluginOpus.zip`），否则音频功能不可用  
- **WebRTC 白名单**：当前 WebRTC 功能为白名单开放，需联系商务经理获取 Endpoint，非公开可用  
- **浏览器兼容性**：AOQ 不支持浏览器环境；WebRTC 和 WebSocket 均原生支持浏览器，但 WebRTC 需用户授权麦克风/摄像头

## 来源文档

- [Realtime API 概述](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-overview.md)
- [SDK下载](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-quick-start-guide/realtime-sdk-download.md)
- [Token鉴权](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-quick-start-guide/realtime-token-authentication.md)
- [接入模型与应用](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-quick-start-guide/realtime-connect-model.md)
- [AOQ SDK简介](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-desc.md)
- [连接状态管理](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-function/aoq-connection-management.md)
- [音频常用功能介绍](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-function/aoq-audio-features.md)
- [媒体流发送管理](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-function/aoq-media-stream-control.md)
- [自定义音频播放](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-function/aoq-custom-audio-playback.md)
- [自定义音频采集](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-function/aoq-custom-audio-capture.md)
- [视频常用功能介绍](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-function/aoq-video-features.md)
- [自定义视频输入](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-function/aoq-custom-video-input.md)



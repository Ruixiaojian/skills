# realtime api user guide

Realtime API 是百炼平台提供的低延迟、高可靠实时交互能力接口，支持多模态（音视频+文本）端到端实时处理。它通过 AOQ、WebRTC 和 WebSocket 三种传输协议，适配不同终端环境与业务场景，为开发者提供灵活、安全、可扩展的实时 AI 服务接入方式。

## 支持的模型/功能

Realtime API 当前支持以下模型与应用类型，但**协议支持存在差异**：

- **实时全模态**（`qwen3.5-omni-plus-realtime`, `qwen3.5-omni-flash-realtime`）：AOQ、WebRTC、WebSocket 均支持  
- **实时语音翻译**（`qwen3.5-livetranslate-flash-realtime`）：AOQ、WebRTC、WebSocket 均支持  
- **多模态开发套件**（`multimodal-dialog`）：AOQ、WebRTC、WebSocket 均支持  
- **实时语音识别**（`Qwen-Audio-3.0-ASR-Flash-Streaming`, `Fun-ASR-Realtime` 系列）：**仅 AOQ 和 WebSocket 支持**，WebRTC 不支持  
- **实时语音合成**（`CosyVoice` 系列、`qwen-audio-3.0-tts-flash`、`qwen-audio-3.0-tts-plus`）：**仅 AOQ 和 WebSocket 支持**，WebRTC 不支持  
- **实时语音对话**（`qwen-audio-3.0-realtime-plus`, `qwen-audio-3.0-realtime-flash`）：AOQ、WebRTC、WebSocket 均支持  

> **注意**：文档 1 中明确列出 WebRTC 对 ASR/TTS 模型“不支持”，但文档 4 的 WebRTC 接入章节未提及此限制，也未提供对应模型的 WebRTC 连接示例。实际开发中请以文档 1 的模型支持矩阵为准，避免在 WebRTC 场景下误用 ASR/TTS 模型。该矛盾已在[Realtime API 概述](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-overview.md)中权威定义。

## 关键参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `model` | string | 是 | 模型标识符，如 `qwen3.5-omni-plus-realtime`；需与所选协议兼容（见上节） |
| `Authorization` | string | 是 | HTTP Header，格式为 `Bearer <API_KEY>`；建连阶段一次性鉴权，详见 [Token鉴权](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-quick-start-guide/realtime-token-authentication.md) |
| `x-dashscope-rtc-transport` | string | 否（AOQ 专用） | 值为 `moq`，用于显式指定 AOQ 协议 |
| `clientIp` | string | 否 | 客户端真实公网 IP，用于 Relay 节点智能调度；若不填则使用请求网关的 IP |
| `sid`, `aoqTokenForClient`, `clientRelayCertFingerprint`, `clientRelayEndpoints` | string/object | 是（AOQ 客户端） | AOQ 连接凭证，由 AppServer 调用 allocate 接口获取，不可直接使用 API Key |

## 使用方式

### 协议选型建议
- **AOQ**：移动端原生应用首选，尤其适用于弱网、多模态、需内置回声消除/降噪的场景；需集成 [AOQ SDK](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-quick-start-guide/realtime-sdk-download.md) 并完成服务端代理鉴权。
- **WebRTC**：浏览器端或已有 WebRTC 基础设施的场景；无需 SDK，直接使用浏览器原生 API 或标准 WebRTC 库；SDP 交换阶段完成鉴权。
- **WebSocket**：服务端集成、快速原型验证、纯文本/低实时性需求场景；可通过 DashScope SDK 快速接入。

### AOQ 典型流程（关键步骤）
1. **服务端获取凭证**：AppServer 调用 `/api/v1/webrtc/realtime?model=xxx`（带 `x-dashscope-rtc-transport: moq`），传入 `clientIp`，获取 `sid`、`aoqTokenForClient` 等字段；
2. **客户端连接**：使用 AOQ SDK 初始化引擎后，调用 `connect(config)`，传入上述凭证；
3. **媒体流控制**：建连后默认发送媒体流，但**必须等待收到 `session.updated` 服务端事件后**，再调用 `enableSendMediaStream(.audio, true)` 开启音频发送（见 [媒体流发送管理](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-function/aoq-media-stream-control.md)）；
4. **自定义采集/播放（可选）**：如需接管音频/视频数据流，可启用外部采集（`isExternal=true`）并配合 `pushAudioExternalStreamData` 或 `pushExternalVideoCapturedFrame` 使用（见 [自定义音频采集](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-function/aoq-custom-audio-capture.md) 和 [自定义视频输入](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-function/aoq-custom-video-input.md)）。

## 限制和注意事项

- **鉴权安全**：API Key **严禁硬编码于客户端**，AOQ 协议强制要求服务端代理鉴权，客户端仅使用临时 `aoqTokenForClient`；其他协议也应通过服务端中转完成建连。
- **连接状态管理**：AOQ SDK 提供明确的状态机（`Connecting` → `Connected`/`Failed` → `Disconnected`），业务层需监听 `onConnectionStatusChange` 回调，`Failed` 为瞬态，SDK 会自动迁移至 `Disconnected`，无需手动调用 `disconnect`（见 [连接状态管理](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/aoq-connection-management.md)）。
- **媒体流时序**：对于多数实时模型（尤其是 Omni 系列），**必须在收到 `session.updated` 后才开启媒体发送**，否则服务端可能拒绝接收数据或导致会话异常；此规则是强约束，非最佳实践建议。
- **编解码依赖**：AOQ SDK 使用 Opus 编解码器需单独下载并集成 `PluginOpus` 插件（见 [SDK下载](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-quick-start-guide/realtime-sdk-download.md)）。
- **平台兼容性**：AOQ 不支持浏览器环境；WebRTC 在浏览器中原生支持，但对 ASR/TTS 模型无支持；WebSocket 兼容性最广，但弱网对抗能力最弱。

## 来源文档

- [Realtime API 概述](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-overview.md)
- [Token鉴权](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-quick-start-guide/realtime-token-authentication.md)
- [SDK下载](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-quick-start-guide/realtime-sdk-download.md)
- [接入模型与应用](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-quick-start-guide/realtime-connect-model.md)
- [AOQ SDK简介](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-desc.md)
- [连接状态管理](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-function/aoq-connection-management.md)
- [媒体流发送管理](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-function/aoq-media-stream-control.md)
- [音频常用功能介绍](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-function/aoq-audio-features.md)
- [自定义音频播放](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-function/aoq-custom-audio-playback.md)
- [自定义音频采集](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-function/aoq-custom-audio-capture.md)
- [视频常用功能介绍](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-function/aoq-video-features.md)
- [自定义视频输入](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-function/aoq-custom-video-input.md)



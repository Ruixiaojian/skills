# realtime api user guide

Realtime API 是百炼平台提供的低延迟、高可靠实时交互能力，支持多模态（音视频+文本）AI 场景。它通过 AOQ（AI over QUIC）、WebRTC 和 WebSocket 三种传输协议，分别面向移动端原生应用、浏览器端互动和服务端快速集成等不同技术栈与业务需求。开发者可根据场景特性（如弱网对抗、建连速度、接入成本、端侧兼容性）选择最适配的协议。

## 支持的模型/功能

Realtime API 当前支持以下核心模型与能力：

- **实时全模态交互**：`qwen3.5-omni-plus-realtime`、`qwen3.5-omni-flash-realtime`、`qwen3.5-livetranslate-flash-realtime`，支持音视频输入 + 文本/音频输出，适用于智能客服、远程协作等场景。  
- **多模态开发套件**：`multimodal-dialog`，提供结构化对话管理能力，**仅 WebRTC 和 WebSocket 支持**，AOQ 不支持 [Realtime API 概述](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-overview.md)。  
- **单模态能力**：`Fun-ASR`（语音识别）、`CosyVoice`（语音合成）、`qwen-audio-3.0-realtime-plus/flash`（语音对话）**仅 WebSocket 协议支持**，AOQ 与 WebRTC 均不支持该类模型。

> **注意**：文档 1 中表格明确标注 `multimodal-dialog` 在 AOQ 列为“不支持”，但部分旧版示例代码或社区文档曾暗示其 AOQ 兼容性。请以[Realtime API 概述](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-overview.md)为准，AOQ 当前不支持该套件。

## 关键参数

| 参数 | 说明 | 协议适用性 |
|------|------|-------------|
| `modalities` | 输出模态列表，如 `["text"]` 或 `["text","audio"]`；决定是否返回合成语音 | 全协议（AOQ/WebRTC/WebSocket）均需在 `session.update` 中指定 |
| `voice` | 合成语音音色（如 `"Ethan"`），仅当 `modalities` 包含 `"audio"` 时生效 | 全协议一致 |
| `input_audio_format` / `output_audio_format` | 当前**仅支持 `"pcm"`**；输入为 16 kHz PCM，输出为 24 kHz PCM | 全协议一致，见 [接入模型与应用](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-quick-start-guide/realtime-connect-model.md) |
| `turn_detection` | 语音活动检测（VAD）配置，推荐 `type: "semantic_vad"`（语义级 VAD）用于 `qwen3.5-omni-realtime` 系列 | AOQ/WebRTC 支持；WebSocket 部分模型需确认服务端兼容性 |
| `x-dashscope-rtc-transport` | HTTP 请求头字段，值为 `"moq"` 表示 AOQ 协议 | **仅 AOQ 鉴权请求中必需**，见 [Token鉴权](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-quick-start-guide/realtime-token-authentication.md) |

## 使用方式

### 1. 协议选型与 SDK 获取
- **AOQ**：面向 Android/iOS/HarmonyOS 原生 App，需集成 [AOQ SDK](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-quick-start-guide/realtime-sdk-download.md)，并**必须下载 Opus [插件](../concepts/plugin.md)**（如 `libPluginOpus.zip`）以启用音频编解码。  
- **WebRTC**：无专用 SDK，Web 端直接使用浏览器原生 API；其他端可基于标准 WebRTC 库实现。需注意当前为白名单开放，需联系商务获取 Endpoint。  
- **WebSocket**：接入门槛最低，推荐服务端集成或原型验证，SDK 参见 [安装SDK](https://help.aliyun.com/zh/model-studio/install-sdk)。

### 2. 鉴权流程
所有协议均使用 `Authorization: Bearer <API_KEY>` 完成建连阶段鉴权：
- **AOQ**：采用服务端代理模式——AppServer 携带 API Key 调用百炼 Allocate 接口获取 `aoqTokenForClient`、`sid`、`relayEndpoints` 等凭证，再下发给客户端 SDK 使用。  
- **WebRTC/WebSocket**：客户端或服务端直连时，在 SDP 交换（WebRTC）或 WebSocket 握手（WebSocket）请求头中携带 API Key。

### 3. 连接与媒体控制（以 AOQ 为例）
- 创建引擎后，**必须先调用 `enableSendMediaStream(.audio, false)` 禁用发送**，避免在服务端未就绪时推送数据。  
- 连接成功后发送 `session.update` 配置会话；收到服务端 `session.updated` 事件后，再调用 `enableSendMediaStream(.audio, true)` 开启媒体流 [媒体流发送管理](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-function/aoq-media-stream-control.md)。  
- 音频/视频采集、播放、编码等高级功能（如自定义采集、外部音频流、视频帧回调）详见 [音频常用功能介绍](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-function/aoq-audio-features.md) 与 [视频常用功能介绍](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-function/aoq-video-features.md)。

## 限制和注意事项

- **协议限制**：AOQ 不支持浏览器，WebRTC 不支持移动端原生 App（需 WebView 或第三方库桥接），WebSocket 无弱网对抗能力且无内置 AEC/降噪。  
- **模型限制**：`qwen3.5-omni-*` 系列模型要求 `turn_detection.type` 设为 `"semantic_vad"` 才能获得最佳响应效果；`Fun-ASR`/`CosyVoice` 等单模态模型**仅 WebSocket 可用**。  
- **安全限制**：API Key **严禁硬编码于客户端**，尤其 AOQ 客户端应只使用服务端下发的临时 `aoqTokenForClient`。  
- **状态管理**：AOQ SDK 连接状态机为 `Connecting → Connected/Failed → Disconnected`，其中 `Failed` 是瞬态，SDK 自动迁移至 `Disconnected`，业务层无需手动 `disconnect` [连接状态管理](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-function/aoq-connection-management.md)。  
- **自定义流注意事项**：使用外部音频/视频流时，需严格按文档要求设置 `isExternal=true`、管理 `streamId` 生命周期，并处理缓冲区满（错误码 110）等异常；原始帧推送需确保 `timeStamp` 准确，否则影响同步效果。

## 来源文档

- [Realtime API 概述](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-overview.md)
- [SDK下载](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-quick-start-guide/realtime-sdk-download.md)
- [接入模型与应用](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-quick-start-guide/realtime-connect-model.md)
- [Token鉴权](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-quick-start-guide/realtime-token-authentication.md)
- [AOQ SDK简介](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-desc.md)
- [连接状态管理](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-function/aoq-connection-management.md)
- [媒体流发送管理](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-function/aoq-media-stream-control.md)
- [音频常用功能介绍](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-function/aoq-audio-features.md)
- [自定义音频播放](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-function/aoq-custom-audio-playback.md)
- [视频常用功能介绍](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-function/aoq-video-features.md)
- [自定义音频采集](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-function/aoq-custom-audio-capture.md)
- [自定义视频输入](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-function/aoq-custom-video-input.md)



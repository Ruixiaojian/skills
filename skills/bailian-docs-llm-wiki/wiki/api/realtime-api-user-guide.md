# realtime api user guide

Realtime API 是百炼平台提供的低延迟、高可靠实时多模态交互能力，支持 AOQ、WebRTC 和 WebSocket 三种传输协议，适用于语音对话、实时翻译、音视频增强等 AI 实时场景。开发者可根据终端类型、网络环境和业务需求选择最适配的协议，并通过统一的模型接口与服务交互。

## 支持的模型/功能

Realtime API 当前支持以下核心模型与应用类型，各协议兼容性存在差异：

- **实时全模态模型**：`qwen3.5-omni-plus-realtime`、`qwen3.5-omni-flash-realtime`、`qwen3.5-livetranslate-flash-realtime` —— 全协议支持（AOQ/WebRTC/WebSocket）  
- **多模态开发套件**：`multimodal-dialog` —— 全协议支持  
- **实时语音识别（ASR）**：`Qwen-Audio-3.0-ASR-Flash-Streaming`、`Fun-ASR-Realtime系列` —— **AOQ 和 WebSocket 支持，WebRTC 不支持**（见[Realtime API 概述](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-overview.md)）  
- **实时语音合成（TTS）**：`CosyVoice系列` —— **AOQ 和 WebSocket 支持，WebRTC 不支持**  
- **实时语音对话模型**：`qwen-audio-3.0-realtime-plus`、`qwen-audio-3.0-realtime-flash` —— AOQ 与 WebRTC 支持，WebSocket 仅支持基础文本流  

> **注意**：文档 1 明确指出 WebRTC 不支持 ASR/TTS 模型，但文档 4 的 WebRTC 接入示例中未强调此限制，实际接入时请以文档 1 的兼容性表格为准，避免因协议误选导致功能不可用。

## 关键参数

建连与会话控制依赖以下关键参数，需在请求或 SDK 配置中正确设置：

- **`Authorization: Bearer <API_KEY>`**：所有协议均在建连阶段通过 HTTP Header 鉴权，API Key 必须由服务端安全下发，**严禁硬编码于客户端**（见[Token鉴权](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-quick-start-guide/realtime-token-authentication.md)）  
- **`x-dashscope-rtc-transport: moq`**：AOQ 协议必需的 Header，用于显式指定传输协议  
- **`clientIp`（可选）**：AOQ 建连请求体中传入客户端真实公网 IP，用于 Relay 接入点智能调度；不填则默认使用网关出口 IP  
- **`modalities`、`voice`、`input_audio_format`、`output_audio_format`、`instructions`、`turn_detection`**：`session.update` 事件中的核心会话配置字段，决定输出模态、音色、音频格式、系统角色及语音活动检测策略（见[接入模型与应用](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-quick-start-guide/realtime-connect-model.md)）  
- **`aoqTokenForClient`、`sid`、`clientRelayCertFingerprint`、`clientRelayEndpoints`**：AOQ 网关分配的连接凭证，必须完整传入 SDK `AoqConnectConfig`（见[Token鉴权](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-quick-start-guide/realtime-token-authentication.md)）

## 使用方式

### 协议选型与接入路径
- **AOQ**：面向 Android/iOS/HarmonyOS 原生应用，需集成 [AOQ SDK](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-quick-start-guide/realtime-sdk-download.md)，流程为：AppServer 代鉴权 → 获取连接凭证 → SDK `connect()` → 收到 `session.updated` 后调用 `enableSendMediaStream()` 开启媒体流  
- **WebRTC**：面向浏览器或具备 WebRTC 栈的客户端，无专用 SDK，直接使用原生 `RTCPeerConnection` API 完成 SDP 交换与 ICE 连接（白名单开放，需联系商务获取 Endpoint）  
- **WebSocket**：面向服务端或快速原型验证，通过 DashScope SDK 或标准 WebSocket 客户端接入，接入门槛最低  

### 关键 SDK 控制逻辑（AOQ）
- **连接状态管理**：SDK 提供明确的状态机（`Connecting` → `Connected` → `Disconnected`），业务需监听 `onConnectionStatusChange` 回调处理状态迁移（见[连接状态管理](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-function/aoq-connection-management.md)）  
- **媒体流精确控制**：必须在收到服务端 `session.updated` 事件后，再调用 `enableSendMediaStream(.audio, true)` 启动音频发送，否则服务端可能拒绝接收数据（见[媒体流发送管理](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-function/aoq-media-stream-control.md)）  
- **自定义音视频处理**：支持外部音频采集/播放、外部视频帧输入（原始帧或 JPEG 编码帧），适用于 TTS 输出推流、AI 生成画面传输等高级场景（见[自定义音频采集](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-function/aoq-custom-audio-capture.md)、[自定义视频输入](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-function/aoq-custom-video-input.md)）

## 限制和注意事项

- **协议能力边界**：AOQ 具备最强弱网对抗与多模态原生支持；WebRTC 依赖浏览器兼容性且不支持 ASR/TTS；WebSocket 仅支持文本/音频/图像基础传输，无内置回声消除，需客户端自行处理（见[Realtime API 概述](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-overview.md)）  
- **AOQ Opus 依赖**：Android/iOS/HarmonyOS SDK 均需单独下载并集成 Opus 插件（`libPluginOpus.zip` 或 `PluginOpus.framework.zip`），否则音频编解码将失败（见[SDK下载](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-quick-start-guide/realtime-sdk-download.md)）  
- **模型就绪时机**：所有协议均要求在服务端返回 `session.updated`（或等效确认事件）后，才开始发送音视频媒体流；AOQ SDK 默认建连即发流，**必须主动调用 `enableSendMediaStream(false)` 暂停，待事件触发后再启用**  
- **资源释放规范**：调用 `disconnect()` 后引擎仍存活，可重连；彻底释放需调用 `destroy()`；自定义音视频流推送必须在 `destroy()` 前停止循环并移除流，否则可能 crash（见[自定义音频采集](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-function/aoq-custom-audio-capture.md)、[自定义音频播放](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-function/aoq-custom-audio-playback.md)）  
- **安全红线**：API Key 绝对不可出现在客户端代码或公开仓库中，必须通过服务端代理鉴权或环境变量注入（见[Token鉴权](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-quick-start-guide/realtime-token-authentication.md)）

## 来源文档

- [Realtime API 概述](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-overview.md)
- [SDK下载](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-quick-start-guide/realtime-sdk-download.md)
- [Token鉴权](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-quick-start-guide/realtime-token-authentication.md)
- [接入模型与应用](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-quick-start-guide/realtime-connect-model.md)
- [连接状态管理](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-function/aoq-connection-management.md)
- [媒体流发送管理](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-function/aoq-media-stream-control.md)
- [自定义音频播放](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-function/aoq-custom-audio-playback.md)
- [音频常用功能介绍](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-function/aoq-audio-features.md)
- [自定义音频采集](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-function/aoq-custom-audio-capture.md)
- [视频常用功能介绍](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-function/aoq-video-features.md)
- [自定义视频输入](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-function/aoq-custom-video-input.md)
- [AOQ SDK简介](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-desc.md)



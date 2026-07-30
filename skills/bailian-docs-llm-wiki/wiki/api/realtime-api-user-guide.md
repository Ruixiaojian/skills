# realtime api user guide

Realtime API 是百炼平台面向实时[多模态](../concepts/multi-modal.md)交互场景提供的低延迟、高可靠通信能力，支持 AOQ、WebRTC 和 WebSocket 三种传输协议，覆盖移动端原生应用、浏览器端互动及服务端快速集成等不同需求。开发者需根据业务场景（如弱网对抗要求、平台兼容性、接入复杂度）选择合适协议，并严格遵循连接状态管理、媒体流控制和鉴权流程。

## 支持的模型/功能

Realtime API 当前支持以下模型与应用类型，不同协议的支持能力存在差异：

- **实时全模态模型**（如 `qwen3.5-omni-plus-realtime`、`qwen3.5-omni-flash-realtime`、`qwen3.5-livetranslate-flash-realtime`）：全部支持 AOQ、WebRTC 和 WebSocket 协议 [Realtime API 概述](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-overview.md)。
- **[多模态](../concepts/multi-modal.md)开发套件**（`multimodal-dialog`）：仅支持 WebRTC 和 WebSocket，**不支持 AOQ**。
- **实时语音识别**（Fun-ASR 系列）、**实时语音合成**（CosyVoice 系列）、**实时语音对话**（`qwen-audio-3.0-realtime-plus` 等）：**仅支持 WebSocket**，AOQ 与 WebRTC 均不支持。

> **注意**：文档 1 明确指出 AOQ 不支持 Fun-ASR/CosyVoice/qwen-audio-3.0 等语音专项模型，但部分 SDK 示例代码（如文档 3 中的 `session.update` 示例）未限定模型适用范围，易引发误用。实际接入时请以 [Realtime API 概述](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-overview.md) 的协议支持矩阵为准。

## 关键参数

### 连接凭证参数（AOQ/WebRTC 共用）
- `token`（AOQ）或 `API_KEY`（WebRTC/WS）：用于建连鉴权，**AOQ 必须使用网关返回的临时 `aoqTokenForClient`，而非原始 API Key**；WebRTC 和 WebSocket 可直接在 HTTP Header 中携带 `Authorization: Bearer <API_KEY>` [Token鉴权](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-quick-start-guide/realtime-token-authentication.md)。
- `sid`：会话唯一标识，由网关分配。
- `certFingerprint`（AOQ）：Relay TLS 证书指纹，用于安全校验。
- `relayEndpoints`（AOQ）：客户端应连接的 Relay 接入点列表。
- `workspaceIdHash`（AOQ）：工作区 ID 哈希，用于路由。

### 会话配置参数（`session.update` 事件）
- `modalities`：输出模态数组，如 `["text", "audio"]` 或 `["text"]`。
- `voice`：TTS 音色名称（如 `"Ethan"`）。
- `input_audio_format` / `output_audio_format`：当前仅支持 `"pcm"`，采样率分别为 16 kHz（输入）和 24 kHz（输出）。
- `instructions`：系统角色提示词。
- `turn_detection`：语音活动检测配置，推荐 `semantic_vad` 类型（适用于 `qwen3.5-omni-realtime` 系列），含 `threshold` 和 `silence_duration_ms`。

## 使用方式

### 协议选型与接入路径
- **AOQ**：适用于移动端原生应用（Android/iOS/HarmonyOS），需集成 [AOQ SDK](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-desc.md)，具备极致弱网对抗与内置 3A（回声消除/降噪/自动增益）。接入流程为：创建引擎 → 设置回调 → 获取网关凭证 → `connect` → 监听 `session.updated` → 启用媒体流。
- **WebRTC**：适用于浏览器端或已有 WebRTC 基础设施的场景，无需专用 SDK，直接调用浏览器原生 API 或 `aiortc` 等库完成 SDP 交换与 ICE 连接。
- **WebSocket**：适用于服务端集成或快速原型验证，接入门槛最低，通过 DashScope SDK 即可实现。

### 核心控制逻辑（AOQ）
- **连接状态管理**：SDK 提供明确的状态机（`Connecting` → `Connected` → `Failed` → `Disconnected`），业务层需监听 `onConnectionStatusChange` 回调处理状态迁移 [连接状态管理](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/aoq-connection-management.md)。
- **媒体流发送控制**：必须在收到 `session.updated` 服务端事件后，再调用 `enableSendMediaStream(.audio, true)` 启用音频发送；视频同理。此机制确保服务端已就绪，避免数据丢失 [媒体流发送管理](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/aoq-media-stream-control.md)。
- **自定义音视频能力**：
  - **自定义音频采集**：通过 `isExternal=true` 关闭内部麦克风，调用 `addAudioExternalStream` 注册外部流，再循环 `pushAudioExternalStreamData` 推送 PCM 数据（建议 10ms/帧）[自定义音频采集](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/aoq-custom-audio-capture.md)。
  - **自定义视频输入**：支持原始帧（I420/NV12/BGRA）或编码帧（JPEG）两种模式，需设置 `isExternal=true` 并调用对应 `pushExternalVideo...Frame` 接口 [自定义视频输入](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/aoq-custom-video-input.md)。
  - **自定义音频播放**：设置 `isExternal=true` 后，通过 `setAudioFrameObserver` + `enableAudioFrameObserver` 获取解码后的 PCM 数据，交由应用层（如 Android `AudioTrack`）渲染 [自定义音频播放](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/aoq-custom-audio-playback.md)。

## 限制和注意事项

- **协议兼容性限制**：AOQ 不支持浏览器环境；WebRTC 在非浏览器端需依赖第三方 WebRTC 库；WebSocket 无平台限制但缺乏弱网优化与内置 3A。
- **模型协议绑定**：`multimodal-dialog`、Fun-ASR、CosyVoice 等模型**不支持 AOQ**，强行接入将失败；`qwen3.5-omni-*` 系列虽三协议均支持，但 AOQ 才能发挥其[多模态](../concepts/multi-modal.md)与弱网优势。
- **AOQ SDK 集成要求**：必须下载并集成 Opus 编解码插件（`libPluginOpus`），否则无法启用 Opus 编码 [SDK下载](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-quick-start-guide/realtime-sdk-download.md)。
- **安全规范**：API Key **严禁硬编码于客户端**，AOQ 必须通过服务端代理鉴权获取临时 [Token](../concepts/token.md)；WebRTC/WS 若由客户端直连，也应通过后端下发 [Token](../concepts/token.md) 或短期有效 Key。
- **资源管理**：调用 `destroy()` 前，必须停止所有外部流推送循环（如 `mPushRunning = false`）并移除流（`removeAudioExternalStream`/`stopVideoCapture`），否则可能触发内存访问异常。

## 来源文档

- [Realtime API 概述](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-overview.md)
- [AOQ SDK简介](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-desc.md)
- [接入模型与应用](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-quick-start-guide/realtime-connect-model.md)
- [SDK下载](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-quick-start-guide/realtime-sdk-download.md)
- [Token鉴权](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-quick-start-guide/realtime-token-authentication.md)
- [连接状态管理](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-function/aoq-connection-management.md)
- [媒体流发送管理](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-function/aoq-media-stream-control.md)
- [音频常用功能介绍](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-function/aoq-audio-features.md)
- [自定义音频采集](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-function/aoq-custom-audio-capture.md)
- [视频常用功能介绍](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-function/aoq-video-features.md)
- [自定义视频输入](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-function/aoq-custom-video-input.md)
- [自定义音频播放](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-function/aoq-custom-audio-playback.md)



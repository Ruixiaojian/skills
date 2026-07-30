# realtime api user guide

Realtime API 是百炼平台提供的低延迟、高可靠[实时交互](../concepts/realtime-interaction.md)能力接口，支持 AOQ、WebRTC 和 WebSocket 三种传输协议，面向多模态 AI 实时对话、语音识别/合成、实时翻译等场景。开发者可根据终端类型、网络环境、功能需求和接入成本灵活选型，并通过统一的模型调用语义与服务端交互。

## 支持的模型/功能

Realtime API 当前支持以下核心模型与应用类型，不同协议的支持能力存在差异：

- **实时全模态模型**（如 `qwen3.5-omni-plus-realtime`、`qwen3.5-omni-flash-realtime`）：AOQ 与 WebRTC 全面支持，WebSocket 仅支持基础文本/音频交互；[原文标题](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-overview.md) 明确指出三者均支持该类模型，但实际能力边界需结合协议特性理解。
- **多模态开发套件**（`multimodal-dialog`）：仅 WebRTC 和 WebSocket 支持，AOQ **不支持**；该限制在 [原文标题](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-overview.md) 的表格中已明确标注。
- **实时语音识别**（Fun-ASR 系列）、**实时语音合成**（CosyVoice 系列）、**实时语音对话**（`qwen-audio-3.0-realtime-plus` 等）：**仅 WebSocket 协议支持**；AOQ 和 WebRTC 均未列出对应支持项，开发者若需 ASR/TTS 能力应优先选用 WebSocket 接入。

> **注意**：文档 1 中称 `qwen3.5-livetranslate-flash-realtime` “支持”于所有三种协议，但文档 5 的“前提条件”链接指向同一文档，且未提供该模型在 AOQ/WebRTC 下的具体能力说明。实践中建议以 [原文标题](../../raw/model-api-reference/realtime-api-user-guide/realtime-connect-model.md) 中的接入流程为准，并通过控制台确认模型当前可用协议。

## 关键参数

建连与会话配置涉及两类关键参数：

### 鉴权参数
- `Authorization: Bearer <API_KEY>`：所有协议均在建连阶段通过 HTTP Header 传递，**API Key 必须由服务端持有并用于请求网关**；客户端不得硬编码或暴露该密钥。AOQ 协议采用服务端代理鉴权模式，客户端使用网关返回的 `aoqTokenForClient` 连接，此设计显著提升安全性 [原文标题](../../raw/model-api-reference/realtime-api-user-guide/realtime-token-authentication.md)。

### 会话配置参数（`session.update`）
- `modalities`: 指定输出模态，如 `["text", "audio"]` 或 `["text"]`。
- `voice`: 输出音色名称（如 `"Ethan"`），仅当 `modalities` 包含 `"audio"` 时生效。
- `input_audio_format` / `output_audio_format`: 当前仅支持 `"pcm"`，采样率分别为 16kHz（输入）和 24kHz（输出）。
- `turn_detection`: 语音活动检测（VAD）配置，推荐对 `qwen3.5-omni-realtime` 系列模型使用 `"type": "semantic_vad"`。

## 使用方式

### 协议选型与接入路径
- **AOQ**：适用于移动端原生应用（Android/iOS/HarmonyOS），需集成 [AOQ SDK](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-sdk-desc.md)，具备极致弱网对抗与内置 AEC/降噪能力。典型流程为：服务端申请 `aoqTokenForClient` → 客户端调用 `connect()` → 收到 `session.updated` 后启用媒体流。
- **WebRTC**：适用于浏览器端或已有 WebRTC 基础设施的场景，无需专用 SDK，直接使用浏览器原生 API 或标准 WebRTC 库。需注意当前为白名单开放，Endpoint 需联系商务获取。
- **WebSocket**：适用于服务端集成、快速原型验证或跨平台轻量接入，支持 DashScope SDK 快速对接，但无内置音视频处理能力，需客户端自行实现回声消除与降噪。

### 核心操作流程（以 AOQ 为例）
1. **初始化引擎**：调用 `createEngine()` 并设置 `AoqEngineDelegate` 回调。
2. **启动采集与播放**：`startAudioCapture()` / `startAudioPlayer()`，可配置 `isExternal=true` 启用自定义采集/播放 [原文标题](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-function/aoq-custom-audio-capture.md)。
3. **建连与状态管理**：调用 `connect(config)`，监听 `onConnectionStatusChange` 处理 `connecting`/`connected`/`failed`/`disconnected` 状态迁移 [原文标题](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/aoq-connection-management.md)。
4. **媒体流控制**：连接后默认发送媒体流，**必须等待收到 `session.updated` 事件后再调用 `enableSendMediaStream(.audio, true)` 开启发送**，否则服务端可能拒绝数据 [原文标题](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-function/aoq-media-stream-control.md)。
5. **自定义扩展**：支持外部音频流注入（TTS/文件）、外部视频帧输入（屏幕共享/AI生成画面）、音视频帧回调（分析/录制）等高级能力，详见各功能文档。

## 限制和注意事项

- **协议兼容性限制**：AOQ 不支持 `multimodal-dialog` 套件及 Fun-ASR/CosyVoice 等单模态模型；WebRTC 不支持 `qwen-audio-3.0-realtime` 系列；WebSocket 不具备弱网对抗与内置音视频处理能力。
- **SDK 依赖**：AOQ 必须使用官方 SDK（v1.0.1 及以上），且需额外下载 Opus 编解码插件 [原文标题](../../raw/model-api-reference/realtime-api-user-guide/realtime-sdk-download.md)；WebRTC 和 WebSocket 可基于标准协议自行实现。
- **安全要求**：API Key 绝对禁止出现在客户端代码或公开仓库中，必须通过服务端下发临时 [Token](../concepts/token.md)（AOQ）或由服务端代为建连（WebRTC/WebSocket）。
- **媒体流时序**：AOQ 下 `enableSendMediaStream` 的调用时机至关重要——**必须在 `session.updated` 后开启**，否则连接虽成功但媒体数据会被丢弃。
- **资源管理**：自定义音频/视频流推送需严格管理生命周期，推送循环必须在 `destroy()` 或 `removeAudioExternalStream()` 前停止，避免访问已释放内存。

## 来源文档

- [Realtime API 概述](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-overview.md)
- [AOQ SDK简介](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-desc.md)
- [SDK下载](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-quick-start-guide/realtime-sdk-download.md)
- [Token鉴权](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-quick-start-guide/realtime-token-authentication.md)
- [接入模型与应用](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-quick-start-guide/realtime-connect-model.md)
- [连接状态管理](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-function/aoq-connection-management.md)
- [媒体流发送管理](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-function/aoq-media-stream-control.md)
- [自定义音频播放](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-function/aoq-custom-audio-playback.md)
- [音频常用功能介绍](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-function/aoq-audio-features.md)
- [视频常用功能介绍](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-function/aoq-video-features.md)
- [自定义音频采集](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-function/aoq-custom-audio-capture.md)
- [自定义视频输入](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-function/aoq-custom-video-input.md)



# realtime api user guide

Realtime API 是百炼平台提供的低延迟、高可靠实时交互能力接口，支持 AOQ、WebRTC 和 WebSocket 三种传输协议，面向[多模态](../concepts/multi-modal.md) AI 场景深度优化。开发者可根据终端类型、网络环境、接入成本和功能需求选择最适配的协议方案，并通过统一鉴权机制与模型/应用建立安全连接。

## 支持的模型/功能

Realtime API 当前支持以下核心模型与应用类型，不同协议的支持范围存在差异：

- **实时全模态模型**：`qwen3.5-omni-plus-realtime`、`qwen3.5-omni-flash-realtime`、`qwen3.5-livetranslate-flash-realtime` —— 全协议（AOQ/WebRTC/WebSocket）均支持。
- **[多模态](../concepts/multi-modal.md)开发套件**：`multimodal-dialog` —— 仅 WebRTC 和 WebSocket 支持，**AOQ 不支持**（见 [Realtime API 概述](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-overview.md)）。
- **实时语音识别**：Fun-ASR 系列模型 —— 仅 WebSocket 支持。
- **实时语音合成**：CosyVoice 系列模型 —— 仅 WebSocket 支持。
- **实时语音对话**：`qwen-audio-3.0-realtime-plus`、`qwen-audio-3.0-realtime-flash` —— 仅 WebSocket 支持。

> **注意**：文档 1 明确指出 AOQ 不支持 `multimodal-dialog`、Fun-ASR、CosyVoice 及 `qwen-audio-*` 系列模型，但文档 5 的“AOQ 接入”章节示例中未明确排除这些模型，且未说明其不可用。实际开发中请以文档 1 的兼容性表格为准，避免误用不支持的模型。

## 关键参数

### 鉴权参数
所有协议均在建连阶段通过 HTTP Header `Authorization: Bearer <API_KEY>` 完成鉴权：
- `API_KEY` 须通过[百炼控制台 → API Key](https://help.aliyun.com/zh/model-studio/get-api-key) 创建并安全保管；
- **严禁硬编码于客户端**，推荐服务端代理下发或通过环境变量管理；
- AOQ 协议采用服务端代理鉴权模式，客户端使用网关返回的 `aoqTokenForClient`，而非原始 API Key（见 [Token鉴权](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-quick-start-guide/realtime-token-authentication.md)）。

### 连接与会话参数
- `model`：必需查询参数，指定目标模型名（如 `qwen3.5-omni-plus-realtime`），不同模型对应不同 endpoint。
- `sid` 与 `aoqTokenForClient`：AOQ 建连必需字段，由服务端 allocate 接口返回。
- `session.update` 事件中的关键字段：
  - `modalities`: 指定输出模态，如 `["text", "audio"]`；
  - `voice`: 输出音色（如 `"Ethan"`）；
  - `input_audio_format` / `output_audio_format`: 当前仅支持 `"pcm"`；
  - `turn_detection.type`: 推荐 `"semantic_vad"`（语义级 VAD），适用于 `qwen3.5-omni-realtime` 系列模型。

## 使用方式

### 协议选型与接入路径
| 协议 | 适用场景 | 客户端要求 | SDK/依赖 |
|------|----------|------------|-----------|
| **AOQ** | 移动端原生 App、极致弱网对抗、[多模态](../concepts/multi-modal.md)混合传输 | Android/iOS/HarmonyOS | 必需 [AOQ SDK](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-quick-start-guide/realtime-sdk-download.md)（含 Opus 插件） |
| **WebRTC** | 浏览器端互动、已有 WebRTC 基础设施 | 浏览器原生支持 | 无专用 SDK，直接使用 `RTCPeerConnection` |
| **WebSocket** | 服务端集成、快速原型验证、低门槛接入 | 任意支持 WebSocket 环境 | 可通过 DashScope SDK 快速实现 |

### 核心流程（以 AOQ 为例）
1. **服务端获取凭证**：AppServer 调用百炼 allocate 接口（带 `x-dashscope-rtc-transport: moq`），传入 `clientIp` 获取 `sid`、`aoqTokenForClient` 等；
2. **客户端初始化引擎**：调用 `AoqClientEngine.createEngine()` 并设置 `AoqEngineDelegate`；
3. **预配置媒体**：启动音频/视频采集与播放（可选），设置编解码参数（如 `setAudioEncoderConfig`）；
4. **连接前禁用发送**：调用 `enableSendMediaStream(.audio, false)` 等，避免模型未就绪即推送数据；
5. **建立连接**：传入 `aoqTokenForClient`、`sid` 等构建 `AoqConnectConfig`，调用 `engine.connect(config)`；
6. **等待会话就绪**：监听 `onDataMsg` 回调，收到 `type == "session.updated"` 后，调用 `enableSendMediaStream(.audio, true)` 开启媒体流；
7. **断开连接**：调用 `engine.disconnect()`，必要时销毁引擎。

> **注意**：文档 5 明确强调“必须在收到 `session.updated` 后才开启媒体流发送”，否则服务端可能拒绝接收数据；而文档 7 的“注意事项”也确认此行为为模型强制要求，建议统一采用“先禁用、后开启”模式。

### 自定义媒体流（高级能力）
- **自定义音频采集**：设置 `isExternal=true` 关闭内部麦克风，通过 `addAudioExternalStream()` 添加外部流，再循环调用 `pushAudioExternalStreamData()` 推送 PCM 数据（见 [自定义音频采集](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-function/aoq-custom-audio-capture.md)）；
- **自定义视频输入**：支持两种模式：
  - *原始帧模式*：`startVideoCapture(isExternal=true)` + `pushExternalVideoCapturedFrame()`（支持 I420/NV12/BGRA 等格式）；
  - *编码帧模式*：`setVideoEncoderConfig(isExternal=true)` + `pushExternalVideoEncodedFrame()`（当前仅 JPEG）。

## 限制和注意事项

- **协议限制**：
  - AOQ 不支持浏览器，仅限原生移动端（Android/iOS/HarmonyOS）；
  - WebRTC 功能当前为白名单开放，需联系商务经理获取 Endpoint（见 [Token鉴权](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-quick-start-guide/realtime-token-authentication.md)）；
  - WebSocket 无内置回声消除/降噪，需客户端自行处理（见 [Realtime API 概述](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-overview.md)）。

- **连接与状态**：
  - AOQ 连接状态机为 `Connecting` → `Connected`/`Failed` → `Disconnected`，`Failed` 为瞬态，SDK 自动迁移至 `Disconnected`，业务层无需手动调用 `disconnect`（见 [连接状态管理](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/aoq-connection-management.md)）；
  - `connect()` 调用后立即进入 `Connecting` 状态并触发回调，返回值 `0` 仅表示异步调用成功，不表示连接已建立。

- **媒体流控制**：
  - `enableSendMediaStream()` 默认行为是 connect 成功后立即发送，若模型要求延迟发送，必须显式调用该 API 控制（见 [媒体流发送管理](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-function/aoq-media-stream-control.md)）；
  - 外部音频/视频流推送时，遇缓冲区满（错误码 `110`）需主动 sleep 后重试，不可丢弃数据（见 [自定义音频采集](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-function/aoq-custom-audio-capture.md) 和 [自定义视频输入](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-function/aoq-custom-video-input.md)）。

- **安全与合规**：
  - API Key 绝对不可暴露于客户端代码或公开仓库；
  - 客户端真实 IP（`clientIp`）建议由 AppServer 获取后填入 allocate 请求，以获得最优 Relay 接入点。

## 来源文档

- [Realtime API 概述](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-overview.md)
- [Token鉴权](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-quick-start-guide/realtime-token-authentication.md)
- [SDK下载](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-quick-start-guide/realtime-sdk-download.md)
- [AOQ SDK简介](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-desc.md)
- [接入模型与应用](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-quick-start-guide/realtime-connect-model.md)
- [连接状态管理](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-function/aoq-connection-management.md)
- [媒体流发送管理](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-function/aoq-media-stream-control.md)
- [音频常用功能介绍](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-function/aoq-audio-features.md)
- [自定义音频播放](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-function/aoq-custom-audio-playback.md)
- [自定义音频采集](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-function/aoq-custom-audio-capture.md)
- [视频常用功能介绍](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-function/aoq-video-features.md)
- [自定义视频输入](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-function/aoq-custom-video-input.md)



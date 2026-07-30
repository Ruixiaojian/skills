# realtime api user guide

Realtime API 是百炼平台提供的低延迟、高可靠实时交互能力，支持 AOQ、WebRTC 和 WebSocket 三种传输协议，面向[多模态](../concepts/multi-modal.md) AI 实时对话、语音识别/合成、实时翻译等场景。开发者可根据终端类型、网络环境、功能需求和接入成本灵活选择协议，并通过统一的模型调用接口与服务交互。

## 支持的模型/功能

Realtime API 当前支持以下模型与应用类型，不同协议的支持能力存在差异：

- **实时全模态模型**（如 `qwen3.5-omni-plus-realtime`、`qwen3.5-omni-flash-realtime`、`qwen3.5-livetranslate-flash-realtime`）：  
  全协议支持（AOQ/WebRTC/WebSocket），适用于端到端音视频+文本联合推理场景。

- **[多模态](../concepts/multi-modal.md)开发套件**（`multimodal-dialog`）：  
  仅 WebRTC 和 WebSocket 支持，不支持 AOQ —— [原文标题](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-overview.md) 明确指出 AOQ 对该套件“不支持”。

- **实时语音识别**（Fun-ASR 系列）、**实时语音合成**（CosyVoice 系列）、**实时语音对话**（`qwen-audio-3.0-realtime-plus` 等）：  
  仅 WebSocket 协议支持，AOQ 与 WebRTC 均不支持 —— 此信息在 [原文标题](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-overview.md) 的表格中一致，无矛盾。

> **注意**：文档 4 中提到“WebRTC 功能目前为白名单开放，请联系商务经理获取 Endpoint”，而文档 1 未提及此限制。实际接入前务必确认 WebRTC 接入权限，避免因白名单缺失导致建连失败。

## 关键参数

| 参数 | 协议适用性 | 说明 |
|------|------------|------|
| `Authorization: Bearer <API_KEY>` | 所有协议 | 仅用于建连阶段鉴权，**严禁硬编码于客户端**；AOQ 场景下 API Key 仅由 AppServer 使用，客户端使用网关返回的 `aoqTokenForClient` —— [原文标题](../../raw/model-api-reference/realtime-api-user-guide/realtime-token-authentication.md) |
| `x-dashscope-rtc-transport: moq` | AOQ | 必须携带，标识使用 AOQ 协议 |
| `clientIp`（请求体） | AOQ | 选填，用于 Relay 节点最优调度；建议由 AppServer 获取客户端真实公网 IP 后传入 |
| `sid` / `aoqTokenForClient` / `clientRelayCertFingerprint` / `clientRelayEndpoints` | AOQ | 均来自网关 Allocate 接口响应，需完整传递至 AOQ SDK 的 `AoqConnectConfig` |
| `session.update` 事件中的 `turn_detection.type` | AOQ/WebRTC | 使用 `qwen3.5-omni-realtime` 系列模型时推荐设为 `semantic_vad`（语义级 VAD），而非 `server_vad` —— [原文标题](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-quick-start-guide/realtime-connect-model.md) |

## 使用方式

### 协议选型建议
- **移动端原生应用（Android/iOS/HarmonyOS）**：优先选用 **AOQ**，具备极致弱网对抗、内置回声消除/降噪、低建连延迟，且支持音视频+数据混合传输。
- **浏览器端互动**：选用 **WebRTC**，复用现有基础设施，但需申请白名单并自行管理 SDP 协商。
- **服务端集成或快速验证**：选用 **WebSocket**，接入门槛最低，支持 DashScope SDK 快速启动。

### AOQ 接入关键步骤（以移动端为例）
1. **下载 SDK**：从 [原文标题](../../raw/model-api-reference/realtime-api-user-guide/realtime-sdk-download.md) 获取对应平台的 `AoqClientSdk` 及 Opus 插件（必需）。
2. **创建引擎并注册回调**：实现 `AoqEngineDelegate`，监听 `onConnectionStatusChange` 和 `onDataMsg`。
3. **获取连接凭证**：AppServer 调用百炼 Allocate 接口（带 `Authorization` 和 `x-dashscope-rtc-transport: moq`），解析返回的 `sid`、`aoqTokenForClient` 等字段。
4. **控制媒体流时机**：`connect` 前调用 `enableSendMediaStream(.audio, false)` 暂停发送；收到服务端 `session.updated` 事件后，再调用 `enableSendMediaStream(.audio, true)` 开启 —— [原文标题](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/aoq-media-stream-control.md) 强调此流程为模型就绪前提。
5. **配置音频/视频**：按需设置采集、播放、编解码参数（如 `setAudioEncoderConfig`、`startVideoCapture`），详见 [原文标题](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/aoq-audio-features.md) 和 [原文标题](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/aoq-video-features.md)。

### WebSocket/WebRTC 接入简述
- **WebSocket**：参考 DashScope SDK 文档安装 SDK，直接调用 `RealtimeClient` 初始化并连接；无需处理底层信令。
- **WebRTC**：无专用 SDK，依赖浏览器原生 `RTCPeerConnection`；需手动完成 Offer/Answer SDP 交换（携带 `Authorization` 头），并通过 DataChannel 接收服务端事件。

## 限制和注意事项

- **AOQ [Token](../concepts/token.md) 有效期**：`sidExpiresInSecs` 默认为 7200 秒（2 小时），超时需重新 Allocate 获取新凭证。
- **媒体流发送约束**：AOQ 协议下，**必须等待 `session.updated` 后再启用媒体发送**，否则服务端可能拒绝接收数据；此行为由模型侧强制要求，非 SDK Bug。
- **自定义采集/播放**：若需外部音频流（如 TTS 输出）或自定义视频源（如屏幕录制），需显式配置 `isExternal=true` 并调用 `addAudioExternalStream` 或 `pushExternalVideoCapturedFrame` —— 相关细节见 [原文标题](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/aoq-custom-audio-capture.md) 和 [原文标题](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/aoq-custom-video-input.md)。
- **连接状态管理**：AOQ SDK 状态机为 `Connecting → Connected/Failed → Disconnected`，`Failed` 为瞬态，SDK 自动迁移至 `Disconnected`，业务层无需在 `onConnectionStatusChange(.failed)` 中调用 `disconnect()` —— [原文标题](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/aoq-connection-management.md) 明确说明。
- **安全红线**：API Key 绝不可出现在客户端代码、前端 JS、移动 App 包内或 Git 仓库中；必须通过后端服务下发临时凭证（如 AOQ 的 `aoqTokenForClient`）。

## 来源文档

- [Realtime API 概述](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-overview.md)
- [SDK下载](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-quick-start-guide/realtime-sdk-download.md)
- [Token鉴权](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-quick-start-guide/realtime-token-authentication.md)
- [接入模型与应用](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-quick-start-guide/realtime-connect-model.md)
- [AOQ SDK简介](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-desc.md)
- [媒体流发送管理](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-function/aoq-media-stream-control.md)
- [音频常用功能介绍](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-function/aoq-audio-features.md)
- [自定义音频播放](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-function/aoq-custom-audio-playback.md)
- [自定义音频采集](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-function/aoq-custom-audio-capture.md)
- [视频常用功能介绍](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-function/aoq-video-features.md)
- [自定义视频输入](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-function/aoq-custom-video-input.md)
- [连接状态管理](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-function/aoq-connection-management.md)



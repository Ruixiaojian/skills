# realtime api user guide

Realtime API 是一套面向低延迟、多模态、弱网对抗的实时 AI 交互协议栈，提供 WebSocket、WebRTC 和 AOQ（AI over QUIC）三种传输方案，支持语音识别、语音合成、实时对话、多模态理解等场景。开发者可根据终端类型、网络环境、功能需求和集成复杂度选择最适配的接入方式。

## 支持的模型/功能

Realtime API 当前支持以下核心模型与应用类型，不同协议的支持能力存在差异：

| 模型/应用类型 | AOQ | WebRTC | WebSocket |
|---------------|-----|--------|-----------|
| 实时全模态对话（`qwen3.5-omni-plus-realtime`, `qwen3.5-omni-flash-realtime`） | ✅ | ✅ | ✅ |
| 实时语音翻译（`qwen3.5-livetranslate-flash-realtime`） | ✅ | ✅ | ✅ |
| 多模态交互套件（`multimodal-dialog`） | ❌ | ✅ | ✅ |
| 实时语音识别（Fun-ASR 系列） | ❌ | ❌ | ✅ |
| 实时语音合成（CosyVoice 系列） | ❌ | ❌ | ✅ |
| 实时语音对话（`qwen-audio-3.0-realtime-plus` 等） | ❌ | ❌ | ✅ |

> **注意**：文档 1 中表格明确标注 `multimodal-dialog` 在 AOQ 协议下“不支持”，但文档 6 的标题与正文均以“通过 WebRTC 使用多模态交互套件”为前提展开，未提及 AOQ 支持。因此该模型在 AOQ 下确实不可用，开发者应避免尝试 [Realtime API简介](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-overview.md)。

AOQ 与 WebRTC 均内置回声消除（AEC）和降噪能力，而 WebSocket 方案需客户端自行处理；AOQ 和 WebRTC 支持音视频+数据混合传输，WebSocket 仅支持文本/音频/图像分通道传输。

## 关键参数

### 鉴权参数
所有协议均使用 `Authorization: Bearer <API_KEY>` 进行建连鉴权：
- WebSocket/WebRTC：客户端或服务端直接携带 API Key 发起连接；
- AOQ：**必须**由业务 AppServer 代为请求百炼网关获取临时 `aoqTokenForClient`，客户端仅使用该 Token 连接，避免 API Key 泄露 [Token鉴权](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-quick-start-guide/realtime-token-authentication.md)。

### 协议特有参数
- **AOQ**：建连请求头需包含 `x-dashscope-rtc-transport: moq`；响应中关键字段包括 `sid`（会话 ID）、`aoqTokenForClient`（客户端令牌）、`clientRelayEndpoints`（中继地址）和 `clientRelayCertFingerprint`（证书指纹）。
- **WebRTC**：SDP 交换时需确保 Offer 中包含 `m=audio`（服务端强制要求），并创建名为 `oai-events` 的 DataChannel 用于事件通信；多模态套件接入需使用 `workspace_id.region.maas.aliyuncs.com` 格式 endpoint [通过WebRTC使用多模态交互套件实现实时通话](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-best-practices/best-practice-webrtc-multimodal-dialog.md)。
- **WebSocket**：无特殊协议头，但需严格遵循 JSON-RPC 2.0 格式发送 `input_audio_buffer.append` 等事件。

### 会话配置参数（`session.update`）
通用配置项（以 AOQ 示例为准）：
```json
{
  "type": "session.update",
  "session": {
    "modalities": ["text", "audio"],
    "voice": "Ethan",
    "input_audio_format": "pcm",
    "output_audio_format": "pcm",
    "instructions": "你是某五星级酒店的AI客服专员...",
    "turn_detection": {
      "type": "semantic_vad",
      "threshold": 0.5,
      "silence_duration_ms": 800
    }
  }
}
```
其中 `turn_detection.type` 在 `qwen3.5-omni-realtime` 模型下推荐设为 `semantic_vad`；`input_audio_format` 固定为 `pcm`（16 kHz 采样率），`output_audio_format` 固定为 `pcm`（24 kHz 采样率）。

## 使用方式

### 协议选型建议
- **WebSocket**：适合服务端集成、快速原型验证、对浏览器兼容性无要求的场景；接入成本最低，但弱网对抗能力差。
- **WebRTC**：适合浏览器端互动、已有 WebRTC 基础设施的项目；原生支持音视频，无需额外 SDK，但需自行处理 SDP 交换与 ICE 协商。
- **AOQ**：适合移动端原生应用（Android/iOS/HarmonyOS），对延迟、弱网、多模态混合传输有极致要求；需集成 [SDK下载](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-quick-start-guide/realtime-sdk-download.md) 提供的 AOQ Client SDK 及 Opus 插件。

### 典型接入流程（AOQ）
1. **AppServer 获取凭证**：调用百炼 `/api/v1/webrtc/realtime?model=...` 接口（带 `x-dashscope-rtc-transport: moq`），传入 `clientIp`，获取 `sid` 和 `aoqTokenForClient`；
2. **客户端初始化引擎**：调用 `createEngine`，设置 `AoqEngineDelegate` 回调；
3. **启动媒体采集**：`startAudioCapture()` / `startVideoCapture()`；
4. **禁用媒体发送**：`enableSendMediaStream(.audio, false)`，防止模型未就绪即推送数据；
5. **建立连接**：构造 `AoqConnectConfig`（填入 `token`/`sid`/`certFingerprint`/`relayEndpoints`），调用 `connect()`；
6. **等待会话就绪**：监听 `onDataMsg`，收到 `session.updated` 后调用 `enableSendMediaStream(.audio, true)` 开启发送；
7. **断开连接**：调用 `disconnect()`，非必须调用 `destroy()`（引擎可复用）。

### 典型接入流程（WebRTC）
1. 创建 `RTCPeerConnection({ iceServers: [] })`；
2. 添加音频轨道（必需）和视频轨道（可选），**立即禁用发送**（`track.enabled = false` + `sender.replaceTrack(null)`）；
3. 创建 `oai-events` DataChannel；
4. 调用 `createOffer()` → `setLocalDescription()`，等待 `iceGatheringState === "complete"` 获取完整 Offer SDP；
5. 由 AppServer 代理 POST Offer SDP 至百炼 WebRTC endpoint（如 `https://<workspace_id>.cn-beijing.maas.aliyuncs.com/api/v1/webrtc/inference?model=multimodal-dialog`）；
6. 将返回的 Answer SDP 规范化（确保 `\r\n` 行尾）后调用 `setRemoteDescription()`；
7. 收到 `pc.ontrack` 后播放远端音频流，收到 `session.created` 后恢复媒体发送。

## 限制和注意事项

- **API Key 安全**：严禁将 API Key 硬编码至客户端代码或提交至代码仓库；AOQ 必须通过服务端代理鉴权，WebSocket/WebRTC 的生产环境也应由 AppServer 代理 SDP 交换或连接建立 [Token鉴权](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-quick-start-guide/realtime-token-authentication.md)。
- **媒体流控制**：AOQ 和 WebRTC 均要求在收到 `session.updated`（或 `session.created`）后再开启媒体发送，否则服务端可能拒绝接收数据；`enableSendMediaStream` 是 AOQ 的关键控制接口，其默认行为是连接成功后立即发送，务必显式禁用再启用 [媒体流发送管理](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-function/aoq-media-stream-control.md)。
- **平台与格式约束**：
  - AOQ 不支持浏览器环境（仅 Android/iOS/HarmonyOS）；
  - WebRTC 的 `multimodal-dialog` 模型需使用工作空间专属 endpoint（`{workspace_id}.{region}.maas.aliyuncs.com`），而非通用 endpoint；
  - AOQ 视频编码默认 `isExternal=false`，若需自定义视频输入，必须先调用 `startVideoCapture(config)` 并设置 `config.isExternal = true`，否则 `pushExternalVideoCapturedFrame` 不生效 [自定义视频输入](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-function/aoq-custom-video-input.md)；
  - 所有协议的音频输入格式均为 `pcm`，但采样率要求不同：WebSocket 输入为 16 kHz，AOQ/WebRTC 输入为 16 kHz（文档 4 明确），输出统一为 24 kHz PCM。
- **异常处理**：AOQ SDK 对物理限制（网络中断、设备故障）和外部因素（token 过期）有分级处理机制，瞬态错误（如 `Failed` 状态）会自动迁移至 `Disconnected`，业务层无需重复调用 `disconnect` [连接状态管理](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-function/aoq-connection-management.md)。

## 来源文档

- [Realtime API简介](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-overview.md)
- [SDK下载](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-quick-start-guide/realtime-sdk-download.md)
- [Token鉴权](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-quick-start-guide/realtime-token-authentication.md)
- [实现接通模型/应用](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-quick-start-guide/realtime-connect-model.md)
- [通过WebRTC使用qwen3.5-omni-plus-realtime实现实时通话](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-best-practices/best-practice-webrtc-omni-realtime.md)
- [通过WebRTC使用多模态交互套件实现实时通话](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-best-practices/best-practice-webrtc-multimodal-dialog.md)
- [通过AOQ使用qwen3.5-omni-plus-realtime实现实时通话](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-best-practices/best-practice-aoq-omni-realtime.md)
- [AOQ SDK简介](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-desc.md)
- [连接状态管理](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-function/aoq-connection-management.md)
- [音频常用功能介绍](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-function/aoq-audio-features.md)
- [自定义音频播放](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-function/aoq-custom-audio-playback.md)
- [媒体流发送管理](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-function/aoq-media-stream-control.md)
- [自定义音频采集](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-function/aoq-custom-audio-capture.md)
- [自定义视频输入](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-function/aoq-custom-video-input.md)
- [视频常用功能介绍](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-function/aoq-video-features.md)



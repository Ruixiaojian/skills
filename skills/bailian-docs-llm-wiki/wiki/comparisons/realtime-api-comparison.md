# 实时 API 方案对比：Omni Realtime API 与 Realtime API 用户指南

为帮助开发者在构建低延迟、多模态实时交互系统时做出精准技术选型，本文对百炼平台两大核心实时能力方案——**Omni Realtime API** 与 **Realtime API 用户指南**（以下简称 Realtime API）进行系统性对比分析。二者虽同属“实时”范畴，但在协议栈设计、模型能力边界、接入复杂度、适用终端及运维范式上存在本质差异。本对比聚焦工程落地关键维度，不替代具体模型文档，旨在提供可操作的选型决策依据。

## 关键维度对比

| 维度 | Omni Realtime API | Realtime API 用户指南 |
|------|-------------------|------------------------|
| **通信协议** | 仅支持 WebSocket（`wss://.../api-ws/v1/realtime`） | 支持三协议栈：<br>• AOQ（推荐移动端原生场景）<br>• WebRTC（浏览器端首选）<br>• WebSocket（服务端/原型验证） |
| **输入格式** | • 音频：PCM（16-bit, mono, 16 kHz），Base64 编码，分块 ≤3200 字节<br>• 图像：JPG/JPEG（≤1080p），Base64 编码，单图 ≤256 KB<br>• 文本：通过 `session.update` 或 `conversation.item.create` 提交 | • 音频：PCM（16 kHz），支持自定义采集（`isExternal=true`）<br>• 视频：H.264/H.265 原始帧或 RTCPacket（AOQ/WebRTC）<br>• 文本/结构化数据：通过 `AoqDataMsg` 或 WebSocket JSON 消息传输<br>• *不支持图像直接上传*（需预处理为文本描述或特征向量） |
| **输出格式** | • 文本 + PCM 音频（24 kHz）流式推送<br>• 事件驱动：`response.text.delta`、`response.audio.delta` 等细粒度事件 | • 文本、PCM 音频（24 kHz）、视频帧（WebRTC/AOQ）<br>• 多轨道分离：`.audio`、`.video`、`.data` 可独立启停<br>• 输出由 SDK 自动解包/渲染（如 `onPlaybackAudioFrame`） |
| **支持模型** | • 专属 Omni 系列：<br> `qwen3.5-omni-realtime`（语义 VAD/搜索/工具调用）<br> `qwen3.5-omni-plus/flash-realtime`（`idle_timeout_ms`）<br> `qwen3-omni-flash-realtime`（`smooth_output`）<br> `qwen-omni-turbo-realtime`（固定参数）<br>• 内置 ASR：`qwen3-asr-flash-realtime`（不可替换） | • 全模态：`qwen3.5-omni-plus/flash-realtime`<br>• 语音翻译：`qwen3.5-livetranslate-flash-realtime`<br>• ASR：`Qwen-Audio-3.0-ASR-Flash-Streaming`、`Fun-ASR-Realtime`<br>• TTS：`CosyVoice` 系列<br>• 对话模型：`qwen-audio-3.0-realtime-plus/flash`<br>• *WebRTC 协议下 ASR/TTS 不可用*（仅 AOQ/WebSocket 支持） |
| **API 端点** | 固定 WebSocket 地址：<br>`wss://{WorkspaceId}.{region}.maas.aliyuncs.com/api-ws/v1/realtime` | • AOQ：无传统 HTTP 端点，通过 Relay 接入点（`relayEndpoints`）建连<br>• WebRTC：`POST /api/v1/webrtc/realtime?model=...`（SDP 交换）<br>• WebSocket：`wss://.../api-ws/v1/realtime`（兼容 Omni 端点，但模型与行为不同） |
| **计费方式** | • 按 **会话时长（秒）+ 音频处理量（分钟）+ 输出 tokens** 计费<br>• `qwen-omni-turbo-realtime` 等轻量模型单价更低<br>• 工具调用、联网搜索按次额外计费 | • 按 **协议类型 + 模型 + 使用时长/用量** 分层计费：<br> AOQ/WebSocket：按会话秒数 + 音频分钟数 + tokens<br> WebRTC：按会话秒数 + 媒体带宽（Mbps·小时）<br>• ASR/TTS 模型单独计费，与主模型解耦 |
| **典型场景** | • 超低延迟语音助手（端到端 <300ms）<br>• 高保真虚拟客服（需复刻音色+语义 VAD）<br>• 多模态对话机器人（图文+语音混合输入） | • 弱网环境移动 App（AOQ 抗丢包/快速重连）<br>• 浏览器端实时会议/教育互动（WebRTC 原生支持）<br>• 多模态开发套件集成（`multimodal-dialog` 快速搭建）<br>• 专业语音翻译/实时字幕系统 |

## 适用场景建议

### ✅ 选择 Omni Realtime API 当：
- 业务核心诉求是 **极致语音交互体验**：需语义级 VAD（`semantic_vad`）、音色复刻、工具自主调用、联网搜索等深度能力；
- 输入以 **语音+图像为主**，且要求服务端内置高精度 ASR（无需客户端集成 ASR SDK）；
- 架构已基于 WebSocket 构建，追求 **最小接入成本** 和 **统一事件模型**（所有交互均通过 `session.*` / `input_audio_buffer.*` / `response.*` 事件驱动）；
- 场景对 **模型参数可控性要求高**（如需动态调节 `temperature`、`top_p`），且不使用 `turbo` 系列限制模型。

### ✅ 选择 Realtime API 当：
- 需要 **跨平台全终端覆盖**：尤其需同时支持 iOS/Android 原生 App（AOQ）与 Chrome/Safari 浏览器（WebRTC）；
- 存在 **弱网/高抖动网络挑战**：AOQ 协议提供 QUIC 层重传、前向纠错、智能路由，显著优于 WebSocket 在 3G/地铁等场景表现；
- 业务涉及 **多模态混合传输**：如视频通话中叠加实时字幕（ASR）、AI 美颜（视频处理）、语音合成（TTS），需独立控制 `.video`/`.audio`/`.data` 轨道；
- 已有 **WebRTC 基础设施** 或需与现有音视频 SDK（如 Agora、腾讯云 TRTC）集成；
- 需要 **灵活的媒体处理链路**：如自定义音频采集（对接硬件麦克风阵列）、自定义播放（混音/降噪/3D 音效）。

## 技术选型参考（面向开发者）

| 选型考量点 | 推荐方案 | 说明 |
|------------|----------|------|
| **首次接入速度** | Omni Realtime API | WebSocket 协议标准、SDK 封装成熟，5 分钟可跑通 Hello World；Realtime API 的 AOQ/WebRTC 需理解信令流程与媒体轨道管理。 |
| **终端兼容性** | Realtime API（WebRTC） | 浏览器零依赖；Omni Realtime API 的 WebSocket 在部分老旧浏览器或企业防火墙下可能受限。 |
| **语音质量与延迟敏感度** | Omni Realtime API | 专为语音优化，VAD 响应更灵敏，音频编解码链路更短；Realtime API 的 AOQ 虽抗丢包强，但协议栈更深，端到端延迟略高（约 +50~100ms）。 |
| **扩展性与长期演进** | Realtime API | 协议栈解耦设计（AOQ/WebRTC/WebSocket 共享同一后端模型服务），未来新增协议（如 AV1 视频）成本更低；Omni API 为垂直领域封闭架构。 |
| **运维与调试复杂度** | Omni Realtime API | 事件日志清晰（`session.created` → `speech_started` → `response.audio.delta`），便于问题定位；Realtime API 的 AOQ 需监控 Relay 连接状态、轨道健康度等多维指标。 |
| **合规与私有化部署** | Realtime API（AOQ） | AOQ 支持私有 Relay 部署，满足金融/政务客户对媒体流不出域的要求；Omni Realtime API 当前仅支持公有云 SaaS 模式。 |

> **重要提醒**：  
> - Omni Realtime API 与 Realtime API **非互换替代关系**，而是互补演进——Omni 专注“语音优先”的极致体验，Realtime API 构建“全模态通信底座”。  
> - 若项目需同时满足“高保真语音交互”与“跨终端弱网鲁棒性”，建议采用 **分层架构**：前端根据终端类型自动选择协议（WebRTC for Browser / AOQ for Mobile），后端统一调用 Omni 系列模型处理核心对话逻辑。  
> - 所有模型名称、参数约束、计费细则请以 [阿里云百炼控制台](https://bailian.console.aliyun.com) 实时信息为准，避免硬编码已下线型号（如文档提及但控制台不可见的 `qwen3.5-omni-plus-realtime`）。

## 被对比主题页

- [omni realtime api](../api/omni-realtime-api.md)
- [realtime api user guide](../api/realtime-api-user-guide.md)



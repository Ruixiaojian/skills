# 实时 API 方案对比：Omni Realtime vs Realtime User Guide

本页旨在为开发者提供清晰、客观的技术选型参考，对比百炼平台当前两类核心实时多模态交互方案：**Omni Realtime API**（基于 WebSocket 的标准化事件驱动接口）与 **Realtime API User Guide**（面向全协议栈的通用实时能力框架）。二者虽均服务于低延迟语音/文本/图像交互场景，但在架构定位、协议支持、模型覆盖、接入复杂度及适用边界上存在显著差异。本文不替代官方文档，而是聚焦关键维度进行横向比对，帮助团队根据业务目标（如端侧类型、网络环境、定制深度、交付周期）快速决策。

## 关键维度对比

| 维度 | Omni Realtime API | Realtime API User Guide |
|------|-------------------|--------------------------|
| **核心定位** | 专用型、强约束的**多模态实时会话协议**（聚焦 Qwen-Omni 系列模型），以事件流（Event-Driven）为核心范式 | 通用型、协议可选的**实时交互能力框架**，统一抽象多模型、多协议（WebSocket/WebRTC/AOQ）接入层 |
| **输入格式** | • PCM 音频（16 kHz，单声道）<br>• JPG/JPEG 图像（≤1080p，Base64 编码 ≤256 KB）<br>• *图像必须在首次音频输入后发送* | • PCM 音频（16 kHz）<br>• 图像支持同 Omni（JPG/JPEG，≤256 KB Base64）<br>• **AOQ/WebRTC 支持原始帧/编码帧视频输入（I420/NV12/BGRA/JPEG）**<br>• **WebSocket 协议下仅支持音频+图像，无视频原生支持** |
| **输出格式** | • 文本（UTF-8）<br>• PCM 音频（24 kHz，单声道）<br>• *固定双模态组合 `["text"]` 或 `["text","audio"]`* | • 文本（UTF-8）<br>• PCM 音频（24 kHz）<br>• **AOQ/WebRTC 支持自定义音频采样率与编码（Opus）**<br>• **WebRTC/AOQ 支持视频流回传（需模型支持）** |
| **支持模型** | • 仅限 `qwen3.5-omni-*` / `qwen3-omni-*` / `qwen-omni-turbo-*` 等 **Omni 系列实时专用模型**<br>• 明确区分 `realtime`、`plus-realtime`、`flash-realtime` 子型号 | • **全谱系覆盖**：<br>  - Omni 全模态模型（`qwen3.5-omni-plus-realtime` 等）<br>  - 多模态开发套件（`multimodal-dialog`）<br>  - Fun-ASR（语音识别）<br>  - CosyVoice（语音合成）<br>  - `qwen-audio-*`（纯语音对话）<br>  - `qwen3.5-livetranslate-flash-realtime`（实时翻译） |
| **API 端点与协议** | • **仅 WebSocket**：<br> `wss://{WorkspaceId}.{region}.maas.aliyuncs.com/api-ws/v1/realtime`<br>• 强制使用事件消息体（JSON-RPC 风格） | • **三协议可选**：<br>  - WebSocket：`wss://.../api-ws/v1/realtime`<br>  - WebRTC：通过 SDP 交换建立 P2P 媒体通道<br>  - AOQ（Media over QUIC）：`moq://` + Relay 接入点<br>• 统一 `session.update` 配置，但信令/媒体传输机制差异巨大 |
| **计费方式** | • 按 **实际调用时长（秒） + 输出 token 数** 计费<br>• 不同 Omni 模型单价不同（如 `turbo` 更低价，`plus` 更高质）<br>• 图像输入不额外计费 | • **按模型+协议+资源维度分项计费**：<br>  - Omni 模型：同 Omni Realtime 计费逻辑<br>  - ASR/CosyVoice：按音频时长（秒）计费<br>  - WebRTC/AOQ：含信令、Relay 流量、媒体转发等附加费用<br>• 控制台可查各模型实时价格快照 |
| **典型场景** | • 对延迟极度敏感的智能客服坐席系统<br>• 需要语音+图像联合理解的工业质检助手<br>• 集成声音复刻（Voice Cloning）的个性化语音助理<br>• 快速验证 Omni 模型能力的 PoC 项目 | • 跨端统一架构：同一业务需同时支持 Web（WebRTC）、App（AOQ）、服务端（WebSocket）<br>• 弱网环境下的移动端语音助手（AOQ 弱网对抗）<br>• 浏览器内嵌实时通话（WebRTC 回声消除+媒体处理）<br>• 分离式 ASR+LLM+TTS 流水线编排（如 Fun-ASR → Omni → CosyVoice） |
| **VAD 能力** | • `server_vad`（全模型支持）<br>• `semantic_vad`（仅 `qwen3.5-omni-realtime` 系列）<br>• `idle_timeout_ms` 仅在 `plus/flash` + `server_vad` 下生效 | • `server_vad` / `semantic_vad` 支持同 Omni<br>• **AOQ/WebRTC 提供更精细的客户端 VAD 控制接口（如 `setVadConfig`）**<br>• WebRTC 内置浏览器级音频预处理（AGC/ANS） |
| **高级能力** | • 工具调用（`tools`）：仅 `qwen3.5-omni-realtime` 系列<br>• 联网搜索（`enable_search`）：同上，且与 `tools` 互斥<br>• 声音复刻：需前置调用 `qwen-voice-enrollment` | • 工具调用 & 联网搜索：同 Omni 限制<br>• **AOQ/WebRTC 支持完全自定义音频采集/播放链路（外部数据源/渲染器）**<br>• **WebRTC 支持多轨道（音频+视频+数据通道）协同**<br>• **AOQ 支持服务端动态下发音色/指令更新（`session.updated` 事件）** |
| **接入复杂度** | • 中等：需理解事件生命周期（`session.created` → `input_audio_buffer.append` → `response.create` → `conversation.item.created`）<br>• SDK 封装较完善（Python/JS） | • **分层复杂度**：<br>  - WebSocket：低（同 Omni）<br>  - WebRTC：高（SDP 交换、ICE 管理、媒体轨道绑定）<br>  - AOQ：中高（SDK 初始化、[Token](../concepts/token.md) 获取、Relay 连接、媒体流启停时序）<br>• 官方提供各协议完整 SDK 与最佳实践示例 |

## 适用场景建议

### 选择 Omni Realtime API 当：
- 你的业务**严格限定于 Qwen-Omni 系列模型**，且需要其独有的多模态理解（语音+图像联合推理）与低延迟响应；
- 你已确定使用 **WebSocket 协议**，并接受其服务端集成为主的部署模式（如 Node.js 后端代理）；
- 你需要快速上线一个具备**声音复刻、语义级 VAD、工具调用**能力的语音助手原型；
- 你对协议扩展性要求不高，但对 Omni 模型行为一致性（如 `idle_timeout_ms` 触发逻辑）有强依赖。

### 选择 Realtime API User Guide 当：
- 你的产品需**跨平台（Web/App/Server）统一接入**，或明确要求 **WebRTC 浏览器原生音视频** 或 **AOQ 移动端极致弱网体验**；
- 你需要**灵活组合不同模型能力**（例如：前端用 Fun-ASR 实时转写 → 后端用 Omni 理解 → 再调 CosyVoice 合成）；
- 你有**深度定制需求**：如自定义音频采集设备（车载麦克风阵列）、自定义视频编码器（H.264 硬编）、或绕过 SDK 直接控制媒体流；
- 你正在构建企业级实时交互中台，需统一管理多种实时能力（ASR/TTS/LLM/Translation）的配额、监控与熔断策略。

## 技术选型参考（面向开发者）

| 选型考量 | 推荐方案 | 理由 |
|----------|----------|------|
| **最小可行产品（MVP）验证 Omni 模型能力** | ✅ Omni Realtime API | 接入路径最短，事件模型清晰，无需处理协议底层（如 SDP、QUIC），专注模型效果调优 |
| **ToC 移动端 App（Android/iOS）且弱网频发** | ✅ Realtime API (AOQ) | AOQ 协议专为移动端优化，建连快、抗丢包、带宽自适应，远优于 WebSocket 在 3G/地铁场景表现 |
| **网页端实时客服（需摄像头+麦克风）** | ✅ Realtime API (WebRTC) | 利用浏览器原生音视频栈，自动处理回声消除、降噪、自动增益；避免 WebSocket 下自行实现复杂音频前处理 |
| **后台服务集成（如呼叫中心中间件）** | ⚖️ 两者皆可，倾向 Omni Realtime | WebSocket 协议成熟稳定，Omni 事件语义明确（如 `speech_stopped` 可精准触发后续流程），运维成本更低 |
| **需同时支持语音识别（ASR）与大模型对话（LLM）** | ✅ Realtime API | Omni Realtime **不支持独立 ASR 模型**；而 Realtime API 可分别调用 `fun-asr-*` 和 `qwen3.5-omni-*`，实现解耦编排 |
| **已有 WebRTC 基础设施，需叠加 AI 能力** | ✅ Realtime API (WebRTC) | 复用现有 SDP/ICE/媒体轨道管理，只需替换 `RTCPeerConnection` 的 `ontrack` 处理逻辑为百炼 Realtime 流程 |
| **安全合规要求 API Key 绝不暴露至客户端** | ✅ Realtime API (AOQ) | AOQ 强制服务端鉴权获取 `aoqTokenForClient`，客户端仅持短期 [Token](../concepts/token.md)；Omni Realtime 的 WebSocket 连接需客户端携带 API Key（需 Proxy 代理） |

> **重要提醒**：  
> - Omni Realtime 是 Realtime API 框架下的一个**特定模型+协议子集**，而非平行方案。其所有能力（除部分参数细节外）均被 Realtime API User Guide 所涵盖。  
> - 若未来计划扩展协议支持（如增加 WebRTC）、模型类型（如引入 ASR）或定制深度（如自定义音频链路），**强烈建议直接采用 Realtime API User Guide 作为长期技术底座**，避免后期迁移成本。  
> - 无论选择哪一方案，务必通过 [百炼控制台](https://dashscope.console.aliyun.com/) 查看模型最新状态、价格、限流策略及地域可用性。

## 被对比主题页

- [omni realtime api](../api/omni-realtime-api.md)
- [realtime api user guide](../api/realtime-api-user-guide.md)



# 实时 API 方案对比：Omni Realtime API vs Realtime API

本文旨在帮助开发者清晰理解百炼平台两大实时交互方案的核心差异，辅助技术选型决策。随着智能语音助手、实时客服、多模态对话等场景对低延迟、高保真、多协议适配能力提出更高要求，百炼平台提供了两类定位互补的实时 API 能力：

- **Omni Realtime API**：聚焦「单点极致体验」，是专为语音优先、强交互性、端到端可控的多模态对话场景深度优化的 WebSocket 原生接口；
- **Realtime API**：面向「全场景工程落地」，提供 AOQ / WebRTC / WebSocket 三协议统一抽象，强调跨终端兼容性、弱网鲁棒性与企业级集成能力。

二者并非简单替代关系，而是分层协作：Omni Realtime API 是 Realtime API 生态中面向高端语音对话场景的**旗舰子集**（当前仅通过 WebSocket 协议暴露），而 Realtime API 则是覆盖更广模型类型、更多传输协议、更强基础设施支持的**统一接入层**。

以下从关键维度展开对比分析，所有信息均基于最新稳定版文档（2024 Q3）整理。

## 关键维度对比

| 维度 | Omni Realtime API | Realtime API |
|------|-------------------|--------------|
| **协议支持** | 仅 WebSocket（`wss://.../api-ws/v1/realtime`） | ✅ AOQ（移动端原生）、✅ WebRTC（浏览器/WebApp）、✅ WebSocket（服务端/原型验证） |
| **输入格式** | PCM 音频（16 kHz，小端序，16-bit）；JPG/JPEG 图像（≤1080p，Base64 编码） | 同 Omni Realtime API（PCM 音频 + 图像），但 **AOQ/WebRTC 支持原生音视频轨道流**（无需手动切片/编码） |
| **输出格式** | 文本（`response.text.delta`）、PCM 音频（24 kHz，小端序，16-bit） | 同 Omni Realtime API；AOQ/WebRTC 还支持直接接收 `MediaStreamTrack` 或 `AudioBuffer`，免解码 |
| **支持模型** | 仅限 Omni 系列实时模型：<br>• `qwen3.5-omni-realtime`（旗舰）<br>• `qwen3-omni-flash-realtime`（高性能）<br>• `qwen-omni-turbo-realtime`（超低延迟） | 更广泛：<br>• Omni 全系列（`qwen3.5-omni-plus-realtime` 等）<br>• ASR 模型（如 `Qwen-Audio-3.0-ASR-Flash-Streaming`）<br>• TTS 模型（如 `CosyVoice`）<br>• 语音对话模型（`qwen-audio-3.0-realtime-plus`）<br>• 多模态开发套件（`multimodal-dialog`） |
| **API 端点** | 固定 WebSocket 地址：<br>`wss://{WorkspaceId}.{region}.maas.aliyuncs.com/api-ws/v1/realtime` | 协议差异化：<br>• AOQ：`wss://.../aoq/v1/realtime`（需 `x-dashscope-rtc-transport: moq`）<br>• WebRTC：SDP 协商后动态 ICE endpoint（白名单开放）<br>• WebSocket：同 Omni 端点，但 URL 参数需显式指定 `?model=...` |
| **计费方式** | 按 **实际音频处理时长（秒） + 文本 token 数量** 计费；语音流空闲期（idle）不计费；工具调用、搜索等扩展能力单独计费 | 同 Omni 计费逻辑，但 **按协议/模型粒度拆分计费项**：<br>• AOQ/WebRTC：含信令、媒体转发、AI 推理三部分费用<br>• WebSocket：仅 AI 推理费用（无信令/转发成本）<br>• ASR/TTS 模型独立计费单元 |
| **VAD 能力** | • `server_vad`（声学级，全模型支持）<br>• `semantic_vad`（语义级，仅 `qwen3.5-omni-realtime` 支持）<br>• `idle_timeout_ms` 仅在 `server_vad` + 特定模型下生效 | • 默认推荐 `semantic_vad`（全协议通用）<br>• `server_vad` 可选，兼容性更广<br>• `idle_timeout_ms` 在 AOQ/WebRTC 中由 SDK 自动管理，WebSocket 下需手动配置 |
| **工具调用（Function Calling）** | ✅ 支持，需客户端回传结果并显式触发 `response.create` | ✅ 支持（Omni 系列模型），但 ASR/TTS 等单向模型不支持 |
| **联网搜索（Search）** | ✅ `qwen3.5-omni-realtime` 支持 `enable_search`（与 `tools` 互斥） | ✅ 同 Omni，且 `qwen3.5-omni-plus-realtime` 等模型亦支持 |
| **声音复刻集成** | ✅ 支持，需先调用 `qwen-voice-enrollment`，再于 `session.update` 中指定 `voice` | ✅ 支持，但音色 ID 需与目标模型严格匹配（如 `Ethan` 仅适用于 `qwen3.5-omni-plus-realtime`） |
| **SDK 与客户端控制粒度** | DashScope SDK 提供 `update_session`、`append_audio_buffer` 等细粒度方法；事件驱动模型要求开发者管理状态机 | • AOQ SDK：提供 `enableSendMediaStream()` 等媒体流生命周期控制<br>• WebRTC：依赖原生 API，控制自由度高<br>• WebSocket：与 Omni SDK 接口高度一致，但缺少 AOQ 的弱网自适应逻辑 |
| **弱网对抗能力** | ❌ 无内置抗丢包、FEC、带宽自适应机制；依赖 WebSocket 底层 TCP 重传，易受网络抖动影响 | ✅ AOQ 协议内置前向纠错（FEC）、动态码率调整、QUIC 传输优化<br>✅ WebRTC 支持 NACK/PLI/FIR、拥塞控制（GCC）<br>❌ WebSocket 无额外优化 |

## 适用场景建议

### ✅ 选择 Omni Realtime API 当：
- 构建**高保真语音助手或虚拟人对话系统**，对语音合成自然度、响应延迟（端到端 < 300ms）、语义 VAD 准确性有极致要求；
- 已具备成熟的 WebSocket 客户端基础设施（如 Electron 桌面应用、Node.js 服务端代理、Flutter Web）；
- 场景以**语音+文本为主，偶发图像理解需求**（如拍照问答），无需 ASR/TTS 独立调用；
- 开发团队熟悉事件驱动编程模型，能自主管理 `session` 状态、音频缓冲区、工具调用闭环；
- 业务部署环境网络质量稳定（如内网、5G 专网），无需强弱网容错。

> 📌 典型客户案例：金融远程银行坐席助手、车载语音交互中控、教育类口语陪练 App（Web 端原型验证阶段）。

### ✅ 选择 Realtime API 当：
- 需要**跨平台统一接入**：同一套业务逻辑需同时支持 iOS/Android/HarmonyOS（AOQ）、Chrome/Safari（WebRTC）、以及后台服务（WebSocket）；
- 场景涉及**混合模型调用**：例如前端用 WebRTC 实时语音对话 + 后端用 WebSocket 异步调用 ASR 分析历史录音；
- 面向**公网弱网用户**（如三四线城市移动网络），需保障 3G/弱 Wi-Fi 下的可用性与流畅度；
- 已有 WebRTC 基础设施（如自研音视频 SDK、SFU 架构），希望复用现有信令与媒体栈；
- 需要**精细化媒体流控制**：如动态开关麦克风/摄像头、混音、音效注入、自定义编解码参数；
- 企业级部署要求**API Key 严格隔离**：AOQ 强制服务端鉴权，杜绝密钥泄露风险。

> 📌 典型客户案例：在线医疗问诊平台（医生端 WebRTC + 患者端 AOQ）、跨国会议实时翻译系统（ASR+TTS+Omni 多模型协同）、IoT 设备语音中控（AOQ 低功耗长连接）。

## 技术选型参考指南（面向开发者）

| 选型考量点 | 推荐方案 | 说明 |
|------------|----------|------|
| **首次集成，快速验证 MVP** | ✅ Omni Realtime API（WebSocket） | 无需申请白名单、无需集成 SDK、无信令协商复杂度；DashScope SDK 开箱即用，5 分钟完成 Hello World 对话 |
| **生产环境，面向海量终端用户** | ✅ Realtime API（AOQ for Mobile / WebRTC for Web） | AOQ 提供最佳移动端体验与弱网稳定性；WebRTC 是浏览器实时交互事实标准；两者均通过百炼统一 Token 鉴权，安全合规 |
| **需要 ASR 或 TTS 独立能力** | ✅ Realtime API | Omni Realtime API 仅封装全模态模型，不提供纯 ASR/TTS 接口；Realtime API 显式支持 `Qwen-Audio-3.0-ASR-Flash-Streaming` 等专用模型 |
| **已有 WebRTC 技术栈** | ✅ Realtime API（WebRTC 协议） | 复用 SDP/ICE/DTLS 流程，仅需对接百炼信令服务；避免 WebSocket 封装音频帧带来的额外延迟与 CPU 开销 |
| **定制化语音处理链路** | ✅ Realtime API（AOQ） | AOQ SDK 提供 `onAudioFrameReceived` 等底层回调，支持在发送前注入降噪、回声消除、VAD 后处理逻辑 |
| **严格遵循最小权限原则（安全合规）** | ✅ Realtime API（AOQ） | 客户端仅持有短期 `aoqTokenForClient`，服务端完全掌控 API Key；WebSocket/AOQ 直连模式必须经后端 Token 中转，否则违反百炼安全规范 |

> ⚠️ 重要提醒：  
> - **Omni Realtime API 是 Realtime API 的子集，非并列关系**。其功能、模型、事件规范均遵循 Realtime API 总体设计，差异在于协议收敛与能力聚焦。  
> - 所有 WebSocket 接入方式（无论 Omni 或 Realtime）**均不推荐在前端 JavaScript 中直连**（存在 API Key 泄露风险），务必通过自有服务端代理鉴权与请求转发。  
> - 若选用 WebRTC，请提前联系商务开通 Endpoint 白名单，并预留至少 3 个工作日完成环境联调。

如需进一步评估具体场景的架构适配性，建议结合 [Realtime API 概述](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-overview.md) 中的协议兼容性矩阵，或使用百炼控制台「实时 API 调试沙箱」进行多协议压测对比。

## 被对比主题页

- [omni realtime api](../api/omni-realtime-api.md)
- [realtime api user guide](../api/realtime-api-user-guide.md)



# 实时 API 方案对比：Omni Realtime API vs Realtime API User Guide

## 对比目的与背景

为帮助开发者在百炼平台构建低延迟、高保真实时交互应用（如智能客服、虚拟助手、实时翻译、多模态对话系统），本文对两类核心实时能力方案进行系统性对比：  
- **Omni Realtime API**：聚焦端到端多模态流式交互的 WebSocket 原生协议，强调语音-文本-图像协同与事件驱动控制；  
- **Realtime API User Guide**：面向工程落地的**协议抽象层方案**，统一支持 AOQ / WebRTC / WebSocket 三种传输协议，强调跨终端适配、网络鲁棒性与企业级集成能力。

二者并非简单替代关系，而是**不同抽象层级与设计目标的技术路径**：Omni Realtime API 是具体模型能力的接口规范；Realtime API User Guide 是覆盖更广模型生态、协议选型与工程实践的综合接入框架。本对比旨在厘清定位差异，辅助技术选型决策。

---

## 关键维度对比表

| 维度 | Omni Realtime API | Realtime API User Guide |
|------|-------------------|--------------------------|
| **协议类型** | 仅支持 WebSocket（`wss://.../api-ws/v1/realtime`） | 支持 **AOQ（推荐移动端）、WebRTC（推荐浏览器）、WebSocket（推荐服务端/原型验证）** 三协议可选 |
| **输入格式** | • 音频：16 kHz PCM 单声道（Base64）<br>• 图像：JPG/JPEG（≤1080p，Base64 ≤256 KB）<br>• 文本：通过 `instructions` 或 `conversation.item.create` 注入 | • 音频/图像/文本格式同 Omni（PCM/JPEG/Base64）<br>• **AOQ 支持原生音视频采集、外部流注入（如 TTS 输出、ASR 输入）及自定义编解码帧**<br>• WebRTC 仅支持标准媒体轨道（无图像/文本直接注入能力） |
| **输出格式** | • 文本：`response.text.delta` 流式 UTF-8 字符串<br>• 音频：24 kHz PCM（Base64）<br>• 转录：`conversation.item.input_audio_transcription.*` 事件 | • 文本/音频格式同 Omni<br>• **AOQ/WebSocket 支持 ASR/TTS 独立模型（如 `Fun-ASR-Realtime`, `CosyVoice`）**<br>• WebRTC **不支持 ASR/TTS 模型**，仅支持对话类模型 |
| **支持模型** | • 专属模型族：<br> `qwen3.5-omni-realtime`（含工具调用/搜索）<br> `qwen3.5-omni-plus-realtime` / `flash-realtime`（含 `idle_timeout_ms`, `smooth_output`）<br> `qwen-omni-turbo-realtime`（基础 VAD + 音文 I/O） | • **更广模型矩阵**：<br> 全协议：`qwen3.5-omni-plus-realtime`, `qwen3.5-omni-flash-realtime`, `multimodal-dialog`, `qwen-audio-3.0-realtime-*`<br> AOQ/WebSocket 专属：`qwen3.5-livetranslate-flash-realtime`, `Qwen-Audio-3.0-ASR-Flash-Streaming`, `CosyVoice`<br> WebRTC 仅支持对话类模型（无 ASR/TTS） |
| **API 端点** | 固定 WebSocket 地址：<br>`wss://{WorkspaceId}.{region}.maas.aliyuncs.com/api-ws/v1/realtime` | • **协议差异化端点**：<br> AOQ：由 `allocate` 接口返回 `relayEndpoints` + `aoqTokenForClient`<br> WebRTC：`wss://.../api-webrtc/v1/realtime`（白名单开放）<br> WebSocket：同 Omni 端点（但需传 `model` 查询参数） |
| **计费方式** | 按 **实际消耗 token 数 + 音频处理时长（秒）** 计费（详见 [计费说明](../../raw/pricing/realtime-api-pricing.md)），模型间单价不同 | 同 Omni Realtime API —— **统一按 token + 音频时长计费**，不同模型对应不同单价；AOQ/WebRTC/WebSocket 协议本身不额外计费 |
| **典型场景** | • 高保真语音助手（需语义 VAD、工具调用、联网搜索）<br>• 多模态客服（语音+图片联合理解）<br>• 声音复刻集成（需预创建音色） | • 移动端弱网环境语音对话（AOQ 抗丢包/低延迟）<br>• 浏览器内嵌实时翻译（WebRTC 免插件）<br>• 服务端批量语音转写（WebSocket + ASR 模型）<br>• 自定义音视频处理链路（AOQ 外部流注入） |
| **鉴权机制** | WebSocket 连接时通过 `Authorization: Bearer <API_KEY>` Header 认证 | • **强制服务端下发 [Token](../concepts/token.md)**：<br> AOQ/WebRTC：`allocate` 接口返回短期有效 `aoqTokenForClient` 或 `webrtcToken`<br> WebSocket：仍支持 API Key，但**强烈建议使用 [Token](../concepts/token.md) 鉴权**（提升安全性） |
| **开发复杂度** | • 中等：需理解事件驱动模型（`session.update`, `input_audio_buffer.append` 等）<br>• SDK 封装较薄（Python/Java SDK 提供基础封装） | • **分层复杂度**：<br> WebSocket：同 Omni，低门槛<br> WebRTC：依赖浏览器 API，需处理 ICE/SDP 协商<br> AOQ：需集成原生 SDK、管理媒体流生命周期、加载 Opus 插件，复杂度最高但能力最强 |
| **高级能力支持** | • 工具调用（仅 `qwen3.5-omni-realtime`）<br>• 联网搜索（仅 `qwen3.5-omni-realtime`，与 tools 互斥）<br>• 声音复刻（需独立 API 创建音色） | • 工具调用/搜索：同 Omni（取决于所选模型）<br>• **AOQ 独有**：<br> 自定义音频采集/播放（TTS 输出直推、ASR 输入接管）<br> 自定义视频输入（原始帧/NV12/JPEG）<br> 内置回声消除（AEC）、降噪（NS）、自动增益（AGC） |

---

## 适用场景建议

### ✅ 选择 Omni Realtime API 当：
- 项目已明确采用 WebSocket 协议，且无需跨协议兼容；
- 核心需求聚焦于 **Qwen-Omni 系列模型的端到端多模态交互**（语音+图像+文本联合理解与生成）；
- 需要 **语义级语音活动检测（semantic_vad）**、**工具调用**或**联网搜索**等高级推理能力；
- 团队熟悉 WebSocket 事件模型，能自主管理会话状态与缓冲区生命周期；
- 快速验证原型，或服务端集成（如 Node.js 后端直连）。

### ✅ 选择 Realtime API User Guide 当：
- 面向 **多终端发布**（iOS/Android/HarmonyOS + Web），需协议灵活适配；
- **移动端弱网环境为关键指标** → 优先选用 AOQ 协议；
- 需要 **独立 ASR/TTS 能力**（如语音转文字、文字转语音分离处理）→ 选用 AOQ 或 WebSocket；
- 已有 WebRTC 基础设施（如视频会议 SDK），希望复用媒体栈 → 选用 WebRTC（注意模型限制）；
- 需深度定制音视频处理流程（如 TTS 输出直送耳机、ASR 结果喂给第三方引擎）→ AOQ 外部流注入是唯一选择；
- 企业级安全要求高 → 强制 [Token](../concepts/token.md) 鉴权 + 服务端管控生命周期。

> ⚠️ 注意：`qwen3.5-omni-realtime` 等模型既可通过 Omni Realtime API（WebSocket 专用）调用，也可通过 Realtime API User Guide 的 WebSocket/AOQ/WebRTC 协议接入。**后者提供更丰富的协议选项与工程支撑，前者提供更精简的模型交互契约。**

---

## 技术选型参考（面向开发者）

| 你的需求 | 推荐方案 | 理由 |
|----------|-----------|------|
| “我只想快速跑通一个语音助手 Demo，用 Python 写后端” | ✅ Omni Realtime API（WebSocket） | SDK 简单，文档聚焦，无需协议选型，5 分钟可连通 |
| “我要开发 iOS App，用户常在地铁/电梯里使用，语音不能卡顿” | ✅ Realtime API + AOQ 协议 | AOQ 专为弱网优化，内置 AEC/NS/AGC，建连快、抗丢包强 |
| “我在做网页版在线翻译，已有 WebRTC 视频通话功能” | ✅ Realtime API + WebRTC 协议 | 复用现有媒体栈，零新增依赖；注意仅支持对话模型，不支持 ASR/TTS |
| “我需要把 TTS 生成的音频实时喂给耳机，同时把麦克风音频送入 ASR” | ✅ Realtime API + AOQ（外部流注入） | 唯一支持双向自定义音频流的方案，可绕过 SDK 默认采集链路 |
| “我要构建客服系统，需同时支持网页、App、小程序，且要调用天气 API” | ✅ Realtime API（协议按端选型） + `qwen3.5-omni-realtime` 模型 | 统一模型能力，协议层解耦：Web 用 WebRTC，App 用 AOQ，后台用 WebSocket；工具调用能力一致 |
| “我只关心语音识别准确率，不需合成，且部署在 Linux 服务器” | ✅ Realtime API + WebSocket + `Qwen-Audio-3.0-ASR-Flash-Streaming` | WebSocket 接入最轻量，ASR 模型专属优化，服务端直连稳定可靠 |

**最终建议**：  
- **新项目起步**：优先评估 Realtime API User Guide，因其协议灵活性与长期演进能力更强；  
- **已有 Omni Realtime API 项目**：无需迁移，但可逐步将 AOQ/WebRTC 纳入多端支持规划；  
- **务必验证模型-协议兼容性**：查阅 [Realtime API 概述](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-overview.md) 中的兼容性矩阵，避免因协议选择导致模型不可用。

## 被对比主题页

- [omni realtime api](../api/omni-realtime-api.md)
- [realtime api user guide](../api/realtime-api-user-guide.md)



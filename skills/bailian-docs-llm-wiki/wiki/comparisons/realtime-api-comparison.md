# 实时 API 方案对比：Omni Realtime 与 Realtime API

本页旨在为开发者提供 **Omni Realtime API** 与 **Realtime API** 两大实时交互方案的系统性对比，帮助技术团队基于业务需求、终端环境、功能复杂度及工程约束，做出清晰、可落地的技术选型决策。二者虽同属百炼平台实时 AI 能力体系，但在设计哲学、协议栈、能力边界和适用场景上存在本质差异：  
- **Omni Realtime API** 是面向「多模态语音助手」场景深度定制的 WebSocket 原生事件驱动接口，强调语义级交互控制与端到端低延迟；  
- **Realtime API** 是平台级统一实时接入层，通过 **AOQ / WebRTC / WebSocket 三协议抽象**，兼顾跨终端兼容性、基础设施复用性与模型能力泛化支持。  

以下从关键维度展开对比，并附选型建议。

---

## 关键维度对比

| 维度 | Omni Realtime API | Realtime API |
|------|-------------------|--------------|
| **核心协议与传输机制** | 纯 WebSocket（WSS），事件驱动（`session.update`, `input_audio_buffer.append`, `response.audio.delta` 等） | **三协议可选**：<br>• AOQ（推荐移动端原生应用，含内置 AEC/NS）<br>• WebRTC（浏览器端首选，SDP 鉴权）<br>• WebSocket（服务端集成/快速验证，SDK 封装） |
| **输入格式** | • 音频：PCM/WAV 单声道，8k–48k Hz，16-bit<br>• 图像：JPG/JPEG（≤1080p，Base64 编码后 ≤256KB）<br>• 文本：通过 `conversation.item.create` 提交 | • 音频/视频：由底层协议处理（AOQ/WebRTC 自动采集编码；WebSocket 需客户端预编码）<br>• 文本：同 Omni<br>• **图像支持依赖模型**：仅 `qwen3.5-omni-plus/flash-realtime` 等全模态模型支持，需配合音频提交 |
| **输出格式** | • `modalities: ["text"]` 或 `["text","audio"]`（强制包含 text）<br>• 音频：PCM/WAV，8k–48k Hz，可独立配置 `sample_rate`<br>• 支持细粒度流式事件（如 `response.audio.delta`, `response.text.delta`） | • 输出模态由所选模型决定（如 ASR 模型仅输出文本，TTS 仅输出音频）<br>• 音频流式交付依赖协议：AOQ/WebRTC 提供原生音视频轨道；WebSocket 返回 Base64 或二进制 chunk<br>• **无统一 `modalities` 控制字段**，由模型能力隐式决定 |
| **支持模型** | 仅支持 Omni 系列实时模型：<br>• `qwen3.5-omni-plus-realtime`（高保真+语义 VAD+联网搜索）<br>• `qwen3.5-omni-flash-realtime`（低延迟+平滑输出）<br>• `qwen-omni-turbo-realtime`（轻量文本/音频，参数锁定） | **模型覆盖更广**：<br>• 全模态：`qwen3.5-omni-plus/flash-realtime`<br>• 语音翻译：`qwen3.5-livetranslate-flash-realtime`<br>• ASR：`Qwen-Audio-3.0-ASR-Flash-Streaming`（**仅 AOQ/WebSocket**）<br>• TTS：`CosyVoice` / `qwen-audio-3.0-tts-*`（**仅 AOQ/WebSocket**）<br>• 语音对话：`qwen-audio-3.0-realtime-*` |
| **API 端点** | 业务空间专属 WSS 地址：<br>`wss://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api-ws/v1/realtime`（推荐）<br>或 `dashscope.aliyuncs.com`（兼容旧版，性能较低） | **协议差异化端点**：<br>• AOQ：`wss://.../api-ws/v1/realtime?model=xxx&x-dashscope-rtc-transport=moq`（需服务端 allocate 获取凭证）<br>• WebRTC：通过 `/api/v1/webrtc/realtime` 获取 SDP Offer/Answer<br>• WebSocket：同 Omni 端点，但请求头需带 `Authorization: Bearer <token>` |
| **鉴权方式** | HTTP Header `Authorization: Bearer <API_KEY>`（建连时一次性传递） | • **AOQ**：强约束服务端代理鉴权，客户端仅使用临时 `aoqTokenForClient`（**禁止 API Key 直连**）<br>• **WebRTC**：SDP 交换阶段完成 Token 鉴权<br>• **WebSocket**：Header `Authorization`（同 Omni，但需注意安全规范） |
| **VAD（语音活动检测）** | 内置双模式：<br>• `server_vad`（声学，通用）<br>• `semantic_vad`（语义，仅 `plus` 模型支持）<br>• 可精细调参（`threshold`, `silence_duration_ms`, `idle_timeout_ms`） | VAD 行为由模型与协议共同决定：<br>• Omni 系列模型继承 Omni 的 VAD 能力<br>• ASR/TTS 模型通常自带轻量 VAD，但**不开放语义级配置**<br>• WebRTC 协议层提供基础静音检测，但不可替代模型级 VAD |
| **工具调用（Function Calling）** | ✅ 原生支持：<br>• 定义 `tools` 后模型自主触发 `function_call`<br>• 客户端执行后回传 `function_call_output`<br>• **与 `enable_search` 互斥** | ✅ 支持（仅 Omni 系列模型），行为与 Omni Realtime 一致；其他模型（如纯 ASR/TTS）不支持 |
| **联网搜索** | ✅ 仅 `qwen3.5-omni-plus-realtime` 支持，通过 `enable_search: true` 开启，**与 `tools` 冲突** | ✅ 同 Omni Realtime（仅 plus 模型），规则一致 |
| **声音复刻（Voice Cloning）** | ✅ 原生集成：<br>• 需先调用 `qwen-voice-enrollment` 创建音色<br>• 在 `session.update` 中通过 `voice` 字段指定 ID | ⚠️ **不直接支持**：<br>• 声音复刻为独立能力，需单独调用 `qwen-voice-enrollment` API<br>• 复刻音色 ID 可在 Realtime API 的 `voice` 参数中复用（若模型支持该字段），但无统一 SDK 封装流程 |
| **计费方式** | 按 **实际音频输入时长（秒） + 文本 token 输出量** 计费<br>• 输入音频按采样率归一化为标准秒（如 16kHz PCM 1 秒 = 1 秒）<br>• 输出文本按 token 计费，音频按等效时长折算 | 按 **模型类型 + 使用时长/请求数/Token 量** 分层计费：<br>• Omni 全模态模型：同 Omni Realtime（音频秒 + token）<br>• ASR/TTS 模型：按音频输入/输出时长（秒）计费<br>• 翻译/对话模型：按会话时长或 token 量计费<br>• **AOQ/WebRTC 协议本身不额外计费**，费用归属模型调用 |
| **典型场景** | • 语音助手（智能音箱、车载语音）<br>• 实时客服坐席辅助（语音转写+意图理解+语音回复）<br>• 多模态交互应用（语音+图像联合分析，如“拍图问价”） | • 跨端实时应用（App/小程序/网页均需接入）<br>• 弱网环境音视频通信（AOQ 内置抗丢包/自适应码率）<br>• 专业语音处理流水线（ASR → NLU → TTS 独立编排）<br>• 浏览器内嵌实时对话（WebRTC 原生支持） |

---

## 适用场景建议

### 选择 **Omni Realtime API** 当：
- ✅ 业务聚焦于 **语音优先、多模态融合的智能助手类应用**（如家庭机器人、教育陪练、医疗问诊助手）；  
- ✅ 需要 **极致可控的交互状态机**（如精确管理音频缓冲、手动 commit、细粒度 VAD 调优、语义级中断恢复）；  
- ✅ 工程团队具备 WebSocket 事件驱动开发经验，且终端环境以 **App/小程序为主**（无需浏览器兼容）；  
- ✅ 要求 **开箱即用的声音复刻集成** 和 **统一的工具调用工作流**；  
- ❌ 不适用于需同时接入 ASR/TTS 独立模型，或必须运行在纯浏览器环境且拒绝 SDK 的场景。

### 选择 **Realtime API** 当：
- ✅ 需要 **一套 API 同时支撑 App（AOQ）、网页（WebRTC）、服务端（WebSocket）三端**，降低多端维护成本；  
- ✅ 业务涉及 **专业化语音处理链路**（例如：前端用 ASR 实时转写 → 后端做合规审核 → 再调用 TTS 合成反馈），需模型解耦；  
- ✅ 面向 **弱网、高抖动移动网络**，依赖 AOQ 的 QoS 保障（前向纠错、动态码率、硬件加速）；  
- ✅ 已有 **WebRTC 基础设施**（如自研音视频 SDK、SFU 架构），希望复用现有信令与媒体栈；  
- ❌ 不适用于需要 Omni 独有高级能力（如 `semantic_vad`、图像理解与语音的强耦合分析）且不愿自行封装协议逻辑的场景。

---

## 技术选型参考（给开发者的行动指南）

| 你的需求 | 推荐方案 | 关键理由 |
|----------|-----------|-----------|
| “我要做一个类似 Siri 的语音助手，支持说话时看图回答，还要能调用订餐 API” | **Omni Realtime API** | 唯一支持语音+图像联合理解、语义 VAD、[函数调用](../concepts/function-calling.md)一体化的方案；事件模型天然匹配助手交互范式。 |
| “我们的 App 需在地铁弱网下稳定语音客服，同时网页版也要有相同体验” | **Realtime API（AOQ + WebRTC）** | AOQ 专为弱网优化；WebRTC 保证网页零 SDK；同一模型（如 `qwen3.5-omni-flash-realtime`）双协议无缝切换。 |
| “我们是呼叫中心，需要把客户语音实时转文字（ASR），再送 NLP 分析，最后合成语音（TTS）播报” | **Realtime API（AOQ/WebSocket）** | ASR/TTS 模型仅 Realtime API 支持；可分阶段调用不同模型，避免 Omni 的能力绑定。 |
| “快速验证一个语音对话 MVP，用 Python Flask 后端 + HTML 前端” | **Realtime API（WebSocket）** | 无需集成 AOQ SDK 或处理 WebRTC SDP；DashScope SDK 一行代码接入，开发效率最高。 |
| “必须在浏览器中运行，且不能加载任何第三方 SDK（安全审计要求）” | **Realtime API（WebRTC）** | 原生浏览器 API，零外部依赖；Omni Realtime 的 WebSocket 事件模型需自行实现完整状态机，风险更高。 |
| “需要复刻销售总监的声音用于自动外呼，且与实时对话系统打通” | **Omni Realtime API** | 声音复刻 ID 可直接用于 `voice` 字段；Realtime API 需额外管理音色生命周期，无标准化集成路径。 |

> 💡 **终极建议**：  
> - **新项目起步**：优先评估 Omni Realtime API —— 若其能力覆盖核心场景，它将显著降低交互逻辑复杂度；  
> - **多端/混合模型/基础设施复用需求明确**：直接选用 Realtime API，利用其协议抽象获得长期架构弹性；  
> - **不确定时**：用 Realtime API 的 WebSocket 模式快速原型，再根据性能与功能瓶颈迁移至 Omni（同模型，协议升级即可）。  

---  
*本文档依据百炼平台 2024 年 Q3 最新文档（`api/omni-realtime-api.md`, `api/realtime-api-user-guide.md`）整理，参数与限制以控制台实时配置及最新 SDK 为准。*

## 被对比主题页

- [omni realtime api](../api/omni-realtime-api.md)
- [realtime api user guide](../api/realtime-api-user-guide.md)



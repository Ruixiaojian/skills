# 实时 API 方案对比：Realtime API 与 Omni Realtime API

本文旨在帮助开发者清晰理解百炼平台提供的两类核心实时交互方案——**Realtime API**（协议级多传输支持方案）与**Omni Realtime API**（基于 WebSocket 的标准化全模态接口），明确其设计定位、能力边界与适用约束，从而在实际项目中做出高效、稳健的技术选型。随着智能语音助手、实时翻译、多模态客服等场景对低延迟、高鲁棒性、易集成性的要求日益提升，选择匹配终端生态、网络条件与开发资源的 API 方案，已成为影响交付周期与用户体验的关键决策点。

## 关键维度对比

| 维度 | Realtime API | Omni Realtime API |
|------|--------------|-------------------|
| **本质定位** | 协议抽象层：提供 **WebSocket / WebRTC / AOQ 三协议统一接入框架**，面向底层协议控制与跨端深度定制 | 接口标准化层：基于 **WebSocket 的开箱即用全模态实时 API**，聚焦业务逻辑快速对接，屏蔽协议细节 |
| **输入格式** | • 音频：PCM（16 kHz，单声道）<br>• 图像：仅 WebRTC & WebSocket 支持（`multimodal-dialog` 套件），需自行编码/传输<br>• 文本：JSON 消息体中 `input.text` 字段 | • 音频：PCM（16 kHz，单声道）<br>• 图像：JPG/JPEG（≤1080p，Base64 编码后 ≤256KB），通过 `input.image` 字段提交<br>• 文本：`input.text` 字段，支持多轮上下文自动维护 |
| **输出格式** | • 文本流：按 `text.delta` 事件分片推送<br>• 音频流：PCM（24 kHz），按 `audio.delta` 事件分片推送<br>• 多模态事件结构因协议而异（如 AOQ 使用二进制帧，WebRTC 使用 DataChannel） | • 统一 JSON 结构：<br> – `text.delta`（文本增量）<br> – `audio.delta`（PCM 音频 Base64 片段）<br> – `tool_calls` / `search_results` 等结构化响应字段<br>• 输出严格遵循 `modalities: ["text", "audio"]` 或 `["text"]` 配置 |
| **支持模型** | • 全模态模型：<br> `qwen3.5-omni-plus-realtime`, `qwen3.5-omni-flash-realtime`, `qwen3.5-livetranslate-flash-realtime`（AOQ/WebRTC 支持）<br>• 纯语音模型：<br> `Fun-ASR`, `CosyVoice`, `qwen-audio-3.0-realtime-plus`（**仅 WebSocket 支持**）<br>• 多模态套件：<br> `multimodal-dialog`（**WebRTC & WebSocket 支持，AOQ 不支持**） | • 仅支持 Qwen-Omni 系列实时模型：<br> `qwen3.5-omni-realtime`（含语义 VAD/工具调用/搜索）<br> `qwen3.5-omni-plus-realtime` / `qwen3.5-omni-flash-realtime`（含 server_vad/超时引导）<br> `qwen-omni-turbo-realtime`（极致低延迟，参数不可调）<br>• **不支持纯语音模型（如 Fun-ASR）或 `multimodal-dialog` 套件** |
| **API 端点与连接方式** | • **AOQ**：需 AppServer 调用网关获取 `aoqTokenForClient`，客户端 SDK 连接专用 AOQ 网关；仅支持 Android/iOS/HarmonyOS 原生应用<br>• **WebRTC**：AppServer 代理 SDP 协商，浏览器原生 `RTCPeerConnection`；需处理 DataChannel 与媒体轨道生命周期<br>• **WebSocket**：标准 WebSocket 连接，URL 含 `?model=` 参数；适用于服务端集成或调试 | • 统一 WebSocket 端点：<br> `wss://{WorkspaceId}.{region}.maas.aliyuncs.com/api-ws/v1/realtime`<br>• 无需 SDP 协商或 [Token](../concepts/token.md) 中转，直接携带 `Authorization` Header 连接<br>• **全平台兼容**：Web 浏览器、Node.js、移动端 WebView、原生 App（通过标准 WebSocket 库）均可直接接入 |
| **计费方式** | • 按 **实际音频时长（秒） + 文本 token 数** 双维度计费<br>• 不同协议下模型单价一致，但 AOQ/WebRTC 因传输效率更高，同等体验下可降低有效音频时长消耗<br>• `multimodal-dialog` 套件单独计费，按会话时长与图像调用次数叠加 | • 按 **音频时长（秒） + 输出文本 token 数** 计费<br>• 图像输入 **不额外计费**（已包含在会话基础费用中）<br>• 工具调用、联网搜索、声音复刻等高级功能 **不产生额外 API 调用费用**（计入主会话） |
| **典型场景** | • 对弱网/高丢包容忍度要求极高的车载、IoT 设备交互<br>• 需深度定制音视频采集/渲染链路的 AR/VR 应用<br>• 多模态套件驱动的复杂人机协作（如远程专家指导系统）<br>• 原生 App 内嵌高保真语音助手（AOQ 专属优势） | • 快速上线 Web/小程序智能客服、语音助手<br>• 需要稳定多模态（语音+图片）输入的教育问答、医疗问诊场景<br>• 对开发效率敏感、无协议层定制需求的 SaaS 产品集成<br>• 要求开箱即用语义 VAD、工具调用、联网搜索能力的对话系统 |

## 适用场景建议

### ✅ 选择 **Realtime API** 当：
- 你的应用是 **原生移动 App（Android/iOS/HarmonyOS）**，且对首字延迟、抗弱网能力有严苛要求（如车载导航、工业巡检设备），可利用 AOQ 协议获得最低端到端延迟（<300ms）；
- 你需要 **完全接管音视频采集与播放逻辑**（例如接入第三方 TTS 引擎、屏幕录制流、自定义降噪模块），AOQ 提供 `injectAudioStream` / `injectVideoStream` 等底层控制能力；
- 业务涉及 **专业多模态协作**，需使用 `multimodal-dialog` 套件实现手势标注、白板协同、3D 模型交互等高级能力；
- 你已有成熟的 WebRTC 基础设施，并希望复用现有信令与媒体服务器架构。

### ✅ 选择 **Omni Realtime API** 当：
- 你的目标平台是 **Web 浏览器、微信小程序、Flutter/React Native 跨端应用**，追求“一行代码接入、零协议适配”；
- 你需要 **快速验证多模态能力**（如用户拍照提问 + 语音追问），且不愿自行实现图像编解码、VAD 判断、音频流拼接等工程模块；
- 业务逻辑依赖 **语义级语音活动检测（semantic_vad）、工具[函数调用](../concepts/function-calling.md)（Function Calling）或联网搜索**，且希望这些能力由服务端统一保障一致性；
- 团队以业务开发为主，**缺乏音视频协议栈经验**，希望将技术风险收敛至百炼标准化接口。

## 技术选型参考指南

| 选型考量因素 | 推荐方案 | 说明 |
|--------------|----------|------|
| **开发周期紧迫（<2 周上线 MVP）** | Omni Realtime API | 无需协议协商、无 SDK 集成门槛、文档示例完备，Python/JS/Java SDK 开箱即用 |
| **终端为 iOS/Android 原生 App，且需极致低延迟** | Realtime API（AOQ） | AOQ 在 4G/弱 Wi-Fi 下平均延迟比 WebSocket 低 35%~50%，并内置 QUIC 重传优化 |
| **需支持浏览器端实时交互（无后端代理）** | Omni Realtime API | Realtime API 的 WebRTC 方案强制要求后端代理 SDP，而 Omni Realtime API 直连 WebSocket 无此限制 |
| **必须使用 Fun-ASR/CosyVoice 等专用语音模型** | Realtime API（WebSocket） | Omni Realtime API 仅绑定 Qwen-Omni 系列模型，不开放 ASR/TTS 模型替换 |
| **计划集成声音复刻、多图理解、搜索溯源等高级能力** | Omni Realtime API | 声音复刻 ID 可直传 `voice` 参数；图像输入自动触发多模态理解；`enable_search` 返回结构化来源信息，均无需额外开发 |
| **已有 WebRTC 基础设施，需复用信令与媒体服务器** | Realtime API（WebRTC） | 可无缝对接现有 SFU/MCU 架构，复用带宽管理与 QoS 策略 |

> ⚠️ **重要提醒**：  
> - 若选用 Realtime API，请务必以 [Realtime API简介](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-overview.md) 中的协议支持矩阵为准，避免因文档片段差异导致误用（如 AOQ 不支持 `multimodal-dialog`）；  
> - Omni Realtime API 的 `qwen-omni-turbo-realtime` 模型虽延迟最低，但**所有生成参数不可配置**，适用于对确定性响应风格无要求的高频轻量交互场景；  
> - 两类方案均**禁止在前端硬编码 API Key**，生产环境必须通过业务后端代理鉴权请求。

## 被对比主题页

- [realtime api user guide](../api/realtime-api-user-guide.md)
- [omni realtime api](../api/omni-realtime-api.md)



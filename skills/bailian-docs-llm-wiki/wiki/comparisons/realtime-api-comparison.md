# 实时API方案对比：Omni Realtime vs Realtime User Guide

## 对比目的与背景

为帮助开发者在百炼平台快速、准确地选型实时多模态交互能力，本文对两类核心实时API方案进行系统性对比：  
- **Omni Realtime API**（`api/omni-realtime-api.md`）：面向**端到端语音助手类场景**的专用 WebSocket 接口，强调低延迟、事件驱动、强会话控制与多模态协同；  
- **Realtime API User Guide**（`api/realtime-api-user-guide.md`）：面向**全链路实时通信基础设施**的协议级能力指南，覆盖 AOQ、WebRTC、WebSocket 三种传输协议，聚焦**协议适配性、平台兼容性与部署灵活性**。

二者并非简单替代关系，而是**垂直能力层（Omni）与水平协议层（Realtime）的协同关系**：Omni Realtime 是基于 Realtime API 协议栈（尤其是 WebSocket）构建的、预封装了 Qwen-Omni 系列模型能力的**开箱即用方案**；而 Realtime User Guide 则是支撑包括 Omni 在内的所有实时模型服务的**底层通信框架规范与接入方法论**。本对比旨在厘清边界、明确分工，避免技术误用与重复集成。

---

## 关键维度对比表

| 维度 | Omni Realtime API | Realtime API User Guide |
|------|-------------------|--------------------------|
| **定位与本质** | 面向 Qwen-Omni 系列模型的**专用会话式 WebSocket SDK 接口**，提供标准化事件流与语义化控制原语 | 百炼平台统一的**实时通信能力抽象层**，定义 AOQ/WebRTC/WebSocket 三协议接入规范与通用配置模型 |
| **输入格式** | • 音频：16 kHz PCM（Base64 编码）<br>• 图像：JPG/JPEG（≤1080p，Base64 编码）<br>• 事件驱动：`input_audio_buffer.append`、`input_image_buffer.append` 等结构化客户端事件 | • 协议无关：AOQ/WebRTC 原生传输原始音视频帧（Opus/H.264等），WebSocket 同 Omni<br>• 输入模态由所选模型决定（如 Fun-ASR 仅音频，CosyVoice 仅文本→音频） |
| **输出格式** | • 固定结构化服务端事件流（如 `response.text.delta`, `response.audio.delta`, `conversation.item.input_audio_transcription.delta`）<br>• 音频输出：24 kHz PCM（Base64） | • 输出模态由 `modalities` 参数声明（如 `["text","audio"]`），但**具体事件格式与字段取决于所用模型**<br>• AOQ/WebRTC 支持原生媒体流直出（无需 Base64 解包），WebSocket 同 Omni |
| **支持模型** | 仅限 Qwen-Omni 系列实时模型：<br>• `qwen3.5-omni-realtime`（plus/flash）<br>• `qwen3-omni-flash-realtime`<br>• `qwen-omni-turbo-realtime` | 全量支持百炼实时模型生态：<br>✅ Qwen-Omni 系列（全协议）<br>✅ `multimodal-dialog`（WebRTC/WebSocket）<br>✅ Fun-ASR / CosyVoice / `qwen-audio-3.0-realtime-plus`（仅 WebSocket） |
| **API 端点** | 固定 WebSocket 地址：<br>`wss://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api-ws/v1/realtime` | 协议差异化端点：<br>• AOQ：`wss://aoq.{Region}.maas.aliyuncs.com/v1/realtime`（需 `aoqTokenForClient`）<br>• WebRTC：`POST https://api.{Region}.maas.aliyuncs.com/api/v1/webrtc/realtime?model=xxx`（SDP 交换）<br>• WebSocket：同 Omni Realtime 端点（但可接入更多模型） |
| **计费方式** | 按 **实际调用的 Qwen-Omni 模型实例 + 使用时长（秒） + 输出 token/音频时长** 计费；图像输入不额外计费；工具调用/联网搜索按次计费 | 计费粒度与所选模型强绑定：<br>• Qwen-Omni 类：同 Omni Realtime<br>• Fun-ASR/CosyVoice：按音频时长（秒）或识别/合成请求数计费<br>• 多模态开发套件：按会话时长 + 资源消耗综合计费 |
| **典型场景** | • 智能语音助手（带 VAD 的连续对话）<br>• 多模态客服机器人（语音+图片联合理解）<br>• 实时语音转写+AI应答一体化终端 | • 移动端 App（弱网高可用）→ 选 AOQ<br>• 浏览器网页应用（免插件）→ 选 WebRTC<br>• 服务端批量处理/原型验证 → 选 WebSocket<br>• 专业语音识别/合成独立服务 → 选对应模型 + WebSocket |
| **VAD 支持** | 提供双模式：<br>• `server_vad`（声学检测，全模型支持）<br>• `semantic_vad`（语义级停顿判断，仅 `qwen3.5-omni-realtime` 系列支持） | 统一配置 `turn_detection`，但语义 VAD 能力**依赖后端模型支持**；AOQ/WebRTC 协议本身不提供 VAD，由模型服务实现 |
| **高级功能** | • 工具调用（Function Calling）<br>• 联网搜索（`enable_search`）<br>• 声音复刻（需预创建音色 ID）<br>• `smooth_output` 风格切换（仅 flash 系列） | • 功能由所选模型决定：<br>  - 工具调用/搜索：仅 Qwen-Omni 系列支持<br>  - 声音复刻：需配合 Omni Realtime 或独立 Voice Cloning API<br>  - AOQ/WebRTC 支持自定义音视频注入（如 TTS 输出直推、AI 视频帧渲染） |
| **SDK 依赖** | Python SDK ≥ v1.25.17，Java SDK ≥ v2.22.15；提供 `update_session`、`append_audio` 等高层封装方法 | • AOQ：专用 AOQ SDK + Opus 插件<br>• WebRTC：浏览器原生 API 或标准库<br>• WebSocket：DashScope SDK 或任意 WebSocket 客户端 |

---

## 适用场景建议

### ✅ 选择 **Omni Realtime API** 当：
- 业务目标是快速上线一个**具备语音输入、实时转写、AI应答、TTS播报、图片理解能力的智能助手**；
- 技术栈以服务端或 Electron/桌面应用为主，**无需深度定制传输协议**；
- 需要开箱即用的 `semantic_vad`、工具调用、声音复刻等高级语义能力；
- 开发团队希望**最小化协议细节处理**，专注业务逻辑与会话状态管理。

> ⚠️ 注意：若需接入非 Qwen-Omni 模型（如纯 ASR 或 CosyVoice），Omni Realtime 不适用。

### ✅ 选择 **Realtime API User Guide（协议层）** 当：
- 需要**跨平台兼容性**：iOS/Android/HarmonyOS App（AOQ）、Web 浏览器（WebRTC）、服务端（WebSocket）；
- 对**弱网稳定性、端到端延迟、媒体流控制精度**有极致要求（如远程医疗问诊、实时教育互动）；
- 已有 WebRTC 基础设施或需要将 AI 能力嵌入现有音视频 SDK；
- 需要**混合使用多种实时模型**（例如：前端用 Fun-ASR 做语音识别，后端用 Qwen-Omni 做多模态推理）；
- 要求**完全掌控媒体流生命周期**（如外部 TTS 引擎输出直推、AI 生成画面帧注入、混音处理）。

> ⚠️ 注意：直接使用 Realtime User Guide 需自行实现会话状态机、事件解析、错误重试等逻辑，开发成本高于 Omni Realtime。

---

## 技术选型参考（面向开发者）

| 选型决策点 | 推荐方案 | 理由 |
|------------|-----------|------|
| **首次集成实时语音助手？** | 👉 Omni Realtime API | 少量代码即可完成“语音输入→实时转写→AI思考→TTS播报”闭环，文档示例丰富，SDK 封装成熟。 |
| **已用 WebRTC 构建音视频会议系统？** | 👉 Realtime API + WebRTC 协议 | 复用现有信令与媒体管道，只需对接 `/webrtc/realtime` Endpoint，避免协议迁移成本。 |
| **开发 iOS/Android 原生 App，要求离线降级与弱网抗丢包？** | 👉 Realtime API + AOQ 协议 | AOQ 基于 QUIC，天然支持 0-RTT 连接、前向纠错、自适应码率，远优于 WebSocket 在移动网络的表现。 |
| **需同时调用 ASR + TTS + 多模态大模型？** | 👉 Realtime API（分协议接入） | ASR/CosyVoice 用 WebSocket，Qwen-Omni 用 WebSocket 或 AOQ，统一鉴权与监控，灵活组合。 |
| **定制化需求强：如外接硬件麦克风、自研语音前端、AI视频生成直推？** | 👉 Realtime API + 自定义音视频流（AOQ/WebRTC） | `pushAudioExternalStreamData()` / `pushExternalVideoCapturedFrame()` 提供底层帧级控制权。 |
| **预算敏感，仅需文本问答+基础语音播报？** | 👉 Omni Realtime API（`qwen-omni-turbo-realtime`） | Turbo 版本成本最低，支持 `["text","audio"]`，且无需配置复杂参数（采样参数锁定）。 |

> 💡 **最佳实践提示**：  
> - **Omni Realtime 是 Realtime API 的“超级子集”**——它默认启用 WebSocket 协议，并预置了 Qwen-Omni 模型的最佳实践配置；  
> - 若未来需扩展至 AOQ/WebRTC，可**平滑升级**：复用相同 `session.update` 参数、事件命名与错误模型，仅替换连接方式与 SDK；  
> - 所有方案均强制要求 **API Key 服务端托管**，禁止客户端硬编码；AOQ 场景必须通过 `aoqTokenForClient` 实现安全凭证分发。

---  
*最后更新：2024年10月*

## 被对比主题页

- [omni realtime api](../api/omni-realtime-api.md)
- [realtime api user guide](../api/realtime-api-user-guide.md)



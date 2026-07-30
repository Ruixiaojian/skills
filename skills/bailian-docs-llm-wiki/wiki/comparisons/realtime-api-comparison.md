# 实时 API 方案对比：Omni Realtime API vs Realtime API User Guide

本对比旨在帮助开发者清晰区分百炼平台两大实时交互技术路径——**Omni Realtime API**（面向[多模态](../concepts/multi-modal.md)对话的专用 WebSocket 接口）与 **Realtime API User Guide**（面向全场景、多协议的实时能力框架），避免因概念混淆导致接入失败、功能缺失或体验降级。二者定位不同：前者是**模型驱动的标准化实时会话协议**，后者是**基础设施层的协议抽象与接入规范体系**。理解其差异对技术选型、架构设计及长期维护至关重要。

## 关键维度对比

| 维度 | Omni Realtime API | Realtime API User Guide |
|------|-------------------|--------------------------|
| **本质定位** | 一个**具体、开箱即用的 WebSocket 实时会话 API**，深度绑定 `qwen-omni-*` 系列[多模态](../concepts/multi-modal.md)模型，提供事件驱动的端到端交互语义。 | 一套**跨协议的实时能力接入指南与规范集合**，涵盖 AOQ、WebRTC、WebSocket 三种传输层，并定义通用会话控制逻辑、鉴权机制与状态管理范式。 |
| **输入格式** | 严格基于 WebSocket 事件流：<br>• `input_audio_buffer.append`（PCM 音频，16 kHz）<br>• `input_image`（JPG/JPEG，≤1080p，Base64 编码 ≤256 KB）<br>• `session.update`（JSON 配置更新） | 协议相关：<br>• **AOQ**：原生 PCM 音频帧（10ms/帧）、I420/NV12/BGRA 视频帧或 JPEG；支持外部采集/播放流注入<br>• **WebRTC**：标准 MediaStream 或 encoded track<br>• **WebSocket**：与 Omni Realtime API 兼容的相同事件格式（如 `input_audio_buffer.append`），但需自行实现连接与状态管理 |
| **输出格式** | 固定事件流：<br>• `response.text.delta`（流式文本）<br>• `response.audio.delta`（24 kHz PCM 音频流）<br>• `response.audio_transcript.delta`（ASR 中间结果）<br>• `input_audio_buffer.speech_stopped`（VAD 结束） | 协议相关：<br>• **AOQ/WebRTC**：解码后 PCM 音频（24 kHz）、文本事件（通过 SDK 回调或 DataChannel）<br>• **WebSocket**：同 Omni Realtime API 的服务端事件格式<br>• **所有协议** 均支持 `modalities: ["text"]` 或 `["text","audio"]` 输出组合 |
| **支持模型** | **仅限 `qwen-omni-*` 系列模型**：<br>• `qwen3.5-omni-realtime`（plus/flash）<br>• `qwen3-omni-flash-realtime`<br>• `qwen-omni-turbo-realtime`<br>（不支持 Fun-ASR、CosyVoice、qwen-audio-3.0 等语音专项模型） | **按协议分层支持**：<br>• `qwen3.5-omni-*`：三协议均支持<br>• `multimodal-dialog`：仅 WebRTC / WebSocket<br>• Fun-ASR / CosyVoice / `qwen-audio-3.0-realtime-plus`：**仅 WebSocket**<br>• `qwen3.5-livetranslate-flash-realtime`：三协议均支持 |
| **API 端点** | 固定 WebSocket URL：<br>`wss://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api-ws/v1/realtime`<br>（需替换 `{WorkspaceId}`） | **无统一端点**：<br>• **AOQ**：由网关动态分配 Relay 接入点（`relayEndpoints`）+ TLS 证书校验（`certFingerprint`）<br>• **WebRTC**：通过 SDP 交换协商 ICE 候选者，无固定地址<br>• **WebSocket**：与 Omni Realtime API **共用同一 URL**，但需按 Realtime API 规范组织消息（如 `session.create` 代替 `session.created` 初始化） |
| **计费方式** | 按 **实际消耗的 token 数 + 音频处理时长（秒）** 计费：<br>• 输入 token（文本/ASR 后文本）<br>• 输出 token（LLM 生成）<br>• 音频流时长（从 `response.audio.start` 到 `response.audio.done`）<br>• 图像输入按分辨率阶梯计费 | 按 **所选模型 + 协议 + 资源类型** 分项计费：<br>• AOQ/WebRTC：按「会话时长（分钟）」+「媒体转发流量（GB）」+「模型调用（token/音频秒）」<br>• WebSocket：同 Omni Realtime API 计费模型<br>• Fun-ASR/CosyVoice 等独立模型按自身单位计费（如 ASR 按音频秒、TTS 按字符） |
| **典型场景** | • 高互动性语音助手（需低延迟 VAD + 流式 TTS）<br>• [多模态](../concepts/multi-modal.md)客服机器人（语音+图像联合理解）<br>• 需精细控制 `temperature`/`tools`/`enable_search` 的专业对话应用<br>• 快速原型验证（Python SDK 开箱即用） | • 移动端原生 App（Android/iOS/HarmonyOS）——首选 **AOQ**（弱网鲁棒、内置 3A）<br>• 浏览器端实时互动（如在线教育、远程协作）——首选 **WebRTC**<br>• 服务端集成、IoT 设备或已有 WebSocket 基础设施——选用 **WebSocket**<br>• 需要复用 Fun-ASR/CosyVoice 等语音专项能力的场景——必须用 **WebSocket** |

## 各方案适用场景建议

### ✅ 选择 **Omni Realtime API** 当：
- 你的核心需求是 **基于 `qwen-omni-*` 模型的端到端多模态对话**（语音+图像→文本+音频），且希望快速上线；
- 你已确定使用 WebSocket 协议，无需弱网对抗、3A 处理或自定义音视频管线；
- 你需要细粒度控制 LLM 采样参数（`temperature`/`top_p`）、工具调用（`tools`）或联网搜索（`enable_search`）；
- 你正在构建智能硬件、桌面客户端或服务端代理，对协议栈轻量性要求高；
- 你接受“模型-协议强绑定”，不计划切换至 Fun-ASR 或 CosyVoice 等垂直模型。

### ✅ 选择 **Realtime API User Guide（按协议选型）** 当：
- **移动端原生 App**：必须选 **AOQ** —— 它提供网络自适应、抗丢包、回声消除等工业级音视频保障，是百炼推荐的移动最优解；
- **浏览器/Web 应用**：优先选 **WebRTC** —— 免 SDK、免部署信令服务器，利用浏览器原生能力实现低延迟互动；
- **服务端/边缘设备/IoT**：选 **WebSocket** —— 与 Omni Realtime API 兼容，但需遵循 Realtime API 的会话生命周期规范（如显式 `session.create`）；
- **需要混合能力**：例如先用 Fun-ASR 做高精度语音识别，再将文本送入 `qwen-omni` 做推理 —— 此类编排必须通过 **WebSocket 协议分别调用不同模型**；
- **未来可能扩展协议**：如从 Web 端迁移到 App 端，采用 Realtime API 规范可最大程度复用业务逻辑（如 `turn_detection` 配置、`modalities` 控制）。

## 技术选型参考（致开发者）

| 你的问题 | 推荐答案 | 说明 |
|----------|-----------|------|
| **我只想快速跑通一个语音助手 Demo，用 Python 写** | → Omni Realtime API + Python SDK | 最少代码、最短路径，SDK 封装了连接、重连、事件解析，专注业务逻辑 |
| **我要开发一款 iOS 语音社交 App，用户常在地铁/电梯里使用** | → Realtime API + AOQ 协议 | AOQ 是唯一提供弱网对抗和 3A 的协议，直接决定用户体验下限 |
| **我在做跨境会议系统，需实时翻译+字幕+发言人检测** | → Realtime API + WebRTC（浏览器端）或 AOQ（App 端） + `qwen3.5-livetranslate-flash-realtime` | WebRTC/AOQ 提供稳定媒体通道，`livetranslate` 模型专为多语种实时转译优化 |
| **我的后端服务要对接百炼，但已有成熟的 WebSocket 连接池** | → Realtime API + WebSocket 协议 | 复用现有基础设施，但需严格遵循 `session.create` → `session.updated` → `input_audio_buffer.append` 的状态机流程 |
| **我需要把用户上传的图片 + 语音一起分析，并调用天气 API 工具** | → Omni Realtime API（`qwen3.5-omni-plus-realtime` + `tools`） | 仅此方案同时支持图像输入、工具调用、`semantic_vad` 精准断句，且无需协议适配 |
| **我正在替换旧版语音合成服务，只想要高质量 TTS，不要 LLM** | → Realtime API + WebSocket + `cosyvoice-*` 模型 | Omni Realtime API **不支持** CosyVoice，必须走 Realtime API 的 WebSocket 路径 |

> ⚠️ **重要提醒**：  
> - **Omni Realtime API 是 Realtime API User Guide 在 WebSocket 协议下的一个特化子集**，二者非并列关系，而是“实例 vs 规范”的关系。  
> - 若使用 WebSocket，**Omni Realtime API 的事件格式与 Realtime API 的 WebSocket 规范高度一致**，但初始化流程（`session.created` 自动触发 vs `session.create` 显式发送）、错误重试策略、部分高级参数（如 `idle_timeout_ms`）的支持范围存在差异，务必以对应文档为准。  
> - 所有协议均要求 `workspaceId` 鉴权，AOQ 额外强制使用网关下发的临时 `aoqTokenForClient`，切勿混用 API Key。  

请根据**目标平台、核心模型需求、音视频质量要求、工程成熟度**四要素综合决策。如不确定，建议从 Omni Realtime API 快速验证模型能力，再按 Realtime API User Guide 迁移至生产协议（AOQ/WebRTC）。

## 被对比主题页

- [omni realtime api](../api/omni-realtime-api.md)
- [realtime api user guide](../api/realtime-api-user-guide.md)



# 实时 API 方案对比：Omni Realtime API 与 Realtime API

本文旨在帮助开发者清晰理解百炼平台两类核心实时 API 的定位差异与能力边界，辅助技术选型决策。随着[多模态](../concepts/multi-modal.md)实时交互需求激增（如语音助手、智能座舱、远程协作、AI 教育等），平台提供了两种互补但设计哲学迥异的实时通信方案：**Omni Realtime API**（专注极致低延迟、强交互控制的 WebSocket 原生协议）与 **Realtime API**（面向全场景、多协议融合的统一实时能力框架）。二者并非简单替代关系，而是在架构层级、适用终端、扩展能力和运维复杂度上形成明确分工。本对比聚焦关键维度，提供客观、可落地的技术参考。

## 关键维度对比

| 维度 | Omni Realtime API | Realtime API |
|------|-------------------|--------------|
| **协议与传输层** | 仅支持 WebSocket（`wss://.../api-ws/v1/realtime`） | 支持三协议：AOQ（移动端原生）、WebRTC（浏览器/跨平台）、WebSocket（服务端/原型验证） |
| **输入格式** | PCM 音频（16 kHz）、Base64 编码 JPG/JPEG 图像（≤1080p，≤256 KB）；通过结构化事件（如 `input_audio_buffer.append`）流式提交 | 同 Omni（音频/图像），但协议层抽象更统一：AOQ/WebRTC 自动处理音视频采集与编码，WebSocket 需手动构造事件；支持自定义外部音视频流（AOQ 特有） |
| **输出格式** | 文本（`response.text.delta`） + 同步音频（`response.audio.delta`，24 kHz PCM）；固定模态组合 `["text"]` 或 `["text","audio"]` | 输出模态同 Omni；AOQ/WebRTC 可直接输出解码后 PCM 音频帧或渲染视频帧，WebSocket 仍以事件流形式返回 |
| **支持模型** | 仅支持 `qwen3.5-omni-*`、`qwen3-omni-flash-*`、`qwen-omni-turbo-*` 等 Omni 系列实时模型；不支持 Fun-ASR、CosyVoice、`qwen-audio-3.0` 等专项模型 | 支持全系实时模型：<br>• Omni 全系列（`qwen3.5-omni-plus-realtime` 等）<br>• 实时语音识别（Fun-ASR）<br>• 实时语音合成（CosyVoice）<br>• 实时语音对话（`qwen-audio-3.0-realtime-plus`）<br>• [多模态](../concepts/multi-modal.md)对话套件（`multimodal-dialog`）<br>※ 注意：部分模型仅限特定协议（如 Fun-ASR/CosyVoice 仅 WebSocket；`multimodal-dialog` 不支持 AOQ） |
| **API 端点** | 单一 WebSocket 端点：`wss://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api-ws/v1/realtime` | 多端点：<br>• AOQ：通过网关获取 Relay 接入点（`relayEndpoints`）+ `aoqTokenForClient`<br>• WebRTC：信令服务器地址（用于 SDP/ICE 交换）<br>• WebSocket：同 Omni 端点（但鉴权方式不同） |
| **计费方式** | 按调用时长（秒）+ 输出 token 数 + 输出音频时长（秒）计费；Omni 系列模型独立定价 | 按所选模型及协议分项计费：<br>• AOQ/WebRTC：按连接时长（分钟）+ 模型调用时长（秒）计费<br>• WebSocket：按模型调用时长（秒）+ token/音频时长计费<br>※ AOQ 协议含弱网优化与 3A 处理成本，单价通常高于 WebSocket |
| **典型场景** | • 对端到端延迟极度敏感的语音助手（目标 <300ms RTT）<br>• 需精细控制 VAD 行为与会话状态的客服机器人<br>• 客户端主导节奏的主动引导式交互（如教学问答） | • 移动端 App（Android/iOS/HarmonyOS）需强弱网对抗与内置 3A<br>• 浏览器端实时互动（如在线会议 AI 助手、网页版语音搜索）<br>• 服务端快速集成或 A/B 测试（WebSocket 快速验证）<br>• 需混合使用 ASR/TTS/LLM 的复合流水线（如实时字幕+翻译+应答） |
| **客户端控制粒度** | 极高：事件驱动（`session.update`, `input_audio_buffer.append`, `response.audio.delta`），支持手动 VAD 控制、参数动态调整（除 turbo 模型外）、主动引导（`idle_timeout_ms`） | 分层抽象：AOQ 提供 SDK 级控制（媒体流启停、外部流注入、状态机监听）；WebRTC 依赖标准 Web API；WebSocket 控制粒度与 Omni 接近，但缺乏 AOQ 特有功能（如自定义音频播放回调） |
| **平台兼容性** | 无平台限制（任何支持 WebSocket 的环境均可接入），但需自行实现音频采集/播放、VAD、网络重连等逻辑 | • AOQ：仅限移动端原生（Android/iOS/HarmonyOS）<br>• WebRTC：主流浏览器（Chrome/Firefox/Safari）及支持 `aiortc` 的服务端<br>• WebSocket：全平台通用 |
| **运维与调试复杂度** | 中等：需维护 WebSocket 连接生命周期、事件解析、音频编解码、VAD 适配；Python SDK 提供封装，但底层逻辑透明 | • AOQ：高（需集成 SDK、Opus 插件、处理 Relay 连接、状态机管理）<br>• WebRTC：中（SDP/ICE 协商、NAT 穿透调试）<br>• WebSocket：低（与 Omni 接近，SDK 封装完善） |

## 适用场景建议

### 选择 Omni Realtime API 当：
- 你的应用运行在**服务端环境**（如 Node.js 后端、Python 微服务）或**轻量级客户端**（如 Electron、小程序 WebView），且已具备成熟的音频采集/播放能力；
- 核心诉求是**确定性低延迟**与**完全可控的交互流程**（例如：严格按用户语句分段生成、静默超时后主动追问、动态调节 temperature 控制响应风格）；
- 业务模型明确限定为 `qwen3.5-omni-*` 系列，无需接入 Fun-ASR、CosyVoice 等专项能力；
- 团队熟悉 WebSocket 开发，愿意承担音频流管理、事件解析、连接保活等基础工作。

### 选择 Realtime API 当：
- 目标平台是**移动端原生 App**，且对弱网（地铁、电梯、偏远地区）下的语音连续性、回声消除、降噪有硬性要求 → **首选 AOQ 协议**；
- 应用部署在**浏览器环境**（如 SaaS 管理后台、教育平台网页端），需开箱即用的实时语音交互 → **首选 WebRTC 协议**；
- 需要构建**混合能力流水线**（例如：前端用 WebRTC 采集语音 → 后端用 WebSocket 调用 Fun-ASR + Omni LLM + CosyVoice 合成 → 返回音频流）→ **利用 Realtime API 的协议互通性与模型广度**；
- 处于**快速原型验证阶段**，希望最小成本验证[多模态](../concepts/multi-modal.md)实时效果 → **选用 WebSocket 协议，复用 Omni 的事件模型与 SDK**；
- 业务涉及**非 Omni 系列模型**（如纯语音识别、专业 TTS 音色、轻量级对话套件），则 Realtime API 是唯一选择。

## 技术选型参考指南（面向开发者）

1. **先定平台，再选协议**：  
   - 移动端原生 → AOQ（强弱网/3A）；  
   - 浏览器 → WebRTC（免 SDK/标准兼容）；  
   - 服务端/跨平台 → WebSocket（低门槛/高可控）。

2. **再看模型需求**：  
   - 若只需 Omni 系列模型，且追求极致控制，Omni Realtime API 与 Realtime API 的 WebSocket 协议能力高度重合，可任选；  
   - 若需 Fun-ASR/CosyVoice/`multimodal-dialog` 等模型，**必须选 Realtime API**，并根据平台匹配协议。

3. **评估工程投入**：  
   - 使用 AOQ/WebRTC 需接受更高集成成本（SDK、证书、状态机、自定义流）；  
   - Omni Realtime API 和 Realtime API 的 WebSocket 模式开发体验接近，但 Omni 文档更聚焦单一路径，Realtime API 文档覆盖更广协议细节。

4. **关注长期演进**：  
   - Omni Realtime API 是 Omni 模型的“专属通道”，功能迭代紧密耦合模型升级（如新 VAD 类型、工具调用增强）；  
   - Realtime API 是平台级“实时能力中枢”，未来将统一纳管更多模态模型与协议（如未来支持 QUIC、SRT），适合构建长期稳定的实时基础设施。

> ⚠️ **重要提醒**：避免常见误用——  
> - 不要在 AOQ 协议下尝试调用 Fun-ASR 模型（会失败）；  
> - 不要在 WebSocket 下使用 `qwen-omni-turbo-realtime` 并试图修改 `temperature`（参数被忽略）；  
> - AOQ 的 `token` 必须使用网关返回的 `aoqTokenForClient`，不可直接使用 API Key；  
> - 所有方案均要求 `input_audio_format="pcm"`（16 kHz）与 `output_audio_format="pcm"`（24 kHz），务必校验采样率匹配。

## 被对比主题页

- [omni realtime api](../api/omni-realtime-api.md)
- [realtime api user guide](../api/realtime-api-user-guide.md)



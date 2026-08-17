# 实时 API 方案对比：Realtime API 与 Omni Realtime API

为帮助开发者在构建低延迟、[多模态](../concepts/multi-modal.md) AI 实时交互应用（如智能语音助手、实时会议翻译、虚拟客服等）时做出高效、可靠的技术选型，本文对百炼平台当前两大核心实时接口方案——**Realtime API** 与 **Omni Realtime API**——进行系统性对比分析。二者虽同属“实时”范畴，但在协议设计、能力边界、集成复杂度及适用场景上存在显著差异。本对比基于最新文档规范（2024年Q3版本），聚焦可落地的技术事实，不依赖主观评价，旨在提供清晰、可执行的选型依据。

## 关键维度对比

| 维度 | Realtime API | Omni Realtime API |
|------|--------------|-------------------|
| **协议栈** | 支持三种传输协议：<br>• AOQ（Media over QUIC，推荐用于移动端/弱网）<br>• WebRTC（原生浏览器支持，无 SDK 依赖）<br>• WebSocket（通用、易调试，跨端兼容性最佳） | **仅支持 WebSocket**（标准 `wss://` 协议，基于事件驱动模型） |
| **输入格式** | • 音频：PCM/WAV（8k–48k Hz），支持外部流注入<br>• 视频：I420/NV12/BGRA 原始帧或 JPEG 编码帧（≤1080p）<br>• 文本：通过 `session.update` 或事件携带指令 | • 音频：PCM/WAV（8k–48k Hz），通过 `input_audio_buffer.append` 流式提交<br>• 图像：JPG/JPEG（≤1080p，Base64 编码后 ≤256KB），需在首次音频后发送<br>• 文本：仅支持系统级 `instructions`，**不支持运行时文本输入** |
| **输出格式** | • 灵活组合：`text` / `audio` / `video` / `tool_calls`（依模型与协议而定）<br>• 音频编码：Opus（AOQ/WebRTC）、PCM/WAV（WebSocket）<br>• 视频：H.264 编码帧（AOQ/WebRTC） | • 固定模态组合：仅支持 `["text"]` 或 `["text", "audio"]`<br>• 音频输出：PCM/WAV（采样率 24k/48k Hz 可配，**默认 24k**）<br>• **不支持视频输出** |
| **支持模型与功能** | • 全模态对话（`qwen3.5-omni-*`）<br>• 实时语音识别（ASR）<br>• 实时语音合成（TTS）<br>• 实时语音翻译（Live Translate）<br>• [多模态](../concepts/multi-modal.md)对话套件（`multimodal-dialog`）<br>• **ASR/TTS 模型在 WebRTC 协议下不可用** | • 专注全模态语音交互：<br> – `qwen3.5-omni-plus/flash-realtime`（语义 VAD、工具调用、联网搜索）<br> – `qwen-omni-turbo-realtime`（轻量级语音响应）<br>• **不支持独立 ASR/TTS 模型调用**（无 `Fun-ASR-Realtime`、`CosyVoice` 等专用模型）<br>• 原生支持工具调用（Function Calling）与声音复刻（Voice Cloning） |
| **API 端点与鉴权** | • 端点因协议而异：<br> – AOQ：需先调用 `/v1/realtime/aoq/token` 获取临时 `aoqTokenForClient`<br> – WebRTC：SDP 交换中携带 `Authorization: Bearer <API_KEY>`<br> – WebSocket：直连 `wss://.../api-ws/v1/realtime`，握手头传 API Key | • 统一 WebSocket 端点：<br> `wss://{WorkspaceId}.{Region}.maas.aliyuncs.com/api-ws/v1/realtime`<br>• 鉴权：WebSocket 握手请求头中携带 `Authorization: Bearer <API_KEY>`（**无需预取 token**） |
| **计费方式** | • 按 **实际调用模型 + 协议类型 + 资源消耗** 计费：<br> – AOQ/WebRTC：按连接时长（秒）+ 音视频带宽（MB）计费<br> – WebSocket：按 **输入 token + 输出 token + 音频时长（秒）** 分项计费<br>• 不同协议下相同模型单价可能不同 | • **统一按会话粒度计费**：<br> – 输入音频时长（秒）<br> – 输出文本 token 数<br> – 输出音频时长（秒）<br> – 工具调用次数（若启用）<br>• **无连接时长/带宽附加费**，成本更可预测 |
| **典型场景** | • 需混合协议部署：如 App 用 AOQ、Web 用 WebRTC、IoT 设备用 WebSocket<br>• 需独立控制 ASR（语音转文字）或 TTS（文字转语音）能力<br>• 需视频理解/生成（如远程协作白板、AR 导览）<br>• 对网络鲁棒性要求极高（如车载、边缘设备） | • 纯语音交互闭环应用：如智能音箱、会议实时字幕+语音应答、语音客服机器人<br>• 需强语义理解与上下文工具联动（如查天气→订机票→读行程）<br>• 需定制音色（声音复刻）且对音频保真度敏感<br>• 快速验证 MVP，追求 SDK 封装度与开发效率 |

## 各方案适用场景建议

### ✅ 推荐选用 **Realtime API** 当：
- 业务需**解耦语音识别（ASR）与语音合成（TTS）**，例如：前端独立做语音输入 → 后端调用 ASR → NLU 处理 → 调用业务 API → 再调用 TTS 返回语音；
- 目标终端**高度异构**：同时覆盖 iOS/Android App（AOQ）、Web 浏览器（WebRTC）、嵌入式设备（WebSocket）；
- 应用涉及**视频流处理**，如实时视频会议中的发言人检测、PPT 内容理解、AR 辅助维修；
- 网络环境不可控（如 4G/弱 Wi-Fi），需 QUIC 协议提供的连接迁移与低重传特性；
- 已有成熟 WebRTC 基础设施，希望复用 SDP 信令与媒体协商逻辑。

### ✅ 推荐选用 **Omni Realtime API** 当：
- 核心需求是**端到端语音对话体验**，强调自然停顿（语义 VAD）、上下文连贯、工具自动触发；
- 开发团队倾向**快速集成、减少协议适配负担**，接受 WebSocket 作为唯一传输层；
- 需要**声音复刻能力**（如品牌专属语音播报）或**联网搜索增强**（如实时回答新闻/股价问题）；
- 成本模型需透明可控，避免因连接抖动、重连导致的带宽/时长意外计费；
- 服务端已具备稳定 WebSocket 网关能力，且客户端以 Web/小程序为主（非原生 App）。

## 技术选型参考（面向开发者）

| 选型考量点 | Realtime API | Omni Realtime API | 建议动作 |
|------------|--------------|-------------------|----------|
| **是否需要 WebRTC 原生浏览器支持？** | ✅ 支持（但 ASR/TTS 不可用） | ❌ 不支持 | 若必须用 WebRTC 且需 ASR，请改用 WebSocket 协议接入 Realtime API |
| **是否需在一次会话中切换 ASR/TTS/LLM 模型？** | ✅ 支持（通过 `model` 参数动态指定） | ❌ 不支持（固定为 Omni 系列模型） | 如需灵活编排，选 Realtime API；如只需“听-思-说”一体化，选 Omni |
| **SDK 集成复杂度** | ⚠️ 较高：AOQ 需专用 SDK + Opus 插件；WebRTC 需手动管理 DataChannel；WebSocket 最简 | ✅ 低：官方 Python/Java SDK 封装完整事件流（`connect()`/`update_session()`/`append_audio()`） | 追求开发速度 → 选 Omni；有专业音视频团队 → Realtime API 更可控 |
| **VAD 精度要求** | • `server_vad`（声学）<br>• `semantic_vad`（仅 Omni 系列模型支持） | ✅ 原生支持 `semantic_vad`（语义级断句，抗背景音干扰更强） | 高噪环境（如工厂、街道）→ 优先 Omni；或 Realtime API 中选用 `qwen3.5-omni-*` 模型 + AOQ/WebSocket 协议 |
| **合规与安全要求** | • API Key **严禁客户端硬编码**，AOQ/WebRTC 均需后端签发临时凭证<br>• WebSocket 可直连但需严格管控 [Token](../concepts/token.md) 生命周期 | • 同样要求 API Key 不暴露，但 WebSocket 握手更易审计 | 两者均满足企业级安全基线，关键在后端凭证服务设计 |
| **未来扩展性** | • 协议层开放，可自定义媒体流、注入外部音视频源<br>• 模型生态更广（含 ASR/TTS/Translate 专用模型） | • 功能聚焦，扩展依赖平台迭代（如新增图像理解需等待 Omni 模型升级） | 长期演进路径明确、需自主掌控媒体链路 → Realtime API；拥抱平台一体化能力 → Omni |

> **最后提醒**：  
> - **不要在 WebRTC 中尝试调用 ASR/TTS 模型**——该限制已由 Realtime API 官方文档明确声明，强行调用将返回 `400 UnsupportedProtocol` 错误。  
> - **Omni Realtime API 的 `audio.output.format.sample_rate` 实际支持 `24000` 和 `48000`**，请以 Python/Java SDK 文档配置项为准，忽略服务端事件文档中“仅支持 pcm”的过时描述。  
> - 两个方案**共享同一套模型底座**（如 `qwen3.5-omni-plus-realtime`），在相同协议（WebSocket）和参数下，核心推理质量与延迟表现一致。差异主要来自协议栈能力与 API 抽象层级。  

如需进一步评估具体业务场景的接入路径，建议使用 [DashScope Playground](https://dashscope.console.aliyun.com/playground) 进行双方案快速验证，并参考对应 SDK 的 Quick Start 示例代码。

## 被对比主题页

- [realtime api user guide](../api/realtime-api-user-guide.md)
- [omni realtime api](../api/omni-realtime-api.md)



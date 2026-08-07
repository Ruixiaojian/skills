# 实时 API 方案对比：Omni Realtime API vs Realtime API User Guide

本对比旨在帮助开发者清晰理解百炼平台两类核心实时交互能力的技术定位与适用边界：**Omni Realtime API**（面向端到端[多模态](../concepts/multi-modal.md)流式对话的专用 WebSocket 接口）与 **Realtime API User Guide**（面向全场景、多协议、可扩展架构的统一实时能力框架）。二者并非简单替代关系，而是在抽象层级、协议灵活性、部署模型和工程权衡上存在系统性差异。本文从技术实现、能力边界与落地实践三个维度展开结构化对比，为选型提供客观依据。

## 关键维度对比

| 维度 | Omni Realtime API | Realtime API User Guide |
|------|-------------------|--------------------------|
| **协议栈** | 仅支持 WebSocket（WSS） | 支持 **AOQ**（专有低延迟协议）、**WebRTC**（浏览器原生）、**WebSocket**（兼容验证）三套协议，可按终端/网络/合规需求动态选择 |
| **输入格式** | • 音频：PCM 16kHz 单声道 16bit（`input_audio_buffer.append`）<br>• 图像：JPG/JPEG Base64 编码（≤256KB，≤1080p）<br>• 文本：通过 `session.update` 或 `input_text` 事件注入 | • 音频：PCM 16kHz（AOQ/WebSocket）或 Opus 编码（AOQ 强制启用插件）<br>• 视频：原始帧（YUV/RGB）或 H.264 编码帧（AOQ 自定义视频输入）<br>• 文本/指令：统一 `session.update` 或协议特定事件（如 WebRTC 的 `datachannel`） |
| **输出格式** | • 文本：`response.text.delta` 流式片段<br>• 音频：PCM 24kHz 单声道 16bit（`response.audio.delta`）<br>• ASR 中间结果：`response.audio_transcript.delta` | • 文本：各协议均支持 `text.delta`<br>• 音频：PCM 24kHz（AOQ/WebSocket）或 Opus 流（AOQ 默认）<br>• 视频：仅 AOQ 支持自定义视频渲染（`onPlaybackVideoFrame`）<br>• [多模态](../concepts/multi-modal.md)结构化响应：如翻译结果、ASR 置信度、TTS 语音事件等按模型能力分层返回 |
| **支持模型** | • 严格限定于 `qwen*-omni-*-realtime` 系列（如 `qwen3.5-omni-realtime`, `qwen3-omni-flash-realtime`, `qwen-omni-turbo-realtime`）<br>• ASR 固定绑定 `qwen3-asr-flash-realtime` | • **全模型谱系覆盖**：<br> ✓ Omni 全模态系列（`qwen3.5-omni-plus-realtime` 等）<br> ✓ 实时语音翻译（`qwen3.5-livetranslate-flash-realtime`）<br> ✓ 独立 ASR/TTS 模型（`Qwen-Audio-3.0-ASR-Flash-Streaming`, `CosyVoice`）<br> ✓ [多模态](../concepts/multi-modal.md)开发套件（`multimodal-dialog`）<br> ✓ 实时语音对话专用模型（`qwen-audio-3.0-realtime-plus`） |
| **API 端点** | 地域专属 WSS 地址：<br>`wss://{WorkspaceId}.{region}.maas.aliyuncs.com/api-ws/v1/realtime` | • AOQ：`POST /api/v1/allocate`（获取 token） + 客户端 SDK 连接 Relay<br>• WebRTC：`POST /api/v1/webrtc/realtime?model=xxx`（信令交换）<br>• WebSocket：`wss://{WorkspaceId}.{region}.maas.aliyuncs.com/api-ws/v1/realtime`（同 Omni，但鉴权与事件语义不同） |
| **计费方式** | 按 **实际音频处理时长（秒） + 文本 token 数量 + 图像调用次数** 分项计费；VAD 检测、工具调用、搜索等高级能力不额外计费 | 按 **所选模型 + 协议类型 + 使用时长/[Token](../concepts/token.md) 数** 统一计费；AOQ 协议因 Relay 资源消耗略高于 WebSocket；WebRTC 在浏览器端免客户端资源占用，服务端带宽成本更高 |
| **典型场景** | • 低延迟语音助手（端侧 VAD 不足，依赖语义级 `semantic_vad`）<br>• 需图像理解的智能客服（如上传截图咨询）<br>• 工具调用密集型对话（如订票、查账）<br>• 声音复刻深度集成（定制音色无缝接入） | • 弱网环境下的移动 App（AOQ 抗丢包/低抖动）<br>• 浏览器端实时协作（WebRTC 免插件、P2P 优化）<br>• 多模态混合应用（同时接入 ASR+TTS+翻译+对话）<br>• 需自定义音视频管线的硬件设备（如会议终端、IoT 设备） |
| **配置灵活性** | • 所有参数通过 `session.update` 事件设置<br>• `qwen-omni-turbo-realtime` 系列为只读配置（不可调采样参数）<br>• VAD 参数（如 `idle_timeout_ms`）与模型强绑定 | • 协议层配置（如 AOQ 的 `clientRelayEndpoints`）与会话层配置（`session.update`）分离<br>• 支持运行时动态切换模态（如通话中开启视频）<br>• 音视频编解码、采集/播放完全可接管（`isExternal=true`）<br>• 各模型独立参数空间（ASR/TTS/对话参数互不影响） |
| **安全模型** | 客户端直连，需在前端管理 `Authorization: Bearer <API_KEY>`（**高风险，不推荐生产环境直接使用**） | • AOQ/WebRTC：**强制服务端代理鉴权**，客户端仅持临时 token（`aoqTokenForClient`）<br>• WebSocket：支持服务端代签模式，避免 API Key 泄露<br>• 所有协议均支持 Workspace 级权限隔离与审计日志 |

## 各方案的适用场景建议

### ✅ 选择 Omni Realtime API 当且仅当：
- 业务形态高度聚焦于 **“语音+文本+图像”三模态端到端对话**，且无需视频、翻译、独立 ASR/TTS 等扩展能力；
- 开发团队具备 WebSocket 流式编程经验，能自主处理 `input_audio_buffer.append`/`response.audio.delta` 等细粒度事件；
- 对 `semantic_vad`（语义级静音检测）、联网搜索、[函数调用](../concepts/function-calling.md)等 Omni 独占能力有刚性需求；
- 可接受客户端暴露短期有效的 API Key（或已构建完善的密钥代理网关）；
- 期望最小化接入复杂度，避免协议选型、Relay 配置、Opus 插件集成等运维负担。

### ✅ 选择 Realtime API User Guide 当且仅当：
- 需要 **跨终端、跨网络、跨模态的统一接入能力**（如 App + Web + IoT 设备共用一套后端逻辑）；
- 存在 **弱网、高并发、低延迟敏感** 场景（AOQ 协议是唯一满足 200ms 端到端 P99 延迟的方案）；
- 要求 **音视频管线完全可控**（如对接专业音频设备、自研降噪算法、H.265 编码）；
- 业务需组合多种模型能力（例如：先 ASR 识别 → 再对话理解 → 最后 TTS 合成），而非单一 Omni 模型闭环；
- 安全合规要求严格，**禁止客户端持有长期 API Key**，必须采用服务端 [Token](../concepts/token.md) 代理机制。

## 技术选型参考（面向开发者）

| 选型考量 | 推荐方案 | 理由说明 |
|----------|----------|----------|
| **快速原型验证 / MVP 开发** | Omni Realtime API | WebSocket 接口简洁，文档事件驱动明确，5 分钟即可跑通语音对话 demo；无需配置 Relay、证书指纹、Opus 插件等 AOQ 依赖项。 |
| **企业级客服系统（含 App/Web/H5）** | Realtime API User Guide（AOQ + WebSocket） | App 端用 AOQ 保障弱网体验，Web/H5 端用 WebSocket 兼容性兜底；统一后端适配层可复用鉴权、会话管理、日志审计逻辑。 |
| **智能硬件（车载/会议终端）** | Realtime API User Guide（AOQ + 自定义音视频） | 通过 `isExternal=true` 直接接入硬件 PCM/I2S 接口，绕过系统音频栈；支持 Opus 编码降低带宽，Relay 保证公网穿透稳定性。 |
| **需要声音复刻 + 工具调用的语音助手** | Omni Realtime API（`qwen3.5-omni-realtime`） | 唯一支持 `voice` ID 注入与 `tools` 同时生效的方案；`semantic_vad` 对自然对话停顿更鲁棒，减少误触发。 |
| **多语言实时翻译会议系统** | Realtime API User Guide（WebRTC + `qwen3.5-livetranslate-flash-realtime`） | WebRTC 原生支持浏览器音视频采集与渲染，无需 SDK；翻译模型独立于 Omni，支持双语字幕、发言者分离等专业功能。 |
| **成本敏感型轻量级聊天机器人** | Omni Realtime API（`qwen-omni-turbo-realtime`） | 固定参数、无搜索/工具开销，单位音频时长成本最低；适合纯文本增强型语音交互（如播报类应用）。 |

> ⚠️ **重要提醒**：  
> - **切勿在前端代码中硬编码 API Key**。若选用 Omni Realtime API，务必通过服务端代理生成短期 [Token](../concepts/token.md) 并签名 WebSocket URL（如 `wss://.../realtime?token=xxx`），或改用 Realtime API 的 AOQ/WebSocket 代理模式。  
> - `qwen-omni-turbo-realtime` 虽成本低，但**不可调节 temperature/top_p 等参数**，对生成多样性要求高的场景（如创意对话）不适用。  
> - WebRTC 协议 **不支持独立 ASR/TTS 模型**，若需分离式语音处理，请选用 AOQ 或 WebSocket 协议。  

选择的本质不是“哪个更好”，而是“哪个更贴合你的架构约束与业务演进路径”。建议初期用 Omni 快速验证核心对话能力，中长期向 Realtime API User Guide 迁移以获得协议弹性、安全合规性与生态延展性。

## 被对比主题页

- [omni realtime api](../api/omni-realtime-api.md)
- [realtime api user guide](../api/realtime-api-user-guide.md)



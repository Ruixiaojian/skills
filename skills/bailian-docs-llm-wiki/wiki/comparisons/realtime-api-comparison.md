# 实时 API 方案对比：Omni Realtime API vs Realtime API User Guide

本文旨在帮助开发者清晰区分百炼平台两类核心实时交互能力——**Omni Realtime API** 与 **Realtime API User Guide** 所定义的通用实时协议栈，避免因概念混淆导致选型偏差、集成失败或功能缺失。二者虽均面向低延迟[多模态](../concepts/multimodal.md)场景，但定位不同：前者是**特定模型驱动的、开箱即用的全栈式 WebSocket 接口**；后者是**面向多模型、多协议、多终端的底层通信协议框架规范**，提供 AOQ/WebRTC/WebSocket 三类传输路径及配套 SDK 约束。本对比聚焦技术本质差异，为架构设计与工程落地提供客观依据。

## 关键维度对比

| 维度 | Omni Realtime API | Realtime API User Guide |
|------|-------------------|--------------------------|
| **定位与性质** | 面向 `qwen-omni-*` 系列模型的**专用实时接口**，封装了语音/文本/图像协同逻辑与事件语义 | 面向全模型生态的**通用实时通信协议规范**，定义传输层（AOQ/WebRTC/WS）、鉴权、媒体流控制等跨模型共性能力 |
| **输入格式** | WebSocket 事件驱动：<br>• `input_audio_buffer.append`（16 kHz PCM）<br>• `input_image_buffer.append`（JPG/JPEG，≤1080p，Base64 ≤256 KB，需在音频缓冲非空后发送） | 协议级抽象：<br>• AOQ：原始 PCM 帧 + 自定义元数据<br>• WebRTC：标准 MediaStream / SDP Offer/Answer<br>• WebSocket：二进制帧或 JSON 事件（依模型而定）<br>• **不强制约束编解码/采样率**（ASR/TTS 模型有独立要求） |
| **输出格式** | 结构化 WebSocket 事件流：<br>• `conversation.item.created`（文本/工具调用）<br>• `response.audio.delta`（24 kHz PCM 音频流）<br>• `session.updated` / `input_audio_buffer.committed` 等状态通知 | 协议无关，由模型决定：<br>• AOQ/WebRTC：支持音频流（Opus/PCM）、文本增量、结构化响应（如工具调用）<br>• WebSocket：依具体模型文档（如 ASR 返回 `transcript` 字段，TTS 返回 `audio_chunk`）<br>• **无统一事件 Schema，需按模型文档解析** |
| **支持模型** | 仅限 `qwen-omni-*` 系列：<br>• `qwen3.5-omni-realtime`（含 semantic_vad、tools、search）<br>• `qwen3.5-omni-plus/flash-realtime`<br>• `qwen3-omni-flash-realtime`<br>• `qwen-omni-turbo-realtime` | 覆盖全实时模型族：<br>• 全模态：`qwen3.5-omni-plus/flash-realtime`<br>• 语音翻译：`qwen3.5-livetranslate-flash-realtime`<br>• ASR：`Qwen-Audio-3.0-ASR-Flash-Streaming`（AOQ/WS 支持，WebRTC ❌）<br>• TTS：`CosyVoice` 系列（AOQ/WS 支持，WebRTC ❌）<br>• 对话：`qwen-audio-3.0-realtime-plus/flash` |
| **API 端点** | 固定 WebSocket 地址：<br>`wss://{WorkspaceId}.{Region}.maas.aliyuncs.com/api-ws/v1/realtime`<br>（地域强绑定，无协议切换能力） | 多协议端点动态生成：<br>• AOQ：`aoq://...`（需服务端 allocate 获取 token）<br>• WebRTC：`https://{Endpoint}/v1/webrtc/join`（白名单 Endpoint）<br>• WebSocket：`wss://{WorkspaceId}.{Region}.maas.aliyuncs.com/api-ws/v1/realtime`（与 Omni 共享域名，但路由逻辑分离） |
| **计费方式** | 按 **[Token](../concepts/token.md) + Audio Duration（秒）** 双维度计费：<br>• 文本输入/输出 [Token](../concepts/token.md)<br>• 音频输出时长（24 kHz PCM 秒数）<br>• 图像输入按次计费（固定单价） | 按 **所选模型 + 使用量** 计费：<br>• ASR/TTS/翻译/对话等模型各自独立计费项<br>• AOQ/WebRTC/WS 传输层本身不额外计费<br>• 同一模型在不同协议下单价一致 |
| **典型场景** | • 需要端到端语音+文本+图像协同的智能客服/虚拟助手<br>• 要求 VAD 自动切分、工具调用、联网搜索的闭环对话<br>• 快速验证 `qwen-omni` 系列能力的原型开发 | • 多终端适配：移动端（AOQ）、浏览器（WebRTC/WS）、服务端（WS）<br>• 弱网环境下的高鲁棒语音交互（AOQ 内置 3A 处理）<br>• 复用现有 WebRTC 基础设施（如视频会议 SDK）<br>• 构建 ASR/TTS 独立流水线（如语音转文字 → NLU → TTS 合成） |
| **开发复杂度** | 中低：<br>• 提供 Python/Java SDK 封装 `connect()`/`append_audio()`/`update_session()`<br>• 事件语义明确（如 `turn_detection` 参数直接生效）<br>• 无需处理 SDP/Relay/Opus [插件](../concepts/plugin.md)等底层细节 | 中高（依协议而异）：<br>• AOQ：需集成 SDK、管理 token、严格遵循状态机（如 `enableSendMediaStream` 时机）<br>• WebRTC：需处理信令、SDP 协商、媒体权限、兼容性（白名单限制）<br>• WebSocket：轻量接入，但需自行解析各模型响应格式 |

## 适用场景建议

### ✅ 选择 Omni Realtime API 当：
- 业务目标明确聚焦于 **`qwen-omni` 系列模型的端到端[多模态](../concepts/multimodal.md)对话体验**（如带图像理解的语音客服）；
- 需要 **开箱即用的 VAD（尤其是 semantic_vad）、工具调用、联网搜索等高级能力**，且不希望自行编排多模型 pipeline；
- 开发团队倾向 **快速交付 MVP**，接受 WebSocket 单协议方案，对弱网对抗、浏览器深度兼容无极致要求；
- 已使用百炼 Python/Java SDK，希望复用 `omni-realtime-python-sdk` 的高层抽象。

### ✅ 选择 Realtime API User Guide（及其协议）当：
- 需要 **跨模型、跨协议的统一接入层**，例如同时集成 ASR（`Qwen-Audio-3.0-ASR`）、TTS（`CosyVoice`）、翻译（`livetranslate`）和对话（`qwen-audio-realtime`）；
- 终端覆盖要求严格：**移动端需 AOQ 弱网优化**，**浏览器端需 WebRTC 原生支持**，**服务端需 WebSocket 简单对接**；
- 已有成熟音视频基础设施（如自研 WebRTC 框架、Opus 编解码模块），希望 **复用现有技术栈而非引入新 SDK**；
- 架构设计强调 **解耦与可扩展性**，例如将语音识别、意图理解、语音合成拆分为独立微服务，通过 Realtime API 协议桥接。

> ⚠️ 注意：二者并非互斥替代关系，而是**垂直分层协作**——Omni Realtime API 本质是 Realtime API 协议栈在 `qwen-omni` 模型上的一个**预配置、强语义的实现特例**。若需 `qwen-omni` 能力但要求 AOQ 传输或 WebRTC 兼容，应基于 Realtime API User Guide 规范，选用 `qwen3.5-omni-plus-realtime` 模型并走 AOQ/WebRTC 协议路径。

## 技术选型参考（面向开发者）

| 选型考量 | 推荐方案 | 理由 |
|----------|----------|------|
| **首次接入百炼实时能力，验证 `qwen-omni` 效果** | Omni Realtime API | 最小学习成本，SDK 开箱即用，事件语义清晰，10 分钟完成 Hello World |
| **构建企业级智能客服系统，需支持 iOS/Android/网页三端** | Realtime API + AOQ（移动端） + WebRTC（网页端） | 协议分层适配最优体验：AOQ 保障移动端弱网稳定性，WebRTC 利用浏览器原生能力免[插件](../concepts/plugin.md) |
| **已有 WebRTC 视频会议产品，需叠加实时语音翻译** | Realtime API + WebRTC | 复用现有信令与媒体管道，仅需对接 `/v1/webrtc/join` 并指定 `model=qwen3.5-livetranslate-flash-realtime` |
| **需要语音识别（ASR）+ 自定义 NLU + 语音合成（TTS）的灵活 pipeline** | Realtime API + WebSocket（ASR） + WebSocket（TTS） | ASR/TTS 模型仅支持 AOQ/WS，WebRTC 不适用；WebSocket 提供最简协议，便于服务端编排 |
| **要求 `semantic_vad` 或 `tools` 调用，且必须运行在浏览器中** | Omni Realtime API（WebSocket） | `semantic_vad` 和 `tools` 仅 `qwen3.5-omni-realtime` 支持，且 Omni API 是其唯一暴露该能力的 WebSocket 接口；WebRTC 在 Omni 场景下不提供等价能力 |

请始终以 [客户端事件](../../raw/model-api-reference/omni-realtime-api/client-events.md) 和 [Realtime API 概述](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-overview.md) 的最新模型兼容性矩阵为准，并在生产环境前进行协议级压力测试与弱网模拟验证。

## 被对比主题页

- [omni realtime api](../api/omni-realtime-api.md)
- [realtime api user guide](../api/realtime-api-user-guide.md)



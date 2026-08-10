# 实时交互 API 对比：Omni Realtime API vs Realtime API

为帮助开发者在构建低延迟、[多模态](../concepts/multi-modal.md)实时 AI 应用（如智能语音助手、实时会议翻译、交互式教育机器人等）时做出精准技术选型，本文系统对比百炼平台两大核心实时交互能力：**Omni Realtime API** 与 **Realtime API**。二者虽均面向实时对话场景，但在架构定位、协议支持、功能边界、接入复杂度及适用范式上存在本质差异。本对比基于最新 v3.5 系列模型能力与生产环境实践，聚焦可落地的技术决策维度。

## 关键维度对比

| 维度 | Omni Realtime API | Realtime API |
|------|-------------------|--------------|
| **核心定位** | 单一、深度优化的 WebSocket [多模态](../concepts/multi-modal.md)对话协议；强调端到端语义级实时性与 VAD 智能控制 | 统一模型能力层 + **多协议抽象层**（AOQ / WebRTC / WebSocket），兼顾终端适配性与功能完整性 |
| **通信协议** | **仅支持 WebSocket**（`wss://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api-ws/v1/realtime`） | **三协议并存**：<br>• AOQ（推荐用于原生 App，含弱网对抗、音视频编解码优化）<br>• WebRTC（推荐用于浏览器，零 SDK 依赖）<br>• WebSocket（推荐用于服务端集成、快速验证） |
| **输入格式** | • 音频：16 kHz PCM 单声道（Base64 编码）<br>• 图像：JPG/JPEG（≤1080p，Base64，≤256 KB）<br>• **不支持文本直接输入**（需通过音频或图像触发） | • 音频：16 kHz PCM（AOQ/WebSocket）；WebRTC 使用 RTP 自动传输原始音频流<br>• 图像：AOQ 支持 I420/NV12/BGRA 原始帧或 JPEG 编码帧；WebRTC 通过 MediaStream 传输<br>• **支持纯文本输入**（如 `conversation.item.create` 发送 `type: "message"`） |
| **输出格式** | • 文本流（`response.text.delta`）<br>• 24 kHz PCM 音频流（`response.audio.delta`）<br>• ASR 中间转录（`response.audio_transcript.delta`）<br>• **无结构化 JSON 响应体，全事件驱动** | • 同 Omni 的文本/音频/ASR 流式事件<br>• **额外支持结构化响应**（如 `conversation.item.created` 返回完整消息对象，含 `role`, `content`, `tool_calls` 等字段）<br>• WebRTC 输出为 RTP 音频流，无需 Base64 解码 |
| **支持模型** | • 仅限 Omni 系列实时模型：<br> `qwen3.5-omni-plus-realtime`<br> `qwen3.5-omni-flash-realtime`<br> `qwen3-omni-flash-realtime`<br> `qwen-omni-turbo-realtime`<br>• **不支持 ASR/TTS 独立模型**（ASR 内置不可替换） | • 全模型矩阵：<br> ✅ Omni 全模态模型<br> ✅ 实时语音翻译（`qwen3.5-livetranslate-flash-realtime`）<br> ✅ 独立 ASR（`Qwen-Audio-3.0-ASR-Flash-Streaming` 等）<br> ✅ 独立 TTS（`CosyVoice` 系列）<br> ✅ 实时语音对话（`qwen-audio-3.0-realtime-plus`）<br>• **协议级模型支持有差异**（如 WebRTC 不支持 ASR/TTS） |
| **API 端点** | 固定 WebSocket 地址：<br>`wss://{WorkspaceId}.{region}.maas.aliyuncs.com/api-ws/v1/realtime`<br>（需业务空间专属域名） | 动态端点，按协议区分：<br>• AOQ：`https://dashscope.aliyuncs.com/api/v1/realtime/allocate`（鉴权） + 客户端直连 Relay 节点<br>• WebRTC：`https://dashscope.aliyuncs.com/api/v1/realtime/webrtc`（SDP 交换）<br>• WebSocket：`wss://dashscope.aliyuncs.com/api-ws/v1/realtime?model=xxx`（通用直连） |
| **计费方式** | • **按 token 计费**（输入 token + 输出 token）<br>• 音频/图像输入按等效文本 token 折算（详见 [计费说明](../../raw/pricing/omni-realtime-pricing.md)）<br>• **连接时长不计费**，仅按实际处理量结算 | • **统一按 token 计费**（同 Omni）<br>• **AOQ/WebRTC 协议额外收取媒体中继流量费**（按 GB 计，WebRTC 默认启用 Relay）<br>• WebSocket 协议无额外流量费 |
| **VAD 与交互模式** | • 支持 `server_vad`（服务端检测）与 `semantic_vad`（语义级检测，仅 qwen3.5 系列）<br>• 显式区分 `Manual`（客户端 commit）与 `VAD`（服务端自动）模式<br>• `idle_timeout_ms` 仅在特定模型+VAD 组合下生效 | • `semantic_vad` 仅 AOQ/WebSocket 支持；WebRTC **仅支持服务端 VAD**，且无手动模式<br>• AOQ 提供精细媒体流控制（如 `enableSendMediaStream`），避免未就绪丢帧<br>• WebRTC 由浏览器自动管理媒体流生命周期 |
| **工具调用与搜索** | • `tools` 与 `enable_search` **互斥且仅 qwen3.5 系列支持**<br>• 工具调用需严格遵循事件序列（`function_call` → 本地执行 → `function_call_output` → `response.create`） | • 同 Omni 的互斥约束（qwen3.5 系列专属）<br>• **结构化事件更清晰**：`conversation.item.created` 明确标识 `type: "function_call"`，便于状态机实现<br>• 支持跨协议复用同一工具定义 |
| **音色与声音复刻** | • 复刻音色需**预先创建**，并在 `session.update` 中显式指定 `voice`<br>• 复刻音色**仅限对应 `target_model` 的 Omni-Realtime 调用** | • 复刻音色同样需预创建，但可通过 `voice` 参数在所有支持 TTS 的模型中复用（如 `CosyVoice` + `qwen3.5-omni-plus-realtime`）<br>• **音色跨模型复用性更高** |

## 适用场景建议

### ✅ 选择 Omni Realtime API 当：
- 你已确定使用 **Qwen-Omni 系列模型**，且业务强依赖其[多模态](../concepts/multi-modal.md)融合能力（如语音+图像联合理解）；
- 客户端为 **服务端应用或可控环境下的桌面/嵌入式设备**，能稳定维持 WebSocket 长连接；
- 需要 **极致 VAD 控制粒度**（如自定义 `silence_duration_ms`、`threshold`，或启用 `semantic_vad` 过滤背景音）；
- 架构简单，**无需对接独立 ASR/TTS 或翻译模型**，所有能力均由单一 Omni 模型闭环完成；
- 开发团队熟悉 WebSocket 事件协议，能自主处理 `input_audio_buffer.append`、`response.audio.delta` 等底层事件流。

### ✅ 选择 Realtime API 当：
- 你需要 **跨终端统一接入**：iOS/Android App（用 AOQ）、Web 浏览器（用 WebRTC）、后端服务（用 WebSocket）共用同一套模型逻辑；
- 业务涉及 **混合能力组合**：例如“语音输入 → ASR 转文本 → LLM 理解 → TTS 合成 → 实时播放”，需分别调用 ASR、LLM、TTS 模型；
- 目标用户网络环境复杂（如弱网移动场景），**需 AOQ 提供的自适应码率、前向纠错、智能重传等 QoS 保障**；
- 要求 **开箱即用的媒体流管理**（如 WebRTC 的自动采集/播放、AOQ 的 `startAudioCapture` 封装），降低音视频工程成本；
- 需要 **结构化消息对象**（而非纯事件流）以简化对话状态管理，或计划集成第三方对话框架（如 Rasa、LangChain）。

## 技术选型参考指南

| 选型考量 | 推荐方案 | 说明 |
|----------|----------|------|
| **终端类型优先** | Web 浏览器 → **Realtime API (WebRTC)**<br>iOS/Android 原生 App → **Realtime API (AOQ)**<br>服务端/边缘设备 → **Omni Realtime API 或 Realtime API (WebSocket)** | WebRTC 无需 SDK，浏览器原生支持；AOQ 提供移动端最佳体验；WebSocket 通用性强，Omni 更轻量 |
| **功能需求优先** | 仅需 Omni 多模态对话 → **Omni Realtime API**<br>需 ASR/TTS/翻译等独立能力 → **Realtime API** | Omni 是 Omni 模型的专用通道；Realtime API 是能力矩阵的统一入口 |
| **开发效率优先** | 快速原型验证 → **Realtime API (WebSocket)**<br>长期维护的生产 App → **Realtime API (AOQ)** | WebSocket 接入最快；AOQ SDK 封装了复杂媒体逻辑，减少重复造轮子 |
| **性能与可靠性优先** | 弱网高可用 → **Realtime API (AOQ)**<br>超低延迟（局域网）→ **Omni Realtime API** | AOQ 内置网络自适应；Omni 协议栈更薄，理论延迟略低（但依赖网络质量） |
| **未来扩展性** | 预期增加新模型（如新 ASR/TTS）或新终端（如车机）→ **Realtime API** | Realtime API 的协议抽象层天然支持能力横向扩展，Omni API 与模型强绑定 |

> **重要提醒**：  
> - 若选用 Omni Realtime API，请务必校验模型名后缀（`-plus-`/`-flash-`/`-turbo-`），其功能集存在关键差异（如 `semantic_vad`、`tools`、参数可调性）；  
> - 若选用 Realtime API，请严格对照 [协议-模型支持矩阵](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-overview.md)，避免在 WebRTC 中误用 ASR/TTS 模型；  
> - 两者均要求 **16 kHz 输入音频**，但 Omni 强制 PCM 格式，Realtime API 的 AOQ/WebRTC 可通过 SDK 自动处理采样率转换。  

选择没有绝对优劣，关键在于匹配你的**终端生态、能力图谱、工程资源与演进路径**。建议初期用 Realtime API WebSocket 快速验证模型效果，再根据终端分布与功能演进，分阶段迁移至 AOQ 或 WebRTC。

## 被对比主题页

- [omni realtime api](../api/omni-realtime-api.md)
- [realtime api user guide](../api/realtime-api-user-guide.md)



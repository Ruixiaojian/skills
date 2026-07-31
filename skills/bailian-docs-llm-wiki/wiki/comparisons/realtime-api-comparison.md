# 实时API方案对比：Omni Realtime vs Realtime API

为帮助开发者在构建语音助手、智能客服、实时音视频交互等低延迟AI应用时做出精准技术选型，本文系统对比百炼平台两大核心实时能力接口：**Omni Realtime API** 与 **Realtime API**。二者虽均面向实时多模态交互场景，但在架构设计、协议支持、模型能力、控制粒度及适用边界上存在显著差异。本对比基于最新文档（截至2024年Q3）整理，聚焦可落地的技术决策要素，不涉及抽象概念或营销表述。

## 关键维度对比

| 维度 | Omni Realtime API | Realtime API |
|------|-------------------|--------------|
| **通信协议** | **仅 WebSocket（WSS）**<br>强制使用业务空间专属域名（如 `wss://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/...`） | **三协议可选**：<br>• AOQ（移动端原生首选）<br>• WebRTC（浏览器/Web端首选）<br>• WebSocket（服务端/原型验证）<br>需通过请求头 `x-dashscope-rtc-transport` 显式指定 |
| **输入格式** | • 音频：**16 kHz PCM（必选）**<br>• 图像：JPG/JPEG（Base64，≤256 KB，需先追加音频）<br>• 事件驱动：`input_audio_buffer.append` 等标准化客户端事件 | • 音频：16 kHz PCM（必选）<br>• 视频：H.264/H.265（AOQ/WebRTC支持，WebSocket不支持）<br>• 文本：纯文本消息（部分协议支持）<br>• **无图像输入能力** |
| **输出格式** | • 默认：**24 kHz PCM 音频 + 文本流**<br>• 可选纯文本（`["text"]`）<br>• 支持细粒度事件：`response.audio.delta`、`response.text.delta`、`conversation.item.input_audio_transcription.delta`（ASR中间结果） | • WebSocket：**仅支持 `["text"]` 输出模态**（文档明确限制）<br>• AOQ/WebRTC：支持 `["text", "audio"]`，输出24 kHz PCM音频+文本<br>• **不提供ASR中间转录流事件**（无 `audio_transcript.delta` 类事件） |
| **支持模型** | • 专属模型族：<br> - `qwen3.5-omni-realtime`（含 `plus`/`flash`）<br> - `qwen3-omni-flash-realtime`<br> - `qwen-omni-turbo-realtime`<br>• **内置ASR模型固定为 `qwen3-asr-flash-realtime`**（不可配置） | • 多模型矩阵：<br> - 全模态：`qwen3.5-omni-plus-realtime` 等<br> - ASR专用：`Qwen-Audio-3.0-ASR-Flash-Streaming`、`Fun-ASR-Realtime`<br> - TTS专用：`CosyVoice` 系列<br> - 对话专用：`qwen-audio-3.0-realtime-plus`<br>• **ASR/TTS模型仅 AOQ & WebSocket 支持，WebRTC 不支持** |
| **API 端点** | 固定 WSS 地址：<br>`wss://{WorkspaceId}.{Region}.maas.aliyuncs.com/api-ws/v1/realtime`<br>（旧域名 `dashscope.aliyuncs.com` 已弃用） | 协议相关端点：<br>• AOQ：`https://dashscope.aliyuncs.com/api/v1/realtime/aoq`（需[Token](../concepts/token.md)鉴权）<br>• WebRTC：信令服务器地址（由网关分配）<br>• WebSocket：`wss://dashscope.aliyuncs.com/api-ws/v1/realtime`（通用域名） |
| **计费方式** | **按会话时长 + 音频处理量计费**：<br>• 基础会话费（分钟级）<br>• 输入音频时长（秒）<br>• 输出音频时长（秒）<br>• 工具调用次数（如启用）<br>• **不按[Token](../concepts/token.md)计费** | **按模型能力分项计费**：<br>• ASR：按识别音频时长（秒）<br>• TTS：按合成音频时长（秒）<br>• LLM推理：按输出[Token](../concepts/token.md)数<br>• 会话管理：按连接时长（分钟）<br>• **支持细粒度能力拆分计费** |
| **VAD 能力** | • 支持双模式：<br> - `server_vad`（全模型支持）<br> - `semantic_vad`（仅 `qwen3.5-omni-realtime` 支持，语义级静音检测）<br>• 可配置 `threshold`、`silence_duration_ms`、`idle_timeout_ms`（部分模型） | • 支持 `server_vad` 和 `semantic_vad`（推荐后者）<br>• 参数配置一致，但 `idle_timeout_ms` 等高级参数未在文档中明确支持 |
| **工具调用与搜索** | • 工具调用（`tools`）与联网搜索（`enable_search`）**互斥**，不可同时启用<br>• 工具函数定义需符合 OpenAPI Schema | • **不支持工具调用与联网搜索**<br>• 为纯感知/生成类模型设计，无函数执行能力 |
| **声音复刻** | • **原生支持**：需预先调用独立声音复刻 API 创建音色，再通过 `session.update.voice` 传入 | • **不支持**：无音色定制化能力，仅提供预置音色（如 `"Ethan"`） |
| **开发复杂度** | • 事件驱动模型，需理解 `session.created` → `session.update` → `input_audio_buffer.append` → `response.create` 完整事件链<br>• 手动/自动 VAD 模式切换需显式控制<br>• 工具调用需实现完整回调闭环 | • 协议差异大：<br> - AOQ：需集成 SDK + Opus 插件，管理 `createEngine`/`enableSendMediaStream` 等生命周期<br> - WebRTC：无SDK，依赖原生API，需自行处理信令与媒体协商<br> - WebSocket：最简，但功能受限（仅文本输出） |

## 各方案的适用场景建议

### ✅ 选择 Omni Realtime API 当：
- 构建**高保真语音助手或智能客服**，要求端到端低延迟（<300ms）、语义级VAD、高自然度TTS及声音复刻；
- 需要**多模态协同**（语音+图像理解），例如远程医疗问诊、教育互动白板；
- 业务逻辑复杂，需**自主触发工具调用**（如查订单、订机票）或**条件性启用联网搜索**；
- 技术栈统一为 WebSocket，且服务端具备稳定长连接运维能力；
- 接受事件驱动编程范式，愿意投入精力管理会话状态与事件流。

### ✅ 选择 Realtime API 当：
- 面向**跨端兼容性优先**的场景：需同时支持 iOS/Android（AOQ）、浏览器（WebRTC）、服务端（WebSocket）；
- 核心需求是**实时语音识别（ASR）或语音合成（TTS）**，且需独立计费与独立模型选型；
- 已有成熟 WebRTC 基础设施（如音视频会议系统），希望叠加AI能力而不重构传输层；
- 需要**严格分离能力模块**（如ASR单独采购、LLM单独扩容），避免耦合；
- 开发团队熟悉原生 WebRTC 或移动端 SDK 集成，能承担协议适配成本；
- **无需图像理解、工具调用、声音复刻等高级能力**。

### ⚠️ 不推荐混用或迁移的典型情况：
- 将 Omni Realtime 的 `semantic_vad` 或工具调用能力迁移到 Realtime API —— **功能缺失，无法替代**；
- 在 WebRTC 场景下强行使用 Realtime API 调用 ASR/TTS 模型 —— **协议不支持，必然失败**；
- 用 WebSocket 协议接入 Realtime API 期望获得音频输出 —— **仅支持文本，设计限制**；
- 为轻量级语音播报（如IoT设备提示音）选用 Omni Realtime —— **过度设计，成本与复杂度不匹配**。

## 技术选型参考指南（面向开发者）

| 决策问题 | Omni Realtime API | Realtime API | 建议动作 |
|----------|-------------------|--------------|----------|
| **是否必须支持图像输入？** | ✅ 是 | ❌ 否 | 选 Omni Realtime |
| **是否需要工具调用或联网搜索？** | ✅ 是 | ❌ 否 | 选 Omni Realtime |
| **是否需声音复刻（定制音色）？** | ✅ 是 | ❌ 否 | 选 Omni Realtime |
| **是否需同时支持 App（iOS/Android）+ 浏览器？** | ❌ 否（仅WebSocket） | ✅ 是（AOQ+WebRTC） | 选 Realtime API |
| **是否需独立采购ASR/TTS能力？** | ❌ 否（ASR固定嵌入） | ✅ 是（可单独调用ASR/TTS模型） | 选 Realtime API |
| **是否已有WebRTC基础设施？** | ❌ 不适用 | ✅ 可直接复用 | 选 Realtime API（WebRTC协议） |
| **是否追求最低开发接入门槛（服务端快速验证）？** | ⚠️ 中（需理解事件流） | ✅ WebSocket模式最简（但仅文本） | 若只需文本，选 Realtime API；若需音视频，选 Omni Realtime |
| **是否对端到端延迟敏感（<250ms）且需语义VAD？** | ✅ 专为该场景优化 | ⚠️ 支持但非专精（尤其WebRTC链路更长） | 优先 Omni Realtime |

> **最后建议**：  
> - **MVP阶段**：若核心验证点是“语音→AI→语音”闭环，且无跨端硬性要求，**从 Omni Realtime 入手**——其开箱即用的ASR+LLM+TTS一体化设计可大幅缩短验证周期；  
> - **规模化部署阶段**：若用户覆盖App、小程序、PC网页，且各端网络质量差异大（如弱网移动场景），**采用 Realtime API 分协议接入**——AOQ保障移动端体验，WebRTC覆盖浏览器，WebSocket承载后台任务；  
> - **永远检查协议与模型的交叉支持**：Realtime API 的 `WebRTC + ASR` 或 `WebSocket + audio output` 组合在文档中明确不支持，务必以[模型支持矩阵](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-overview.md)为准，避免集成返工。

## 被对比主题页

- [omni realtime api](../api/omni-realtime-api.md)
- [realtime api user guide](../api/realtime-api-user-guide.md)



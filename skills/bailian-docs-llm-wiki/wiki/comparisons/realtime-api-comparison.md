# 实时 API 方案对比：Realtime API vs Omni Realtime API

为帮助开发者在百炼平台中高效选型，本文对两类核心实时交互能力——**Realtime API** 与 **Omni Realtime API**——进行系统性对比分析。二者均面向低延迟、多模态 AI 实时场景（如语音对话、实时翻译、音视频增强），但设计哲学、协议架构、能力边界与适用范式存在显著差异。本对比聚焦技术可行性、集成成本、功能完备性与运维复杂度，旨在为产品架构师与一线开发者提供可落地的选型决策依据。

## 关键维度对比

| 维度 | Realtime API | Omni Realtime API |
|------|--------------|-------------------|
| **协议支持** | ✅ AOQ（原生端首选）、✅ WebRTC（浏览器端）、✅ WebSocket（服务端/原型验证）<br>• 三协议统一模型接口，能力分层明确 | ❌ 仅支持 WebSocket<br>• 纯事件驱动流式通信，无原生音视频栈封装 |
| **输入格式** | • 音频：Opus（AOQ/WebRTC）、PCM（WebSocket）<br>• 视频：原始帧 / JPEG 编码帧（AOQ 支持自定义输入）<br>• 文本/指令：`session.update` 事件配置 | • 音频：16 kHz PCM（Base64 编码）<br>• 图像：JPG/JPEG（≤1080p，Base64 后 ≤256 KB，需在首段音频后发送）<br>• 文本/指令：标准化客户端事件（`session.update`, `input_audio_buffer.append` 等） |
| **输出格式** | • 文本：UTF-8 字符流<br>• 音频：Opus（AOQ/WebRTC）、PCM（WebSocket）<br>• 视频：AI 生成画面原始帧或 JPEG 流（AOQ 支持自定义播放）<br>• 多模态同步：支持音画严格时间对齐（AOQ 原生支持） | • 文本：`response.text.delta` / `response.text.done`<br>• 音频：固定 24 kHz PCM（`response.audio.delta`）<br>• **不支持视频输出**<br>• 输出模态仅限 `["text"]` 或 `["text","audio"]`，不可动态切换 |
| **支持模型** | • 全模态模型：<br> `qwen3.5-omni-plus-realtime`, `qwen3.5-omni-flash-realtime`, `qwen3.5-livetranslate-flash-realtime`<br>• 多模态套件：`multimodal-dialog`<br>• 独立 ASR/TTS：<br> ASR：`Qwen-Audio-3.0-ASR-Flash-Streaming`, `Fun-ASR-Realtime系列`<br> TTS：`CosyVoice系列`<br>• 实时语音对话模型：<br> `qwen-audio-3.0-realtime-plus`, `qwen-audio-3.0-realtime-flash` | • 专属 Omni 系列模型：<br> `qwen3.5-omni-realtime`, `qwen3.5-omni-plus-realtime`, `qwen3.5-omni-flash-realtime`, `qwen3-omni-flash-realtime`, `qwen-omni-turbo-realtime`<br>• **内置 ASR**：`qwen3-asr-flash-realtime`（不可替换）<br>• **不支持独立 TTS 模型调用**（TTS 与模型强绑定） |
| **API 端点与接入方式** | • 协议级端点分离：<br> AOQ：`https://dashscope.aliyuncs.com/api/v1/realtime/aoq/connect`（需服务端鉴权 + 凭证下发）<br> WebRTC：白名单专属 STUN/TURN Endpoint（需商务开通）<br> WebSocket：`wss://.../api-ws/v1/realtime`（标准 WebSocket 连接）<br>• 强依赖 SDK（AOQ/WebRTC）或手动信令（WebRTC） | • 统一 WebSocket 端点：<br> `wss://{WorkspaceId}.{Region}.maas.aliyuncs.com/api-ws/v1/realtime`<br>• 无专用 SDK，基于标准 WebSocket 客户端实现<br>• 事件驱动：所有交互通过 JSON-RPC 风格事件（`session.created`, `response.audio.delta` 等）完成 |
| **计费方式** | • 按 **会话时长（秒） + 模型调用次数** 双维度计费<br>• AOQ/WebRTC 会话按连接时长计费（含空闲期）；WebSocket 按实际媒体流传输时长计费<br>• ASR/TTS 模型单独计费（按音频时长） | • 按 **Token 数量 + 音频处理时长** 计费<br>• 输入 Token（文本+音频转录结果）、输出 Token（文本+音频合成等效 Token）均计入<br>• 音频处理时长 = ASR 耗时 + TTS 耗时（以毫秒为单位折算）<br>• **不区分协议或连接时长** |
| **典型场景** | • 原生 App 语音助手（iOS/Android/HarmonyOS）<br>• 浏览器端实时会议增强（背景降噪、实时字幕）<br>• 工业音视频质检（多模态联合分析）<br>• 需弱网对抗、端侧音视频深度定制的高要求场景 | • Web 应用/小程序实时对话（客服、教育陪练）<br>• 快速验证多模态对话逻辑（工具调用、联网搜索）<br>• 对视频无需求、聚焦语音+文本闭环的轻量级产品<br>• 需要语义级 VAD（`semantic_vad`）或主动引导（`idle_timeout_ms`）的交互设计 |

## 适用场景建议

### ✅ 推荐选用 **Realtime API** 当：
- 目标平台为 **原生移动应用（iOS/Android/HarmonyOS）**，且需极致低延迟（<200ms 端到端）与弱网鲁棒性；
- 业务涉及 **独立 ASR/TTS 模型选型或混搭**（例如：用 Fun-ASR 做方言识别 + CosyVoice 做情感合成）；
- 需要 **视频流输入/输出能力**（如 AI 教师实时生成手势动画、AR 场景叠加）；
- 要求 **端侧音视频链路完全可控**（自定义采集、前处理、播放器集成）；
- 已有成熟 WebRTC 基础设施，且仅需浏览器端语音对话（注意：WebRTC 不支持 ASR/TTS）。

### ✅ 推荐选用 **Omni Realtime API** 当：
- 主要运行环境为 **Web 浏览器或跨平台框架（React Native/Flutter）**，追求快速上线与轻量集成；
- 核心需求是 **语音+文本双模态闭环**，且接受统一 ASR/TTS 与模型强耦合；
- 需要 **语义级语音活动检测（`semantic_vad`）** 或 **静默超时主动引导**（`idle_timeout_ms`）提升对话自然度；
- 业务逻辑依赖 **工具调用（Function Calling）或联网搜索（`enable_search`）**，且使用 `qwen3.5-omni-realtime` 系列模型；
- 团队具备 WebSocket 事件处理经验，能自主管理状态机（如 VAD 切换、工具回调、响应消费）；
- 对视频无需求，且希望规避 Opus 插件集成、SDP 信令、ICE 连接等底层复杂度。

## 技术选型参考指南

| 选型考量项 | Realtime API | Omni Realtime API | 建议动作 |
|------------|--------------|-------------------|----------|
| **开发周期** | ⚠️ 中高（AOQ 需集成 SDK + Opus 插件；WebRTC 需信令开发） | ✅ 低（纯 WebSocket + JSON 事件，1 小时可跑通 Hello World） | 快速验证选 Omni；长期产品化选 Realtime |
| **维护成本** | ⚠️ 中高（协议兼容性、SDK 版本升级、Opus 编解码适配） | ✅ 低（协议单一，事件接口稳定，无客户端依赖） | 运维人力有限时优先 Omni |
| **功能扩展性** | ✅ 高（支持自定义音视频处理、多模型组合、协议级优化） | ⚠️ 中（模型能力由 Omni 系列限定，无法替换 ASR/TTS） | 需深度定制或未来扩展模型能力 → Realtime |
| **跨平台覆盖** | ✅ 全平台（AOQ：原生；WebRTC：浏览器；WebSocket：通用） | ✅ 广泛（任何支持 WebSocket 的环境） | 若需同时覆盖 App + Web → Realtime（三协议）更优 |
| **合规与安全** | ✅ 强（API Key 服务端下发、AOQ 端到端加密、Relay IP 调度） | ✅ 强（同 Realtime，基于统一鉴权体系） | 两者均满足金融/政务级安全要求 |

> **重要提醒**：  
> - WebRTC 协议在 Realtime API 中 **不支持 ASR/TTS 模型**，若需浏览器端语音合成，请选择 AOQ（通过 WebView 容器）或 Omni Realtime API；  
> - Omni Realtime API 的 `enable_search` 与 `tools` 功能 **互斥且仅限 `qwen3.5-omni-realtime` 系列**，选型时务必核对模型文档；  
> - Realtime API 的 AOQ 方案要求客户端 **必须监听 `session.updated` 后再启用媒体流**，否则服务端拒绝接收数据——这是常见集成失败根源，请严格遵循 SDK 控制逻辑。  

根据您的具体技术栈、交付节奏与长期演进规划，合理匹配方案可显著降低开发风险、提升用户体验一致性。建议初期用 Omni Realtime API 快速验证核心交互逻辑，再平滑迁移至 Realtime API 承载高阶能力。

## 被对比主题页

- [realtime api user guide](../api/realtime-api-user-guide.md)
- [omni realtime api](../api/omni-realtime-api.md)



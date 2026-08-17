# 实时 API 方案对比：Omni Realtime API vs Realtime API User Guide

本对比旨在帮助开发者清晰区分百炼平台两大实时交互技术路径：**Omni Realtime API**（聚焦多模态语音助手级端到端实时会话）与 **Realtime API User Guide**（面向全场景、多协议、可组合的实时 AI 服务基础设施）。二者定位不同——前者是**特定模型族（Qwen-Omni-Realtime 系列）的专用 WebSocket 接口规范**，后者是**覆盖 ASR/TTS/翻译/对话等多类模型、支持 AOQ/WebRTC/WebSocket 三协议的通用实时能力框架**。理解差异有助于避免误用（如在 WebRTC 中调用 ASR 模型）、规避鉴权风险（如客户端硬埋 API Key），并实现精准技术选型。

## 关键维度对比

| 维度 | Omni Realtime API | Realtime API User Guide |
|------|-------------------|--------------------------|
| **本质定位** | `qwen3.5-omni-*` 系列模型专属的、事件驱动的 WebSocket 实时会话接口（*模型绑定型 API*） | 覆盖 ASR/TTS/翻译/多模态对话等全栈实时能力的**协议无关抽象层**，统一事件模型 + 多协议接入支持（*能力平台型 API*） |
| **核心协议** | 仅支持 **WebSocket**（强制依赖 DashScope SDK 的 `RealtimeClient`） | 支持 **AOQ（MOQ）、WebRTC、WebSocket** 三种协议，需通过请求头 `x-dashscope-rtc-transport` 显式指定 |
| **输入格式** | • 音频流：PCM/WAV（8k/16k/24k/48k Hz，`qwen3.5-omni-plus/flash` 支持自定义）<br>• 图像：JPG/JPEG（≤1080p，Base64 编码 ≤256KB）<br>• 文本：`instructions` 字段或 `input_text` 事件 | • 音频流：**当前仅支持 PCM**（所有协议均不支持 WAV；AOQ/WebRTC 对采样率有硬件/网络适配要求）<br>• 图像：仅 `multimodal-dialog` 和 `qwen3.5-omni-*` 模型支持（同 Omni）<br>• 文本：`input_text` 或指令注入 |
| **输出格式** | • 文本：`response.text.delta` / `response.text.done`<br>• 音频：PCM/WAV（多采样率可选，`qwen3.5-omni-plus/flash` 支持）<br>• 工具调用：`function_call` 事件 + 客户端回传结果 | • 文本：`response.text.delta`（全协议一致）<br>• 音频：PCM（**所有协议均不支持 WAV 输出**；AOQ/WebRTC 使用 Opus 封装，WebSocket 为裸 PCM）<br>• ASR 结果：`transcript` 事件（AOQ/WebSocket 支持，WebRTC 不支持）<br>• TTS 结果：`response.audio.delta`（AOQ/WebSocket 支持，WebRTC 不支持） |
| **支持模型** | 仅限 `qwen3.5-omni-plus-realtime`、`qwen3.5-omni-flash-realtime`、`qwen-omni-turbo-realtime` 三款模型 | 全面覆盖：<br>• 多模态：`qwen3.5-omni-*`, `multimodal-dialog`<br>• 翻译：`qwen3.5-livetranslate-flash-realtime`<br>• ASR：`Qwen-Audio-3.0-ASR-Flash-Streaming`, `Fun-ASR-Realtime`（**AOQ/WebSocket only**）<br>• TTS：`CosyVoice`, `qwen-audio-3.0-tts-*`（**AOQ/WebSocket only**）<br>• 语音对话：`qwen-audio-3.0-realtime-*` |
| **API 端点与建连** | WebSocket URL 固定（由 DashScope SDK 自动构造），建连即进入会话生命周期 | • AOQ：需服务端调用网关 `allocate` 获取 `aoqTokenForClient`，客户端用 AOQ SDK 连接<br>• WebRTC：标准 SDP 协商流程<br>• WebSocket：SDK `RealtimeClient` 初始化，传入 `model` + `api_key` 即可 |
| **鉴权方式** | `Authorization: Bearer <API_KEY>`（**直接暴露于客户端 SDK 调用中**） | • AOQ：**API Key 严禁出现在客户端**，必须由服务端换取 `aoqTokenForClient` 后传递给客户端<br>• WebRTC/WebSocket：`Authorization: Bearer <API_KEY>`（但 WebRTC 建连仍需服务端签发临时凭证） |
| **VAD 能力** | • `server_vad`：全部模型支持<br>• `semantic_vad`：仅 `qwen3.5-omni-plus-realtime` 支持（语义级静音检测） | • `server_vad`：全模型支持<br>• `semantic_vad`：文档明确推荐使用（尤其在 `qwen3.5-omni-*` 场景），但未限定模型范围；实际支持取决于所选模型 |
| **高级功能** | • 联网搜索（`enable_search`）：仅 `qwen3.5-omni-plus-realtime` 支持，且与 `tools` 互斥<br>• 工具调用（`tools`）：仅 `qwen3.5-omni-plus-realtime` 支持，需客户端显式 `response.create`<br>• 声音复刻集成：支持传入 `voice` 参数 | • 联网搜索：未在文档中作为独立能力提及（由模型自身能力决定）<br>• 工具调用：未在文档中作为通用能力描述（属 `qwen3.5-omni-*` 模型特性）<br>• 声音复刻：同 Omni（通过 `voice` 参数） |
| **采样参数控制** | • `qwen3.5-omni-plus-realtime`：全量支持 `temperature`/`top_p`/`top_k`/`max_tokens`/`repetition_penalty`/`presence_penalty`/`seed`<br>• `qwen3.5-omni-flash-realtime`：支持除 `max_tokens` 外的其余参数<br>• `qwen-omni-turbo-realtime`：**完全不支持修改任何采样参数** | 未在通用文档中定义采样参数字段；参数控制能力**完全继承自所选模型**（例如使用 `qwen3.5-omni-plus-realtime` 时，其参数可用性与 Omni API 一致） |
| **计费方式** | 按 **实际消耗的音频时长（秒） + 文本 [Token](../concepts/token.md) 数** 计费（多模态叠加计费），具体以控制台定价页为准 | 按 **所选模型类型 + 协议 + 实际资源消耗** 计费：<br>• ASR/TTS：按音频时长（秒）计费<br>• 多模态对话：按音频时长 + 文本 [Token](../concepts/token.md) 数计费<br>• 翻译：按字符数或音频时长计费<br>• *协议本身不额外计费，但 AOQ 在弱网下更省带宽，间接影响成本* |
| **典型场景** | • 语音助手（手机/车机/智能硬件）<br>• 高拟真智能客服（需语音+图像+工具协同）<br>• 实时音视频会议中的多模态交互插件（如会议纪要+发言人识别+内容摘要） | • 移动端原生 App（Android/iOS/HarmonyOS）：首选 **AOQ**（低延迟、强弱网适应）<br>• 浏览器 Web 应用：首选 **WebRTC**（零 SDK、利用浏览器原生能力）<br>• 服务端集成/快速验证/跨平台轻量应用：选用 **WebSocket**<br>• 需要分离 ASR/TTS 能力的系统（如自研语音前端 + 百炼 ASR）：必须选 AOQ 或 WebSocket |

## 各方案适用场景建议

### ✅ 选择 Omni Realtime API 当且仅当：
- 你的业务**严格限定于 `qwen3.5-omni-*` 系列模型**，且需要发挥其**多模态（语音+图像+文本）、语义 VAD、联网搜索、工具调用**等深度能力；
- 你已确定采用 **WebSocket 协议**，且能接受客户端直接使用 API Key（无服务端鉴权代理需求）；
- 你追求**最简接入路径**：无需关心协议选型、SDP 协商、Opus 插件集成等底层细节，专注会话逻辑开发；
- 你正在构建**端到端语音优先的智能体（Agent）**，而非拆解 ASR/TTS/LLM 等原子能力。

### ✅ 选择 Realtime API User Guide 当且仅当：
- 你需要**灵活组合不同 AI 能力**（例如：前端用 WebRTC 采集语音 → 后端用 AOQ 调用 ASR → 再调用 LLM → 最后用 TTS 合成返回），或**支持多终端形态**（App + Web + 小程序）；
- 你对**传输可靠性、弱网表现、端到端延迟有严苛要求**（AOQ 是唯一满足极致要求的协议）；
- 你有**安全合规强约束**，必须将 API Key 保留在服务端，禁止任何客户端暴露（AOQ 强制要求 token 中转）；
- 你需要**接入非 Omni 模型**（如纯 ASR、纯 TTS、实时翻译），或未来计划扩展能力矩阵；
- 你正在构建**企业级实时 AI 中间件**，需统一管理协议、鉴权、熔断、监控等基础设施能力。

## 技术选型参考（致开发者）

| 你的需求 | 推荐方案 | 关键原因 |
|----------|-----------|-----------|
| “我要快速上线一个语音问答小程序，只用 Qwen-Omni 模型，3 天内交付” | **Omni Realtime API** | SDK 开箱即用，WebSocket 一行代码初始化，无需处理协议、鉴权、媒体流控制等复杂链路 |
| “我们的金融客服 App 需在 4G 弱网下稳定运行，且必须隐藏 API Key” | **Realtime API (AOQ)** | AOQ 协议专为移动端优化，内置抗丢包/回声消除；强制服务端鉴权，满足金融级安全审计要求 |
| “我们已有 WebRTC 视频会议系统，想叠加实时字幕和发言摘要” | **Realtime API (WebRTC)** | 复用现有 WebRTC 基础设施，零 SDK 集成，直接在 `ontrack` 流上注入实时 ASR/TTS 事件 |
| “我们需要把 ASR 结果喂给自研 NLU 引擎，再把指令发给百炼 TTS 合成” | **Realtime API (AOQ or WebSocket)** | Omni API 不提供独立 ASR/TTS 能力；Realtime API 允许按需调用 `Fun-ASR-Realtime` + `CosyVoice` 等原子模型 |
| “我们想做多模态教育硬件，需同时处理学生语音、手写板图像、实验视频帧” | **Omni Realtime API**（搭配 `qwen3.5-omni-plus-realtime`） | 唯一支持图像（≤1080p）+ 音频流 + 文本指令三者同步输入的接口，且 `semantic_vad` 可精准捕捉学生思考停顿 |
| “我们是 SaaS 厂商，需为不同客户配置不同模型（有的要 ASR，有的要翻译，有的要 Omni）” | **Realtime API** | 统一 API 网关 + 协议抽象层，客户只需切换 `model` 参数和 `x-dashscope-rtc-transport`，后端逻辑完全复用 |

> **重要提醒**：  
> - ❗ **切勿混用**：不要在 Realtime API 的 WebRTC 连接中尝试调用 `Fun-ASR-Realtime` 模型（文档明确不支持），也不要期望 Omni API 提供 AOQ 的弱网优化能力。  
> - 🔐 **安全红线**：若选择 Realtime API 的 AOQ 协议，**客户端代码中绝对不可出现 `Bearer sk-xxx`**；必须通过服务端 allocate 接口获取临时 token。  
> - 📦 **依赖检查**：AOQ SDK 集成时，务必加载 `libPluginOpus`（Android/iOS）或 `PluginOpus.framework`（iOS），否则 ASR/TTS 功能静默失效。  
> - 🧪 **验证先行**：新项目启动前，建议先用 Realtime API 的 WebSocket 模式快速验证模型效果，再根据性能/安全/终端需求升级至 AOQ 或 WebRTC。

## 被对比主题页

- [omni realtime api](../api/omni-realtime-api.md)
- [realtime api user guide](../api/realtime-api-user-guide.md)



# 实时 API 方案对比：Omni Realtime vs Realtime API

本文旨在帮助开发者清晰理解百炼平台两大实时交互能力方案的核心差异，辅助技术选型决策。随着语音助手、智能座舱、远程教育、实时翻译等低延迟多模态场景快速发展，选择适配业务需求的实时 API 架构至关重要。**Omni Realtime API** 是面向全模态语音助手深度优化的 WebSocket 原生接口；而 **Realtime API** 是统一抽象层下的多协议（AOQ/WebRTC/WebSocket）通用实时能力平台，覆盖更广的模型类型与终端生态。二者定位互补，非简单替代关系。

---

## 关键维度对比

| 维度 | Omni Realtime API | Realtime API |
|------|-------------------|--------------|
| **核心协议** | 仅支持 WebSocket（强制） | 支持三类协议：<br>• AOQ（QUIC，移动端首选）<br>• WebRTC（浏览器端原生）<br>• WebSocket（服务端/快速验证） |
| **输入格式** | • 音频：16kHz PCM 单声道（必需）<br>• 图像：JPG/JPEG，Base64 编码 ≤256KB<br>• 文本：通过 `input_text` 事件（可选） | • 音频：16kHz PCM（AOQ/WebSocket），WebRTC 自动适配（支持 Opus 等）<br>• 图像：仅部分模型（如 `multimodal-dialog`）支持，需按模型文档确认<br>• 文本/结构化数据：通过 `session.update` 或 DataChannel 传递 |
| **输出格式** | • 文本：UTF-8 字符串流（`response.text.delta`）<br>• 音频：24kHz PCM 流（`response.audio.delta`）<br>• 工具调用/搜索结果：结构化 JSON 事件 | • 文本：UTF-8 字符串流（各协议一致）<br>• 音频：24kHz PCM（AOQ/WebSocket），WebRTC 输出为 Opus 流（可配置）<br>• 多模态响应：依模型能力而定（如 ASR 输出 `transcript`，TTS 输出 `audio`） |
| **支持模型** | 仅 `qwen3.5-omni-realtime` / `qwen3-omni-flash-realtime` / `qwen-omni-turbo-realtime` 三类实时 Omni 模型系列 | 广泛覆盖：<br>• 全模态：`qwen3.5-omni-plus-realtime`, `qwen3.5-omni-flash-realtime`<br>• 语音翻译：`qwen3.5-livetranslate-flash-realtime`<br>• ASR：`Qwen-Audio-3.0-ASR-Flash-Streaming`, `Fun-ASR-Realtime`<br>• TTS：`CosyVoice` 系列<br>• 对话：`qwen-audio-3.0-realtime-plus` 等<br>• 多模态套件：`multimodal-dialog` |
| **VAD 能力** | • `server_vad`（基础静音检测）<br>• `semantic_vad`（语义级起止判断，仅 `qwen3.5-omni-realtime` 支持）<br>• 支持 `idle_timeout_ms` 主动引导 | • 全协议统一支持 `semantic_vad`（推荐）与 `server_vad`<br>• AOQ 内置 AEC/降噪，VAD 更鲁棒；WebRTC 依赖浏览器音频处理链 |
| **工具调用 & 联网搜索** | • `tools`：仅 `qwen3.5-omni-realtime` 支持<br>• `enable_search`：仅 `qwen3.5-omni-realtime` 支持，且与 `tools` 互斥 | • 工具调用：由具体模型决定（如 `multimodal-dialog` 支持[函数调用](../concepts/function-calling.md)）<br>• 联网搜索：当前未作为通用能力开放，需模型显式支持（如部分 Omni Plus 模型） |
| **API 端点** | WebSocket 专属地址：<br>`wss://{WorkspaceId}.{region}.maas.aliyuncs.com/api-ws/v1/realtime` | 协议差异化端点：<br>• AOQ：`allocate` 接口获取动态 Relay 地址<br>• WebRTC：`https://{endpoint}/api/v1/webrtc/realtime?model=xxx`<br>• WebSocket：`wss://{WorkspaceId}.{region}.maas.aliyuncs.com/api-ws/v1/realtime`（与 Omni Realtime 共享域名，但路由与鉴权逻辑独立） |
| **计费方式** | 按 **实际音频处理时长（秒） + 生成 [Token](../concepts/token.md) 数** 双维度计费：<br>• 音频输入/输出流时长计入“语音时长”<br>• 文本生成按 `output_tokens` 计费<br>• 工具调用、图像解析等附加操作单独计费 | 按 **模型调用粒度 + 协议类型** 计费：<br>• ASR/TTS/Translation 等按“请求次数”或“音频时长”计费<br>• 全模态对话按“会话时长”或“[Token](../concepts/token.md) 数”计费（依模型定价策略）<br>• AOQ 协议额外收取连接维持费用（弱网优化成本） |
| **典型场景** | • 高沉浸语音助手（带 VAD+工具+多模态）<br>• 低延迟客服机器人（需语义级中断响应）<br>• 教育陪练应用（语音+图像联合理解） | • 跨端语音应用（iOS/Android/Web 全覆盖）<br>• 实时字幕/同传系统（ASR+TTS 组合）<br>• 智能硬件 SDK 集成（AOQ 提供强弱网保障）<br>• 快速 PoC 验证（WebSocket 最简接入） |

---

## 适用场景建议

### ✅ 选择 Omni Realtime API 当：
- 你的产品是**纯语音助手形态**，核心诉求是极致低延迟、语义级 VAD、工具调用与联网搜索闭环；
- 你已确定使用 `qwen3.5-omni-realtime` 等 Omni 系列模型，且需精细控制 `temperature`/`top_p`/`presence_penalty` 等生成参数；
- 你具备 WebSocket 客户端开发能力，且终端环境稳定（如桌面应用、可控内网设备）；
- 你需要在单次会话中混合处理语音、文本、图像（如“拍题讲解”场景），并要求模型联合推理。

> ⚠️ 注意：不适用于需浏览器原生支持、弱网移动环境、或需复用现有 WebRTC 基础设施的项目。

### ✅ 选择 Realtime API 当：
- 你需要**一套 API 同时支撑 iOS/Android/Web/HarmonyOS 多端**，尤其重视移动端弱网稳定性（AOQ）或浏览器零依赖（WebRTC）；
- 你的业务涉及**ASR、TTS、翻译、对话等多类型模型组合**（例如：先 ASR → 再 LLM → 最后 TTS）；
- 你正在构建**标准化 AI 中间件或 SDK**，需要协议抽象与统一事件模型降低维护成本；
- 你是初创团队或 PoC 阶段，希望用 WebSocket 快速验证，后续平滑迁移到 AOQ/WebRTC。

> ⚠️ 注意：若仅需 `qwen-omni-turbo-realtime` 这类参数不可调的极简模型，两者均可，但 Realtime API 的 WebSocket 接入路径更轻量。

---

## 技术选型参考（面向开发者）

| 你的需求 | 推荐方案 | 理由 |
|----------|-----------|------|
| “我要做一个带声音复刻和工具调用的语音助教 App，用户说‘查下这张图里的股票代码’，模型需看图+联网+调用股票 API” | **Omni Realtime API** | 唯一支持 `semantic_vad` + `tools` + `input_image_buffer` + 声音复刻 ID 的组合；`qwen3.5-omni-realtime` 是当前唯一满足全链路的模型。 |
| “我需要在微信小程序里嵌入实时语音对话，并兼容安卓/iOS App，还要支持离线语音识别兜底” | **Realtime API（WebRTC + AOQ）** | WebRTC 原生支持小程序；AOQ 提供移动端离线/弱网能力；统一模型注册体系便于跨端切换 ASR/TTS/LLM。 |
| “我们是智能音箱厂商，已有自研音频采集栈，要求超低延迟（<300ms）和抗回声能力” | **Realtime API（AOQ 协议）** | AOQ 内置专业级 AEC、噪声抑制与网络自适应算法，SDK 提供 `customAudioCapture` 接口无缝对接硬件采集链。 |
| “我正在用 Python 写一个后台语音质检服务，只需把录音流喂给模型，拿到文本和情绪分析结果” | **Realtime API（WebSocket）** | 无需客户端 SDK，直接用 DashScope Python SDK 连接；可灵活选用 `Fun-ASR-Realtime` + `qwen3.5-omni-flash-realtime` 组合，计费透明。 |
| “我们想快速验证 Qwen-Omni 的多模态能力，不关心部署细节” | **Omni Realtime API（WebSocket）** | 文档最完整、示例最丰富；Python/JS SDK 开箱即用；`qwen3-omni-flash-realtime` 默认配置开箱可用，适合 1 小时内跑通 demo。 |

> 💡 **终极建议**：  
> - **从模型出发选 API**：先确认业务必须使用的模型（如 `qwen3.5-omni-realtime` → Omni Realtime；`CosyVoice` → Realtime API）；  
> - **从终端出发定协议**：移动端优先 AOQ，Web 优先 WebRTC，服务端/原型优先 WebSocket；  
> - **生产环境务必压测**：实测不同网络条件下 `first-audio-latency` 和 `end-to-end-delay`，避免仅依赖文档标称值。

---  
*最后更新：2024年6月*  
*本文档依据百炼平台 v3.5 实时能力文档集编写，具体以控制台最新模型列表与 SDK 版本为准。*

## 被对比主题页

- [omni realtime api](../api/omni-realtime-api.md)
- [realtime api user guide](../api/realtime-api-user-guide.md)



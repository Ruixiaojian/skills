# 实时 API 方案对比：Realtime API vs Omni Realtime API

本文旨在帮助开发者清晰理解百炼平台两类核心实时交互能力的定位差异与技术边界，为语音对话、多模态智能体、实时音视频应用等场景提供可落地的技术选型依据。随着 Qwen-Omni 系列模型能力持续增强，平台同步演进出了面向不同架构范式与工程约束的实时 API 路径：**Realtime API**（协议灵活、终端适配广、功能解耦强）与 **Omni Realtime API**（协议统一、语义深度集成、会话抽象高）。二者并非简单替代关系，而是在模型能力、传输层控制粒度、开发复杂度与运维成本之间做出的不同权衡。

---

## 关键维度对比

| 维度 | Realtime API | Omni Realtime API |
|------|--------------|-------------------|
| **协议支持** | ✅ AOQ（自研低延迟协议）、✅ WebRTC、✅ WebSocket（三选一） | ❌ 仅支持 WebSocket（强制统一） |
| **输入格式** | - 音频：PCM（16kHz/24kHz，依模型而定）<br>- 图像：不支持原生图像输入（需通过 `multimodal-dialog` 等独立能力接入）<br>- 文本：支持 `session.update` 指令注入 | ✅ 音频：PCM（16kHz）<br>✅ 图像：JPG/JPEG（≤1080p，Base64 编码后 ≤256KB）<br>✅ 文本：`session.update` + `input_text` 事件 |
| **输出格式** | - 文本：流式 `text.delta`<br>- 音频：PCM（16kHz 或 24kHz，依模型与配置）<br>- 视频/图像：不直接输出（需结合 `multimodal-dialog` 或自定义渲染） | ✅ 文本：`text.delta` + `text.done`<br>✅ 音频：PCM（24kHz）<br>❌ 不支持原生视频/图像输出（仅支持图像作为输入上下文） |
| **支持模型/能力** | - 全模态：`qwen3.5-omni-plus-realtime`, `qwen3.5-omni-flash-realtime`<br>- 语音翻译：`qwen3.5-livetranslate-flash-realtime`<br>- ASR/TTS：独立模型（如 `Fun-ASR-Realtime`, `CosyVoice`）<br>- 多模态套件：`multimodal-dialog`<br>→ **能力按协议分层支持，WebRTC 不支持 ASR/TTS** | - 全模态旗舰：`qwen3.5-omni-realtime`（支持 `semantic_vad`、`tools`、`enable_search`）<br>- 轻量高吞吐：`qwen3-omni-flash-realtime`（支持 `smooth_output`，不支持搜索/VAD 语义模式）<br>- 极致低延迟：`qwen-omni-turbo-realtime`（参数不可调，仅基础语音交互）<br>→ **能力严格绑定模型，无独立 ASR/TTS 模块** |
| **API 端点与接入方式** | - AOQ：需集成原生 SDK（Android/iOS/HarmonyOS/Linux），依赖 `aoqTokenForClient` 和 Relay 配置<br>- WebRTC：需白名单开通，SDP 协商 + 自定义信令，Endpoint 由商务提供<br>- WebSocket：最简路径，DashScope SDK 直连，适合服务端或原型验证 | - 统一 WebSocket 端点：`wss://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api-ws/v1/realtime`（**必须使用新域名**）<br>- 无 SDK 强依赖，但推荐使用官方 Python/Java SDK 封装事件协议<br>- 所有交互基于标准化事件（`session.created`, `session.update`, `input_audio`, `response.text.delta` 等） |
| **语音活动检测（VAD）** | - 支持 `semantic_vad`（全协议）<br>- `server_vad`（AOQ/WebSocket）<br>- WebRTC 使用浏览器原生 VAD 或服务端 fallback | - `server_vad`：通用支持，含 `threshold` / `silence_duration_ms` / `idle_timeout_ms`（后两者仅限 `plus`/`flash` + `server_vad`）<br>- `semantic_vad`：**仅 `qwen3.5-omni-realtime` 支持**，更精准但延迟略高 |
| **高级功能支持** | - [工具调用](../concepts/tool-use.md)（`tools`）：需配合 `multimodal-dialog` 或自定义编排<br>- 联网搜索：需在业务侧实现，非原生能力<br>- 声音复刻：支持，但需严格匹配 `target_model`（如 `qwen3.5-omni-plus-realtime`） | - ✅ 原生[工具调用](../concepts/tool-use.md)（`tools`）：模型自主触发，客户端回传结果后生成最终响应<br>- ✅ 原生联网搜索（`enable_search`）：仅 `qwen3.5-omni-realtime`，与 `tools` 互斥<br>- ✅ 声音复刻：深度集成，音色与驱动模型强绑定，失败提示明确 |
| **计费方式** | - 按 **实际调用模型 + 传输协议 + 资源消耗** 分项计费<br>- AOQ/WebRTC：含连接时长、中继带宽、媒体处理单元（MPU）<br>- WebSocket：按 token + 音频时长（秒）计费<br>- 各协议定价独立，详见控制台最新资费页 | - 统一按 **会话生命周期内模型调用 + 音频 I/O 时长** 计费<br>- 计费粒度为：文本 token（输入/输出）、音频秒（输入/输出）、图像请求次数<br>- 不区分传输协议开销，无额外中继/连接费 |
| **典型场景** | - 移动端原生 App 的语音助手（强弱网对抗、AEC/降噪刚需）<br>- 浏览器端音视频会议嵌入 AI 客服（复用现有 WebRTC 基础设施）<br>- 快速验证 ASR/TTS 独立能力（如实时字幕、TTS 播报）<br>- 多模态对话需拆解为 ASR → LLM → TTS 的流水线编排 | - 全栈可控的智能客服系统（统一 WebSocket + 事件驱动）<br>- 多模态语音助手（语音+图片提问，如拍照问诊、商品识别问答）<br>- 需要语义级 VAD 或[工具调用](../concepts/tool-use.md)的对话机器人（如订机票、查订单）<br>- 对部署一致性要求高、希望减少协议适配成本的服务端集成 |

---

## 适用场景建议

### ✅ 选择 **Realtime API** 当：
- 你的应用是 **原生移动 App（iOS/Android/HarmonyOS）**，且对弱网、抖动、回声消除（AEC）、本地降噪有硬性要求 → **优先选 AOQ**；
- 你已构建了成熟的 **WebRTC 音视频基础设施**（如会议 SDK、直播推流），希望最小改动集成 AI 能力 → **选 WebRTC 协议**；
- 你需要 **独立调用 ASR 或 TTS 模块**（例如仅做实时转写，或仅做语音播报），不依赖完整对话流程 → Realtime API 提供专用模型；
- 你正在快速验证某个模型能力（如 `qwen3.5-livetranslate-flash-realtime`），追求最低接入门槛 → **WebSocket 协议 + DashScope SDK 即可启动**；
- 你需精细控制媒体流（如混音、TTS 注入、屏幕共享帧注入）→ AOQ SDK 提供 `pushAudioExternalStreamData` 等底层接口。

### ✅ 选择 **Omni Realtime API** 当：
- 你构建的是 **端到端多模态对话系统**，需同时处理语音、图像、文本，并期望模型自动决策是否调用工具或搜索 → **Omni 是唯一原生支持方案**；
- 你追求 **开发与运维一致性**：所有终端（Web/H5/小程序/服务端）均通过同一 WebSocket 协议接入，无需维护多套协议逻辑；
- 你需要 **语义级语音活动检测（`semantic_vad`）** 或 **模型自主触发函数（`tools`）** 等高级对话能力 → 仅 `qwen3.5-omni-realtime` 在 Omni API 中提供；
- 你的团队熟悉事件驱动编程模型，能接受 `append_audio` → `response.text.delta` → `response.audio.delta` 的标准事件流，而非传统 Request/Response；
- 你希望降低长期维护成本，避免因协议差异导致的兼容性问题（如 WebRTC 版本碎片化、AOQ SDK 升级适配）。

> ⚠️ 注意：若需同时使用 ASR 和 TTS（如“听清用户说的，再合成回答”），**Realtime API 更灵活**（可分别调用 `Fun-ASR-Realtime` + `CosyVoice`）；而 Omni Realtime API 将 ASR/TTS 与 LLM 深度耦合，无法单独剥离使用。

---

## 技术选型参考（面向开发者）

| 你的需求 | 推荐方案 | 关键理由 |
|----------|----------|----------|
| “我要做一个 iOS 语音助手 App，用户在地铁里也能稳定说话” | **Realtime API + AOQ** | AOQ 内置弱网重传、AEC、动态码率，实测 30% 丢包下仍可维持可用 VAD 与 TTS 连续性 |
| “我在 Electron 桌面应用里嵌入实时翻译，已有 WebRTC 音视频模块” | **Realtime API + WebRTC** | 复用现有 SDP 信令与 PeerConnection，只需扩展 `onTrack` 处理 AI 输出流，零协议改造 |
| “我用 Python 写后台服务，想快速测试 `qwen3.5-omni-flash-realtime` 的响应速度” | **Realtime API + WebSocket**（或 **Omni Realtime API**） | 前者 SDK 更轻量（DashScope）；后者语义更完整（支持 `smooth_output`），但需处理事件协议 |
| “我要开发一个支持拍照提问的客服 H5 页面：用户拍商品图 + 语音问‘这个能退货吗？’” | **Omni Realtime API** | 唯一支持 `input_image` + `input_audio` 同步输入的方案，且 `qwen3.5-omni-realtime` 可联合理解图文语音 |
| “我的对话机器人需要调用天气 API 和订单查询接口，希望模型自己决定何时调用” | **Omni Realtime API + `qwen3.5-omni-realtime`** | `tools` 字段声明函数，模型输出 `tool_calls` 事件，客户端执行后回传 `tool_result`，流程完全标准化 |
| “我只需要把用户语音实时转成文字，不涉及对话或合成” | **Realtime API + `Fun-ASR-Realtime`（AOQ/WebSocket）** | Omni Realtime API 不提供纯 ASR 模型，必须走完整 `audio→text→audio` 流程，成本与延迟均更高 |

📌 **最后建议**：  
- 新项目优先评估 **Omni Realtime API** —— 它代表百炼平台实时能力的演进方向，文档完备、SDK 统一、功能收敛；  
- 存量项目或有特殊协议依赖（如已上线 AOQ App、WebRTC 会议系统），请继续使用 **Realtime API**，其稳定性与终端适配能力经过大规模验证；  
- 两者模型能力正快速对齐（如 `qwen3.5-omni-realtime` 同时支持 Realtime API 与 Omni Realtime API），未来可通过切换协议层平滑迁移。

## 被对比主题页

- [realtime api user guide](../api/realtime-api-user-guide.md)
- [omni realtime api](../api/omni-realtime-api.md)



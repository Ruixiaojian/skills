# 实时 API 方案对比：Omni Realtime API vs Realtime API User Guide

## 对比目的与背景

为帮助开发者在百炼平台快速、准确地选择适合业务需求的实时交互方案，本文对两类核心实时能力接口进行系统性对比分析：  
- **Omni Realtime API**（`api/omni-realtime-api.md`）：面向端到端[多模态](../concepts/multi-modal.md)智能体的**一体化、开箱即用型实时对话接口**，聚焦“语音/音视频输入 → 语义理解 → 工具调用/联网搜索 → 文本+音频输出”的全链路闭环。  
- **Realtime API User Guide**（`api/realtime-api-user-guide.md`）：面向工程集成的**协议级实时通信框架指南**，定义 WebSocket / WebRTC / AOQ 三种传输协议的能力边界、接入范式与模型兼容矩阵，强调**跨终端、弱网鲁棒性与协议可选性**。

二者并非互斥替代关系，而是**抽象层级不同、定位互补的技术方案**：Omni Realtime API 是构建于 Realtime API 协议栈之上的高阶封装；而 Realtime API User Guide 是底层协议能力的统一说明文档。本对比旨在厘清技术边界，避免因概念混淆导致选型偏差。

---

## 关键维度对比表

| 维度 | Omni Realtime API | Realtime API User Guide |
|------|-------------------|--------------------------|
| **本质定位** | 面向场景的**高阶 SDK 封装接口**（Python/Java SDK 主导），提供预编排的[多模态](../concepts/multi-modal.md)对话流水线 | 面向架构的**协议能力说明书**，定义 WebSocket / WebRTC / AOQ 三类传输层标准及模型支持矩阵 |
| **输入格式** | 支持 `append_audio`（Base64 PCM）、`append_video`（H.264 编码帧或原始 I420/NV12 帧）；VAD 模式下自动分段 | 协议相关：<br>• WebSocket：Base64 PCM 音频 + 可选视频帧<br>• WebRTC：MediaStream 或 Raw Video Frame（I420/BGRA）<br>• AOQ：支持外部注入原始音频帧（PCM/I2S）或编码帧（AAC/H.264） |
| **输出格式** | 固定流式事件结构：`response.text.delta`、`response.audio.delta`、`response.function_call_arguments.*` 等；支持 `TEXT` + `AUDIO` 同步输出 | 协议相关：<br>• WebSocket：JSON 事件流（含 `text`/`audio` 字段）<br>• WebRTC：DataChannel 传输文本 + AudioTrack 输出合成语音<br>• AOQ：混合通道（`text` via DataChannel, `audio` via AudioTrack, `video` via VideoTrack） |
| **支持模型** | 仅限 `qwen3.5-omni-*` 系列实时模型（如 `qwen3.5-omni-realtime`, `qwen3.5-omni-flash-realtime` 等），且功能严格按模型版本隔离 | 覆盖更广：<br>• 全模态模型（`qwen3.5-omni-*`, `qwen3.5-livetranslate-flash-realtime`）→ 三协议均支持<br>• Fun-ASR / CosyVoice / `qwen-audio-3.0-realtime-plus` → **仅 WebSocket 支持**<br>• `multimodal-dialog` 套件 → **仅 WebSocket/WebRTC 支持，不支持 AOQ** |
| **API 端点** | 固定 WebSocket 地址：<br>`wss://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api-ws/v1/realtime`（地域专属域名） | 协议差异化：<br>• WebSocket：同上，但模型可通过 URL Query（`?model=xxx`）或消息体指定<br>• WebRTC：`POST /v1/realtime/webrtc/offer` 获取 SDP，建连后通过 DataChannel 通信<br>• AOQ：需先调用 `POST /v1/realtime/aoq/allocate` 获取 `sid` 和 `aoqTokenForClient`，再连接 AOQ 服务节点 |
| **计费方式** | 按**实际消耗的 token 数量 + 音频处理时长（秒）** 计费（含 ASR/TTS/LLM 推理），模型不同单价不同；`qwen-omni-turbo-realtime` 按会话时长阶梯计费 | **统一按模型调用粒度计费**，与所选协议无关；但 AOQ/WebRTC 的媒体传输带宽、信令调用等基础资源不额外计费（计入百炼平台基础配额） |
| **典型场景** | 智能客服坐席助手、AI 会议纪要员、语音驱动的虚拟数字人（需工具调用/联网搜索/声音复刻） | <ul><li>**WebSocket**：后台语音质检、IVR 系统集成、快速 PoC 验证</li><li>**WebRTC**：浏览器端在线教育互动白板、远程医疗问诊、Web 端虚拟主播</li><li>**AOQ**：移动端音视频社交 App、车载语音助手、鸿蒙设备本地化 AI 交互</li></ul> |
| **VAD 能力** | 提供 `server_vad`（服务端静音检测）和 `semantic_vad`（语义级说话人意图识别）；后者**仅 `qwen3.5-omni-realtime` 支持** | `semantic_vad` 在三协议中均可用（需模型支持），但 `turn_detection.type` 参数需在 `session.update` 中显式设置；`server_vad` 为默认回退选项 |
| **开发者控制粒度** | **低控制粒度**：SDK 自动管理连接、会话生命周期、媒体缓冲区提交、响应流解析；手动模式需显式 `commit()`，但仍受限于 Omni 协议语义 | **高控制粒度**：WebRTC/AOQ 允许完全接管媒体采集、编码、网络传输（如 AOQ 支持 `isExternal=true` 注入自定义音频帧、WebRTC 支持 `RTCPeerConnection` 级配置） |
| **SDK 支持** | 官方提供 Python / Java SDK，封装连接、会话、事件回调全流程；无 JS SDK | 提供：<br>• WebSocket：DashScope Python/Java SDK<br>• WebRTC：TypeScript SDK（基于 Web API）<br>• AOQ：Android/iOS/HarmonyOS 原生 SDK（含 C++ 底层接口） |

---

## 适用场景建议

### ✅ 选择 Omni Realtime API 当：
- 业务目标是快速上线一个**具备完整 AI 对话能力的语音/音视频应用**（如客服机器人、会议助理），且无需深度定制媒体链路；
- 需要**开箱即用的语义级 VAD、工具调用、联网搜索、声音复刻**等高级能力，并接受其模型功能绑定（如仅 `qwen3.5-omni-realtime` 支持全部特性）；
- 开发团队以服务端为主（Python/Java），或希望最小化前端音视频工程复杂度；
- 对弱网适应性要求不高（依赖 WebSocket，无原生抗丢包机制）。

### ✅ 选择 Realtime API User Guide（按协议选型）当：
- 需要**跨终端一致体验**：浏览器（WebRTC）、App（AOQ）、服务端（WebSocket）共用同一模型能力；
- 对**弱网鲁棒性、低延迟、混合媒体传输（音+视+数据）有硬性要求** → 优先选 AOQ；
- 需要**深度控制媒体流**：如接入自研 ASR 引擎、注入 TTS 音频、处理 H.264 编码帧、实现回声消除旁路等；
- 使用非 Omni 系列模型（如纯 ASR/CosyVoice/`qwen-audio-3.0-realtime-plus`）→ **必须使用 WebSocket 协议**；
- 构建标准化 AI 通信中间件或 SDK 层，需解耦协议与模型。

> ⚠️ 注意：Omni Realtime API 本质是 Realtime API 的一种**特定协议（WebSocket）+ 特定模型（Omni 系列）+ 特定 SDK 封装**的组合。若项目需 WebRTC 浏览器支持或 AOQ 移动端弱网能力，**不能直接使用 Omni Realtime API SDK**，而应遵循 Realtime API User Guide 中对应协议的接入规范。

---

## 技术选型参考（面向开发者）

| 你的需求 | 推荐方案 | 关键依据 |
|----------|-----------|-----------|
| “我要 3 天内上线一个带语音问答和搜索的客服机器人” | ✅ Omni Realtime API（`qwen3.5-omni-realtime`） | SDK 开箱即用，`enable_search` + `tools` 一键启用，无需处理 SDP/AOQ [Token](../concepts/token.md) |
| “我要在微信小程序里做实时语音翻译，需适配低端安卓机弱网” | ✅ Realtime API + AOQ 协议 | AOQ 原生支持 QUIC 重传、前向纠错、带宽自适应；Omni API 不支持 AOQ |
| “我已有自研音视频 SDK，只需把百炼 LLM 接入现有通话流程” | ✅ Realtime API + WebRTC 或 AOQ | 可复用现有媒体采集链路，通过 `isExternal=true` 注入音频，避免重复开发 |
| “我要同时支持网页端（Chrome）、iOS App、车载中控屏” | ✅ Realtime API（三协议分别接入） | Omni API 仅提供 WebSocket，无法覆盖 WebRTC/AOQ 场景；需统一模型 + 分协议实现 |
| “我只需要实时语音转文字（ASR），不要 LLM” | ✅ Realtime API + WebSocket（Fun-ASR 模型） | Omni Realtime API **不提供独立 ASR 接口**，其 ASR 固定为 `qwen3-asr-flash-realtime` 且不可替换 |
| “我要做声音复刻驱动的虚拟人，且需毫秒级唇形同步” | ✅ Realtime API + AOQ + `qwen3.5-omni-plus-realtime` | AOQ 支持音视频帧级时间戳对齐；Omni SDK 未暴露帧同步控制接口 |

> 💡 最佳实践提示：  
> - 若初期验证用 WebSocket 快速跑通，后期需扩展至移动端，请**从 Realtime API User Guide 出发设计协议无关的会话抽象层**，避免 Omni SDK 绑定导致重构成本；  
> - 所有方案均需确保 `workspaceId` 与模型所在地域匹配（北京/新加坡），且 API Key 具备对应模型调用权限；  
> - `semantic_vad` 虽为高级能力，但在嘈杂环境或多人对话中可能误触发，生产环境建议结合 `idle_timeout_ms` + `silence_duration_ms` 进行参数调优。

## 被对比主题页

- [omni realtime api](../api/omni-realtime-api.md)
- [realtime api user guide](../api/realtime-api-user-guide.md)



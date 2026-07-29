# 实时 API 方案对比：Realtime API vs Omni Realtime API

## 对比目的与背景

为帮助开发者在百炼平台上高效选型，本文系统对比两种主流实时交互方案：**Realtime API**（多协议统一架构）与 **Omni Realtime API**（WebSocket 专用增强接口）。二者均面向低延迟、多模态 AI 交互场景，但设计目标、能力边界与集成路径存在显著差异。

- **Realtime API** 是平台级实时能力底座，通过 AOQ / WebRTC / WebSocket 三协议分层支持，强调**跨端兼容性、弱网鲁棒性与协议灵活性**，适用于对传输质量、端侧生态或服务端可控性有差异化要求的中大型业务。
- **Omni Realtime API** 是基于 WebSocket 的垂直优化接口，聚焦**对话体验深度控制**（如 VAD 精细调参、工具链闭环、搜索/[函数调用](../concepts/function-calling.md)），面向需要高自由度会话编排、快速原型验证或轻量级 Web/服务端集成的开发者。

本对比不替代具体模型文档，而是从工程落地视角提供技术选型决策依据。

---

## 关键维度对比表

| 维度 | Realtime API | Omni Realtime API |
|------|--------------|-------------------|
| **核心定位** | 多协议统一实时交互底座（协议即能力） | WebSocket 原生增强型多模态对话接口（功能即能力） |
| **支持协议** | ✅ AOQ（移动端原生）、✅ WebRTC（浏览器/WebApp）、✅ WebSocket（服务端/通用） | ❌ 仅 WebSocket（无 AOQ/WebRTC 支持） |
| **输入格式** | - 音频：16 kHz PCM（`input_audio_format="pcm"`）<br>- 视频：H.264/H.265 编码流（AOQ/WebRTC）<br>- 文本：`session.update` 中 `input_text` 字段（部分模型） | - 音频：16 kHz PCM（Base64 编码，`input_audio_buffer.append`）<br>- 图像：JPG/JPEG（≤1080p，Base64 ≤256KB，`input_image_buffer.append`）<br>- 文本：不支持直接文本输入（需转音频或图像） |
| **输出格式** | - 文本：`response.text.delta` / `response.text.done`<br>- 音频：24 kHz PCM（`modalities=["text","audio"]`）<br>- 视频：H.264/H.265 解码帧（AOQ/WebRTC） | - 文本：`conversation.item.text.delta` / `conversation.item.text.done`<br>- 音频：24 kHz PCM（`modalities=["text","audio"]`）<br>- **不支持视频输出** |
| **支持模型** | - 全模态：`qwen3.5-omni-plus-realtime`、`qwen3.5-omni-flash-realtime`、`qwen3.5-livetranslate-flash-realtime`<br>- 单模态：`Fun-ASR`、`CosyVoice`、`qwen-audio-3.0-realtime-plus/flash`（**仅 WebSocket**）<br>- 多模态套件：`multimodal-dialog`（**仅 WebRTC/WebSocket**，AOQ 不支持） | - 全模态：`qwen3.5-omni-realtime`（最强能力）、`qwen3-omni-flash-realtime`、`qwen-omni-turbo-realtime`<br>- 内置 ASR：`qwen3-asr-flash-realtime`（增量转录）<br>- **不支持单模态独立模型（如 Fun-ASR/CosyVoice）** |
| **API 端点** | - AOQ：`https://dashscope.aliyuncs.com/api/v1/realtime/allocate`（鉴权） + 客户端直连 relay endpoint<br>- WebRTC：白名单专属 STUN/TURN + 信令 endpoint（需商务开通）<br>- WebSocket：`wss://dashscope.aliyuncs.com/api-ws/v1/realtime` | - 统一 WebSocket endpoint：<br>`wss://{WorkspaceId}.{Region}.maas.aliyuncs.com/api-ws/v1/realtime`（按工作空间地域路由） |
| **计费方式** | 按 **实际调用时长（秒）+ 输出 token 数 + 输入 token 数** 计费<br>不同协议、不同模型单价独立（AOQ/WebRTC 通常略高于 WebSocket） | 按 **实际调用时长（秒）+ 输出 token 数 + 输入 token 数** 计费<br>与 Realtime API 同源计费体系，但 `qwen3.5-omni-realtime` 等高级模型单价更高 |
| **VAD 能力** | - `semantic_vad`：支持（推荐用于 `qwen3.5-omni-*` 系列）<br>- `server_vad`：部分模型支持（需确认服务端兼容性）<br>- 客户端 VAD：需自行实现并触发 `input_audio_buffer.commit` | - `semantic_vad`：仅 `qwen3.5-omni-realtime` 支持<br>- `server_vad`：全系列支持，可配 `silence_duration_ms` / `idle_timeout_ms`<br>- Manual 模式：完全由客户端控制 `commit` 时机 |
| **高级功能** | - 工具调用：✅（`qwen3.5-omni-*` 系列）<br>- 联网搜索：❌（当前未开放）<br>- 自定义采样参数：✅（`temperature`/`top_p` 等，依模型而定） | - 工具调用：✅（`qwen3.5-omni-realtime`，需 `tools` 配置）<br>- 联网搜索：✅（`enable_search=true`，与 `tools` 互斥）<br>- 自定义采样参数：✅（`qwen3.5-omni-realtime`），❌（`turbo` 系列不可调） |
| **开发门槛** | - AOQ：需集成 SDK + Opus [插件](../concepts/plugin.md) + 服务端 [Token](../concepts/token.md) 分发，移动端适配成本高<br>- WebRTC：需处理 SDP 协商、ICE 连接、媒体轨道管理，浏览器兼容性需验证<br>- WebSocket：最低门槛，类 HTTP 接入 | - WebSocket 原生协议，事件驱动清晰（`session.created` → `session.update` → `input_audio_buffer.append` → `response.done`）<br>- 提供 Java/Python SDK 封装，开箱即用 |
| **弱网对抗能力** | - AOQ：QUIC 底层，内置丢包重传、拥塞控制、前向纠错（FEC）<br>- WebRTC：内置 NACK/PLI/FIR、带宽自适应（ABR）<br>- WebSocket：无原生弱网优化，依赖 TCP 重传 | - 依赖 WebSocket 底层（TCP），无协议级弱网优化<br>- 依赖客户端实现重连、缓冲、降质保连等策略 |
| **安全要求** | - AOQ：**严禁客户端硬编码 API Key**，必须使用服务端下发的临时 `aoqTokenForClient`<br>- WebRTC/WebSocket：API Key 可直连，但仍建议服务端代理鉴权 | - API Key 直连 WebSocket，**强烈建议通过服务端代理中转连接**（避免 Key 泄露） |

---

## 适用场景建议

### ✅ 选择 Realtime API 当：
- **需覆盖多端生态**：同时支持 iOS/Android/HarmonyOS 原生 App（AOQ）、Web 浏览器（WebRTC）、后端服务（WebSocket）；
- **弱网环境关键**：用户常处于移动网络波动、高丢包场景（如远程教育、户外巡检），需 QUIC 或 WebRTC 级别抗抖动能力；
- **音视频双向实时性严苛**：如远程协作白板、AR 实时标注、多方会议语音增强，需端到端 <200ms 延迟；
- **已有音视频技术栈**：团队熟悉 WebRTC 开发或已集成 AOQ SDK，希望复用现有采集/渲染/编解码逻辑；
- **需混合模态能力**：既要语音对话，又要实时视频分析（如手势识别、表情反馈）。

### ✅ 选择 Omni Realtime API 当：
- **聚焦对话体验深度优化**：需精细控制 VAD 参数、动态启用联网搜索、灵活编排工具调用链路；
- **快速验证与 MVP 开发**：Web 前端或 Python 服务端快速接入，无需协议适配、SDK 集成、[插件](../concepts/plugin.md)安装；
- **纯语音+图文交互场景**：如智能客服机器人、语音助手、无障碍交互应用，无需视频流；
- **需要结构化事件流**：偏好明确的 `session` / `input_buffer` / `conversation.item` 事件语义，便于状态机管理；
- **预算敏感且模型能力匹配**：选用 `qwen-omni-turbo-realtime` 等低成本模型，牺牲参数自由度换取性价比。

> ⚠️ 注意：若业务需同时使用 `Fun-ASR`（独立语音识别）和 `qwen3.5-omni-realtime`（全模态对话），**必须选用 Realtime API 的 WebSocket 协议**——Omni Realtime API 不提供单模态模型入口。

---

## 技术选型参考（面向开发者）

| 你的需求 | 推荐方案 | 关键理由 |
|----------|-----------|-----------|
| “我要在安卓 App 里嵌入低延迟语音客服，用户常在地铁里使用” | **Realtime API + AOQ** | AOQ 的 QUIC 传输在弱网下建连更快、丢包恢复更强，Opus [插件](../concepts/plugin.md)保障音频质量 |
| “我正在做 Web 端在线陪练应用，需实时语音+文字+简单图像理解” | **Omni Realtime API** | WebSocket 接入快，`input_image_buffer.append` + `semantic_vad` + `tools` 可一站式满足需求，无需处理 WebRTC 兼容性 |
| “我们已有 WebRTC 视频会议系统，想叠加 AI 实时字幕+翻译” | **Realtime API + WebRTC** | 复用现有 WebRTC 媒体轨道，直接注入音频流；`qwen3.5-livetranslate-flash-realtime` 专为实时翻译优化 |
| “后端服务需批量发起语音合成任务，不涉及实时交互” | **Realtime API + WebSocket**（或考虑非实时 TTS API） | WebSocket 成本低、易运维；但注意：若只需合成，非实时 `qwen-audio-3.0` 更经济 |
| “需要模型自主调用天气 API 并返回口语化结果，且支持用户打断重说” | **Omni Realtime API + `qwen3.5-omni-realtime`** | 唯一支持 `tools` + `enable_search` + `smooth_output` + `semantic_vad` 组合的接口 |
| “团队无音视频开发经验，只想用几行代码跑通语音对话 demo” | **Omni Realtime API** | Python SDK 3 行代码即可连接、发送音频、接收文本+音频，文档示例完备 |

> 💡 **终极建议**：  
> - **先跑通 Omni Realtime API**：用其快速验证模型效果、对话逻辑与业务流程；  
> - **再评估是否需协议升级**：若遇到弱网卡顿、端侧兼容问题、或需视频能力，则切换至 Realtime API 并按端选协议；  
> - **始终遵循最小权限原则**：API Key 不出现于前端代码，AOQ [Token](../concepts/token.md) 必须服务端签发，WebSocket 连接建议经反向代理鉴权。  

---  
*最后更新：2024年10月*

## 被对比主题页

- [realtime api user guide](../api/realtime-api-user-guide.md)
- [omni realtime api](../api/omni-realtime-api.md)



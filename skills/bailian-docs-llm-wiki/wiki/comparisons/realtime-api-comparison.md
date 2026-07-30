# 实时 API 方案对比：Realtime API vs Omni Realtime API

本对比旨在帮助开发者清晰理解百炼平台两类核心[实时交互](../concepts/realtime-interaction.md)能力的技术定位、能力边界与适用条件，避免因协议/模型/功能错配导致集成失败或体验降级。随着多模态[实时交互](../concepts/realtime-interaction.md)场景（如智能座舱、AI客服、虚拟人直播）复杂度提升，选择匹配业务需求的底层 API 方案已成为架构设计的关键决策点。本文基于最新文档（截至 2024 年 Q3）对 `Realtime API`（多协议统一抽象层）与 `Omni Realtime API`（专精 WebSocket 的端到端多模态流式接口）进行系统性对比分析。

## 关键维度对比

| 维度 | Realtime API | Omni Realtime API |
|------|--------------|-------------------|
| **协议支持** | ✅ AOQ（移动端原生）、✅ WebRTC（浏览器/已有 WebRTC 基础设施）、✅ WebSocket（服务端/轻量接入）<br>→ 协议能力不均等，需按模型+协议交叉验证 | ❌ 仅支持 WebSocket（WSS）<br>→ 协议单一但深度优化，全链路事件驱动、低延迟音频流控成熟 |
| **输入格式** | • 文本：标准 JSON 字段<br>• 音频：PCM（16 kHz，单声道）<br>• 图像：❌ 不支持<br>• 视频：❌ 不支持 | • 文本：`input_text` 或 `conversation.item.create`<br>• 音频：PCM（16 kHz，单声道），支持 `append_audio` 流式注入<br>• 图像：JPG/JPEG（≤1080p，Base64 编码 ≤256 KB）<br>• 视频：❌ 不支持（但支持图像帧作为视觉输入） |
| **输出格式** | • 文本：`response.text.delta`<br>• 音频：PCM（24 kHz），`response.audio.delta`<br>• 多模态同步：✅ 支持 `["text","audio"]` 同步[流式输出](../concepts/streaming-output.md)<br>• 结构化数据：❌ 不提供原生工具调用响应结构 | • 文本：`response.text.delta`<br>• 音频：PCM（24 kHz），`response.audio.delta`<br>• 多模态同步：✅ 支持 `["text","audio"]` 同步[流式输出](../concepts/streaming-output.md)<br>• 结构化数据：✅ 原生支持 `function_call` / `tool_use` 事件，含完整 `conversation.item.created` → `conversation.item.create` 回调闭环 |
| **支持模型** | • 全模态模型：<br> `qwen3.5-omni-plus-realtime`、`qwen3.5-omni-flash-realtime`（AOQ/WebRTC 全能力；WebSocket 限文本/基础音频）<br>• 单模态专用模型：<br> Fun-ASR（实时语音识别）、CosyVoice（实时语音合成）、`qwen-audio-3.0-realtime-plus`（仅 WebSocket）<br>• 多模态套件：<br> `multimodal-dialog`（仅 WebRTC/WebSocket） | • 严格限定 Omni 系列模型：<br> `qwen3.5-omni-realtime`（语义 VAD + 工具调用 + 联网搜索）<br> `qwen3.5-omni-plus-realtime` / `qwen3.5-omni-flash-realtime`（静默超时引导 + 平滑输出）<br> `qwen3-omni-flash-realtime`（Server VAD + 默认 Cherry 音色）<br> `qwen-omni-turbo-realtime`（极致低延迟，生成参数锁定）<br>• ❌ 不支持非 Omni 命名模型（如 ASR/TTS 独立模型、`qwen-audio-3.0` 等） |
| **API 端点** | • AOQ：`https://api.aliyun.com/v1/realtime/aoq/token`（获取临时 token） + 客户端 SDK 连接网关<br>• WebRTC：白名单专属 STUN/TURN + Signaling Endpoint（商务申请）<br>• WebSocket：`wss://dashscope.aliyuncs.com/api-ws/v1/realtime`（通用） | • 统一 WSS 端点：<br> `wss://{WorkspaceId}.{region}.maas.aliyuncs.com/api-ws/v1/realtime`<br>→ 强制使用业务空间专属域名，性能与稳定性优于旧域名 |
| **计费方式** | • 按 **实际调用时长（秒） + 模型单价** 计费<br>• 音频流传输、VAD 检测、会话维持均计入时长<br>• AOQ/WebRTC 因协议开销略高，WebSocket 成本相对可控 | • 按 **实际音频处理时长（秒） + 模型单价** 计费<br>• 仅对有效语音段（VAD 检出后）计费，静音/等待期不计费<br>• 图像输入按次计费（每次 ≤256 KB Base64）<br>• 工具调用、联网搜索不额外计费（含在模型调用内） |
| **典型场景** | • 移动端强弱网对抗场景（如车载语音助手、户外巡检终端）→ 选 AOQ<br>• 浏览器嵌入式 AI 应用（如在线教育互动白板）→ 选 WebRTC<br>• 快速验证/服务端代理/跨平台原型 → 选 WebSocket<br>• 需独立 ASR/TTS 能力（如会议转录+合成）→ 必选 WebSocket | • 全链路语音交互闭环（如智能客服坐席辅助、虚拟数字人实时对话）<br>• 多模态意图理解（语音+图像联合输入，如“帮我看看这张发票金额是否正确”）<br>• 需主动引导与状态管理（静默超时自动提问、语义 VAD 精准切分）<br>• 需工具调用与外部系统集成（如查订单、改地址、调取 CRM 数据） |

## 适用场景建议

### ✅ 推荐选用 Realtime API 当：
- **终端类型多样且需协议灵活性**：同时覆盖 iOS/Android/HarmonyOS 原生 App（AOQ）、Web 页面（WebRTC）、IoT 设备（WebSocket）；
- **已有音视频基础设施**：团队已具备 WebRTC 信令/媒体服务器，或需复用现有 AOQ SDK 生产环境；
- **功能需求聚焦单模态增强**：明确需要 Fun-ASR 高精度转写、CosyVoice 多音色合成，或 `multimodal-dialog` 套件快速搭建对话逻辑；
- **安全合规要求极高**：需服务端完全掌控鉴权（AOQ 的 `aoqTokenForClient` 机制杜绝客户端密钥暴露）；
- **弱网环境为首要挑战**：移动网络抖动频繁、丢包率高（AOQ 内置 AEC/降噪/抗丢包重传）。

### ✅ 推荐选用 Omni Realtime API 当：
- **交互范式为“语音主导+多模态补充”**：用户以语音为主输入，辅以图片/文字上下文，且需模型统一理解并生成语音响应；
- **业务逻辑依赖主动状态管理**：需静默超时自动追问（`idle_timeout_ms`）、语义级语音活动检测（`semantic_vad`）、平滑音频输出（`smooth_output`）；
- **必须集成外部系统能力**：需模型自主触发[函数调用](../concepts/function-calling.md)（如支付确认、库存查询），并要求服务端能可靠接收 `conversation.item.created` 事件；
- **追求端到端最低延迟与一致性体验**：放弃协议适配成本，换取 WebSocket 协议下全链路（建连→VAD→推理→TTS→流式返回）的深度优化；
- **音色定制与模型版本强绑定**：已使用 `qwen-voice-enrollment` 创建专属音色，且需确保与 Omni 模型版本（如 `qwen3.5-omni-plus-realtime`）严格一致。

## 技术选型参考（面向开发者）

| 选型考量 | Realtime API | Omni Realtime API |
|----------|--------------|-------------------|
| **上手速度** | ⚠️ 中高：需理解三种协议差异、SDK 生命周期、媒体流时序（如 AOQ 必须 `session.updated` 后才 `enableSendMediaStream`） | ✅ 高：统一 WebSocket 协议，事件模型清晰（`session.created` → `input_audio_buffer.append` → `response.audio.delta`），SDK 封装完善 |
| **扩展能力** | ✅ 强：支持外部音频流注入（TTS 文件播放）、外部视频帧输入（屏幕共享/AI画面）、音视频帧回调（用于分析/录制） | ⚠️ 中：支持图像输入与工具调用，但不开放底层音视频帧访问；音色复刻需严格匹配模型版本 |
| **调试难度** | ⚠️ 高：协议层问题（如 WebRTC ICE 失败）、SDK 版本兼容（AOQ v1.0.1+ + Opus 插件）、服务端 [Token](../concepts/token.md) 时效性均需排查 | ✅ 中：全链路事件日志可追溯，`server_events` 明确返回错误码（如 `invalid_session`、`vad_timeout`），控制台提供实时会话追踪 |
| **长期维护成本** | ⚠️ 中高：多协议意味着多测试矩阵（iOS/Android/Web）、多 SDK 版本升级路径、协议特性演进不同步风险 | ✅ 低：单一协议、统一事件模型、模型能力演进集中（Omni 系列迭代同步更新所有特性） |
| **推荐起点** | • 新项目若需覆盖 App/Web/IoT 三端 → 从 WebSocket 子集起步，再逐步接入 AOQ/WebRTC<br>• 已有 WebRTC 基础 → 直接复用，聚焦模型能力验证 | • 所有新语音交互类项目默认首选；<br>• 若需图像理解 → 必选 Omni；<br>• 若需工具调用 → 必选 Omni（Realtime API 不支持原生 function calling） |

> **重要提醒**：  
> - **不要混用模型与协议**：`qwen3.5-omni-realtime` 在 AOQ/WebRTC 下不支持 `semantic_vad` 和工具调用，在 WebSocket 下能力受限；而 Omni Realtime API 仅接受 Omni 系列模型，传入 `qwen-audio-3.0-realtime-plus` 将直接报错。  
> - **安全红线**：无论哪种方案，`API Key` 绝不可出现在客户端代码中。Realtime API 的 AOQ 使用服务端下发 token，Omni Realtime API 依赖服务端代建连或短期 JWT，务必通过后端代理完成鉴权。  
> - **版本对齐**：Omni 音色复刻模型 `target_model` 必须与调用模型完全一致（含 `.5` 版本号），否则合成失败；Realtime API 的 AOQ SDK 与 Opus 插件需严格匹配文档要求版本。  

选择本质是权衡——Realtime API 提供「广度」与「适配弹性」，Omni Realtime API 提供「深度」与「体验确定性」。建议初期用 Omni 快速验证核心交互闭环，再根据终端覆盖需求决定是否引入 Realtime API 的 AOQ/WebRTC 协议扩展。

## 被对比主题页

- [realtime api user guide](../api/realtime-api-user-guide.md)
- [omni realtime api](../api/omni-realtime-api.md)



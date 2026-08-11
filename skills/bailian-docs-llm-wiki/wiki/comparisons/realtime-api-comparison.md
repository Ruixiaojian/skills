# 实时 API 方案对比：Omni Realtime API vs Realtime API User Guide

本对比旨在帮助开发者清晰理解百炼平台两类核心实时 API 的定位差异、能力边界与技术选型依据。随着[多模态](../concepts/multi-modal.md)实时交互场景（如智能座舱、远程医疗、AI 教育助手）对低延迟、高可靠性、协议适应性提出更高要求，平台提供了 **Omni Realtime API**（聚焦全栈优化的统一 WebSocket 接口）与 **Realtime API User Guide**（面向异构终端的协议可选型架构）两套方案。二者并非简单替代关系，而是在模型能力、传输层抽象、接入复杂度与运维控制粒度上存在系统性权衡。本文从关键维度展开结构化对比，并给出明确的适用场景建议。

## 关键维度对比

| 维度 | Omni Realtime API | Realtime API User Guide |
|------|-------------------|--------------------------|
| **核心定位** | 面向“开箱即用”的高性能实时对话场景，提供标准化、事件驱动的 WebSocket 协议封装，强调端到端一致性与快速集成 | 面向“协议自适应”的企业级实时通信需求，提供 AOQ（QUIC）、WebRTC、WebSocket 三协议统一接口，强调网络鲁棒性、终端兼容性与媒体流精细控制 |
| **输入格式** | 支持 PCM 音频（16 kHz）和 JPG/JPEG 图像（≤1080p，Base64 编码 ≤256 KB）；图像需在音频缓冲提交后发送，且必须通过 `input_audio_buffer.commit` 统一触发 | 支持 PCM 音频（16 kHz）；**图像输入暂未开放**（文档中无任何图像相关事件或参数说明）；视频采集仅限 AOQ SDK 的自定义帧模式（原始/编码），非标准会话输入 |
| **输出格式** | 支持 `["text"]` 或 `["text", "audio"]`（默认）；音频为 24 kHz PCM 流；`qwen3-omni-flash-realtime` 系列支持 `smooth_output` 控制文本风格 | 支持 `["text"]` 或 `["text", "audio"]`；音频为 24 kHz PCM 流；**不支持纯音频输出 `["audio"]`（与 Omni 一致）**；无文本风格控制参数 |
| **支持模型** | 专属模型系列：<br>• `qwen3.5-omni-realtime`（含工具调用、语义 VAD、联网搜索）<br>• `qwen3.5-omni-plus-realtime` / `qwen3.5-omni-flash-realtime`（含 server_vad、idle_timeout）<br>• `qwen3-omni-flash-realtime` / `qwen-omni-turbo-realtime`（基础对话） | 多模型矩阵，按协议能力分层：<br>• 全协议支持：`qwen3.5-omni-plus-realtime`, `qwen3.5-omni-flash-realtime`, `qwen3.5-livetranslate-flash-realtime`, `multimodal-dialog`, `qwen-audio-3.0-realtime-plus/flash`<br>• AOQ/WebSocket 专属：ASR（`Qwen-Audio-3.0-ASR-Flash-Streaming`）、TTS（`CosyVoice`, `qwen-audio-3.0-tts-*`）<br>• WebRTC **不支持 ASR/TTS** |
| **API 端点与协议** | 固定 WebSocket 端点：<br>`wss://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api-ws/v1/realtime`<br>（推荐业务空间专属域名） | 三协议统一入口，由请求头或 URL 参数动态路由：<br>• AOQ：`POST /api/v1/aoq/realtime` + `x-dashscope-rtc-transport: moq`<br>• WebRTC：`POST /api/v1/webrtc/realtime?model=xxx`<br>• WebSocket：`wss://.../api-ws/v1/realtime`（同 Omni，但鉴权与参数解析逻辑独立） |
| **计费方式** | 按 **实际消耗的 token 数量（输入+输出） + 音频处理时长（秒）** 计费；语音识别（ASR）、语音合成（TTS）、大模型推理分别计费；音色复刻单独计费 | 按 **协议通道 + 模型调用 + 媒体流时长** 综合计费：<br>• AOQ/WebRTC：按连接时长（分钟）+ 媒体流带宽（GB）+ 模型 token<br>• WebSocket：同 Omni 计费模型（token + 音频时长）<br>• ASR/TTS 模型仅在 AOQ/WebSocket 下产生费用，WebRTC 场景下不可用故无对应费用 |
| **VAD 能力** | 提供双模式：<br>• `server_vad`（声学特征，全模型支持）<br>• `semantic_vad`（语义有效性，**仅 `qwen3.5-omni-realtime` 系列支持**）<br>Manual 模式需显式 `commit()` + `create_response()` | 统一支持 `semantic_vad` 类型（推荐），但**未声明模型级限制**；`server_vad` 未在文档中提及；所有模型均依赖 `turn_detection` 配置，无 Manual/VAD 模式切换概念 |
| **高级能力** | • 工具调用（`tools`）：仅 `qwen3.5-omni-realtime` 支持，需客户端回传执行结果<br>• 联网搜索（`enable_search`）：仅 `qwen3.5-omni-realtime` 支持，与 `tools` 互斥<br>• 声音复刻：需预创建音色，且 `target_model` 必须与会话模型完全一致 | • **无工具调用与联网搜索能力**（文档未定义相关事件、参数或流程）<br>• 声音复刻：未在 Realtime API 文档中提及，视为不支持<br>• **媒体流级控制丰富**：AOQ SDK 支持 `enableSendMediaStream()`、`isExternal` 自定义采集/播放、帧级推流等 |
| **典型场景** | • 需要快速上线的语音助手 App（iOS/Android WebView）<br>• 对话逻辑强耦合工具调用的客服机器人（如查订单、改地址）<br>• 要求严格音色一致性与低首包延迟的虚拟人播报 | • 弱网环境下的车载语音交互（AOQ 抗丢包）<br>• 浏览器端实时会议翻译（WebRTC 兼容性优先）<br>• 需深度定制音频前处理（降噪、回声消除）或视频编码（H.264/H.265）的工业设备远程指导 |

## 适用场景建议

### 选择 Omni Realtime API 当：
- 你的应用是 **移动端 App 或混合 WebView 应用**，追求最简接入路径与最快迭代速度；
- 业务逻辑 **强依赖结构化工具调用**（如电商客服需调用订单查询、物流跟踪 API）或 **需要联网实时检索补充知识**；
- 对 **音色复刻有刚性需求**，且能确保音色模型与会话模型版本严格匹配；
- 团队缺乏 WebRTC/AOQ 协议栈开发经验，希望规避 SDP 协商、ICE 连接、QUIC 流控等底层复杂性；
- 场景以 **单轮语音输入 → [多模态](../concepts/multi-modal.md)输出（文本+语音）** 为主，无需复杂媒体流编排。

### 选择 Realtime API User Guide 当：
- 你需要 **跨终端统一架构**：同一套后端服务同时支撑 iOS App（AOQ）、Web 浏览器（WebRTC）、老旧设备（WebSocket）；
- 面临 **弱网、高丢包、NAT 穿透困难** 等网络挑战，需 AOQ 的 QUIC 多路复用与前向纠错能力；
- 业务涉及 **专业音视频处理**：如自定义麦克风阵列采集、硬件编码器直出、Web Audio API 混音、低延迟播放缓冲控制；
- 需要 **分离 ASR 与 TTS 能力**：例如仅用 `Qwen-Audio-3.0-ASR-Flash-Streaming` 做实时转写，再将文本送入其他大模型处理；
- 团队具备 **实时音视频协议开发能力**，或已使用 WebRTC/AOQ SDK（如 libwebrtc、moq-sdk）构建过类似系统。

## 技术选型参考（面向开发者）

- **起步验证阶段**：优先选用 Omni Realtime API。其 WebSocket 协议成熟、SDK 封装完善、错误反馈明确（如 `["audio"]` 非法值直接报错），可 1 小时内完成 Hello World 对话，快速验证模型效果与业务流程。
  
- **生产级高可用部署**：若用户终端网络环境不可控（如车载、IoT 设备），务必评估 Realtime API 的 AOQ 协议。其连接建立成功率、弱网下音频连续性、断线自动重连机制均经过大规模场景锤炼，远超通用 WebSocket。

- **模型能力是硬约束**：若业务必需工具调用或联网搜索，请 **只能选择 Omni Realtime API** 并锁定 `qwen3.5-omni-realtime` 模型；Realtime API 当前不提供该能力，切勿在选型时忽略此前提。

- **计费敏感型项目**：对比相同会话的 token 消耗与音频时长，Omni 方案更透明；但若需长时连接（>10 分钟）且带宽受限，AOQ 的带宽计费模式可能更具成本优势，需结合实测数据决策。

- **未来演进考量**：Omni Realtime API 定位为“下一代统一实时接口”，新模型（如[多模态](../concepts/multi-modal.md) Agent）将优先在此发布；Realtime API User Guide 则持续强化协议生态（如即将支持 AV1 视频编码、SRT 协议），适合长期投入音视频基础设施建设的团队。

> **重要提醒**：两类 API **共享同一套模型服务后端与鉴权体系**，但会话上下文、事件格式、错误码定义、SDK 接口契约完全独立。切勿混用 Omni 的 `response.function_call_arguments.done` 事件与 Realtime API 的 `onDataMsg` 解析逻辑——这将导致不可预测的解析失败。

## 被对比主题页

- [omni realtime api](../api/omni-realtime-api.md)
- [realtime api user guide](../api/realtime-api-user-guide.md)



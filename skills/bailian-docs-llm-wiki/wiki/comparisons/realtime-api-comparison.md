# 实时API方案对比：Omni Realtime vs Realtime API

本文旨在帮助开发者清晰区分百炼平台两大实时交互能力——**Omni Realtime API** 与 **Realtime API**，明确其技术定位、能力边界与适用场景。二者虽均面向低延迟[多模态](../concepts/multi-modal.md)实时交互，但在协议架构、模型支持、接入复杂度、功能粒度及运维模型上存在本质差异。本对比不替代具体业务验证，而是提供结构化选型依据，助力团队在智能客服、虚拟助手、实时翻译、音视频AI等场景中做出高效、可持续的技术决策。

## 关键维度对比

| 维度 | Omni Realtime API | Realtime API |
|------|-------------------|--------------|
| **核心协议** | 仅支持 WebSocket（强制事件驱动） | 支持三种协议：<br>• AOQ（推荐移动端，含弱网优化/回声消除）<br>• WebRTC（推荐浏览器端，需白名单）<br>• WebSocket（推荐服务端集成/快速验证） |
| **输入格式** | • PCM 音频（16 kHz，Base64 编码）<br>• JPG/JPEG 图像（≤1080p，Base64 编码，≤256KB）<br>• 文本（通过 `session.update` 或 `input_text` 事件） | • 协议相关：<br> - AOQ/WebRTC：原生音频流（Opus/PCM）、视频帧（H.264/H.265）、文本<br> - WebSocket：PCM 音频（16 kHz）、文本；图像暂不原生支持（需预处理为文本描述或绕行其他接口） |
| **输出格式** | • 可配置 `["text"]` 或 `["text", "audio"]`<br>• 音频为 24 kHz PCM [流式输出](../concepts/streaming-output.md)（`response.audio.delta`）<br>• 文本为 token 级增量（`response.text.delta`） | • 协议相关：<br> - AOQ/WebRTC：支持音视频+文本混合输出（如语音合成+字幕+画面标注）<br> - WebSocket：仅支持文本 + 音频（PCM），无视频输出能力 |
| **支持模型** | 专属 Qwen-Omni 实时系列：<br>• `qwen3.5-omni-realtime`（全能力：语义VAD、搜索、工具调用）<br>• `qwen3-omni-flash-realtime`（轻量语音优化，支持风格控制）<br>• `qwen-omni-turbo-realtime`（极简固定参数，高吞吐低延迟） | 更广谱模型生态：<br>• 全模态模型：`qwen3.5-omni-plus-realtime`、`qwen3.5-livetranslate-flash-realtime`<br>• 专用模型：Fun-ASR（语音识别）、CosyVoice（语音合成）、`qwen-audio-3.0-realtime-plus`（语音对话）<br>• [多模态](../concepts/multi-modal.md)套件：`multimodal-dialog`（WebRTC/WebSocket） |
| **API 端点** | 固定 WebSocket 地址：<br>`wss://{WorkspaceId}.{Region}.maas.aliyuncs.com/api-ws/v1/realtime` | 协议差异化：<br>• AOQ：`wss://aoq.{Region}.maas.aliyuncs.com`（需 Allocate 获取 `sid`/`aoqTokenForClient`）<br>• WebRTC：STUN/TURN + 信令服务器地址（白名单分配）<br>• WebSocket：同 Omni Realtime（但路径与鉴权逻辑不同） |
| **计费方式** | 按 **实际消耗的音频时长（秒） + 文本 token 数** 计费<br>• 音频输入/输出均计费<br>• 图像输入按次计费（每张）<br>• 不区分协议，统一计量 | 按 **协议 + 模型 + 资源维度** 分层计费：<br>• AOQ/WebRTC：按连接时长（分钟） + 媒体流带宽（GB） + 模型调用（如 ASR 秒数、TTS 字符数）<br>• WebSocket：按音频时长 + token 数（类 Omni）<br>• [多模态](../concepts/multi-modal.md)套件按会话时长 + 功能模块订阅 |
| **典型场景** | • 高保真语音助手（需端到端 VAD+TTS+语义理解）<br>• 低延迟智能客服（单通道语音+文本交互）<br>• 多模态问答（语音提问+图片上传+语音回答） | • 全链路音视频AI应用（如远程医疗问诊、在线教育互动）<br>• 弱网环境下的移动语音应用（AOQ 抗丢包/低建连延迟）<br>• 浏览器内实时翻译/会议纪要（WebRTC 原生支持）<br>• 服务端批量语音处理（WebSocket 快速集成） |

## 适用场景建议

### ✅ 推荐选用 **Omni Realtime API** 当：
- 项目以 **语音为核心交互模态**，且对端到端延迟（<300ms）、语音自然度、语义级静音检测（`semantic_vad`）有严苛要求；
- 需要 **统一 WebSocket 接入栈**，避免多协议适配成本（如纯服务端调度、IoT 设备直连）；
- 业务聚焦于 **Qwen-Omni 系列模型能力**（如联网搜索、工具调用），且无需视频流、WebRTC 特性或 AOQ 弱网增强；
- 团队具备 WebSocket 事件驱动开发经验，能处理 `input_audio_buffer.append` / `response.audio.delta` 等细粒度流控。

### ✅ 推荐选用 **Realtime API** 当：
- 应用需 **跨终端一致体验**：移动端用 AOQ（抗弱网）、浏览器用 WebRTC（免插件）、后台用 WebSocket（易维护）；
- 场景涉及 **音视频混合处理**（如实时会议中语音转文字+人脸情绪分析+PPT标注）；
- 需要 **灵活组合专用能力**：例如将 Fun-ASR 的高精度语音识别与 CosyVoice 的情感化TTS 解耦调用；
- 项目处于 **快速验证或MVP阶段**，希望复用现有 WebRTC 基础设施，或已有 AOQ SDK 集成经验；
- 运维侧要求 **连接状态强管控**（AOQ 提供 `Connecting → Connected → Disconnected` 明确状态机）或需定制采集/播放链路（如接入第三方TTS引擎）。

## 技术选型参考指南

| 决策因素 | Omni Realtime API | Realtime API |
|----------|-------------------|--------------|
| **接入复杂度** | ⭐⭐⭐⭐☆（WebSocket 事件模型需学习，但协议单一） | ⭐⭐☆☆☆（AOQ/WebRTC 需处理信令、媒体协商、证书指纹；WebSocket 最简） |
| **模型灵活性** | ⭐⭐⭐☆☆（仅限 Omni 系列，参数可调范围因模型而异） | ⭐⭐⭐⭐☆（覆盖 ASR/TTS/对话/翻译/多模态套件，协议与模型解耦） |
| **延迟敏感度** | ⭐⭐⭐⭐⭐（专为 <300ms 优化，语义VAD显著降低误触发） | ⭐⭐⭐⭐☆（AOQ 协议在弱网下更优；WebSocket 与 Omni 延迟接近） |
| **扩展性需求** | ⭐⭐⭐☆☆（支持图像输入+工具调用，但无视频输出） | ⭐⭐⭐⭐⭐（支持音视频双向流、自定义外部流、SDP 级控制） |
| **运维成熟度** | ⭐⭐⭐⭐☆（统一 WebSocket 监控、日志、重连策略） | ⭐⭐⭐☆☆（AOQ/WebRTC 需额外关注网络质量、Relay 节点调度、[Token](../concepts/token.md) 刷新） |
| **成本可控性** | ⭐⭐⭐⭐☆（计量维度清晰，无隐性带宽/连接费） | ⭐⭐⭐☆☆（AOQ/WebRTC 存在连接时长+带宽双重成本，需精细评估） |

> 💡 **选型口诀**：  
> **“单模强交互，选 Omni；多端多能力，选 Realtime”**  
> 若您的核心诉求是「用一个 WebSocket 连接，跑通语音+图片+搜索的端到端助手」，Omni Realtime 是最精简路径；  
> 若您需要「在安卓App里抗弱网语音，在Chrome里做实时字幕，在后台调度ASR任务」，Realtime API 的协议矩阵与模型生态将提供不可替代的弹性。  

请结合自身技术栈、终端分布、SLA 要求及长期演进规划综合判断。建议在 POC 阶段并行验证两种方案的端到端延迟、错误率与开发效率，再锁定最终架构。

## 被对比主题页

- [omni realtime api](../api/omni-realtime-api.md)
- [realtime api user guide](../api/realtime-api-user-guide.md)



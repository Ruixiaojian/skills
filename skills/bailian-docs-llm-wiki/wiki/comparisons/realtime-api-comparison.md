# 实时API方案对比：Omni Realtime vs Realtime API

为帮助开发者在百炼平台快速识别并选用最适合业务需求的实时交互方案，本文对两大核心实时能力接口——**Omni Realtime API** 与 **Realtime API** 进行系统性对比分析。二者虽同属“实时”范畴，但在设计定位、协议栈架构、模型支持粒度及适用场景上存在本质差异：  
- **Omni Realtime API** 是面向**端到端多模态智能体（Agent）交互**的**一体化协议**，以 WebSocket 为唯一传输通道，深度集成 VAD、ASR、TTS、工具调用与搜索等全链路能力，强调“开箱即用”的语义级实时性；  
- **Realtime API** 是面向**基础设施层**的**协议栈抽象**，提供 WebSocket / WebRTC / AOQ 三类传输协议选择，按模型/应用类型划分支持范围，强调**跨终端、弱网鲁棒性与协议灵活性**，需开发者根据终端环境主动选型。

以下从关键维度展开对比，并附技术选型建议。

## 关键维度对比

| 维度 | Omni Realtime API | Realtime API |
|------|-------------------|--------------|
| **定位与设计目标** | 面向强交互智能体（如虚拟助手、智能客服）的一体化实时交互协议，聚焦语义级低延迟与多模态协同 | 面向多终端（Web/移动端/嵌入式）的实时 AI 协议栈，强调协议可选性、弱网适应性与模型/应用解耦 |
| **传输协议** | **仅支持 WebSocket**（推荐使用业务空间专属域名 `wss://{WorkspaceId}.{region}.maas.aliyuncs.com`） | **支持三种协议**：<br>• WebSocket：服务端集成/原型验证<br>• WebRTC：浏览器音视频原生交互（含 AEC/NS）<br>• AOQ（AI over QUIC）：移动端原生 App 极致弱网场景 |
| **输入格式** | • 音频：`PCM_16000HZ_MONO_16BIT`（Base64 编码）<br>• 视频帧：JPG/JPEG（≤256KB/帧，480P–720P）<br>• 支持麦克风+摄像头实时流或本地文件 | • 协议决定输入方式：<br> – WebSocket：同 Omni（PCM Base64）<br> – WebRTC：原生 MediaStream，自动处理编码/同步<br> – AOQ：自定义媒体流封装，支持混合数据通道（音频+元数据） |
| **输出格式** | • 文本：流式 `response.text.delta`<br>• 音频：固定 `PCM_24000HZ_MONO_16BIT`（Base64）<br>• 不支持自定义采样率或编码格式 | • 文本：各协议均支持流式文本 delta<br>• 音频：统一为 `pcm` 格式，但采样率/位深由模型能力决定（如 `CosyVoice` 系列支持 24kHz/16bit）<br>• WebRTC/AOQ 可直接输出 AudioTrack，避免 Base64 解码开销 |
| **支持模型** | 限定于 `qwen*-omni-*realtime` 系列：<br>• `qwen3.5-omni-realtime`（全能力：semantic_vad + tools + search）<br>• `qwen3.5-omni-plus-realtime` / `qwen3.5-omni-flash-realtime`<br>• `qwen3-omni-flash-realtime` / `qwen-omni-turbo-realtime`（能力精简） | **按协议分层支持**：<br>• 全模态模型（如 `qwen3.5-omni-plus-realtime`）：WebSocket/WebRTC/AOQ 均支持<br>• 多模态开发套件（`multimodal-dialog`）：WebSocket/WebRTC 支持，**AOQ 不支持**<br>• 专用模型（`Fun-ASR`, `CosyVoice`, `qwen-audio-3.0-realtime-plus`）：**仅 WebSocket 支持** |
| **高级能力支持** | • ✅ 语义级 VAD（`semantic_vad`）<br>• ✅ 工具调用（Function Calling）<br>• ✅ 联网搜索（`enable_search`）<br>• ✅ 声音复刻（需预创建音色且 model 严格匹配）<br>• ❌ 不支持 WebRTC/AOQ 特有特性（如 AEC、QUIC 重传） | • ✅ 各协议均支持基础 VAD（`server_vad`），`semantic_vad` 依赖模型与协议组合（如 WebRTC + `qwen3.5-omni-realtime`）<br>• ✅ 工具调用：仅 WebSocket 和 WebRTC 支持（AOQ 当前不支持）<br>• ✅ 搜索：同 Omni，仅 `qwen3.5-omni-realtime` 系列支持<br>• ✅ 声音复刻：需通过独立 API 创建，接入时指定 `voice` 即可，**无 model 严格绑定限制**（更灵活） |
| **API 端点** | 固定 WebSocket 地址：<br>`wss://{WorkspaceId}.{region}.maas.aliyuncs.com/api-ws/v1/realtime`<br>（强烈推荐业务空间专属域名，禁用旧域名 `dashscope.aliyuncs.com`） | 多端点，按协议区分：<br>• WebSocket：同 Omni 格式<br>• WebRTC：信令端点（如 `https://.../webrtc/v1/sdp`），需携带 `?model=xxx`<br>• AOQ：由 AppServer 动态分配 `relayEndpoints` + `aoqTokenForClient` |
| **计费方式** | 按 **实际调用时长（秒） + 输出 token 数量** 计费：<br>• 输入音频时长计入调用时长<br>• 文本输出按 token 计费，音频输出按等效 token 折算<br>• 不区分协议或终端类型 | 按 **协议 + 模型 + 使用量** 三维计费：<br>• WebSocket：按 token + 时长<br>• WebRTC/AOQ：额外收取**连接维持费**与**弱网增强服务费**（如丢包补偿、QUIC 重传）<br>• 专用模型（ASR/TTS）单独计价，不与对话模型捆绑 |
| **典型场景** | • 需要语音打断、语义级静音检测的智能客服坐席辅助<br>• 多轮语音+视觉交互的车载助手（如看图问答）<br>• 对话中需实时调用天气/订单等工具的虚拟数字人 | • 浏览器端在线教育实时双师课堂（WebRTC 音视频+文本）<br>• 移动端离线弱网环境下的语音翻译 App（AOQ 抗抖动）<br>• 后台服务批量语音转写（WebSocket + Fun-ASR） |

## 适用场景建议

### 选择 Omni Realtime API 当：
- 你的产品是**标准化多模态智能体应用**（如客服机器人、AI 助手 App），且终端以 **iOS/Android 原生 App 或 Electron 桌面端为主**；
- 要求 **开箱即用的全链路能力**（无需自行集成 ASR/TTS/VAD），尤其需要 `semantic_vad` 实现自然打断、或 `tools` + `enable_search` 构建自主决策 Agent；
- 开发团队希望**最小化协议适配成本**，接受 WebSocket 作为唯一传输方式；
- 对音频格式兼容性要求不高（输入强制 16kHz PCM，输出固定 24kHz PCM）。

### 选择 Realtime API 当：
- 你需要**覆盖多类终端与网络环境**：例如同一产品需同时支持 Chrome 浏览器（WebRTC）、华为鸿蒙手机（AOQ）和 Python 后台服务（WebSocket）；
- 业务涉及**非 Omni 类模型**：如纯语音识别（`Fun-ASR`）、高保真语音合成（`CosyVoice`）或轻量级实时翻译（`qwen3.5-livetranslate-flash-realtime`）；
- 对**弱网稳定性、建连速度或音视频质量**有严苛要求（如跨国会议、偏远地区教育），需利用 WebRTC 的 AEC/NS 或 AOQ 的 QUIC 快速重传；
- 团队具备一定底层协议理解能力，愿意为协议选型与媒体流控制（如 WebRTC 的 `gateMedia`、AOQ 的 `enableSendMediaStream`）投入开发资源。

## 技术选型参考（面向开发者）

| 你的需求 | 推荐方案 | 关键理由 |
|----------|-----------|-----------|
| “我要快速上线一个带语音打断的微信小程序客服插件” | ❌ Omni Realtime（小程序不支持 WebSocket 长连接）<br>✅ Realtime API + **WebRTC** | 小程序 WebView 支持 WebRTC，可直连媒体流，避免 WebSocket 中转延迟；Omni 无小程序 SDK 支持 |
| “我正在开发 iOS 原生虚拟偶像 App，需支持声音复刻+实时工具调用” | ✅ Omni Realtime（首选）<br>⚠️ Realtime API + WebSocket（次选） | Omni 对 `qwen3.5-omni-realtime` + 声音复刻 + tools 的组合支持最完整；Realtime WebSocket 也可实现，但需自行管理 session 生命周期 |
| “我需要将一段录音批量转成文字，并做敏感词过滤” | ❌ Omni Realtime（不支持纯 ASR 场景）<br>✅ Realtime API + **WebSocket + Fun-ASR** | Omni 仅面向交互式会话，无离线批量 ASR 接口；Realtime API 明确支持 `Fun-ASR` 系列，且 WebSocket 最适合服务端批处理 |
| “我的 App 主要在地铁/山区运行，语音通话常卡顿” | ❌ Omni Realtime（无弱网增强机制）<br>✅ Realtime API + **AOQ** | AOQ 内置 QUIC 传输、前向纠错（FEC）与智能重传，专为弱网优化；Omni 依赖标准 WebSocket，在高丢包下易断连 |
| “我想用摄像头拍一张商品图，让 AI 直接告诉我价格和竞品” | ✅ Omni Realtime（推荐）<br>✅ Realtime API + WebRTC（可行） | Omni 原生支持 `append_video` + `qwen3.5-omni-realtime` 的视觉理解，流程简洁；WebRTC 亦可传视频帧，但需自行解析 SDP 并绑定 DataChannel，开发复杂度更高 |

> **重要提醒**：  
> - **不要混用协议与模型**：例如 `multimodal-dialog` 应用不可通过 AOQ 接入；`Fun-ASR` 模型不可通过 WebRTC 调用。务必查阅 [Realtime API 简介](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-overview.md) 中的协议支持矩阵。  
> - **迁移优先级**：Omni Realtime 用户请立即迁移到业务空间专属域名（`wss://{WorkspaceId}.{region}.maas.aliyuncs.com`），旧域名已逐步限流。  
> - **参数兼容性陷阱**：`qwen-omni-turbo-realtime` 系列禁止修改 `temperature`/`top_p` 等生成参数，若需可控输出，请选用 `qwen3.5-omni-realtime` 或 `qwen3.5-omni-plus-realtime`。  

如需进一步评估，建议使用百炼控制台的 **“实时 API 压测沙箱”** 工具，针对目标终端与网络模拟真实流量，对比首字节延迟（TTFT）、端到端延迟（E2E Latency）与错误率（WER/CER）。

## 被对比主题页

- [omni realtime api](../api/omni-realtime-api.md)
- [realtime api user guide](../api/realtime-api-user-guide.md)



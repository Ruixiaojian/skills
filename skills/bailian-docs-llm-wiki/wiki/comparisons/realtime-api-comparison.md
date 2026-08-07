# 实时API方案对比：Omni Realtime API vs Realtime API

为帮助开发者在构建低延迟、多模态实时交互应用（如智能客服、虚拟助手、语音翻译、AI陪练等）时做出精准技术选型，本文系统对比百炼平台两大核心实时能力接口：**Omni Realtime API** 与 **Realtime API**。二者虽同属“实时”范畴，但在协议栈设计、模型支持粒度、功能边界、接入复杂度及适用场景上存在本质差异。本对比基于最新稳定版文档（2024年Q3），聚焦可落地的技术事实，不涉及未来规划或实验性特性。

---

## 关键维度对比

| 维度 | Omni Realtime API | Realtime API |
|------|-------------------|--------------|
| **核心定位** | **会话驱动的全模态实时对话引擎**：以自然对话节奏为中心，强耦合语音输入→语义理解→工具/搜索→多模态响应的端到端闭环 | **协议抽象层+模型能力矩阵**：提供统一通信协议栈（AOQ/WebRTC/WebSocket），解耦传输与模型，支持多样化实时AI任务（ASR/TTS/翻译/对话/多模态） |
| **输入格式** | • 音频：**强制 16kHz PCM**（`input_audio_format` 仅支持 `"pcm"`）<br>• 文本：通过 `conversation.item.create` 提交<br>• 图像：`append_video`（JPG/JPEG，≤256KB Base64）<br>• **不支持自定义编解码或原始帧输入** | • 音频：**支持多种格式**（`"pcm"`、`"opus"`、`"wav"` 等，具体依模型而定）；AOQ/WebRTC 支持 Opus 原生流<br>• 文本/图像：按模型能力独立支持（如 `multimodal-dialog` 支持图像，ASR 模型仅支持音频）<br>• **支持高级自定义输入**：AOQ 可推原始音频帧（I2S/PCM）、视频帧（I420/NV12/BGRA/JPEG） |
| **输出格式** | • 文本：结构化事件流（`response.content_part.added`）<br>• 音频：**强制 24kHz PCM**（`output_audio_format` 仅支持 `"pcm"`）<br>• **无原始音视频流控制权**，纯服务端合成输出 | • 文本：事件流（WebSocket）或 DataChannel 消息（WebRTC/AOQ）<br>• 音频：**格式灵活**（`"pcm"`、`"opus"`、`"wav"`），TTS 模型可配置采样率与比特率<br>• **支持原始音视频流输出**：AOQ/WebRTC 可直接接收编码后音视频流（如 Opus 包），供客户端自定义播放/混音/录制 |
| **支持模型** | • 仅限 `qwen*-omni-*realtime` 全模态系列：<br> – `qwen3.5-omni-realtime`（唯一支持 `semantic_vad` + `enable_search`）<br> – `qwen3-omni-flash-realtime`（唯一支持 `smooth_output`）<br> – `qwen-omni-turbo-realtime`（参数完全不可调，轻量级）<br>• **不支持 ASR/TTS/翻译等单模态模型** | • **全模型谱系覆盖**：<br> – 全模态：`qwen3.5-omni-plus-realtime`, `qwen3.5-omni-flash-realtime`<br> – 语音翻译：`qwen3.5-livetranslate-flash-realtime`<br> – ASR：`Qwen-Audio-3.0-ASR-Flash-Streaming`, `Fun-ASR-Realtime`<br> – TTS：`CosyVoice` 系列<br> – 对话：`qwen-audio-3.0-realtime-plus`<br> – 多模态开发套件：`multimodal-dialog`<br>• **协议支持因模型而异**（如 ASR/TTS 不支持 WebRTC） |
| **API 端点与协议** | • **仅 WebSocket 协议**：<br> `wss://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api-ws/v1/realtime`<br>• 无 AOQ/WebRTC 支持 | • **三协议统一接入**：<br> – AOQ（推荐移动端原生）：`moq://...` + `aoqTokenForClient`<br> – WebRTC（推荐浏览器/弱网）：SDP 交换建连，白名单开放<br> – WebSocket（推荐服务端/快速验证）：`wss://.../api-ws/v1/realtime`<br>• 同一模型在不同协议下能力一致（ASR/TTS 除外） |
| **计费方式** | • **按 token + 音频时长双重计费**：<br> – 输入文本 token、输出文本 token<br> – 输入音频时长（秒）、输出音频时长（秒）<br>• **无连接时长费**，但 VAD 超时（`idle_timeout_ms`）触发的引导响应计入费用 | • **按模型+协议+资源维度计费**：<br> – ASR/TTS/翻译/对话等模型按调用次数或时长计费<br> – AOQ/WebRTC 连接产生带宽与中继费用<br> – WebSocket 按标准 API 调用计费<br>• **明确区分模型成本与传输成本** |
| **典型场景** | • 需要**强语义理解+自然对话节奏**的场景：<br> – 智能客服（支持工具调用查订单、`enable_search` 解答知识库外问题）<br> – 虚拟陪伴助手（多轮上下文、语音+文本混合输出、声音复刻）<br> – 教育陪练（实时纠错、口语反馈、`semantic_vad` 精准切分学生发言） | • 需要**协议灵活性+多任务组合**的场景：<br> – 移动端会议APP（AOQ 低延迟传输 + `qwen3.5-livetranslate-flash-realtime` 实时翻译）<br> – 浏览器端语音助手（WebRTC 弱网对抗 + `qwen-audio-3.0-realtime-plus` 对话）<br> – 服务端批量语音处理（WebSocket + `Qwen-Audio-3.0-ASR-Flash-Streaming` 流式转写）<br> – 自定义音视频工作流（AOQ 推送 TTS 输出流 + 外部混音器） |
| **VAD 能力** | • 两种模式：<br> – `server_vad`（默认，服务端检测）<br> – `semantic_vad`（仅 `qwen3.5-omni-realtime`，语义级静音判断，更精准）<br>• `idle_timeout_ms` 仅对部分模型生效（需 `server_vad`） | • `semantic_vad` 为通用推荐配置，**所有支持语音输入的模型均可启用**<br>• 无 `server_vad` 概念，VAD 行为由模型与协议协同决定（如 AOQ 在传输层做初步静音过滤） |
| **扩展能力** | • 工具调用（`tools`）与联网搜索（`enable_search`）**互斥**，且仅 `qwen3.5-omni-realtime` 支持后者<br>• **不支持自定义音视频处理链路**（如外部降噪、回声消除） | • 工具调用、搜索、多步推理等能力**按模型独立支持**，无全局互斥限制<br>• **支持深度音视频定制**：AOQ 可接入外部音频采集/处理模块、自定义视频编码器、第三方播放器集成 |

---

## 适用场景建议

### ✅ 选择 Omni Realtime API 当：
- 你的核心需求是构建一个**以自然语言对话为第一体验**的应用，强调上下文连贯性、语音交互节奏感和多模态响应一致性；
- 你需要开箱即用的**语义级 VAD（`semantic_vad`）** 或 **联网搜索能力（`enable_search`）**，且接受其仅在 `qwen3.5-omni-realtime` 上可用；
- 你采用 **WebSocket 架构**，服务端具备 WebSocket 长连接管理能力，且无需在客户端处理音视频编解码细节；
- 你追求**快速上线验证**，希望最小化客户端 SDK 集成复杂度（如无须集成 AOQ/WebRTC 库、Opus 插件等）。

### ✅ 选择 Realtime API 当：
- 你需要**跨平台、跨网络环境**部署（如 iOS/Android/HarmonyOS/浏览器/服务端），且对弱网鲁棒性、端到端延迟有严苛要求；
- 你的业务涉及**多种实时 AI 任务组合**（例如：前端用 WebRTC 做语音输入 → 后端用 WebSocket 调用 ASR → 再调用 TTS 生成音频 → 最终通过 AOQ 推送给移动端）；
- 你需要**完全掌控音视频数据流**，例如：在客户端集成专业降噪算法、自定义音频混音逻辑、对接硬件音频设备、或实现低延迟屏幕共享；
- 你正在构建**企业级音视频中间件**，需要将百炼能力作为底层组件嵌入自有通信协议栈，而非直接面向终端用户交付对话界面。

---

## 技术选型参考（致开发者）

| 你的问题 | 推荐方案 | 理由简述 |
|----------|-----------|-----------|
| “我只想快速做一个微信小程序里的语音客服，支持说话提问、文字+语音回答，不需要复杂定制。” | **Omni Realtime API** | WebSocket 易接入，`qwen3.5-omni-realtime` 开箱即用 `semantic_vad` + 工具调用，小程序端用 `wx.connectSocket` 即可，无编解码负担。 |
| “我们APP要在地铁、电梯等弱网环境下提供实时翻译，必须保证卡顿率 < 1%。” | **Realtime API（AOQ 协议）** | AOQ 基于 QUIC，专为弱网优化；`qwen3.5-livetranslate-flash-realtime` 模型针对翻译场景深度优化；SDK 提供自动重传、前向纠错等机制。 |
| “我们需要把百炼的 TTS 集成进现有 VoIP 系统，要求输出 Opus 流并精确控制每个音频包的时间戳。” | **Realtime API（AOQ 或 WebSocket）** | Realtime API 明确支持 `opus` 输出格式与毫秒级时间戳控制；Omni API 强制 `24kHz PCM`，无法满足此需求。 |
| “我们的产品需要同时支持语音输入、图像上传识别、以及调用内部 API 查询数据——三者需在同一轮对话中协同。” | **Omni Realtime API** | `qwen3.5-omni-realtime` 原生支持 `append_video` + `tools`，且在同一会话上下文中完成多模态融合推理；Realtime API 中 `multimodal-dialog` 与 `tools` 属不同模型能力，需自行编排。 |
| “我们是 SaaS 厂商，要为客户提供可嵌入的‘AI 实时语音插件’，兼容网页、Electron、iOS App 三种形态。” | **Realtime API（WebRTC + WebSocket + AOQ 分别适配）** | Realtime API 的三协议设计天然匹配多端：WebRTC 用于网页，WebSocket 用于 Electron，AOQ 用于 iOS；Omni API 仅 WebSocket，无法覆盖全场景。 |

> **重要提醒**：  
> - **安全红线**：若客户端直连（尤其 WebRTC/WebSocket），务必通过服务端代理鉴权，禁止硬编码 API Key；AOQ 协议强制使用临时 `aoqTokenForClient`，安全性更高。  
> - **模型演进**：`qwen-omni-turbo-realtime` 等轻量模型参数不可调，适合固定场景；若需精细控制生成质量（如 `temperature` 调节创意性），请选用 `qwen3.5-omni-realtime` 或 Realtime API 中支持参数调节的模型。  
> - **成本意识**：Omni API 的音频时长计费对长语音场景成本敏感；Realtime API 中 ASR/TTS 按调用计费，更适合短语音高频交互。  

如需进一步评估，请结合 [模型能力矩阵](../../raw/model-api-reference) 与 [SDK 快速启动指南](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-quick-start-guide.md) 进行原型验证。

## 被对比主题页

- [omni realtime api](../api/omni-realtime-api.md)
- [realtime api user guide](../api/realtime-api-user-guide.md)



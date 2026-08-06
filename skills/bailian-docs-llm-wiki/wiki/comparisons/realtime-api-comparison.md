# 实时 API 方案对比：Omni Realtime API vs Realtime API

本文旨在帮助开发者清晰理解百炼平台当前两大实时交互接口——**Omni Realtime API** 与 **Realtime API** 的核心差异，辅助技术选型决策。二者虽均面向低延迟、[多模态](../concepts/multimodal.md)实时对话场景，但在协议设计、能力边界、模型支持、接入复杂度及适用生态上存在系统性差异。本对比基于最新稳定版文档（2024年Q3），聚焦可落地的技术事实，不涉及未公开或实验性功能。

## 关键维度对比

| 维度 | Omni Realtime API | Realtime API |
|------|-------------------|--------------|
| **协议基础** | **纯 WebSocket 协议**（强制 `wss://` 连接），事件驱动、会话生命周期由客户端显式管理（`session.update` 等） | **三协议统一抽象**：支持 **AOQ**（专有低延迟协议）、**WebRTC**（浏览器/音视频通话标准）、**WebSocket**（轻量兼容模式）；协议选择直接影响能力集与部署形态 |
| **输入格式** | ✅ PCM 音频（**严格 16 kHz**，单通道）<br>✅ JPG/JPEG 图像（≤1080p，Base64 编码，单图 ≤256 KB）<br>❌ 不支持视频流、MP3/WAV 等编码、文本直接输入（需通过 `input_text` 事件，但非主流路径） | ✅ PCM 音频（**严格 16 kHz**）<br>✅ 视频帧（H.264/H.265，通过 AOQ/WebRTC 原生传输）<br>✅ 文本（`input_text` 事件）<br>❌ 不支持图像上传（无 Base64 图片事件） |
| **输出格式** | ✅ 文本（流式 `response.content_part.added`）<br>✅ 音频（**固定 24 kHz PCM**，`response.audio.delta`）<br>❌ 不支持视频输出、TTS 音色参数化控制（仅通过 `voice` 字符串指定） | ✅ 文本（流式）<br>✅ 音频（**固定 24 kHz PCM**）<br>✅ 视频（AOQ/WebRTC 下支持服务端生成并推送 H.264/H.265 流）<br>✅ 支持细粒度 TTS 控制（如语速、语调、停顿标记，取决于模型） |
| **支持模型** | 仅限 **Qwen-Omni 系列实时模型**：<br>`qwen3.5-omni-realtime`、`qwen3.5-omni-plus-realtime`、<br>`qwen3.5-omni-flash-realtime`、`qwen3-omni-flash-realtime`、<br>`qwen-omni-turbo-realtime`<br>（*不支持 ASR/TTS 独立模型或非 Omni 架构模型*） | **全模型谱系覆盖**：<br>✅ Qwen-Omni 全系列（含 `plus`/`flash`）<br>✅ 实时语音识别（ASR）：`Qwen-Audio-3.0-ASR-Flash-Streaming`<br>✅ 实时语音合成（TTS）：`CosyVoice` 系列<br>✅ 实时翻译：`qwen3.5-livetranslate-flash-realtime`<br>✅ [多模态](../concepts/multimodal.md)开发套件：`multimodal-dialog`<br>✅ 实时语音对话：`qwen-audio-3.0-realtime-plus` |
| **API 端点** | 单一 WebSocket 地址：<br>`wss://{WorkspaceId}.{region}.maas.aliyuncs.com/api-ws/v1/realtime`<br>（地域强绑定，需按 Workspace 配置） | **协议差异化端点**：<br>- AOQ：通过 `allocate` 接口获取动态 Relay 地址（含 `relayEndpoints`）<br>- WebRTC：`https://{endpoint}/api/v1/webrtc/realtime?model={model_name}`（HTTP 信令 + SDP 交换）<br>- WebSocket：`wss://{endpoint}/api/v1/ws/realtime?model={model_name}`（类 Omni，但行为不同） |
| **计费方式** | **按 token + 音频时长双重计费**：<br>- 输入/输出文本 token（按千 token 计）<br>- 输入音频时长（秒，按实际发送的 PCM 数据时长计）<br>- *不单独计费图像*（计入请求带宽，但无显式图像费用） | **按模型能力分项计费**：<br>- ASR 模型：按识别音频时长（秒）计费<br>- TTS 模型：按合成音频时长（秒）计费<br>- Omni/对话类模型：按 token + 音频时长计费（同 Omni API）<br>- *视频处理能力另计*（如启用服务端视频生成） |
| **高级能力** | ✅ 工具调用（`tools`，仅 `qwen3.5-omni-realtime`）<br>✅ 联网搜索（`enable_search`，仅 `qwen3.5-omni-realtime`，与 tools 互斥）<br>✅ Semantic VAD（仅 `qwen3.5-omni-realtime`）<br>✅ 声音复刻音色集成（需严格匹配 `target_model`）<br>❌ 无回声消除、降噪、AGC 等音频前处理能力 | ✅ 工具调用（部分 Omni 模型）<br>✅ 联网搜索（同 Omni）<br>✅ Semantic VAD（通用支持）<br>✅ **AOQ 内置专业音频处理**：回声消除（AEC）、噪声抑制（ANS）、自动增益控制（AGC）、丢包补偿（PLC）<br>✅ **WebRTC 原生音视频同步与 QoS 保障**<br>❌ 声音复刻需通过独立 API 预注册，与 Realtime API 调用解耦 |
| **典型场景** | - 智能客服语音坐席（需快速响应+语音+简单图文辅助）<br>- 轻量级虚拟助手 App（移动端 WebView 或简易 SDK 集成）<br>- 对话式 AI 应用原型验证（快速启动，无需音视频基建） | - 全栈智能硬件（车载、机器人、AR眼镜）→ 选用 **AOQ**<br>- 浏览器端实时会议助手/同传 → 选用 **WebRTC**<br>- 服务端语音中台（需同时调度 ASR+TTS+Omni）→ 选用 **WebSocket**<br>- [多模态](../concepts/multimodal.md)人机协作系统（需音视频+文本+工具链闭环） |

## 各方案适用场景建议

### ✅ 选择 Omni Realtime API 当：
- 你的产品是 **以语音为核心、文本为辅的轻量级对话应用**（如电话客服 IVR 升级、小程序语音助手）；
- 你已具备音频采集/播放能力（如使用 Web Audio API 或原生 SDK），**无需服务端提供音频前处理**；
- 你明确只需要 **Qwen-Omni 系列模型**，且业务逻辑不依赖 ASR/TTS 独立能力；
- 你追求 **最简接入路径**：一个 WebSocket 连接 + 标准 JSON 事件即可启动，适合前端或快速 PoC；
- 你需要 **工具调用或联网搜索**，且接受其仅在 `qwen3.5-omni-realtime` 上可用的限制。

### ✅ 选择 Realtime API 当：
- 你的终端覆盖 **多平台**（iOS/Android/Web/嵌入式），且对 **弱网、高抖动、回声场景有严苛要求** → 必选 **AOQ**；
- 你需要构建 **浏览器原生音视频应用**（如在线教育实时答疑、远程医疗问诊）→ 必选 **WebRTC**；
- 你的架构需要 **混合调用多种实时模型**（例如：先 ASR 识别用户语音 → 送 Omni 理解意图 → 调用工具 → 用 CosyVoice 合成回复）→ 必选 **Realtime API 的统一协议抽象**；
- 你正在开发 **AI 原生硬件设备**（如智能音箱、陪伴机器人），需服务端提供 **端到端音视频链路保障与专业音频处理**；
- 你要求 **视频理解或生成能力**（如实时手势识别、虚拟形象驱动），必须通过 AOQ/WebRTC 协议栈。

## 技术选型参考指南（致开发者）

| 你的需求 | 推荐方案 | 关键理由 |
|----------|-----------|-----------|
| “我只想用几行 JS 在网页里跑个语音问答 demo” | **Omni Realtime API** | WebSocket 直连，无信令协商，SDK 封装成熟，10 分钟可跑通流式语音对话 |
| “我的 App 要在地铁/电梯等弱网环境稳定工作，用户抱怨语音卡顿、回声大” | **Realtime API + AOQ** | AOQ 协议内置 AEC/ANS/PLC，Relay 架构抗丢包，实测 30% 丢包下仍可维持可懂度 |
| “我要做一款支持中英日韩实时互译的会议软件，用户用 Chrome 打开即用” | **Realtime API + WebRTC** | 浏览器原生支持，无需安装插件；WebRTC DataChannel 保证事件低延迟；可同时传输音轨+字幕+翻译结果 |
| “我有一个语音中台，要统一调度 ASR、TTS、大模型对话，后端用 Python 写” | **Realtime API + WebSocket** | 同一协议接入所有模型类型；服务端可灵活编排 pipeline；DashScope SDK 提供 Python 同步/异步封装 |
| “我需要让 AI 看见用户上传的照片并回答问题（如‘这张发票金额是多少？’）” | **Omni Realtime API** | 唯一支持 Base64 图像输入的实时 API；`qwen3.5-omni-realtime` 具备强图文理解能力 |
| “我要给硬件设备烧录固件，实现离线唤醒+云端实时对话，对启动速度和内存占用敏感” | **Realtime API + AOQ（精简 SDK）** | AOQ C++ SDK 可裁剪至 <500KB；支持硬件加速音频处理；连接建立耗时 <300ms |

> **重要提醒**：  
> - **不要混用协议与模型**：`qwen3.5-omni-realtime` 在 Omni Realtime API 和 Realtime API（WebSocket 模式）中行为一致，但 `Qwen-Audio-3.0-ASR-Flash-Streaming` **仅 Realtime API 支持**；  
> - **音频采样率是硬约束**：两个 API 均**强制要求输入 16 kHz PCM、输出 24 kHz PCM**，任何偏差将导致连接失败或静音；  
> - **VAD 配置需匹配模型**：`semantic_vad` 仅 `qwen3.5-omni-realtime` 支持，若误用于 `qwen-omni-turbo-realtime` 将被忽略；  
> - **生产环境务必启用重连机制**：WebSocket 连接可能因网络抖动断开，Omni Realtime API 无自动重连，Realtime API 的 AOQ/WebRTC SDK 提供内置重连策略（需配置 `maxRetries`）。  

如需进一步验证性能指标（端到端延迟 P95、弱网吞吐量、并发连接数上限），请查阅《百炼实时 API 性能白皮书》或联系技术支持申请压测支持。

## 被对比主题页

- [omni realtime api](../api/omni-realtime-api.md)
- [realtime api user guide](../api/realtime-api-user-guide.md)



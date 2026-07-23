# 实时 API 对比：Realtime API vs Omni Realtime API

本文旨在帮助开发者清晰理解百炼平台提供的两类核心实时交互能力——**Realtime API** 与 **Omni Realtime API** 的技术定位、能力边界与适用场景，避免因协议选型不当导致集成成本上升、功能缺失或性能不达预期。二者虽均面向“实时 AI 交互”，但在架构设计、协议栈、模型支持、控制粒度及工程落地路径上存在系统性差异。本对比基于最新文档（2024 Q3）整理，适用于新项目技术选型与存量系统升级评估。

## 关键维度对比

| 维度 | Realtime API | Omni Realtime API |
|------|--------------|-------------------|
| **协议栈与传输层** | 提供 **三套并行协议栈**：WebSocket、WebRTC、AOQ（AI over QUIC），可按终端/网络/功能需求灵活选择 | **仅基于 WebSocket**（`wss://.../api-ws/v1/realtime`），事件驱动、JSON-RPC 风格，无原生音视频信令能力 |
| **输入格式** | • WebSocket：支持文本、PCM 音频（16 kHz）、Base64 图像（分通道）<br>• WebRTC/AOQ：支持音视频流 + 数据通道混合传输（如 `oai-events` DataChannel） | • **统一 JSON 事件流**：<br>– `input_audio_buffer.append`（PCM，16 kHz）<br>– `input_image.append`（JPG/JPEG，≤256 KB Base64）<br>– 文本通过 `instructions` 或 ASR 转录隐式注入<br>• **不支持原始音视频流直传** |
| **输出格式** | • WebSocket：纯文本 + 分离音频流（需客户端合成）<br>• WebRTC/AOQ：原生音视频流 + 结构化事件（如 `session.updated`、`response.audio.delta`） | • **同步双模态输出**：服务端直接返回 `<text>` + `<audio delta>` 流式 PCM（24 kHz），支持 `modalities: ["text", "audio"]` 或 `["text"]` |
| **支持模型** | • 全系列实时模型：<br>– `qwen3.5-omni-plus-realtime` / `qwen3.5-omni-flash-realtime`<br>– `qwen3.5-livetranslate-flash-realtime`<br>– `qwen-audio-3.0-realtime-plus`<br>– Fun-ASR / CosyVoice 独立语音模型<br>• 多模态套件 `multimodal-dialog`（WebRTC/WebSocket 支持，AOQ 不支持） | • **仅 `-realtime` 后缀的 Omni 系列模型**：<br>– `qwen3.5-omni-realtime`（全能力）<br>– `qwen3.5-omni-plus-realtime` / `qwen3.5-omni-flash-realtime`（无 `semantic_vad`）<br>– `qwen3-omni-flash-realtime`（风格控制）<br>– `qwen-omni-turbo-realtime`（固定参数）<br>• **不支持独立 ASR/TTS 模型或 `multimodal-dialog`** |
| **VAD（语音活动检测）能力** | • WebSocket：仅支持 `server_vad`（服务端静音检测）<br>• WebRTC/AOQ：支持 `server_vad` + **端侧 AEC/降噪**，但无 `semantic_vad` | • `qwen3.5-omni-realtime`：支持 **`semantic_vad`**（语义级起止判断，更精准）<br>• 其他 Omni 模型：仅 `server_vad`，但支持 `idle_timeout_ms` 主动引导 |
| **工具调用与联网搜索** | • 未明确支持结构化工具调用或联网搜索能力 | • **仅 `qwen3.5-omni-realtime` 支持**：<br>– `tools`：定义函数列表，服务端触发 `function_call` 事件<br>– `enable_search`：启用联网检索（与 `tools` 互斥） |
| **API 端点** | • WebSocket：`wss://{workspace}.region.maas.aliyuncs.com/api/v1/realtime`<br>• WebRTC：`https://{workspace}.region.maas.aliyuncs.com/api/v1/webrtc/inference`（Offer/Answer 代理）<br>• AOQ：`https://{workspace}.region.maas.aliyuncs.com/api/v1/webrtc/realtime?model=...`（需 `x-dashscope-rtc-transport: moq`） | • 统一 WebSocket 端点：<br>`wss://{WorkspaceId}.region.maas.aliyuncs.com/api-ws/v1/realtime`<br>• **必须使用业务空间专属域名**（旧域名已弃用） |
| **鉴权方式** | • WebSocket/WebRTC：`Authorization: Bearer <API_KEY>` 直连<br>• AOQ：**强制 AppServer 代领 `aoqTokenForClient`**，客户端仅持临时 Token 连接（安全增强） | • `Authorization: Bearer <API_KEY>` 直连 WebSocket，无中间 Token 代理要求 |
| **计费方式** | • 按 **实际消耗 Token 数 + 音频时长（秒）** 双维度计费<br>• 不同协议下相同模型单位成本一致，但 AOQ/WebRTC 因弱网优化可能降低重传开销 | • 按 **输入 Token + 输出 Token + 音频时长（秒）** 计费<br>• 图像输入按分辨率折算 Token，`qwen-omni-turbo-realtime` 有独立低价套餐 |
| **典型场景** | • 弱网环境下的移动端实时通话（AOQ）<br>• 浏览器端音视频+数据混合交互（WebRTC）<br>• 快速验证/服务端托管的语音客服原型（WebSocket） | • 高保真语音助手（语义 VAD + 流式音频）<br>• 智能客服中台（工具调用 + 联网搜索）<br>• 多模态输入（语音+图片）的轻量级应用（如拍照问诊） |

## 适用场景建议

### ✅ 选择 **Realtime API** 当：
- 需要 **原生音视频能力**（如视频会议嵌入 AI 助手、AR 眼镜实时翻译）；
- 终端为 **移动端原生 App**，且对 **500ms 内端到端延迟、弱网鲁棒性（丢包率 >15%）有硬性要求** → 优先选用 **AOQ**；
- 已有 **WebRTC 基础设施**（如自研音视频 SDK），希望复用 ICE/STUN/TURN 逻辑 → 选用 **WebRTC 协议**；
- 快速搭建 **服务端驱动的语音机器人**（如 IVR 系统），无需浏览器兼容性 → 选用 **WebSocket 协议**；
- 需要 **独立 ASR/TTS 模块** 或 **多模态对话套件 `multimodal-dialog`**（如手势+语音协同控制）。

### ✅ 选择 **Omni Realtime API** 当：
- 构建 **纯 WebSocket 架构的中台服务**，要求统一协议、简化运维（避免维护多套连接逻辑）；
- 核心诉求是 **高精度语义级语音断句（`semantic_vad`）** 与 **文本+音频同步流式响应**（如虚拟主播、无障碍播报）；
- 业务需 **结构化工具调用**（如查订单、改地址）或 **实时联网检索**（如政策咨询、新闻摘要）→ 必选 `qwen3.5-omni-realtime`；
- 输入含 **图像+语音混合内容**（如“这张发票金额是多少？”），且希望服务端统一处理多模态对齐；
- 团队熟悉 JSON-RPC 事件模型，追求 **最小 SDK 依赖**（仅需标准 WebSocket 客户端 + 百炼 SDK 封装）。

### ⚠️ 避免混用的典型误区：
- 误将 `qwen3.5-omni-plus`（非实时 batch 模型）用于 Omni Realtime API → 连接立即失败；
- 在 AOQ 协议下尝试调用 `multimodal-dialog` 模型 → 服务端拒绝响应（文档明确标注 ❌）；
- 期望 Omni Realtime API 提供 WebRTC 音视频流 → 其输出仅为 `audio.delta` 字节流，需客户端合成播放；
- 使用旧域名 `dashscope.aliyuncs.com` 接入 Omni Realtime API → 连接成功率下降，延迟波动大。

## 技术选型决策参考

| 决策因素 | Realtime API 更优 | Omni Realtime API 更优 |
|----------|-------------------|-------------------------|
| **终端类型** | 移动端原生 App（iOS/Android/HarmonyOS）、Web 浏览器（需音视频） | Web 应用、Electron 桌面端、服务端 Node.js 中台 |
| **网络环境** | 弱网（地铁、偏远地区）、高丢包、高抖动 | 稳定宽带/WiFi、企业内网 |
| **功能复杂度** | 需音视频流控、AEC、多路数据通道、自定义媒体处理 | 专注 AI 逻辑：VAD、多模态理解、工具编排、流式音频生成 |
| **开发资源** | 有音视频协议栈经验（WebRTC/AOQ SDK 集成能力） | 熟悉 WebSocket/EventSource、偏好声明式配置（`session.update`） |
| **安全合规要求** | 敏感场景需 API Key 严格隔离（AOQ 的 token 代理机制） | 标准 Bearer Token 鉴权已满足多数场景 |
| **长期演进** | 协议栈持续扩展（如未来支持 AV1 编码、低功耗 BLE 传输） | 模型能力深度迭代（`semantic_vad` 优化、多图理解、3D 场景支持） |

> **总结建议**：  
> - 若项目以 **“实时音视频交互”为第一优先级**（如远程医疗问诊、在线教育互动白板），请选择 **Realtime API（WebRTC/AOQ）**；  
> - 若项目以 **“AI 对话智能”为核心**（如金融投顾助手、政务智能问答），且接受 WebSocket 架构，则 **Omni Realtime API 是更简洁、能力更聚焦的选择**；  
> - 对于混合需求（如既需视频画面分析，又需语音对话），建议采用 **Realtime API（WebRTC）承载音视频，叠加 Omni Realtime API 处理语音语义**，通过会话 ID 关联两路流——这是当前最佳实践组合。

## 被对比主题页

- [realtime api user guide](../api/realtime-api-user-guide.md)
- [omni realtime api](../api/omni-realtime-api.md)



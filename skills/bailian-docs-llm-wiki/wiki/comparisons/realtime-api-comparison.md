# 实时 API 方案对比：Realtime API 与 Omni Realtime API

本文旨在帮助开发者清晰理解百炼平台两类核心实时交互能力——**Realtime API** 与 **Omni Realtime API** 的定位差异、能力边界与技术选型依据。随着[多模态](../concepts/multi-modal.md) AI 应用向低延迟、强交互、跨终端方向演进，选择适配业务场景的实时接口方案，直接影响端到端体验质量、开发效率与运维成本。本对比基于当前（2024 Q3）正式发布的功能与文档规范，聚焦可落地的技术维度，不涉及内部架构或未公开灰度能力。

---

## 关键维度对比

| 维度 | Realtime API | Omni Realtime API |
|------|--------------|-------------------|
| **协议基础** | 支持三协议：AOQ（专有低延迟协议）、WebRTC、WebSocket | **仅 WebSocket**（标准协议，无 AOQ/WebRTC 支持） |
| **输入格式** | [多模态](../concepts/multi-modal.md)灵活接入：<br>• AOQ/WebRTC：原生音频/视频流（PCM/NV12 等）<br>• WebSocket：分块 PCM 音频（`append_audio`）+ 文本事件 | 仅支持 **WebSocket 分块 PCM 音频流**（16 kHz） + 文本指令；不支持原始视频帧或编码帧输入 |
| **输出格式** | • 文本 + 音频（PCM，24 kHz）<br>• 可选视频流（WebRTC/AOQ 下支持 H.264 编码帧或原始帧渲染）<br>• [多模态](../concepts/multi-modal.md)结构化事件（如 `modalities: ["text", "audio", "video"]`） | • 文本 + 音频（PCM，24 kHz）<br>• **不支持视频输出**；所有模型仅返回 `["text"]` 或 `["text","audio"]` |
| **支持模型** | • 全模态模型：`qwen3.5-omni-plus-realtime`、`qwen3.5-omni-flash-realtime` 等<br>• 多模态套件：`multimodal-dialog`（WebRTC/WebSocket）<br>• 语音专项：Fun-ASR（WS）、CosyVoice（WS）、`qwen-audio-*`（WS） | • 仅 `qwen3.x-omni-*` 系列模型：<br> `qwen3.5-omni-realtime`、`qwen3.5-omni-plus-realtime`、`qwen3.5-omni-flash-realtime`、<br> `qwen3-omni-flash-realtime`、`qwen-omni-turbo-realtime`<br>• **不支持 ASR、TTS、对话模型等非 Omni 系列模型** |
| **API 端点** | • AOQ：`https://dashscope.aliyuncs.com/api/v1/realtime/allocate`（鉴权） + 客户端直连网关<br>• WebRTC：白名单专属 STUN/TURN + Signaling Endpoint（需商务开通）<br>• WebSocket：`wss://.../api-ws/v1/realtime`（统一入口） | • 统一 WebSocket 端点：<br> `wss://{WorkspaceId}.{region}.maas.aliyuncs.com/api-ws/v1/realtime`（推荐）<br> 或兼容旧域名 `wss://dashscope.aliyuncs.com/api-ws/v1/realtime` |
| **计费方式** | • 按 **连接时长（秒） + 流量（MB）** 双维度计费<br>• AOQ/WebRTC 连接时长计费；WebSocket 按会话生命周期计费<br>• 音频/视频编解码、传输带宽单独计量 | • 按 **[Token](../concepts/token.md) 消耗量（输入 + 输出）** 计费<br>• 音频流按等效文本 [Token](../concepts/token.md) 折算（1 秒 16 kHz PCM ≈ 100 tokens）<br>• **不单独收取连接时长或流量费用** |
| **典型场景** | • 原生 App 内嵌超低延迟音视频互动（如远程医疗问诊、AR 教育）<br>• 浏览器端实时协作白板 + 语音批注（WebRTC）<br>• 后台服务对接 ASR/TTS 流式处理（WebSocket） | • Web/H5 虚拟助手（客服对话、智能导购）<br>• 小程序/轻应用中语音唤醒 + 多轮问答 + 语音播报<br>• 需要[工具调用](../concepts/tool-use.md)（天气查询、订单状态）或联网搜索的对话系统 |

---

## 适用场景建议

### ✅ 推荐选用 **Realtime API** 当：
- **终端类型为原生移动 App（Android/iOS/HarmonyOS）且对弱网鲁棒性要求极高** → 必选 AOQ 协议，其自适应丢包补偿、Opus 超窄带编码、端到端 <200ms 延迟是 WebRTC/WebSocket 无法替代的；
- **需同时处理音视频流并进行多模态联合推理**（如手势+语音指令识别）→ `multimodal-dialog` 套件仅 Realtime API 支持；
- **已有 ASR/TTS 服务链路需无缝集成** → Fun-ASR / CosyVoice 等语音专项模型仅通过 Realtime API 的 WebSocket 接入；
- **浏览器端需原生音视频采集与渲染**（如在线面试、远程协作）→ WebRTC 提供最佳兼容性与媒体控制粒度。

### ✅ 推荐选用 **Omni Realtime API** 当：
- **目标平台为 Web/H5/小程序等轻量级前端环境**，且无需视频能力 → WebSocket 协议零依赖、易调试、免 SDK；
- **核心需求是“语音输入 → 文本+语音输出”的闭环对话**，并需要 VAD 自动断句、[工具调用](../concepts/tool-use.md)或联网搜索 → Omni 系列模型深度优化该路径，`semantic_vad`、`tools`、`enable_search` 均开箱即用；
- **追求快速上线与低成本维护** → 无需管理连接状态机、媒体轨道、回声消除等底层细节，SDK 封装完善（DashScope JS/Python SDK）；
- **对生成可控性有明确要求**（如温度调节、最大 token 限制）→ `qwen3.5-omni-realtime` 和 `qwen3-omni-flash-realtime` 支持全参数调节，而 Turbo 版本提供极致性能与确定性。

### ⚠️ 不建议混用或迁移的典型情况：
- 若已基于 Realtime API 的 AOQ 开发成熟 App，**不建议为新增 H5 页面单独引入 Omni Realtime API** —— 会导致模型微调、提示词、VAD 配置逻辑双线维护；
- 若业务需 `multimodal-dialog` 或 `qwen-audio-3.0-realtime-plus`，**Omni Realtime API 完全不可替代**；
- 若依赖 `qwen-omni-turbo-realtime` 的固定采样参数特性（如合规场景），**Realtime API 无对应 Turbo 模型**，不可迁移。

---

## 技术选型参考指南（面向开发者）

| 决策问题 | Realtime API | Omni Realtime API | 建议动作 |
|----------|--------------|-------------------|----------|
| **是否必须在 iOS/Android App 中实现 <300ms 端到端延迟？** | ✅ 强支持（AOQ） | ❌ 仅 WebSocket，延迟更高 | 选 Realtime API + AOQ SDK |
| **是否需在浏览器中直接调用摄像头+麦克风，并渲染远端视频？** | ✅ WebRTC 原生支持 | ❌ 不支持视频输入/输出 | 选 Realtime API + WebRTC |
| **是否只需语音唤醒+问答+播报，且部署在微信小程序？** | ⚠️ 可行但需自行处理 WebSocket 媒体流拼接 | ✅ 最佳匹配（轻量、SDK 完善） | 选 Omni Realtime API |
| **是否需调用外部 API（如查快递、订会议室）并让模型自主决策？** | ❌ 不支持[工具调用](../concepts/tool-use.md) | ✅ `tools` 字段原生支持（仅 `qwen3.5-omni-realtime`） | 选 Omni Realtime API |
| **是否需对 ASR 结果做实时标点/语义分割？** | ✅ Fun-ASR 模型直连 | ❌ 不支持 ASR 功能 | 选 Realtime API + WebSocket |
| **是否要求所有生成参数（temperature/top_p 等）完全可控？** | ⚠️ 部分模型支持（见文档），但非 Omni 系列统一设计 | ✅ `qwen3.5-omni-realtime` / `qwen3-omni-flash-realtime` 全参数开放 | 选 Omni Realtime API（避开 Turbo） |
| **是否已有大量 WebSocket 服务端代码，希望最小改造接入？** | ✅ WebSocket 协议可用（但模型能力受限） | ✅ 原生设计，SDK 封装更友好 | 评估模型需求：若仅需 Omni 系列，优先 Omni；若需 ASR/TTS，则 Realtime API |

> **最后提醒**：  
> - **协议 ≠ 模型**：Realtime API 是传输框架，Omni Realtime API 是特定模型族的 WebSocket 封装。二者并非互斥层级，而是“能力集合”与“专用接口”的关系。  
> - **鉴权统一**：均使用 `Authorization: Bearer <API_KEY>`，但 AOQ 需额外服务端换取 `aoqTokenForClient`，Omni 直连即可。  
> - **务必验证兼容性**：AOQ 不支持 `multimodal-dialog` 等模型，Omni 不支持 `qwen-audio-*`，实际接入前请以 [模型支持列表](https://help.aliyun.com/zh/model-studio/realtime-api-model-support) 为准。  

---  
*文档更新时间：2024年10月*  
*技术咨询支持：百炼开发者社区 / 工单系统*

## 被对比主题页

- [realtime api user guide](../api/realtime-api-user-guide.md)
- [omni realtime api](../api/omni-realtime-api.md)



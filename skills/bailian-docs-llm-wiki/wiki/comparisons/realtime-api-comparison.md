# 实时 API 方案对比：Realtime API vs Omni Realtime API

本文旨在帮助开发者清晰理解百炼平台两类核心实时交互能力的技术定位与适用边界，避免因方案误选导致接入成本上升、功能缺失或性能不达预期。  
**Realtime API** 是面向多协议、多终端的**通用型实时交互基础设施**，提供 WebSocket / WebRTC / AOQ 三种传输层抽象，强调协议灵活性与场景覆盖广度；  
**Omni Realtime API** 是基于 WebSocket 的**垂直优化型语音对话接口**，专为低延迟、高保真、强交互的[多模态](../concepts/multi-modal.md)语音对话场景设计，聚焦模型能力深度与会话控制精细度。  
二者并非简单替代关系，而是“基础设施层”与“场景化能力层”的协同关系：Omni Realtime API 实际运行于 Realtime API 的 WebSocket 协议栈之上，是其在语音对话领域的标准化封装与能力增强。

---

## 关键维度对比

| 维度 | Realtime API | Omni Realtime API |
|------|--------------|-------------------|
| **协议支持** | ✅ WebSocket、✅ WebRTC、✅ AOQ（三协议统一接入） | ❌ 仅支持 WebSocket（单协议，但深度优化） |
| **输入格式** | 支持 `input_audio_buffer.append`（流式 PCM 音频）、`input_text`（文本输入）、`input_image`（图片输入，部分模型支持） | ✅ 仅支持 `input_audio_buffer.append`（PCM 音频流）<br>❌ 不支持纯文本/图像输入（无 `input_text` 或 `input_image` 事件） |
| **输出格式** | ✅ `response.text.delta` / `response.text.final`（文本）<br>✅ `response.audio.delta`（音频流）<br>✅ `response.tool_calls`（工具调用）<br>✅ [多模态](../concepts/multi-modal.md)混合输出（如 `["text", "audio", "image"]`，依模型而定） | ✅ `response.text.delta` / `response.text.final`<br>✅ `response.audio.delta`（仅 PCM）<br>❌ 不支持 `response.image` 等非语音/文本模态<br>✅ 输出模态严格限定为 `["text"]` 或 `["text", "audio"]` |
| **支持模型/应用** | • 全模态模型：<br> `qwen3.5-omni-plus-realtime`, `qwen3.5-omni-flash-realtime`, `qwen3.5-livetranslate-flash-realtime`（全协议支持）<br>• [多模态](../concepts/multi-modal.md)套件：<br> `multimodal-dialog`（仅 WebSocket/WebRTC）<br>• ASR/TTS/对话专用模型：<br> `Fun-ASR系列`、`CosyVoice系列`、`qwen-audio-3.0-realtime-*`（仅 WebSocket） | • 仅限 Omni 系列模型：<br> `qwen3.5-omni-plus-realtime`<br> `qwen3.5-omni-flash-realtime`<br> `qwen3-omni-flash-realtime`<br> `qwen-omni-turbo-realtime`<br>• ❌ 不支持 `multimodal-dialog`、`Fun-ASR`、`CosyVoice` 等非 Omni 模型 |
| **API 端点** | • WebSocket：<br> `wss://{workspaceId}.{region}.maas.aliyuncs.com/api-ws/v1/realtime`<br>• WebRTC：<br> `POST https://{workspaceId}.{region}.maas.aliyuncs.com/api-webrtc/v1/offer`<br>• AOQ：<br> 需通过 `aoqTokenForClient` + SDK 引擎连接 | • 统一 WebSocket 端点：<br> `wss://{workspaceId}.{region}.maas.aliyuncs.com/api-ws/v1/realtime`<br>（与 Realtime API WebSocket 端点相同，但路由与鉴权逻辑隔离） |
| **计费方式** | • 按 **实际调用模型 + 使用资源维度** 计费：<br> – 音频处理时长（秒）<br> – 文本 token 数（输入+输出）<br> – 图像 token 数（若启用）<br>• 不同协议无额外协议溢价 | • 按 **Omni 模型专属计费单元** 计费：<br> – 以「语音会话分钟」（含 ASR+LLM+TTS 全链路）为主计量单位<br> – 支持按「音频输入秒数」或「响应音频秒数」细分计费（可配置）<br>• 计费粒度更粗、模型绑定更强，无跨模型混用计费 |
| **典型场景** | • 跨端统一实时服务（Web/App/嵌入式）<br>• 弱网环境下的音视频通话（AOQ）<br>• 浏览器原生音视频互动（WebRTC）<br>• 快速验证与服务端集成（WebSocket）<br>• 多模态混合交互（图文声协同） | • 语音助手、智能客服、车载对话等**强语音交互场景**<br>• 需要语义级 VAD（`semantic_vad`）、主动引导（`idle_timeout_ms`）、工具链闭环的对话系统<br>• 对音色定制（声音复刻）、联网搜索、平滑口语输出有明确需求<br>• 客户端可稳定维持 WebSocket 长连接 |

---

## 适用场景建议

### ✅ 选择 **Realtime API** 当：
- 你的应用需**同时支持浏览器、iOS、Android、IoT 设备等多种终端**，且对弱网稳定性、建连速度、回声消除等有差异化要求；
- 你需要**灵活组合不同能力模块**，例如：用 `Fun-ASR` 做高精度语音识别 + `qwen3.5-omni-plus-realtime` 做推理 + `CosyVoice` 做定制音色合成；
- 你正在构建**多模态交互产品**（如带白板协作的会议系统、AR 导览助手），需同步处理语音、文本、图像甚至视频帧；
- 你已有 WebRTC 基础设施（如自研 SFU），希望复用现有媒体栈对接百炼 AI 能力；
- 你追求**协议自主可控性**，需要精细管理 SDP 交换、媒体轨道、DataChannel 或 AOQ 流控策略。

### ✅ 选择 **Omni Realtime API** 当：
- 你的核心场景是**语音优先的实时对话**（如电话客服、语音导航、儿童陪伴机器人），且客户端能稳定维持 WebSocket 连接；
- 你需要开箱即用的**语义级语音活动检测（`semantic_vad`）**，而非传统能量阈值型 VAD；
- 你依赖**主动会话引导能力**（如用户静默 8 秒后自动追问），需 `idle_timeout_ms` 参数；
- 你要求**工具调用与语音响应无缝衔接**（如查询天气 → 播报结果 → 自动播放背景音乐），并接受服务端自动触发后续响应（VAD 模式）；
- 你已选定 `qwen3.5-omni-*` 系列模型，并希望获得**标准化 SDK、统一参数体系、精细化生成控制（temperature/top_p 等）及声音复刻集成支持**；
- 你倾向**降低客户端复杂度**：无需管理 SDP、媒体轨道、AOQ 凭证，仅需处理 WebSocket 事件流。

> ⚠️ 注意：Omni Realtime API **不是 Realtime API 的子集，而是其能力子集上的深度封装**。它不提供 Realtime API 的协议扩展性与模型泛化能力，但显著提升了语音对话场景下的开发效率与体验一致性。

---

## 技术选型参考（面向开发者）

| 决策因素 | 推荐方案 | 说明 |
|----------|----------|------|
| **终端兼容性要求高（尤其需支持 Safari / iOS WebRTC 或弱网移动端）** | Realtime API（选 WebRTC 或 AOQ） | Omni Realtime API 仅 WebSocket，无法满足原生 WebRTC 或极致弱网需求 |
| **需接入非 Omni 模型（如独立 ASR/TTS、多模态套件、Livetranslate）** | Realtime API | Omni Realtime API 严格限定模型范围，不可替换底层 ASR 或 TTS |
| **项目周期紧，需快速上线标准语音助手** | Omni Realtime API | 提供完整 Java/Python/JS SDK、预置 VAD 策略、标准化事件流，接入代码量减少约 40% |
| **需深度定制语音交互流程（如分段提交音频、混合文本指令、动态切换音色）** | Realtime API（WebSocket） | Omni Realtime API 的 `input_audio_buffer.commit` 仅支持 Manual 模式，且不支持文本混输 |
| **安全合规要求极高（如金融级 [Token](../concepts/token.md) 隔离、客户端零密钥暴露）** | Realtime API（AOQ 或 WebRTC 代理模式） | AOQ 使用 `aoqTokenForClient`，WebRTC 强制服务端代理 SDP，比 Omni 的 WebSocket 直连更易满足审计要求 |
| **需长期演进支持多模态扩展（未来加入图像理解、3D 动作生成等）** | Realtime API | 架构设计面向多模态扩展，Omni Realtime API 明确锁定语音+文本双模态 |

**最终建议**：  
- 若业务本质是「语音对话」，且无特殊协议或跨模态需求 → **首选 Omni Realtime API**，享受开箱即用的对话体验与维护优势；  
- 若业务本质是「实时交互平台」，需承载多种终端、多种模型、多种协议 → **必须选用 Realtime API**，并根据终端特性选择对应协议；  
- **二者可共存**：同一 Workspace 下可同时调用 Omni Realtime API（用于主语音通道）与 Realtime API WebSocket（用于后台 ASR 异步转写或图文辅助），共享统一鉴权与配额体系。

## 被对比主题页

- [realtime api user guide](../api/realtime-api-user-guide.md)
- [omni realtime api](../api/omni-realtime-api.md)



# 实时 API 方案对比：Omni Realtime API 与 Realtime API

为帮助开发者在构建语音助手、智能客服、实时音视频交互等低延迟 AI 应用时做出精准技术选型，本文系统对比百炼平台两大核心实时能力接口：**Omni Realtime API** 与 **Realtime API**。二者虽同属“实时”范畴，但在架构定位、协议支持、能力边界、工程集成方式及适用场景上存在本质差异。本对比基于最新文档（截至 2024 年 Q3）整理，聚焦可落地的技术事实，规避模糊表述与过时信息，旨在提供清晰、可执行的选型依据。

## 关键维度对比

| 维度 | Omni Realtime API | Realtime API |
|------|-------------------|--------------|
| **核心定位** | 专为**多模态实时会话**深度优化的 WebSocket 原生接口，强调端到端语义级控制与事件驱动流式交互 | 百炼平台统一的**实时能力接入层**，提供 AOQ / WebRTC / WebSocket 三协议抽象，覆盖 ASR/TTS/翻译/对话等全栈能力 |
| **输入格式** | - 音频：16 kHz PCM（单通道）<br>- 图像：JPG/JPEG（≤1080p，Base64 编码 ≤256 KB）<br>- 文本：通过 `conversation.item.create` 事件注入 | - 音频：16 kHz PCM（ASR/Omni 等模型要求）<br>- 视频：原始帧（I420/NV12 等）或 JPEG 编码帧<br>- **不支持图像理解**（无视觉输入能力） |
| **输出格式** | - 文本 + 24 kHz PCM 音频（可选模态组合 `["text"]` 或 `["text","audio"]`）<br>- 支持增量文本（`stash`）、情感识别（`emotion` 字段）、音频 delta 流（`response.audio.delta`） | - 文本、24 kHz PCM 音频、翻译结果、ASR 识别文本等，依模型而定<br>- **无统一多模态输出结构**；各能力模块输出格式独立（如 ASR 输出 JSON，TTS 输出二进制音频流） |
| **支持模型** | 仅限 `qwen*-omni-*realtime` 系列：<br>- `qwen3.5-omni-realtime`（含 semantic VAD、联网搜索、完整工具调用）<br>- `qwen3.5-omni-plus/flash-realtime`（含 idle_timeout_ms、声音复刻）<br>- `qwen3-omni-flash-realtime` / `qwen-omni-turbo-realtime`（轻量级，仅 server_vad） | 覆盖更广模型矩阵：<br>- 全模态：`qwen3.5-omni-plus/flash-realtime`<br>- 实时翻译：`qwen3.5-livetranslate-flash-realtime`<br>- ASR：`Qwen-Audio-3.0-ASR-Flash-Streaming`、`Fun-ASR-Realtime`<br>- TTS：`CosyVoice`、`qwen-audio-3.0-tts-flash/plus`<br>- 对话：`qwen-audio-3.0-realtime-plus/flash` |
| **API 端点与协议** | 单一 WebSocket 端点：<br>`wss://{WorkspaceId}.{region}.maas.aliyuncs.com/api-ws/v1/realtime`<br>**仅 WebSocket**，无 AOQ/WebRTC 原生支持 | 三协议统一入口：<br>- AOQ：`/api/v1/aoq/realtime`（需服务端分配 token）<br>- WebRTC：`/api/v1/webrtc/realtime`（SDP 交换）<br>- WebSocket：`/api-ws/v1/realtime`（兼容 Omni 端点，但能力受限） |
| **计费方式** | 按**实际处理的音频时长（秒）+ 文本 token 数**计费（含 ASR/TTS/LLM 推理），具体见 [计费说明](../../raw/pricing/realtime-api-pricing.md) | 按**所用模型能力分项计费**：<br>- ASR/TTS 按音频时长（秒）<br>- 翻译按字符数<br>- 对话/多模态按 token 数<br>- AOQ/WebRTC 协议本身不额外计费 |
| **VAD 与交互模式** | 内置双 VAD：`server_vad`（全系列）与 `semantic_vad`（仅 `qwen3.5-omni-realtime`）；支持自动提交（VAD 模式）与手动提交（Manual 模式） | VAD 行为由底层模型决定，**不暴露统一 VAD 控制参数**；交互逻辑依赖协议层（如 AOQ 的媒体流开关、WebRTC 的 DataChannel 消息） |
| **高级功能** | ✅ 声音复刻（需预注册音色）<br>✅ 工具调用（Function Calling）<br>✅ 联网搜索（`enable_search`，仅 `qwen3.5-omni-realtime`）<br>✅ 多模态上下文（图文混合输入） | ⚠️ 工具调用：仅部分 Omni 模型支持（需通过 `tools` 参数传入）<br>❌ 联网搜索：未开放<br>❌ 声音复刻：未开放<br>❌ 图像理解：不支持 |
| **客户端 SDK 支持** | 提供 Python/Java/JS 官方 SDK，封装 WebSocket 连接、事件序列化、重连逻辑 | 提供 AOQ SDK（Android/iOS/HarmonyOS/Linux）、WebSocket SDK；**WebRTC 无官方 SDK，需自行实现标准协议栈** |
| **安全性设计** | API Key 直接用于 WebSocket 鉴权（Header `Authorization: Bearer <API_KEY>`），**需严格管控客户端密钥暴露风险** | AOQ 协议强制服务端代理鉴权：客户端仅使用临时 `aoqTokenForClient`；WebSocket/WebRTC 可直接携带 API Key（但强烈建议服务端中转） |

## 各方案的适用场景建议

### ✅ 选择 Omni Realtime API 当：
- 构建**强交互性语音助手或智能客服**，需同时处理语音输入、文本生成、语音合成，并要求毫秒级响应与自然对话节奏；
- 应用需**多模态融合能力**（如用户上传图片提问 + 语音追问）；
- 业务对**声音个性化有明确需求**（如品牌音色复刻、角色化播报）；
- 团队具备 WebSocket 开发经验，且终端环境（Web/移动端 WebView/桌面应用）稳定支持 WebSocket；
- 需要细粒度控制会话状态（如动态更新 `instructions`、切换 `voice`、启用 `semantic_vad`）。

### ✅ 选择 Realtime API 当：
- 需要**跨协议统一接入**：同一套后端服务需同时支持 iOS App（AOQ）、浏览器（WebRTC）、服务端调度（WebSocket）；
- 场景聚焦**单一能力模块**：如纯实时语音识别（ASR）、实时语音合成（TTS）、或实时多语言翻译，无需图文混合；
- 项目已基于 WebRTC 架构建设（如在线教育、远程医疗），需复用现有信令与媒体管道；
- 对**客户端密钥安全有强合规要求**（如金融、政务类 App），必须采用 AOQ 的服务端鉴权模式；
- 需要接入**非 Omni 系列模型**（如专用 ASR/TTS 模型、轻量级对话模型 `qwen-audio-3.0-realtime-flash`）。

### ⚠️ 不推荐混用或强行替代的情况：
- 在 WebRTC 场景中尝试调用 Omni Realtime API —— WebRTC 协议不支持 Omni 的事件模型与多模态 payload 结构；
- 用 Omni Realtime API 替代 Realtime API 的 ASR/TTS 专项能力 —— Omni 的 ASR 是其内置组件，不可单独剥离计费或配置；
- 在 `qwen-omni-turbo-realtime` 上设置 `temperature`/`top_p`/`max_tokens` —— 文档明确标注该系列参数不可修改，设置将被忽略或触发错误。

## 技术选型参考指南（面向开发者）

1. **先定协议，再选 API**  
   若项目已确定使用 WebRTC（如浏览器音视频会议），则 **Realtime API 是唯一可行路径**；若仅需 WebSocket 且追求最简集成，Omni Realtime API 提供更丰富的语义控制。

2. **能力需求 > 协议偏好**  
   需要图像理解？→ 必选 Omni Realtime API。  
   只需高精度 ASR？→ Realtime API 的 `Fun-ASR-Realtime` 系列更专业，且支持 AOQ 低延迟传输。

3. **关注参数兼容性**  
   `qwen-omni-turbo-realtime` 等轻量模型**不支持采样参数与 `smooth_output`**，若业务需动态调节生成风格，请选用 `qwen3.5-omni-realtime` 或 `qwen3.5-omni-plus-realtime`。

4. **安全红线不可逾越**  
   移动端 App 中，**禁止硬编码 API Key**。优先采用 Realtime API 的 AOQ 方案（服务端签发临时 [Token](../concepts/token.md)）；若必须用 Omni Realtime API，请通过业务网关代理请求，避免 Key 泄露。

5. **性能与成本平衡**  
   `qwen-omni-turbo-realtime` 延迟最低、成本最优，适合高频短交互（如语音指令）；`qwen3.5-omni-realtime` 功能最全但资源消耗更高，适合复杂任务（如带搜索的客服问答）。

> **最后建议**：新项目推荐从 Realtime API 的 WebSocket 接入开始快速验证，再根据实际能力缺口（是否需图像/工具/搜索）决定是否升级至 Omni Realtime API；存量 WebSocket 应用若已满足需求，无需主动迁移。

## 被对比主题页

- [omni realtime api](../api/omni-realtime-api.md)
- [realtime api user guide](../api/realtime-api-user-guide.md)



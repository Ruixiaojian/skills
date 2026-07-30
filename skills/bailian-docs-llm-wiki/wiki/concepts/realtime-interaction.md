# 实时交互

实时交互是百炼平台中面向低延迟、流式、双向持续通信场景的核心能力，指客户端与服务端在单一会话生命周期内，以毫秒级响应为目标，支持语音、文本、图像等多模态输入的即时处理，并同步流式返回文本、音频等输出结果的端到端交互范式。它强调“边说边想、边听边答”的自然对话节奏，而非传统请求-响应式的离散调用。

## 在百炼平台的不同场景中，这个概念如何使用

实时交互能力主要通过两类技术路径落地，适用不同终端形态与业务需求：

- **Realtime API（协议级实时）**  
  面向对端到端延迟、音视频质量、弱网鲁棒性有严苛要求的场景（如智能硬件、车载系统、会议终端）。提供 AOQ（移动端原生）、WebRTC（浏览器/WebApp）、WebSocket（服务端/原型验证）三种接入协议：  
  - AOQ：集成 SDK 后可启用硬件加速采集、内置 AEC/降噪、语义级 VAD，适合 Android/iOS/HarmonyOS 原生应用；  
  - WebRTC：复用浏览器原生能力，免 SDK，适用于 Web 端实时音视频对话，需白名单开通；  
  - WebSocket：轻量通用，支持 DashScope SDK 快速接入，但音视频前处理（如回声消除）需客户端自行实现。

- **Omni Realtime API（模型级实时）**  
  是 Realtime API 的一个具体实现子集，专为 `qwen3.5-omni-*` 系列全模态实时模型设计，基于 WebSocket 协议，采用事件驱动模型（如 `input_audio_buffer.append` → `response.audio.delta`）。它封装了 ASR/TTS/LLM 多阶段协同，支持语音+图像+文本混合输入、文本+音频[流式输出](streaming-output.md)，并内置 `semantic_vad`、工具调用、联网搜索等高级能力，适用于虚拟助手、智能客服、音视频会议插件等高保真交互场景。

> 注意：`application call`（应用调用）和 `LLM Application`（智能体/工作流）虽支持 `stream=true` 流式响应，但其本质是**同步请求的流式化输出**，不具备持续媒体流传输、实时语音活动检测（VAD）、端侧音视频处理等实时交互核心特征，不属于本概念范畴。它们属于“准实时”或“流式响应”，不参与实时会话状态管理。

## 关键参数和配置

所有实时交互会话均通过 `session.update` 事件统一配置，关键参数如下（按功能分组）：

| 类别 | 参数 | 类型 | 说明 | 典型值/约束 |
|------|------|------|------|-------------|
| **基础控制** | `modalities` | `array` | 指定输出模态 | `["text"]` 或 `["text","audio"]`（必填） |
| | `voice` | `string` | 输出音色名称 | `"Tina"`（Qwen3.5）、`"Cherry"`（Flash）、`"Chelsie"`（Turbo），Turbo 系列不可修改 |
| **音频格式** | `input_audio_format` / `output_audio_format` | `string` | 固定为 `"pcm"` | 输入采样率必须为 `16kHz`，输出为 `24kHz` |
| **语音检测** | `turn_detection.type` | `string` | VAD 类型 | `"server_vad"`（声学，通用）或 `"semantic_vad"`（语义，仅 `qwen3.5-omni-realtime` 支持） |
| | `turn_detection.silence_duration_ms` | `integer` | 静音判定阈值 | `[200, 6000]` ms，默认 `800` |
| | `turn_detection.idle_timeout_ms` | `integer` | 静默超时主动引导 | `[5000, 30000]` ms，仅 Qwen3.5-Plus/Flash + `server_vad` 生效 |
| **高级能力** | `enable_search` | `boolean` | 启用联网搜索 | 仅 `qwen3.5-omni-realtime` 支持，且与 `tools` 不兼容 |
| | `tools` | `array` | 工具定义列表 | 仅 `qwen3.5-omni-realtime` 支持，需配合 `conversation.item.create` 回传结果 |
| | `instructions` | `string` | 系统角色指令 | 影响模型初始行为，建议简洁明确 |

> ⚠️ 鉴权安全提示：`Authorization: Bearer <API_KEY>` **必须由服务端持有并用于网关请求**，严禁在客户端硬编码。AOQ 协议额外要求服务端申请 `aoqTokenForClient`，客户端仅用该临时 [Token](token.md) 连接，杜绝密钥暴露风险。

## 面向开发者，简洁实用

- **选协议**：移动端 → 选 AOQ；浏览器 → 选 WebRTC（联系商务开通）；服务端/快速验证 → 选 WebSocket。
- **建会话**：先发 `session.update` 配置 `modalities` 和 `voice`，再发送媒体数据（AOQ/WebRTC 自动推流，WebSocket 需手动发 `input_audio_buffer.append`）。
- **等就绪**：AOQ 必须监听 `session.updated` 事件后，再调用 `enableSendMediaStream(.audio, true)`；WebSocket 无此依赖。
- **控VAD**：追求自然打断 → 用 `semantic_vad`（Qwen3.5）；追求低延迟稳定 → 用 `server_vad` + 调整 `silence_duration_ms`。
- **避坑**：Turbo 系列模型不支持调节 `temperature`/`top_p` 等生成参数；声音复刻音色必须与 Omni 模型版本严格一致（如 `qwen3.5-omni-plus-realtime` 创建的音色，只能用于同名模型）。
- **调试建议**：本地开发优先用 WebSocket + DashScope SDK；上线前务必在目标终端（iOS/Android/Chrome）实测 AOQ 或 WebRTC 的弱网表现。

## 关联主题页

- [realtime api user guide](../api/realtime-api-user-guide.md)
- [omni realtime api](../api/omni-realtime-api.md)
- [application call](../api/application-call.md)
- [llm application](../guides/llm-application.md)



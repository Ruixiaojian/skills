# 实时 API 方案对比：Omni Realtime API 与 Realtime API

本对比旨在帮助开发者清晰理解百炼平台两大实时交互接口——**Omni Realtime API** 与 **Realtime API** 的定位差异、能力边界与适用条件，避免因选型偏差导致集成成本上升、功能缺失或性能不达预期。二者虽均面向低延迟多模态实时场景，但在协议设计、模型覆盖、部署灵活性及工程约束上存在系统性差异。本文基于最新 v3.5 系列模型能力与生产环境实践整理，适用于语音助手、智能客服、实时翻译、音视频互动等核心场景的技术选型决策。

## 关键维度对比

| 维度 | Omni Realtime API | Realtime API |
|------|-------------------|--------------|
| **协议基础** | 仅支持 WebSocket（`wss://.../api-ws/v1/realtime`） | 支持 **WebSocket / WebRTC / AOQ** 三协议，可按终端类型动态选择 |
| **输入格式** | - 音频：PCM（16 kHz，Base64）<br>- 图像：JPG/JPEG（≤1080p，≤256 KB Base64）<br>- 视频帧：通过 `append_video` 事件流式传入<br>- **图像必须在首次音频输入后发送，且与音频缓冲区协同提交** | - WebSocket：同 Omni（文本/音频/图像分通道）<br>- WebRTC/AOQ：原生支持音视频+文本**混合传输**（如带时间戳的 AV sync stream）<br>- 所有协议均支持 `input_audio_buffer.append` 等标准事件 |
| **输出格式** | - 文本 + PCM 音频（24 kHz）<br>- 可配置 `modalities: ["text"]` 或 `["text","audio"]`，**不支持纯音频输出**<br>- 增量事件：`response.text.delta`、`response.audio.delta`、`conversation.item.input_audio_transcription.delta`（内置 ASR） | - 同 Omni 的文本/音频增量输出<br>- WebRTC/AOQ 额外支持**端到端音视频流直出**（如 H.264 视频帧 + Opus 音频包）<br>- WebSocket 模式下不支持原生视频流输出 |
| **支持模型与能力** | - 专属模型系列：<br> ✓ `qwen3.5-omni-realtime`（语义 VAD、联网搜索、工具调用）<br> ✓ `qwen3.5-omni-plus/flash-realtime`（`idle_timeout_ms`、`smooth_output`）<br> ✓ `qwen3-omni-flash-realtime`（默认音色 `Cherry`）<br> ✗ 不支持 `livetranslate`、`multimodal-dialog`、`Fun-ASR`、`CosyVoice` 等非 Omni 系列模型 | - **统一模型网关**，覆盖更广：<br> ✓ 全模态：`qwen3.5-omni-plus/flash-realtime`<br> ✓ 实时翻译：`qwen3.5-livetranslate-flash-realtime`<br> ✓ 多模态套件：`multimodal-dialog`（WebRTC/WebSocket）<br> ✓ 专用 ASR/TTS：`Fun-ASR`、`CosyVoice`（WebSocket）<br> ✓ 语音对话：`qwen-audio-3.0-realtime-plus/flash`（WebSocket） |
| **API 端点** | 固定 WebSocket 地址：<br>`wss://{WorkspaceId}.{region}.maas.aliyuncs.com/api-ws/v1/realtime`<br>（推荐业务空间专属域名，已弃用 `dashscope.aliyuncs.com`） | 协议差异化端点：<br>- WebSocket：`wss://dashscope.aliyuncs.com/...`（或工作空间域名）<br>- WebRTC：`{workspace_id}.{region}.maas.aliyuncs.com`（SDP 交换需后端代理）<br>- AOQ：通过 `aoqTokenForClient` 动态协商，无固定 URL |
| **计费方式** | 按 **实际调用时长（秒） + 输出 token 数量** 计费<br>- 音频输入/输出按采样点折算为等效时长<br>- 工具调用、联网搜索不额外计费，但计入会话总耗时 | 按 **协议 + 模型 + 资源消耗** 分层计费：<br>- WebSocket：同 Omni（时长 + token）<br>- WebRTC/AOQ：**增加媒体处理资源费**（如 AEC、弱网对抗、编解码开销）<br>- `multimodal-dialog`、`livetranslate` 等应用类模型有独立定价单元 |
| **典型场景** | - 低延迟语音助手（端侧 VAD 触发、快速响应）<br>- 智能客服坐席辅助（实时转录+语音回复）<br>- 需深度定制会话状态机的 B2B 交互系统（事件驱动精细控制） | - 浏览器端网页客服（WebRTC，免插件、强弱网适应）<br>- 原生 App 音视频通话（AOQ，毫秒级延迟、离线降级）<br>- 多语言实时会议翻译（`livetranslate` + WebRTC）<br>- 快速验证原型（WebSocket，零客户端依赖） |
| **VAD 与交互控制** | - 强事件驱动：`server_vad`（声学）或 `semantic_vad`（语义，仅 `qwen3.5-omni-realtime`）<br>- Manual 模式需显式 `commit` + `response.create`<br>- 支持 `idle_timeout_ms`（主动引导） | - VAD 类型一致（`server_vad`/`semantic_vad`），但 WebRTC/AOQ 内置硬件级 AEC+降噪，VAD 更鲁棒<br>- WebRTC/AOQ 支持**端侧触发响应**（如按键说话、手势唤醒），不依赖服务端 VAD 判定 |
| **安全与部署约束** | - 鉴权：`Authorization: Bearer <API_KEY>`（建连时携带）<br>- **禁止在前端暴露 API Key**，必须由业务服务端代理<br>- 无 [Token](../concepts/token.md) 机制，依赖长期密钥管理 | - WebSocket：同 Omni<br>- WebRTC：SDP 交换必须经业务后端代理（防 CORS + 密钥泄露）<br>- AOQ：**强制 [Token](../concepts/token.md) 鉴权**（`aoqTokenForClient`），时效短、可撤销、支持细粒度权限 |

## 各方案适用场景建议

### ✅ 推荐选用 **Omni Realtime API** 当：
- 业务聚焦于 **纯语音/语音+图像** 的轻量级实时交互（如车载助手、IoT 设备语音控制）；
- 需要 **语义级语音活动检测（`semantic_vad`）** 或 **联网搜索能力**（仅 `qwen3.5-omni-realtime` 提供）；
- 已有成熟 WebSocket 客户端栈，追求 **最小接入成本** 与 **确定性低延迟**（端到端 P99 < 400ms）；
- 对音色复刻、工具链深度集成（如自定义工具回调流程）有强需求；
- 运行环境受限（如嵌入式设备、无 WebRTC 支持的旧浏览器）。

### ✅ 推荐选用 **Realtime API** 当：
- 面向 **多终端统一体验**：需同时支持 Web（WebRTC）、iOS/Android（AOQ）、服务端（WebSocket）；
- 场景涉及 **真实音视频通话**（如远程医疗、在线教育），要求端到端 AEC、抗丢包、弱网自适应；
- 需要 **非 Omni 系列模型能力**：如专业语音翻译（`livetranslate`）、多模态对话套件（`multimodal-dialog`）、高保真 TTS（`CosyVoice`）；
- 安全合规要求严格：需 **短期 [Token](../concepts/token.md) 鉴权（AOQ）** 或 **后端代理 SDP（WebRTC）**，杜绝密钥暴露风险；
- 开发团队具备跨协议调试能力，愿为极致体验承担稍高集成复杂度。

> ⚠️ 注意：若项目需同时使用 `qwen3.5-omni-realtime`（语义 VAD）和 `multimodal-dialog`（多轮视觉引导），**必须选用 Realtime API + WebRTC 协议**——Omni Realtime API 不支持该套件。

## 技术选型参考（致开发者）

| 你的需求 | 推荐方案 | 关键理由 |
|----------|-----------|-----------|
| “我要做一个微信小程序里的语音客服，用户说一句话，立刻听到回答” | **Omni Realtime API**（WebSocket） | 小程序 WebView 支持 WebSocket；Omni 的 `semantic_vad` 可精准截断口语停顿，避免“等说完才响应”；无需处理 WebRTC 信令复杂度。 |
| “我们开发 iOS/Android App，要做一个带美颜和实时字幕的视频面试系统” | **Realtime API + AOQ** | AOQ 提供原生 SDK、毫秒级音画同步、内置美颜/降噪/字幕渲染管线；`multimodal-dialog` 模型可理解面试者微表情与肢体动作。 |
| “客户要求支持 Chrome/Firefox/Safari 全浏览器实时翻译，且能应对 4G 弱网” | **Realtime API + WebRTC** | WebRTC 是浏览器唯一原生低延迟音视频协议；内置 ICE-lite 和拥塞控制，弱网下自动降码率保流畅；`livetranslate` 模型专为跨语言对话优化。 |
| “我们是 SaaS 厂商，需为不同客户提供隔离的语音助手，且要审计每次调用” | **Realtime API（WebSocket） + 业务服务端代理** | 通过服务端统一注入 `workspace_id` 和鉴权头，天然实现租户隔离；所有请求经代理可记录完整 trace 日志，满足 SOC2 审计要求。 |
| “想快速验证 Qwen-Omni 的语音生成效果，本地 Node.js 脚本跑通就行” | **Omni Realtime API**（WebSocket） | 无需安装 SDK、无需处理信令，几行代码即可建立连接、发送音频、接收流式响应，原型验证效率最高。 |

> 💡 **终极建议**：  
> - **从协议出发选型**：先明确终端类型（Web/iOS/Android/Server）与网络环境（强网/弱网/局域网），再决定用 WebRTC/AOQ/WebSocket；  
> - **再匹配模型能力**：若需 `semantic_vad` 或联网搜索，锁定 `qwen3.5-omni-realtime` → 选 Omni；若需 `livetranslate` 或 `multimodal-dialog` → 选 Realtime；  
> - **最后评估工程成本**：团队是否熟悉 WebRTC SDP？是否有能力维护 AOQ Token 服务？这些将直接影响上线周期。  

如需进一步比对具体模型参数、错误码处理或迁移路径，请查阅对应 SDK 文档与 [实时 API 最佳实践](https://help.aliyun.com/zh/model-studio/realtime-api-best-practices)。

## 被对比主题页

- [omni realtime api](../api/omni-realtime-api.md)
- [realtime api user guide](../api/realtime-api-user-guide.md)



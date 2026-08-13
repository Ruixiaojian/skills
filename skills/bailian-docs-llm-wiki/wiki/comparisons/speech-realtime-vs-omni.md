# 实时语音 API 对比：Realtime API 与 Omni Realtime API

本文档面向百炼平台开发者，旨在清晰对比 **Realtime API**（通用实时语音交互接口）与 **Omni Realtime API**（专注[多模态](../concepts/multimodal.md)原生实时对话的增强型接口），帮助技术团队基于业务目标、终端环境、功能需求及工程约束，做出高效、可持续的 API 选型决策。二者同属百炼实时语音能力体系，但定位分层明确：Realtime API 提供协议灵活、模型广谱、接入路径多元的“基础实时能力底座”；Omni Realtime API 则聚焦于 WebSocket 协议下深度优化的“全栈[多模态](../concepts/multimodal.md)实时对话体验”，在语义理解、工具协同、音画融合等高阶场景具备原生支持优势。

---

## 关键维度对比

| 维度 | Realtime API | Omni Realtime API |
|------|--------------|-------------------|
| **核心定位** | 通用型实时语音交互底座，支持 ASR/TTS/翻译/对话/全模态等多类任务，强调协议适配性与模型覆盖广度 | 专用型[多模态](../concepts/multimodal.md)实时对话接口，以“语音+文本+图像+工具”一体化流式交互为核心，强调语义连贯性与端到端体验一致性 |
| **支持协议** | ✅ AOQ（推荐移动端/弱网）、✅ WebRTC（浏览器原生）、✅ WebSocket（服务端/原型验证） | ✅ WebSocket（**唯一支持协议**）<br>❌ 不支持 AOQ / WebRTC |
| **输入格式** | - 音频：PCM（仅 `pcm`）<br>- 文本：`instructions` 或 ASR 转录结果<br>- 图像：**不支持** | - 音频：PCM 或 WAV（`audio.input.format = {type: "pcm"\|"wav", sample_rate: int}`），支持 8k/16k/24k/48k Hz<br>- 文本：`instructions` 或 ASR 转录结果<br>- 图像：JPG/JPEG（Base64 编码 ≤256KB，分辨率 ≤1080p）✅ |
| **输出格式** | - 文本：流式 `text.delta`<br>- 音频：流式 `audio.delta`（仅 `pcm`）<br>- 结构化数据：有限（如翻译结果 JSON） | - 文本：流式 `response.text.delta`<br>- 音频：流式 `response.audio.delta`（PCM 或 WAV，`audio.output.format` 可配）✅<br>- 工具调用：`response.function_call_arguments.*` 事件 ✅<br>- 联网搜索结果：`response.search_results.*`（仅 Qwen3.5 系列）✅ |
| **支持模型** | - 全模态：`qwen3.5-omni-plus-realtime`, `qwen3.5-omni-flash-realtime`<br>- 翻译：`qwen3.5-livetranslate-flash-realtime`<br>- ASR：`Qwen-Audio-3.0-ASR-Flash-Streaming`, `Fun-ASR-Realtime`（AOQ/WebSocket only）<br>- TTS：`CosyVoice`, `qwen-audio-3.0-tts-*`（AOQ/WebSocket only）<br>- 对话：`qwen-audio-3.0-realtime-plus/flash` | - 仅限 Omni 系列模型：<br> `qwen3.5-omni-plus-realtime`（全能）、<br> `qwen3.5-omni-flash-realtime`（低延迟）、<br> `qwen3.5-omni-turbo-realtime`（极致轻量）<br>- ❌ 不支持独立 ASR/TTS/翻译等单点模型 |
| **API 端点** | - AOQ：`POST /api/v1/aoq/allocate`（获取连接凭证） + QUIC Relay 连接<br>- WebRTC：`POST https://{endpoint}/api/v1/webrtc/realtime?model=...`<br>- WebSocket：`wss://{endpoint}/api-ws/v1/realtime`（统一入口） | - WebSocket 唯一端点：<br> `wss://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api-ws/v1/realtime`<br> （需替换 `{WorkspaceId}`，推荐使用专属域名） |
| **计费方式** | 按 **实际调用模型 + 输入/输出 token 数 + 音频时长（秒）** 分项计费<br>（例：ASR 按音频秒数计费，TTS 按合成秒数计费，LLM 推理按 input/output tokens 计费） | 按 **会话生命周期内消耗的总 token 数 + 音频处理时长（秒）** 统一计费<br>（ASR/TTS/LLM/Tool Call 全链路合并计量，无模型拆分计费项） |
| **VAD 支持** | - `server_vad`（声学）<br>- `semantic_vad`（语义，仅 Omni 系列模型支持）<br>⚠️ WebRTC 协议下不支持 ASR/TTS，故 VAD 仅用于对话类模型 | - `server_vad`（全系列）<br>- `semantic_vad`（仅 `qwen3.5-omni-plus/flash` 支持）✅<br>- 支持 `idle_timeout_ms`（静默超时控制，Plus/Flash + server_vad 下生效）✅ |
| **高级能力** | - 多协议传输控制（如 AOQ 自定义采集、WebRTC DataChannel 管理）<br>- 原生 TTS 音色切换（`voice` 参数）<br>- 基础指令控制（`instructions`） | - ✅ 原生工具调用（Function Calling）<br>- ✅ 联网搜索（`enable_search`，仅 Qwen3.5 系列）<br>- ✅ 声音复刻集成（严格匹配驱动模型）<br>- ✅ 多参数精细调控（temperature/top_p/max_tokens 等，Turbo 系列受限） |
| **典型场景** | - 移动端语音助手（AOQ 弱网优化）<br>- 浏览器实时字幕（WebRTC）<br>- 服务端批量语音转写（WebSocket + ASR）<br>- 实时会议双语翻译（WebSocket + Livetranslate） | - 智能客服语音坐席（语音+图像+知识库工具联动）<br>- 实时会议纪要生成（语音+PPT截图理解+结构化摘要）<br>- 多轮语音购物助手（语音提问 → 图片识别商品 → 工具查库存 → 合成播报）<br>- 无障碍交互应用（语音+图像描述+自定义音色） |

---

## 适用场景建议

### ✅ 选择 Realtime API 当：
- **终端类型复杂**：需同时支持 iOS/Android App（AOQ）、Web 浏览器（WebRTC）、IoT 设备（WebSocket）；
- **功能需求单一或分层**：仅需 ASR（语音转文字）、仅需 TTS（文字转语音）、仅需实时翻译，无需多模态耦合；
- **对网络鲁棒性要求极高**：在弱网、高丢包环境下需 QUIC 重传与 AOQ 自适应媒体流控制；
- **已有 WebRTC 基础设施**：希望复用现有信令/SDP 管理逻辑，快速接入语音对话能力；
- **成本敏感且任务可解耦**：例如将 ASR、NLU、TTS 拆分为独立服务调用，分别优化各环节计费。

### ✅ 选择 Omni Realtime API 当：
- **核心诉求是“多模态实时对话”**：语音输入 + 图像理解 + 文本推理 + 工具执行 + 语音播报，需原子化、低延迟、强一致的端到端流式体验；
- **技术栈统一为 WebSocket**：服务端/客户端均基于 WebSocket 构建，无 WebRTC 或原生 SDK 集成负担；
- **需深度语义交互能力**：依赖 `semantic_vad` 实现自然打断、工具调用触发业务系统、联网搜索补充实时信息；
- **追求开发效率与体验一致性**：避免手动拼接 ASR→LLM→TTS 流程，由一个会话生命周期统管全部模态流转；
- **产品形态面向专业场景**：如金融远程面签（语音+身份证图像核验+OCR工具）、医疗问诊（语音症状描述+检查报告图片理解+药品查询工具）。

---

## 技术选型参考（致开发者）

| 选型考量 | Realtime API | Omni Realtime API | 建议动作 |
|----------|--------------|-------------------|----------|
| **协议兼容性要求** | 支持 AOQ/WebRTC/WebSocket 三协议 | 仅支持 WebSocket | 若需 WebRTC 或 AOQ，**必须选 Realtime API**；若已锁定 WebSocket，两者均可，优先 Omni |
| **是否需要图像理解** | ❌ 不支持 | ✅ 原生支持（JPG/JPEG ≤256KB） | 有图像输入需求 → **Omni Realtime API** |
| **是否需调用外部系统（数据库/API）** | ❌ 需自行实现回调与状态同步 | ✅ 原生 Function Calling 事件流 | 需工具集成 → **Omni Realtime API** |
| **是否需联网搜索能力** | ❌ 不支持 | ✅ `enable_search`（Qwen3.5 系列） | 需实时网络信息 → **Omni Realtime API** |
| **是否需极致弱网稳定性** | ✅ AOQ 协议专为弱网设计 | ❌ WebSocket 在弱网下易断连 | 移动端弱网为主 → **Realtime API（AOQ）** |
| **是否需独立控制 ASR/TTS 模块** | ✅ 可单独调用 ASR/TTS 模型 | ❌ 所有模态绑定于 Omni 模型，不可解耦 | 需 ASR/TTS 独立计费或定制 → **Realtime API** |
| **SDK 依赖与维护成本** | 需集成 AOQ SDK（多端）或管理 WebRTC SDP | 仅需标准 WebSocket Client 或百炼 Python/JS SDK | 团队熟悉 WebSocket → **Omni 更轻量；需原生性能 → Realtime（AOQ）更优** |

> 💡 **最佳实践提示**：  
> - 新项目启动，若无特殊协议约束，**强烈推荐从 Omni Realtime API 入手**——其设计更贴近现代多模态 AI 应用范式，API 清晰、事件语义丰富、长期演进路线明确；  
> - 现有 Realtime API 用户，若新增图像理解或工具调用需求，**无需推翻重做**：可在 Realtime API 会话中完成 ASR → 将文本+图像送至 Omni Realtime API 发起新会话 → 获取结果后由 Realtime TTS 播报，实现能力组合；  
> - 所有生产环境务必通过 **百炼控制台** 核验模型最新名称、定价、上下文长度及限流策略，避免硬编码过期配置。

---  
*文档最后更新：2024年6月*  
*© 阿里云百炼平台技术文档组*

## 被对比主题页

- [realtime api user guide](../api/realtime-api-user-guide.md)
- [omni realtime api](../api/omni-realtime-api.md)



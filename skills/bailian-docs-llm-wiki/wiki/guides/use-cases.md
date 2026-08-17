# use cases

百炼平台提供覆盖文本、视觉、语音、多模态等全栈能力的 AI 应用构建支持，面向开发者提供开箱即用的行业方案与灵活可组合的技术组件。核心价值在于降低大模型应用门槛：无需自建基础设施即可快速验证业务逻辑，同时支持从 [Prompt 工程](../concepts/prompt-engineering.md)、RAG、Agent 编排到自定义模型微调的全链路开发。

## 支持的模型/功能

百炼支持两类模型接入方式：**平台原生模型**（如 `qwen3-vl-plus`、`qwen3.5-omni-plus-realtime`、`wan2.7`）和**第三方直供模型**（如 DeepSeek、Kimi、GLM、MiniMax、MiMo）。所有模型均通过统一 API 接口调用，支持 OpenAI 兼容协议与 DashScope SDK。

- **多模态理解与生成**：`qwen3-vl-plus` 支持图文输入解题与批改；`wan2.7` 和 `HappyHorse` 构成端到端视频生成管线；`qwen3.5-omni-plus-realtime` 支持音视频实时交互 [原文标题](../../raw/model-user-guide/use-cases/infinite-canvas.md)。
- **深度推理与研究**：`Qwen-Deep-Research` 模型专用于多轮检索、交叉验证与结构化报告生成，适用于投资尽调与战略分析场景 [原文标题](../../raw/model-user-guide/use-cases/deep-research.md)。
- **实时语音交互**：`qwen-audio-3.0-realtime-plus`（VAD 自动模式）与 `qwen3.5-omni-plus-realtime`（Manual 按键模式）分别适配不同硬件交互范式，AOQ SDK 提供跨平台（Android/iOS/HarmonyOS）接入能力 [原文标题](../../raw/model-user-guide/use-cases/best-practice-aoq-omni-realtime.md)。
- **第三方模型集成**：DeepSeek、Kimi、GLM、MiniMax、MiMo 等模型均需在华北2（北京）地域开通并使用专属业务空间域名（`https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com`），部分模型（如 `deepseek-v4-pro`）支持 `enable_thinking` 参数控制推理过程输出 [原文标题](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/deepseek-api-by-vanchin.md)。

> **注意**：文档 19 与文档 29 均描述 DeepSeek 集成，但存在关键差异：文档 19（阿里云百炼供应商）明确支持联网搜索与上下文缓存；文档 29（硅基流动供应商）强调更长上下文支持。二者限流策略与功能边界不同，开发者需根据业务需求选择对应供应商。

## 关键参数

- **Prompt 控制**：文生图（`text-to-image-prompt.md`）与文生视频（`text-to-video-prompt.md`）均采用结构化公式（主体+场景+运动/风格+美学控制），支持 `negative_prompt` 与 `prompt_extend`（V2）等精细化控制；Vidu 视频生成额外支持运镜、景别、导演风格等维度关键词 [原文标题](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/vidu-video-generation-prompt-guide.md)。
- **实时交互模式**：`qwen3.5-omni-plus-realtime` 支持 `server_vad`（服务端自动检测）与 `Manual`（客户端按键控制）两种轮次划分方式，后者需显式调用 `input_audio_buffer.commit` 与 `response.create` [原文标题](../../raw/model-user-guide/use-cases/use-aoq-to-access-qwen3-5-omni-plus-realtime-to-realize-key-voice-dialogue.md)。
- **思考模式开关**：DeepSeek、Kimi、GLM、MiniMax、MiMo 等第三方模型均通过非标准参数（如 `enable_thinking` 或 `reasoning_effort`）控制是否输出推理过程，该参数需通过 `extra_body`（Python SDK）或顶层字段（Node.js SDK）传入。
- **缓存与限流**：显式缓存（`cache_control`）支持对 system [prompt](prompt.md)、env、user message 等关键上下文片段进行标记复用；限流维度包含 RPM/TPM（分钟级）、RPS/TPS（瞬时）、Traffic Burst（增速），需配合 `X-DashScope-Wait-Timeout` 请求头应对突发流量 [原文标题](../../raw/model-user-guide/use-cases/rate-limiting-best-practices.md)。

## 使用方式

1. **快速验证**：所有方案均提供“15–30 分钟部署”路径，基于函数计算（FC）封装 Web 服务，依赖对象存储（OSS）、百炼模型服务与可选的 ECS 资源，按量付费且含免费试用额度。
2. **SDK 集成**：
   - 文本/多模态：使用 DashScope SDK 或 OpenAI 兼容 SDK，配置 `base_url` 为业务空间专属地址（如 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`）。
   - 实时音视频：WebRTC 方案需浏览器端直接连接，依赖 `RTCPeerConnection` 与 SDP 交换；AOQ 方案需 AppServer 代理鉴权获取 [Token](../concepts/token.md)，客户端集成 AOQ SDK 并处理 Audio/Data 双轨事件。
3. **RAG 构建**：通过 LlamaIndex 集成百炼知识库服务，使用 `DashScopeParse` 解析 PDF/DOCX 文件（单文件 ≤100MB，≤1000 页），调用 `DashScopeCloudIndex` 创建与检索索引。
4. **自定义模型**：遵循“调优→部署→评测”三步流程，训练数据需格式化为 `Prompt-Completion` 对，最低建议 500 条；模型必须部署后方可调用与评测。

## 限制和注意事项

- **地域与域名约束**：第三方模型（DeepSeek/Kimi/GLM/MiniMax/MiMo）仅在华北2（北京）地域可用，且强烈推荐迁移至业务空间专属域名（`{WorkspaceId}.cn-beijing.maas.aliyuncs.com`），旧域名 `dashscope.aliyuncs.com` 性能与稳定性较低。
- **模型下架计划**：`deepseek-v3.*`、`kimi-k2-*`、`glm-4.*`、`MiniMax-M2.1` 等模型将于 2026 年中至年末陆续下架，官方推荐迁移到 `qwen3.7-plus` 等通义系列模型。
- **实时交互权限**：WebRTC 方案需浏览器麦克风/摄像头权限；AOQ 方案在 Android/iOS/HarmonyOS 上需声明并动态申请 `RECORD_AUDIO`、`CAMERA` 权限，iOS 还需在 `Info.plist` 中配置 `NSMicrophoneUsageDescription`。
- **缓存与成本**：显式缓存首次写入产生 25% 额外开销，但命中后节省 90% 成本；若未发生至少一次命中，则总体成本高于不启用缓存。
- **文件解析限制**：`DashScopeParse` 仅支持 `.pdf`、`.doc`、`.docx`，单文件大小上限 100MB，页数上限 1000 页。

## 来源文档

- [高效搭建 AI 智能体与工作流应用](../../raw/model-user-guide/use-cases/build-ai-applications-based-on-alibaba-cloud-model-studio.md)
- [AI 解题 + 批改：推动课程教学智变](../../raw/model-user-guide/use-cases/ai-homework-helper.md)
- [HappyHorse 打造一站式影视创作平台](../../raw/model-user-guide/use-cases/infinite-canvas.md)
- [深度研究：生成你的独家洞察报告](../../raw/model-user-guide/use-cases/deep-research.md)
- [文生视频/图生视频Prompt指南](../../raw/model-user-guide/use-cases/text-to-video-prompt.md)
- [基于LlamaIndex构建RAG应用](../../raw/model-user-guide/use-cases/build-rag-applications-based-on-llamaindex.md)
- [自定义模型调优、部署与评测](../../raw/model-user-guide/use-cases/model-training-best-practices.md)
- [借助大模型将文档转换为视频](../../raw/model-user-guide/use-cases/use-llm-to-convert-document-to-video.md)
- [限流应对最佳实践 ](../../raw/model-user-guide/use-cases/rate-limiting-best-practices.md)
- [显式缓存最佳实践](../../raw/model-user-guide/use-cases/explicit-cache-guide.md)
- [通过WebRTC使用多模态交互套件实现实时通话](../../raw/model-user-guide/use-cases/best-practice-webrtc-multimodal-dialog.md)
- [通过WebRTC使用qwen3.5-omni-plus-realtime实现实时通话](../../raw/model-user-guide/use-cases/best-practice-webrtc-omni-realtime.md)
- [通过AOQ使用qwen3.5-omni-plus-realtime实现实时通话](../../raw/model-user-guide/use-cases/best-practice-aoq-omni-realtime.md)
- [使用 AOQ 接入 qwen3.5-omni-plus-realtime 实现按键语音对话](../../raw/model-user-guide/use-cases/use-aoq-to-access-qwen3-5-omni-plus-realtime-to-realize-key-voice-dialogue.md)
- [使用 AOQ 接入 qwen-audio-3.0-realtime-plus 实现实时语音对话](../../raw/model-user-guide/use-cases/real-time-voice-conversation-using-aoq-access-qwen-audio-3-0-realtime-plus.md)
- [使用 AOQ 接入 qwen-audio-3.0-tts-flash 实现语音合成](../../raw/model-user-guide/use-cases/speech-synthesis-using-aoq-access-qwen-audio-3-0-tts-flash.md)
- [使用 AOQ 接入 fun-asr-realtime 实现实时语音识别](../../raw/model-user-guide/use-cases/real-time-speech-recognition-using-aoq-access-fun-asr-realtime.md)
- [文生图Prompt指南](../../raw/model-user-guide/use-cases/text-to-image-prompt.md)
- [DeepSeek-阿里云](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/deepseek-api.md)
- [DeepSeek](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/deepseek-api-by-vanchin.md)
- [Kimi](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/kimi-api.md)
- [Kimi-月之暗面](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/kimi-api-by-moonshot-ai.md)
- [GLM](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/glm.md)
- [GLM-智谱](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/glm-zhipu.md)
- [MiniMax](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/minimax-api.md)
- [MiniMax](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/minimax-api-by-minimax.md)
- [Vidu视频生成Prompt指南](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/vidu-video-generation-prompt-guide.md)
- [MiMo-小米](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/mimo.md)
- [DeepSeek-硅基流动](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/siliconflow-deepseek-api.md)



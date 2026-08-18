# use cases

百炼平台的 use cases 覆盖从基础文本生成到多模态实时交互的全栈能力，支持开发者快速构建生产级 AI 应用。核心价值在于提供开箱即用的模型服务、标准化的调用接口与面向真实业务场景的端到端解决方案，而非仅限于单点 API 调用。

## 支持的模型/功能

百炼平台提供两类核心能力：**原生模型服务**与**第三方模型集成**。

- **原生模型**：覆盖文本（Qwen 系列）、视觉（万相、HappyHorse、Qwen-VL）、语音（qwen-audio-*、qwen3.5-omni-plus-realtime）及多模态（qwen3.5-omni-plus-realtime）全栈能力。例如，`qwen3-vl-plus` 专用于解题与批改 [AI 解题 + 批改：推动课程教学智变](../../raw/model-user-guide/use-cases/ai-homework-helper.md)，`HappyHorse` 支持影视级图生视频 [HappyHorse 打造一站式影视创作平台](../../raw/model-user-guide/use-cases/infinite-canvas.md)。
  
- **第三方模型集成**：通过 [OpenAI 兼容接口](../concepts/openai-compatible-api.md)或 DashScope SDK 接入 DeepSeek、Kimi、GLM、MiniMax、MiMo、Stepfun 等厂商模型。所有第三方模型均需在华北2（北京）地域开通并配置专属 `base_url`，且多数仅支持该地域（如 [DeepSeek-硅基流动](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/siliconflow-deepseek-api.md)、[Kimi-月之暗面](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/kimi-api-by-moonshot-ai.md)）。> **注意**：多个文档（如文档20、23、25、27）均声明部分第三方模型将于2026年下架，但未统一说明迁移路径或兼容性保障，建议以控制台最新公告为准。

- **专用工具链**：除通用模型外，平台提供深度研究（Qwen-Deep-Research）、RAG（基于 LlamaIndex）、[Prompt 工程](../concepts/prompt-engineering.md)（文生文/文生图/文生视频指南）、实时音视频（WebRTC/AOQ）、缓存优化（显式缓存）、限流应对等垂直能力模块。

## 关键参数

不同模型与协议对关键参数有明确约定：

- **Prompt 相关**：  
  - 文生文：推荐使用 `背景/目的/风格/语气/受众/输出` 六要素 Prompt 框架 [文生文Prompt指南](../../raw/model-user-guide/use-cases/prompt-engineering-guide.md)；  
  - 文生图：`prompt`（正向）与 `negative_prompt`（反向）为必需参数，V2 版本默认启用 `prompt_extend` 智能改写；  
  - 文生视频：基础公式为 `主体+场景+运动`，进阶需补充 `美学控制` 与 `风格化`，多镜头需显式指定 `时间戳` 与 `分镜内容`。

- **实时交互**：  
  - WebRTC 模式必须设置 `X-DashScope-Wait-Timeout` 头应对突发流量 [限流应对最佳实践](../../raw/model-user-guide/use-cases/rate-limiting-best-practices.md)；  
  - AOQ Manual 模式需将 `session.turn_detection` 设为 `null` 并显式调用 `input_audio_buffer.commit` 与 `response.create` [使用 AOQ 接入 qwen3.5-omni-plus-realtime 实现按键语音对话](../../raw/model-user-guide/use-cases/use-aoq-to-access-qwen3-5-omni-plus-realtime-to-realize-key-voice-dialogue.md)。

- **第三方模型扩展参数**：  
  `enable_thinking`（DeepSeek、MiMo、Stepfun）、`reasoning_effort`（Kimi、GLM）、`preserve_thinking`（Kimi）等非 OpenAI 标准参数，须通过 `extra_body`（Python SDK）或顶层字段（Node.js SDK）传入。

## 使用方式

接入方式按技术栈与部署形态分为三类：

- **低代码/无代码**：通过百炼控制台直接创建应用，如“无限画布”可视化编排节点、“AI 电商客服助手”流程拖拽配置，适用于快速验证 [高效搭建 AI 智能体与工作流应用](../../raw/model-user-guide/use-cases/build-ai-applications-based-on-alibaba-cloud-model-studio.md)。

- **SDK/API 编程**：  
  - 通用模型：使用 DashScope SDK 或 OpenAI 兼容客户端，按 `model`、`messages`、`parameters` 结构构造请求；  
  - RAG 场景：集成 `llama-index-indices-managed-dashscope`，通过 `DashScopeCloudIndex` 创建与检索知识库 [基于LlamaIndex构建RAG应用](../../raw/model-user-guide/use-cases/build-rag-applications-based-on-llamaindex.md)；  
  - 实时音视频：WebRTC 需浏览器原生 `RTCPeerConnection` + SDP 交换；AOQ 需各端 SDK（Android/iOS/HarmonyOS）导入 `.aar`/`.framework`/`.har` 包并申请 `RECORD_AUDIO` 权限。

- **Serverless 部署**：函数计算（FC）作为主流载体，支撑深度研究、文档转视频等端到端方案，15 分钟内可完成部署 [深度研究：生成你的独家洞察报告](../../raw/model-user-guide/use-cases/deep-research.md)。

## 限制和注意事项

- **地域与模型绑定**：绝大多数第三方模型（DeepSeek、Kimi、GLM、MiniMax、MiMo、Stepfun）仅支持华北2（北京）地域，且需使用业务空间专属域名 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com`，旧域名 `dashscope.aliyuncs.com` 性能与稳定性较低 [GLM-智谱](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/glm-zhipu.md)。

- **限流策略**：API 受 RPM/TPM（分钟级）、RPS/TPS（瞬时）、Traffic Burst（增速）三重约束。单纯重试无效，必须结合 `X-DashScope-Wait-Timeout` 头、客户端令牌桶或架构层 MQ 削峰 [限流应对最佳实践](../../raw/model-user-guide/use-cases/rate-limiting-best-practices.md)。

- **安全与合规**：  
  - API Key 严禁硬编码至客户端，必须由业务 AppServer 代理鉴权并下发临时 Token [使用 AOQ 接入 qwen3.5-omni-plus-realtime 实现按键语音对话](../../raw/model-user-guide/use-cases/use-aoq-to-access-qwen3-5-omni-plus-realtime-to-realize-key-voice-dialogue.md)；  
  - 训练数据需脱敏处理，避免泄露个人身份信息或敏感内容 [自定义模型调优、部署与评测](../../raw/model-user-guide/use-cases/model-training-best-practices.md)。

- **成本控制**：显式缓存首次写入产生 25% 额外开销，但命中后节省 90% 成本；需确保至少一次命中才优于不缓存方案 [显式缓存最佳实践](../../raw/model-user-guide/use-cases/explicit-cache-guide.md)。

## 来源文档

- [HappyHorse 打造一站式影视创作平台](../../raw/model-user-guide/use-cases/infinite-canvas.md)
- [高效搭建 AI 智能体与工作流应用](../../raw/model-user-guide/use-cases/build-ai-applications-based-on-alibaba-cloud-model-studio.md)
- [深度研究：生成你的独家洞察报告](../../raw/model-user-guide/use-cases/deep-research.md)
- [文生文Prompt指南](../../raw/model-user-guide/use-cases/prompt-engineering-guide.md)
- [文生图Prompt指南](../../raw/model-user-guide/use-cases/text-to-image-prompt.md)
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
- [AI 解题 + 批改：推动课程教学智变](../../raw/model-user-guide/use-cases/ai-homework-helper.md)
- [使用 AOQ 接入 qwen-audio-3.0-tts-flash 实现语音合成](../../raw/model-user-guide/use-cases/speech-synthesis-using-aoq-access-qwen-audio-3-0-tts-flash.md)
- [使用 AOQ 接入 fun-asr-realtime 实现实时语音识别](../../raw/model-user-guide/use-cases/real-time-speech-recognition-using-aoq-access-fun-asr-realtime.md)
- [DeepSeek-阿里云](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/deepseek-api.md)
- [DeepSeek-硅基流动](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/siliconflow-deepseek-api.md)
- [DeepSeek](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/deepseek-api-by-vanchin.md)
- [Kimi](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/kimi-api.md)
- [Kimi-月之暗面](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/kimi-api-by-moonshot-ai.md)
- [GLM](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/glm.md)
- [GLM-智谱](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/glm-zhipu.md)
- [MiniMax](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/minimax-api.md)
- [MiniMax](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/minimax-api-by-minimax.md)
- [Vidu视频生成Prompt指南](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/vidu-video-generation-prompt-guide.md)
- [MiMo-小米](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/mimo.md)
- [Stepfun-阶跃星辰](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/stepfun.md)



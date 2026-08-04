# use cases

百炼平台提供覆盖文本、图像、视频、语音、多模态及智能体等全场景的 AI 应用能力，支持从 [Prompt 工程](../concepts/prompt-engineering.md)、RAG 构建、模型微调到实时音视频交互的完整技术栈。开发者可基于预置模型快速验证业务逻辑，也可通过自定义模型与高级编排能力构建生产级应用。

## 支持的模型/功能

百炼平台支持两类核心模型能力：**阿里云自研模型**（如 Qwen 系列、Qwen3-VL、qwen3.5-omni-plus-realtime）和**第三方直供模型**（如 DeepSeek、Kimi、GLM、MiniMax、MiMo、Stepfun、Vidu）。其中：

- **文本生成与推理**：Qwen3.7-plus/max、qwen3-vl-plus、deepseek-v3.2、kimi-k3、glm-5.2、MiniMax-M2.7、xiaomi/mimo-v2.5-pro、stepfun/step-3.7-flash 等均支持 `enable_thinking` 或 `reasoning_effort` 参数开启结构化推理过程 [DeepSeek-硅基流动](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/siliconflow-deepseek-api.md)；  
- **多模态理解与生成**：Qwen3-VL 系列模型支撑 AI 解题与批改场景，具备 MathVista、MMMU 等权威评测 SOTA 能力 [AI 解题 + 批改：推动课程教学智变](../../raw/model-user-guide/use-cases/ai-homework-helper.md)；  
- **视觉生成**：万相（Wan2.7）、HappyHorse、Vidu 提供文生图、图生图、文生视频、图生视频等能力，支持精细化 Prompt 控制（景别、运镜、风格、动态等）[Vidu视频生成Prompt指南](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/vidu-video-generation-prompt-guide.md)；  
- **实时音视频交互**：`qwen3.5-omni-plus-realtime` 与多模态交互套件（multimodal-dialog）分别支持 WebRTC 浏览器端低延迟通话与 AOQ SDK 移动端集成 [通过WebRTC使用qwen3.5-omni-plus-realtime实现实时通话](../../raw/model-user-guide/use-cases/best-practice-webrtc-omni-realtime.md)；  
- **智能体与工作流**：支持 RAG（基于 LlamaIndex 集成）、自主决策 Agent、复杂对话流编排，典型应用于电商客服助手 [高效搭建 AI 智能体与工作流应用](../../raw/model-user-guide/use-cases/build-ai-applications-based-on-alibaba-cloud-model-studio.md)。

> **注意**：多个第三方模型文档（如 [DeepSeek-阿里云](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/deepseek-api.md)、[Kimi](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/kimi-api.md)、[GLM](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/glm.md)、[MiniMax](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/minimax-api.md)）均声明部分旧版本模型将于 2026 年下架，并统一推荐迁移至 Qwen3 系列。该迁移路径为平台当前主推策略，开发者应优先选用 qwen3.7-plus/max/flash 等新版模型。

## 关键参数

不同模型与能力模块暴露差异化关键参数，需按场景正确配置：

- **推理控制**：`enable_thinking`（DeepSeek、MiMo、Stepfun）、`reasoning_effort`（Kimi、GLM）、`server_vad`（Realtime API）为非 OpenAI 标准参数，须通过 `extra_body`（Python SDK）或顶层字段（Node.js SDK）传入；  
- **视觉生成**：文生图支持 `prompt`（正向）、`negative_prompt`（反向）、`prompt_extend`（是否启用大模型智能扩写）；文生视频支持 `motion`、`aesthetic_control`、`style` 及多镜头时间戳语法 [文生视频/图生视频Prompt指南](../../raw/model-user-guide/use-cases/text-to-video-prompt.md)；  
- **缓存与限流**：显式缓存依赖 `cache_control` 字段（Anthropic 协议兼容），需在 system [prompt](prompt.md) 或 user message 中标记；限流应对需设置 `X-DashScope-Wait-Timeout` 请求头实现服务端排队 [限流应对最佳实践](../../raw/model-user-guide/use-cases/rate-limiting-best-practices.md)；  
- **实时音视频**：WebRTC 模式强制要求 `server_vad` 或 `semantic_vad`，不支持手动 VAD；AOQ SDK 需通过 AppServer 获取 [Token](../concepts/token.md) 完成鉴权 [通过AOQ使用qwen3.5-omni-plus-realtime实现实时通话](../../raw/model-user-guide/use-cases/best-practice-aoq-omni-realtime.md)。

## 使用方式

百炼提供多种接入路径，适配不同开发阶段与架构需求：

- **零代码/低代码**：通过控制台可视化创建知识库、配置 RAG 应用、部署智能体工作流，或使用 Prompt 一键优化工具提升提示词质量 [文生文Prompt指南](../../raw/model-user-guide/use-cases/prompt-engineering-guide.md)；  
- **SDK/API 集成**：  
  - [OpenAI 兼容接口](../concepts/openai-compatible-interface.md)：适用于华北2（北京）等支持地域，需配置 `base_url` 为 `{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`；  
  - DashScope 原生 SDK：适用于跨地域调用，需设置 `base_http_api_url`；  
  - 第三方框架集成：LlamaIndex 通过 `llama-index-indices-managed-dashscope` 插件直接对接百炼知识库服务 [基于LlamaIndex构建RAG应用](../../raw/model-user-guide/use-cases/build-rag-applications-based-on-llamaindex.md)；  
- **端侧部署**：WebRTC 方案依赖浏览器 `RTCPeerConnection` 与 `getUserMedia`，需处理 SDP 交换代理（Demo 中用 curl，生产环境需业务后端代理）；AOQ SDK 提供 Android/iOS/HarmonyOS 原生封装，需集成 `.aar`/`.framework`/`.har` 并申请运行时权限；  
- **批量与异步处理**：函数计算（FC）是主流部署模式，用于深度研究报告生成、文档转视频等长耗时任务，具备弹性伸缩与按量付费优势 [借助大模型将文档转换为视频](../../raw/model-user-guide/use-cases/use-llm-to-convert-document-to-video.md)。

## 限制和注意事项

- **地域与域名约束**：多数第三方模型（DeepSeek、Kimi、GLM、MiniMax、MiMo、Stepfun）仅在华北2（北京）地域可用，且强烈建议使用业务空间专属域名 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com` 替代通用 `dashscope.aliyuncs.com` 以获得更高稳定性 [GLM-智谱](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/glm-zhipu.md)；  
- **限流维度**：API 同时受 RPM（每分钟请求数）、TPM（每分钟 [Token](../concepts/token.md) 数）、RPS/TPS（瞬时速率）及 Traffic Burst（增速突增）四重限制，单一重试策略无效，必须结合服务端排队、客户端令牌桶、架构层 MQ 削峰等组合方案 [限流应对最佳实践](../../raw/model-user-guide/use-cases/rate-limiting-best-practices.md)；  
- **缓存确定性**：显式缓存仅对完全相同的 `prompt` + `cache_control` 标记组合 100% 命中，Agent 场景中动态 system [prompt](prompt.md)（如含 git 状态）会显著降低跨会话命中率，建议启用 `--exclude-dynamic-system-prompt-sections` 参数 [显式缓存最佳实践](../../raw/model-user-guide/use-cases/explicit-cache-guide.md)；  
- **文件与资源限制**：DashScopeParse 文档解析器单文件上限为 100MB 且页数 ≤1000；FFmpeg/Marp 等本地工具需提前安装并配置国内镜像源；浏览器端 WebRTC 需确保麦克风/摄像头权限及 CORS 代理支持。

## 来源文档

- [高效搭建 AI 智能体与工作流应用](../../raw/model-user-guide/use-cases/build-ai-applications-based-on-alibaba-cloud-model-studio.md)
- [深度研究：生成你的独家洞察报告](../../raw/model-user-guide/use-cases/deep-research.md)
- [文生文Prompt指南](../../raw/model-user-guide/use-cases/prompt-engineering-guide.md)
- [AI 解题 + 批改：推动课程教学智变](../../raw/model-user-guide/use-cases/ai-homework-helper.md)
- [文生图Prompt指南](../../raw/model-user-guide/use-cases/text-to-image-prompt.md)
- [基于LlamaIndex构建RAG应用](../../raw/model-user-guide/use-cases/build-rag-applications-based-on-llamaindex.md)
- [自定义模型调优、部署与评测](../../raw/model-user-guide/use-cases/model-training-best-practices.md)
- [借助大模型将文档转换为视频](../../raw/model-user-guide/use-cases/use-llm-to-convert-document-to-video.md)
- [限流应对最佳实践 ](../../raw/model-user-guide/use-cases/rate-limiting-best-practices.md)
- [显式缓存最佳实践](../../raw/model-user-guide/use-cases/explicit-cache-guide.md)
- [通过WebRTC使用多模态交互套件实现实时通话](../../raw/model-user-guide/use-cases/best-practice-webrtc-multimodal-dialog.md)
- [通过WebRTC使用qwen3.5-omni-plus-realtime实现实时通话](../../raw/model-user-guide/use-cases/best-practice-webrtc-omni-realtime.md)
- [通过AOQ使用qwen3.5-omni-plus-realtime实现实时通话](../../raw/model-user-guide/use-cases/best-practice-aoq-omni-realtime.md)
- [HappyHorse 打造一站式影视创作平台](../../raw/model-user-guide/use-cases/infinite-canvas.md)
- [文生视频/图生视频Prompt指南](../../raw/model-user-guide/use-cases/text-to-video-prompt.md)
- [DeepSeek-硅基流动](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/siliconflow-deepseek-api.md)
- [DeepSeek-阿里云](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/deepseek-api.md)
- [Kimi](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/kimi-api.md)
- [DeepSeek](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/deepseek-api-by-vanchin.md)
- [Kimi-月之暗面](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/kimi-api-by-moonshot-ai.md)
- [GLM](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/glm.md)
- [GLM-智谱](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/glm-zhipu.md)
- [MiniMax](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/minimax-api.md)
- [MiMo-小米](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/mimo.md)
- [Vidu视频生成Prompt指南](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/vidu-video-generation-prompt-guide.md)
- [Stepfun-阶跃星辰](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/stepfun.md)
- [MiniMax](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/minimax-api-by-minimax.md)



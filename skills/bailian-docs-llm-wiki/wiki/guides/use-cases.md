# use cases

百炼平台提供覆盖文本、图像、视频、语音等多模态的端到端 AI 应用场景支持，面向开发者提供开箱即用的解决方案与可组合的底层能力。核心价值在于通过统一模型服务、可视化编排、智能体工作流与专业 [Prompt 工程](../concepts/prompt-engineering.md)体系，降低复杂 AI 应用的构建门槛，同时保障生产级稳定性与可控性。

## 支持的模型/功能

百炼支持两类能力：**阿里云自研模型**（如 Qwen 系列、Wan2.7、HappyHorse、Qwen3-VL）和**第三方直供模型**（如 DeepSeek、Kimi、GLM、MiniMax、Stepfun、MiMo）。所有模型均通过统一 API 接口（OpenAI 兼容或 DashScope SDK）调用，支持流式响应、思考模式（`enable_thinking`/`reasoning_effort`）、长上下文（最高 1M tokens）及多模态输入（文本、图像、视频）。

- **文本生成与推理**：Qwen3.7-max、qwen-plus、kimi/kimi-k3、ZHIPU/GLM-5.2 等支持结构化输出、深度推理与代码生成；[DeepSeek-阿里云](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/deepseek-api.md) 提供联网搜索与上下文缓存能力。
- **视觉生成**：万相系列（文生图 V1/V2、文生视频、图生视频）、Vidu、HappyHorse 视频生成模型，支持节点式无限画布编排与 AI 导演对话式创作；[HappyHorse 打造一站式影视创作平台](../../raw/model-user-guide/use-cases/infinite-canvas.md) 展示了从分镜到成片的全链路闭环。
- **智能体与工作流**：支持 RAG（基于 LlamaIndex 构建[知识库](../concepts/knowledge-base.md)）、自主决策 Agent、多步骤对话流编排；[高效搭建 AI 智能体与工作流应用](../../raw/model-user-guide/use-cases/build-ai-applications-based-on-alibaba-cloud-model-studio.md) 提供电商客服等典型范式。
- **专业垂直场景**：Qwen-Deep-Research 实现多源交叉验证的深度研究报告生成；Qwen3-VL 支持中小学至大学全学科的解题与批改；文档转视频方案实现图文、语音、字幕一体化输出。

> **注意**：多个第三方模型文档（如 [DeepSeek-阿里云](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/deepseek-api.md)、[Kimi](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/kimi-api.md)、[GLM](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/glm.md)、[MiniMax](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/minimax-api.md)）均声明部分旧版本将于 2026 年下架，并统一推荐迁移至 Qwen3 系列。该策略具有一致性，非矛盾信息。

## 关键参数

不同模态任务需关注特定参数：

- **文本模型通用参数**：`model`（模型标识符，如 `qwen3.7-max` 或 `kimi/kimi-k3`）、`stream`（是否流式）、`extra_body`（非标准参数载体，用于 `enable_thinking`、`reasoning_effort`、`preserve_thinking` 等）。
- **文生图参数**：`prompt`（正向提示词）、`negative_prompt`（反向提示词）、`prompt_extend`（是否启用大模型智能改写，默认 `true`）；[文生图Prompt指南](../../raw/model-user-guide/use-cases/text-to-image-prompt.md) 提供基础与进阶公式。
- **文生/图生视频参数**：`prompt`（描述主体、场景、运动及美学控制）、`shot_type`（已弃用，由模型自动判断单/多镜头）、`video_length`（时长）、`frame_rate`（帧率）；[文生视频/图生视频Prompt指南](../../raw/model-user-guide/use-cases/text-to-video-prompt.md) 明确多镜头需用时间戳分镜语法。
- **缓存与限流**：`cache_control`（显式缓存标记，用于 Claude Code、OpenCode 等工具）、`X-DashScope-Wait-Timeout`（服务端排队等待头，应对突发流量）；[显式缓存最佳实践](../../raw/model-user-guide/use-cases/explicit-cache-guide.md) 和 [限流应对最佳实践](../../raw/model-user-guide/use-cases/rate-limiting-best-practices.md) 分别详述其配置逻辑。

## 使用方式

开发者可通过三种路径快速集成：

1. **零代码方案**：直接部署预置解决方案，如 15 分钟内完成 [深度研究：生成你的独家洞察报告](../../raw/model-user-guide/use-cases/deep-research.md) 或 [AI 解题 + 批改：推动课程教学智变](../../raw/model-user-guide/use-cases/ai-homework-helper.md) 的函数计算 Web 服务。
2. **低代码编排**：在百炼控制台使用可视化节点（文本、图像、视频、RAG、Agent）拖拽构建工作流，适用于 [HappyHorse 打造一站式影视创作平台](../../raw/model-user-guide/use-cases/infinite-canvas.md) 中的无限画布场景。
3. **代码集成**：
   - 调用 [OpenAI 兼容接口](../concepts/openai-compatible-interface.md)（推荐），配置 `base_url` 为地域专属域名（如 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`）；
   - 使用 DashScope SDK，设置 `base_http_api_url`；
   - 第三方模型需按供应商开通（如 SiliconFlow DeepSeek 需单独开通卡片），并注意 `model` 参数前缀（如 `siliconflow/deepseek-v3.2`）。

所有方案均依赖 API Key 认证，建议通过环境变量配置以规避密钥泄露风险。

## 限制和注意事项

- **地域与模型绑定**：多数第三方模型（DeepSeek、Kimi、GLM、MiniMax、Stepfun、MiMo）仅在华北2（北京）地域可用，且必须使用该地域的 API Key 与业务空间 ID；[DeepSeek-硅基流动](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/siliconflow-deepseek-api.md) 文档明确指出“仅适用于华北2（北京）地域”。
- **限流维度**：API 受 RPM（每分钟请求数）、TPM（每分钟 Token 数）、RPS（每秒请求数）、TPS（每秒 Token 数）及 Traffic Burst（增速限制）五重约束；单纯重试无效，需结合 [限流应对最佳实践](../../raw/model-user-guide/use-cases/rate-limiting-best-practices.md) 中的服务端排队、客户端令牌桶或架构层 MQ 削峰。
- **缓存适用性**：显式缓存要求输入内容高度稳定，动态字段（如当前日期、Git 状态）会降低跨会话命中率；[显式缓存最佳实践](../../raw/model-user-guide/use-cases/explicit-cache-guide.md) 建议通过 `--exclude-dynamic-system-prompt-sections` 等参数剥离。
- **实时音视频约束**：WebRTC 模式下浏览器无法直连 SDP 交换，需后端代理；AOQ SDK 需按平台（Android/iOS/HarmonyOS）导入对应 native 库与权限声明；所有实时方案均强制要求麦克风权限，视频为可选。
- **[Prompt 工程](../concepts/prompt-engineering.md)必要性**：对生成质量敏感的场景（文生图、文生视频），必须遵循结构化公式（如 [文生图Prompt指南](../../raw/model-user-guide/use-cases/text-to-image-prompt.md) 中的“主体+场景+风格”基础公式），模糊提示将导致结果不可控。

## 来源文档

- [HappyHorse 打造一站式影视创作平台](../../raw/model-user-guide/use-cases/infinite-canvas.md)
- [高效搭建 AI 智能体与工作流应用](../../raw/model-user-guide/use-cases/build-ai-applications-based-on-alibaba-cloud-model-studio.md)
- [深度研究：生成你的独家洞察报告](../../raw/model-user-guide/use-cases/deep-research.md)
- [AI 解题 + 批改：推动课程教学智变](../../raw/model-user-guide/use-cases/ai-homework-helper.md)
- [文生文Prompt指南](../../raw/model-user-guide/use-cases/prompt-engineering-guide.md)
- [文生图Prompt指南](../../raw/model-user-guide/use-cases/text-to-image-prompt.md)
- [基于LlamaIndex构建RAG应用](../../raw/model-user-guide/use-cases/build-rag-applications-based-on-llamaindex.md)
- [文生视频/图生视频Prompt指南](../../raw/model-user-guide/use-cases/text-to-video-prompt.md)
- [自定义模型调优、部署与评测](../../raw/model-user-guide/use-cases/model-training-best-practices.md)
- [借助大模型将文档转换为视频](../../raw/model-user-guide/use-cases/use-llm-to-convert-document-to-video.md)
- [限流应对最佳实践 ](../../raw/model-user-guide/use-cases/rate-limiting-best-practices.md)
- [显式缓存最佳实践](../../raw/model-user-guide/use-cases/explicit-cache-guide.md)
- [通过WebRTC使用多模态交互套件实现实时通话](../../raw/model-user-guide/use-cases/best-practice-webrtc-multimodal-dialog.md)
- [通过WebRTC使用qwen3.5-omni-plus-realtime实现实时通话](../../raw/model-user-guide/use-cases/best-practice-webrtc-omni-realtime.md)
- [通过AOQ使用qwen3.5-omni-plus-realtime实现实时通话](../../raw/model-user-guide/use-cases/best-practice-aoq-omni-realtime.md)
- [DeepSeek-阿里云](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/deepseek-api.md)
- [DeepSeek-硅基流动](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/siliconflow-deepseek-api.md)
- [DeepSeek](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/deepseek-api-by-vanchin.md)
- [Kimi-月之暗面](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/kimi-api-by-moonshot-ai.md)
- [Kimi](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/kimi-api.md)
- [GLM](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/glm.md)
- [GLM-智谱](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/glm-zhipu.md)
- [MiniMax](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/minimax-api.md)
- [Vidu视频生成Prompt指南](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/vidu-video-generation-prompt-guide.md)
- [MiniMax](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/minimax-api-by-minimax.md)
- [Stepfun-阶跃星辰](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/stepfun.md)
- [MiMo-小米](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/mimo.md)



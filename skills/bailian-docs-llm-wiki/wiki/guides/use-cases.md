# use cases

百炼平台提供覆盖文本、图像、视频、语音及多模态的全栈AI能力，支持从Prompt工程、RAG构建、智能体编排到实时音视频交互等多样化生产级用例。开发者可基于预置模型快速验证场景，也可通过自定义模型调优、第三方模型集成与缓存优化等手段深度适配业务需求。

## 支持的模型/功能

百炼平台支持两类核心模型能力：**阿里云自研模型**（如 Qwen3 系列、Wan2.7、HappyHorse、Qwen3-VL）和**第三方直供模型**（如 DeepSeek、Kimi、GLM、MiniMax、MiMo、Stepfun）。其中，Qwen3-VL 模型在 MathVista、MMMU 等评测中达到 SOTA 水平，适用于高精度解题与批改场景 [AI 解题 + 批改：推动课程教学智变](../../raw/model-user-guide/use-cases/ai-homework-helper.md)；Wan2.7 与 HappyHorse 分别支撑文生视频与图生视频能力，支持多镜头叙事、运镜控制与声音公式等高级提示词结构 [文生视频/图生视频Prompt指南](../../raw/model-user-guide/use-cases/text-to-video-prompt.md)；而 MiniMax-M2.7、Kimi-k3 等第三方模型均支持 `enable_thinking` 或 `reasoning_effort` 参数开启结构化推理过程，便于调试与可解释性分析 [MiniMax](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/minimax-api-by-minimax.md)。

> **注意**：多个第三方模型文档（如 DeepSeek、Kimi、GLM、MiniMax）均声明部分旧版本将于 2026 年下架，并统一推荐迁移至 Qwen3 系列（如 `qwen3.7-plus`、`qwen3.7-max`），但各文档未明确说明迁移路径是否兼容历史 API 参数或 [Token](../concepts/token.md) 计费策略，建议以[模型市场](https://bailian.console.aliyun.com/cn-beijing/?tab=model#/model-market)最新规格为准。

## 关键参数

- **Prompt 相关**：文生文场景推荐使用 Prompt 框架（含背景、目的、风格、语气、受众、输出六要素）提升生成质量；文生图/视频需区分 `prompt`（正向）与 `negative_prompt`（反向），V2 版本默认启用 `prompt_extend` 智能改写；Vidu 视频生成支持 `大动态`、`固定镜头`、`宫崎骏风格` 等细粒度关键词控制 [Vidu视频生成Prompt指南](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/vidu-video-generation-prompt-guide.md)。
- **推理控制**：第三方模型普遍支持非标准参数：`enable_thinking`（开启思考流）、`reasoning_effort`（控制推理深度）、`preserve_thinking`（多轮传递思考过程），需通过 `extra_body`（Python SDK）或顶层参数（Node.js SDK）传入。
- **缓存与性能**：显式缓存通过 `cache_control` 标记实现确定性命中，适用于高频复用 Prompt 或 Agent 长上下文管理；WebRTC 实时通话强制使用 `server_vad` 模式，不支持手动 VAD [通过WebRTC使用qwen3.5-omni-plus-realtime实现实时通话](../../raw/model-user-guide/use-cases/best-practice-webrtc-omni-realtime.md)。

## 使用方式

1. **快速部署**：所有方案均提供“15 分钟部署”路径，依赖函数计算（FC）+ 百炼模型服务组合，按量付费（典型成本 0.3–30 元/次），支持一键部署至阿里云环境。
2. **SDK/API 调用**：
   - OpenAI 兼容模式：配置 `base_url` 指向地域专属端点（如 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`），模型名格式为 `vendor/model-name`（如 `xiaomi/mimo-v2.5-pro`）。
   - DashScope 原生模式：需设置 `base_http_api_url`，并按模型类型选择 `text-generation` 或 `multimodal-generation` 接口。
3. **工作流编排**：通过节点式无限画布（Infinite Canvas）可视化连接文本、图像、视频生成节点，或使用 LlamaIndex 构建 RAG 应用，将知识库与 Qwen-Max 等大模型无缝集成 [基于LlamaIndex构建RAG应用](../../raw/model-user-guide/use-cases/build-rag-applications-based-on-llamaindex.md)。

## 限制和注意事项

- **地域与权限约束**：DeepSeek、Kimi、GLM、MiniMax、MiMo、Stepfun 等第三方模型文档均强调“仅华北2（北京）地域可用”，且要求使用该地域的 API Key；AOQ SDK 需在 Android/iOS/HarmonyOS 工程中声明麦克风与摄像头运行时权限。
- **限流机制**：百炼 API 按 RPM/TPM（分钟级）、RPS/TPS（瞬时）、Traffic Burst（增速）三维度限流，`429` 错误需结合错误码诊断具体触发维度，推荐首选服务端排队等待（`X-DashScope-Wait-Timeout` 请求头）应对突发流量 [限流应对最佳实践](../../raw/model-user-guide/use-cases/rate-limiting-best-practices.md)。
- **模型生命周期**：第三方模型存在明确下架时间（如 DeepSeek-v3 系列于 2026-10-10 下架），且不同供应商模型能力差异显著——硅基流动版 DeepSeek 支持更长上下文，阿里云百炼版则提供联网搜索与上下文缓存功能，选型时需权衡 [DeepSeek-硅基流动](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/siliconflow-deepseek-api.md)。

## 来源文档

- [HappyHorse 打造一站式影视创作平台](../../raw/model-user-guide/use-cases/infinite-canvas.md)
- [深度研究：生成你的独家洞察报告](../../raw/model-user-guide/use-cases/deep-research.md)
- [高效搭建 AI 智能体与工作流应用](../../raw/model-user-guide/use-cases/build-ai-applications-based-on-alibaba-cloud-model-studio.md)
- [AI 解题 + 批改：推动课程教学智变](../../raw/model-user-guide/use-cases/ai-homework-helper.md)
- [文生文Prompt指南](../../raw/model-user-guide/use-cases/prompt-engineering-guide.md)
- [文生图Prompt指南](../../raw/model-user-guide/use-cases/text-to-image-prompt.md)
- [文生视频/图生视频Prompt指南](../../raw/model-user-guide/use-cases/text-to-video-prompt.md)
- [基于LlamaIndex构建RAG应用](../../raw/model-user-guide/use-cases/build-rag-applications-based-on-llamaindex.md)
- [自定义模型调优、部署与评测](../../raw/model-user-guide/use-cases/model-training-best-practices.md)
- [限流应对最佳实践 ](../../raw/model-user-guide/use-cases/rate-limiting-best-practices.md)
- [借助大模型将文档转换为视频](../../raw/model-user-guide/use-cases/use-llm-to-convert-document-to-video.md)
- [显式缓存最佳实践](../../raw/model-user-guide/use-cases/explicit-cache-guide.md)
- [通过WebRTC使用qwen3.5-omni-plus-realtime实现实时通话](../../raw/model-user-guide/use-cases/best-practice-webrtc-omni-realtime.md)
- [通过AOQ使用qwen3.5-omni-plus-realtime实现实时通话](../../raw/model-user-guide/use-cases/best-practice-aoq-omni-realtime.md)
- [通过WebRTC使用多模态交互套件实现实时通话](../../raw/model-user-guide/use-cases/best-practice-webrtc-multimodal-dialog.md)
- [DeepSeek-阿里云](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/deepseek-api.md)
- [DeepSeek](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/deepseek-api-by-vanchin.md)
- [DeepSeek-硅基流动](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/siliconflow-deepseek-api.md)
- [Kimi-月之暗面](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/kimi-api-by-moonshot-ai.md)
- [Kimi](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/kimi-api.md)
- [GLM](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/glm.md)
- [GLM-智谱](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/glm-zhipu.md)
- [MiniMax](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/minimax-api.md)
- [MiniMax](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/minimax-api-by-minimax.md)
- [MiMo-小米](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/mimo.md)
- [Vidu视频生成Prompt指南](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/vidu-video-generation-prompt-guide.md)
- [Stepfun-阶跃星辰](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/stepfun.md)



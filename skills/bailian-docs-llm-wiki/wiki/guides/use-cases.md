# use cases

百炼平台提供覆盖文本、图像、视频、[多模态](../concepts/multimodal.md)及智能体等全栈能力的 AI 应用场景支持，面向开发者提供开箱即用的解决方案与灵活可定制的底层接口。本文档系统梳理主流 use cases 的模型支持、关键参数、调用方式及实践约束，帮助开发者快速选型并规避常见陷阱。

## 支持的模型/功能

百炼平台支持两类核心能力：**阿里云自研模型**（如 Qwen 系列、Wan2.7、HappyHorse）和**第三方直供模型**（如 DeepSeek、Kimi、GLM、MiniMax、MiMo、Stepfun）。其中：

- **视觉生成类**：`wan2.7`（文生/图生视频）、`happyhorse`（长视频生成）、`wanx`（万相文生图 V1/V2）是官方主推的[多模态](../concepts/multimodal.md)模型，深度集成于 [HappyHorse 打造一站式影视创作平台](../../raw/model-user-guide/use-cases/infinite-canvas.md) 方案中，支持节点式编排与无限画布。
- **深度研究类**：`qwen-deep-research` 是专用推理模型，用于自动规划研究路径、多源交叉验证与结构化报告生成，详见 [深度研究：生成你的独家洞察报告](../../raw/model-user-guide/use-cases/deep-research.md)。
- **教育辅学类**：`qwen3-vl-plus` 专为[多模态](../concepts/multimodal.md)理解优化，在 MathVista、MMMU 等评测中达 SOTA，支撑拍照解题与作业批改，见 [AI 解题 + 批改：推动课程教学智变](../../raw/model-user-guide/use-cases/ai-homework-helper.md)。
- **第三方模型**：DeepSeek、Kimi、GLM、MiniMax、MiMo、Stepfun 均通过 [OpenAI 兼容接口](../concepts/openai-compatible-interface.md)或 DashScope SDK 接入，但存在地域与功能差异。例如，所有第三方模型均仅在华北2（北京）地域提供完整服务（[DeepSeek](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/deepseek-api-by-vanchin.md)、[Kimi](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/kimi-api-by-moonshot-ai.md)、[GLM](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/glm-zhipu.md)、[MiniMax](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/minimax-api-by-minimax.md)、[MiMo](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/mimo.md)、[Stepfun](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/stepfun.md)），且普遍支持 `enable_thinking` 或 `reasoning_effort` 参数控制推理过程输出。

> **注意**：多个第三方模型文档（如文档16、19、21、23）声明了下架时间（2026年7月或10月），但推荐迁移目标不一致：DeepSeek 文档推荐 `qwen3.7-plus/max/flash`，而 Kimi 和 MiniMax 文档推荐相同三款模型；GLM 文档则推荐 `qwen3.7-plus/8-max/7-flash`。此处存在版本命名不一致（`qwen3.8-max` vs `qwen3.7-max`），建议以控制台实际可用模型为准。

## 关键参数

不同任务类型对应差异化参数体系：

- **文生图（WanX）**：核心参数为 `prompt`（正向提示词）与 `negative_prompt`（反向提示词），V2 版本额外支持 `prompt_extend`（默认 `true`，启用大模型智能改写）[文生图Prompt指南](../../raw/model-user-guide/use-cases/text-to-image-prompt.md)。
- **文生/图生视频（Wan2.7）**：采用结构化公式，基础为 `主体 + 场景 + 运动`，进阶需补充 `美学控制`（镜头、运镜）与 `风格化`；多镜头需显式标注 `镜头序号` 与 `时间戳`；声音控制需分离 `人声/音效/BGM` 描述 [文生视频/图生视频Prompt指南](../../raw/model-user-guide/use-cases/text-to-video-prompt.md)。
- **Vidu 视频生成**：强调“主体/场景+场景描述+环境描述+艺术风格/媒介”结构，并依赖特定关键词触发效果（如“大动态”、“固定镜头”、“宫崎骏风格”），见 [Vidu视频生成Prompt指南](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/vidu-video-generation-prompt-guide.md)。
- **思考模式模型**（DeepSeek/Kimi/GLM/MiMo/Stepfun）：均通过非标准字段控制，OpenAI SDK 需用 `extra_body` 传入 `{"enable_thinking": true}` 或 `{"reasoning_effort": "max"}`；Node.js SDK 可作为顶层参数直接传递。
- **显式缓存**：通过请求头 `X-DashScope-Wait-Timeout` 控制排队等待（仅对 Traffic Burst 有效），或在消息中注入 `cache_control` 标记实现确定性命中 [显式缓存最佳实践](../../raw/model-user-guide/use-cases/explicit-cache-guide.md)。

## 使用方式

开发者可通过三种主流路径接入：

1. **方案级一键部署**：适用于典型业务场景，如影视创作（[HappyHorse](../../raw/model-user-guide/use-cases/infinite-canvas.md)）、深度研究（[Qwen-Deep-Research](../../raw/model-user-guide/use-cases/deep-research.md)）、AI 客服（[构建 AI 智能体与工作流应用](../../raw/model-user-guide/use-cases/build-ai-applications-based-on-alibaba-cloud-model-studio.md)）、教育辅学（[AI 解题 + 批改](../../raw/model-user-guide/use-cases/ai-homework-helper.md)）。此类方案基于函数计算（FC）封装，15–30 分钟即可完成 Web 服务部署。
2. **SDK/API 直接调用**：适用于定制化开发，支持 [OpenAI 兼容接口](../concepts/openai-compatible-interface.md)（推荐）与 DashScope 原生 SDK。所有第三方模型均需配置地域专属 `base_url`（如华北2为 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`），且必须使用对应地域的 API Key。
3. **RAG 与 Agent 构建**：通过 LlamaIndex 集成知识库（[基于LlamaIndex构建RAG应用](../../raw/model-user-guide/use-cases/build-rag-applications-based-on-llamaindex.md)），或利用百炼工作流引擎编排复杂任务（如电商客服中的 RAG、Agent、对话流四类助手）。

## 限制和注意事项

- **地域锁定**：除通用模型外，所有第三方直供模型（DeepSeek/Kimi/GLM/MiniMax/MiMo/Stepfun）及部分实时通话能力（WebRTC、AOQ）均**仅限华北2（北京）地域使用**，跨地域调用将失败。
- **限流策略**：百炼 API 按 RPM（请求数/分钟）、TPM（[Token](../concepts/token.md)/分钟）、RPS/TPS（瞬时速率）及 Traffic Burst（增速）四维限流。突发流量应优先启用 `X-DashScope-Wait-Timeout` 头，而非简单重试 [限流应对最佳实践](../../raw/model-user-guide/use-cases/rate-limiting-best-practices.md)。
- **WebRTC 权限与代理**：浏览器端 WebRTC 调用受 CORS 限制，Demo 中需通过 `curl` 代理 SDP 交换；生产环境必须由业务后端代理 [通过WebRTC使用多模态交互套件实现实时通话](../../raw/model-user-guide/use-cases/best-practice-webrtc-multimodal-dialog.md)。
- **模型下架风险**：DeepSeek-v3 系列、Kimi-K2 系列、MiniMax-M2.1、GLM-4.x 等模型已明确标注下架日期（2026年7月或10月），迁移需提前规划。
- **输入格式约束**：文档转视频方案依赖 `FFmpeg` 与 `Marp` 工具链，且图片生成需 Chromium 渲染引擎；RAG 文件解析要求 `.pdf/.doc/.docx` 单文件 ≤100MB、≤1000 页 [借助大模型将文档转换为视频](../../raw/model-user-guide/use-cases/use-llm-to-convert-document-to-video.md)、[基于LlamaIndex构建RAG应用](../../raw/model-user-guide/use-cases/build-rag-applications-based-on-llamaindex.md)。

## 来源文档

- [HappyHorse 打造一站式影视创作平台](../../raw/model-user-guide/use-cases/infinite-canvas.md)
- [深度研究：生成你的独家洞察报告](../../raw/model-user-guide/use-cases/deep-research.md)
- [高效搭建 AI 智能体与工作流应用](../../raw/model-user-guide/use-cases/build-ai-applications-based-on-alibaba-cloud-model-studio.md)
- [AI 解题 + 批改：推动课程教学智变](../../raw/model-user-guide/use-cases/ai-homework-helper.md)
- [文生图Prompt指南](../../raw/model-user-guide/use-cases/text-to-image-prompt.md)
- [文生文Prompt指南](../../raw/model-user-guide/use-cases/prompt-engineering-guide.md)
- [文生视频/图生视频Prompt指南](../../raw/model-user-guide/use-cases/text-to-video-prompt.md)
- [基于LlamaIndex构建RAG应用](../../raw/model-user-guide/use-cases/build-rag-applications-based-on-llamaindex.md)
- [自定义模型调优、部署与评测](../../raw/model-user-guide/use-cases/model-training-best-practices.md)
- [借助大模型将文档转换为视频](../../raw/model-user-guide/use-cases/use-llm-to-convert-document-to-video.md)
- [显式缓存最佳实践](../../raw/model-user-guide/use-cases/explicit-cache-guide.md)
- [通过WebRTC使用多模态交互套件实现实时通话](../../raw/model-user-guide/use-cases/best-practice-webrtc-multimodal-dialog.md)
- [通过WebRTC使用qwen3.5-omni-plus-realtime实现实时通话](../../raw/model-user-guide/use-cases/best-practice-webrtc-omni-realtime.md)
- [通过AOQ使用qwen3.5-omni-plus-realtime实现实时通话](../../raw/model-user-guide/use-cases/best-practice-aoq-omni-realtime.md)
- [限流应对最佳实践 ](../../raw/model-user-guide/use-cases/rate-limiting-best-practices.md)
- [DeepSeek-阿里云](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/deepseek-api.md)
- [DeepSeek](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/deepseek-api-by-vanchin.md)
- [DeepSeek-硅基流动](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/siliconflow-deepseek-api.md)
- [Kimi](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/kimi-api.md)
- [Kimi-月之暗面](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/kimi-api-by-moonshot-ai.md)
- [GLM](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/glm.md)
- [GLM-智谱](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/glm-zhipu.md)
- [MiniMax](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/minimax-api.md)
- [MiniMax](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/minimax-api-by-minimax.md)
- [Vidu视频生成Prompt指南](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/vidu-video-generation-prompt-guide.md)
- [MiMo-小米](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/mimo.md)
- [Stepfun-阶跃星辰](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/stepfun.md)



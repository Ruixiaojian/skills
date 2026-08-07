# use cases

百炼平台提供覆盖文本、图像、视频、语音、[多模态](../concepts/multi-modal.md)及智能体等全栈能力的 AI 应用场景支持，面向开发者提供开箱即用的解决方案与可组合的底层能力。本文档系统梳理核心使用模式，涵盖模型支持范围、关键参数配置、典型调用方式及关键限制，帮助开发者快速选型并规避常见陷阱。

## 支持的模型/功能

百炼平台支持两类模型能力：**原生模型**（如 Qwen 系列、Wan2.7、HappyHorse）和**第三方直供模型**（如 DeepSeek、Kimi、GLM、MiniMax、MiMo、Stepfun）。所有模型均通过统一 API 接口（OpenAI 兼容或 DashScope SDK）调用，但部署地域与开通方式存在差异。

- **原生视觉模型**：`wan2.7`（文生视频/图生视频）、`happyhorse`（视频生成）、`qwen3-vl-plus`（[多模态](../concepts/multi-modal.md)理解）等，深度集成于[HappyHorse 打造一站式影视创作平台](../../raw/model-user-guide/use-cases/infinite-canvas.md)等端到端方案中。
- **第三方模型**：需按供应商单独开通，例如 `siliconflow/deepseek-v3.2`、`kimi/kimi-k3`、`ZHIPU/GLM-5.2`、`MiniMax/MiniMax-M2.7`、`xiaomi/mimo-v2.5-pro`、`stepfun/step-3.7-flash`。所有第三方模型当前**仅支持华北2（北京）地域**，且必须使用业务空间专属域名 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com`（见 [GLM-智谱](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/glm-zhipu.md) 文档），旧域名 `https://dashscope.aliyuncs.com` 已不推荐。
- **[多模态](../concepts/multi-modal.md)实时交互**：`qwen3.5-omni-plus-realtime` 支持 WebRTC 和 AOQ 两种接入方式，分别面向浏览器端与移动端硬件（如学习机、AI眼镜），详见 [通过WebRTC使用qwen3.5-omni-plus-realtime实现实时通话](../../raw/model-user-guide/use-cases/best-practice-webrtc-omni-realtime.md) 和 [通过AOQ使用qwen3.5-omni-plus-realtime实现实时通话](../../raw/model-user-guide/use-cases/best-practice-aoq-omni-realtime.md)。

> **注意**：多个第三方模型文档（如 [DeepSeek-阿里云](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/deepseek-api.md)、[Kimi](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/kimi-api.md)、[MiniMax](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/minimax-api.md)、[GLM](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/glm.md)）均声明部分旧版本将于 2026 年下架，并统一推荐迁移至 `qwen3.7-plus`/`qwen3.7-max` 等 Qwen 新系列模型。该迁移路径为平台级策略，开发者应优先选用 Qwen 系列以保障长期兼容性与服务稳定性。

## 关键参数

不同任务类型对应不同关键参数，需严格遵循规范：

- **文生文（LLM）**：核心为 `prompt`，推荐使用 [Prompt 框架](../../raw/model-user-guide/use-cases/prompt-engineering-guide.md)（背景/目的/风格/语气/受众/输出）结构化构造；第三方模型（如 DeepSeek、Kimi、GLM）普遍支持非标准参数 `enable_thinking` 或 `reasoning_effort` 控制思考模式，须通过 `extra_body`（Python OpenAI SDK）传入。
- **文生图/图生图**：`prompt`（正向描述）与 `negative_prompt`（反向排除）为必需参数；`wan2.7` 支持 `prompt_extend: true` 启用大模型智能扩写，强烈推荐保持默认开启。
- **文生视频/图生视频**：基础公式为 `主体 + 场景 + 运动`；进阶需补充 `美学控制`（镜头/运镜/光线）与 `风格化`；多镜头叙事需显式使用 `镜头序号 + 时间戳 + 分镜内容` 结构（见 [文生视频/图生视频Prompt指南](../../raw/model-user-guide/use-cases/text-to-video-prompt.md)）。
- **Vidu 视频生成**：采用 `主体/场景+场景描述+环境描述+艺术风格/媒介` 公式，强调氛围词（如“宁静”、“温馨浪漫”）在句首、景物、收束处重复强化；运镜控制（如“镜头推”、“固定镜头”）需用明确动词短语（见 [Vidu视频生成Prompt指南](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/vidu-video-generation-prompt-guide.md)）。
- **缓存与流控**：显式缓存依赖 `cache_control` 标记（由 Claude Code、OpenCode 等工具自动注入）；限流应对首选 `X-DashScope-Wait-Timeout` 请求头实现服务端排队（见 [限流应对最佳实践](../../raw/model-user-guide/use-cases/rate-limiting-best-practices.md)）。

## 使用方式

- **端到端方案**：直接部署预置应用，如 [HappyHorse 影视创作平台](../../raw/model-user-guide/use-cases/infinite-canvas.md)（基于函数计算 + Wan2.7/ HappyHorse）、[AI 解题 + 批改](../../raw/model-user-guide/use-cases/ai-homework-helper.md)（基于函数计算 + qwen3-vl-plus）、[深度研究报告生成](../../raw/model-user-guide/use-cases/deep-research.md)（基于函数计算 + Qwen-Deep-Research）。
- **RAG 应用**：通过 LlamaIndex 集成百炼知识库服务，使用 `DashScopeCloudIndex` 创建索引，`DashScopeCloudRetriever` 获取检索器（见 [基于LlamaIndex构建RAG应用](../../raw/model-user-guide/use-cases/build-rag-applications-based-on-llamaindex.md)）。
- **文档转视频**：需本地安装 FFmpeg、Marp 及 Chromium，通过 Python 脚本完成文档切片、图文生成、语音合成、字幕嵌入与视频合成全流程（见 [借助大模型将文档转换为视频](../../raw/model-user-guide/use-cases/use-llm-to-convert-document-to-video.md)）。
- **实时音视频交互**：WebRTC 方式需浏览器获取媒体流并建立 `RTCPeerConnection`；AOQ 方式需在 Android/iOS/HarmonyOS 工程中集成 SDK 并申请麦克风/摄像头权限（见 [通过WebRTC使用多模态交互套件](../../raw/model-user-guide/use-cases/best-practice-webrtc-multimodal-dialog.md) 和 [通过AOQ使用qwen3.5-omni-plus-realtime](../../raw/model-user-guide/use-cases/best-practice-aoq-omni-realtime.md)）。

## 限制和注意事项

- **地域与域名约束**：所有第三方模型（DeepSeek、Kimi、GLM、MiniMax、MiMo、Stepfun）**仅限华北2（北京）地域**，且必须使用业务空间专属域名 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com`，否则调用失败。
- **[Token](../concepts/token.md) 与限流**：API 按请求数（RPM/RPS）和 [Token](../concepts/token.md) 用量（TPM/TPS）双重限流；突发流量（Traffic Burst）触发时，`X-DashScope-Wait-Timeout` 是最简有效解法，但需同步延长客户端超时时间（见 [限流应对最佳实践](../../raw/model-user-guide/use-cases/rate-limiting-best-practices.md)）。
- **模型下架风险**：`deepseek-v3.x`、`kimi-k2-*`、`glm-4.*`、`MiniMax-M2.1` 等旧版模型已明确标注下架日期（2026年7月或10月），新项目应避免选用。
- **WebRTC CORS 限制**：浏览器端无法直接发起 SDP 交换请求，Demo 中需通过 `curl` 命令代理；生产环境必须由业务后端代理完成连接建立（见 [通过WebRTC使用多模态交互套件](../../raw/model-user-guide/use-cases/best-practice-webrtc-multimodal-dialog.md)）。
- **显式缓存适用场景**：适用于高频复用相同 Prompt 的工业级 Agent（如压缩、recap 场景），对动态变化的上下文（如含当前目录、日期的 system [prompt](prompt.md)）需通过 `--exclude-dynamic-system-prompt-sections` 等参数提升跨会话命中率（见 [显式缓存最佳实践](../../raw/model-user-guide/use-cases/explicit-cache-guide.md)）。

## 来源文档

- [HappyHorse 打造一站式影视创作平台](../../raw/model-user-guide/use-cases/infinite-canvas.md)
- [高效搭建 AI 智能体与工作流应用](../../raw/model-user-guide/use-cases/build-ai-applications-based-on-alibaba-cloud-model-studio.md)
- [深度研究：生成你的独家洞察报告](../../raw/model-user-guide/use-cases/deep-research.md)
- [AI 解题 + 批改：推动课程教学智变](../../raw/model-user-guide/use-cases/ai-homework-helper.md)
- [文生文Prompt指南](../../raw/model-user-guide/use-cases/prompt-engineering-guide.md)
- [文生图Prompt指南](../../raw/model-user-guide/use-cases/text-to-image-prompt.md)
- [文生视频/图生视频Prompt指南](../../raw/model-user-guide/use-cases/text-to-video-prompt.md)
- [基于LlamaIndex构建RAG应用](../../raw/model-user-guide/use-cases/build-rag-applications-based-on-llamaindex.md)
- [借助大模型将文档转换为视频](../../raw/model-user-guide/use-cases/use-llm-to-convert-document-to-video.md)
- [自定义模型调优、部署与评测](../../raw/model-user-guide/use-cases/model-training-best-practices.md)
- [显式缓存最佳实践](../../raw/model-user-guide/use-cases/explicit-cache-guide.md)
- [限流应对最佳实践 ](../../raw/model-user-guide/use-cases/rate-limiting-best-practices.md)
- [通过WebRTC使用多模态交互套件实现实时通话](../../raw/model-user-guide/use-cases/best-practice-webrtc-multimodal-dialog.md)
- [通过WebRTC使用qwen3.5-omni-plus-realtime实现实时通话](../../raw/model-user-guide/use-cases/best-practice-webrtc-omni-realtime.md)
- [通过AOQ使用qwen3.5-omni-plus-realtime实现实时通话](../../raw/model-user-guide/use-cases/best-practice-aoq-omni-realtime.md)
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



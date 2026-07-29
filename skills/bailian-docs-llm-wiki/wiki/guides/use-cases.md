# use cases

百炼平台的 use cases 文档聚焦于开发者如何将大模型能力落地为实际业务应用。它覆盖从智能体构建、多模态创作到深度研究、教育辅学等典型场景，并提供模型调用、提示工程、缓存与限流等关键工程实践。本文档不介绍抽象概念，而是提炼可直接复用的技术路径与配置要点。

## 支持的模型/功能

百炼支持两类核心能力：**原生模型服务**与**第三方模型集成**。原生模型包括 Qwen 系列（如 `qwen3-vl-plus` 用于解题批改 [AI 解题 + 批改：推动课程教学智变](../../raw/model-user-guide/use-cases/ai-homework-helper.md)）、Wan2.7/HappyHorse 视觉模型（用于影视创作 [HappyHorse 打造一站式影视创作平台](../../raw/model-user-guide/use-cases/infinite-canvas.md)）及 Qwen-Deep-Research（用于结构化报告生成 [深度研究：生成你的独家洞察报告](../../raw/model-user-guide/use-cases/deep-research.md)）。第三方模型通过 [OpenAI 兼容接口](../concepts/openai-compatible-interface.md)或 DashScope SDK 接入，涵盖 DeepSeek（`deepseek-v4-pro`）、Kimi（`kimi/kimi-k3`）、MiniMax（`MiniMax-M2.7`）、GLM（`ZHIPU/GLM-5.2`）、MiMo（`xiaomi/mimo-v2.5-pro`）和 Step（`stepfun/step-3.7-flash`）等。> **注意**：多个第三方模型文档（如 [DeepSeek-阿里云](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/deepseek-api.md)、[Kimi](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/kimi-api.md)、[MiniMax](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/minimax-api.md)）均声明部分旧版本模型将于 2026 年下架，但未统一标注推荐替代模型的兼容性差异，开发者需自行验证 `qwen3.7-plus` 等替代方案在具体任务上的表现。

## 关键参数

不同模态任务依赖特定参数控制输出质量：
- **文生文**：核心是 Prompt 设计，推荐使用结构化框架（背景/目的/风格/语气/受众/输出），并利用平台 [Prompt一键优化工具](../../raw/model-user-guide/use-cases/prompt-engineering-guide.md) 进行扩写。
- **文生图/图生图**：必需 `prompt`（正向描述）与 `negative_prompt`（反向排除），V2 版本支持 `prompt_extend: true` 启用智能改写；公式建议按“主体+场景+风格”（基础）或“主体描述+场景描述+风格+镜头语言+氛围词+细节修饰”（进阶）组织。
- **文生视频/图生视频**：强调运动描述（如“缓慢移动”、“猛烈摇摆”）与美学控制（运镜、景别、光线），Wan2.7 支持多镜头公式（含时间戳与分镜内容）及声音公式（人声/音效/BGM）。
- **第三方模型通用参数**：`enable_thinking`（开启思考模式，返回 `reasoning_content`）与 `reasoning_effort`（控制推理深度）是非标准但广泛支持的参数，需通过 `extra_body`（Python SDK）或顶层字段（Node.js SDK）传入。

## 使用方式

典型工作流包含四步：**准备 → 部署 → 调用 → 优化**。
- **准备**：知识库场景需先通过 [DashScopeParse](../../raw/model-user-guide/use-cases/build-rag-applications-based-on-llamaindex.md) 解析 PDF/DOCX 文件，并上传至百炼知识库；视觉/视频任务需按指南构造高质量 Prompt。
- **部署**：自定义模型必须完成“调优→部署→评测”闭环，部署后方可调用；第三方模型需在控制台开通对应服务（如 [Kimi-月之暗面](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/kimi-api-by-moonshot-ai.md) 或 [GLM-智谱](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/glm-zhipu.md)），并配置地域专属域名（如 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com`）以获得更优性能。
- **调用**：推荐使用 OpenAI 兼容 SDK（如 `openai==1.40.0+`），设置 `base_url` 指向百炼兼容端点，并传入 `model` 名称（如 `"siliconflow/deepseek-v3.2"`）；流式响应需处理 `reasoning_content` 与 `content` 字段分离的 chunk。
- **优化**：高频固定 Prompt 场景应启用 [显式缓存](../../raw/model-user-guide/use-cases/explicit-cache-guide.md)，通过 `cache_control` 标记实现确定性命中；突发流量需配置 `X-DashScope-Wait-Timeout` 请求头启用服务端排队。

## 限制和注意事项

- **限流机制**：百炼 API 按 RPM（请求数/分钟）、TPM（[Token](../concepts/token.md) 数/分钟）、RPS/TPS（瞬时速率）及 Traffic Burst（增速）四维限流。`429` 错误需结合 [错误诊断表](../../raw/model-user-guide/use-cases/rate-limiting-best-practices.md) 定位维度，而非简单重试。
- **地域与模型绑定**：多数第三方模型（DeepSeek、Kimi、MiniMax、GLM、MiMo、Stepfun）仅在华北2（北京）地域可用，且需使用该地域 API Key 及业务空间 ID 构造 URL；Vidu 视频生成等服务亦有地域限制。
- **模型生命周期**：第三方模型存在明确下架计划（如 DeepSeek 系列 2026-10-10、Kimi/MiMo/MiniMax/GLM 系列 2026-07-09），文档中虽给出迁移建议，但未说明旧模型停服后历史调用数据的兼容性策略。
- **缓存与 Agent**：显式缓存对工业级 Agent 的长上下文管理（如 recap、system reminder）极为有效，但需注意 Claude Code 等工具默认注入动态信息（如 git 状态），可能降低跨会话命中率，需通过 `--exclude-dynamic-system-prompt-sections` 参数规避。

## 来源文档

- [高效搭建 AI 智能体与工作流应用](../../raw/model-user-guide/use-cases/build-ai-applications-based-on-alibaba-cloud-model-studio.md)
- [HappyHorse 打造一站式影视创作平台](../../raw/model-user-guide/use-cases/infinite-canvas.md)
- [深度研究：生成你的独家洞察报告](../../raw/model-user-guide/use-cases/deep-research.md)
- [AI 解题 + 批改：推动课程教学智变](../../raw/model-user-guide/use-cases/ai-homework-helper.md)
- [文生文Prompt指南](../../raw/model-user-guide/use-cases/prompt-engineering-guide.md)
- [文生图Prompt指南](../../raw/model-user-guide/use-cases/text-to-image-prompt.md)
- [文生视频/图生视频Prompt指南](../../raw/model-user-guide/use-cases/text-to-video-prompt.md)
- [基于LlamaIndex构建RAG应用](../../raw/model-user-guide/use-cases/build-rag-applications-based-on-llamaindex.md)
- [自定义模型调优、部署与评测](../../raw/model-user-guide/use-cases/model-training-best-practices.md)
- [借助大模型将文档转换为视频](../../raw/model-user-guide/use-cases/use-llm-to-convert-document-to-video.md)
- [限流应对最佳实践 ](../../raw/model-user-guide/use-cases/rate-limiting-best-practices.md)
- [显式缓存最佳实践](../../raw/model-user-guide/use-cases/explicit-cache-guide.md)
- [DeepSeek-阿里云](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/deepseek-api.md)
- [DeepSeek-硅基流动](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/siliconflow-deepseek-api.md)
- [Kimi-月之暗面](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/kimi-api-by-moonshot-ai.md)
- [DeepSeek](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/deepseek-api-by-vanchin.md)
- [Kimi](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/kimi-api.md)
- [MiniMax](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/minimax-api.md)
- [GLM-智谱](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/glm-zhipu.md)
- [GLM](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/glm.md)
- [MiniMax](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/minimax-api-by-minimax.md)
- [Vidu视频生成Prompt指南](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/vidu-video-generation-prompt-guide.md)
- [MiMo-小米](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/mimo.md)
- [Stepfun-阶跃星辰](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/stepfun.md)



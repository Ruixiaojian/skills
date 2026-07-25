# use cases

百炼平台的 use cases 覆盖从多模态内容生成、智能体构建到专业领域深度分析的完整技术谱系。本文档面向开发者，系统梳理平台支持的核心能力、关键参数配置、标准使用方式及实际部署限制，所有信息均基于官方技术文档提炼，不包含营销性描述。

## 支持的模型/功能

百炼提供两类核心能力：**原生模型服务**与**第三方模型集成**。原生模型包括 `qwen3-vl-plus`（用于AI解题与批改）、`wan2.7`（文生视频/图生视频）、`qwen-deep-research`（深度研究）等，均通过统一 API 接口调用；第三方模型则通过 OpenAI 兼容协议或 DashScope SDK 接入，涵盖 DeepSeek、Kimi、GLM、MiniMax、Vidu、Stepfun 和 MiMo 等系列 [DeepSeek-阿里云](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/deepseek-api.md)、[Kimi-月之暗面](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/kimi-api-by-moonshot-ai.md)、[Vidu视频生成Prompt指南](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/vidu-video-generation-prompt-guide.md)。所有第三方模型均需在华北2（北京）地域开通并配置对应 Workspace ID 或业务空间，部分模型（如硅基流动版 DeepSeek）明确要求使用专属地域接入地址以启用长上下文等高级特性。

> **注意**：多个第三方模型文档存在下架时间冲突。例如，`deepseek-v3` 系列模型下架时间为 2026年10月10日 [DeepSeek-阿里云](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/deepseek-api.md)，而 `kimi-k2-instruct` 和 `glm-4.6` 下架时间为 2026年7月9日 [Kimi](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/kimi-api.md)、[GLM](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/glm.md)。开发者应优先迁移至推荐的 `qwen3.7-plus` 等 Qwen 系列模型，避免依赖即将下线的旧版本。

## 关键参数

不同任务类型的关键参数差异显著：
- **文生文**：核心为 `prompt` 结构设计，推荐使用 Prompt 框架（背景/目的/风格/语气/受众/输出）提升效果 [文生文Prompt指南](../../raw/model-user-guide/use-cases/prompt-engineering-guide.md)；
- **文生图/图生图**：`prompt`（正向提示词）与 `negative_prompt`（反向提示词）为必需参数，`prompt_extend`（是否启用大模型智能改写）默认开启且强烈推荐；
- **文生视频**：除基础 `prompt` 外，`wan2.7` 支持 `shot_type`（单/多镜头）、`prompt_extend` 及声音控制参数；但需注意 `wan2.7` 已不再支持 `shot_type` 显式指定，应改用“总体描述 + 镜头序号 + 时间戳 + 分镜内容”的多镜头公式；
- **第三方模型通用参数**：`enable_thinking`（开启思考模式）、`reasoning_effort`（控制推理深度）为非 OpenAI 标准参数，需通过 `extra_body`（Python）或顶层参数（Node.js）传入；
- **缓存与限流**：显式缓存依赖 `cache_control` 标记；限流应对需设置 `X-DashScope-Wait-Timeout` 请求头实现服务端排队。

## 使用方式

标准调用流程为：开通模型 → 获取 API Key → 配置环境变量 → 构造请求。具体方式分三类：
- **可视化编排**：适用于影视创作等复杂工作流，通过 HappyHorse 无限画布节点式拖拽组合 Wan2.7 图像与视频生成能力 [HappyHorse 打造一站式影视创作平台](../../raw/model-user-guide/use-cases/infinite-canvas.md)；
- **代码集成**：主流语言 SDK 均支持 [OpenAI 兼容接口](../concepts/openai-compatible-interface.md)（`base_url` 需按地域配置）和 DashScope 原生接口，示例代码覆盖 Python/Node.js 流式与非流式调用；
- **RAG 应用构建**：基于 LlamaIndex，通过 `DashScopeCloudIndex` 创建知识库，再调用 `as_query_engine` 实现[检索增强生成](../concepts/rag.md) [基于LlamaIndex构建RAG应用](../../raw/model-user-guide/use-cases/build-rag-applications-based-on-llamaindex.md)。

所有方案均支持函数计算（FC）一键部署，典型耗时 15–30 分钟，费用在免费试用额度内可覆盖多数体验场景。

## 限制和注意事项

- **地域与权限绑定**：第三方模型（DeepSeek、Kimi、GLM、MiniMax、Stepfun、MiMo）普遍限定华北2（北京）地域使用，且需对应地域的 API Key 和 Workspace ID，跨地域调用将失败；
- **输入约束**：`DashScopeParse` 文档解析器要求单个文件 ≤100MB 且 ≤1000 页；`qwen3-vl-plus` 解题场景支持 33 种语言，但图像理解精度受原始图片质量影响；
- **限流策略**：API 同时受 RPM（每分钟请求数）、TPM（每分钟 [Token](../concepts/token.md) 数）和 Traffic Burst（流量增速）三重限制，单纯重试无效，必须采用服务端排队（`X-DashScope-Wait-Timeout`）、令牌桶或消息队列等主动流控策略 [限流应对最佳实践](../../raw/model-user-guide/use-cases/rate-limiting-best-practices.md)；
- **缓存适用性**：显式缓存仅对完全相同的 `prompt` 输入保证 100% 命中，Agent 场景中动态 system [prompt](prompt.md)（如含当前目录、日期）会降低跨会话命中率，建议使用 `--exclude-dynamic-system-prompt-sections` 参数优化；
- **模型生命周期**：所有第三方模型均标注明确下架时间，开发者须定期核查文档更新，及时迁移至推荐替代模型。

## 来源文档

- [HappyHorse 打造一站式影视创作平台](../../raw/model-user-guide/use-cases/infinite-canvas.md)
- [高效搭建 AI 智能体与工作流应用](../../raw/model-user-guide/use-cases/build-ai-applications-based-on-alibaba-cloud-model-studio.md)
- [AI 解题 + 批改：推动课程教学智变](../../raw/model-user-guide/use-cases/ai-homework-helper.md)
- [文生文Prompt指南](../../raw/model-user-guide/use-cases/prompt-engineering-guide.md)
- [文生图Prompt指南](../../raw/model-user-guide/use-cases/text-to-image-prompt.md)
- [文生视频/图生视频Prompt指南](../../raw/model-user-guide/use-cases/text-to-video-prompt.md)
- [基于LlamaIndex构建RAG应用](../../raw/model-user-guide/use-cases/build-rag-applications-based-on-llamaindex.md)
- [自定义模型调优、部署与评测](../../raw/model-user-guide/use-cases/model-training-best-practices.md)
- [借助大模型将文档转换为视频](../../raw/model-user-guide/use-cases/use-llm-to-convert-document-to-video.md)
- [限流应对最佳实践 ](../../raw/model-user-guide/use-cases/rate-limiting-best-practices.md)
- [显式缓存最佳实践](../../raw/model-user-guide/use-cases/explicit-cache-guide.md)
- [深度研究：生成你的独家洞察报告](../../raw/model-user-guide/use-cases/deep-research.md)
- [DeepSeek-阿里云](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/deepseek-api.md)
- [DeepSeek-硅基流动](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/siliconflow-deepseek-api.md)
- [DeepSeek](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/deepseek-api-by-vanchin.md)
- [Kimi](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/kimi-api.md)
- [GLM](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/glm.md)
- [GLM-智谱](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/glm-zhipu.md)
- [MiniMax](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/minimax-api-by-minimax.md)
- [Vidu视频生成Prompt指南](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/vidu-video-generation-prompt-guide.md)
- [Kimi-月之暗面](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/kimi-api-by-moonshot-ai.md)
- [Stepfun-阶跃星辰](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/stepfun.md)
- [MiniMax](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/minimax-api.md)
- [MiMo-小米](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/mimo.md)



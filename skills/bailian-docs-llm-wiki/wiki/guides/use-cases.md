# use cases

百炼平台提供覆盖文本、图像、视频、多模态及智能体工作流的全栈AI能力，支持从Prompt工程、模型调用、RAG构建到端到端应用部署的完整开发链路。开发者可基于预置模型快速验证场景，也可通过自定义训练、缓存优化与限流治理实现生产级落地。

## 支持的模型/功能

百炼支持多类原生与第三方大模型，并提供配套的视觉生成、深度研究、智能教学等垂直能力套件：

- **文本模型**：Qwen系列（如 `qwen3.7-max`、`qwen3-vl-plus`）、DeepSeek（`deepseek-v4-pro`）、Kimi（`kimi/kimi-k2.6`）、GLM（`ZHIPU/GLM-5.2`）、MiniMax（`MiniMax/MiniMax-M2.7`）、MiMo（`xiaomi/mimo-v2.5-pro`）、Step（`stepfun/step-3.7-flash`）等；所有第三方模型均需注意[下架时间](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/deepseek-api.md)，例如 `deepseek-v3` 系列将于 2026 年 7 月 9 日下架。
- **视觉模型**：Wan2.7 图像/视频生成、HappyHorse 视频生成、Qwen3-VL 多模态理解（用于解题批改），详见 [HappyHorse 打造一站式影视创作平台](../../raw/model-user-guide/use-cases/infinite-canvas.md)。
- **专用能力套件**：
  - 深度研究：`Qwen-Deep-Research` 自动规划检索路径、多源交叉验证并生成结构化报告，适用于投资尽调与战略分析场景 [深度研究：生成你的独家洞察报告](../../raw/model-user-guide/use-cases/deep-research.md)；
  - AI 教学：基于 `qwen3-vl-plus` 实现拍照解题、自动批改与题库生成，支持 33 种语言 [AI 解题 + 批改：推动课程教学智变](../../raw/model-user-guide/use-cases/ai-homework-helper.md)；
  - 智能体与工作流：支持 RAG（通过 LlamaIndex 集成知识库）、自主决策 Agent 及复杂对话流编排 [高效搭建 AI 智能体与工作流应用](../../raw/model-user-guide/use-cases/build-ai-applications-based-on-alibaba-cloud-model-studio.md)。

> **注意**：文档中提及的 `qwen3-vl-plus` 在 [AI 解题 + 批改](../../raw/model-user-guide/use-cases/ai-homework-helper.md) 中明确为视觉模型，但部分第三方集成文档（如 Kimi、MiniMax）未说明其多模态能力支持情况，实际调用前请以控制台模型详情页为准。

## 关键参数

不同任务类型依赖特定参数组合，需严格遵循接口规范：

- **Prompt 工程**：
  - 文生图：使用 `prompt`（正向）与 `negative_prompt`（反向），V2 版本支持 `prompt_extend: true` 启用大模型智能扩写 [文生图Prompt指南](../../raw/model-user-guide/use-cases/text-to-image-prompt.md)；
  - 文生视频/图生视频：采用结构化公式，如基础公式 `主体 + 场景 + 运动`，进阶公式需补充 `美学控制` 与 `风格化`；多镜头需显式指定 `镜头序号` 与 `时间戳` [文生视频/图生视频Prompt指南](../../raw/model-user-guide/use-cases/text-to-video-prompt.md)；
  - Vidu 视频生成：强调句式简洁、避免主体分散，推荐按 `"主体/场景+场景描述+环境描述+艺术风格/媒介"` 结构组织提示词 [Vidu视频生成Prompt指南](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/vidu-video-generation-prompt-guide.md)。

- **模型推理**：
  - 思考模式：DeepSeek、Kimi、GLM、MiMo、Step 等均支持 `enable_thinking` 参数（非 OpenAI 标准），需通过 `extra_body`（Python SDK）或顶层字段（Node.js）传入；
  - 缓存控制：Anthropic 协议兼容工具（Claude Code、OpenCode、OpenClaw）默认注入 `cache_control`，支持对 system [prompt](prompt.md) 与最近 user message 进行显式缓存标记 [显式缓存最佳实践](../../raw/model-user-guide/use-cases/explicit-cache-guide.md)。

## 使用方式

- **快速启动**：所有方案均提供“15 分钟部署”指引，依赖函数计算（FC）或 ECS 构建 Web 服务，开箱即用（如深度研究方案、AI 教学方案）；
- **SDK 调用**：
  - OpenAI 兼容模式：统一使用 `base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"`，模型名按供应商前缀格式（如 `siliconflow/deepseek-v3.2`、`kimi/kimi-k2.6`）；
  - DashScope 原生 SDK：无需配置 `base_url`（华北2默认），但跨地域需手动设置 `base_http_api_url`（如德国法兰克福需设为 `https://{WorkspaceId}.eu-central-1.maas.aliyuncs.com/api/v1`）；
- **RAG 构建**：通过 LlamaIndex 集成百炼知识库，使用 `DashScopeCloudIndex` 创建索引，`DashScopeCloudRetriever` 获取检索器，`as_query_engine` 绑定 LLM [基于LlamaIndex构建RAG应用](../../raw/model-user-guide/use-cases/build-rag-applications-based-on-llamaindex.md)；
- **文档转视频**：需本地安装 FFmpeg 与 Marp，依赖浏览器渲染生成演示文稿图片，再合成带语音与字幕的最终视频 [借助大模型将文档转换为视频](../../raw/model-user-guide/use-cases/use-llm-to-convert-document-to-video.md)。

## 限制和注意事项

- **限流策略**：百炼 API 按主账号维度、按模型独立限制 RPM/TPM、RPS/TPS 及 Traffic Burst。突发流量推荐优先启用 `X-DashScope-Wait-Timeout` 请求头实现服务端排队，而非简单重试 [限流应对最佳实践](../../raw/model-user-guide/use-cases/rate-limiting-best-practices.md)；
- **地域约束**：第三方模型（DeepSeek、Kimi、GLM、MiniMax、MiMo、Step）多数仅在华北2（北京）可用，开通服务与获取 API Key 必须匹配该地域；部分模型（如 Kimi、GLM）在新加坡、美国等地域亦支持，但需替换 `WorkspaceId` 并配置对应 `base_url`；
- **缓存成本**：显式缓存首次写入产生标准价格 25% 额外开销，后续命中节省 90% 成本；但 Claude Code 默认在 system [prompt](prompt.md) 中嵌入动态信息（如当前目录、日期），会降低跨会话命中率，建议启动时加 `--exclude-dynamic-system-prompt-sections` 参数 [显式缓存最佳实践](../../raw/model-user-guide/use-cases/explicit-cache-guide.md)；
- **模型生命周期**：多个第三方模型（DeepSeek、Kimi、GLM、MiniMax）已明确标注下架时间（2026年7月9日），文档中均给出迁移建议（统一推荐 `qwen3.7-plus` / `qwen3.7-max` / `qwen3.6-flash`），开发者应提前规划升级路径。

## 来源文档

- [HappyHorse 打造一站式影视创作平台](../../raw/model-user-guide/use-cases/infinite-canvas.md)
- [高效搭建 AI 智能体与工作流应用](../../raw/model-user-guide/use-cases/build-ai-applications-based-on-alibaba-cloud-model-studio.md)
- [深度研究：生成你的独家洞察报告](../../raw/model-user-guide/use-cases/deep-research.md)
- [文生文Prompt指南](../../raw/model-user-guide/use-cases/prompt-engineering-guide.md)
- [AI 解题 + 批改：推动课程教学智变](../../raw/model-user-guide/use-cases/ai-homework-helper.md)
- [文生视频/图生视频Prompt指南](../../raw/model-user-guide/use-cases/text-to-video-prompt.md)
- [基于LlamaIndex构建RAG应用](../../raw/model-user-guide/use-cases/build-rag-applications-based-on-llamaindex.md)
- [自定义模型调优、部署与评测](../../raw/model-user-guide/use-cases/model-training-best-practices.md)
- [借助大模型将文档转换为视频](../../raw/model-user-guide/use-cases/use-llm-to-convert-document-to-video.md)
- [限流应对最佳实践 ](../../raw/model-user-guide/use-cases/rate-limiting-best-practices.md)
- [显式缓存最佳实践](../../raw/model-user-guide/use-cases/explicit-cache-guide.md)
- [文生图Prompt指南](../../raw/model-user-guide/use-cases/text-to-image-prompt.md)
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



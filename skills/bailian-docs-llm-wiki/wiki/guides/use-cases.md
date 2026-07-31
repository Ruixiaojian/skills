# use cases

阿里云百炼平台提供覆盖文本、图像、视频、语音及[多模态](../concepts/multi-modal.md)的全栈式 AI 能力，支持从简单 Prompt 调用到复杂工作流编排的多样化应用场景。开发者可基于预置模型快速验证业务逻辑，也可通过自定义模型、RAG、Agent 编排与实时音视频交互等能力构建生产级应用。所有方案均以函数计算、知识库、WebRTC 等标准化基础设施为底座，兼顾开箱即用性与工程可扩展性。

## 支持的模型/功能

百炼支持两类核心能力：**原生模型服务**与**第三方模型集成**。

- **原生模型**：包括 Qwen 系列（如 `qwen3-vl-plus` 用于解题批改 [原文标题](../../raw/model-user-guide/use-cases/ai-homework-helper.md)）、Wan2.7 / HappyHorse（用于文生视频与无限画布影视创作 [原文标题](../../raw/model-user-guide/use-cases/infinite-canvas.md)）、Qwen-Deep-Research（用于深度情报分析 [原文标题](../../raw/model-user-guide/use-cases/deep-research.md)）等。这些模型深度集成于百炼控制台，支持一键部署、可视化编排与资产统一管理。

- **第三方模型**：通过 [OpenAI 兼容接口](../concepts/openai-compatible-api.md)或 DashScope SDK 接入 DeepSeek、Kimi、GLM、MiniMax、MiMo、Stepfun 等厂商模型。各模型开通方式、地域限制与参数用法存在差异，例如 DeepSeek 系列需通过 `extra_body` 传入 `enable_thinking`，而 Kimi-K3 则使用 `reasoning_effort` 控制思考深度 [原文标题](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/kimi-api-by-moonshot-ai.md)。

> **注意**：多个第三方模型文档（如 DeepSeek、Kimi、GLM）均声明部分旧版本将于 2026 年下架，并统一推荐迁移至 `qwen3.7-plus`/`qwen3.7-max`。但各文档未明确说明迁移是否影响现有 API 兼容性或 [Token](../concepts/token.md) 计费规则，建议以[模型市场](https://bailian.console.aliyun.com/#/model-market)最新公告为准。

## 关键参数

不同模态任务依赖特定参数组合，需严格遵循接口规范：

- **文生文**：核心为 `prompt`，推荐采用结构化 Prompt 框架（背景/目的/风格/语气/受众/输出）提升可控性；`system` 指令需明确角色与约束 [原文标题](../../raw/model-user-guide/use-cases/prompt-engineering-guide.md)。

- **文生图/图生图**：`prompt`（正向描述）与 `negative_prompt`（反向过滤）为必需；V2 版本支持 `prompt_extend: true` 启用大模型智能扩写，显著降低提示词编写门槛 [原文标题](../../raw/model-user-guide/use-cases/text-to-image-prompt.md)。

- **文生视频/图生视频**：除基础 `prompt` 外，`wan2.7` 支持 `shot_type`（已弃用）、多镜头时间戳语法及 `sound` 描述（人声/音效/BGM）；Vidu 模型则需显式指定运镜关键词（如 `镜头推近`、`固定镜头`）和风格词（如 `宫崎骏风格`）[原文标题](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/vidu-video-generation-prompt-guide.md)。

- **实时音视频**：WebRTC 模式下必须启用 `server_vad`（服务端语音活动检测），不支持手动 VAD；AOQ SDK 需通过 AppServer 获取短期 [Token](../concepts/token.md) 实现鉴权 [原文标题](../../raw/model-user-guide/use-cases/best-practice-aoq-omni-realtime.md)。

## 使用方式

典型接入路径分为三层：

1. **低代码编排**：适用于影视创作、电商客服等场景。通过「无限画布」节点拖拽连接 Wan2.7 图像生成与 HappyHorse 视频生成模块，或在百炼控制台配置 RAG 知识库并绑定 `qwen-max` 模型构建问答引擎 [原文标题](../../raw/model-user-guide/use-cases/infinite-canvas.md)。

2. **SDK/API 直接调用**：适用于定制化开发。Python/Node.js 客户端需配置 `base_url`（区分地域与业务空间 ID）、`api_key` 及模型名（如 `siliconflow/deepseek-v3.2`）；流式响应需处理 `reasoning_content` 与 `content` 字段分离的 chunk 数据 [原文标题](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/siliconflow-deepseek-api.md)。

3. **框架集成**：LlamaIndex 用户可直接使用 `DashScopeCloudIndex` 加载知识库，`DashScopeCloudRetriever` 执行检索，无需自行实现向量存储与分块逻辑 [原文标题](../../raw/model-user-guide/use-cases/build-rag-applications-based-on-llamaindex.md)。

## 限制和注意事项

- **限流策略**：百炼按 RPM（请求/分钟）、TPM（[Token](../concepts/token.md)/分钟）及 Traffic Burst（瞬时增速）三维度限流。突发流量应优先启用 `X-DashScope-Wait-Timeout` 请求头实现服务端排队，而非客户端重试 [原文标题](../../raw/model-user-guide/use-cases/rate-limiting-best-practices.md)。

- **缓存机制**：显式缓存（`cache_control`）仅对 Anthropic 协议兼容的工具（Claude Code、OpenCode、OpenClaw）自动生效，且需确保 `baseURL` 指向 `/apps/anthropic` 路径；普通 OpenAI 兼容调用不支持该特性。

- **地域与域名约束**：第三方模型（DeepSeek、Kimi、GLM、MiniMax 等）多数仅支持华北2（北京）地域，且强烈建议使用业务空间专属域名 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com` 替代通用 `dashscope.aliyuncs.com`，以获得更高稳定性与性能 [原文标题](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/glm-zhipu.md)。

- **文件处理限制**：DashScopeParse 文档解析器单文件上限为 100MB、1000 页，超限文件需预处理切分 [原文标题](../../raw/model-user-guide/use-cases/build-rag-applications-based-on-llamaindex.md)。

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
- [限流应对最佳实践 ](../../raw/model-user-guide/use-cases/rate-limiting-best-practices.md)
- [显式缓存最佳实践](../../raw/model-user-guide/use-cases/explicit-cache-guide.md)
- [通过WebRTC使用多模态交互套件实现实时通话](../../raw/model-user-guide/use-cases/best-practice-webrtc-multimodal-dialog.md)
- [通过AOQ使用qwen3.5-omni-plus-realtime实现实时通话](../../raw/model-user-guide/use-cases/best-practice-aoq-omni-realtime.md)
- [通过WebRTC使用qwen3.5-omni-plus-realtime实现实时通话](../../raw/model-user-guide/use-cases/best-practice-webrtc-omni-realtime.md)
- [DeepSeek-阿里云](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/deepseek-api.md)
- [DeepSeek-硅基流动](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/siliconflow-deepseek-api.md)
- [DeepSeek](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/deepseek-api-by-vanchin.md)
- [Kimi](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/kimi-api.md)
- [Kimi-月之暗面](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/kimi-api-by-moonshot-ai.md)
- [GLM](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/glm.md)
- [GLM-智谱](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/glm-zhipu.md)
- [MiniMax](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/minimax-api-by-minimax.md)
- [MiniMax](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/minimax-api.md)
- [Vidu视频生成Prompt指南](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/vidu-video-generation-prompt-guide.md)
- [MiMo-小米](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/mimo.md)
- [Stepfun-阶跃星辰](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/stepfun.md)



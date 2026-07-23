# use cases

百炼平台的 use cases 覆盖从[多模态](../concepts/multi-modal.md)内容生成、智能体构建、深度研究到教育辅助等全场景落地实践。这些方案均基于百炼统一模型服务与编排能力，支持开箱即用的部署流程和面向生产环境的工程化配置（如限流、缓存、RAG集成），开发者可快速验证业务逻辑并规模化上线。

## 支持的模型/功能

百炼提供两类核心能力：**原生模型服务**与**第三方模型直供接入**。  
- **原生模型**包括 `qwen3-vl-plus`（用于AI解题与批改）、`wan2.7`（文生视频/图生视频）、`qwen-deep-research`（深度研究）、`qwen3.7-*` 系列（通用文本生成）等，均深度集成于百炼控制台与API体系。  
- **第三方模型**通过标准化接口接入，覆盖 DeepSeek（[DeepSeek-阿里云](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/deepseek-api.md)、[DeepSeek-硅基流动](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/siliconflow-deepseek-api.md)、[DeepSeek (快手万擎)](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/deepseek-api-by-vanchin.md)）、Kimi（[Kimi](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/kimi-api.md)、[Kimi-月之暗面](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/kimi-api-by-moonshot-ai.md)）、GLM（[GLM](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/glm.md)、[GLM-智谱](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/glm-zhipu.md)）、MiniMax（[MiniMax](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/minimax-api.md)、[MiniMax (稀宇科技)](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/minimax-api-by-minimax.md)）、MiMo（[MiMo-小米](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/mimo.md)）、Stepfun（[Stepfun-阶跃星辰](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/stepfun.md)）及 Vidu（[Vidu视频生成Prompt指南](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/vidu-video-generation-prompt-guide.md)）。  
> **注意**：多个第三方模型文档（如 DeepSeek、Kimi、GLM、MiniMax）均声明部分旧版本将于 2026 年中下架，并统一推荐迁移至 `qwen3.7-plus`/`qwen3.7-max`/`qwen3.6-flash`。该迁移路径具有一致性，但各供应商的地域支持范围存在差异（例如硅基流动仅限华北2，而阿里云百炼版支持多地域），需按实际部署需求选择。

## 关键参数

不同模态任务依赖特定参数组合：  
- **文生图（万相）**：必填 `prompt`（正向提示词），可选 `negative_prompt`（反向提示词）与 `prompt_extend`（是否启用大模型智能扩写，默认 `true`）[文生图Prompt指南](../../raw/model-user-guide/use-cases/text-to-image-prompt.md)。  
- **文生视频/图生视频（万相）**：支持结构化公式，关键参数包括 `prompt`（主体+场景+运动）、`prompt_extend`（同上）、`enable_thinking`（控制思考模式，非OpenAI标准参数，需通过 `extra_body` 传入）[文生视频/图生视频Prompt指南](../../raw/model-user-guide/use-cases/text-to-video-prompt.md)。  
- **第三方模型调用**：普遍支持 `enable_thinking` 或 `reasoning_effort` 控制推理过程输出；Vidu 支持 `大动态`/`固定镜头` 等运镜关键词 [Vidu视频生成Prompt指南](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/vidu-video-generation-prompt-guide.md)。  
- **缓存与限流**：显式缓存需在请求中注入 `cache_control` 标记；限流应对需配置 `X-DashScope-Wait-Timeout` 请求头或客户端令牌桶策略 [限流应对最佳实践](../../raw/model-user-guide/use-cases/rate-limiting-best-practices.md)、[显式缓存最佳实践](../../raw/model-user-guide/use-cases/explicit-cache-guide.md)。

## 使用方式

典型工作流分为三类：  
1. **低代码编排**：通过无限画布（[HappyHorse 打造一站式影视创作平台](../../raw/model-user-guide/use-cases/infinite-canvas.md)）或节点式工作流（[高效搭建 AI 智能体与工作流应用](../../raw/model-user-guide/use-cases/build-ai-applications-based-on-alibaba-cloud-model-studio.md)）可视化连接模型、工具与数据源，无需编写代码即可构建端到端应用。  
2. **SDK/API 集成**：使用 OpenAI 兼容 SDK（如 `openai` Python 包）或 DashScope SDK，按模型文档指定 `base_url`、`model` 名称及参数（如 `extra_body={"enable_thinking": True}`）发起调用。所有第三方模型均提供 Python/Node.js 示例代码。  
3. **RAG 与知识库增强**：基于 LlamaIndex 构建检索增强应用，通过 `DashScopeCloudIndex` 创建知识库，再以 `as_query_engine()` 封装为可调用接口 [基于LlamaIndex构建RAG应用](../../raw/model-user-guide/use-cases/build-rag-applications-based-on-llamaindex.md)。

## 限制和注意事项

- **地域与权限约束**：多数第三方模型（如硅基流动、月之暗面、快手万擎、小米、阶跃星辰）仅支持华北2（北京）地域，且需对应地域的 API Key；部分模型（如 Kimi、GLM）在新加坡/美国等地域需替换 `WorkspaceId` 到 Base URL 中。  
- **限流维度**：百炼 API 同时受 RPM（每分钟请求数）、TPM（每分钟 [Token](../concepts/token.md) 数）、RPS/TPS（瞬时速率）及 Traffic Burst（增速突增）四重限制，单一重试策略无效，必须结合服务端排队（`X-DashScope-Wait-Timeout`）或客户端自适应拥塞控制 [限流应对最佳实践](../../raw/model-user-guide/use-cases/rate-limiting-best-practices.md)。  
- **缓存生效条件**：显式缓存要求输入内容完全一致（含 system [prompt](prompt.md) 动态字段），Claude Code 等工具默认注入当前目录/日期等变量，会降低跨会话命中率，需启用 `--exclude-dynamic-system-prompt-sections` 参数优化 [显式缓存最佳实践](../../raw/model-user-guide/use-cases/explicit-cache-guide.md)。  
- **模型生命周期**：所有第三方模型文档均明确标注下架时间（集中于 2026 年 7–10 月），且推荐路径统一指向 Qwen 系列，开发者应规划迁移节奏，避免依赖已标记为 deprecated 的模型。

## 来源文档

- [HappyHorse 打造一站式影视创作平台](../../raw/model-user-guide/use-cases/infinite-canvas.md)
- [高效搭建 AI 智能体与工作流应用](../../raw/model-user-guide/use-cases/build-ai-applications-based-on-alibaba-cloud-model-studio.md)
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
- [DeepSeek](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/deepseek-api-by-vanchin.md)
- [Kimi](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/kimi-api.md)
- [Kimi-月之暗面](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/kimi-api-by-moonshot-ai.md)
- [GLM](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/glm.md)
- [GLM-智谱](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/glm-zhipu.md)
- [MiniMax](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/minimax-api.md)
- [MiniMax](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/minimax-api-by-minimax.md)
- [MiMo-小米](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/mimo.md)
- [Stepfun-阶跃星辰](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/stepfun.md)
- [Vidu视频生成Prompt指南](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/vidu-video-generation-prompt-guide.md)



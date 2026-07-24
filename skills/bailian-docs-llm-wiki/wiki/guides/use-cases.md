# use cases

百炼平台的 use cases 覆盖从基础文本生成到多模态智能体构建的全栈能力，支持开发者快速落地 RAG、AI 智能体、深度研究、影视创作、教育辅学等典型场景。所有用例均基于平台统一 API 接口与模型服务，可直接集成至现有系统，无需自建基础设施。

## 支持的模型/功能

百炼提供两类核心能力：**原生模型服务**与**第三方模型直供**。

- **原生模型**：Qwen 系列（如 `qwen3.7-plus`、`qwen3-vl-plus`）、Wan2.7（文生图/视频）、HappyHorse（视频生成）等，具备完整功能链路，如 Wan2.7 支持多镜头叙事与声音控制 [文生视频/图生视频Prompt指南](../../raw/model-user-guide/use-cases/text-to-video-prompt.md)，HappyHorse 支持节点式无限画布编排 [HappyHorse 打造一站式影视创作平台](../../raw/model-user-guide/use-cases/infinite-canvas.md)。
  
- **第三方模型直供**：DeepSeek（硅基流动、阿里云、快手万擎三路接入）、Kimi（月之暗面）、GLM（智谱）、MiniMax、Stepfun、MiMo（小米）等。各供应商模型在上下文长度、限流策略、思考模式参数（如 `enable_thinking` 或 `reasoning_effort`）上存在差异，需按文档配置。例如，硅基流动版 DeepSeek 支持更长上下文，而阿里云版支持联网搜索与缓存 [DeepSeek-硅基流动](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/siliconflow-deepseek-api.md)。

> **注意**：多个第三方模型文档（如 [DeepSeek-阿里云](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/deepseek-api.md)、[Kimi](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/kimi-api.md)、[MiniMax](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/minimax-api.md)）均标注了明确的下架时间（2026年7月或10月），且推荐迁移至 Qwen 系列。此为平台统一演进策略，开发者应优先选用 Qwen 新版本模型。

## 关键参数

不同任务类型依赖特定参数组合，需严格遵循规范：

- **文本生成**：`enable_thinking`（开启思考模式，返回 `reasoning_content` 字段）、`reasoning_effort`（控制推理深度，值为 `"max"`/`"high"`/`"none"`）、`stream`（[流式输出](../concepts/streaming-output.md)开关）。非 OpenAI 标准参数须通过 `extra_body`（Python SDK）或顶层字段（Node.js SDK）传入。
  
- **文生图**：`prompt`（正向提示词）、`negative_prompt`（反向提示词）、`prompt_extend`（是否启用大模型智能改写，默认 `true`）[文生图Prompt指南](../../raw/model-user-guide/use-cases/text-to-image-prompt.md)。
  
- **文生视频**：除基础 `prompt` 外，支持 `shot_type`（单/多镜头）、`sound_description`（人声/音效/BGM）、`time_stamp`（分镜时间戳）等结构化参数，详见多镜头公式 [文生视频/图生视频Prompt指南](../../raw/model-user-guide/use-cases/text-to-video-prompt.md)。
  
- **限流控制**：`X-DashScope-Wait-Timeout`（服务端排队等待秒数，仅对 Traffic Burst 有效）[限流应对最佳实践](../../raw/model-user-guide/use-cases/rate-limiting-best-practices.md)。
  
- **缓存控制**：`cache_control`（显式缓存标记，需通过 Anthropic 兼容协议调用）[显式缓存最佳实践](../../raw/model-user-guide/use-cases/explicit-cache-guide.md)。

## 使用方式

1. **API 调用**：所有模型均支持 [OpenAI 兼容接口](../concepts/openai-compatible-api.md)（`base_url` 需按地域配置）与 DashScope 原生 SDK。华北2（北京）地域多数第三方模型（如 SiliconFlow DeepSeek、Moonshot Kimi）要求使用专属业务空间域名 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com` 以获得更高稳定性 [GLM-智谱](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/glm-zhipu.md)。
   
2. **RAG 构建**：通过 LlamaIndex 集成百炼知识库服务，使用 `DashScopeCloudIndex` 创建索引，`DashScopeCloudRetriever` 获取检索器，再结合 `DashScope` LLM 实例构建 Query Engine [基于LlamaIndex构建RAG应用](../../raw/model-user-guide/use-cases/build-rag-applications-based-on-llamaindex.md)。
   
3. **工作流编排**：电商客服等复杂场景需组合智能体（Agent）、RAG、[函数调用](../concepts/function-calling.md)（Function Call）与对话流（Dialog Flow），通过百炼可视化流程编排工具实现 [高效搭建 AI 智能体与工作流应用](../../raw/model-user-guide/use-cases/build-ai-applications-based-on-alibaba-cloud-model-studio.md)。
   
4. **文档转视频**：采用分阶段流水线：文档切片 → 生成演示文稿图片 → 合成讲解语音与字幕 → 剪辑合成视频，依赖 FFmpeg 与 Marp 工具链 [借助大模型将文档转换为视频](../../raw/model-user-guide/use-cases/use-llm-to-convert-document-to-video.md)。

## 限制和注意事项

- **地域限制**：多数第三方模型（SiliconFlow DeepSeek、Moonshot Kimi、Stepfun、MiMo）仅在华北2（北京）地域可用，且必须使用该地域的 API Key；部分模型（如 GLM、MiniMax）在海外地域（美国、新加坡等）亦有部署，但需替换对应 `base_url` [GLM](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/glm.md)。
  
- **限流维度**：百炼 API 同时受请求数（RPM/RPS）、[Token](../concepts/token.md) 用量（TPM/TPS）及增速（Traffic Burst）三重约束。单纯重试无效，需结合服务端排队（`X-DashScope-Wait-Timeout`）、客户端令牌桶或架构层 MQ 削峰 [限流应对最佳实践](../../raw/model-user-guide/use-cases/rate-limiting-best-practices.md)。
  
- **缓存生效条件**：显式缓存仅在 Anthropic 兼容协议下自动启用（如 Claude Code、OpenCode），且需确保 `cache_control` 标记被正确注入 system [prompt](prompt.md) 或 user message；普通 OpenAI 协议调用不触发此机制 [显式缓存最佳实践](../../raw/model-user-guide/use-cases/explicit-cache-guide.md)。
  
- **模型生命周期**：第三方模型存在明确下架计划（如 DeepSeek 系列于 2026 年 10 月下架），平台持续推荐迁移至 Qwen 新版本。开发者应避免在生产环境长期绑定已标注下架日期的模型。

## 来源文档

- [高效搭建 AI 智能体与工作流应用](../../raw/model-user-guide/use-cases/build-ai-applications-based-on-alibaba-cloud-model-studio.md)
- [深度研究：生成你的独家洞察报告](../../raw/model-user-guide/use-cases/deep-research.md)
- [HappyHorse 打造一站式影视创作平台](../../raw/model-user-guide/use-cases/infinite-canvas.md)
- [文生文Prompt指南](../../raw/model-user-guide/use-cases/prompt-engineering-guide.md)
- [文生图Prompt指南](../../raw/model-user-guide/use-cases/text-to-image-prompt.md)
- [文生视频/图生视频Prompt指南](../../raw/model-user-guide/use-cases/text-to-video-prompt.md)
- [基于LlamaIndex构建RAG应用](../../raw/model-user-guide/use-cases/build-rag-applications-based-on-llamaindex.md)
- [自定义模型调优、部署与评测](../../raw/model-user-guide/use-cases/model-training-best-practices.md)
- [借助大模型将文档转换为视频](../../raw/model-user-guide/use-cases/use-llm-to-convert-document-to-video.md)
- [限流应对最佳实践 ](../../raw/model-user-guide/use-cases/rate-limiting-best-practices.md)
- [显式缓存最佳实践](../../raw/model-user-guide/use-cases/explicit-cache-guide.md)
- [AI 解题 + 批改：推动课程教学智变](../../raw/model-user-guide/use-cases/ai-homework-helper.md)
- [DeepSeek-硅基流动](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/siliconflow-deepseek-api.md)
- [DeepSeek-阿里云](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/deepseek-api.md)
- [Kimi](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/kimi-api.md)
- [DeepSeek](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/deepseek-api-by-vanchin.md)
- [Kimi-月之暗面](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/kimi-api-by-moonshot-ai.md)
- [GLM-智谱](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/glm-zhipu.md)
- [MiniMax](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/minimax-api.md)
- [GLM](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/glm.md)
- [MiniMax](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/minimax-api-by-minimax.md)
- [Vidu视频生成Prompt指南](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/vidu-video-generation-prompt-guide.md)
- [Stepfun-阶跃星辰](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/stepfun.md)
- [MiMo-小米](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/mimo.md)



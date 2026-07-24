# use cases

百炼平台的 use cases 覆盖从[多模态](../concepts/multi-modal.md)内容生成、智能体构建到深度研究与教育辅助等核心场景，支持开发者基于预置模型或第三方模型快速落地生产级应用。所有方案均依托函数计算等免运维基础设施，强调开箱即用与成本可控，适用于初创团队、中大型企业及教育机构等不同规模客户。

## 支持的模型/功能

百炼提供两类模型能力：**阿里云自研模型**（如 Qwen 系列、Wan2.7、HappyHorse、Qwen3-VL）和**第三方直供模型**（如 DeepSeek、Kimi、GLM、MiniMax、MiMo、Stepfun、Vidu）。  
- **视觉生成**：万相（Wan2.7/Wan2.6）支持文生图、图生视频、多镜头叙事；HappyHorse 专注高质量视频生成；Vidu 提供差异化运镜与风格控制能力 [Vidu视频生成Prompt指南](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/vidu-video-generation-prompt-guide.md)。  
- **文本与[多模态](../concepts/multi-modal.md)理解**：Qwen3-VL 系列在 MathVista、MMMU 等评测中达 SOTA，支撑解题与批改场景 [AI 解题 + 批改：推动课程教学智变](../../raw/model-user-guide/use-cases/ai-homework-helper.md)；Qwen-Deep-Research 实现多源交叉验证与结构化报告生成 [深度研究：生成你的独家洞察报告](../../raw/model-user-guide/use-cases/deep-research.md)。  
- **智能体与工作流**：通过节点式编排（如无限画布）、RAG、Function Call 和对话流，支持电商客服、影视创作等复杂任务自动化 [高效搭建 AI 智能体与工作流应用](../../raw/model-user-guide/use-cases/build-ai-applications-based-on-alibaba-cloud-model-studio.md)。  
- **第三方模型集成**：DeepSeek、Kimi、GLM 等均支持 [OpenAI 兼容接口](../concepts/openai-compatible-api.md)调用，并提供 `enable_thinking` 或 `reasoning_effort` 等参数控制推理过程；部分模型（如 GLM-5.2）支持 1M 上下文 [GLM-智谱](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/glm-zhipu.md)。

> **注意**：文档 14（Kimi）、16（GLM）、18（MiniMax）和 24（DeepSeek-阿里云）均明确标注了模型下架时间（2026年7月9日或10月10日），但文档 15（Kimi-月之暗面）、17（GLM-智谱）、19（MiniMax）、21（MiMo）、22（Stepfun）及 13（DeepSeek-硅基流动）未提下架计划，建议优先采用后者以保障长期可用性。

## 关键参数

不同模型类型对应关键参数如下：  
- **文生图（万相）**：`prompt`（正向提示词）、`negative_prompt`（反向提示词）、`prompt_extend`（是否启用大模型智能改写，默认 `true`）[文生图Prompt指南](../../raw/model-user-guide/use-cases/text-to-image-prompt.md)。  
- **文生/图生视频（万相）**：`prompt` 需按基础公式（主体+场景+运动）或进阶公式（含美学控制、风格化）组织；多镜头需显式指定时间戳与分镜内容；声音控制需分离人声、音效、BGM 描述 [文生视频/图生视频Prompt指南](../../raw/model-user-guide/use-cases/text-to-video-prompt.md)。  
- **思考模式模型（DeepSeek/Kimi/GLM/MiMo/Stepfun）**：非 OpenAI 标准参数需通过 `extra_body`（Python SDK）或顶层字段（Node.js SDK）传入，如 `{"enable_thinking": true}` 或 `{"reasoning_effort": "max"}`。  
- **限流控制**：`X-DashScope-Wait-Timeout` 请求头用于服务端排队等待，仅对 Traffic Burst 有效；需同步延长客户端超时时间 [限流应对最佳实践](../../raw/model-user-guide/use-cases/rate-limiting-best-practices.md)。  
- **显式缓存**：通过 `cache_control` 标记（Anthropic 协议）实现确定性命中，适用于 Agent 长上下文管理 [显式缓存最佳实践](../../raw/model-user-guide/use-cases/explicit-cache-guide.md)。

## 使用方式

1. **模型开通与配置**：在百炼控制台模型市场开通目标模型（如 HappyHorse、Kimi、GLM），获取 API Key 并配置环境变量；第三方模型需注意地域限制（多数仅支持华北2北京）及业务空间 ID 绑定。  
2. **[Prompt 工程](../concepts/prompt-engineering.md)**：遵循结构化公式编写提示词——文生图用“主体+场景+风格”，文生视频用“主体+场景+运动+美学控制”，图生视频聚焦“运动+运镜”；Vidu 等模型需结合提示词词典选择运镜、风格、特效关键词。  
3. **SDK 调用**：推荐使用 [OpenAI 兼容接口](../concepts/openai-compatible-api.md)（`base_url` 指向 `compatible-mode/v1`），第三方模型需在 `model` 参数中指定完整命名（如 `"kimi/kimi-k3"`、`"ZHIPU/GLM-5.2"`）；思考模式结果需解析 `reasoning_content` 与 `content` 字段。  
4. **高级能力集成**：  
   - RAG 应用：通过 LlamaIndex + DashScopeCloudIndex 构建知识库，调用 `as_retriever()` 或 `as_query_engine()` [基于LlamaIndex构建RAG应用](../../raw/model-user-guide/use-cases/build-rag-applications-based-on-llamaindex.md)；  
   - 文档转视频：结合大模型切片、[多模态](../concepts/multi-modal.md)生成、FFmpeg 剪辑与 Marp 渲染 [借助大模型将文档转换为视频](../../raw/model-user-guide/use-cases/use-llm-to-convert-document-to-video.md)；  
   - 自定义模型：完成训练数据准备（Prompt-Completion 格式）、模型调优、部署与评测闭环 [自定义模型调优、部署与评测](../../raw/model-user-guide/use-cases/model-training-best-practices.md)。

## 限制和注意事项

- **地域与域名约束**：Kimi、GLM-智谱、MiniMax、MiMo、Stepfun、DeepSeek（硅基流动/快手万擎）等第三方模型仅支持华北2（北京）地域，且 GLM-智谱强烈推荐使用业务空间专属域名 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com` 以获得更高稳定性。  
- **限流维度**：百炼 API 同时受 RPM/TPM（分钟级配额）、RPS/TPS（瞬时频率）和 Traffic Burst（增速限制）三重约束；`X-DashScope-Wait-Timeout` 仅缓解后一种，不可替代客户端流控 [限流应对最佳实践](../../raw/model-user-guide/use-cases/rate-limiting-best-practices.md)。  
- **缓存适用性**：显式缓存要求请求内容完全一致（含 `cache_control` 标记），适用于高频复用 Prompt 场景；首次写入有 25% 额外开销，但后续命中可节省 90% 成本。  
- **模型兼容性**：DashScope SDK 与 OpenAI SDK 调用方式存在差异（如 `base_url` 设置、思考参数传递位置），需严格参照各模型文档示例代码，避免因参数位置错误导致静默失败。  
- **废弃风险**：多个第三方模型（Kimi、GLM、MiniMax）已明确标注下架日期，新项目应优先选用 Qwen 系列或未标注下架的第三方模型（如 Vidu、Stepfun），并关注控制台公告。

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
- [限流应对最佳实践 ](../../raw/model-user-guide/use-cases/rate-limiting-best-practices.md)
- [显式缓存最佳实践](../../raw/model-user-guide/use-cases/explicit-cache-guide.md)
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
- [DeepSeek](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/deepseek-api-by-vanchin.md)
- [DeepSeek-阿里云](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/deepseek-api.md)



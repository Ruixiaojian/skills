# use cases

百炼平台提供覆盖文本、图像、视频、语音、[多模态](../concepts/multi-modal.md)及智能体工作流的全栈AI能力，支持从Prompt工程、RAG构建、模型微调到实时音视频交互等典型开发场景。开发者可基于预置模型快速验证业务逻辑，或通过自定义模型、第三方模型集成等方式深度适配领域需求。所有能力均通过统一API接口和控制台可视化操作交付，兼顾开箱即用性与工程可控性。

## 支持的模型/功能

百炼支持两类模型接入方式：**平台原生模型**（如Qwen系列、万相系列）和**第三方直供模型**（如DeepSeek、Kimi、GLM、MiniMax、MiMo、Stepfun等）。不同模型在能力维度上存在明确分工：

- **文本生成与推理**：Qwen3-VL（[多模态](../concepts/multi-modal.md)解题）、Qwen3.7-max（长上下文推理）、Qwen-Deep-Research（多轮深度分析）；第三方模型如 `kimi/kimi-k3`、`ZHIPU/GLM-5.2`、`MiniMax/MiniMax-M2.7` 均支持 `enable_thinking` 或 `reasoning_effort` 参数开启结构化推理过程 [原文标题](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/kimi-api-by-moonshot-ai.md)。
- **视觉生成**：万相（Wan2.7/Wan2.6）支持文生图、图生视频、参考生视频；Vidu 提供独立视频生成能力，其提示词需严格遵循“主体/场景+场景描述+环境描述+艺术风格/媒介”公式 [原文标题](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/vidu-video-generation-prompt-guide.md)。
- **[多模态](../concepts/multi-modal.md)与实时交互**：`qwen3.5-omni-plus-realtime` 支持WebRTC及AOQ SDK双通道音视频实时通话；`multimodal-dialog` 套件面向硬件终端提供预置Agent与音色管理 [原文标题](../../raw/model-user-guide/use-cases/best-practice-webrtc-multimodal-dialog.md)。
- **智能体与工作流**：通过RAG（基于LlamaIndex）、自主决策Agent、对话流编排实现复杂任务自动化，典型应用包括电商客服助手与深度研究报告生成 [原文标题](../../raw/model-user-guide/use-cases/build-ai-applications-based-on-alibaba-cloud-model-studio.md)。

> **注意**：多个第三方模型文档（如[DeepSeek-硅基流动](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/siliconflow-deepseek-api.md)与[DeepSeek-阿里云](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/deepseek-api.md)）均声明部分模型将于2026年下架，但下架时间不一致（前者未标注具体日期，后者明确为2026年10月10日），建议以控制台实际服务状态为准。

## 关键参数

不同模型与能力模块的关键参数设计高度结构化，开发者需按协议规范传入：

- **文本模型通用参数**：`model`（模型标识符，如 `"qwen3.7-max"`）、`messages`（对话历史）、`stream`（流式开关）。第三方模型需通过 `extra_body`（OpenAI SDK）或顶层字段（Node.js）传入非标准参数，如 `enable_thinking: true` 或 `reasoning_effort: "max"`。
- **视觉生成参数**：
  - 文生图：`prompt`（正向提示词）、`negative_prompt`（反向提示词）、`prompt_extend`（是否启用大模型智能扩写，默认`true`）[原文标题](../../raw/model-user-guide/use-cases/text-to-image-prompt.md)。
  - 文生视频：基础公式为 `主体 + 场景 + 运动`，进阶公式扩展为 `主体描述 + 场景描述 + 运动描述 + 美学控制 + 风格化`；支持 `sound_description` 控制人声/音效/BGM [原文标题](../../raw/model-user-guide/use-cases/text-to-video-prompt.md)。
- **实时交互参数**：WebRTC模式强制使用 `server_vad` 或 `semantic_vad`，不支持手动VAD；AOQ SDK需通过AppServer鉴权获取[Token](../concepts/token.md)，并配置Opus插件。
- **缓存与限流**：显式缓存通过请求头 `cache_control` 标记启用；限流应对依赖 `X-DashScope-Wait-Timeout` 头实现服务端排队 [原文标题](../../raw/model-user-guide/use-cases/rate-limiting-best-practices.md)。

## 使用方式

开发者可根据技术栈选择三种主流接入路径：

1. **低代码/无代码**：通过百炼控制台直接部署预置方案（如AI电商客服助手、深度研究报告生成），15–30分钟完成端到端搭建，无需编写代码。
2. **SDK/API集成**：
   - OpenAI兼容模式：适用于Python/Node.js等语言，配置`base_url`指向地域专属域名（如华北2为 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`），调用标准`chat.completions.create`接口。
   - DashScope SDK：需安装`dashscope`包，设置`base_http_api_url`，调用`Generation`类。
3. **框架集成**：LlamaIndex用户可直接使用`llama-index-indices-managed-dashscope`包，通过`DashScopeCloudIndex`创建知识库并获取`retriever`或`query_engine` [原文标题](../../raw/model-user-guide/use-cases/build-rag-applications-based-on-llamaindex.md)。

所有方案均依赖API Key认证，且需提前在控制台开通对应模型服务及知识库等资源。

## 限制和注意事项

- **地域与域名约束**：多数第三方模型（DeepSeek、Kimi、GLM、MiniMax、MiMo、Stepfun）仅支持华北2（北京）地域，且强烈推荐使用业务空间专属域名 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com` 替代通用域名，以获得更高稳定性与性能 [原文标题](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/glm-zhipu.md)。
- **限流策略**：百炼API按RPM/TPM（分钟级）、RPS/TPS（瞬时）、Traffic Burst（增速）三维度限流。突发流量应优先启用`X-DashScope-Wait-Timeout`头，而非简单重试 [原文标题](../../raw/model-user-guide/use-cases/rate-limiting-best-practices.md)。
- **文件处理限制**：`DashScopeParse`文档解析器要求单个PDF/DOCX文件≤100MB且≤1000页；图像理解模型（如Qwen3-VL）对输入图片尺寸与格式有隐式约束，超限将导致解析失败。
- **缓存适用性**：显式缓存仅对完全相同的`prompt`内容100%命中，动态内容（如含当前时间、git状态）需通过`--exclude-dynamic-system-prompt-sections`等参数剥离，否则跨会话命中率极低。
- **模型生命周期**：GLM-4.6/4.7、MiniMax-M2.1、Kimi-K2系列等模型已明确标注下架时间（2026年7月9日），开发者应规划迁移至Qwen3系列替代方案。

## 来源文档

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
- [HappyHorse 打造一站式影视创作平台](../../raw/model-user-guide/use-cases/infinite-canvas.md)
- [通过WebRTC使用多模态交互套件实现实时通话](../../raw/model-user-guide/use-cases/best-practice-webrtc-multimodal-dialog.md)
- [通过AOQ使用qwen3.5-omni-plus-realtime实现实时通话](../../raw/model-user-guide/use-cases/best-practice-aoq-omni-realtime.md)
- [通过WebRTC使用qwen3.5-omni-plus-realtime实现实时通话](../../raw/model-user-guide/use-cases/best-practice-webrtc-omni-realtime.md)
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
- [DeepSeek-阿里云](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/deepseek-api.md)



# use cases

百炼平台提供覆盖文本、图像、视频、语音及多模态的全栈AI能力，支持从Prompt工程、RAG构建、智能体编排到端侧实时交互等多样化生产场景。本文档面向开发者，系统梳理平台核心用例、关键参数、调用方式及实践约束，帮助快速选型与落地。

## 支持的模型/功能

百炼支持两类模型接入方式：**原生模型**（如Qwen系列、Wan2.7、HappyHorse）和**第三方直供模型**（如DeepSeek、Kimi、GLM、MiniMax、MiMo、Stepfun等）。所有模型均通过统一API接口调用，支持OpenAI兼容协议与DashScope SDK。

- **文本生成**：Qwen3.7系列（`qwen3.7-plus`、`qwen3.7-max`）、DeepSeek-v3.2/v4-pro、Kimi-k3/k2.6、GLM-5.2、MiniMax-M2.7、MiMo-v2.5-pro、Step-3.7-flash等，均支持`enable_thinking`或`reasoning_effort`参数控制推理过程输出 [DeepSeek-硅基流动](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/siliconflow-deepseek-api.md)。
- **多模态理解与生成**：`qwen3-vl-plus`用于解题批改 [AI 解题 + 批改：推动课程教学智变](../../raw/model-user-guide/use-cases/ai-homework-helper.md)，`wan2.7`与`happyhorse`联合支撑影视创作全流程 [HappyHorse 打造一站式影视创作平台](../../raw/model-user-guide/use-cases/infinite-canvas.md)。
- **检索增强（RAG）**：通过LlamaIndex集成百炼知识库服务，支持PDF/DOCX等格式解析与向量检索 [基于LlamaIndex构建RAG应用](../../raw/model-user-guide/use-cases/build-rag-applications-based-on-llamaindex.md)。
- **深度研究**：`qwen-deep-research`模型专用于多轮搜索、交叉验证与结构化报告生成。
- **实时音视频交互**：`qwen3.5-omni-plus-realtime`支持WebRTC与AOQ双通道低延迟通话，适用于AI眼镜、学习机等硬件终端。

> **注意**：多个第三方模型文档（如[DeepSeek-阿里云](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/deepseek-api.md)、[Kimi](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/kimi-api.md)、[GLM](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/glm.md)、[MiniMax](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/minimax-api.md)）均明确标注部分旧版模型将于2026年下架，且推荐迁移至Qwen3.x系列。该迁移建议具有一致性，属平台统一演进策略，非矛盾信息。

## 关键参数

不同任务类型对应差异化参数体系：

- **文本生成通用参数**：
  - `model`：必需，指定模型ID（如`qwen3.7-plus`、`siliconflow/deepseek-v3.2`）。
  - `stream`：布尔值，控制流式响应。
  - `extra_body`：承载非标准参数，如`{"enable_thinking": true}`（DeepSeek/Kimi/MiMo/Stepfun）或`{"reasoning_effort": "max"}`（Kimi）。
- **文生图/视频参数**：
  - `prompt` / `negative_prompt`：正向与反向提示词（见[文生图Prompt指南](../../raw/model-user-guide/use-cases/text-to-image-prompt.md)）。
  - `prompt_extend`：文生图V2中是否启用大模型智能扩写（默认`true`）。
  - 多镜头控制需使用时间戳分镜语法（如`第1个镜头[0-3秒]...`），详见[文生视频/图生视频Prompt指南](../../raw/model-user-guide/use-cases/text-to-video-prompt.md)。
- **缓存与限流**：
  - `cache_control`：显式缓存标记，用于Agent[长上下文](../concepts/long-context.md)管理 [显式缓存最佳实践](../../raw/model-user-guide/use-cases/explicit-cache-guide.md)。
  - `X-DashScope-Wait-Timeout`：服务端排队等待头，专用于应对突发流量限流（`Throttling.BurstRate`） [限流应对最佳实践](../../raw/model-user-guide/use-cases/rate-limiting-best-practices.md)。

## 使用方式

- **开发环境**：所有方案均基于函数计算（FC）或本地Python环境部署，依赖`dashscope` SDK或OpenAI兼容客户端。需提前配置API Key至环境变量。
- **模型开通**：第三方模型（DeepSeek/Kimi/GLM等）需在百炼控制台模型市场手动开通，并确认地域匹配（绝大多数仅支持华北2北京）。
- **Prompt工程**：推荐采用结构化框架（背景/目的/风格/语气/受众/输出）设计文本Prompt；图像/视频Prompt应遵循“主体+场景+运动/风格”公式，并善用提示词词典细化景别、运镜与氛围 [文生文Prompt指南](../../raw/model-user-guide/use-cases/prompt-engineering-guide.md)。
- **RAG构建**：使用`DashScopeParse`解析文档，通过`DashScopeCloudIndex`创建知识库，再集成至LlamaIndex Query Engine。
- **实时交互**：WebRTC方案需处理SDP交换代理（浏览器CORS限制），AOQ方案需集成Opus[插件](../concepts/plugin.md)并申请运行时权限。

## 限制和注意事项

- **地域与域名约束**：第三方模型（DeepSeek/Kimi/GLM/MiniMax/MiMo/Stepfun）及部分实时模型（`qwen3.5-omni-plus-realtime`）**仅支持华北2（北京）地域**，且强烈建议使用业务空间专属域名`https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com`替代通用域名，以获得更高稳定性 [GLM-智谱](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/glm-zhipu.md)。
- **限流维度**：API受RPM（请求/分钟）、TPM（[Token](../concepts/token.md)/分钟）、RPS（请求/秒）、TPS（[Token](../concepts/token.md)/秒）及Traffic Burst（增速）五维限流。单纯重试无效，需结合服务端排队、令牌桶或MQ削峰 [限流应对最佳实践](../../raw/model-user-guide/use-cases/rate-limiting-best-practices.md)。
- **输入格式**：`qwen3-vl-plus`等视觉模型要求输入为图片URL或base64编码；`qwen-deep-research`需纯文本课题描述；Vidu视频生成对提示词长度与结构敏感，避免主体分散与模糊术语 [Vidu视频生成Prompt指南](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/vidu-video-generation-prompt-guide.md)。
- **成本控制**：显式缓存首次写入产生25%额外开销，但命中后可降本90%，适用于高频复用Prompt场景；函数计算按量付费，各方案均标注典型体验成本（如深度研究方案约6元）。

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
- [通过WebRTC使用多模态交互套件实现实时通话](../../raw/model-user-guide/use-cases/best-practice-webrtc-multimodal-dialog.md)
- [通过AOQ使用qwen3.5-omni-plus-realtime实现实时通话](../../raw/model-user-guide/use-cases/best-practice-aoq-omni-realtime.md)
- [通过WebRTC使用qwen3.5-omni-plus-realtime实现实时通话](../../raw/model-user-guide/use-cases/best-practice-webrtc-omni-realtime.md)
- [DeepSeek-硅基流动](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/siliconflow-deepseek-api.md)
- [DeepSeek](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/deepseek-api-by-vanchin.md)
- [DeepSeek-阿里云](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/deepseek-api.md)
- [Kimi-月之暗面](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/kimi-api-by-moonshot-ai.md)
- [Kimi](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/kimi-api.md)
- [GLM](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/glm.md)
- [MiniMax](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/minimax-api.md)
- [GLM-智谱](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/glm-zhipu.md)
- [Vidu视频生成Prompt指南](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/vidu-video-generation-prompt-guide.md)
- [MiniMax](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/minimax-api-by-minimax.md)
- [MiMo-小米](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/mimo.md)
- [Stepfun-阶跃星辰](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/stepfun.md)



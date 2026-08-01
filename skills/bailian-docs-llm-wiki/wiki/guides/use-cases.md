# use cases

百炼平台提供覆盖文本、图像、视频、语音等多模态的生成与理解能力，支持从简单 Prompt 调用到复杂工作流编排的全栈 AI 应用构建。本文档面向开发者，系统梳理平台核心使用场景、模型能力边界、关键参数配置及工程实践约束，帮助快速落地生产级应用。

## 支持的模型/功能

百炼平台支持两类模型接入方式：**原生模型**（如 Qwen 系列、Wan2.7、HappyHorse）和**第三方直供模型**（如 DeepSeek、Kimi、GLM、MiniMax、MiMo、Stepfun、Vidu）。所有模型均通过统一 API 接口调用，但能力差异显著：

- **文本模型**：Qwen3-VL（多模态推理）、Qwen-Max（强逻辑）、Qwen-Deep-Research（多轮深度检索）、qwen3.5-omni-plus-realtime（实时音视频交互）；第三方模型如 `siliconflow/deepseek-v3.2`、`kimi/kimi-k3`、`ZHIPU/GLM-5.2` 均支持 `enable_thinking` 或 `reasoning_effort` 参数控制推理过程输出 [DeepSeek-硅基流动](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/siliconflow-deepseek-api.md)。
- **视觉模型**：万相系列（文生图 V1/V2、文生视频、图生视频）、HappyHorse（专业视频生成）、Vidu（高动态视频生成），均需遵循结构化 Prompt 公式 [Vidu视频生成Prompt指南](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/vidu-video-generation-prompt-guide.md)。
- **智能体与工作流**：支持基于 RAG 的问答（通过 LlamaIndex 集成 [基于LlamaIndex构建RAG应用](../../raw/model-user-guide/use-cases/build-rag-applications-based-on-llamaindex.md)）、自主决策 Agent、可视化节点编排（如 HappyHorse 无限画布方案）。
- **实时交互套件**：提供 WebRTC 和 AOQ 两种 SDK，分别适配浏览器端与移动端音视频实时通话，底层模型可灵活切换为 `qwen3.5-omni-plus-realtime` 或第三方模型。

> **注意**：多个第三方模型文档（如 [DeepSeek-阿里云](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/deepseek-api.md)、[Kimi-月之暗面](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/kimi-api-by-moonshot-ai.md)、[GLM-智谱](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/glm-zhipu.md)）均声明部分旧版本模型（如 deepseek-v3.2-exp、kimi-k2-thinking、glm-4.7）将于 2026 年下架，且明确推荐迁移至 Qwen3 系列。该迁移路径具有一致性，开发者应优先评估 `qwen3.7-plus` 等原生模型替代方案。

## 关键参数

不同模态与模型类型的关键参数存在显著差异，需按场景精准配置：

- **文本生成**：`stream`（流式响应）、`extra_body`（非标准参数载体，用于传递 `enable_thinking`、`reasoning_effort`、`preserve_thinking` 等）、`cache_control`（显式缓存标记，见 [显式缓存最佳实践](../../raw/model-user-guide/use-cases/explicit-cache-guide.md)）。
- **文生图**：`prompt`（正向提示词）、`negative_prompt`（反向提示词）、`prompt_extend`（是否启用大模型智能改写，默认 true）。
- **文生/图生视频**：除基础 `prompt` 外，需按公式组织（主体+场景+运动 → 进阶含美学控制与风格化），多镜头需显式标注时间戳与分镜内容；Wan2.7 支持 `shot_type` 已废弃，须用自然语言描述“生成单镜头”或分镜结构。
- **实时音视频**：WebRTC 模式强制启用 `server_vad`（服务端语音活动检测），不支持手动 VAD；AOQ 模式需业务侧 AppServer 颁发 Token。
- **限流控制**：`X-DashScope-Wait-Timeout` 请求头用于应对突发流量（Traffic Burst），仅对增速限流生效，需同步延长客户端超时时间。

## 使用方式

典型开发流程遵循“准备→调用→编排→优化”四步：

1. **环境准备**：获取 API Key 并配置为环境变量；开通对应模型服务（如在控制台开通 Wan2.7 或 SiliconFlow DeepSeek）；安装必要 SDK（`dashscope`、`llama-index-llms-dashscope` 等）。
2. **基础调用**：使用 [OpenAI 兼容接口](../concepts/openai-compatible-interface.md)或 DashScope SDK 发起请求。第三方模型必须指定华北2（北京）地域专属域名 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`，且 Workspace ID 不可省略。
3. **工作流编排**：
   - 对于 RAG 应用，使用 LlamaIndex 封装知识库上传、索引创建与查询引擎 [基于LlamaIndex构建RAG应用](../../raw/model-user-guide/use-cases/build-rag-applications-based-on-llamaindex.md)；
   - 对于多步骤任务，利用百炼可视化画布或代码化工作流（如电商客服助手中的智能问答、RAG、Agent、对话流四类模式）。
4. **效果优化**：
   - [Prompt 工程](../concepts/prompt-engineering.md)：文本遵循 [文生文Prompt指南](../../raw/model-user-guide/use-cases/prompt-engineering-guide.md) 的框架法；图像/视频严格套用对应公式与词典；
   - 性能优化：启用显式缓存降低重复 Prompt 成本；对突发流量配置 `X-DashScope-Wait-Timeout`；长上下文场景结合 `preserve_thinking` 传递推理链。

## 限制和注意事项

- **地域与域名约束**：所有第三方直供模型（DeepSeek、Kimi、GLM、MiniMax、MiMo、Stepfun）及部分实时能力（WebRTC、AOQ）**仅支持华北2（北京）地域**，且必须使用业务空间专属域名（`{WorkspaceId}.cn-beijing.maas.aliyuncs.com`），通用域名 `dashscope.aliyuncs.com` 不可用。
- **限流维度**：API 同时受 RPM（每分钟请求数）、TPM（每分钟 Token 数）、RPS（每秒请求数）、TPS（每秒 Token 数）及 Traffic Burst（增速）五重限制。`429` 错误需结合错误码（如 `Throttling.BurstRate`）与特征诊断选择策略，单纯重试无效 [限流应对最佳实践](../../raw/model-user-guide/use-cases/rate-limiting-best-practices.md)。
- **文件处理限制**：DashScopeParse 文档解析器要求单个 PDF/DOCX 文件 ≤100MB 且 ≤1000 页；函数计算部署方案有 15 分钟执行时长上限。
- **模型能力边界**：Qwen3-VL 系列专精数学与多学科解题，但未声明支持代码生成；Wan2.7 视频生成不支持 `shot_type` 参数；Vidu 模型对“大动态”等关键词敏感，需严格按词典使用。
- **缓存一致性**：显式缓存要求输入内容完全一致才能命中，动态信息（如当前日期、git 状态）会破坏跨会话命中率，建议通过 `--exclude-dynamic-system-prompt-sections` 等参数剥离 [显式缓存最佳实践](../../raw/model-user-guide/use-cases/explicit-cache-guide.md)。

## 来源文档

- [HappyHorse 打造一站式影视创作平台](../../raw/model-user-guide/use-cases/infinite-canvas.md)
- [深度研究：生成你的独家洞察报告](../../raw/model-user-guide/use-cases/deep-research.md)
- [高效搭建 AI 智能体与工作流应用](../../raw/model-user-guide/use-cases/build-ai-applications-based-on-alibaba-cloud-model-studio.md)
- [AI 解题 + 批改：推动课程教学智变](../../raw/model-user-guide/use-cases/ai-homework-helper.md)
- [文生文Prompt指南](../../raw/model-user-guide/use-cases/prompt-engineering-guide.md)
- [文生图Prompt指南](../../raw/model-user-guide/use-cases/text-to-image-prompt.md)
- [基于LlamaIndex构建RAG应用](../../raw/model-user-guide/use-cases/build-rag-applications-based-on-llamaindex.md)
- [文生视频/图生视频Prompt指南](../../raw/model-user-guide/use-cases/text-to-video-prompt.md)
- [自定义模型调优、部署与评测](../../raw/model-user-guide/use-cases/model-training-best-practices.md)
- [限流应对最佳实践 ](../../raw/model-user-guide/use-cases/rate-limiting-best-practices.md)
- [借助大模型将文档转换为视频](../../raw/model-user-guide/use-cases/use-llm-to-convert-document-to-video.md)
- [通过WebRTC使用多模态交互套件实现实时通话](../../raw/model-user-guide/use-cases/best-practice-webrtc-multimodal-dialog.md)
- [显式缓存最佳实践](../../raw/model-user-guide/use-cases/explicit-cache-guide.md)
- [通过WebRTC使用qwen3.5-omni-plus-realtime实现实时通话](../../raw/model-user-guide/use-cases/best-practice-webrtc-omni-realtime.md)
- [通过AOQ使用qwen3.5-omni-plus-realtime实现实时通话](../../raw/model-user-guide/use-cases/best-practice-aoq-omni-realtime.md)
- [DeepSeek-硅基流动](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/siliconflow-deepseek-api.md)
- [DeepSeek-阿里云](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/deepseek-api.md)
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



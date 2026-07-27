# use cases

百炼平台的 use cases 覆盖从多模态内容生成、智能体工作流构建到深度研究与教育辅助等核心场景，为开发者提供开箱即用的端到端解决方案。所有方案均基于百炼托管模型服务（如 Qwen 系列、Wan2.7、HappyHorse）或第三方模型集成能力，支持函数计算、知识库、RAG 等基础设施联动，强调可部署性与工程落地性。

## 支持的模型/功能

百炼平台支持两类模型能力：**原生模型**与**第三方直供模型**。  
- **原生模型**：包括 `qwen3-vl-plus`（用于解题批改）、`qwen-deep-research`（用于深度报告生成）、`wan2.7` 与 `happyhorse`（用于文生视频/图生视频），以及 `qwen3.7-plus/max/flash` 等通用大模型。这些模型深度集成于百炼控制台，支持一键部署、自定义微调与评测 [HappyHorse 打造一站式影视创作平台](../../raw/model-user-guide/use-cases/infinite-canvas.md)。  
- **第三方直供模型**：覆盖 DeepSeek（`deepseek-v4-pro`、`siliconflow/deepseek-v3.2`）、Kimi（`kimi/kimi-k3`）、GLM（`ZHIPU/GLM-5.2`）、MiniMax（`MiniMax/MiniMax-M2.7`）、MiMo（`xiaomi/mimo-v2.5-pro`）和 Step（`stepfun/step-3.7-flash`）等。所有第三方模型均需在华北2（北京）地域开通并使用对应业务空间域名，且多数支持 `enable_thinking` 或 `reasoning_effort` 参数控制推理模式 [DeepSeek-硅基流动](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/siliconflow-deepseek-api.md)。  
> **注意**：文档 13（DeepSeek-阿里云）、15（Kimi）、19（GLM）、20（MiniMax）均声明部分旧版模型将于 2026 年下架，并统一推荐迁移至 `qwen3.7-plus` 等 Qwen 新系列模型；而文档 14、16、17、18、21、23、24 均明确限定仅支持华北2（北京）地域，与文档 13/15/19 中列出的多地域接入地址存在矛盾。实际开发应以控制台开通页及最新 API 文档为准，优先采用北京地域 + 业务空间专属域名（如 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com`）[GLM-智谱](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/glm-zhipu.md)。

## 关键参数

不同任务类型依赖特定参数组合：  
- **文生图/文生视频**：`prompt`（正向提示词）与 `negative_prompt`（反向提示词）为必需字段；`prompt_extend: true`（默认）启用大模型智能扩写；`shot_type` 已废弃，多镜头需通过分镜式提示词结构控制 [文生视频/图生视频Prompt指南](../../raw/model-user-guide/use-cases/text-to-video-prompt.md)。  
- **思考模式控制**：非 OpenAI 标准参数，须通过 `extra_body`（Python SDK）或顶层参数（Node.js SDK）传入，如 `{"enable_thinking": true}` 或 `{"reasoning_effort": "max"}`。各模型参数名不一致（`enable_thinking` vs `reasoning_effort`），且默认行为不同（如 `mimo-v2.5-pro` 默认开启，`step-3.7-flash` 默认关闭）。  
- **缓存与限流**：`X-DashScope-Wait-Timeout` 头用于突发流量排队；`cache_control` 标记（Anthropic 协议）启用显式缓存，对 `system` 和最近 `user` 消息自动生效，但需注意 Claude Code 默认注入动态信息（如 git 状态）会降低跨会话命中率 [显式缓存最佳实践](../../raw/model-user-guide/use-cases/explicit-cache-guide.md)。  

## 使用方式

典型链路为：**准备资源 → 配置模型 → 编排逻辑 → 部署调用**。  
- **资源准备**：获取 API Key 并配置环境变量；开通知识库服务（RAG 场景）；上传训练数据（自定义模型）；安装依赖（如 `llama-index-llms-dashscope`、`ffmpeg`、`marp-cli`）。  
- **模型配置**：在控制台开通模型服务（如 `siliconflow/deepseek-v3.2` 或 `qwen3-vl-plus`）；设置 `base_url`（OpenAI 兼容模式需匹配地域，如北京用 `https://dashscope.aliyuncs.com/compatible-mode/v1`，新加坡需带 `WorkspaceId`）；选择合适参数（如 `stream: true` + `stream_options.include_usage: true`）。  
- **逻辑编排**：  
  - 视觉生成类：使用节点式画布（Infinite Canvas）或结构化 Prompt 公式（主体+场景+运动+美学控制）；  
  - RAG 类：通过 `DashScopeCloudIndex` 创建知识库，再调用 `as_query_engine`；  
  - 深度研究类：依赖函数计算（FC）串联多轮搜索、验证与报告生成流程。  
- **部署调用**：推荐函数计算免运维部署；生产环境需配置客户端流控（如令牌桶）与架构兜底（MQ 削峰、模型降级）应对限流 [限流应对最佳实践](../../raw/model-user-guide/use-cases/rate-limiting-best-practices.md)。

## 限制和注意事项

- **地域与模型绑定严格**：除 Qwen 系列外，绝大多数第三方模型（DeepSeek、Kimi、GLM、MiniMax、MiMo、Step）仅支持华北2（北京）地域，且必须使用该地域 API Key 及业务空间专属域名，跨地域调用将失败。  
- **限流维度双重约束**：百炼 API 同时按请求数（RPM/RPS）和 [Token](../concepts/token.md) 用量（TPM/TPS）限流，且存在动态增速限制（Traffic Burst）。单纯重试无效，必须结合 `X-DashScope-Wait-Timeout` 头或客户端自适应拥塞控制 [限流应对最佳实践](../../raw/model-user-guide/use-cases/rate-limiting-best-practices.md)。  
- **缓存确定性前提**：显式缓存要求输入完全一致（含 system [prompt](prompt.md) 动态字段），Claude Code 等工具需启用 `--exclude-dynamic-system-prompt-sections` 才能保障跨会话命中。  
- **模型生命周期管理**：第三方模型存在明确下架时间（如 Kimi-K2 系列 2026-07-09），开发者需主动规划迁移路径，避免业务中断。

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
- [Kimi](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/kimi-api.md)
- [DeepSeek](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/deepseek-api-by-vanchin.md)
- [Kimi-月之暗面](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/kimi-api-by-moonshot-ai.md)
- [GLM-智谱](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/glm-zhipu.md)
- [GLM](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/glm.md)
- [MiniMax](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/minimax-api.md)
- [MiniMax](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/minimax-api-by-minimax.md)
- [Vidu视频生成Prompt指南](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/vidu-video-generation-prompt-guide.md)
- [MiMo-小米](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/mimo.md)
- [Stepfun-阶跃星辰](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/stepfun.md)



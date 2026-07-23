# use cases

百炼平台的 use cases 覆盖从多模态内容生成、智能体构建、深度研究到教育辅助等核心场景，支持开发者基于预置模型快速落地生产级应用。所有方案均以函数计算、知识库服务、[Prompt 工程](../concepts/prompt-engineering.md)和流控机制为技术底座，强调开箱即用与可扩展性。本文档结构化梳理关键能力边界与实践要点，面向工程师提供可直接复用的技术路径。

## 支持的模型/功能

百炼提供两类模型能力：**原生模型服务**（如 `qwen3-vl-plus`、`wan2.7`、`HappyHorse`）与**第三方直供模型**（如 `kimi/kimi-k3`、`ZHIPU/GLM-5.2`、`stepfun/step-3.7-flash`）。前者深度集成于视觉创作、文档转视频等端到端方案；后者通过 [OpenAI 兼容接口](../concepts/openai-compatible-api.md)或 DashScope SDK 接入，支持思考模式（`enable_thinking`）、长上下文（GLM-5.2 支持 1M tokens）及多模态输入（Kimi-K2.7-code 等）[原文标题](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/kimi-api-by-moonshot-ai.md)。  
> **注意**：多个第三方模型文档存在下架时间冲突——`deepseek-v3` 系列将于 2026 年 10 月 10 日下架 [原文标题](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/deepseek-api.md)，而 `kimi-k2-instruct`、`glm-4.6`、`MiniMax-M2.1` 均标注为 2026 年 7 月 9 日下架 [原文标题](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/kimi-api.md)。推荐统一迁移至 `qwen3.7-plus` 等阿里云自研模型。

## 关键参数

- **Prompt 控制**：文生图/文生视频均依赖结构化提示词公式，基础公式为 `主体 + 场景 + 运动`（视频）或 `主体 + 场景 + 风格`（图像），进阶公式需补充美学控制、镜头语言与氛围词 [原文标题](../../raw/model-user-guide/use-cases/text-to-image-prompt.md)。  
- **模型特有参数**：`enable_thinking`（DeepSeek、MiMo、Stepfun）、`reasoning_effort`（Kimi）、`preserve_thinking`（Kimi-K2.6/K2.5）等非 OpenAI 标准参数需通过 `extra_body`（Python SDK）或顶层字段（Node.js SDK）传入。  
- **缓存与限流**：显式缓存通过 `cache_control` 标记实现确定性命中；限流维度包括 RPM/TPM（分钟级配额）、RPS/TPS（瞬时频率）及 Traffic Burst（增速限制）[原文标题](../../raw/model-user-guide/use-cases/rate-limiting-best-practices.md)。

## 使用方式

1. **方案级部署**：影视创作、AI 客服、深度研究等场景提供一键部署模板（如函数计算 + 百炼模型组合），15–30 分钟完成环境搭建 [原文标题](../../raw/model-user-guide/use-cases/infinite-canvas.md)。  
2. **代码级集成**：  
   - RAG 应用需通过 `llama-index-indices-managed-dashscope` 初始化知识库索引，并调用 `DashScopeCloudRetriever` 或 `as_query_engine`；  
   - 第三方模型调用需配置地域专属 `base_url`（如华北2 北京使用 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`），并处理 `reasoning_content` 流式字段；  
   - 文档转视频需依赖 FFmpeg、Marp 及浏览器渲染引擎，分四步执行：文档切片 → 生成演示文稿 → 合成语音字幕 → 剪辑嵌入 [原文标题](../../raw/model-user-guide/use-cases/use-llm-to-convert-document-to-video.md)。  

## 限制和注意事项

- **地域与权限约束**：多数第三方模型（DeepSeek 硅基流动版、Kimi 月之暗面版、MiniMax、MiMo、Stepfun）仅支持华北2（北京）地域，且需对应地域的 API Key [原文标题](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/siliconflow-deepseek-api.md)。  
- **文件与资源限制**：DashScopeParse 解析器单个 PDF/DOCX 文件上限为 100MB 且页数 ≤1000；无限画布方案依赖函数计算弹性伸缩，但需自行管理冷启动延迟。  
- **缓存与成本权衡**：显式缓存首次写入产生 25% 额外开销，但后续命中可降本 90%；若 Agent 中 system [prompt](prompt.md) 含动态信息（如当前目录、git 状态），需启用 `--exclude-dynamic-system-prompt-sections` 提升跨会话命中率。  
- **模型输出解析**：开启思考模式后，`reasoning_content` 与 `content` 字段需分别捕获，且 `reasoning_content` 可能为空（如 MiniMax-M2.5 示例中未返回该字段），需做健壮性判断。

## 来源文档

- [HappyHorse 打造一站式影视创作平台](../../raw/model-user-guide/use-cases/infinite-canvas.md)
- [高效搭建 AI 智能体与工作流应用](../../raw/model-user-guide/use-cases/build-ai-applications-based-on-alibaba-cloud-model-studio.md)
- [深度研究：生成你的独家洞察报告](../../raw/model-user-guide/use-cases/deep-research.md)
- [AI 解题 + 批改：推动课程教学智变](../../raw/model-user-guide/use-cases/ai-homework-helper.md)
- [文生文Prompt指南](../../raw/model-user-guide/use-cases/prompt-engineering-guide.md)
- [文生视频/图生视频Prompt指南](../../raw/model-user-guide/use-cases/text-to-video-prompt.md)
- [基于LlamaIndex构建RAG应用](../../raw/model-user-guide/use-cases/build-rag-applications-based-on-llamaindex.md)
- [文生图Prompt指南](../../raw/model-user-guide/use-cases/text-to-image-prompt.md)
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
- [Vidu视频生成Prompt指南](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/vidu-video-generation-prompt-guide.md)
- [MiMo-小米](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/mimo.md)
- [Stepfun-阶跃星辰](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/stepfun.md)



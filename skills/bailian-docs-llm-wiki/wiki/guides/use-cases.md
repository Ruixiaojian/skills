# use cases

百炼平台的 use cases 覆盖从基础文本生成、多模态内容创作到复杂智能体编排的全栈能力。开发者可基于预置模型快速构建生产级应用，也可通过自定义模型、RAG、显式缓存等机制深度优化业务逻辑。所有方案均提供开箱即用的部署路径与明确的成本预期。

## 支持的模型/功能

百炼支持两类核心能力：**原生模型服务**与**第三方模型集成**。

- **原生模型**：包括 `qwen3-vl-plus`（文生图/图生图）、`qwen3.5-omni-plus-realtime`（实时音视频）、`qwen3.7-max`（通用大模型）、`wan2.7`（文生视频）及 `HappyHorse`（视频生成）等，覆盖文本、图像、视频、语音全模态。其中 `qwen3-vl-plus` 在 MathVista、MMMU 等评测中达到 SOTA 水平 [AI 解题 + 批改：推动课程教学智变](../../raw/model-user-guide/use-cases/ai-homework-helper.md)。
- **第三方模型**：通过 [OpenAI 兼容接口](../concepts/openai-compatible-interface.md)或 DashScope SDK 接入 DeepSeek、Kimi、GLM、MiniMax、MiMo、Stepfun 等厂商模型。需注意地域限制与下架时间——例如 `deepseek-v3` 系列将于 2026 年 10 月 10 日下架 [DeepSeek-阿里云](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/deepseek-api.md)，而 `kimi-k2-thinking` 等模型则于 2026 年 7 月 9 日下架 [Kimi](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/kimi-api.md)。
- **专用能力套件**：如 `multimodal-dialog`（多模态交互套件）面向 AI 眼镜、学习机等硬件场景；`Qwen-Deep-Research` 提供自动规划研究路径、多源交叉验证与结构化报告生成能力 [深度研究：生成你的独家洞察报告](../../raw/model-user-guide/use-cases/deep-research.md)。

> **注意**：文档 16、19、21、23 中均声明部分第三方模型将于 2026 年集中下架，但各文档推荐的替代模型不一致（如 `qwen3.7-plus`、`qwen3.8-max`、`qwen3.7-flash`），实际选型应以[模型市场](https://bailian.console.aliyun.com/cn-beijing/?tab=model#/model-market)最新状态为准。

## 关键参数

不同任务类型依赖特定参数控制输出质量与行为：

- **文生文**：使用 Prompt 框架（背景/目的/风格/语气/受众/输出）结构化输入；支持一键优化工具扩写 [文生文Prompt指南](../../raw/model-user-guide/use-cases/prompt-engineering-guide.md)。
- **文生图/图生图**：`prompt`（正向提示词）、`negative_prompt`（反向提示词），V2 版本支持 `prompt_extend: true` 启用智能改写 [文生图Prompt指南](../../raw/model-user-guide/use-cases/text-to-image-prompt.md)。
- **文生视频/图生视频**：除基础 `prompt` 外，支持 `shot_type`（已弃用）、多镜头公式（含时间戳与分镜内容）、声音公式（人声/音效/BGM）及参考生视频公式（`图n`/`视频n` 指代） [文生视频/图生视频Prompt指南](../../raw/model-user-guide/use-cases/text-to-video-prompt.md)。
- **实时通话**：WebRTC 场景需设置 `server_vad` 模式；AOQ SDK 需通过 AppServer 获取 [Token](../concepts/token.md)；所有实时模型均支持 `enable_thinking` 或 `reasoning_effort` 控制推理过程输出 [通过AOQ使用qwen3.5-omni-plus-realtime实现实时通话](../../raw/model-user-guide/use-cases/best-practice-aoq-omni-realtime.md)。
- **缓存与限流**：显式缓存通过 `cache_control` 标记实现确定性命中；限流响应需结合 `X-DashScope-Wait-Timeout` 请求头与客户端超时调整 [显式缓存最佳实践](../../raw/model-user-guide/use-cases/explicit-cache-guide.md)、[限流应对最佳实践](../../raw/model-user-guide/use-cases/rate-limiting-best-practices.md)。

## 使用方式

典型集成路径分为三类：

1. **低代码编排**：通过无限画布节点式拖拽（文本/图像/视频节点），结合 AI 导演对话式创建工作流，适用于影视创作、电商设计等场景 [HappyHorse 打造一站式影视创作平台](../../raw/model-user-guide/use-cases/infinite-canvas.md)。
2. **SDK/API 直接调用**：
   - OpenAI 兼容模式：配置 `base_url` 为地域专属域名（如 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`），传入 `model` 名称与 `messages`。
   - DashScope 原生模式：使用 `dashscope.base_http_api_url` 指向对应地域 API 端点。
3. **框架集成**：如基于 LlamaIndex 构建 RAG 应用，需安装 `llama-index-indices-managed-dashscope`，通过 `DashScopeCloudIndex` 创建知识库并获取 `retriever` 或 `query_engine` [基于LlamaIndex构建RAG应用](../../raw/model-user-guide/use-cases/build-rag-applications-based-on-llamaindex.md)。

## 限制和注意事项

- **地域与权限约束**：多数第三方模型（DeepSeek、Kimi、GLM、MiniMax、MiMo、Stepfun）仅支持华北2（北京）地域，且需该地域 API Key [DeepSeek-硅基流动](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/siliconflow-deepseek-api.md)、[Kimi-月之暗面](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/kimi-api-by-moonshot-ai.md)。
- **资源与成本**：函数计算方案（如无限画布、深度研究）标注了典型体验成本（如 30 元、6 元），但强调“实际费用可能因规格不同而变化”；显式缓存首次写入产生 25% 额外开销，后续命中节省 90% 成本 [限流应对最佳实践](../../raw/model-user-guide/use-cases/rate-limiting-best-practices.md)。
- **技术兼容性**：WebRTC 方案受浏览器 CORS 限制，Demo 中需 curl 代理 SDP 交换；正式环境必须由业务 AppServer 代理 [通过WebRTC使用qwen3.5-omni-plus-realtime实现实时通话](../../raw/model-user-guide/use-cases/best-practice-webrtc-omni-realtime.md)。
- **模型生命周期**：所有第三方模型文档均明确标注下架日期与迁移建议，开发者需主动规划模型替换路径，避免服务中断。

## 来源文档

- [HappyHorse 打造一站式影视创作平台](../../raw/model-user-guide/use-cases/infinite-canvas.md)
- [高效搭建 AI 智能体与工作流应用](../../raw/model-user-guide/use-cases/build-ai-applications-based-on-alibaba-cloud-model-studio.md)
- [文生文Prompt指南](../../raw/model-user-guide/use-cases/prompt-engineering-guide.md)
- [深度研究：生成你的独家洞察报告](../../raw/model-user-guide/use-cases/deep-research.md)
- [AI 解题 + 批改：推动课程教学智变](../../raw/model-user-guide/use-cases/ai-homework-helper.md)
- [文生图Prompt指南](../../raw/model-user-guide/use-cases/text-to-image-prompt.md)
- [基于LlamaIndex构建RAG应用](../../raw/model-user-guide/use-cases/build-rag-applications-based-on-llamaindex.md)
- [文生视频/图生视频Prompt指南](../../raw/model-user-guide/use-cases/text-to-video-prompt.md)
- [自定义模型调优、部署与评测](../../raw/model-user-guide/use-cases/model-training-best-practices.md)
- [借助大模型将文档转换为视频](../../raw/model-user-guide/use-cases/use-llm-to-convert-document-to-video.md)
- [限流应对最佳实践 ](../../raw/model-user-guide/use-cases/rate-limiting-best-practices.md)
- [显式缓存最佳实践](../../raw/model-user-guide/use-cases/explicit-cache-guide.md)
- [通过WebRTC使用qwen3.5-omni-plus-realtime实现实时通话](../../raw/model-user-guide/use-cases/best-practice-webrtc-omni-realtime.md)
- [通过WebRTC使用多模态交互套件实现实时通话](../../raw/model-user-guide/use-cases/best-practice-webrtc-multimodal-dialog.md)
- [通过AOQ使用qwen3.5-omni-plus-realtime实现实时通话](../../raw/model-user-guide/use-cases/best-practice-aoq-omni-realtime.md)
- [DeepSeek-阿里云](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/deepseek-api.md)
- [DeepSeek-硅基流动](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/siliconflow-deepseek-api.md)
- [DeepSeek](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/deepseek-api-by-vanchin.md)
- [Kimi](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/kimi-api.md)
- [Kimi-月之暗面](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/kimi-api-by-moonshot-ai.md)
- [GLM](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/glm.md)
- [GLM-智谱](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/glm-zhipu.md)
- [MiniMax](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/minimax-api.md)
- [Vidu视频生成Prompt指南](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/vidu-video-generation-prompt-guide.md)
- [MiniMax](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/minimax-api-by-minimax.md)
- [MiMo-小米](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/mimo.md)
- [Stepfun-阶跃星辰](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/stepfun.md)



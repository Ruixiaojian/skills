# use cases

百炼平台的 use cases 覆盖从多模态内容生成、智能体与工作流构建，到深度研究、教育辅助及第三方模型集成等核心场景。这些用例均基于百炼统一 API 与模型服务层，支持开发者通过标准化接口快速落地生产级应用，无需关注底层基础设施运维。所有方案均提供开箱即用的部署路径与明确的成本预估。

## 支持的模型/功能

百炼提供两类核心能力：**阿里云自研模型**（如 Qwen 系列、Wan2.7、HappyHorse、Qwen3-VL）和**第三方直供模型**（如 DeepSeek、Kimi、GLM、MiniMax、MiMo、Stepfun、Vidu）。  
- **视觉生成**：万相（文生图 V1/V2、文生视频、图生视频）、HappyHorse（视频生成）、Vidu（视频生成）支持结构化提示词控制，覆盖主体、场景、运动、运镜、风格等维度 [Vidu视频生成Prompt指南](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/vidu-video-generation-prompt-guide.md)。  
- **多模态理解与生成**：Qwen3-VL 系列模型支撑解题与批改场景，具备 MathVista、MMMU 等权威评测 SOTA 能力 [AI 解题 + 批改：推动课程教学智变](../../raw/model-user-guide/use-cases/ai-homework-helper.md)。  
- **深度推理与研究**：Qwen-Deep-Research 模型实现自动路径规划、多源交叉验证与结构化报告生成 [深度研究：生成你的独家洞察报告](../../raw/model-user-guide/use-cases/deep-research.md)。  
- **第三方模型集成**：DeepSeek（v3/v4-pro）、Kimi（k2.6/k2.7-code）、GLM（5.2）、MiniMax（M2.5/M2.7）、MiMo（v2.5-pro）、Stepfun（step-3.7-flash）均通过 [OpenAI 兼容接口](../concepts/openai-compatible-api.md)或 DashScope SDK 接入，支持 `enable_thinking` 等非标参数控制推理模式。

> **注意**：多个第三方模型文档（如 [DeepSeek-阿里云](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/deepseek-api.md)、[GLM](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/glm.md)、[MiniMax](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/minimax-api.md)）均声明部分旧版本模型（如 deepseek-v3、glm-4.6、MiniMax-M2.1）将于 2026 年 7 月 9 日下架，且推荐迁移至 Qwen3 系列。但各文档未统一说明迁移后是否保留原模型特性（如上下文长度、联网搜索），实际选型需以控制台最新模型详情页为准。

## 关键参数

- **Prompt 控制**：  
  - 文生文：推荐使用 [Prompt 框架](../../raw/model-user-guide/use-cases/prompt-engineering-guide.md)（背景/目的/风格/语气/受众/输出），避免模糊指令；平台提供一键优化工具，但会消耗 Token。  
  - 文生图/视频：采用分层公式（基础：主体+场景+运动；进阶：主体描述+场景描述+运动描述+美学控制+风格化），支持 `prompt_extend`（V2 默认开启）、`negative_prompt`、`cache_control` 等参数。  
- **思考模式控制**：DeepSeek、Kimi、GLM、MiMo、Stepfun 等模型均支持 `enable_thinking` 参数（OpenAI SDK 需通过 `extra_body` 传入），开启后返回 `reasoning_content` 字段；部分模型（如 MiMo-v2.5-pro）默认开启，GLM-5.2 还支持 `reasoning_effort` 控制深度。  
- **缓存与限流**：显式缓存通过 `cache_control` 标记实现确定性命中；限流应对需结合 `X-DashScope-Wait-Timeout` 请求头（仅对 Traffic Burst 有效）与客户端流控策略。

## 使用方式

1. **模型调用**：  
   - OpenAI 兼容模式：配置 `base_url`（如 `https://dashscope.aliyuncs.com/compatible-mode/v1`），使用标准 `chat.completions.create` 接口。  
   - DashScope 原生模式：直接调用 `text-generation/generation` 或 `multimodal-generation/generation` 端点，需按模型类型选择 HTTP 地址与 SDK 配置。  
2. **工作流编排**：  
   - 可视化节点编排（如 HappyHorse 无限画布方案）支持拖拽连接文本、图像、视频生成节点 [HappyHorse 打造一站式影视创作平台](../../raw/model-user-guide/use-cases/infinite-canvas.md)。  
   - RAG 应用通过 LlamaIndex 集成百炼知识库服务，使用 `DashScopeCloudIndex` 创建索引，`DashScopeCloudRetriever` 检索，`as_query_engine` 构建问答引擎。  
3. **部署与评测**：  
   - 自定义模型需完成调优→部署→评测三阶段闭环，部署为独占实例后方可调用；评测支持自动化指标计算与人工模板评估。

## 限制和注意事项

- **地域与权限约束**：多数第三方模型（DeepSeek-硅基流动、Kimi、GLM-智谱、MiniMax、MiMo、Stepfun）仅支持华北2（北京）地域，且需对应地域的 API Key；部分模型（如 Kimi、GLM）在新加坡/东京等地域需配置 `WorkspaceId` 域名。  
- **输入输出限制**：  
  - DashScopeParse 文档解析支持单文件 ≤100MB、≤1000 页；函数计算部署方案有内存与超时限制（如深度研究方案为 15 分钟）。  
  - Vidu 视频生成对提示词复杂度敏感，需避免主体物过多或句式模糊；万相图生视频需注意原始图片与运动描述的逻辑一致性（如火车方向需通过比例关系强化）。  
- **成本与计费**：  
  - 显式缓存首次写入产生 25% 额外开销，但后续命中可降本 90%；若未发生命中，总体成本高于不启用缓存。  
  - 第三方模型调用按 Token 计费，部分模型（如 GLM 系列）提供 100 万免费 Token，但需注意免费额度是否跨模型共享。  
- **兼容性风险**：`enable_thinking` 等非 OpenAI 标准参数在不同 SDK 实现中存在差异（如 Python SDK 用 `extra_body`，Node.js SDK 作顶层参数），需严格参照各模型文档示例代码。

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
- [显式缓存最佳实践](../../raw/model-user-guide/use-cases/explicit-cache-guide.md)
- [限流应对最佳实践 ](../../raw/model-user-guide/use-cases/rate-limiting-best-practices.md)
- [DeepSeek-阿里云](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/deepseek-api.md)
- [DeepSeek-硅基流动](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/siliconflow-deepseek-api.md)
- [DeepSeek](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/deepseek-api-by-vanchin.md)
- [Kimi-月之暗面](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/kimi-api-by-moonshot-ai.md)
- [Kimi](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/kimi-api.md)
- [GLM](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/glm.md)
- [MiniMax](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/minimax-api.md)
- [GLM-智谱](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/glm-zhipu.md)
- [MiniMax](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/minimax-api-by-minimax.md)
- [Vidu视频生成Prompt指南](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/vidu-video-generation-prompt-guide.md)
- [MiMo-小米](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/mimo.md)
- [Stepfun-阶跃星辰](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/stepfun.md)



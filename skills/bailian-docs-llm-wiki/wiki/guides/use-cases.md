# use cases

百炼平台提供覆盖文本、图像、视频、语音、多模态及智能体工作流的全栈 AI 应用能力，支持从 [Prompt 工程](../concepts/prompt-engineering.md)、RAG 构建到实时音视频交互的完整开发链路。开发者可基于预置模型快速验证场景，也可通过自定义训练与第三方模型集成满足深度业务需求。所有能力均通过统一 API 接口和控制台可视化工具交付，无需底层基础设施运维。

## 支持的模型/功能

百炼平台支持三类模型调用路径：  
- **百炼原生模型**：包括 `qwen3.7-plus`、`qwen3.7-max`、`qwen3.6-flash` 等最新 Qwen 系列大模型，以及 `qwen3-vl-plus` 视觉多模态模型（见 [AI 解题 + 批改：推动课程教学智变](../../raw/model-user-guide/use-cases/ai-homework-helper.md)）；  
- **第三方直供模型**：通过百炼统一接入层调用 DeepSeek、Kimi、GLM、MiniMax、MiMo、Stepfun 等厂商模型，均支持 OpenAI 兼容协议与思考模式（`enable_thinking`/`reasoning_effort`），例如 `kimi/kimi-k3` 和 `stepfun/step-3.7-flash`；  
- **视觉生成模型**：万相系列（`wan2.7`、`wan2.6`）支持文生图、图生视频、参考生视频等能力，配合 HappyHorse 实现影视级多镜头叙事（见 [HappyHorse 打造一站式影视创作平台](../../raw/model-user-guide/use-cases/infinite-canvas.md)）；  
- **专用模型服务**：如 `Qwen-Deep-Research` 用于深度情报分析（见 [深度研究：生成你的独家洞察报告](../../raw/model-user-guide/use-cases/deep-research.md)）、`qwen3.5-omni-plus-realtime` 专为 WebRTC 实时音视频优化。

> **注意**：文档 16、18、20、23 中均声明部分第三方模型（如 `deepseek-v3.*`、`kimi-k2-*`、`glm-4.*`、`MiniMax-M2.1`）将于 2026 年下架，且明确推荐迁移至 `qwen3.7-plus` 等 Qwen 新模型。该信息具有一致性，非矛盾项，属平台演进规划。

## 关键参数

不同模型类型对应关键参数如下：  
- **文本模型通用参数**：`model`（模型标识符）、`messages`（对话历史）、`stream`（流式开关）、`temperature`、`max_tokens`；  
- **思考模式参数**：非 OpenAI 标准字段，需通过 `extra_body`（Python SDK）或顶层参数（Node.js SDK）传入，如 `enable_thinking: true` 或 `reasoning_effort: "max"`；  
- **视觉生成参数**：  
  - 文生图：`prompt`（正向提示词）、`negative_prompt`（反向提示词）、`prompt_extend`（是否启用大模型智能扩写，默认 `true`）；  
  - 文生视频：支持 `motion`、`aesthetic_control`（光源/运镜）、`style` 及 `sound_description`（人声/音效/BGM）；  
  - Vidu 视频生成：支持 `dynamic_control`（大/中/小动态）、`camera_movement`（推/拉/升/降/固定）、`video_style`（2D动漫/3D渲染/水墨等）；  
- **实时音视频参数**：WebRTC 模式强制使用 `server_vad`（服务端语音活动检测），不支持手动 VAD；AOQ SDK 则需通过 AppServer 获取 [Token](../concepts/token.md) 鉴权。

## 使用方式

- **低代码构建**：通过控制台“应用编排”拖拽节点（如 RAG、Agent、Function Call），结合 [高效搭建 AI 智能体与工作流应用](../../raw/model-user-guide/use-cases/build-ai-applications-based-on-alibaba-cloud-model-studio.md) 中的电商客服案例快速上线；  
- **[Prompt 工程](../concepts/prompt-engineering.md)化**：遵循结构化框架（背景/目的/风格/语气/受众/输出），利用平台 Prompt 一键优化工具扩写（见 [文生文Prompt指南](../../raw/model-user-guide/use-cases/prompt-engineering-guide.md)）；  
- **RAG 开发**：基于 LlamaIndex 集成百炼知识库服务，通过 `DashScopeCloudIndex` 创建索引，`DashScopeCloudRetriever` 检索，`as_query_engine` 构建问答引擎；  
- **实时交互接入**：浏览器端用 WebRTC（需处理 SDP 代理限制），移动端用 AOQ SDK（Android/iOS/HarmonyOS），均需前置获取 Workspace ID、App ID 与 [Token](../concepts/token.md)；  
- **缓存与限流控制**：显式缓存通过 `cache_control` 标记实现确定性命中（适用于 Agent 长上下文管理）；限流应对优先配置 `X-DashScope-Wait-Timeout` 请求头实现服务端排队（见 [限流应对最佳实践](../../raw/model-user-guide/use-cases/rate-limiting-best-practices.md)）。

## 限制和注意事项

- **地域与域名约束**：所有第三方模型（DeepSeek、Kimi、GLM、MiniMax、MiMo、Stepfun）均明确限定仅华北2（北京）地域可用，且强烈建议使用业务空间专属域名 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com` 替代通用域名以获得更高稳定性；  
- **[Token](../concepts/token.md) 用量监控**：API 调用受 RPM/TPM、RPS/TPS 及 Traffic Burst 三重限流，需结合 [限流应对最佳实践](../../raw/model-user-guide/use-cases/rate-limiting-best-practices.md) 中的客户端流控与架构兜底策略；  
- **视觉模型输入限制**：`DashScopeParse` 文档解析器要求单个文件 ≤100MB 且 ≤1000 页；万相文生图 V2 的 `prompt` 长度上限为 1024 字符；  
- **缓存适用边界**：显式缓存仅对 Anthropic 协议接入的工具（Claude Code、OpenCode、OpenClaw）原生支持，普通 DashScope API 需手动构造 `cache_control`；  
- **模型生命周期**：第三方模型存在明确下架时间（2026 年中至年末），生产环境应避免依赖已标记为“将下架”的模型版本。

## 来源文档

- [高效搭建 AI 智能体与工作流应用](../../raw/model-user-guide/use-cases/build-ai-applications-based-on-alibaba-cloud-model-studio.md)
- [深度研究：生成你的独家洞察报告](../../raw/model-user-guide/use-cases/deep-research.md)
- [AI 解题 + 批改：推动课程教学智变](../../raw/model-user-guide/use-cases/ai-homework-helper.md)
- [文生文Prompt指南](../../raw/model-user-guide/use-cases/prompt-engineering-guide.md)
- [文生图Prompt指南](../../raw/model-user-guide/use-cases/text-to-image-prompt.md)
- [文生视频/图生视频Prompt指南](../../raw/model-user-guide/use-cases/text-to-video-prompt.md)
- [HappyHorse 打造一站式影视创作平台](../../raw/model-user-guide/use-cases/infinite-canvas.md)
- [自定义模型调优、部署与评测](../../raw/model-user-guide/use-cases/model-training-best-practices.md)
- [限流应对最佳实践 ](../../raw/model-user-guide/use-cases/rate-limiting-best-practices.md)
- [借助大模型将文档转换为视频](../../raw/model-user-guide/use-cases/use-llm-to-convert-document-to-video.md)
- [显式缓存最佳实践](../../raw/model-user-guide/use-cases/explicit-cache-guide.md)
- [通过WebRTC使用多模态交互套件实现实时通话](../../raw/model-user-guide/use-cases/best-practice-webrtc-multimodal-dialog.md)
- [通过WebRTC使用qwen3.5-omni-plus-realtime实现实时通话](../../raw/model-user-guide/use-cases/best-practice-webrtc-omni-realtime.md)
- [通过AOQ使用qwen3.5-omni-plus-realtime实现实时通话](../../raw/model-user-guide/use-cases/best-practice-aoq-omni-realtime.md)
- [基于LlamaIndex构建RAG应用](../../raw/model-user-guide/use-cases/build-rag-applications-based-on-llamaindex.md)
- [DeepSeek-阿里云](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/deepseek-api.md)
- [DeepSeek-硅基流动](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/siliconflow-deepseek-api.md)
- [Kimi](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/kimi-api.md)
- [Kimi-月之暗面](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/kimi-api-by-moonshot-ai.md)
- [GLM](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/glm.md)
- [GLM-智谱](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/glm-zhipu.md)
- [DeepSeek](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/deepseek-api-by-vanchin.md)
- [MiniMax](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/minimax-api.md)
- [Vidu视频生成Prompt指南](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/vidu-video-generation-prompt-guide.md)
- [MiMo-小米](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/mimo.md)
- [MiniMax](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/minimax-api-by-minimax.md)
- [Stepfun-阶跃星辰](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/stepfun.md)



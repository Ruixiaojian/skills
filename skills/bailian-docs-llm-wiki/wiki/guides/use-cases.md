# use cases

百炼平台的 use cases 覆盖从基础文本生成到[多模态](../concepts/multimodal.md)实时交互的全栈能力，支持开发者快速构建生产级 AI 应用。核心价值在于提供开箱即用的模型服务、结构化提示工程指南、灵活的流控与缓存机制，以及面向硬件终端的低延迟交互方案。所有用例均基于阿里云统一 API 体系，可按需组合编排。

## 支持的模型/功能

百炼平台提供两类核心能力：**原生模型服务**与**第三方模型集成**。

- **原生模型**：包括 Qwen 系列（如 `qwen3.7-max`、`qwen3.5-omni-plus-realtime`）、万相系列（`wan2.7` 视频生成、`wan2.6` 多镜头视频）、DeepResearch（`qwen-deep-research`）等，覆盖文生文、文生图、文生视频、深度研究、实时音视频通话等场景。
- **第三方模型集成**：支持 DeepSeek（硅基流动、阿里云、快手万擎三路供应商）、Kimi（月之暗面）、GLM（智谱）、MiniMax、MiMo（小米）、Stepfun（阶跃星辰）等，均通过 [OpenAI 兼容接口](../concepts/openai-compatibility.md)或 DashScope SDK 接入。各模型支持 `enable_thinking` 或 `reasoning_effort` 参数控制推理过程输出，详见 [DeepSeek-硅基流动](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/siliconflow-deepseek-api.md)、[Kimi-月之暗面](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/kimi-api-by-moonshot-ai.md) 和 [Stepfun-阶跃星辰](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/stepfun.md)。

> **注意**：多个第三方模型文档（如 [DeepSeek-阿里云](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/deepseek-api.md)、[GLM](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/glm.md)、[MiniMax](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/minimax-api.md)）均声明部分旧版本模型将于 2026 年下架，并推荐迁移至 Qwen 系列。该信息为统一策略，非矛盾，开发者应优先选用 `qwen3.7-plus` 等新模型。

## 关键参数

不同模态任务的关键参数设计高度结构化，便于精准控制输出：

- **文生文**：核心为 `messages` 数组，支持 `system`/`user`/`assistant` 角色；高级能力依赖 `extra_body` 传入非标准参数（如 `enable_thinking`），详见 [文生文Prompt指南](../../raw/model-user-guide/use-cases/prompt-engineering-guide.md)。
- **文生图/图生图**：`prompt`（正向描述）与 `negative_prompt`（反向过滤）为必需字段；`prompt_extend`（默认 `true`）启用大模型智能扩写，显著提升画面质量。
- **文生视频/图生视频**：除 `prompt` 外，`wan2.7` 支持多镜头公式（含时间戳与分镜内容）、声音公式（人声/音效/BGM）及参考生视频公式（`图n`/`视频n` 指代），详见 [文生视频/图生视频Prompt指南](../../raw/model-user-guide/use-cases/text-to-video-prompt.md)。
- **实时音视频**：WebRTC 模式需配置 `server_vad` 模式，AOQ 模式需通过 AppServer 获取 [Token](../concepts/token.md) 并建立连接，详见 [通过WebRTC使用qwen3.5-omni-plus-realtime实现实时通话](../../raw/model-user-guide/use-cases/best-practice-webrtc-omni-realtime.md) 和 [通过AOQ使用qwen3.5-omni-plus-realtime实现实时通话](../../raw/model-user-guide/use-cases/best-practice-aoq-omni-realtime.md)。

## 使用方式

典型工作流遵循“准备→调用→处理”三步法：

1. **准备阶段**：获取并安全配置 `DASHSCOPE_API_KEY`（推荐环境变量）；开通对应模型服务（如在控制台点击“立即开通”）；对于[多模态](../concepts/multimodal.md)或实时交互场景，还需创建业务空间、应用并获取 `Workspace ID` 和 `App ID`。
2. **调用阶段**：
   - 文本类任务：直接调用 `/chat/completions`（OpenAI 兼容）或 `/generation`（DashScope）端点；
   - 视频生成：构造符合公式结构的 `prompt`，提交至 `text-to-video` API；
   - 实时交互：WebRTC 需浏览器端创建 `RTCPeerConnection` 并交换 SDP；AOQ 需客户端集成 SDK 并由 AppServer 代理鉴权。
3. **处理阶段**：流式响应需按 `delta.reasoning_content` 与 `delta.content` 分离处理思考过程与最终答案；音视频流需绑定至 `<audio>` 或 `<video>` 元素播放；生成结果（图像/视频）需按 API 返回的 URL 下载或直接嵌入。

## 限制和注意事项

- **限流策略**：百炼 API 同时受 RPM（每分钟请求数）、TPM（每分钟 [Token](../concepts/token.md) 数）和 Traffic Burst（瞬时增速）三重限制。突发流量应首选 `X-DashScope-Wait-Timeout` 请求头实现服务端排队，而非简单重试，详见 [限流应对最佳实践](../../raw/model-user-guide/use-cases/rate-limiting-best-practices.md)。
- **缓存机制**：显式缓存（`cache_control`）仅对 Anthropic 协议接入的工具（如 Claude Code、OpenCode）原生支持，且需确保请求端点为 `/apps/anthropic`；普通 OpenAI 兼容调用不支持此特性。
- **地域与域名**：第三方模型（DeepSeek、Kimi、GLM 等）多数仅限华北2（北京）地域使用，且强烈推荐迁移到业务空间专属域名 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com`，以获得更高稳定性与性能。
- **硬件兼容性**：WebRTC 方案依赖浏览器麦克风/摄像头权限，且 Demo 中 SDP 交换需后端代理规避 CORS；AOQ 方案需按 Android/iOS/HarmonyOS 平台分别集成 SDK 并声明运行时权限。

## 来源文档

- [HappyHorse 打造一站式影视创作平台](../../raw/model-user-guide/use-cases/infinite-canvas.md)
- [高效搭建 AI 智能体与工作流应用](../../raw/model-user-guide/use-cases/build-ai-applications-based-on-alibaba-cloud-model-studio.md)
- [文生文Prompt指南](../../raw/model-user-guide/use-cases/prompt-engineering-guide.md)
- [文生图Prompt指南](../../raw/model-user-guide/use-cases/text-to-image-prompt.md)
- [文生视频/图生视频Prompt指南](../../raw/model-user-guide/use-cases/text-to-video-prompt.md)
- [基于LlamaIndex构建RAG应用](../../raw/model-user-guide/use-cases/build-rag-applications-based-on-llamaindex.md)
- [自定义模型调优、部署与评测](../../raw/model-user-guide/use-cases/model-training-best-practices.md)
- [深度研究：生成你的独家洞察报告](../../raw/model-user-guide/use-cases/deep-research.md)
- [借助大模型将文档转换为视频](../../raw/model-user-guide/use-cases/use-llm-to-convert-document-to-video.md)
- [限流应对最佳实践 ](../../raw/model-user-guide/use-cases/rate-limiting-best-practices.md)
- [显式缓存最佳实践](../../raw/model-user-guide/use-cases/explicit-cache-guide.md)
- [通过WebRTC使用多模态交互套件实现实时通话](../../raw/model-user-guide/use-cases/best-practice-webrtc-multimodal-dialog.md)
- [通过WebRTC使用qwen3.5-omni-plus-realtime实现实时通话](../../raw/model-user-guide/use-cases/best-practice-webrtc-omni-realtime.md)
- [通过AOQ使用qwen3.5-omni-plus-realtime实现实时通话](../../raw/model-user-guide/use-cases/best-practice-aoq-omni-realtime.md)
- [使用 AOQ 接入 fun-asr-realtime 实现实时语音识别](../../raw/model-user-guide/use-cases/real-time-speech-recognition-using-aoq-access-fun-asr-realtime.md)
- [DeepSeek-硅基流动](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/siliconflow-deepseek-api.md)
- [DeepSeek-阿里云](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/deepseek-api.md)
- [DeepSeek](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/deepseek-api-by-vanchin.md)
- [Kimi-月之暗面](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/kimi-api-by-moonshot-ai.md)
- [Kimi](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/kimi-api.md)
- [GLM-智谱](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/glm-zhipu.md)
- [GLM](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/glm.md)
- [MiniMax](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/minimax-api.md)
- [MiniMax](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/minimax-api-by-minimax.md)
- [Vidu视频生成Prompt指南](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/vidu-video-generation-prompt-guide.md)
- [MiMo-小米](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/mimo.md)
- [Stepfun-阶跃星辰](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/stepfun.md)



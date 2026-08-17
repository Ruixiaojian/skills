# use cases

百炼平台提供覆盖文本、图像、视频、语音、[多模态](../concepts/multi-modal.md)及智能体工作流的全栈AI能力，支持从基础生成到复杂推理的多样化业务场景。开发者可通过统一API或低代码工具快速集成，结合模型调优、缓存优化、流控策略等工程实践，构建生产级AI应用。

## 支持的模型/功能

百炼平台支持两类核心能力：**原生模型服务**与**第三方模型集成**。

- **原生模型**：包括Qwen系列（如`qwen3.7-max`、`qwen3.5-omni-plus-realtime`）、万相（Wan2.7）文生图/文生视频、HappyHorse视频生成、Fun-ASR实时语音识别、Qwen-Audio语音合成等。这些模型深度适配百炼平台特性，支持显式缓存、WebRTC/AOQ实时协议、[多模态](../concepts/multi-modal.md)交互套件等专有功能 [原文标题](../../raw/model-user-guide/use-cases/best-practice-webrtc-omni-realtime.md)。

- **第三方模型**：通过OpenAI兼容接口或DashScope SDK接入DeepSeek、Kimi、GLM、MiniMax、MiMo、Stepfun等厂商模型。需注意地域限制（多数仅华北2可用）和下架计划（如`deepseek-v3`将于2026年10月10日下架）[原文标题](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/deepseek-api.md)。不同供应商模型能力存在差异，例如硅基流动版DeepSeek支持更长上下文，而阿里云百炼版支持联网搜索与上下文缓存 [原文标题](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/siliconflow-deepseek-api.md)。

> **注意**：文档23与文档27均提及Kimi和MiniMax模型下架时间，但文档23标注`Moonshot-Kimi-K2-Instruct`下架时间为2026年7月9日，文档27标注`MiniMax-M2.1`下架时间为2026年7月9日；而文档19、24、27中DeepSeek、GLM、MiniMax的下架时间均为2026年10月10日。该不一致需以控制台最新公告为准，建议开发者定期核查模型市场状态。

## 关键参数

不同模态任务依赖特定参数控制输出质量：

- **文生文（LLM）**：`prompt`为核心输入，推荐使用结构化框架（背景/目的/风格/语气/受众/输出）提升可控性；支持`enable_thinking`（DeepSeek/Kimi等）、`reasoning_effort`（Kimi/GLM）等非标准参数开启思考链输出 [原文标题](../../raw/model-user-guide/use-cases/prompt-engineering-guide.md)。

- **文生图/图生图**：`prompt`（正向提示词）、`negative_prompt`（反向提示词）及`prompt_extend`（是否启用大模型智能改写，默认true）为关键参数 [原文标题](../../raw/model-user-guide/use-cases/text-to-image-prompt.md)。

- **文生视频/图生视频**：除基础`prompt`外，Vidu模型支持`动态控制`（大/中/小动态）、`运镜控制`（推/拉/固定镜头）及`导演风格`（宫崎骏/新海诚等）等细粒度参数 [原文标题](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/vidu-video-generation-prompt-guide.md)。

- **实时语音交互**：`turn_detection`参数决定轮次控制模式——`server_vad`（服务端自动检测）或`null`（客户端手动控制，需配合`input_audio_buffer.commit`）[原文标题](../../raw/model-user-guide/use-cases/use-aoq-to-access-qwen3-5-omni-plus-realtime-to-realize-key-voice-dialogue.md)。

## 使用方式

开发者可根据技术栈选择集成路径：

- **低代码编排**：通过“无限画布”可视化节点拖拽，集成Wan2.7图像生成与HappyHorse视频生成，实现影视创作全流程闭环 [原文标题](../../raw/model-user-guide/use-cases/infinite-canvas.md)。

- **SDK/API调用**：
  - 文本类任务：使用OpenAI兼容接口（需配置`base_url`为地域专属域名，如`https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`）或DashScope SDK。
  - [多模态](../concepts/multi-modal.md)/实时任务：优先选用AOQ Client SDK（Android/iOS/HarmonyOS），其分轨传输设计（Audio轨传音视频，Data轨传事件）显著降低延迟与带宽压力 [原文标题](../../raw/model-user-guide/use-cases/best-practice-aoq-omni-realtime.md)。
  - RAG应用：基于LlamaIndex集成百炼知识库服务，通过`DashScopeCloudIndex`创建索引，`DashScopeCloudRetriever`执行检索 [原文标题](../../raw/model-user-guide/use-cases/build-rag-applications-based-on-llamaindex.md)。

- **工程化实践**：
  - 缓存：对高频复用Prompt启用显式缓存（`cache_control`标记），可节省90%成本；Claude Code/OpenCode等工具原生支持 [原文标题](../../raw/model-user-guide/use-cases/explicit-cache-guide.md)。
  - 流控：针对`429`错误，优先尝试服务端排队等待（`X-DashScope-Wait-Timeout`请求头），再按需实施客户端令牌桶或架构层MQ削峰 [原文标题](../../raw/model-user-guide/use-cases/rate-limiting-best-practices.md)。

## 限制和注意事项

- **地域与权限约束**：第三方模型（DeepSeek/Kimi/GLM/MiniMax/MiMo/Stepfun）普遍仅支持华北2（北京）地域，且需对应地域的API Key；WebRTC方案要求浏览器麦克风/摄像头权限，并需后端代理SDP交换以规避CORS限制 [原文标题](../../raw/model-user-guide/use-cases/best-practice-webrtc-multimodal-dialog.md)。

- **资源与成本**：自定义模型训练需预估GPU资源消耗；函数计算部署方案虽免运维，但费用随调用量线性增长（如深度研究方案单次约6元）；显式缓存首次写入产生25%额外开销，需确保至少一次命中才具成本优势 [原文标题](../../raw/model-user-guide/use-cases/deep-research.md)。

- **模型演进风险**：第三方模型存在明确下架计划（如文档19、23、24、27所列），且不同供应商同名模型能力不一致（如`deepseek-v3.2`在硅基流动版支持`enable_thinking`，而阿里云百炼版未提及此参数）。开发者应避免硬编码模型名，优先通过模型市场API动态获取可用列表。

## 来源文档

- [HappyHorse 打造一站式影视创作平台](../../raw/model-user-guide/use-cases/infinite-canvas.md)
- [深度研究：生成你的独家洞察报告](../../raw/model-user-guide/use-cases/deep-research.md)
- [高效搭建 AI 智能体与工作流应用](../../raw/model-user-guide/use-cases/build-ai-applications-based-on-alibaba-cloud-model-studio.md)
- [文生图Prompt指南](../../raw/model-user-guide/use-cases/text-to-image-prompt.md)
- [文生视频/图生视频Prompt指南](../../raw/model-user-guide/use-cases/text-to-video-prompt.md)
- [基于LlamaIndex构建RAG应用](../../raw/model-user-guide/use-cases/build-rag-applications-based-on-llamaindex.md)
- [自定义模型调优、部署与评测](../../raw/model-user-guide/use-cases/model-training-best-practices.md)
- [借助大模型将文档转换为视频](../../raw/model-user-guide/use-cases/use-llm-to-convert-document-to-video.md)
- [限流应对最佳实践 ](../../raw/model-user-guide/use-cases/rate-limiting-best-practices.md)
- [显式缓存最佳实践](../../raw/model-user-guide/use-cases/explicit-cache-guide.md)
- [文生文Prompt指南](../../raw/model-user-guide/use-cases/prompt-engineering-guide.md)
- [通过WebRTC使用qwen3.5-omni-plus-realtime实现实时通话](../../raw/model-user-guide/use-cases/best-practice-webrtc-omni-realtime.md)
- [通过WebRTC使用多模态交互套件实现实时通话](../../raw/model-user-guide/use-cases/best-practice-webrtc-multimodal-dialog.md)
- [使用 AOQ 接入 qwen3.5-omni-plus-realtime 实现按键语音对话](../../raw/model-user-guide/use-cases/use-aoq-to-access-qwen3-5-omni-plus-realtime-to-realize-key-voice-dialogue.md)
- [通过AOQ使用qwen3.5-omni-plus-realtime实现实时通话](../../raw/model-user-guide/use-cases/best-practice-aoq-omni-realtime.md)
- [使用 AOQ 接入 qwen-audio-3.0-realtime-plus 实现实时语音对话](../../raw/model-user-guide/use-cases/real-time-voice-conversation-using-aoq-access-qwen-audio-3-0-realtime-plus.md)
- [使用 AOQ 接入 qwen-audio-3.0-tts-flash 实现语音合成](../../raw/model-user-guide/use-cases/speech-synthesis-using-aoq-access-qwen-audio-3-0-tts-flash.md)
- [使用 AOQ 接入 fun-asr-realtime 实现实时语音识别](../../raw/model-user-guide/use-cases/real-time-speech-recognition-using-aoq-access-fun-asr-realtime.md)
- [DeepSeek-阿里云](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/deepseek-api.md)
- [DeepSeek-硅基流动](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/siliconflow-deepseek-api.md)
- [DeepSeek](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/deepseek-api-by-vanchin.md)
- [Kimi-月之暗面](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/kimi-api-by-moonshot-ai.md)
- [Kimi](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/kimi-api.md)
- [GLM](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/glm.md)
- [MiniMax](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/minimax-api-by-minimax.md)
- [GLM-智谱](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/glm-zhipu.md)
- [MiniMax](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/minimax-api.md)
- [Vidu视频生成Prompt指南](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/vidu-video-generation-prompt-guide.md)
- [MiMo-小米](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/mimo.md)
- [Stepfun-阶跃星辰](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/stepfun.md)



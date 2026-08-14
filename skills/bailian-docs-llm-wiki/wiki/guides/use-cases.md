# use cases

百炼平台提供覆盖文本、图像、视频、语音、多模态等全栈能力的模型服务与工程化工具，支持从 Prompt 工程、RAG 构建、智能体编排到实时音视频交互的多样化生产级用例。所有方案均基于函数计算、知识库、AOQ 等标准化基础设施，开箱即用，按需付费，面向开发者提供可复用、可扩展、可监控的落地路径。

## 支持的模型/功能

百炼支持两类核心能力：**原生模型服务**与**第三方模型集成**。

- **原生模型**：包括 Qwen 系列（如 `qwen3-vl-plus` 用于解题批改 [AI 解题 + 批改：推动课程教学智变](../../raw/model-user-guide/use-cases/ai-homework-helper.md)）、Wan2.7 / HappyHorse（用于影视创作全流程 [HappyHorse 打造一站式影视创作平台](../../raw/model-user-guide/use-cases/infinite-canvas.md)）、Qwen-Deep-Research（用于深度情报分析）、qwen3.5-omni-plus-realtime（用于 WebRTC 实时对话）等。
  
- **第三方模型**：通过 [OpenAI 兼容接口](../concepts/openai-compatible-api.md)或 DashScope SDK 接入 DeepSeek（硅基流动/万擎双源）、Kimi（月之暗面）、GLM（智谱）、MiniMax、MiMo（小米）、Stepfun、Vidu 等。所有第三方模型均需在华北2（北京）地域开通并使用专属业务空间域名（如 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com`），且部分模型存在明确下架时间（如 GLM-4.6/4.7 将于 2026年10月10日下架 [GLM](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/glm.md)）。

> **注意**：文档 20（DeepSeek-硅基流动）与文档 21（DeepSeek-万擎）均声明仅支持华北2（北京）地域，但文档 31（DeepSeek-阿里云）明确列出美国、新加坡、德国、日本等多地接入地址；实际部署时应以控制台可用模型列表及限流文档为准，避免因地域配置错误导致调用失败。

## 关键参数

不同模态任务依赖特定参数组合，需严格遵循 API 规范：

- **文生文**：核心为 `prompt`，推荐使用结构化 Prompt 框架（背景/目的/风格/语气/受众/输出）提升可控性 [文生文Prompt指南](../../raw/model-user-guide/use-cases/prompt-engineering-guide.md)。
- **文生图/图生图**：`prompt`（正向描述）与 `negative_prompt`（排除项）为必需；V2 版本默认启用 `prompt_extend: true`（大模型智能扩写）。
- **文生视频/图生视频**：除基础 `prompt` 外，需显式指定运动、运镜、声音（人声/音效/BGM）或多镜头结构（含时间戳与分镜内容）[文生视频/图生视频Prompt指南](../../raw/model-user-guide/use-cases/text-to-video-prompt.md)。
- **实时语音交互（AOQ/WebRTC）**：关键参数包括 `turn_detection`（`server_vad`/`semantic_vad`/`null` 控制轮次模式）、`input_audio_buffer.commit`（Manual 模式必需）、`preserve_thinking`（Kimi 多轮思考传递）等。
- **第三方模型通用参数**：`enable_thinking`（开启思考模式）、`reasoning_effort`（控制推理深度）、`stream`（流式开关）均为非 OpenAI 标准字段，须通过 `extra_body`（Python SDK）或顶层参数（Node.js SDK）传入。

## 使用方式

典型工作流分为四类，均支持函数计算免运维部署：

1. **低代码编排**：通过无限画布节点式拖拽（图像生成+视频生成+剪辑）构建影视创作管线 [HappyHorse 打造一站式影视创作平台](../../raw/model-user-guide/use-cases/infinite-canvas.md)；或通过百炼流程编排引擎构建电商客服智能体（RAG/Agent/对话流）[高效搭建 AI 智能体与工作流应用](../../raw/model-user-guide/use-cases/build-ai-applications-based-on-alibaba-cloud-model-studio.md)。
2. **SDK 集成**：
   - RAG：使用 `llama-index-indices-managed-dashscope` 直接对接百炼知识库服务 [基于LlamaIndex构建RAG应用](../../raw/model-user-guide/use-cases/build-rag-applications-based-on-llamaindex.md)；
   - 多模态文档转视频：调用 Qwen-VL 解析文档、万相生成图片、TTS 合成语音、FFmpeg 合成最终视频 [借助大模型将文档转换为视频](../../raw/model-user-guide/use-cases/use-llm-to-convert-document-to-video.md)。
3. **实时交互协议**：
   - WebRTC：浏览器端直连，适用于低延迟音视频场景（需处理 CORS 代理）；
   - AOQ：移动端 SDK 接入，支持 Manual/VAD 模式切换、Data/Audio 分轨传输，适用于硬件终端（眼镜/机器人）[通过AOQ使用qwen3.5-omni-plus-realtime实现实时通话](../../raw/model-user-guide/use-cases/best-practice-aoq-omni-realtime.md)。
4. **缓存与流控**：
   - 显式缓存：通过 `cache_control` 标记 system/user message 实现确定性命中，适用于 Agent 长上下文管理 [显式缓存最佳实践](../../raw/model-user-guide/use-cases/explicit-cache-guide.md)；
   - 限流应对：优先采用服务端排队（`X-DashScope-Wait-Timeout` 头），其次客户端令牌桶/并发信号量，最后架构层 MQ 削峰 [限流应对最佳实践](../../raw/model-user-guide/use-cases/rate-limiting-best-practices.md)。

## 限制和注意事项

- **地域与模型绑定**：所有第三方模型（DeepSeek/Kimi/GLM/MiniMax/MiMo/Stepfun/Vidu）及部分原生模型（如 qwen3.5-omni-plus-realtime）仅在华北2（北京）地域可用，跨地域调用将失败。
- **API Key 安全**：严禁将 API Key 硬编码至客户端（iOS/Android/HarmonyOS App），必须通过业务 AppServer 代理鉴权并下发临时 [Token](../concepts/token.md) [使用 AOQ 接入 qwen3.5-omni-plus-realtime 实现按键语音对话](../../raw/model-user-guide/use-cases/use-aoq-to-access-qwen3-5-omni-plus-realtime-to-realize-key-voice-dialogue.md)。
- **资源约束**：
  - 文档解析：DashScopeParse 单文件 ≤100MB 且 ≤1000 页 [基于LlamaIndex构建RAG应用](../../raw/model-user-guide/use-cases/build-rag-applications-based-on-llamaindex.md)；
  - 视频生成：Vidu 对提示词长度与动态复杂度敏感，需避免主体分散、术语模糊 [Vidu视频生成Prompt指南](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/vidu-video-generation-prompt-guide.md)；
  - 实时语音：WebRTC 视频发送帧率建议降至 2fps 以保障弱网稳定性 [通过WebRTC使用qwen3.5-omni-plus-realtime实现实时通话](../../raw/model-user-guide/use-cases/best-practice-webrtc-omni-realtime.md)。
- **模型生命周期**：GLM-4.6/4.7、MiniMax-M2.1、Moonshot-Kimi-K2-Instruct 等模型已明确标注下架时间，迁移至 Qwen3 系列为官方推荐路径。

## 来源文档

- [HappyHorse 打造一站式影视创作平台](../../raw/model-user-guide/use-cases/infinite-canvas.md)
- [高效搭建 AI 智能体与工作流应用](../../raw/model-user-guide/use-cases/build-ai-applications-based-on-alibaba-cloud-model-studio.md)
- [AI 解题 + 批改：推动课程教学智变](../../raw/model-user-guide/use-cases/ai-homework-helper.md)
- [文生文Prompt指南](../../raw/model-user-guide/use-cases/prompt-engineering-guide.md)
- [文生图Prompt指南](../../raw/model-user-guide/use-cases/text-to-image-prompt.md)
- [文生视频/图生视频Prompt指南](../../raw/model-user-guide/use-cases/text-to-video-prompt.md)
- [基于LlamaIndex构建RAG应用](../../raw/model-user-guide/use-cases/build-rag-applications-based-on-llamaindex.md)
- [自定义模型调优、部署与评测](../../raw/model-user-guide/use-cases/model-training-best-practices.md)
- [借助大模型将文档转换为视频](../../raw/model-user-guide/use-cases/use-llm-to-convert-document-to-video.md)
- [深度研究：生成你的独家洞察报告](../../raw/model-user-guide/use-cases/deep-research.md)
- [限流应对最佳实践 ](../../raw/model-user-guide/use-cases/rate-limiting-best-practices.md)
- [显式缓存最佳实践](../../raw/model-user-guide/use-cases/explicit-cache-guide.md)
- [通过WebRTC使用多模态交互套件实现实时通话](../../raw/model-user-guide/use-cases/best-practice-webrtc-multimodal-dialog.md)
- [通过WebRTC使用qwen3.5-omni-plus-realtime实现实时通话](../../raw/model-user-guide/use-cases/best-practice-webrtc-omni-realtime.md)
- [通过AOQ使用qwen3.5-omni-plus-realtime实现实时通话](../../raw/model-user-guide/use-cases/best-practice-aoq-omni-realtime.md)
- [使用 AOQ 接入 qwen3.5-omni-plus-realtime 实现按键语音对话](../../raw/model-user-guide/use-cases/use-aoq-to-access-qwen3-5-omni-plus-realtime-to-realize-key-voice-dialogue.md)
- [使用 AOQ 接入 fun-asr-realtime 实现实时语音识别](../../raw/model-user-guide/use-cases/real-time-speech-recognition-using-aoq-access-fun-asr-realtime.md)
- [使用 AOQ 接入 qwen-audio-3.0-tts-flash 实现语音合成](../../raw/model-user-guide/use-cases/speech-synthesis-using-aoq-access-qwen-audio-3-0-tts-flash.md)
- [使用 AOQ 接入 qwen-audio-3.0-realtime-plus 实现实时语音对话](../../raw/model-user-guide/use-cases/real-time-voice-conversation-using-aoq-access-qwen-audio-3-0-realtime-plus.md)
- [DeepSeek-硅基流动](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/siliconflow-deepseek-api.md)
- [DeepSeek](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/deepseek-api-by-vanchin.md)
- [Kimi-月之暗面](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/kimi-api-by-moonshot-ai.md)
- [GLM](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/glm.md)
- [GLM-智谱](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/glm-zhipu.md)
- [MiniMax](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/minimax-api.md)
- [MiniMax](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/minimax-api-by-minimax.md)
- [Kimi](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/kimi-api.md)
- [MiMo-小米](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/mimo.md)
- [Stepfun-阶跃星辰](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/stepfun.md)
- [Vidu视频生成Prompt指南](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/vidu-video-generation-prompt-guide.md)
- [DeepSeek-阿里云](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/deepseek-api.md)



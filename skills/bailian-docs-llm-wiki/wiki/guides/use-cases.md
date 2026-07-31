# use cases

百炼平台提供覆盖文本、图像、视频、语音及多模态的全栈AI能力，支持从Prompt工程、RAG构建、智能体编排到实时音视频交互等多样化生产级用例。开发者可基于预置模型快速落地业务场景，也可通过自定义训练、第三方模型集成与缓存优化等机制实现深度定制。所有用例均依托统一API接口与计费体系，兼顾易用性与工程可控性。

## 支持的模型/功能

百炼平台支持两类核心模型能力：**阿里云自研模型**（如Qwen系列、Wan2.7、HappyHorse、qwen3.5-omni-plus-realtime）和**第三方直供模型**（如DeepSeek、Kimi、GLM、MiniMax、Stepfun、MiMo等）。其中，Qwen3-VL系列模型专用于多模态理解任务，已在[AI 解题 + 批改：推动课程教学智变](../../raw/model-user-guide/use-cases/ai-homework-helper.md)中验证其在MathVista、MMMU等评测中的SOTA表现；Wan2.7与HappyHorse则深度集成于影视创作场景，构成[HappyHorse 打造一站式影视创作平台](../../raw/model-user-guide/use-cases/infinite-canvas.md)的核心视觉引擎。

第三方模型接入遵循统一OpenAI兼容协议或DashScope SDK，但存在地域与功能差异：DeepSeek、Kimi、GLM、MiniMax、Stepfun、MiMo等均明确限定仅在华北2（北京）地域可用（见[DeepSeek-硅基流动](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/siliconflow-deepseek-api.md)、[Kimi-月之暗面](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/kimi-api-by-moonshot-ai.md)等文档），且部分模型（如kimi/kimi-k2.5）不支持`preserve_thinking`参数传递思考过程。> **注意**：文档16、19、21、23、25中关于模型下架时间的声明存在不一致——DeepSeek系列模型标注为2026年10月10日下架，而Kimi、GLM、MiniMax-M2.1均标注为2026年7月9日下架，需以百炼控制台实时公告为准。

## 关键参数

不同模态任务依赖特定参数控制生成质量：
- **文生文**：推荐使用结构化Prompt框架（背景/目的/风格/语气/受众/输出），并启用[文生文Prompt指南](../../raw/model-user-guide/use-cases/prompt-engineering-guide.md)中的自动优化工具；
- **文生图/图生图**：核心参数为`prompt`（正向提示词）与`negative_prompt`（反向提示词），V2版本支持`prompt_extend`智能扩写；
- **文生视频/图生视频**：除基础`prompt`外，wan2.7支持`shot_type`（已弃用）、多镜头时间戳标记及`sound_description`音频控制；
- **实时音视频**：WebRTC模式强制使用`server_vad`或`semantic_vad`语音活动检测，不支持手动VAD；
- **第三方模型**：通用非标准参数如`enable_thinking`、`reasoning_effort`需通过`extra_body`（Python OpenAI SDK）或顶层字段（Node.js）传入。

## 使用方式

典型工作流包含四类实践路径：
1. **开箱即用方案**：直接部署预置模板，如15分钟内完成[深度研究：生成你的独家洞察报告](../../raw/model-user-guide/use-cases/deep-research.md)的函数计算服务；
2. **低代码编排**：通过无限画布节点式拖拽（如[HappyHorse 打造一站式影视创作平台](../../raw/model-user-guide/use-cases/infinite-canvas.md)）或流程引擎（如AI电商客服助手）构建复杂工作流；
3. **SDK/API集成**：调用DashScope SDK或OpenAI兼容接口，配合显式缓存（`cache_control`）、限流控制（`X-DashScope-Wait-Timeout`）等高级特性；
4. **端侧嵌入**：通过AOQ Client SDK（Android/iOS/HarmonyOS）或WebRTC（浏览器）实现实时多模态交互，适用于AI眼镜、学习机等硬件场景。

## 限制和注意事项

- **地域与模型绑定**：所有第三方模型（DeepSeek/Kimi/GLM/MiniMax/Stepfun/MiMo）及部分实时模型（qwen3.5-omni-plus-realtime）仅支持华北2（北京）地域，跨地域调用将失败；
- **限流维度**：API受RPM（请求/分钟）、TPM（[Token](../concepts/token.md)/分钟）、RPS（请求/秒）、TPS（[Token](../concepts/token.md)/秒）及Traffic Burst（增速突增）五重限制，需结合[限流应对最佳实践](../../raw/model-user-guide/use-cases/rate-limiting-best-practices.md)设计客户端重试与服务端排队策略；
- **缓存确定性**：显式缓存（`cache_control`）仅对Anthropic协议接入的Agent/Coding工具（如Claude Code、OpenCode）原生支持，其他调用需手动注入标记；
- **文件处理约束**：DashScopeParse文档解析器要求单个PDF/DOC/DOCX文件≤100MB且≤1000页；
- **实时音视频权限**：WebRTC方案需用户主动授予麦克风/摄像头权限，且浏览器端SDP交换需后端代理规避CORS限制。

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
- [通过WebRTC使用qwen3.5-omni-plus-realtime实现实时通话](../../raw/model-user-guide/use-cases/best-practice-webrtc-omni-realtime.md)
- [通过AOQ使用qwen3.5-omni-plus-realtime实现实时通话](../../raw/model-user-guide/use-cases/best-practice-aoq-omni-realtime.md)
- [DeepSeek-阿里云](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/deepseek-api.md)
- [DeepSeek-硅基流动](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/siliconflow-deepseek-api.md)
- [DeepSeek](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/deepseek-api-by-vanchin.md)
- [Kimi](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/kimi-api.md)
- [Kimi-月之暗面](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/kimi-api-by-moonshot-ai.md)
- [GLM](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/glm.md)
- [GLM-智谱](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/glm-zhipu.md)
- [MiniMax](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/minimax-api-by-minimax.md)
- [Vidu视频生成Prompt指南](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/vidu-video-generation-prompt-guide.md)
- [MiniMax](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/minimax-api.md)
- [Stepfun-阶跃星辰](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/stepfun.md)
- [MiMo-小米](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/mimo.md)



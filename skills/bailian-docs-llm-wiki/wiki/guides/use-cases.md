# use cases

百炼平台提供覆盖文本、图像、视频、语音及多模态的全栈AI能力，支持从Prompt工程、RAG构建、智能体编排到端侧实时交互的完整开发链路。开发者可基于预置模型快速验证场景，也可通过自定义训练、第三方模型集成与缓存优化等手段深度适配业务需求。所有方案均以函数计算、知识库、WebRTC等标准化服务为底座，兼顾开箱即用性与生产级可扩展性。

## 支持的模型/功能

百炼平台支持两类核心模型能力：**阿里云自研模型**（如Qwen系列、Wan2.7、HappyHorse、Vidu）和**第三方直供模型**（如DeepSeek、Kimi、GLM、MiniMax、Stepfun、MiMo）。其中：

- **多模态视觉生成**：`Wan2.7`（文生/图生视频）、`HappyHorse`（长视频生成）、`Vidu`（高保真视频生成）构成统一视频能力矩阵，支持多镜头叙事、运镜控制与风格化输出 [原文标题](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/vidu-video-generation-prompt-guide.md)；  
- **大语言模型**：`qwen3-vl-plus` 专用于教育解题与批改场景，具备MathVista/MMMU SOTA级多模态推理能力 [原文标题](../../raw/model-user-guide/use-cases/ai-homework-helper.md)；`qwen3.5-omni-plus-realtime` 支持WebRTC低延迟音视频通话，内置服务端VAD与回声消除；  
- **第三方模型集成**：DeepSeek（v3/v4-pro）、Kimi（k3/k2.7-code）、GLM（5.2）、MiniMax（M2.7）、Stepfun（step-3.7-flash）、MiMo（v2.5-pro）均通过OpenAI兼容接口或DashScope SDK接入，全部支持`enable_thinking`或`reasoning_effort`参数控制思考模式 [原文标题](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/deepseek-api-by-vanchin.md)；  
- **检索增强与智能体**：`Qwen-Max`等模型可与LlamaIndex深度集成，构建RAG应用；同时支持通过节点式编排（如无限画布）或流程引擎构建自主决策Agent。

> **注意**：文档中提及的`deepseek-v3`等模型将于2026年10月10日下架，`kimi-k2-instruct`等将于2026年7月9日下架，官方明确推荐迁移至`qwen3.7-plus`等Qwen系列模型，需在新项目中优先选用。

## 关键参数

不同模型类型对应关键参数存在显著差异，开发者需严格按规范配置：

- **文生图（万相）**：`prompt`（正向提示词）、`negative_prompt`（反向提示词）、`prompt_extend`（是否启用大模型智能改写，默认`true`）；  
- **文生/图生视频（Wan2.7/HappyHorse）**：除基础`prompt`外，支持`shot_type`（单/多镜头）、`sound_description`（人声/音效/BGM）、`reference_image`（参考图编号）等结构化参数；  
- **第三方模型（DeepSeek/Kimi/GLM等）**：非标准参数需通过`extra_body`（Python OpenAI SDK）或顶层字段（Node.js SDK）传入，如`{"enable_thinking": true, "reasoning_effort": "max"}`；  
- **限流与缓存**：`X-DashScope-Wait-Timeout`（服务端排队等待秒数）、`cache_control`（显式缓存标记，需配合Anthropic协议端点使用）；  
- **实时通话（WebRTC）**：`server_vad`（服务端语音活动检测）、`sendFps`（视频发送帧率，建议2fps以平衡带宽与效果）。

## 使用方式

典型开发路径遵循“准备→调用→编排→优化”四阶段：

1. **环境准备**：获取API Key并配置至环境变量；开通对应模型服务（如[HappyHorse视频生成](https://bailian.console.aliyun.com/?tab=model#/model-market/detail/happyhorse)）；第三方模型需在控制台单独开通（如[DeepSeek硅基流动版](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/siliconflow-deepseek-api.md)）；  
2. **基础调用**：使用OpenAI SDK或DashScope SDK发起请求，注意地域Endpoint（如华北2需替换`{WorkspaceId}`）；视频类任务需构造符合[文生视频Prompt指南](../../raw/model-user-guide/use-cases/text-to-video-prompt.md)的结构化提示词；  
3. **高级编排**：  
   - 构建RAG应用：通过`DashScopeParse`解析PDF/DOCX，用`LlamaIndex`创建知识库索引，并绑定`Qwen-Max`作为LLM；  
   - 搭建智能体：利用无限画布节点式编排，将文本生成、图像生成、视频生成串联为影视创作流水线；  
   - 实时交互：WebRTC模式下需创建`RTCPeerConnection`，添加媒体轨道，并通过DataChannel传输事件；  
4. **性能优化**：  
   - 启用显式缓存：对高频复用Prompt（如Agent系统提示词）添加`cache_control={"type": "ephemeral"}`；  
   - 应对限流：突发流量优先配置`X-DashScope-Wait-Timeout: 30`，长文本处理需同时限制RPM与TPM（双重令牌桶）；  
   - 成本控制：函数计算部署方案（如[AI解题助手](../../raw/model-user-guide/use-cases/ai-homework-helper.md)）按量付费，单次体验成本低于1元。

## 限制和注意事项

- **地域与模型绑定**：所有第三方模型（DeepSeek/Kimi/GLM/MiniMax/Stepfun/MiMo）仅支持华北2（北京）地域，且必须使用业务空间专属域名`https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com`，旧域名`dashscope.aliyuncs.com`性能与稳定性较低；  
- **输入格式约束**：`DashScopeParse`解析PDF/DOCX文件时，单个文件≤100MB且≤1000页；WebRTC视频采集需通过Canvas降帧（如2fps），避免直接传输原始摄像头流；  
- **协议兼容性**：显式缓存仅在Anthropic协议端点（`/apps/anthropic`）生效，OpenAI兼容端点不支持；`cache_control`标记需置于system [prompt](prompt.md)或最近user message中；  
- **模型生命周期**：第三方模型存在明确下架时间（如DeepSeek系列2026-10-10），开发者应定期检查[模型市场](https://bailian.console.aliyun.com/?tab=model#/model-market)状态，避免线上服务中断；  
- **安全合规**：训练数据需完成脱敏处理（移除PII信息），知识库上传前应校验内容合规性；实时通话场景需在App中显式申请麦克风/摄像头运行时权限。

## 来源文档

- [HappyHorse 打造一站式影视创作平台](../../raw/model-user-guide/use-cases/infinite-canvas.md)
- [高效搭建 AI 智能体与工作流应用](../../raw/model-user-guide/use-cases/build-ai-applications-based-on-alibaba-cloud-model-studio.md)
- [AI 解题 + 批改：推动课程教学智变](../../raw/model-user-guide/use-cases/ai-homework-helper.md)
- [深度研究：生成你的独家洞察报告](../../raw/model-user-guide/use-cases/deep-research.md)
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
- [MiniMax](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/minimax-api.md)
- [MiniMax](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/minimax-api-by-minimax.md)
- [Vidu视频生成Prompt指南](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/vidu-video-generation-prompt-guide.md)
- [Stepfun-阶跃星辰](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/stepfun.md)
- [MiMo-小米](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/mimo.md)



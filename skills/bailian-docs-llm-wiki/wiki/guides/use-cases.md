# use cases

百炼平台的 use cases 覆盖从[多模态](../concepts/multi-modal.md)内容生成、智能体构建、深度研究到教育辅助等全场景 AI 应用。这些方案均基于百炼托管的模型服务（如 Qwen 系列、Wan2.7、HappyHorse）或第三方直供模型（如 DeepSeek、Kimi），通过标准化 API、Prompt 工程与工作流编排能力，帮助开发者快速落地生产级应用。核心价值在于降低大模型集成门槛，同时提供可扩展的工程化支撑。

## 支持的模型/功能

百炼支持两类模型接入方式：  
- **原生模型**：Qwen 系列（`qwen3-vl-plus`、`qwen3.7-max`、`qwen3.5-omni-plus-realtime`）、Wan2.7（文生图/视频）、HappyHorse（视频生成）、Qwen-Deep-Research 等专有模型，具备开箱即用的[多模态](../concepts/multi-modal.md)理解与生成能力。例如，[AI 解题 + 批改：推动课程教学智变](../../raw/model-user-guide/use-cases/ai-homework-helper.md) 方案即依赖 `qwen3-vl-plus` 实现图像解析与多学科解题。  
- **第三方直供模型**：通过百炼统一接入 DeepSeek（`deepseek-v4-pro`）、Kimi（`kimi/kimi-k3`）、GLM（`ZHIPU/GLM-5.2`）、MiniMax（`MiniMax/MiniMax-M2.7`）、MiMo（`xiaomi/mimo-v2.5-pro`）、Step（`stepfun/step-3.7-flash`）等，支持 [OpenAI 兼容接口](../concepts/openai-compatible-api.md)与 DashScope SDK。需注意地域限制——所有第三方直供模型（如 [DeepSeek-硅基流动](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/siliconflow-deepseek-api.md)、[Kimi-月之暗面](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/kimi-api-by-moonshot-ai.md)）仅在华北2（北京）地域可用，且必须使用该地域的 API Key。  

> **注意**：多个文档对同一模型的下架时间表述不一致。[DeepSeek-阿里云](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/deepseek-api.md) 和 [GLM](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/glm.md) 均标注下架时间为 2026年10月10日；而 [Kimi](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/kimi-api.md) 和 [MiniMax](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/minimax-api.md) 则标注为 2026年7月9日。请以控制台实时公告为准，推荐优先迁移至 Qwen 系列模型。

## 关键参数

不同任务类型对应关键参数组合：  
- **文本生成**：`model`（指定模型名）、`messages`（对话历史）、`stream`（流式开关）、`extra_body`（非标准参数，如 `enable_thinking` 或 `reasoning_effort`）。例如，调用 Kimi 的思考模式需通过 `extra_body={"reasoning_effort": "max"}`。  
- **文生图/视频**：`prompt`（正向提示词）、`negative_prompt`（反向提示词）、`prompt_extend`（是否启用智能改写，默认 `true`）。[文生图Prompt指南](../../raw/model-user-guide/use-cases/text-to-image-prompt.md) 明确指出该参数仅适用于 Wan2.7 V2 版本。  
- **实时音视频通话**：`server_vad`（服务端语音活动检测）、`audio_format`（音频编码格式）。WebRTC 模式强制使用 UDP 传输，不支持手动 VAD 模式。  
- **缓存与限流**：`cache_control`（显式缓存标记）、`X-DashScope-Wait-Timeout`（服务端排队等待头）。后者仅对 `Throttling.BurstRate` 类型限流生效，对 RPM/TPM 绝对值限流无效。

## 使用方式

典型集成路径分为三层：  
1. **基础调用**：通过 [OpenAI 兼容接口](../concepts/openai-compatible-api.md)或 DashScope SDK 直接请求。需配置 `base_url`（如 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`）并传入 `model` 名称。  
2. **工作流编排**：利用百炼可视化节点（如 [HappyHorse 打造一站式影视创作平台](../../raw/model-user-guide/use-cases/infinite-canvas.md) 中的“AI 导演”引擎）或代码化流程（如 LlamaIndex RAG 应用中的 `DashScopeCloudIndex`）串联多模型任务。  
3. **工程化部署**：结合函数计算（FC）构建无服务器后端，如 [深度研究：生成你的独家洞察报告](../../raw/model-user-guide/use-cases/deep-research.md) 方案所示，将模型服务封装为 Web API，实现弹性伸缩与按量付费。

## 限制和注意事项

- **地域与权限约束**：第三方直供模型（DeepSeek、Kimi、GLM、MiniMax、MiMo、Step）均强制要求华北2（北京）地域 API Key 及业务空间 ID；WebRTC 实时通话需浏览器麦克风/摄像头权限，且 SDP 交换需后端代理规避 CORS 限制。  
- **限流维度**：百炼 API 同时限制请求数（RPM/RPS）和 [Token](../concepts/token.md) 用量（TPM/TPS），突发流量（Traffic Burst）触发时推荐首选 `X-DashScope-Wait-Timeout` 头而非简单重试。  
- **缓存适用性**：显式缓存仅对 `cache_control` 标记的请求生效，且需确保输入内容确定性；Agent 场景中动态 system [prompt](prompt.md)（如 Claude Code 默认包含 git 状态）会降低跨会话命中率，建议启用 `--exclude-dynamic-system-prompt-sections` 参数。  
- **模型能力边界**：Wan2.7 文生视频 API 不再支持 `shot_type` 参数控制单/多镜头，需改用多镜头公式描述；Vidu 视频生成中“大动态”等关键词仅对特定模型生效，需查阅 [Vidu视频生成Prompt指南](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/vidu-video-generation-prompt-guide.md) 的适用模型列表。

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
- [DeepSeek-硅基流动](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/siliconflow-deepseek-api.md)


